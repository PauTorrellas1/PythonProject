from segment import *
import matplotlib.pyplot as p


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g,n):
    '''
    Esta función busca un nodo en el grafo y lo añade si no lo encuentra y
    False si no lo añade
    '''
    if n in g.nodes:
        b = False
    elif n not in g.nodes:
        g.nodes.append(n)
        b = True
    else:
        print("ERROR(AddNode)")
        b = False
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

def SearchSegment(g, Vector):
    '''''
    Esta función buscará segmentos en el grafo para retornarlo si lo encuentra
    o retornar None si no lo hace. Es esencialmente lo mismo que SearchNode
    '''
    a = True
    for segment in g.segments:
        if segment.name == Vector:
            a = False
            return segment
        if a:
            return None

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
    '''Especificamos la configuración de los nodos mostrados en el gráfico'''
    # Crea la configuración base de los nodos
    for n in g.nodes:
        p.plot([n.x], [n.y], "r", marker="D", zorder=2)
        p.text(n.x+0.5, n.y-0.5, n.name, fontweight='bold')

def SegmentConfig(g,color:str):
    ''''Especificamos la configuración de los segmentos mostrados en el gráfico'''
    #Crea la configuración base de los segmentos
    for s in g. segments:
        p.plot([s.origin.x, s.destination.x], [s.origin.y, s.destination.y], color, zorder=1)
        p.text((s.origin.x + s.destination.x) / 2 + 0.5, (s.origin.y + s.destination.y) / 2 + 0.5, f"{s.cost:.2f}",
                zorder=3)

def Plot(g):
    '''Fabricamos el gráfico que mostrará todos nuestros datos'''
    #Muestra todos los nodos y los segmentos y su coste
    NodeConfig(g)
    SegmentConfig(g,"#979797")

    p.grid(color="#717171", linestyle="--")
    p.xlabel("x")
    p.ylabel("y")
    p.show()

def PlotNode (g, Norigin):
    '''Fabricamos un gráfico que nos muestre un nodo de origen en azul, a sus vecinos en verde y los
    segmentos que los unen en rojo. Todos los nodos que no sean vecinos serán mostrados en gris'''
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
    '''Esta función crea un node y lo añade a Node'''
    return AddNode(g,Node(name, x, y))


def DeleteNode(g, node_name):
    '''Esta función elimina un nodo de nodos'''
    node = SearchNode(g, node_name)
    if node:
        g.nodes.remove(node)
        g.segments = [s for s in g.segments if s.origin != node and s.destination != node]
        for n in g.nodes:
            if node in n.neighbors:
                n.neighbors.remove(node)
                return True
    else:
        return False

def DeleteSegment(g, Vector):
    '''Esta función elimina un segmento de segmentos'''
    segments_to_remove = [s for s in g.segments if s.name in (Vector, Vector[::-1])]
    SearchSegment(g, Vector)
    if not segments_to_remove:
        print('No encontrado')
        return False
    for segment in segments_to_remove:
        g.segments.remove(segment)
