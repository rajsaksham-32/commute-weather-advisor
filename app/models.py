from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class Location(BaseModel):
    latitude: float = Field(..., example=12.9352)
    longitude: float = Field(..., example=77.6245)


class CommuteRequest(BaseModel):
    home: Location
    office: Location

    planned_departure: str = Field(
        ...,
        example="2026-01-10T08:30:00",
        description="Planned departure time in ISO format"
    )

    duration_minutes: Optional[int] = Field(
        45,
        example=45,
        description="Commute duration in minutes (default: 45)"
    )


class WeatherSnapshotHour(BaseModel):
    time: str
    rain_prob: int
    wind_kmh: float


class CommuteResponse(BaseModel):
    risk_score: int
    recommendation: str
    recommended_departure: Optional[str]

    reason: List[str]

    risk_breakdown: Dict[str, int]
    weather_snapshot: Dict[str, Any]
    
