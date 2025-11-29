# Geofence Event Processor (FastAPI + Shapely)

## Overview
Simple prototype that:
- Accepts real-time location events via `POST /location`.
- Detects enter/exit events as vehicles cross zone boundaries.
- Stores vehicle zone state and event history in memory.
- Provides `GET /vehicle/{id}/zone`, `GET /events`, and `GET /zones`.

## Tech
- Python + FastAPI
- Shapely (geometry)
- Uvicorn (ASGI server)
- In-memory store (thread-safe)
- Tests via pytest

## Setup (VS Code)
1. Create virtualenv and activate:
   - `python -m venv .venv`
   - Activate `.venv` (Windows or macOS/Linux)
2. Install:
   - `pip install -r requirements.txt`
3. Run server:
   - `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## Endpoints
- `POST /location` — JSON body: `{vehicleId, lat, lon, timestamp?}`
  - Returns 204 on success.
- `GET /vehicle/{id}/zone` — JSON body: current zone for vehicle.
- `GET /events` — last events (enter/exit).
- `GET /zones` — list of defined zones.

## How it detects enter/exit
- On each location event we check point-in-polygon or point-in-circle.
- We compare the detected zone with previously stored zone in memory.
- If changed → create exit (for old) and enter (for new) events with timestamp.

## Assumptions & Tradeoffs
- Zones are static and loaded from `zones.json`.
- In-memory store used for simplicity (not durable).
- Single process; for horizontal scaling you'd use Redis and an event stream (Kafka), and PostGIS for spatial queries.

## Improvements (given more time)
- Persist events and vehicle state in Redis / Postgres + PostGIS.
- Use Kafka for event streaming and downstream consumption.
- Add authentication and authorization.
- Add metrics (Prometheus) and structured logs.
- Add more robust geospatial logic (buffering, fuzzy boundaries), and rate limiting.

## Testing
- Run `pytest` to execute tests in `tests/`.
- Use Postman or curl for manual testing (examples below).

## Example curl
