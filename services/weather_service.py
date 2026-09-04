import requests

from models.schemas import WeatherData
from utils.constants import REQUEST_TIMEOUT
from utils.validators import validate_coordinates

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

CURRENT_VARIABLES = [
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "wind_speed_10m",
    "wind_gusts_10m",
    "precipitation",
    "weather_code",
    "uv_index",
]

DAILY_VARIABLES = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "uv_index_max",
]


def get_weather(latitude: float, longitude: float, forecast_days: int = 7) -> WeatherData:
    validate_coordinates(latitude, longitude)
    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(CURRENT_VARIABLES),
            "daily": ",".join(DAILY_VARIABLES),
            "forecast_days": forecast_days,
            "timezone": "auto",
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    daily = data.get("daily", {})
    daily_rows = []
    times = daily.get("time", [])
    for i, day in enumerate(times):
        daily_rows.append(
            {
                "date": day,
                "weather_code": _at(daily, "weather_code", i),
                "temperature_max": _at(daily, "temperature_2m_max", i),
                "temperature_min": _at(daily, "temperature_2m_min", i),
                "precipitation": _at(daily, "precipitation_sum", i),
                "uv_max": _at(daily, "uv_index_max", i),
            }
        )

    return WeatherData(
        time=current.get("time", ""),
        temperature_c=current.get("temperature_2m"),
        apparent_temperature_c=current.get("apparent_temperature"),
        humidity_pct=current.get("relative_humidity_2m"),
        wind_speed_kmh=current.get("wind_speed_10m"),
        wind_gusts_kmh=current.get("wind_gusts_10m"),
        precipitation_mm=current.get("precipitation"),
        weather_code=current.get("weather_code"),
        uv_index=current.get("uv_index"),
        daily=daily_rows,
    )


def _at(data, key, index):
    values = data.get(key, [])
    return values[index] if index < len(values) else None
