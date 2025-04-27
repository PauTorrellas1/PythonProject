import math

class Node:
    def __init__(self, name, x, y):
        '''Definimo la clase Node, compuesta por su nombre y la posición x, y'''
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.neighbors = []


def AddNeighbor(n1, n2):
    """
    Esta función añade un nodo (n2) a la lista de los vecinos de n1
    Si n2 ya está en su lista de vecinos retorna False
    Si no, retornará True.
    """
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True


def Distance(n1, n2):
    """
    Devuelve la distancia aproximada entre n1 y n2
    """
    dx = n1.x - n2.x
    dy = n1.y - n2.y
    return math.sqrt(dx ** 2 + dy ** 2)