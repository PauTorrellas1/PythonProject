from matplotlib.figure import Figure
from graph import *
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox
import heapq
import time
import math

root = tk.Tk()
current_display_mode = "edited"
message_label = None
clear_timer = None
error_window = None
fig = Figure(figsize=(8.5, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)


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
    '''Plots the Path in the Graph'''
    global fig, ax, canvas
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
    ax.set_axisbelow(True)
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
    for seg in graph.segments:
        is_path_segment = False
        for path_seg in path.segments:
            if (seg.origin == path_seg.origin and seg.destination == path_seg.destination):
                is_path_segment = True
                break
        if is_path_segment:
            draw_segment(seg, color='red', width=2, zorder=2)
        else:
            draw_segment(seg, color='#CCCCCC', width=1, zorder=1)
    canvas.draw()
    show_message(
        f"Displaying path '{path.name}' from {path.origin.name} to {path.destination.name} (Cost: {path.cost:.2f})")

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
                     dx * 0.95 * length, dy * 0.95 * length,
                     head_width=0.5, head_length=0.5,
                     fc=color, ec=color,
                     length_includes_head=True,
                     linewidth=width,
                     zorder=zorder)
        else:
            ax.arrow(seg.destination.x, seg.destination.y,
                     -dx * 0.95 * length, -dy * 0.95 * length,
                     head_width=0.5, head_length=0.5,
                     fc=color, ec=color,
                     length_includes_head=True,
                     linewidth=width,
                     zorder=zorder)

def find_closest_path_entries():
    """Introducimos los botones que usaremos para encontrar el camino más corto
    y las diferentes entradas donde introduciremos nuestros nodos"""
    tk.Label(root, text="Find the closest path between two nodes:").grid(row=1, column=3)
    tk.Label(root, text="From").grid(row=2, column=2)
    tk.Label(root, text="To").grid(row=3, column=2)
    e_path_from = tk.Entry(root)
    e_path_from.grid(row=2, column=3)
    e_path_to = tk.Entry(root)
    e_path_to.grid(row=3, column=3)

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
                # Buscamos el segmento
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
        else:
            return None

    def highlight_path(path_obj):
        """Remarcamos los caminos mostrados en la GUI usando el objeto Path"""
        PlotPath(G, path_obj)

    def search_closest_path(event=None):
        """Guarda la información introducida en las entradas anteriores"""
        node_from = e_path_from.get().strip()
        node_to = e_path_to.get().strip()
        from_node = SearchNode(G, node_from)
        to_node = SearchNode(G, node_to)
        if not from_node:
            show_message(f"Node '{node_from}' doesn't exist", is_error=True)
            e_path_from.delete(0, 'end')
            return
        if not to_node:
            show_message(f"Node '{node_to}' doesn't exist", is_error=True)
            e_path_to.delete(0, 'end')
            return
        path_obj = finding_shortest_path(G, from_node, to_node)
        if path_obj:
            path_names = " → ".join([node.name for node in path_obj.nodes])
            highlight_path(path_obj)
            show_message(f"Shortest path from {node_from} to {node_to}: {path_names} (Distance: {path_obj.cost:.2f})")
        else:
            show_message(f"No path exists from {node_from} to {node_to}", is_error=True)
        e_path_to.delete(0, 'end')
        e_path_from.delete(0, 'end')
    path_shortest = [e_path_from, e_path_to]
    work_with_entry(path_shortest, search_closest_path)
    search_btn = tk.Button(
        root,
        text='Find closest path',
        command=search_closest_path,
        cursor='hand2')
    search_btn.grid(row=4, column=3)

def show_paths():
    """Muestra todos los posibles caminos de un nodo establecido"""
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) not in (1, 5):  # Borramos todos lo widgets (entradas) anteriores
            widget.destroy()
    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_paths = tk.Entry(root)
    e_paths.grid(row=0, column=3)

    def PlotAllPaths(node_name):
        '''Resalta todos los caminos de un nodo establecido con anterioridad'''
        global fig, ax, canvas, G
        ax.clear()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
        ax.set_axisbelow(True)
        start_node = SearchNode(G, node_name)
        if not start_node:
            show_message(f"Node '{node_name}' doesn't exist", is_error=True)
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
                         head_width=0.5, head_length=0.5,
                         fc=arrow_color, ec=arrow_color,
                         length_includes_head=True,
                         width=0.001,
                         zorder=z)
        if canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
        show_message(f"Showing paths from node {node_name}")

    def search_paths(event=None):
        '''Guardamos la información introducida en las entradas'''
        node_name = e_paths.get().strip()
        if not node_name:
            show_message("Please enter a node name", is_error=True)
            return
        PlotAllPaths(node_name)
        e_paths.delete(0, 'end')

    paths_entry = [e_paths]
    work_with_entry(paths_entry, search_paths)
    search_btn = tk.Button(
        root,
        text='Show paths',
        command=lambda: search_paths(),
        cursor='hand2')
    search_btn.grid(row=0, column=4)

