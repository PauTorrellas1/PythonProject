from graph import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import heapq
import math


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
    if 'ax' not in globals():
        fig = Figure(figsize=(8.5, 7), dpi=100)
        ax = fig.add_subplot(111)
    else:
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
    if 'canvas' not in globals() or not canvas.get_tk_widget().winfo_exists():
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
    else:
        canvas.draw()
    show_message(f"Displaying path from {path.origin.name} to {path.destination.name}")

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
        if is_real_map(graph):
            # AirSpace version
            start_point = next((p for p in graph.nav_points if p['name'] == start_node.name), None)
            end_point = next((p for p in graph.nav_points if p['name'] == end_node.name), None)

            if not start_point or not end_point:
                return None

            # Dijkstra's algorithm implementation for real maps
            distances = {p['name']: float('inf') for p in graph.nav_points}
            previous = {p['name']: None for p in graph.nav_points}
            distances[start_node.name] = 0
            queue = [(0, start_node.name)]

            while queue:
                current_dist, current_name = heapq.heappop(queue)
                if current_name == end_node.name:
                    break

                if current_dist > distances[current_name]:
                    continue

                current_point = next(p for p in graph.nav_points if p['name'] == current_name)
                for seg in [s for s in graph.nav_segments if s['origin_id'] == current_point['id']]:
                    neighbor = next(p for p in graph.nav_points if p['id'] == seg['dest_id'])
                    new_dist = current_dist + seg['distance']
                    if new_dist < distances[neighbor['name']]:
                        distances[neighbor['name']] = new_dist
                        previous[neighbor['name']] = current_name
                        heapq.heappush(queue, (new_dist, neighbor['name']))

            # Path reconstruction
            path = []
            current = end_node.name
            while current:
                path.insert(0, current)
                current = previous.get(current)

            if distances[end_node.name] != float('inf'):
                # Corrected segment filtering
                path_segments = []
                for p, q in zip(path[:-1], path[1:]):
                    p_id = next(point['id'] for point in graph.nav_points if point['name'] == p)
                    q_id = next(point['id'] for point in graph.nav_points if point['name'] == q)
                    segment = next((s for s in graph.nav_segments
                                    if s['origin_id'] == p_id and s['dest_id'] == q_id), None)
                    if segment:
                        path_segments.append(segment)

                return {
                    'path': path,
                    'distance': distances[end_node.name],
                    'points': [p for p in graph.nav_points if p['name'] in path],
                    'segments': path_segments
                }
            return None
        else:
            # Original graph version
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
            return None

    def highlight_path(path_data):
        """Remarcamos los caminos mostrados en la GUI usando el objeto Path"""
        global fig, ax, canvas

        # Clear the plot
        ax.clear()

        if isinstance(path_data, dict):  # AirSpace path
            # Get all point names in the path for easy lookup
            path_point_names = set(path_data['path'])

            # Plot all points first (gray)
            for point in G.nav_points:
                # Determine point color
                if point['name'] == path_data['path'][0]:  # Origin
                    color = 'blue'
                    markersize = 8
                elif point['name'] == path_data['path'][-1]:  # Destination
                    color = 'red'
                    markersize = 8
                elif point['name'] in path_point_names:  # Path point
                    color = 'green'
                    markersize = 7
                else:  # Regular point
                    color = 'gray'
                    markersize = 5

                ax.plot(point['lon'], point['lat'], 'o',
                        color=color,
                        markersize=markersize,
                        zorder=3)
                ax.text(point['lon'] + 0.05, point['lat'] + 0.05,
                        point['name'],
                        fontsize=8,
                        zorder=4)

            # Plot all segments first (gray)
            for seg in G.nav_segments:
                origin = next((p for p in G.nav_points if p['id'] == seg['origin_id']), None)
                dest = next((p for p in G.nav_points if p['id'] == seg['dest_id']), None)

                if not origin or not dest:
                    continue  # Skip if points not found

                # Check if this segment is in the path
                is_path_segment = False
                for i in range(len(path_data['path']) - 1):
                    if (origin['name'] == path_data['path'][i] and
                            dest['name'] == path_data['path'][i + 1]):
                        is_path_segment = True
                        break
                    if (dest['name'] == path_data['path'][i] and
                            origin['name'] == path_data['path'][i + 1]):
                        is_path_segment = True
                        break

                if is_path_segment:
                    # Path segment - red
                    ax.plot([origin['lon'], dest['lon']],
                            [origin['lat'], dest['lat']],
                            'r-', linewidth=2, zorder=2)
                else:
                    # Regular segment - gray
                    ax.plot([origin['lon'], dest['lon']],
                            [origin['lat'], dest['lat']],
                            '#CCCCCC', linewidth=1, zorder=1)

                # Add distance label for all segments
                ax.text((origin['lon'] + dest['lon']) / 2,
                        (origin['lat'] + dest['lat']) / 2,
                        f"{seg['distance']:.1f}",
                        fontsize=8,
                        zorder=3)
        else:
            # Original graph path plotting (keep existing style)
            PlotPath(G, path_data)

        # Common plot settings
        ax.grid(color="#717171", linestyle="--")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Airspace Map")

        # Update the canvas
        canvas.draw()

    def search_closest_path(event=None):
        node_from = e_path_from.get().strip()
        node_to = e_path_to.get().strip()

        if is_real_map(G):
            # AirSpace handling
            from_point = next((p for p in G.nav_points if p['name'] == node_from), None)
            to_point = next((p for p in G.nav_points if p['name'] == node_to), None)

            if not from_point or not to_point:
                show_message(f"One or both nodes not found", is_error=True)
                return

            # Create consistent node objects
            from_node = SimpleNamespace(name=from_point['name'],
                                        x=from_point['lon'],
                                        y=from_point['lat'])
            to_node = SimpleNamespace(name=to_point['name'],
                                      x=to_point['lon'],
                                      y=to_point['lat'])

            path_data = finding_shortest_path(G, from_node, to_node)
        else:
            # Original graph handling
            from_node = SearchNode(G, node_from)
            to_node = SearchNode(G, node_to)
            if not from_node or not to_node:
                show_message(f"One or both nodes not found", is_error=True)
                return
            path_data = finding_shortest_path(G, from_node, to_node)

        if path_data:
            highlight_path(path_data)
            if isinstance(path_data, dict):
                show_message(f"Path found with distance: {path_data['distance']:.2f}")
            else:  # It's a Path object
                show_message(f"Path found with distance: {path_data.cost:.2f}")
        else:
            show_message(f"No path exists between {node_from} and {node_to}", is_error=True)
    search_btn = tk.Button(
        root,
        text='Find Path',
        command=search_closest_path,
        cursor='hand2')
    search_btn.grid(row=4, column=3)
    work_with_entry([e_path_from, e_path_to], search_closest_path)

def show_paths():
    """Muestra todos los posibles caminos de un nodo establecido"""
    global G  # Make sure we're using the current graph
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_paths = tk.Entry(root)
    e_paths.grid(row=0, column=3)

    def PlotAllPaths(node_name):
        '''Resalta todos los caminos de un nodo establecido con anterioridad'''
        global fig, ax, canvas, G  # Use the current graph
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

