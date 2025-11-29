# storage.py
from typing import Dict, Optional, List
from threading import Lock
from models import GeofenceEvent
import time

class InMemoryStore:
    def __init__(self):
        self._lock = Lock()
        # vehicleId -> {"zone_id": Optional[str], "last_location": (lat, lon, ts)}
        self.vehicle_states: Dict[str, Dict] = {}
        # list of GeofenceEvent dicts
        self.events: List[dict] = []

    def get_vehicle_zone(self, vehicle_id: str) -> Optional[str]:
        with self._lock:
            state = self.vehicle_states.get(vehicle_id)
            return state.get("zone_id") if state else None

    def update_vehicle(self, vehicle_id: str, lat: float, lon: float, ts: int, zone_id: Optional[str], zone_name: Optional[str]):
        with self._lock:
            prev = self.vehicle_states.get(vehicle_id, {"zone_id": None, "last_location": None})
            prev_zone = prev.get("zone_id")
            # if changed, create events
            if prev_zone != zone_id:
                # exit event for prev_zone
                if prev_zone is not None:
                    e = {"vehicleId": vehicle_id, "event": "exit", "zoneId": prev_zone, "zoneName": prev.get("zone_name"), "timestamp": ts}
                    self.events.append(e)
                # enter event for new zone
                if zone_id is not None:
                    e = {"vehicleId": vehicle_id, "event": "enter", "zoneId": zone_id, "zoneName": zone_name, "timestamp": ts}
                    self.events.append(e)
            # update state
            self.vehicle_states[vehicle_id] = {"zone_id": zone_id, "zone_name": zone_name, "last_location": (lat, lon, ts)}

    def list_events(self, limit=100):
        with self._lock:
            return list(self.events)[-limit:]

store = InMemoryStore()
