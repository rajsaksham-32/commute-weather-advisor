from fastapi import FastAPI
from app.models import CommuteRequest, CommuteResponse
from app.weather import fetch_hourly_forecast
from app.recommendation import find_best_departure

app = FastAPI(
    title="Commute Weather Risk Advisor",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Commute Weather Advisor API is running."}


@app.post("/commute-advice", response_model=CommuteResponse)
def commute_advice(request: CommuteRequest):

    forecast = fetch_hourly_forecast(
        request.home.latitude,
        request.home.longitude
    )

    hourly_data = forecast["hourly"]

    best_option, all_results = find_best_departure(
        hourly_data,
        request.planned_departure,
        request.duration_minutes
    )

    if best_option is None:
        return {
            "risk_score": 0,
            "recommendation": "No forecast data available",
            "recommended_departure": request.planned_departure,
            "reason": [],
            "risk_breakdown": {},
            "weather_snapshot": {}
        }

    planned_dt = request.planned_departure
    best_dt = best_option["departure"].isoformat()

    if best_dt == planned_dt:
        message = "No change needed — planned departure is already the safest option."
    else:
        message = f"Better weather expected if you leave at {best_option['departure'].strftime('%H:%M')}"

    return {
        "risk_score": best_option["score"],
        "recommendation": message,
        "recommended_departure": best_dt,
        "reason": best_option["reasons"],
        "risk_breakdown": best_option["breakdown"],
        "weather_snapshot": {
            "checked_options": [
                {
                    "departure": r["departure"].strftime("%H:%M"),
                    "score": r["score"]
                }
                for r in all_results
            ]
        }
    }
