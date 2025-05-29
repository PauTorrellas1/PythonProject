from navPoint import *

class NavSegment:
    '''Definimos la clase NavSegment, que está formada por 2 puntos y la distancia'''
    def __init__(self, origin_number: NavPoint, destination_number: NavPoint, distance: float):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

