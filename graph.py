from segment import *
import matplotlib.pyplot as p
class Graph:
    def __init__(self):
        self.nodes=[]
        self.segments=[]

def AddNode(g,n):
    if n in g.nodes:
        b=False
    elif n not in g.nodes:
        g.nodes.append(n)
        b=True
    else:
        print("ERROR(AddNode)")
        b=False
    return b
def AddSegment (g, Vector:str, nOrigin, nDestination):
    Origin=Destination=g.nodes[0]
    a=c=False
    j=0
    while j<len(g.nodes) and not c and not a:
        if nOrigin==g.nodes[j].name:
            Origin=g.nodes[j]
            c=True
        if nDestination==g.nodes[j].name!=nOrigin:
            Destination=g.nodes[j]
            a=True
        j+=1
    if a and c:
        g.segments.append(Segment(Vector,Origin,Destination))
        AddNeighbor(Origin, Destination)
    elif not(a and c):
        print("node not valid")
    return (a and c)
def GetClosest (g, x:float,y:float):
    i=0
    Dmin=0
    Closestn = g.nodes[i]
    while i<len(g.nodes):
        if Dmin>Distance(Node("nxy",x,y), g.nodes[i]):
            Dmin=Distance(Node("nxy",x,y), g.nodes[i])
            Closestn=g.nodes[i]
        i+=1
    return Closestn
def Plot(g):
    X=Y=[]
    i=1
    while g.nodes!=[]:
        X.append(g.nodes[i].x)
        Y.append(g.nodes[i].y)
        p.text(g.nodes[i].x,g.nodes[i].y, g.nodes[i].name)
        i+=1
    o=0
    while o<len(g.segments):
        p.plot([g.segments[o].na.x,g.segments[o].nb.x],[g.segments[o].na.y,g.segments[o].nb.y])
        p.text((g.segments[o].na.x+g.segments[o].nb.x)/2,(g.segments.na.y[o]+g.segments[o].nb.y)/2, g.segment[o].cost)
        o+=1
    p.scatter(X,Y,"r", marker="D")
    p.grid(color="g")
    p.xlabel("x")
    p.ylabel("y")
    p.show()
def PlotNode (g, origin):
    o=0
    while o<len(g.nodes): #Es pot fer els grisos despres per més eficiència
        p.scatter(g.nodes[o].x,g.nodes[o].y, color="858585")
        o+=1
    p.scatter(origin.x,origin.y,color='#0000FF')
    i=0
    while i<len(origin.neighbor):
        p.scatter(origin.neighbor[i].x,origin.neighbor[i].y,color='#00FF00')
        i+=1
    t=0
    while t<len(g.segments):
        if g.segments[t].na.name==origin and (g.segments[t].nb in origin.neighbors):
            p.plot([g.segments.na[t].x, g.segments.nb[t].x], [g.segments[t].na.y, g.segments[t].nb.y],color='FF0000')
            p.text((g.segments[o].na.x + g.segments[o].nb.x) / 2, (g.segments[o].na.y + g.segments[o].nb.y) / 2, g.segment.cost[o])
        t+=1
    if origin not in g.nodes:
        return False
    else:
        return True