from models.schemas import AQIData, RiskAssessment, UserProfile, WeatherData
from utils.risk_rules import (
    age_points,
    aqi_points,
    exposure_points,
    heat_points,
    risk_level,
    sensitivity_points,
    uv_points,
)


def assess_risk(weather: WeatherData, aqi: AQIData, profile: UserProfile) -> RiskAssessment:
    air_score = aqi_points(aqi.us_aqi)
    heat_score = heat_points(weather.temperature_c, weather.humidity_pct)
    uv_score = uv_points(weather.uv_index)
    exposure_score = exposure_points(profile.occupation, aqi.us_aqi)
    sensitivity_score = sensitivity_points(profile.health_sensitivity)
    age_score = age_points(profile.age_group)

    total = min(100, round(air_score + heat_score + uv_score + exposure_score + sensitivity_score + age_score))
    level = risk_level(total)

    air_risk = _component_level(air_score, 70)
    weather_risk = _component_level(heat_score + uv_score, 38)
    exposure_risk = _component_level(exposure_score + sensitivity_score + age_score, 31)

    factors = []
    if aqi.us_aqi is not None and aqi.us_aqi > 100:
        factors.append("Elevated air pollution")
    if weather.temperature_c is not None and weather.temperature_c >= 35:
        factors.append("High temperature")
    if weather.humidity_pct is not None and weather.humidity_pct >= 70 and (weather.temperature_c or 0) >= 30:
        factors.append("High humidity with heat")
    if weather.uv_index is not None and weather.uv_index >= 6:
        factors.append("High UV exposure")
    if profile.occupation in {"Outdoor worker", "Delivery worker", "Athlete"}:
        factors.append("Frequent outdoor exposure")
    if profile.health_sensitivity != "None":
        factors.append("Higher sensitivity profile")
    if profile.age_group in {"Child", "Senior"}:
        factors.append("Age-related sensitivity factor")
    if not factors:
        factors.append("No major environmental stressors detected")

    explanation = _build_explanation(level, factors)
    return RiskAssessment(
        overall_score=total,
        overall_level=level,
        air_risk=air_risk,
        weather_risk=weather_risk,
        exposure_risk=exposure_risk,
        factors=factors,
        explanation=explanation,
    )


def _component_level(score: int, max_score: int) -> str:
    ratio = score / max_score if max_score else 0
    if ratio < 0.35:
        return "Low"
    if ratio < 0.65:
        return "Moderate"
    if ratio < 0.85:
        return "High"
    return "Very High"


def _build_explanation(level: str, factors) -> str:
    joined = ", ".join(factors[:4])
    return f"The current risk is {level.lower()} mainly because of {joined}."
