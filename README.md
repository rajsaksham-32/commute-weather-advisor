# Commute Weather Risk Advisor

This project is a backend service that helps commuters decide whether it’s a good idea to leave at their planned time, or adjust their departure to avoid bad weather conditions like heavy rain, strong winds, or poor visibility.

The API fetches an hourly weather forecast and generates:

- a Weather Risk Score (0–100)
- a short explanation of what caused the risk
- a suggested safer departure time (if needed)

---

## What this service does

Given:

- home coordinates
- office coordinates
- planned departure time
- commute duration

The service:

1. pulls hourly forecast data using the Open-Meteo public API  
2. checks weather conditions during the commute window  
3. calculates a deterministic risk score  
4. recommends the best departure time within the next few hours  

---

## Tech used

- Python 3
- FastAPI (REST API framework)
- Uvicorn (server)
- httpx (API requests)
- Open-Meteo (free weather forecast provider)

---

## Setup (run locally)

## 1.Clone the repository
```
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

## Example curl request
```curl -X POST "http://127.0.0.1:8000/commute-advice" \
-H "Content-Type: application/json" \
-d '{
  "home": {"latitude": 12.9352, "longitude": 77.6245},
  "office": {"latitude": 12.9698, "longitude": 77.7500},
  "planned_departure": "2026-02-01T19:00:00",
  "duration_minutes": 90
}'
```
---

# Risk scoring logic

The score ranges from 0 (safe) to 100 (very risky).

The current scoring rules are:

- +45 if rain probability is above 60%
- +20 if wind speed is above 25 km/h
- +10 if visibility drops below 2000 m
Each response includes a breakdown so it’s clear where the score comes from.

---

# Departure recommendation

Instead of only checking the planned time, the service also looks at nearby departure options (up to the next 3 hours).

It selects the departure time with the lowest risk score.

If all times have the same risk, it simply recommends leaving as planned.

---

# Assumptions

- Forecast is fetched using the home/start location
- No database is used (everything is calculated live)
- Recommendation logic is kept simple and explainable

---

## If I had one extra day, I would probably add:

- caching weather responses to reduce API calls
- AQI/pollution-based risk scoring
- unit tests + CI pipeline
- deployment on Render/Railway for a live demo

---

## Author

Hi, I’m **Saksham Raj**  
I’m a Computer Science student with a strong interest in **AI and Machine Learning**, along with backend development.

I enjoy working on projects that combine real-world data, clean API design, and practical problem solving.

Some areas I’m especially enthusiastic about:

- Machine Learning & AI applications  
- Backend Development (FastAPI, REST APIs)  
- Python Programming  
- Software Engineering & System Design  
- Building useful tools with real-world integrations  

This project was built as part of a backend take-home assignment to demonstrate weather-based risk analysis, explainable scoring logic, and departure-time recommendations.
