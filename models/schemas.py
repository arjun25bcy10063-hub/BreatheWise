from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class LocationData:
    name: str
    latitude: float
    longitude: float
    country: str = ""
    timezone: str = ""


@dataclass
class UserProfile:
    user_id: int = 1
    age_group: str = "Adult"
    health_sensitivity: str = "None"
    occupation: str = "Indoor worker"
    location_name: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class WeatherData:
    time: str
    temperature_c: Optional[float] = None
    apparent_temperature_c: Optional[float] = None
    humidity_pct: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    wind_gusts_kmh: Optional[float] = None
    precipitation_mm: Optional[float] = None
    weather_code: Optional[int] = None
    uv_index: Optional[float] = None
    daily: List[Dict] = field(default_factory=list)


@dataclass
class AQIData:
    time: str
    us_aqi: Optional[float] = None
    pm2_5: Optional[float] = None
    pm10: Optional[float] = None
    no2: Optional[float] = None
    ozone: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    hourly: List[Dict] = field(default_factory=list)


@dataclass
class RiskAssessment:
    overall_score: int
    overall_level: str
    air_risk: str
    weather_risk: str
    exposure_risk: str
    factors: List[str]
    explanation: str


@dataclass
class Advisory:
    summary: str
    actions: List[str]
    outdoor_guidance: str
    personalization_reason: str
    disclaimer: str


@dataclass
class Alert:
    risk_level: str
    title: str
    message: str
    timestamp: str
