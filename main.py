# main.py
import json
import time
from fastapi import FastAPI, HTTPException
from models import LocationEvent, ZoneStatus
from storage import store
from utils import point_in_circle, point_in_polygon
from typing import Optional

app = FastAPI(title="Geofence Event Processor", version="1.0")

# Load zones
with open("zones.json", "r", encoding="utf-8") as f:
    ZONES = json.load(f)

def find_zone_for_point(lat: float, lon: float) -> Optional[dict]:
    # return the first matching zone (priority: as defined in file)
    for z in ZONES:
        if z.get("type") == "circle":
            c_lat, c_lon = z["center"]
            if point_in_circle(lat, lon, c_lat, c_lon, z["radius_m"]):
                return z
        elif z.get("type") == "polygon":
            poly = z["polygon"]  # list of [lat, lon]
            if point_in_polygon(lat, lon, poly):
                return z
    return None

@app.post("/location", status_code=204)
async def post_location(evt: LocationEvent):
    # validate lat/lon ranges
    if not (-90.0 <= evt.lat <= 90.0 and -180.0 <= evt.lon <= 180.0):
        raise HTTPException(status_code=400, detail="invalid lat/lon")
    ts = evt.timestamp or int(time.time())
    zone = find_zone_for_point(evt.lat, evt.lon)
    zone_id = zone["id"] if zone else None
    zone_name = zone.get("name") if zone else None

    # update store (will create enter/exit events if zone changed)
    store.update_vehicle(evt.vehicleId, evt.lat, evt.lon, ts, zone_id, zone_name)
    return None

@app.get("/vehicle/{vehicle_id}/zone", response_model=ZoneStatus)
async def get_vehicle_zone(vehicle_id: str):
    zone_id = store.get_vehicle_zone(vehicle_id)
    zone_name = None
    if zone_id:
        # find zone name
        for z in ZONES:
            if z["id"] == zone_id:
                zone_name = z.get("name")
                break
    return ZoneStatus(vehicleId=vehicle_id, currentZoneId=zone_id, currentZoneName=zone_name)

@app.get("/events")
async def list_events(limit: int = 100):
    return store.list_events(limit=limit)

@app.get("/zones")
async def list_zones():
    # expose zone definitions for demo/testing
    return ZONES
