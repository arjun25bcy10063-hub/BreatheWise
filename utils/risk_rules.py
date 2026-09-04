from typing import Optional


def aqi_points(aqi: Optional[float]) -> int:
    if aqi is None:
        return 10
    aqi = float(aqi)
    if aqi <= 50:
        return 5
    if aqi <= 100:
        return 15
    if aqi <= 150:
        return 30
    if aqi <= 200:
        return 45
    if aqi <= 300:
        return 60
    return 70


def heat_points(temp_c: Optional[float], humidity: Optional[float]) -> int:
    if temp_c is None:
        return 5
    temp = float(temp_c)
    humidity = 50 if humidity is None else float(humidity)
    score = 0
    if temp >= 40:
        score += 25
    elif temp >= 35:
        score += 18
    elif temp >= 32:
        score += 10
    elif temp <= 5:
        score += 12
    if humidity >= 80 and temp >= 30:
        score += 8
    elif humidity >= 70 and temp >= 30:
        score += 4
    return min(score, 30)


def uv_points(uv: Optional[float]) -> int:
    if uv is None:
        return 2
    uv = float(uv)
    if uv >= 11:
        return 10
    if uv >= 8:
        return 8
    if uv >= 6:
        return 6
    if uv >= 3:
        return 3
    return 1


def sensitivity_points(health_sensitivity: str) -> int:
    mapping = {
        "None": 0,
        "Allergies": 5,
        "Respiratory sensitivity": 8,
        "Asthma": 10,
        "Heart sensitivity": 10,
    }
    return mapping.get(health_sensitivity, 0)


def age_points(age_group: str) -> int:
    return {"Child": 6, "Adult": 0, "Senior": 7}.get(age_group, 0)


def exposure_points(occupation: str, aqi: Optional[float]) -> int:
    outdoor = occupation in {"Outdoor worker", "Delivery worker", "Athlete"}
    if not outdoor:
        return 2
    if aqi is None:
        return 7
    aqi = float(aqi)
    if aqi >= 200:
        return 15
    if aqi >= 150:
        return 12
    if aqi >= 100:
        return 8
    return 4


def risk_level(score: int) -> str:
    if score < 30:
        return "Low"
    if score < 55:
        return "Moderate"
    if score < 75:
        return "High"
    return "Very High"
