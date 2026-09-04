import requests

from models.schemas import LocationData
from utils.constants import REQUEST_TIMEOUT

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def search_locations(query: str, count: int = 5):
    query = query.strip()
    if not query:
        return []

    response = requests.get(
        GEOCODING_URL,
        params={"name": query, "count": count, "language": "en", "format": "json"},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data.get("results", []):
        results.append(
            LocationData(
                name=item.get("name", "Unknown"),
                latitude=float(item["latitude"]),
                longitude=float(item["longitude"]),
                country=item.get("country", ""),
                timezone=item.get("timezone", ""),
            )
        )
    return results
