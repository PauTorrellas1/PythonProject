from segment import *
import matplotlib.pyplot as p
from airSpace import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from types import SimpleNamespace

root = tk.Tk()
root.title("Airspace Visualization")
message_label = None
clear_timer = None
error_window = None
fig = Figure(figsize=(8.5, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)

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

def SearchNode(g, name):
    '''
    Esta función busca un nodo en el grafo y retorna el node si lo encuentra y
    None si no lo encuentra
    '''
    if is_real_map(g):
        # For real maps, search in nav_points
        point = next((p for p in g.nav_points if p['name'] == name), None)
        if point:
            # Create a hashable SimpleNamespace by implementing __hash__
            ns = SimpleNamespace(name=point['name'], x=point['lon'], y=point['lat'])
            ns.__hash__ = lambda self: hash(self.name)
            return ns
        return None
    else:
        # Búsqueda de nodo original
        for n in g.nodes:
            if n.name == name:
                return n
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
    if is_real_map(g):
        closest = None
        min_dist = float('inf')
        for point in g.nav_points:
            dist = math.sqrt((x - float(point['lon'])) ** 2 + (y - float(point['lat'])) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest = point
        return closest
    else:
        # Original implementation
        i = 0
        Dmin = Distance(Node("nxy", x, y), g.nodes[i])
        Closestn = g.nodes[i]
        while i < len(g.nodes):
            if Dmin > Distance(Node("nxy", x, y), g.nodes[i]):
                Dmin = Distance(Node("nxy", x, y), g.nodes[i])
                Closestn = g.nodes[i]
            i += 1
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

def create_message_area():
    """Crea un mensaje que se muestre al final de la GUI"""
    global message_label
    message_frame = tk.Frame(root)
    message_frame.grid(row=20, column=1, columnspan=5, sticky="ew", padx=10, pady=5)
    message_label = tk.Label(
        message_frame,
        text="",
        fg="black",
        wraplength=1000,
        justify="left",
        anchor="w")
    message_label.pack(fill="x", expand=True)

def show_message(message, is_error=False, persistent=False):
    """Mostramos cierto mensaje en la GUI del área de mensaje creada antes"""
    global message_label
    if message_label is None:
        create_message_area()

    def show_modern_error(title, message, code=None):
        '''Ajustes del mensaje de error que mostraremos en pantalla
        cuando algo falle, ya sea por no haber rellenado todas las entradas
        de cierta función o por haberlas rellenado de manera indebida'''
        global error_window
        if error_window is not None and error_window.winfo_exists():
            error_window.destroy()
        error_window = tk.Toplevel(root)
        error_window.title(title)
        error_window.resizable(False, False)
        window_width = 500
        window_height = 180
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        error_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        error_window.configure(bg='#2c2c2c')
        error_window.attributes('-alpha', 0.98)
        header_frame = tk.Frame(error_window, bg='#1e1e1e', height=25)
        header_frame.pack(fill='x')
        for color in ['#ff5f57', '#ffbd2e', '#28c840']:
            tk.Canvas(header_frame, width=12, height=12, bg=color, bd=0, relief='flat').pack(side='left', padx=5,
                                                                                             pady=6)
        content_frame = tk.Frame(error_window, bg='#2c2c2c')
        content_frame.pack(expand=True, fill='both', padx=20, pady=10)
        icon_canvas = tk.Canvas(content_frame, width=60, height=60, bg='#2c2c2c', highlightthickness=0)
        icon_canvas.create_polygon(30, 5, 55, 20, 55, 45, 30, 60, 5, 45, 5, 20, fill='#e74c3c')
        icon_canvas.create_text(30, 32, text='!', font=("Segoe UI", 22, 'bold'), fill='white')
        icon_canvas.grid(row=0, column=0, padx=10)
        tk.Label(
            content_frame,
            text=message,
            font=("Segoe UI", 12),
            bg='#2c2c2c',
            fg='white',
            wraplength=380,
            justify='left').grid(row=0, column=1, padx=10)
        button_frame = tk.Frame(error_window, bg='#2c2c2c')
        button_frame.pack(fill='x', pady=(10, 0))
        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=error_window.destroy,
            bg='#007bff',
            fg='white',
            activebackground='#0056b3',
            font=("Segoe UI", 10, 'bold'),
            width=8,
            relief='flat',
            bd=0)
        ok_btn.pack(side='right', padx=20)
        error_window.grab_set()
        error_window.transient(root)

    def clear_message(delay=0):
        """Borramos el mensaje después de un delay"""

        def clear():
            message_label.config(text="")

        global clear_timer
        if clear_timer:
            root.after_cancel(clear_timer)
        if delay > 0:
            clear_timer = root.after(int(delay * 1000), lambda: message_label.config(text=""))
        else:
            clear()
    clear_message()
    if is_error:
        formatted_message = f"Error: {message}"
        message_label.config(fg="red")
        show_modern_error("Error", message)
    else:
        formatted_message = message
        message_label.config(fg="black")
    message_label.config(text=formatted_message)
    message_label.update_idletasks()
    if not persistent:
        if is_error:
            clear_message(delay=5)

def Plot(g):
    global fig, ax, canvas

    # Initialize figure if it doesn't exist
    if 'fig' not in globals():
        fig = Figure(figsize=(8.5, 7), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
    else:
        ax.clear()

    if is_real_map(g):
        # Plot real map (AirSpace)
        ax.set_title(f"Airspace Map")

        # Plot navigation points
        for point in g.nav_points:
            ax.plot(point['lon'], point['lat'], 'ro', markersize=4)
            ax.text(point['lon'] + 0.05, point['lat'] + 0.05, point['name'], fontsize=8)

        # Highlight airports
        for airport in g.nav_airports:
            point = next((p for p in g.nav_points if p['name'] == airport), None)
            if point:
                ax.plot(point['lon'], point['lat'], 'gD', markersize=6)

        # Plot segments
        for seg in g.nav_segments:
            origin = next((p for p in g.nav_points if p['id'] == seg['origin_id']), None)
            dest = next((p for p in g.nav_points if p['id'] == seg['dest_id']), None)
            if origin and dest:
                ax.plot([origin['lon'], dest['lon']],
                        [origin['lat'], dest['lat']],
                        'b-', linewidth=1)
                # Add distance label
                ax.text((origin['lon'] + dest['lon']) / 2,
                        (origin['lat'] + dest['lat']) / 2,
                        f"{seg['distance']:.1f}", fontsize=8)
    else:
        # Plot regular graph
        NodeConfig(g)
        SegmentConfig(g, "#979797")

    # Common plot settings
    ax.grid(color="#717171", linestyle="--")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Update canvas
    canvas.draw()

def PlotRealMap(g):
    # Plot navPoints
    for point in g.nav_points:
        p.plot(point['lon'], point['lat'], "ro", markersize=4)
        p.text(point['lon'] + 0.05, point['lat'] - 0.05, point['name'], fontsize=8)

    # Plot navAirports with different markers
    for airport in g.nav_airports:
        point = next((p for p in g.nav_points if p['name'] == airport), None)
        if point:
            p.plot(point['lon'], point['lat'], "gD", markersize=6)

    # Plot navSegments
    for seg in g.nav_segments:
        origin = next((p for p in g.nav_points if p['id'] == seg['origin_id']), None)
        dest = next((p for p in g.nav_points if p['id'] == seg['dest_id']), None)
        if origin and dest:
            p.plot([origin['lon'], dest['lon']],
                   [origin['lat'], dest['lat']],
                   "b-", linewidth=1)
            # Add distance label
            p.text((origin['lon'] + dest['lon']) / 2,
                   (origin['lat'] + dest['lat']) / 2,
                   f"{seg['distance']:.1f}", fontsize=8)

    p.grid(color="#717171", linestyle="--")
    p.xlabel("Longitude")
    p.ylabel("Latitude")
    p.title("Airspace Map")
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

def CreateNode(g,name,x,y):
    '''Esta función crea un node y lo añade a Node'''
    return AddNode(g,Node(name, x, y))

def DeleteNode(g, node_name):
    '''Esta función elimina un nodo de nodos'''
    if is_real_map(g):
        # For real maps, we can't actually delete nodes
        show_message("Cannot delete nodes in real maps", is_error=True)
        return False
    else:
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
    if is_real_map(graph):
        # AirSpace version - segment_name should be in format "origin_destination"
        try:
            origin_name, dest_name = segment_name.split('_')
            origin_id = next(p['id'] for p in graph.nav_points if p['name'] == origin_name)
            dest_id = next(p['id'] for p in graph.nav_points if p['name'] == dest_name)

            # Remove both directions if they exist
            graph.nav_segments = [s for s in graph.nav_segments
                                  if not ((s['origin_id'] == origin_id and s['dest_id'] == dest_id) or
                                          (s['origin_id'] == dest_id and s['dest_id'] == origin_id))]
            return True
        except (ValueError, StopIteration):
            return False
    else:
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

