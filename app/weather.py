import httpx
from datetime import datetime, timedelta


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_hourly_forecast(latitude: float, longitude: float):
    """
    Fetch hourly forecast from Open-Meteo API.

    Returns:
        dict containing hourly time, precipitation probability, wind speed.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability,windspeed_10m,visibility",
        "timezone": "auto"
    }

    response = httpx.get(OPEN_METEO_URL, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch weather data")

    return response.json()


def extract_commute_window(hourly_data: dict, departure_time: str, duration_minutes: int):
    """
    Extract forecast values during the commute window.

    Example:
    Departure: 08:30
    Duration: 45 min
    Window covers: 08:00–09:00 hourly blocks
    """

    departure_dt = datetime.fromisoformat(departure_time)
    end_dt = departure_dt + timedelta(minutes=duration_minutes)

    times = hourly_data["time"]
    rain_probs = hourly_data["precipitation_probability"]
    wind_speeds = hourly_data["windspeed_10m"]
    visibility = hourly_data["visibility"]

    snapshot = []

    for i, t in enumerate(times):
        hour_dt = datetime.fromisoformat(t)

        start_hour = departure_dt.replace(minute=0, second=0)

        if start_hour <= hour_dt <= end_dt:
            snapshot.append({
                "time": hour_dt.strftime("%H:%M"),
                "rain_prob": rain_probs[i],
                "wind_kmh": wind_speeds[i],
                "visibility_m": visibility[i]
            })

    return snapshot
