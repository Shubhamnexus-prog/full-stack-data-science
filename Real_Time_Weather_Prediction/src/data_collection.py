
import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import re


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_city_coordinates(city):

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        GEOCODING_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    results = response.json().get("results")

    if not results:
        raise ValueError(f"City not found: {city}")

    location = results[0]

    return location


def collect_historical_weather(city):

    location = get_city_coordinates(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Archive data can have a publication delay.
    end_date = date.today() - timedelta(days=6)

    # Collect approximately two years of data.
    start_date = end_date - timedelta(days=730)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "apparent_temperature",
            "precipitation",
            "surface_pressure",
            "cloud_cover",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m"
        ],
        "timezone": "auto"
    }

    print("\nDownloading historical weather data...")
    print("City:", location["name"])
    print("Country:", location.get("country"))
    print("Start date:", start_date)
    print("End date:", end_date)

    response = requests.get(
        HISTORICAL_URL,
        params=params,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    if "hourly" not in result:
        raise ValueError("Historical hourly data not available.")

    df = pd.DataFrame(result["hourly"])

    df.rename(columns={"time": "datetime"}, inplace=True)

    df["datetime"] = pd.to_datetime(df["datetime"])

    df["city"] = location["name"]
    df["country"] = location.get("country", "Unknown")

    # Arrange columns.
    first_columns = ["datetime", "city", "country"]

    remaining_columns = [
        col for col in df.columns
        if col not in first_columns
    ]

    df = df[first_columns + remaining_columns]

    # Create data folder if it does not exist.
    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    city_slug = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        location["name"].strip()
    ).strip("_").lower()

    file_path = data_folder / f"{city_slug}_historical_weather.csv"

    df.to_csv(file_path, index=False)

    print("\nHistorical data downloaded successfully!")

    print("\nDataset shape:", df.shape)

    print("\nFirst five records:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nSaved file:")
    print(file_path)

    return df


if __name__ == "__main__":

    city = input("Enter city name: ").strip()

    try:
        dataset = collect_historical_weather(city)

    except requests.RequestException as error:
        print("API connection error:", error)

    except Exception as error:
        print("Error:", error)
