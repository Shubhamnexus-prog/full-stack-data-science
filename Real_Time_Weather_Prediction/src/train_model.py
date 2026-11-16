
import json
import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
MODEL_FOLDER = PROJECT_ROOT / "models"
REPORT_FOLDER = PROJECT_ROOT / "reports"

MODEL_FOLDER.mkdir(exist_ok=True)
REPORT_FOLDER.mkdir(exist_ok=True)


def train_weather_model(city):

    city_slug = city.strip().lower().replace(" ", "_")

    data_path = DATA_FOLDER / f"{city_slug}_engineered.csv"

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    # Load engineered dataset
    df = pd.read_csv(data_path)

    print("\nDataset shape:", df.shape)

    # Separate features and target
    X = df.drop(columns=["target_temperature"])
    y = df["target_temperature"]

    # Chronological 80/20 split (no shuffling)
    split_index = int(len(df) * 0.80)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    print("\nTraining records:", len(X_train))
    print("Testing records:", len(X_test))

    # Create Random Forest model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    # Train
    print("\nTraining Random Forest model...")
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Evaluate
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\n========== MODEL EVALUATION ==========")
    print(f"MAE  : {mae:.3f} °C")
    print(f"RMSE : {rmse:.3f} °C")
    print(f"R2   : {r2:.4f}")

    # Save model and feature names
    model_path = MODEL_FOLDER / f"{city_slug}_random_forest.joblib"

    joblib.dump(
        {
            "model": model,
            "features": list(X.columns)
        },
        model_path
    )

    # Save metrics
    metrics = {
        "city": city,
        "model": "Random Forest",
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "training_records": len(X_train),
        "testing_records": len(X_test)
    }

    metrics_path = REPORT_FOLDER / f"{city_slug}_model_metrics.json"

    with open(metrics_path, "w") as file:
        json.dump(metrics, file, indent=4)

    print("\nModel saved:", model_path)
    print("Metrics saved:", metrics_path)

    # Show actual vs predicted
    results = pd.DataFrame({
        "Actual_Temperature": y_test.values,
        "Predicted_Temperature": predictions
    })

    results_path = REPORT_FOLDER / f"{city_slug}_predictions.csv"
    results.to_csv(results_path, index=False)

    print("Predictions saved:", results_path)


if __name__ == "__main__":
    city = input("Enter city name (Mumbai): ").strip()

    if not city:
        city = "Mumbai"

    train_weather_model(city)
