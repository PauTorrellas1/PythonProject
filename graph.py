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


def SegmentConfig(g, color: str):
    '''Configuramos los segmentos mostrados en el gráfico'''
    for s in g.segments:
        p.plot([s.origin.x, s.destination.x],
                 [s.origin.y, s.destination.y],
                 color='blue', zorder=1, linewidth= 1.5)
        dx = s.destination.x - s.origin.x
        dy = s.destination.y - s.origin.y
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length > 0:
            arrow_length = length * 0.1
            p.arrow(s.origin.x, s.origin.y,
                    dx * 1, dy * 1, head_width=0.2, head_length=0.3,
                    fc=color, ec=color,
                    length_includes_head=True,
                    zorder=1)
        # Mostrar coste con 2 decimales
        cost_text = f"{s.cost:.2f}"  # Formato: 2 decimales
        p.text((s.origin.x + s.destination.x) / 2 + 0.3,
               (s.origin.y + s.destination.y) / 2 + 0.3,
               cost_text, zorder=3,
               bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

def Plot(g):
    '''Fabricamos el gráfico que mostrará todos nuestros datos'''
    #Muestra todos los nodos y los segmentos y su coste
    NodeConfig(g)
    SegmentConfig(g,"#979797")

    p.grid(color="#717171", linestyle="--")
    p.xlabel("x")
    p.ylabel("y")
    p.show()


def PlotNode(g, Norigin):
    '''Muestra un nodo de origen (azul), sus vecinos (verde) y segmentos (rojo).
    Nodos no vecinos en gris. Costes con 2 decimales y mejor alineación.'''
    origin = SearchNode(g, Norigin)
    if origin not in g.nodes:
        return False
    for n in g.nodes:
        p.scatter(n.x, n.y, color="#979797", zorder=2)
        p.text(n.x + 0.5, n.y + 0.5, n.name, fontweight='bold', fontsize=9)
    p.scatter(origin.x, origin.y, color="b", s=100, zorder=3)
    for neighbor in origin.neighbors:
        p.plot([origin.x, neighbor.x], [origin.y, neighbor.y],
               color="r", linewidth=2, zorder=1)
        cost = f"{Distance(origin, neighbor):.2f}"
        text_x = (origin.x + neighbor.x) / 2 + 0.3
        text_y = (origin.y + neighbor.y) / 2 + 0.3
        p.text(text_x, text_y, cost,
               zorder=4, fontsize=8, color='black',
               bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round'))
    for neighbor in origin.neighbors:
        p.scatter(neighbor.x, neighbor.y, color="g", s=80, zorder=3)
    p.grid(color="#717171", linestyle="--", alpha=0.5)
    p.xlabel("X", fontsize=10)
    p.ylabel("Y", fontsize=10)
    p.title(f"Neighbors of '{Norigin}'", fontweight='bold')
    p.show()
    return True

def read_file(Nfile:str):
    """
    CSV file
    Format:
        Type of add (S=segment N=node), Name, Attribute1, Attribute 2
    """
    G = Graph()
    with open(Nfile,"r") as F:
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

def DeleteSegment(g, segment_name):
    '''Esta función elimina un segmento de segmentos'''
    g.segments = [s for s in g.segments if s.name != segment_name]
    for node in g.nodes:
        node.neighbors = [n for n in node.neighbors
                          if not any(s.name == segment_name
                                     for s in g.segments
                                     if s.origin == node and s.destination == n)]
