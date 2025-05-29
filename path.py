from matplotlib.figure import Figure
from graph import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox
import heapq, math


root = tk.Tk()
current_display_mode = "edited"
message_label = None
clear_timer = None
error_window = None
fig = Figure(figsize=(8.5, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
def not_valid():
    #not valid msg for not valid inputs
    lb = tk.Message(root, text="Not Valid", bg='red',pady=20,padx=20)
    lb.grid(row=20, column=0)
    # noinspection PyTypeChecker
    root.after(1000, lb.destroy)
def message(txt,mster=root):
    lb = tk.Message(master=mster,text=txt,width=800,font=("Arial",16))
    lb.grid(row=22, column=5,columnspan=3)
    root.after(10000, lb.destroy)


class Path:
    def __init__(self, name: str, origin: Node, destination: Node = None, cost: float = 0):
        '''Definimos la clase path, compuesta por un nombre, un nodo origen, un nodo final y el coste del camino.'''
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = cost
        self.nodes = [origin]  # List of nodes in order
        self.segments = []  # List of segments in order
        self.cumulative_costs = {origin: 0}  # Cumulative costs from origin to each node

    def AddNodeToPath(self, node: Node, segment: Segment):
        '''Adds a node to the path with its connecting segment'''
        if node not in self.nodes:
            self.nodes.append(node)
            self.segments.append(segment)
            last_node = self.nodes[-2]
            self.cumulative_costs[node] = self.cumulative_costs[last_node] + segment.cost
            self.destination = node
            self.cost = self.cumulative_costs[node]

    def ContainsNode(self, node: Node) -> bool:
        '''Returns True if the Node is in the Path and False otherwise.'''
        return node in self.nodes

    def CostToNode(self, node: Node) -> float:
        '''Returns the total cost from the origin of the Path to the Node.
        Returns -1 if the Node is not in the Path.'''
        return self.cumulative_costs.get(node, -1)

def PlotPath(graph: Graph, path: Path):
    '''Plots path with clean cost labels'''
    global fig, ax, canvas
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
    ax.set_axisbelow(True)

    # Draw all nodes from the provided graph
    for node in graph.nodes:
        color = 'gray'
        if node == path.origin:
            color = 'blue'
        elif node == path.destination:
            color = 'red'
        elif path.ContainsNode(node):
            color = 'green'
        ax.plot(node.x, node.y, 'o', color=color, markersize=8, zorder=3)
        ax.text(node.x, node.y, node.name, fontsize=10, zorder=4)

    # Draw all segments from the provided graph
    for seg in graph.segments:
        is_path_segment = any(
            (seg.origin == path_seg.origin and seg.destination == path_seg.destination)
            for path_seg in path.segments
        )

        if is_path_segment:
            ax.plot([seg.origin.x, seg.destination.x],
                    [seg.origin.y, seg.destination.y],
                    'r-', linewidth=2, zorder=2)
        else:
            ax.plot([seg.origin.x, seg.destination.x],
                    [seg.origin.y, seg.destination.y],
                    '#CCCCCC', linewidth=1, zorder=1)

        # Cost label for all segments
        ax.text((seg.origin.x + seg.destination.x) / 2 + 0.2,
                (seg.origin.y + seg.destination.y) / 2 + 0.2,
                f"{seg.cost:.2f}",
                color='black', fontsize=8, zorder=3)

    canvas.draw()
    message(f"Displaying path from {path.origin.name} to {path.destination.name}")


def set_graph(graph_instance):
    '''Esta función especifica qué codigo será el que mostraremos'''
    global G
    G = graph_instance

def work_with_entry(controls, function):
    """Facilita el uso de la GUI haciendo funcional el botón del enter y saltando de una entrada
    a otra en caso de haber varias entradas en una misma función"""
    for i, control in enumerate(controls):
        if i < len(controls) - 1:
            if isinstance(control, tk.Entry):
                control.bind('<Return>', lambda e, n=controls[i + 1]: n.focus_set())
        else:
            if isinstance(control, tk.Entry):
                control.bind('<Return>', lambda e: function())


def draw_segment(seg, color, width, zorder, reverse=False):
    """Dibujamos los segmentos, con sus líneas y flechas corresponientes para
    indicarnos el destino del segmento"""
    dx = seg.destination.x - seg.origin.x
    dy = seg.destination.y - seg.origin.y
    length = math.sqrt(dx ** 2 + dy ** 2)
    if length > 0:
        dx /= length
        dy /= length
        if not reverse:
            ax.arrow(seg.origin.x, seg.origin.y,
                     dx * 0.99 * length, dy * 0.99 * length,
                     head_width=0.1, head_length=0.1,
                     fc=color, ec=color,
                     length_includes_head=True,
                     linewidth=width,
                     zorder=zorder)
        else:
            ax.arrow(seg.destination.x, seg.destination.y,
                     -dx * 0.99 * length, -dy * 0.99 * length,
                     head_width=0.1, head_length=0.1,
                     fc=color, ec=color,
                     length_includes_head=True,
                     linewidth=width,
                     zorder=zorder)

def finding_shortest_path(graph, start_node, end_node):
    """Esta función encuentra el camino más corto entre dos nodos y lo retorna"""
    distances = {node: float('inf') for node in graph.nodes}
    previous_nodes = {node: None for node in graph.nodes}
    distances[start_node] = 0
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node.name, start_node))

    while priority_queue:
        current_distance, _, current_node = heapq.heappop(priority_queue)
        if current_node == end_node:
            break
        if current_distance > distances[current_node]:
            continue

        for neighbor in current_node.neighbors:
            # Find the connecting segment
            segment = None
            for s in graph.segments:
                if s.origin == current_node and s.destination == neighbor:
                    segment = s
                    break

            if not segment:
                continue

            distance = current_distance + segment.cost
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor.name, neighbor))

    # Reconstruct path
    path = []
    current = end_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes.get(current, None)

    if distances[end_node] != float('inf'):
        path_obj = Path(f"{start_node.name}_to_{end_node.name}", start_node, end_node, distances[end_node])
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            for seg in graph.segments:
                if seg.origin == from_node and seg.destination == to_node:
                    path_obj.AddNodeToPath(to_node, seg)
                    break
        return path_obj
    return None

def search_closest_path(node_from,node_to,event=None):
    """Guarda la información introducida en las entradas anteriores"""
    global G  # Use the current graph
    from_node = SearchNode(G, node_from)
    to_node = SearchNode(G, node_to)
    if not from_node:
        not_valid(),message(f"Node '{node_from}' doesn't exist")
        return
    if not to_node:
        not_valid(),message(f"Node '{node_to}' doesn't exist")
        return
    path_obj = finding_shortest_path(G, from_node, to_node)  # Pass the current graph
    if path_obj:
        path_names = " → ".join([node.name for node in path_obj.nodes])
        PlotPath(G, path_obj)
        message(f"Shortest path from {node_from} to {node_to}: {path_names} (Distance: {path_obj.cost:.2f})")
    else:
        message(f"No path exists from {node_from} to {node_to}")
    """e_path_to.delete(0, 'end')
    e_path_from.delete(0, 'end') Potser ho necessitem"""

def PlotAllPaths(node_name):
    '''Resalta todos los caminos de un nodo establecido con anterioridad'''
    global fig, ax, canvas, G  # Use the current graph
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
    ax.set_axisbelow(True)
    start_node = SearchNode(G, node_name)
    if not start_node:
        not_valid(),message(f"Node '{node_name}' doesn't exist")
        return
    visited = set()
    path_segments = set()
    queue = [start_node]
    visited.add(start_node)
    while queue:
        current_node = queue.pop(0)
        for seg in [s for s in G.segments if s.origin == current_node]:
            neighbor = seg.destination
            path_segments.add(seg)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    # Dibuja,os los nodos
    for node in G.nodes:
        color = 'gray'
        if node == start_node:
            color = 'red'
        elif node in visited:
            color = 'pink'
        ax.plot(node.x, node.y, 'o', color=color, markersize=8, zorder=3)
        ax.text(node.x, node.y, node.name,
                color='black', ha='left', va='bottom', zorder=4)
    # Dibujamos los segmentos
    for seg in G.segments:
        dx = seg.destination.x - seg.origin.x
        dy = seg.destination.y - seg.origin.y
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length > 0:
            dx /= length
            dy /= length
            if seg in path_segments:
                arrow_color = 'blue'
                z = 2
            else:
                arrow_color = 'gray'
                z = 1
            ax.arrow(seg.origin.x, seg.origin.y,
                     dx * 0.95 * length, dy * 0.95 * length,
                     head_width=0.1, head_length=0.3,
                     fc=arrow_color, ec=arrow_color,
                     length_includes_head=True,
                     width=0.001,
                     zorder=z)
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
    message(f"Showing paths from node {node_name}")

def search_paths(e_paths, event=None):
    '''Guardamos la información introducida en las entradas'''
    node_name = e_paths.strip()
    if not node_name:
        not_valid(),message("Please enter a node name")
        return
    PlotAllPaths(node_name)
    e_paths.delete(0, 'end')

def find_closest_path(e_path_from,e_path_to):
    """Introducimos los botones que usaremos para encontrar el camino más corto
    y las diferentes entradas donde introduciremos nuestros nodos"""
    epf = SearchNode(G,e_path_from)
    ept = SearchNode(G, e_path_to)
    if epf==None:
        epf=G.nodes[0]
    if ept==None:
        ept=G.nodes[1]
    finding_shortest_path(G, epf, ept)
    search_closest_path(epf, ept, event=None)
    path_shortest = [epf, ept]
    work_with_entry(path_shortest, search_closest_path)


def show_paths(e_paths):
    """Muestra todos los posibles caminos de un nodo establecido"""
    global G  # Make sure we're using the current graph

    """for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) not in (1, 5):
            widget.destroy()"""

    PlotAllPaths(e_paths)
    search_paths(e_paths, event=None)

    paths_entry = [e_paths]
    work_with_entry(paths_entry, search_paths)