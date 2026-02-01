from datetime import datetime, timedelta
from app.weather import extract_commute_window
from app.risk import calculate_risk


def find_best_departure(hourly_data, planned_departure: str, duration_minutes: int):
    """
    Checks multiple departure windows within the next 3 hours
    and returns the lowest-risk departure time.
    """

    planned_dt = datetime.fromisoformat(planned_departure)

    # Candidate offsets (minutes)
    candidate_offsets = [0, -30, 30, 60, 90, 120, 180]

    best_option = None
    results = []

    for offset in candidate_offsets:
        candidate_dt = planned_dt + timedelta(minutes=offset)

        # Extract forecast window
        snapshot = extract_commute_window(
            hourly_data,
            candidate_dt.isoformat(),
            duration_minutes
        )

        if not snapshot:
            continue

        # Calculate risk score
        score, breakdown, reasons = calculate_risk(snapshot)

        results.append({
            "departure": candidate_dt,
            "score": score,
            "breakdown": breakdown,
            "reasons": reasons
        })

        # Choose best option (lowest score)
        if best_option is None or score < best_option["score"]:
            best_option = {
                "departure": candidate_dt,
                "score": score,
                "breakdown": breakdown,
                "reasons": reasons
            }

        # Tie-breaker: prefer planned departure if equal score
        elif score == best_option["score"]:
            if candidate_dt == planned_dt:
                best_option = {
                    "departure": candidate_dt,
                    "score": score,
                    "breakdown": breakdown,
                    "reasons": reasons
                }

    # ✅ ALWAYS return tuple
    return best_option, results
