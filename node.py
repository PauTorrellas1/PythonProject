import math


class Node:
    def __init__(self,name: str, x: float, y: float):
        self.name=name
        self.x=x
        self.y=y
        self.neighbors=[]


def IsNeighbor(n1,n2):
    #Combrueba si el segundo nodo es vecino del primero
    if n2 in n1.neighbors:
        return True
    else:
        False

def AddNeighbor (n1,n2):
    #Si el segundo nodo introducido no es vecino, lo añade
    if not IsNeighbor(n1,n2):
        n1.neighbors.append(n2)
    return not IsNeighbor(n1, n2)

def Distance (n1,n2):
    #Retorna la distancia entre dos nodos redondeada
    D=round(math.sqrt((n1.x-n2.x)**2+(n1.y-n2.y)**2), 1)
    if D%10==0:
        D=round(D)
    return D