"""
Risk Scoring Module
-------------------

Weather Risk Score: 0–100

Rules (deterministic + explainable):

+45 if rain probability > 60%
+20 if wind speed > 25 km/h
+10 if visibility < 2000 m
(max score capped at 100)

Returns:
- total score
- breakdown
- human-readable reasons
"""


def calculate_risk(hourly_snapshot: list):
    total_score = 0
    breakdown = {
        "rain": 0,
        "wind": 0,
        "visibility": 0
    }
    reasons = []

    for hour in hourly_snapshot:
        rain_prob = hour["rain_prob"]
        wind_kmh = hour["wind_kmh"]
        visibility_m = hour["visibility_m"]

        # Rain Risk
        if rain_prob > 60:
            breakdown["rain"] = 45
            reasons.append(
                f"High rain probability ({rain_prob}%) during commute window"
            )

        # Wind Risk
        if wind_kmh > 25:
            breakdown["wind"] = 20
            reasons.append(
                f"Strong wind speeds ({wind_kmh} km/h) during commute window"
            )

        # Visibility Risk
        if visibility_m < 2000:
            breakdown["visibility"] = 10
            reasons.append(
                f"Low visibility ({visibility_m} m) during commute window"
            )

    # Sum breakdown
    total_score = sum(breakdown.values())

    # Cap at 100
    total_score = min(total_score, 100)

    # If no issues
    if total_score == 0:
        reasons.append("No significant weather risks detected")

    return total_score, breakdown, reasons
