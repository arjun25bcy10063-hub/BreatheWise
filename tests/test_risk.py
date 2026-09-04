from agents.risk_agent import assess_risk
from models.schemas import AQIData, UserProfile, WeatherData


def test_high_risk_outdoor_sensitive_profile():
    weather = WeatherData(time="2026-09-04T12:00", temperature_c=38, humidity_pct=75, uv_index=9)
    aqi = AQIData(time="2026-09-04T12:00", us_aqi=180, pm2_5=100, pm10=150)
    profile = UserProfile(age_group="Senior", health_sensitivity="Asthma", occupation="Outdoor worker")
    result = assess_risk(weather, aqi, profile)
    assert result.overall_score >= 75
    assert result.overall_level == "Very High"


def test_low_risk_profile():
    weather = WeatherData(time="2026-09-04T12:00", temperature_c=24, humidity_pct=45, uv_index=2)
    aqi = AQIData(time="2026-09-04T12:00", us_aqi=35, pm2_5=8, pm10=12)
    profile = UserProfile(age_group="Adult", health_sensitivity="None", occupation="Indoor worker")
    result = assess_risk(weather, aqi, profile)
    assert result.overall_level == "Low"
