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
        example="2026-02-01T19:00:00",
        description="Planned departure time in ISO format"
    )

    duration_minutes: Optional[int] = Field(
        45,
        example=90,
        description="Commute duration in minutes"
    )



class CommuteResponse(BaseModel):
    risk_score: int
    cache_status: str

    recommendation: str
    recommended_departure: Optional[str]

    reason: List[str]
    risk_breakdown: Dict[str, int]
    weather_snapshot: Dict[str, Any]
