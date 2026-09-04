import requests

from models.schemas import AQIData
from utils.constants import REQUEST_TIMEOUT
from utils.validators import validate_coordinates

AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
AQI_HOURLY_VARIABLES = [
    "pm2_5",
    "pm10",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "us_aqi",
]


def get_air_quality(latitude: float, longitude: float, forecast_days: int = 7) -> AQIData:
    validate_coordinates(latitude, longitude)
    response = requests.get(
        AQI_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(AQI_HOURLY_VARIABLES),
            "forecast_days": forecast_days,
            "timezone": "auto",
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    rows = []
    for i, timestamp in enumerate(times):
        rows.append(
            {
                "time": timestamp,
                "us_aqi": _at(hourly, "us_aqi", i),
                "pm2_5": _at(hourly, "pm2_5", i),
                "pm10": _at(hourly, "pm10", i),
                "no2": _at(hourly, "nitrogen_dioxide", i),
                "ozone": _at(hourly, "ozone", i),
                "so2": _at(hourly, "sulphur_dioxide", i),
                "co": _at(hourly, "carbon_monoxide", i),
            }
        )

    current = rows[0] if rows else {}
    return AQIData(
        time=current.get("time", ""),
        us_aqi=current.get("us_aqi"),
        pm2_5=current.get("pm2_5"),
        pm10=current.get("pm10"),
        no2=current.get("no2"),
        ozone=current.get("ozone"),
        so2=current.get("so2"),
        co=current.get("co"),
        hourly=rows,
    )


def _at(data, key, index):
    values = data.get(key, [])
    return values[index] if index < len(values) else None
