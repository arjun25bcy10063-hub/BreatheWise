import json
import os
from typing import Dict

from models.schemas import Advisory, AQIData, RiskAssessment, UserProfile, WeatherData
from utils.constants import AI_MODEL
from utils.validators import validate_advisory


SYSTEM_INSTRUCTIONS = """
You create concise environmental health guidance.
Use only the supplied data.
Do not diagnose illness.
Do not prescribe medication.
Do not tell the user to stop prescribed treatment.
Do not invent measurements.
Use cautious, practical language.
Return valid JSON with keys:
summary, actions, outdoor_guidance, personalization_reason
""".strip()


def generate_advisory(weather: WeatherData, aqi: AQIData, risk: RiskAssessment, profile: UserProfile) -> Advisory:
    api_key = os.getenv("AI_API_KEY", "").strip()
    if not api_key:
        return _fallback_advisory(risk, profile)

    prompt = {
        "location": profile.location_name,
        "profile": {
            "age_group": profile.age_group,
            "health_sensitivity": profile.health_sensitivity,
            "occupation": profile.occupation,
        },
        "weather": {
            "temperature_c": weather.temperature_c,
            "apparent_temperature_c": weather.apparent_temperature_c,
            "humidity_pct": weather.humidity_pct,
            "wind_speed_kmh": weather.wind_speed_kmh,
            "uv_index": weather.uv_index,
            "precipitation_mm": weather.precipitation_mm,
        },
        "air_quality": {
            "us_aqi": aqi.us_aqi,
            "pm2_5": aqi.pm2_5,
            "pm10": aqi.pm10,
            "no2": aqi.no2,
            "ozone": aqi.ozone,
            "so2": aqi.so2,
            "co": aqi.co,
        },
        "risk": {
            "score": risk.overall_score,
            "level": risk.overall_level,
            "air_risk": risk.air_risk,
            "weather_risk": risk.weather_risk,
            "exposure_risk": risk.exposure_risk,
            "factors": risk.factors,
        },
    }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=f"{SYSTEM_INSTRUCTIONS}\n\nDATA:\n{json.dumps(prompt, indent=2)}",
        )
        parsed = _extract_json(getattr(response, "text", ""))
        if not validate_advisory(parsed):
            return _fallback_advisory(risk, profile)
        actions = parsed.get("actions", [])
        if isinstance(actions, str):
            actions = [actions]
        return Advisory(
            summary=str(parsed["summary"]),
            actions=[str(item) for item in actions[:3]],
            outdoor_guidance=str(parsed["outdoor_guidance"]),
            personalization_reason=str(parsed["personalization_reason"]),
            disclaimer="This is environmental guidance, not a medical diagnosis.",
        )
    except Exception:
        return _fallback_advisory(risk, profile)


def _extract_json(text: str) -> Dict:
    text = (text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {}


def _fallback_advisory(risk: RiskAssessment, profile: UserProfile) -> Advisory:
    actions = [
        "Check the latest local air-quality and weather conditions before going outdoors.",
        "Reduce prolonged outdoor exposure when the risk level is high.",
        "Use your usual personal health plan and seek professional help for concerning symptoms.",
    ]
    if profile.occupation in {"Outdoor worker", "Delivery worker", "Athlete"}:
        actions[1] = "Take regular breaks in cleaner or cooler indoor spaces when conditions are unfavorable."
    return Advisory(
        summary=f"Current environmental risk is {risk.overall_level.lower()} for your profile.",
        actions=actions,
        outdoor_guidance="Outdoor activity should be adjusted to the current conditions and your personal situation.",
        personalization_reason=risk.explanation,
        disclaimer="This is environmental guidance, not a medical diagnosis.",
    )
