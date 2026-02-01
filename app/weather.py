"""
app/weather.py

Handles external weather + air quality integration.

Includes BONUS:
Weather API Caching (10 min TTL)
AQI (Air Quality Index) support
"""

import httpx
import time
from datetime import datetime, timedelta


OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


OPEN_METEO_AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

CACHE = {}
CACHE_TTL_SECONDS = 600  


def fetch_hourly_forecast(latitude: float, longitude: float):
    """
    Fetch hourly forecast from Open-Meteo.

    BONUS A:
    Forecast responses are cached per location for 10 minutes.

    Returns:
    - forecast_data (dict)
    - cache_status ("HIT" or "MISS")
    """

    cache_key = f"{round(latitude, 4)},{round(longitude, 4)}"
    now = time.time()

    if cache_key in CACHE:
        cached_data, timestamp = CACHE[cache_key]

        if now - timestamp < CACHE_TTL_SECONDS:
            print("Using cached weather forecast data")
            return cached_data, "HIT"

    print("Fetching fresh weather data from Open-Meteo...")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability,windspeed_10m,visibility",
        "timezone": "auto"
    }

    response = httpx.get(OPEN_METEO_FORECAST_URL, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch weather forecast")

    data = response.json()

    CACHE[cache_key] = (data, now)

    return data, "MISS"


def fetch_aqi(latitude: float, longitude: float):
    """
    Fetch Air Quality Index (US AQI) from Open-Meteo Air Quality API.

    Returns:
    - AQI value (int) or None if unavailable
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "us_aqi",
        "timezone": "auto"
    }

    response = httpx.get(OPEN_METEO_AQI_URL, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    try:
        return int(data["hourly"]["us_aqi"][0])
    except Exception:
        return None


def extract_commute_window(hourly_data: dict, departure_time: str, duration_minutes: int):
    """
    Extract hourly forecast values during the commute window.
    """

    departure_dt = datetime.fromisoformat(departure_time)
    end_dt = departure_dt + timedelta(minutes=duration_minutes)

    times = hourly_data["time"]
    rain_probs = hourly_data["precipitation_probability"]
    wind_speeds = hourly_data["windspeed_10m"]
    visibility = hourly_data["visibility"]

    snapshot = []


    start_hour = departure_dt.replace(minute=0, second=0)

    for i, t in enumerate(times):
        hour_dt = datetime.fromisoformat(t)

        if start_hour <= hour_dt <= end_dt:
            snapshot.append({
                "time": hour_dt.strftime("%H:%M"),
                "rain_prob": rain_probs[i],
                "wind_kmh": wind_speeds[i],
                "visibility_m": visibility[i]
            })

    return snapshot
