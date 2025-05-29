from navPoint import *

class NavSegment:
    def __init__(self, origin_number: NavPoint, destination_number: NavPoint, distance: float):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

