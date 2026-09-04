from typing import Any, Dict


def validate_coordinates(latitude: float, longitude: float) -> None:
    if not -90 <= float(latitude) <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= float(longitude) <= 180:
        raise ValueError("Longitude must be between -180 and 180.")


def validate_non_negative(value: Any, field_name: str) -> None:
    if value is None:
        return
    if float(value) < 0:
        raise ValueError(f"{field_name} cannot be negative.")


def validate_profile(profile: Dict[str, Any]) -> None:
    required = ["age_group", "health_sensitivity", "occupation"]
    for field in required:
        if not str(profile.get(field, "")).strip():
            raise ValueError(f"{field} is required.")


def validate_advisory(advisory: Dict[str, Any]) -> bool:
    required = ["summary", "actions", "outdoor_guidance", "personalization_reason"]
    return all(advisory.get(key) for key in required)
