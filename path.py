from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox
import heapq
from Create_New_Graph import *

root = tk.Tk()
current_display_mode = "edited"
message_label = None
clear_timer = None
fig = Figure(figsize=(8.5, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = None

def set_graph(graph_instance):
    global G
    G = graph_instance

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
        anchor="w"
    )
    message_label.pack(fill="x", expand=True)

def clear_message(delay=0):
    """Clear the message after a delay"""
    def clear():
        message_label.config(text="")
    global clear_timer
    if clear_timer:
        root.after_cancel(clear_timer)
    if delay > 0:
        clear_timer = root.after(int(delay * 1000), lambda: message_label.config(text=""))
    else:
        clear()

def show_message(message, is_error=False, persistent=False):
    """Display a message in the GUI message area"""
    global message_label
    if message_label is None:
        create_message_area()
    clear_message()
    if is_error:
        formatted_message = f"Error: {message}"
        message_label.config(fg="red")
        messagebox.showerror("Error", message)
    else:
        formatted_message = message
        message_label.config(fg="black")
    message_label.config(text=formatted_message)
    message_label.update_idletasks()
    if not persistent:
        if is_error:
            clear_message(delay=5)
        else:
            clear_message(delay=3)

def draw_segment(seg, color, width, zorder, reverse=False):
    """Helper function to draw a segment with proper styling"""
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

def highlight_path(path):
    """Highlights paths of interest to display them in the GUI"""
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.7, color='#AA336A')
    ax.set_axisbelow(True)

    for node in G.nodes:
        color = 'gray'
        if node in path:
            color = 'green' if node != path[0] and node != path[-1] else 'blue'
        ax.plot(node.x, node.y, 'o', color=color, markersize=8, zorder=4)
        ax.text(node.x, node.y, node.name, fontsize=10, zorder=5)

    path_segments = set()
    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        path_segments.add((from_node.name, to_node.name))
        path_segments.add((to_node.name, from_node.name))

    for seg in G.segments:
        if (seg.origin.name, seg.destination.name) not in path_segments:
            draw_segment(seg, color='#CCCCCC', width=1, zorder=1)

    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        seg = None
        for s in G.segments:
            if s.origin == from_node and s.destination == to_node:
                seg = s
                break
        if seg:
            draw_segment(seg, color='red', width=2, zorder=3)
        else:
            for s in G.segments:
                if s.origin == to_node and s.destination == from_node:
                    draw_segment(s, color='red', width=2, zorder=3, reverse=True)
                    break
    canvas.draw()

def finding_shortest_path(graph, start_node, end_node):
    """Finds the minimum distance between two nodes using Dijkstra's algorithm"""
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
            # Find the segment
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
        return path, distances[end_node]
    else:
        return None, None

def find_closest_path():
    """Set of entries/buttons to find the shortest path between two nodes"""
    tk.Label(root, text="Find the closest path between two nodes:").grid(row=1, column=3)
    tk.Label(root, text="From").grid(row=2, column=2)
    tk.Label(root, text="To").grid(row=3, column=2)
    e_path_from = tk.Entry(root)
    e_path_from.grid(row=2, column=3)
    e_path_to = tk.Entry(root)
    e_path_to.grid(row=3, column=3)

    def search_closest_path():
        """Finds the shortest path between two nodes"""
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

        path, total_distance = finding_shortest_path(G, from_node, to_node)
        if path:
            path_names = " → ".join([node.name for node in path])
            highlight_path(path)
            show_message(f"Shortest path from {node_from} to {node_to}: {path_names} (Distance: {total_distance:.2f})")
        else:
            show_message(f"No path exists from {node_from} to {node_to}", is_error=True)

        e_path_to.delete(0, 'end')
        e_path_from.delete(0, 'end')

    search_btn = tk.Button(
        root,
        text='Find closest path',
        command=search_closest_path,
        cursor='hand2'
    )
    search_btn.grid(row=4, column=3)

def show_paths():
    """Shows all paths from a node"""
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) not in (1, 5):  # Keep main buttons and canvas
            widget.destroy()

    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_paths = tk.Entry(root)
    e_paths.grid(row=0, column=3)

    def search_paths():
        node_name = e_paths.get().strip()
        if not node_name:
            show_message("Please enter a node name", is_error=True)
            return
        highlight_paths(node_name)
        e_paths.delete(0, 'end')

    search_btn = tk.Button(
        root,
        text='Show paths',
        command=lambda: search_paths(),
        cursor='hand2'
    )
    search_btn.grid(row=0, column=4)

def highlight_paths(node_name):
    """Highlights all paths from a given node"""
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

    # Draw nodes
    for node in G.nodes:
        color = 'gray'
        if node == start_node:
            color = 'red'
        elif node in visited:
            color = 'pink'
        ax.plot(node.x, node.y, 'o', color=color, markersize=8, zorder=3)
        ax.text(node.x, node.y, node.name,
                color='black', ha='left', va='bottom', zorder=4)

    # Draw segments
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

