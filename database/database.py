import json
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from models.schemas import Advisory, Alert, AQIData, RiskAssessment, UserProfile, WeatherData
from utils.constants import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            age_group TEXT NOT NULL,
            health_sensitivity TEXT NOT NULL,
            occupation TEXT NOT NULL,
            location_name TEXT,
            latitude REAL,
            longitude REAL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS environmental_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            temperature_c REAL,
            humidity_pct REAL,
            uv_index REAL,
            wind_speed_kmh REAL,
            us_aqi REAL,
            pm2_5 REAL,
            pm10 REAL,
            no2 REAL,
            ozone REAL,
            so2 REAL,
            co REAL
        );
        CREATE TABLE IF NOT EXISTS risk_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            score INTEGER NOT NULL,
            level TEXT NOT NULL,
            factors TEXT NOT NULL,
            explanation TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS advisories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            summary TEXT NOT NULL,
            actions TEXT NOT NULL,
            outdoor_guidance TEXT NOT NULL,
            personalization_reason TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def save_profile(profile: UserProfile):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO users (user_id, age_group, health_sensitivity, occupation, location_name, latitude, longitude, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            age_group=excluded.age_group,
            health_sensitivity=excluded.health_sensitivity,
            occupation=excluded.occupation,
            location_name=excluded.location_name,
            latitude=excluded.latitude,
            longitude=excluded.longitude,
            updated_at=excluded.updated_at
        """,
        (
            profile.user_id,
            profile.age_group,
            profile.health_sensitivity,
            profile.occupation,
            profile.location_name,
            profile.latitude,
            profile.longitude,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_profile(user_id: int = 1) -> Optional[UserProfile]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return UserProfile(
        user_id=row["user_id"],
        age_group=row["age_group"],
        health_sensitivity=row["health_sensitivity"],
        occupation=row["occupation"],
        location_name=row["location_name"] or "",
        latitude=row["latitude"],
        longitude=row["longitude"],
    )


def save_snapshot(user_id: int, weather: WeatherData, aqi: AQIData, risk: RiskAssessment, advisory: Advisory):
    timestamp = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO environmental_readings
        (user_id, timestamp, temperature_c, humidity_pct, uv_index, wind_speed_kmh,
         us_aqi, pm2_5, pm10, no2, ozone, so2, co)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            timestamp,
            weather.temperature_c,
            weather.humidity_pct,
            weather.uv_index,
            weather.wind_speed_kmh,
            aqi.us_aqi,
            aqi.pm2_5,
            aqi.pm10,
            aqi.no2,
            aqi.ozone,
            aqi.so2,
            aqi.co,
        ),
    )
    conn.execute(
        "INSERT INTO risk_assessments (user_id, timestamp, score, level, factors, explanation) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, timestamp, risk.overall_score, risk.overall_level, json.dumps(risk.factors), risk.explanation),
    )
    conn.execute(
        "INSERT INTO advisories (user_id, timestamp, summary, actions, outdoor_guidance, personalization_reason) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, timestamp, advisory.summary, json.dumps(advisory.actions), advisory.outdoor_guidance, advisory.personalization_reason),
    )
    conn.commit()
    conn.close()


def save_alert(user_id: int, alert: Alert):
    conn = get_connection()
    conn.execute(
        "INSERT INTO alerts (user_id, timestamp, risk_level, title, message) VALUES (?, ?, ?, ?, ?)",
        (user_id, alert.timestamp, alert.risk_level, alert.title, alert.message),
    )
    conn.commit()
    conn.close()


def get_alert_history(user_id: int = 1, limit: int = 50) -> List[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM alerts WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return rows


def get_trend_data(user_id: int = 1, limit: int = 168) -> List[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM environmental_readings WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return rows


def get_latest_risk_score(user_id: int = 1):
    conn = get_connection()
    row = conn.execute(
        "SELECT score FROM risk_assessments WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1 OFFSET 1",
        (user_id,),
    ).fetchone()
    conn.close()
    return row["score"] if row else None
