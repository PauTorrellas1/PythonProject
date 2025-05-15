from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from Create_New_Graph import *
import tkinter as tk
from tkinter import messagebox
import threading
import heapq
from matplotlib.patches import ArrowStyle

'''create new graph falta interfaz'''
root = tk.Tk()
current_display_mode = "edited"
message_label = None
clear_timer = None
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = None

def create_message_area():
    """Create the message display area at the bottom of the GUI"""
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

def CreateGraph_1 ():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
    AddSegment(G, "BK","B","K")
    AddSegment(G, "BG","B","G")
    AddSegment(G, "CD","C","D")
    AddSegment(G, "CG","C","G")
    AddSegment(G, "DG","D","G")
    AddSegment(G, "DH","D","H")
    AddSegment(G, "DI","D","I")
    AddSegment(G, "EF","E","F")
    AddSegment(G, "FL","F","L")
    AddSegment(G, "GB","G","B")
    AddSegment(G, "GF","G","F")
    AddSegment(G, "GH","G","H")
    AddSegment(G, "ID","I","D")
    AddSegment(G, "IJ","I","J")
    AddSegment(G, "JI","J","I")
    AddSegment(G, "KA","K","A")
    AddSegment(G, "KL","K","L")
    AddSegment(G, "LK","L","K")
    AddSegment(G, "LF","L","F")
    return G

def show_new_graph():
    '''Establecemos que gráfico debe mostrar la GUI'''
    global fig, ax, canvas
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color= '#AA336A')
    ax.set_axisbelow(True)

    for seg in G.segments:
        dx = seg.destination.x - seg.origin.x
        dy = seg.destination.y - seg.origin.y
        length = math.sqrt(dx ** 2 + dy ** 2)

        if length > 0:
            dx /= length
            dy /= length
            ax.arrow(
                seg.origin.x, seg.origin.y,
                dx * length * 0.95,  # 95% of length to leave space for arrowhead
                dy * length * 0.95,
                head_width=0.4,
                head_length=0.5,
                fc='blue',
                ec='blue',
                length_includes_head=True,
                width=0.001,
                zorder=1
            )
        ax.text((seg.origin.x + seg.destination.x) / 2 + 0.3,
                (seg.origin.y + seg.destination.y) / 2 + 0.3,
                f"{seg.cost:.2f}",
                zorder=4, fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    for node in G.nodes:
        ax.plot(node.x, node.y, 'ro', markersize=8)
        ax.text(node.x, node.y, node.name, fontsize=10)
    if canvas is None:
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
    else:
        canvas.draw()

show_message("Probando el grafo...")
original_G = CreateGraph_1()
edited_G = CreateGraph_1()  #Hacemos una copia del gráfico original, donde se mostrarán todas las ediciones hechas por nosotros
G = edited_G  # El gráfico mostrado será el editado (a espera de algún cambio)
root.title("GUI")
create_message_area()
show_new_graph()
path_info_frame = tk.Frame(root)
path_info_frame.grid(row=19, column=5, sticky="ew", padx=10, pady=5)

path_info_text = tk.Text(
    path_info_frame,
    height=4,
    wrap=tk.WORD,
    font=("Arial", 10),
    bg="white",
    fg="black",
    relief=tk.FLAT
)
path_info_text.pack(fill=tk.BOTH, expand=True)

def draw_segment_with_arrow(ax, seg):
    '''Helper function to draw a single segment with arrow'''
    dx = seg.destination.x - seg.origin.x
    dy = seg.destination.y - seg.origin.y
    length = math.sqrt(dx ** 2 + dy ** 2)

    if length > 0:
        dx /= length
        dy /= length
    # Draw arrow (positioned at 80% of length)
    arrow_length = 0.8 * length
    ax.arrow(seg.origin.x, seg.origin.y,
             dx * arrow_length, dy * arrow_length,
             head_width=0.3, head_length=0.4,
             fc='#979797', ec='#979797',
             length_includes_head=True,
             zorder=3)

    # Check for bidirectional
    is_bidirectional = any(
        s.origin == seg.destination and s.destination == seg.origin
        for s in G.segments
    )

    if is_bidirectional:
        ax.arrow(seg.destination.x, seg.destination.y,
                 -dx * arrow_length, -dy * arrow_length,
                 head_width=0.3, head_length=0.4,
                 fc='#979797', ec='#979797',
                 length_includes_head=True,
                 zorder=3)

    # Add cost text
    ax.text((seg.origin.x + seg.destination.x) / 2 + 0.3,
            (seg.origin.y + seg.destination.y) / 2 + 0.3,
            f"{seg.cost:.2f}",
            zorder=4, fontsize=8,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

def show_graph():
    '''Show the original graph'''
    global current_display_mode, G
    current_display_mode = "original"
    G = original_G
    restore_main_view()
    show_new_graph()
    show_message("Showing original graph")

def show_graph_1():
    '''Show the edited graph'''
    global current_display_mode, G
    current_display_mode = "edited"
    G = edited_G
    restore_main_view()
    show_new_graph()
    show_message("Showing edited graph")

def restore_main_view():
    '''Restore all main view widgets'''
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    Entries()
    show_new_graph()

def print_graph_info():
    """Muestra todos los nodos y segmentos dentro del GUI"""
    def save_info():
        '''Guarda toda la información de los nodos y segmentos en un archivo que se puede abrir después'''
        with open('Graph information', 'w') as graph_info:
            if hasattr(G, 'nodes') and G.nodes:
                for node in G.nodes:
                    graph_info.write(f'N,{node.name},{node.x},{node.y}\n')
            else:
                show_message('There are not any nodes in the graph', is_error=True)
            if hasattr(G, 'segments') and G.segments:
                for segment in G.segments:
                    graph_info.write(f'S,{segment.name},{segment.origin.name},{segment.destination.name}\n')
            else:
                show_message('There are not any segments in the graph', is_error=True)

    global G
    info_window = tk.Toplevel(root)
    info_window.title("Graph Information")

    text_frame = tk.Frame(info_window)
    text_frame.pack(fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_widget.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    '''Opciones de visualización de la ventana donde observamos todos los nodos y segmentos del gráfico'''

    info_text = "=== GRAPH INFORMATION ===\n\n"

    if hasattr(G, 'nodes') and G.nodes:
        info_text += "NODES:\n"
        for node in G.nodes:
            info_text += f"- {node.name}: (x={node.x}, y={node.y})\n"
    else:
        info_text += "No nodes in the graph\n"
    info_text += "\n"
    if hasattr(G, 'segments') and G.segments:
        info_text += "SEGMENTS:\n"
        for segment in G.segments:
            dist = Distance(segment.origin, segment.destination)
            info_text += f"- {segment.name}: {segment.origin.name} -> {segment.destination.name} (Distance: {dist})\n"
    else:
        info_text += "No segments in the graph\n"
    text_widget.insert(tk.END, info_text)
    '''Mostramos toda la información guardada, es decir, los Nodos y sus posiciones, 
    y los segmentos y sus nombres, los respectivos nodos que los forman y el 
    coste de cada uno de ellos'''

    save_button = tk.Button(info_window, text='Save the information', command=lambda: [save_info(), info_window.destroy()])
    save_button.pack(pady=9)
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=10)

def show_neighbors():
    '''Show the neighbors of a node'''
    for widget in root.winfo_children():
        if widget.grid_info().get("row", 0) == 0 and widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_neighbor = tk.Entry(root)
    e_neighbor.grid(row=0, column=3)
    def search_and_clear():
        node_name = e_neighbor.get().strip()
        highlight_neighbors(node_name)
        e_neighbor.delete(0, 'end')
    search_btn = tk.Button(
        root,
        text='Show Neighbors',
        command=lambda: search_and_clear(),
        cursor='hand2'
    )
    search_btn.grid(row=0, column=4)

def highlight_neighbors(node_name):
    '''Highlight neighbors of a node'''
    global fig, ax, canvas
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)
    node_name = node_name.strip()
    if not node_name:
        show_message("Enter a node name", is_error=True)
        return
    node = SearchNode(G, node_name)
    if not node:
        show_message(f"Node '{node_name}' doesn't exist", is_error=True)
        return
    if not node.neighbors:
        show_message(f"Node '{node_name}' has no neighbors", is_error=True)
        return
    for seg in G.segments:
        dx = seg.destination.x - seg.origin.x
        dy = seg.destination.y - seg.origin.y
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length > 0:
            dx /= length
            dy /= length
    for neighbor in node.neighbors:
        seg = next((s for s in G.segments if
                    s.origin == node and s.destination == neighbor), None)
        if seg:
            dx = neighbor.x - node.x
            dy = neighbor.y - node.y
            length = math.sqrt(dx ** 2 + dy ** 2)
            if length > 0:
                dx /= length
                dy /= length
            ax.plot([node.x, neighbor.x],
                    [node.y, neighbor.y],
                    'r-', linewidth=2)
            ax.arrow(node.x, node.y,
                     dx * 0.95 * length, dy * 0.95 * length,
                     head_width=0.5, head_length=0.5,
                     fc='red', ec='red',
                     length_includes_head=True)
    for n in G.nodes:
        color = 'gray'
        if n == node:
            color = 'blue'
        elif n in node.neighbors:
            color = 'green'
        ax.plot(n.x, n.y, 'o', color=color, markersize=8)
        ax.text(n.x, n.y, n.name, color='black', ha='left', va='bottom')
    ax.plot(node.x, node.y, 'blue', markersize=8)
    ax.text(node.x, node.y, node.name, color='black', ha='left', va='bottom')
    if 'canvas' in globals() and canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)

def show_paths():
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) not in (1,5):  # Keep main buttons and canvas
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
        text='Show paths from the node',
        command=lambda: search_paths(),
        cursor='hand2'
    )
    search_btn.grid(row=0, column=4)

    def highlight_paths(node_name):
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
        for node in G.nodes:
            color = 'gray'
            if node == start_node:
                color = 'red'
            elif node in visited:
                color = 'pink'
            ax.plot(node.x, node.y, 'o', color=color, markersize=8, zorder=3)
            ax.text(node.x, node.y, node.name,
                    color='black', ha='left', va='bottom', zorder=4)
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

def show_path_info(node_from, node_to, path_names, total_distance):
    """Display path information in the dedicated area below the map"""
    path_info_text.config(state=tk.NORMAL)
    path_info_text.delete(1.0, tk.END)
    info = (f"Shortest path from {node_from} to {node_to}:\n"
            f"Path: {path_names}\n"
            f"Total distance: {total_distance:.2f}")
    path_info_text.insert(tk.END, info)
    path_info_text.config(state=tk.DISABLED)

def find_closest_path():
    tk.Label(root, text="Find the closest path between two nodes:").grid(row=1, column=3)
    tk.Label(root, text="From").grid(row=2, column=2)
    tk.Label(root, text="To").grid(row=3, column=2)
    e_path_from = tk.Entry(root)
    e_path_from.grid(row=2, column=3)
    node_from = e_path_from.get().strip()
    e_path_to = tk.Entry(root)
    e_path_to.grid(row=3, column=3)
    node_to = e_path_to.get().strip()

    def highlight_path(path):
        """Highlights a path on the graph visualization with proper layering"""
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

    def search_closest_path():
        node_from = e_path_from.get().strip()  # Get from entry widget
        node_to = e_path_to.get().strip()  # Get from entry widget
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
            show_path_info(node_from, node_to, path_names, total_distance)
            highlight_path(path)
        else:
            show_message(f"No path exists from {node_from} to {node_to}", is_error=True)
        e_path_to.delete(0, 'end')
        e_path_from.delete(0, 'end')

    def finding_shortest_path(graph, start_node, end_node):
        """Finds the shortest path from start_node to end_node using Dijkstra's algorithm"""
        distances = {node: float('inf') for node in graph.nodes}
        previous_nodes = {node: None for node in graph.nodes}
        distances[start_node] = 0

        # Use a tuple with (distance, node.name, node) to ensure proper comparison
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_node.name, start_node))

        while priority_queue:
            current_distance, _, current_node = heapq.heappop(priority_queue)

            if current_node == end_node:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor in current_node.neighbors:
                segment = next(s for s in graph.segments
                               if s.origin == current_node and s.destination == neighbor)

                distance = current_distance + segment.cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    # Push with node.name to ensure comparable tuples
                    heapq.heappush(priority_queue, (distance, neighbor.name, neighbor))

        # Reconstruct path
        path = []
        current = end_node
        while current is not None:
            path.insert(0, current)
            current = previous_nodes.get(current, None)

        if distances[end_node] != float('inf'):
            return path, distances[end_node]
        else:
            return None, None

    search_btn = tk.Button(
        root,
        text='Show paths from the node',
        command=search_closest_path,
        cursor='hand2'
    )
    search_btn.grid(row= 4, column = 3)

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

def create_new_graph():
    '''Creamos un nuevo gráfico en blanco'''
    global edited_G, G, current_display_mode
    edited_G = Graph()
    G = edited_G
    current_display_mode = "edited"
    restore_main_view()
    show_new_graph()
    show_message("Created new empty graph")

def confirm_new_graph():
    """Shows a confirmation dialog before creating new graph"""
    confirm_window = tk.Toplevel(root)
    confirm_window.title("Confirm")
    confirm_window.transient(root)
    confirm_window.grab_set()
    confirm_window.resizable(False, False)
    window_width = 300
    window_height = 150
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    confirm_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def on_yes_confirm():
        confirm_window.destroy()
        create_new_graph()
    warning_text = tk.Text(confirm_window,
                           height=3,
                           wrap=tk.WORD,
                           bg='white',
                           fg='black',
                           relief=tk.FLAT,
                           font=('Arial', 10),
                           padx=10,
                           pady=5)
    warning_text.insert(tk.END, "Are you sure you want to create a new graph?\n", 'black')
    warning_text.insert(tk.END, "All unsaved changes will be lost.\n", 'red')
    warning_text.insert(tk.END, "We recommend saving your previous graph first.", 'black')
    warning_text.tag_config('black', foreground='black')
    warning_text.tag_config('red', foreground='red')
    warning_text.config(state=tk.DISABLED)
    warning_text.pack(pady=10)
    button_frame = tk.Frame(confirm_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame,
              text="Yes, continue",
              command=on_yes_confirm,
              width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame,
              text="No, cancel",
              command=confirm_window.destroy,
              width=12).pack(side=tk.RIGHT, padx=10)
    confirm_window.grab_set()
    confirm_window.wait_window()

def add_node_to_new_graph(name_entry, x_entry, y_entry):
    '''Está función añade nodos al nuevo gráfico'''
    global G
    name = name_entry.get().strip()
    x_str = x_entry.get().strip()
    y_str = y_entry.get().strip()
    if not name or not x_str or not y_str:
        show_message("All the entries must be filled", is_error=True)
        return
    try:
        x = float(x_str)
        y = float(y_str)
    except ValueError:
        show_message("The coordinates must be numbers", is_error=True)
        return
    if SearchNode(G, name):
        show_message(f'The node "{name}" already exists', is_error=True)
        return
    AddNode(G, Node(name, x, y))
    show_new_graph()
    name_entry.delete(0, 'end')
    x_entry.delete(0, 'end')
    y_entry.delete(0, 'end')

def add_segment_to_new_graph(from_entry, to_entry):
    '''Con esta función añadimos segmentos entre dos
    nodos creados a nuestro nuevo gráfico'''
    global G
    from_node_name = from_entry.get().strip()
    to_node_name = to_entry.get().strip()
    if not from_node_name or not to_node_name:
        show_message("Both nodes must be specified", is_error=True)
        return
    from_node = SearchNode(G, from_node_name)
    to_node = SearchNode(G, to_node_name)
    if not from_node:
        show_message(f"Node '{from_node_name}' doesn't exist", is_error=True)
        return
    if not to_node:
        show_message(f"Node '{to_node_name}' doesn't exist", is_error=True)
        return
    e_seg = f"{from_node_name}{to_node_name}"
    #e_seg1 = f"{to_node_name}{from_node_name}"
    segment_exists = any(
        (s.name == e_seg) #or s.name == e_seg1
        for s in G.segments)
    if segment_exists:
        show_message(f"Segment between {from_node_name} and {to_node_name} already exists", is_error=True)
        return
    AddSegment(G, e_seg, from_node_name, to_node_name)
    #AddSegment(G, e_seg1, to_node_name, from_node_name)
    from_entry.delete(0, 'end')
    to_entry.delete(0, 'end')
    show_new_graph()

def delete_node_to_new_graph(entry_widget):
    '''Esta función elimina nodos del nuevo gráfico'''
    global G
    node_name = entry_widget.get().strip()
    if not node_name:
        show_message("You must enter a node name to delete", is_error=True)
        return
    node_to_delete = SearchNode(G, node_name)
    if not node_to_delete:
        show_message(f"Node '{node_name}' doesn't exist", is_error=True)
        entry_widget.delete(0, 'end')
        return
    DeleteNode(G, node_name)
    show_message(f"Node '{node_name}' deleted successfully")
    entry_widget.delete(0, 'end')
    show_new_graph()

def delete_segment_to_new_graph(e_delete_s):
    '''Eliminamos un segmento de nuestro gráfico'''
    segment_name = e_delete_s.get().strip()
    if not segment_name:
        show_message("You must write the name of the segment you want to delete.", is_error=True)
        e_delete_s.delete(0, 'end')
        return
    segment_to_delete = None
    for seg in G.segments:
        if seg.name == segment_name: #or seg.name == segment_name[::-1]:
            segment_to_delete = seg
            break
    if not segment_to_delete:
        show_message(f"It doesn't exists any segment called '{segment_name}'", is_error=True)
        e_delete_s.delete(0, 'end')
        return
    DeleteSegment(G, segment_to_delete.name)
    show_message(f"Segment '{segment_to_delete.name}' deleted successfully.")
    e_delete_s.delete(0, 'end')
    show_new_graph()

def button_show_original_graph():
    '''Mostramos el gráfico original con la información propporcionada'''
    button_show_original_graph = tk.Button(root,
                       text="Show original graph",
                       command=show_graph,
                       activebackground="blue",
                       activeforeground="white",
                       anchor="center",
                       bd=3,
                       bg="lightgray",
                       cursor="hand2",
                       disabledforeground="gray",
                       fg="black",
                       font=("Arial", 12),
                       height=2,
                       highlightbackground="black",
                       highlightcolor="green",
                       highlightthickness=2,
                       justify="center",
                       overrelief="raised",
                       padx=10,
                       pady=5,
                       width=15,
                       wraplength=100)

    button_show_original_graph.grid(row=0, column=1)

def button_show_edited_graph():
    '''Mostramos el nuevo gráfico editado por nosotros'''
    button_show_edited_graph = tk.Button(root,
                       text="Show edited graph",
                       command=show_graph_1,
                       activebackground="blue",
                       activeforeground="white",
                       anchor="center",
                       bd=3,
                       bg="lightgray",
                       cursor="hand2",
                       disabledforeground="gray",
                       fg="black",
                       font=("Arial", 12),
                       height=2,
                       highlightbackground="black",
                       highlightcolor="green",
                       highlightthickness=2,
                       justify="center",
                       overrelief="raised",
                       padx=10,
                       pady=5,
                       width=15,
                       wraplength=100)

    button_show_edited_graph.grid(row=1, column=1)

def button_create_new_graph():
    '''Creamos un nuevo gráfico a nuestro gusto. Esta opción abre una ventana nueva de tk
    donde podemos personalizar nuestro gráfico como queramos. Es esencialmente lo mismo que
    la ventana anterior con la diferencia que este gráfico está creado desde cero por nostros mismos'''
    button_create_new_graph = tk.Button(root,
                       text="Crete new graph",
                       command=confirm_new_graph,
                       activebackground="blue",
                       activeforeground="white",
                       anchor="center",
                       bd=3,
                       bg="lightgray",
                       cursor="hand2",
                       disabledforeground="gray",
                       fg="black",
                       font=("Arial", 12),
                       height=2,
                       highlightbackground="black",
                       highlightcolor="green",
                       highlightthickness=2,
                       justify="center",
                       overrelief="raised",
                       padx=10,
                       pady=5,
                       width=15,
                       wraplength=100)
    button_create_new_graph.grid(row=2, column=1)

def button_save_graph_info():
    ''''
    Este botón pretende guardar toda la información de un gráfico creado en un documento
    '''
    button_save_graph_info = tk.Button(root,
                        text="Save the information of the graph",
                        command=print_graph_info,
                        activebackground="blue",
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=2,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)

    button_save_graph_info.grid(row=3, column=1)

def button_show_paths():
    '''Este botón pretende que se puedan observar todos los caminos posibles de un nodo'''
    button_show_paths = tk.Button(root,
                                      text="Analyze paths",
                                      command=lambda: [func() for func in (show_paths, find_closest_path)],
                                      activebackground="blue",
                                      activeforeground="white",
                                      anchor="center",
                                      bd=3,
                                      bg="lightgray",
                                      cursor="hand2",
                                      disabledforeground="lightgray",
                                      fg="black",
                                      font=("Arial", 12),
                                      height=3,
                                      highlightbackground="black",
                                      highlightcolor="green",
                                      highlightthickness=2,
                                      justify="center",
                                      overrelief="raised",
                                      padx=10,
                                      pady=5,
                                      width=15,
                                      wraplength=100)

    button_show_paths.grid(row=5, column=1)

def button_show_neighbors():
    '''Este botón pretende que se puedan observar todos los nodos vecinos de un nodo'''
    button_show_neighbors = tk.Button(root,
                        text="Show the neighbors of a node",
                        command=show_neighbors,
                        activebackground="blue",
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="lightgray",
                        cursor="hand2",
                        disabledforeground="gray",
                        fg="black",
                        font=("Arial", 12),
                        height=3,
                        highlightbackground="black",
                        highlightcolor="green",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100)

    button_show_neighbors.grid(row=4, column=1)

button_show_original_graph()
button_show_edited_graph()
button_create_new_graph()
button_save_graph_info()
button_show_paths()
button_show_neighbors()

def Entries():
    '''Cada una de las entradas de texto que usaremos en el menú principal
    de nuestra aplicación. si llevan tk.Label son únicamente texto,
    mientras que si llevan tk.Entry son entradas de texto donde debemos escribir.
    Si llevan tk.Button son botones para presionar y llevar acabo una acción o comando.'''
    global e_name, e_x, e_y, e_from, e_to, e_delete_n, e_delete_s, e_file
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="File Name").grid(row=0, column=2)
    tk.Label(root, text="New node name").grid(row=1, column=2)
    tk.Label(root, text="X").grid(row=2, column=2)
    tk.Label(root, text="Y").grid(row=3, column=2)
    tk.Label(root, text="From").grid(row=5, column=2)
    tk.Label(root, text="To").grid(row=6, column=2)
    tk.Label(root, text="Delete Node").grid(row=8, column=2)
    tk.Label(root, text='Delete segment').grid(row=10, column=2)


    e_file = tk.Entry(root) #Primer entry
    e_name = tk.Entry(root) #New_node nombre
    e_x = tk.Entry(root) #New_node valor x
    e_y = tk.Entry(root) #New_node valor y
    e_from = tk.Entry(root) #Origen new_segment
    e_to = tk.Entry(root) #Destino new_segment
    e_delete_n = tk.Entry(root) #Delete node
    e_delete_s = tk.Entry(root) #Delete origin segment

    e_file.grid(row=0, column=3)
    e_name.grid(row=1, column=3)
    e_x.grid(row=2, column=3)
    e_y.grid(row=3, column=3)
    e_from.grid(row=5, column=3)
    e_to.grid(row=6, column=3)
    e_delete_n.grid(row=8, column=3)
    e_delete_s.grid(row=10, column=3)

    def entry1():
        '''Lee el texto de un documento determinado y nos muestra dicho gráfico'''
        global G, edited_G, current_display_mode
        try:
            new_graph = read_file(e_file.get())
            if new_graph.nodes:
                edited_G = new_graph
                G = edited_G
                current_display_mode = "edited"
                show_graph_1()
                show_message(f"Successfully loaded graph from {e_file.get()}")
                e_file.delete(0, 'end')
            else:
                show_message("No valid nodes found in file", is_error=True)
                e_file.delete(0, 'end')
        except FileNotFoundError:
            show_message(f"File not found: {e_file.get()}", is_error=True)
        except Exception as e:
            show_message(f"Error loading file: {str(e)}", is_error=True)

    def add_node():
        '''Añadimos un nodo al gráfico, marcando el nombre del nodo
        y sus cordenadas. Si ese nodo ya existe el código nos lo hará saber'''
        global edited_G
        name = e_name.get().strip()
        x_str = e_x.get().strip()
        y_str = e_y.get().strip()
        if not name or not x_str or not y_str:
            show_message("All the entries must be filled", is_error=True)
            return
        try:
            x = float(x_str)
            y = float(y_str)
        except ValueError:
            show_message("The coordinates must be numbers, they can't be letters or weird symbols", is_error=True)
            e_x.delete(0, 'end')
            e_y.delete(0, 'end')
            return
        if SearchNode(edited_G, name):
            show_message(f'The node "{name}" already exists', is_error=True)
            e_name.delete(0, 'end')
            return
        AddNode(edited_G, Node(name, x, y))
        show_graph_1()
        e_name.delete(0, 'end')
        e_x.delete(0, 'end')
        e_y.delete(0, 'end')

    def add_segment():
        '''Añadimos un segmento al gráfico entre dos puntos, ya sean antiguos
        o creados con la función de AddNode'''
        global edited_G
        e_name_from = e_from.get().strip()  # Obtenemos de donde proviene
        e_name_to = e_to.get().strip()  # Obtenemos el nodo destinación
        if not e_name_from or not e_name_to:
            show_message("You must write both nodes first.", is_error=True)
            return
        node_from = SearchNode(edited_G, e_name_from)
        node_to = SearchNode(edited_G, e_name_to)
        if not node_from:
            show_message(f"The node '{e_name_from}' doesn't exists. Create it first.", is_error=True)
            e_from.delete(0, 'end')
            return
        if not node_to:
            show_message(f"The node '{e_name_to}' doesn't exists. Create it first.", is_error=True)
            e_to.delete(0, 'end')
            return
        e_seg = f"{e_name_from}{e_name_to}"
        '''Creamos el nombre del segmento (vector) 
                a partir del nodo destino  del nodo final'''
        #e_seg1 = f"{e_name_to}{e_name_from}"
        '''Creamos el otro vector (AB - BA)'''
        segment_exists = any(
            (s.name == e_seg) #or s.name == e_seg1)
            for s in edited_G.segments)
        if segment_exists:
            show_message(f"It already exists a segment between {e_name_from} and {e_name_to}", is_error=True)
            e_from.delete(0, 'end')
            e_to.delete(0, 'end')
            return
        AddSegment(edited_G, e_seg, e_name_from, e_name_to)
        #AddSegment(edited_G, e_seg1, e_name_to, e_name_from)
        e_from.delete(0, 'end')
        e_to.delete(0, 'end')
        '''Añadimos estos segmentos a nuestro gráfico y fuente de información'''
        e_to.delete(0, 'end')
        e_from.delete(0, 'end')
        '''Limpiamos las entradas de texto'''
        show_graph_1()

    def delete_node():
        '''Eliminamos nodos del gráfico, ya sean creados por nosotros o anteriores'''
        global edited_G
        node_name = e_delete_n.get().strip()
        if not node_name:
            show_message("You must write the name of the node you want to delete.", is_error=True)
            e_delete_n.delete(0, 'end')
            return
        if not SearchNode(edited_G, node_name):
            show_message(f"The node '{node_name}' doesn't exists.", is_error=True)
            e_delete_n.delete(0, 'end')
            return
        DeleteNode(edited_G, node_name)
        show_message(f"The node '{node_name}' was eliminated successfully.")
        e_delete_n.delete(0, 'end')
        show_graph_1()

    def delete_segment():
        '''La misma función que delete_node, solo que en lugar de eliminar
        nodos esta función elimina segmentos'''
        global edited_G
        segment_name = e_delete_s.get().strip()
        if not segment_name:
            show_message("You must write the name of the segment you want to delete.", is_error=True)
            e_delete_s.delete(0, 'end')
            return
        segment_to_delete = None
        for seg in edited_G.segments:
            if seg.name == segment_name: #for seg.name == segment_name[::-1]:
                segment_to_delete = seg
                break
        if not segment_to_delete:
            show_message(f"It doesn't exists any segment called '{segment_name}'", is_error=True)
            e_delete_s.delete(0, 'end')
            return
        DeleteSegment(edited_G, segment_to_delete.name)
        show_message(f"Segment '{segment_to_delete.name}' deleted successfully.")
        e_delete_s.delete(0, 'end')
        show_graph_1()

    '''def button4():
        button4 = tk.Button(root,
                            text="Entry",
                            command=(entry2),
                            activebackground="blue",
                            activeforeground="white",
                            anchor="center",
                            bd=3,
                            bg="lightgray",
                            cursor="hand2",
                            disabledforeground="gray",
                            fg="black",
                            font=("Arial", 12),
                            height=2,
                            highlightbackground="black",
                            highlightcolor="green",
                            highlightthickness=2,
                            justify="center",
                            overrelief="raised",
                            padx=10,
                            pady=5,
                            width=5,
                            wraplength=100)

        button4.grid(row=1, column=4)'''

    tk.Button(root, text="Entry", command=entry1, cursor="hand2").grid(row=0, column=4)
    tk.Button(root, text="Add Node", command=add_node, cursor="hand2").grid(row=4, column=3)
    tk.Button(root, text="Add Segment", command=add_segment, cursor="hand2").grid(row=7, column=3)
    tk.Button(root, text="Delete Node", command=delete_node, cursor="hand2").grid(row=9, column=3)
    tk.Button(root, text='Delete Segment', command=delete_segment, cursor='hand2').grid(row=13, column=3)
    '''Botones para llevar acabo acciones determinadas anteriormente, el cursor
    se transforma en una mano (hand2) al pasar por encima'''
    root.geometry('1200x600')

Entries()

root.mainloop()