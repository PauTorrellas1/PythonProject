from node import *


class Segment:
    def __init__(self,name:str, na:Node, nb:Node):
        self.name=name
        self.na=na
        self.nb=nb
        self.cost=Distance(na,nb)
#Definimos la clase segment