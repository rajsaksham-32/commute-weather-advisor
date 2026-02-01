# Commute Weather Risk Advisor API

A backend service that analyzes hourly weather + air quality forecasts and provides a **Commute Weather Risk Score (0–100)** along with a recommended departure time.

This project helps commuters avoid leaving during risky conditions such as heavy rain, strong winds, low visibility, or unhealthy air quality.

---

## Features

- REST API endpoint: **POST /commute-advice**
- Hourly weather forecast integration (Open-Meteo)
- Deterministic and explainable **Weather Risk Score (0–100)**
- Departure-time recommendation engine (checks safer windows)
- Full reason + breakdown output

### Bonus Extensions Included

- **Bonus A: Weather API Caching**
  - Forecast results are cached for ~10 minutes per location
  - Response includes `"cache_status": "HIT"` or `"MISS"`

- **Bonus B: Structured Risk Breakdown**
  - Risk score is broken down by contributing factors:
    - AQI
    - Rain
    - Wind
    - Visibility

---

## Tech Stack

- Python 3.12.3
- FastAPI
- Uvicorn
- HTTPX (API requests)
- Open-Meteo Weather + AQI APIs

---

## Setup (run locally)
Requirements: Python 3.10 or above  
Note: `.venv/` is ignored via `.gitignore` and should not be committed.

## 1.Clone the repository
```bash
git clone https://github.com/rajsaksham-32/commute-weather-advisor.git
cd commute-weather-advisor

```

## 2. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate

```

## 3. Install dependencies
```
pip install -r requirements.txt

```

## 4. Run the server
```
uvicorn app.main:app --reload

```
The server will keep running in **this terminal**.  
**Open a second terminal window/tab to send API requests (curl/Postman)**.

Server runs at:
- http://127.0.0.1:8000

- Swagger docs:
    -- http://127.0.0.1:8000/docs

## API Usage
**Endpoint** 

`POST /commute-advice`

## Example Request
Run in a new terminal (while server is running):
```bash
curl -X POST "http://127.0.0.1:8000/commute-advice" \
-H "Content-Type: application/json" \
-d '{
  "home": {
    "latitude": 12.9352,
    "longitude": 77.6245
  },
  "office": {
    "latitude": 12.9698,
    "longitude": 77.7500
  },
  "planned_departure": "2026-02-01T19:00:00",
  "duration_minutes": 90
}'

```
## Example Response
``` {
  "risk_score": 15,
  "cache_status": "MISS",
  "recommendation": "No change needed — planned departure is already the safest option.",
  "recommended_departure": "2026-02-01T19:00:00",
  "reason": [
    "Air quality is moderate (AQI 72)"
  ],
  "risk_breakdown": {
    "AQI": 15,
    "rain": 0,
    "wind": 0,
    "visibility": 0
  },
  "weather_snapshot": {
    "checked_options": [...], //checked_options truncated in README output
    "aqi_value": 72
  }
}
```

# API Documentation
FastAPI automatically provides Swagger UI:
```
http://127.0.0.1:8000/docs
```

---

## Risk Scoring Logic
The total risk score is computed deterministically:
| Condition              | Score Added |
| ---------------------- | ----------- |
| AQI ≥ 150              | +60         |
| AQI ≥ 100              | +45         |
| AQI ≥ 50               | +15         |
| Rain probability > 60% | +45         |
| Rain probability > 30% | +20         |
| Wind speed > 25 km/h   | +20         |
| Wind speed > 15 km/h   | +10         |
| Visibility < 2000 m    | +10         |
Final score is capped at **100**.
---

## Departure recommendation logic

The system checks multiple departure options:
- Planned time
- 30 min earlier
- 30–180 min later

The lowest-risk departure is recommended.

---

# Assumptions

- Forecast is fetched using the home/start location
- Office coordinates are accepted but not yet used for route-based sampling
- Caching is in-memory (resets when server restarts)
- Recommendation logic is simple but deterministic and explainable

---

## If I had one extra day, I would probably add:

- More advanced route-based forecasting (multiple points between home & office)
- Persistent caching (Redis)
- Unit testing for scoring + recommendation logic
- Deployment support (Docker + cloud hosting)

---

## Author

Hi, I’m **Saksham Raj**  
I’m a Computer Science student with a strong interest in AI and Machine Learning, along with backend development.

I enjoy working on projects that combine real-world data, clean API design, and practical problem solving.

Some areas I’m especially enthusiastic about:

- Machine Learning & AI applications  
- Backend Development (FastAPI, REST APIs)  
- Python Programming  
- Software Engineering & System Design  
- Building useful tools with real-world integrations  

This project was built as part of a backend take-home assignment to demonstrate weather-based risk analysis, explainable scoring logic, and departure-time recommendations.
