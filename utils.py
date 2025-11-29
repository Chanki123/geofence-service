# utils.py
from shapely.geometry import Point, Polygon
import math
from typing import Dict, List, Optional, Any

EARTH_RADIUS_M = 6371000.0

def haversine_distance_m(lat1, lon1, lat2, lon2):
    # all args in degrees
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return EARTH_RADIUS_M * c

def point_in_circle(lat, lon, center_lat, center_lon, radius_m) -> bool:
    return haversine_distance_m(lat, lon, center_lat, center_lon) <= radius_m

def point_in_polygon(lat, lon, polygon_coords: List[List[float]]) -> bool:
    p = Point(lon, lat)  # shapely uses (x=lon, y=lat)
    poly = Polygon([(c[1], c[0]) if len(c)==2 else (c[1], c[0]) for c in polygon_coords])
    # NOTE: above flipping to (x=lon, y=lat) because polygon coords are [lat, lon]
    return p.within(poly) or p.touches(poly)
