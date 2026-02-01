"""
app/risk.py

This module contains the deterministic and explainable
Weather Risk Scoring Logic.

Risk Score Range:
0   = No risk
100 = Very high risk

Factors considered:
- AQI (Air Quality Index)
- Rain probability
- Wind speed
- Visibility
"""


def calculate_risk(snapshot, aqi=None):
    """
    Calculate commute weather risk score (0–100).

    Parameters:
    - snapshot: list of hourly weather points during commute window
    - aqi: optional AQI value (US AQI scale)

    Returns:
    - total_score (int)
    - breakdown (dict)
    - reasons (list of strings)
    """

    total_score = 0

 
    breakdown = {
        "AQI": 0,
        "rain": 0,
        "wind": 0,
        "visibility": 0
    }

    reasons = []


    if aqi is not None:
        if aqi >= 150:
            breakdown["AQI"] = 60
            total_score += 60
            reasons.append(f"Air quality is very unhealthy (AQI {aqi})")

        elif aqi >= 100:
            breakdown["AQI"] = 45
            total_score += 45
            reasons.append(f"Air quality is unhealthy (AQI {aqi})")

        elif aqi >= 50:
            breakdown["AQI"] = 15
            total_score += 15
            reasons.append(f"Air quality is moderate (AQI {aqi})")


    max_rain = max([h["rain_prob"] for h in snapshot])
    max_wind = max([h["wind_kmh"] for h in snapshot])
    min_visibility = min([h["visibility_m"] for h in snapshot])


    if max_rain > 60:
        breakdown["rain"] = 45
        total_score += 45
        reasons.append(f"High rain probability ({max_rain}%) during commute window")

    elif max_rain > 30:
        breakdown["rain"] = 20
        total_score += 20
        reasons.append(f"Moderate rain probability ({max_rain}%) during commute window")


    if max_wind > 25:
        breakdown["wind"] = 20
        total_score += 20
        reasons.append(f"Strong winds expected ({max_wind} km/h)")

    elif max_wind > 15:
        breakdown["wind"] = 10
        total_score += 10
        reasons.append(f"Moderate winds expected ({max_wind} km/h)")


    if min_visibility < 2000:
        breakdown["visibility"] = 10
        total_score += 10
        reasons.append(f"Low visibility ({min_visibility} m) during commute")

    
    if total_score > 100:
        total_score = 100

    if total_score == 0:
        reasons.append("No significant weather risks detected")

    return total_score, breakdown, reasons
