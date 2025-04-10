import math
class Node:
    def __init__(self,name: str, x: float, y: float):
        self.name=name
        self.x=x
        self.y=y
        self.neighbors=[]

def AddNeighbor (n1,n2):
    b=True
    i=0
    while i<len(n1.neighbors) and b:
        if n1.neighbors[i].name==n2.name:
            b=False
        else:
            n1.neighbors.append(n2)
        i+=1
    return b
def Distance (n1:Node, n2:Node):
    return math.sqrt((n1.x-n2.x)**2+(n1.y-n2.y)**2)