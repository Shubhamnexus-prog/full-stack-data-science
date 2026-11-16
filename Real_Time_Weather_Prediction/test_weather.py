
from src.weather_api import (
    get_coordinates,
    get_current_weather,
    get_weather_description
)

city = input("Enter city name: ")

try:
    location = get_coordinates(city)

    print("\nLocation:", location["name"])
    print("Country:", location["country"])

    weather = get_current_weather(
        location["latitude"],
        location["longitude"]
    )

    current = weather["current"]

    print("\n----- CURRENT WEATHER -----")

    print("Temperature:",
          current["temperature_2m"], "°C")

    print("Feels Like:",
          current["apparent_temperature"], "°C")

    print("Humidity:",
          current["relative_humidity_2m"], "%")

    print("Wind Speed:",
          current["wind_speed_10m"], "km/h")

    print("Weather:",
          get_weather_description(current["weather_code"]))

    print("Observation Time:",
          current["time"])

except Exception as error:
    print("Error:", error)
