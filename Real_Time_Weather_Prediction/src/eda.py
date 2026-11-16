
import pandas as pd
import plotly.express as px
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "mumbai_historical_weather.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(exist_ok=True)


# Load dataset
df = pd.read_csv(DATA_PATH)

df["datetime"] = pd.to_datetime(df["datetime"])

print("\n========== DATASET INFORMATION ==========")

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\n========== STATISTICAL ANALYSIS ==========")

print(
    df[
        [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ]
    ].describe()
)

print("\n========== DATA QUALITY ==========")

print("Missing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print(
    "Duplicate timestamps:",
    df["datetime"].duplicated().sum()
)

# Check hourly gaps
time_diff = df["datetime"].sort_values().diff()

print(
    "\nNumber of gaps greater than one hour:",
    (time_diff > pd.Timedelta(hours=1)).sum()
)


# 1. Temperature trend
fig1 = px.line(
    df,
    x="datetime",
    y="temperature_2m",
    title="Mumbai Historical Hourly Temperature",
    labels={
        "datetime": "Date",
        "temperature_2m": "Temperature (°C)"
    }
)

fig1.write_html(REPORTS_DIR / "temperature_trend.html")


# 2. Humidity trend
fig2 = px.line(
    df,
    x="datetime",
    y="relative_humidity_2m",
    title="Mumbai Historical Humidity",
    labels={
        "datetime": "Date",
        "relative_humidity_2m": "Humidity (%)"
    }
)

fig2.write_html(REPORTS_DIR / "humidity_trend.html")


# 3. Temperature distribution
fig3 = px.histogram(
    df,
    x="temperature_2m",
    nbins=50,
    title="Temperature Distribution",
    labels={"temperature_2m": "Temperature (°C)"}
)

fig3.write_html(REPORTS_DIR / "temperature_distribution.html")


# 4. Monthly average temperature
df["month"] = df["datetime"].dt.month

monthly_data = (
    df.groupby("month", as_index=False)["temperature_2m"]
    .mean()
)

fig4 = px.bar(
    monthly_data,
    x="month",
    y="temperature_2m",
    title="Average Temperature by Month",
    labels={
        "month": "Month",
        "temperature_2m": "Average Temperature (°C)"
    }
)

fig4.write_html(REPORTS_DIR / "monthly_temperature.html")


print("\n========== EDA COMPLETED ==========")

print("Reports saved inside:", REPORTS_DIR)

print("\nGenerated files:")
print("- temperature_trend.html")
print("- humidity_trend.html")
print("- temperature_distribution.html")
print("- monthly_temperature.html")
