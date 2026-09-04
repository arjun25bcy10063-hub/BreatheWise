def number_or_dash(value, suffix="", decimals=0):
    if value is None:
        return "—"
    if decimals == 0:
        return f"{round(float(value))}{suffix}"
    return f"{float(value):.{decimals}f}{suffix}"


def aqi_label(aqi):
    if aqi is None:
        return "Unavailable"
    aqi = float(aqi)
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def risk_badge(level):
    return level.upper()
