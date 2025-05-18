from navPoint import *
from navAirpoint import *
from navSegment import *

class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_segments = []
        self.nav_airports = []


def get_node_by_name(airspace: AirSpace, name: str) -> NavPoint:
    """Find a NavPoint by name in the AirSpace"""
    for point in airspace.nav_points:
        if point.name == name:
            return point
    return None


def get_segment_between(airspace: AirSpace, origin_name: str, destination_name: str) -> NavSegment:
    """Find a NavSegment between two named points"""
    origin = get_node_by_name(airspace, origin_name)
    destination = get_node_by_name(airspace, destination_name)

    if origin and destination:
        for segment in airspace.nav_segments:
            if segment.origin_number == origin.number and segment.destination_number == destination.number:
                return segment
    return None


def get_neighbors(airspace: AirSpace, point_name: str) -> list:
    """Get all neighbors of a NavPoint"""
    point = get_node_by_name(airspace, point_name)
    if not point:
        return []

    neighbors = []
    for segment in airspace.nav_segments:
        if segment.origin_number == point.number:
            dest_point = next((p for p in airspace.nav_points if p.number == segment.destination_number), None)
            if dest_point:
                neighbors.append(dest_point)
    return neighbors