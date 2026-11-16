
import pandas as pd
import numpy as np
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"


def create_features(city):

    city_slug = city.strip().lower().replace(" ", "_")

    input_file = DATA_FOLDER / f"{city_slug}_historical_weather.csv"

    if not input_file.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_file}"
        )

    df = pd.read_csv(input_file)

    df["datetime"] = pd.to_datetime(df["datetime"])

    df = df.sort_values("datetime").reset_index(drop=True)

    # Ensure observations are hourly and continuous.
    if df["datetime"].duplicated().any():
        raise ValueError("Duplicate timestamps found.")

    if not df["datetime"].diff().dropna().eq(
        pd.Timedelta(hours=1)
    ).all():
        raise ValueError(
            "Missing or irregular hourly timestamps found."
        )

    print("Original dataset shape:", df.shape)

    # 1. Time features for the prediction hour.
    forecast_time = df["datetime"] + pd.Timedelta(hours=1)

    df["hour"] = forecast_time.dt.hour
    df["day_of_week"] = forecast_time.dt.dayofweek
    df["month"] = forecast_time.dt.month
    df["day_of_year"] = forecast_time.dt.dayofyear

    # Cyclical encoding: hour.
    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )

    # Cyclical encoding: day of week.
    df["day_sin"] = np.sin(
        2 * np.pi * df["day_of_week"] / 7
    )

    df["day_cos"] = np.cos(
        2 * np.pi * df["day_of_week"] / 7
    )

    # Cyclical encoding: month.
    df["month_sin"] = np.sin(
        2 * np.pi * (df["month"] - 1) / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * (df["month"] - 1) / 12
    )

    # 2. Temperature lag features.
    for lag in [1, 2, 3, 6, 12, 24, 48, 168]:

        df[f"temp_lag_{lag}"] = (
            df["temperature_2m"].shift(lag)
        )

    # 3. Rolling temperature features.
    # These include the current observation and earlier observations.
    for window in [6, 12, 24, 48]:

        df[f"temp_rolling_{window}"] = (
            df["temperature_2m"]
            .rolling(window=window)
            .mean()
        )

    # 4. Other weather features.
    # Convert wind direction to cyclical values.
    df["wind_direction_sin"] = np.sin(
        np.deg2rad(df["wind_direction_10m"])
    )

    df["wind_direction_cos"] = np.cos(
        np.deg2rad(df["wind_direction_10m"])
    )

    # 5. Prediction target: temperature one hour ahead.
    df["target_temperature"] = (
        df["temperature_2m"].shift(-1)
    )

    # 6. Remove columns that should not be model inputs.
    drop_columns = [
        "datetime",
        "city",
        "country",
        "hour",
        "day_of_week",
        "month",
        "day_of_year",
        "wind_direction_10m",
        "target_temperature"
    ]

    feature_columns = [
        column for column in df.columns
        if column not in drop_columns
    ]

    # Keep only features and target.
    final_df = df[
        feature_columns + ["target_temperature"]
    ].copy()

    # Remove rows affected by lag features or target shifting.
    final_df = final_df.dropna().reset_index(drop=True)

    # Save the engineered dataset.
    output_file = (
        DATA_FOLDER / f"{city_slug}_engineered.csv"
    )

    final_df.to_csv(output_file, index=False)

    print("\n========== FEATURE ENGINEERING COMPLETED ==========")

    print("Final dataset shape:", final_df.shape)

    print("\nFeatures:")
    print(feature_columns)

    print("\nTarget:")
    print("target_temperature")

    print("\nFirst five records:")
    print(final_df.head())

    print("\nMissing values:")
    print(final_df.isnull().sum().sum())

    print("\nSaved dataset:")
    print(output_file)

    return final_df


if __name__ == "__main__":

    city = input("Enter city name: ").strip()

    try:
        dataset = create_features(city)

    except Exception as error:
        print("Error:", error)
