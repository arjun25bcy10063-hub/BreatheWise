from services.aqi_service import _at as aqi_at
from services.weather_service import _at as weather_at


def test_weather_at():
    assert weather_at({"x": [1, 2]}, "x", 1) == 2
    assert weather_at({"x": [1]}, "x", 2) is None


def test_aqi_at():
    assert aqi_at({"x": [3]}, "x", 0) == 3
