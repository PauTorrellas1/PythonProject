from segment import *
import matplotlib.pyplot as p
class Graph:
    def __init__(self):
        self.nodes=[]
        self.segments=[]

def AddNode(g,n):
    b = True
    i = 0
    while i < len(g.nodes) and b:
        if g.nodes.name[i] == n.name:
            b = False
        elif b:
            g.nodes.append(n)
            b=False
        i+=1
    return b
def AddSegment (g, Vector:str, nOrigin, nDestination):
    Origin=Destination=g.nodes[0]
    a=c=False
    j=0
    while j<len(g.nodes) and not c and not a:
        if nOrigin==g.nodes.name[j]:
            Origin=g.nodes[j]
            c=True
        if nDestination==g.nodes.name[j]!=nOrigin:
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
    i=0
    while g.nodes!=[]:
        X.append(g.nodes.x[i])
        Y.append(g.nodes.y[i])
        p.text(g.nodes.x[i],g.nodes.y[i], g.nodes.name[i])
        i+=1
    o=0
    while o<len(g.segments):
        p.plot([g.segments.na.x[o],g.segments.nb.x[o]],[g.segments.na.y[o],g.segments.nb.y[o]])
        p.text((g.segments.na.x[o]+g.segments.nb.x[o])/2,(g.segments.na.y[o]+g.segments.nb.y[o])/2, g.segment.cost[o])
        o+=1
    p.scatter(X,Y,"r", marker="D")
    p.grid(color="g")
    p.xlabel("x")
    p.ylabel("y")
    p.show()
def PlotNode (g, origin):
    o=0
    while o<len(g.nodes): #Es pot fer els grisos despres per més eficiència
        p.scatter(g.nodes.x[o],g.nodes.y[o], color="858585")
        o+=1
    p.scatter(origin.x,origin.y,color='#0000FF')
    i=0
    while i<len(origin.neighbor):
        p.scatter(origin.neighbor.x[i],origin.neighbor.y[i],color='#00FF00')
        i+=1
    t=0
    while t<len(g.segments):
        if g.segments.na.name[t]==origin and (g.segments.nb[t] in origin.neighbors):
            p.plot([g.segments.na.x[t], g.segments.nb.x[t]], [g.segments.na.y[t], g.segments.nb.y[t]],color='FF0000')
            p.text((g.segments.na.x[o] + g.segments.nb.x[o]) / 2, (g.segments.na.y[o] + g.segments.nb.y[o]) / 2, g.segment.cost[o])
        t+=1
    if origin not in g.nodes:
        return False
    else:
        return True