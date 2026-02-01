from datetime import datetime, timedelta

from app.weather import extract_commute_window
from app.risk import calculate_risk


def find_best_departure(hourly_data, planned_departure: str, duration_minutes: int, aqi=None):
    """
    Departure Recommendation Engine

    Checks multiple departure options within the next 3 hours
    and selects the departure time with the lowest weather risk score.

    Bonus Support:
    - AQI risk is included in scoring if provided.
    """

    planned_dt = datetime.fromisoformat(planned_departure)

    
    candidate_offsets = [0, -30, 30, 60, 90, 120, 180]

    best_option = None
    results = []

    for offset in candidate_offsets:
        candidate_dt = planned_dt + timedelta(minutes=offset)

        
        snapshot = extract_commute_window(
            hourly_data,
            candidate_dt.isoformat(),
            duration_minutes
        )

        if not snapshot:
            continue

        
        score, breakdown, reasons = calculate_risk(snapshot, aqi=aqi)

        results.append({
            "departure": candidate_dt,
            "score": score,
            "breakdown": breakdown,
            "reasons": reasons
        })

        
        if best_option is None or score < best_option["score"]:
            best_option = {
                "departure": candidate_dt,
                "score": score,
                "breakdown": breakdown,
                "reasons": reasons
            }

        
        elif score == best_option["score"]:
            if candidate_dt == planned_dt:
                best_option = {
                    "departure": candidate_dt,
                    "score": score,
                    "breakdown": breakdown,
                    "reasons": reasons
                }

    return best_option, results
