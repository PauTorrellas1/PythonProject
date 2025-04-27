from node import *

class Segment:
    def __init__(self,name:str, origin:Node, destination:Node):
        ''''Definimos la clase segmento, compuesta por un nombre, un nodo origen y un nodo final.
        También contiene los costes de viajar de un nodo al otro, calculados según la distancia'''
        self.name=name
        self.origin=origin
        self.destination=destination
        self.cost=Distance(origin,destination)
#Definimos la clase segment