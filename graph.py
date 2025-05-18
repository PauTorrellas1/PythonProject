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
    '''Configures the segments with clean cost labels'''
    for s in g.segments:
        # Draw simple line
        p.plot([s.origin.x, s.destination.x],
               [s.origin.y, s.destination.y],
               color=color, zorder=1, linewidth=1.5)

        # Add cost label (small, black, no box)
        cost_text = f"{s.cost:.2f}"
        p.text((s.origin.x + s.destination.x) / 2 + 0.2,
               (s.origin.y + s.destination.y) / 2 + 0.2,
               cost_text, zorder=3, color='black', fontsize=8)

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

def read_file(Nfile: str):
    """
    CSV file reader for graph data
    Format:
        Type of add (S=segment N=node), Name, Attribute1, Attribute 2
    """
    G = Graph()
    with open(Nfile, "r") as F:
        for line in F:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 4:
                continue
            if parts[0] == "N":
                _, name, x, y = parts[:4]
                AddNode(G, Node(name, float(x), float(y)))
            elif parts[0] == "S":
                _, name, n1, n2 = parts[:4]
                AddSegment(G, name, n1, n2)
    return G

def read_map_file(region: str):
    standard_regions = {'Catalunya': 'Cat', 'España': 'Esp', 'Europa': 'Eur'}
    if region in standard_regions:
        prefix = standard_regions[region]
        try:
            id_to_name = {}
            name_to_node = {}
            with open(f'{prefix}_nav.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        node_id, name, lat, lon = parts[:4]
                        id_to_name[node_id] = name
            airport_nodes = set()
            with open(f'{prefix}_aer.txt', 'r') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        airport_nodes.add(name)
            G = Graph()
            with open(f'{prefix}_nav.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        node_id, name, lat, lon = parts[:4]
                        node = Node(name, float(lon), float(lat))
                        AddNode(G, node)
                        name_to_node[name] = node
            successful = 0
            with open(f'{prefix}_seg.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        origin_id, dest_id, distance = parts[:3]
                        origin_name = id_to_name.get(origin_id)
                        dest_name = id_to_name.get(dest_id)
                        if origin_name and dest_name:
                            origin_node = name_to_node.get(origin_name)
                            dest_node = name_to_node.get(dest_name)
                            if origin_node and dest_node:
                                seg_name = f"{origin_name}_{dest_name}"
                                segment = Segment(seg_name, origin_node, dest_node)
                                segment.cost = float(distance)
                                G.segments.append(segment)
                                AddNeighbor(origin_node, dest_node)
                                successful += 1
                            else:
                                print(f"Node objects not found: {origin_name} -> {dest_name}")
                        else:
                            print(f"Names not found for IDs: {origin_id} -> {dest_id}")
            print(f"Successfully connected {successful} segments")
            return G
        except Exception as e:
            print(f"Error: {str(e)}")
            return read_file(region)
    else:
        return read_file(region)

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

def DeleteSegment(graph, segment_name):
    segment_to_delete = None
    for seg in graph.segments:
        if seg.name == segment_name:
            segment_to_delete = seg
            break
    if segment_to_delete:
        if segment_to_delete.destination in segment_to_delete.origin.neighbors:
            segment_to_delete.origin.neighbors.remove(segment_to_delete.destination)
        if segment_to_delete.origin in segment_to_delete.destination.neighbors:
            segment_to_delete.destination.neighbors.remove(segment_to_delete.origin)
        graph.segments.remove(segment_to_delete)
        return True
    return False

