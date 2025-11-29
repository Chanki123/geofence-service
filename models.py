# models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class LocationEvent(BaseModel):
    vehicleId: str = Field(..., example="TX123")
    lat: float = Field(..., example=12.9718915)
    lon: float = Field(..., example=77.6411545)
    timestamp: Optional[int] = Field(None, description="Unix epoch seconds; server will fill if omitted")

class ZoneStatus(BaseModel):
    vehicleId: str
    currentZoneId: Optional[str]
    currentZoneName: Optional[str]

class GeofenceEvent(BaseModel):
    vehicleId: str
    event: str   # "enter" or "exit"
    zoneId: str
    zoneName: Optional[str]
    timestamp: int
