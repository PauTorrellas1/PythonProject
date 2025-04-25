from segment import *
import matplotlib.pyplot as p


class Graph:
    def __init__(self):
        self.nodes=[]
        self.segments=[]


def AddNode(g,n):
    '''
    Esta función busca un nodo en el grafo y lo añade si no lo encuentra y
    False si no lo añade
    '''
    if n in g.nodes:
        b = False
    elif n not in g.nodes:
        g.nodes.append(n)
        b =True
    else:
        print("ERROR(AddNode)")
        b=False
    return b

def SearchNode(g,name):
    '''
    Esta función busca un nodo en el grafo y retorna el node si lo encuentra y
    None si no lo encuentra
    '''
    b=True
    for n in g.nodes:
        if n.name == name:
            b=False
            return n
    if b:
        return None

def AddSegment(g, Vector:str, nOrigin, nDestination):
    '''
    Esta función añade un segmento al grafo si encuentra los nodos en la lista g.nodes
    y retorna True o False en caso de que no pueda
    '''
    Origin = SearchNode(g, nOrigin)
    Destination = SearchNode(g, nDestination)
    if Origin != None and Destination != None:
        g.segments.append(Segment(Vector,Origin,Destination))
        AddNeighbor(Origin, Destination)
        return True
    else:
        print("node not valid")
        return False

def GetClosest (g, x:float,y:float):
    '''
    Esta función encuentra el nodo más cercano a un punto y lo retorna
    '''
    i=0
    Dmin=Distance(Node("nxy",x,y),g.nodes[i])
    Closestn = g.nodes[i]
    while i<len(g.nodes):
        if Dmin>Distance(Node("nxy",x,y), g.nodes[i]):
            Dmin=Distance(Node("nxy",x,y), g.nodes[i])
            Closestn=g.nodes[i]
        i+=1
    return Closestn

def NodeConfig (g):
    # Crea la configuración base de los nodos
    for n in g.nodes:
        p.plot([n.x], [n.y], "r", marker="D", zorder=2)
        p.text(n.x+0.5, n.y-0.5, n.name, fontweight='bold')

def SegmentConfig(g,color:str):
    #Crea la configuración base de los segmentos
    for s in g. segments:
        p.plot([s.na.x, s.nb.x], [s.na.y, s.nb.y], color, zorder=1)
        p.text((s.na.x + s.nb.x)/2+0.5, (s.na.y + s.nb.y)/2+0.5, f"{s.cost}", zorder=3)

def Plot(g):
    #Muestra todos los nodos y los segmentos y su coste
    NodeConfig(g)
    SegmentConfig(g,"#979797")

    p.grid(color="#717171", linestyle="--")
    p.xlabel("x")
    p.ylabel("y")
    p.show()

def PlotNode (g, Norigin):
    #Esta función muestra el origen azul, sus vecinos verdes, los segmentos que los unen rojos y el resto de nodos grises
    origin=SearchNode(g,Norigin)
    if origin in g.nodes:
        for n in g.nodes:
            p.scatter(n.x, n.y, color="#979797", zorder=2) #zorder es el orden en el que se muestran
            p.text(n.x+0.5, n.y+0.5, n.name, fontweight='bold')

        p.scatter(origin.x, origin.y, color="b", zorder=3)

        for n in origin.neighbors:
            p.scatter(n.x, n.y, color="g", zorder=3)

        for n in origin.neighbors: #segmentos origen-vecinos
            p.plot([origin.x, n.x], [origin.y, n.y], color="r", zorder=1)
            p.text((origin.x + n.x)/2+0.5, (origin.y + n.y)/2+0.5, f"{Distance(origin,n)}", zorder=4)

        p.grid(color="#717171", linestyle="--")
        p.xlabel("x")
        p.ylabel("y")
        p.show()

        return True
    else:
        return False

def read_file(Nfile:str):
    """
    CSV file
    Format:
        Type of add (S=segment N=node), Name, Attribute1, Attribute 2
    """
    G = Graph()
    F=open(Nfile,"r")
    line=F.readline()
    while line!="":
        parts=line.strip().split(",")
        if parts[0]=="N":
            _, name, x, y = parts
            AddNode(G, Node(name, eval(x), eval(y)))
        if parts[0] == "S":
            _, name, n1, n2 = parts
            AddSegment(G, name, n1, n2)
        line = F.readline()
    return G

def CreateNode(g,name,x,y):
    return AddNode(g,Node(name, x, y))

def DeleteNode(g, node_name):
    node = SearchNode(g, node_name)
    if node:
        g.nodes.remove(node)
        g.segments = [s for s in g.segments if s.na != node and s.nb != node]
        for n in g.nodes:
            if node in n.neighbors:
                n.neighbors.remove(node)
        return True
    else:
        print ('No encontrado')
        return False