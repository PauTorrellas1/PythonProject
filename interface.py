from path import *
from tkinter import filedialog
current_visualization_mode = "main"
current_visualization_node = None

def CreateGraph_1 ():
    '''Crea un grafo con la información dada, cada uno de los nodos y segmentos'''
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
    '''esta función limpia la GUI y muestra el gráfico'''
    global fig, ax, canvas
    global current_visualization_mode, current_visualization_node
    current_visualization_mode = "main"
    current_visualization_node = None
    if 'ax' in globals():
        ax.clear()
    else:
        fig = Figure(figsize=(8.5, 7), dpi=100)
        ax = fig.add_subplot(111)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
    ax.set_axisbelow(True)
    if is_real_map(G):
        for point in G.nav_points:
            ax.plot(point['lon'], point['lat'], 'ko', markersize=3)
            ax.text(point['lon'], point['lat'], point['name'], fontsize=7, color='black')
        for seg in G.nav_segments:
            origin = next((p for p in G.nav_points if p['id'] == seg['origin_id']), None)
            dest = next((p for p in G.nav_points if p['id'] == seg['dest_id']), None)
            if origin and dest:
                ax.plot([origin['lon'], dest['lon']],
                        [origin['lat'], dest['lat']],
                        'blue', linewidth=1.5, zorder=1)
                ax.text((origin['lon'] + dest['lon']) / 2,
                        (origin['lat'] + dest['lat']) / 2,
                        f"{seg['distance']:.2f}",
                        color='black', fontsize=8, zorder=3)
    else:
        for seg in G.segments:
            ax.plot([seg.origin.x, seg.destination.x],
                    [seg.origin.y, seg.destination.y],
                    'blue', linewidth=1.5, zorder=1)
            ax.text((seg.origin.x + seg.destination.x) / 2 + 0.2,
                    (seg.origin.y + seg.destination.y) / 2 + 0.2,
                    f"{seg.cost:.2f}",
                    color='black', fontsize=8, zorder=3)
        for node in G.nodes:
            ax.plot(node.x, node.y, 'ko', markersize=3)
            ax.text(node.x, node.y, node.name, fontsize=7, color='black')
    if 'canvas' not in globals() or not canvas.get_tk_widget().winfo_exists():
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)
    else:
        canvas.draw()

show_message("Probando el grafo...")
original_G = CreateGraph_1() #Guardamos el gráfico original en una variable
edited_G = CreateGraph_1()  #Hacemos una copia del gráfico original, donde se mostrarán todas las ediciones hechas por nosotros
G = edited_G #Especificamos que por el momento el gráfico a mostrar será el editado
set_graph(G) # El gráfico mostrado será el editado (a espera de algún cambio)
root.title("GUI") #Abrimos la ventana del GUI
create_message_area() #Creamos el área para mensajes que usaremos más tarde
show_new_graph() #Mostramos el gráfico
path_info_frame = tk.Frame(root)
path_info_frame.grid(row=19, column=5, sticky="ew", padx=10, pady=5)
path_info_text = tk.Text(
    path_info_frame,
    height=4,
    wrap=tk.WORD,
    font=("Arial", 10),
    bg="white",
    fg="black",
    relief=tk.FLAT)
path_info_text.pack(fill=tk.BOTH, expand=True)

def button(command,tex,row,column,abg="blue",width=None,pady=2,master=root):
    '''definimos la configuración que deberán tener los botones que usemos'''
    tk.Button(master=master,
        text=tex,
        command=command,
        activebackground=abg,
        cursor='hand2',
        padx=5,
        pady=pady,
        width=width,
        wraplength=1000).grid(row=row, column=column)

def label(text, row, column,master=root):
    '''definimos una caja donde podremos mostrar mensajes'''
    tk.Label(master=master, text=text, padx=10).grid(row=row, column=column)

def show_graph():
    '''Función que nos muestra el grafo original'''
    global current_display_mode, G
    current_display_mode = "original"
    G = original_G
    restore_main_view()
    show_new_graph()
    show_message("Showing original graph")

def show_graph_1():
    '''Función que nos muestra el grafo editado'''
    global current_display_mode, G
    current_display_mode = "edited"
    G = edited_G
    restore_main_view()
    show_new_graph()
    show_message("Showing edited graph")

def restore_main_view():
    '''Reseteamos la vista para no superponer unos botones con otros,
    aunque estos sean idénticos'''
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    Entries()
    show_new_graph()

def print_graph_info():
    """Muestra todos los grafos en una ventanita donde el usuario puede asegurarse de que toda la información ha sido propiamente guardad"""

    def detect_region():
        """identifica si este es un mapa inventado o uno real """
        if any(p.get('name') == 'LEBL' for p in G.nav_points):  # Barcelona
            return 'Cat'
        elif any(p.get('name') == 'LEMD' for p in G.nav_points):  # Madrid
            return 'Spain'
        elif any(p.get('name') == 'EGLL' for p in G.nav_points):  # London
            return 'ECAC'
        if hasattr(G, 'loaded_prefix'):
            return G.loaded_prefix


    def save_info():
        """Permite guardar el gráfo"""
        if is_real_map(G):
            prefix = detect_region()
            if prefix:
                try:
                    with open(f'{prefix}_aer.txt', 'w') as f:
                        f.write("\n".join(sorted(G.nav_airports)))
                    with open(f'{prefix}_nav.txt', 'w') as f:
                        for p in sorted(G.nav_points, key=lambda x: int(x['id'])):
                            f.write(f"{p['id']} {p['name']} {p['lat']} {p['lon']}\n")
                    with open(f'{prefix}_seg.txt', 'w') as f:
                        for s in G.nav_segments:
                            f.write(f"{s['origin_id']} {s['dest_id']} {s['distance']}\n")
                    show_message(f"Saved real map to {prefix}_aer.txt, {prefix}_nav.txt, {prefix}_seg.txt")
                except Exception as e:
                    show_message(f"Save error: {str(e)}", is_error=True)
            else:
                show_message("Could not detect map region", is_error=True)
        else:
            with open('Graph_information.txt', 'w') as f:
                if G.nodes:
                    f.write("\n".join(f"N,{n.name},{n.x},{n.y}" for n in G.nodes))
                if G.segments:
                    f.write("\n" + "\n".join(
                        f"S,{s.name},{s.origin.name},{s.destination.name}"
                        for s in G.segments))
            show_message("Saved graph to Graph_information.txt")

    info_window = tk.Toplevel(root)
    info_window.title("Graph Information")
    text_frame = tk.Frame(info_window)
    text_frame.pack(fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget = tk.Text(
        text_frame,
        wrap=tk.WORD,
        yscrollcommand=scrollbar.set,
        font=("Consolas", 10))
    text_widget.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_widget.yview)
    info_text = "=== GRAPH INFORMATION ===\n\n"

    if is_real_map(G):
        if hasattr(G, 'nav_points') and G.nav_points:
            info_text += "NAVIGATION POINTS:\n"
            for point in G.nav_points:
                info_text += f"- {point['name']} (ID: {point['id']}): Lat={point['lat']}, Lon={point['lon']}\n"
        else:
            info_text += "No navigation points in the graph\n"

        info_text += "\nAIRPORTS:\n"
        if hasattr(G, 'nav_airports') and G.nav_airports:
            for airport in G.nav_airports:
                info_text += f"- {airport}\n"
        else:
            info_text += "No airports in the graph\n"
        info_text += "\nSEGMENTS:\n"
        if hasattr(G, 'nav_segments') and G.nav_segments:
            for segment in G.nav_segments:
                origin = next((p for p in G.nav_points if p['id'] == segment['origin_id']), None)
                dest = next((p for p in G.nav_points if p['id'] == segment['dest_id']), None)
                if origin and dest:
                    info_text += f"- {origin['name']} -> {dest['name']}: {segment['distance']:.2f} distance\n"
        else:
            info_text += "No segments in the graph\n"
    else:
        # Regular graph info
        if hasattr(G, 'nodes') and G.nodes:
            info_text += "NODES:\n"
            for node in G.nodes:
                info_text += f"- {node.name}: (x={node.x}, y={node.y})\n"
        else:
            info_text += "No nodes in the graph\n"
        info_text += "\nSEGMENTS:\n"
        if hasattr(G, 'segments') and G.segments:
            for segment in G.segments:
                dist = Distance(segment.origin, segment.destination)
                info_text += f"- {segment.name}: {segment.origin.name} -> {segment.destination.name} (Distance: {dist})\n"
        else:
            info_text += "No segments in the graph\n"
    text_widget.insert(tk.END, info_text)

    btn_frame = tk.Frame(info_window)
    btn_frame.pack(pady=10)
    tk.Button(
        btn_frame,
        text='Save',
        command=lambda: [save_info(), info_window.destroy()],
        width=15
    ).pack(side=tk.RIGHT, padx=10)
    tk.Button(
        btn_frame,
        text="Close",
        command=info_window.destroy,
        width=15
    ).pack(side=tk.LEFT, padx=10)

def import_map():
    '''Esta función será la encargada de importar todos los gráficos reales que queramos'''
    for widget in root.winfo_children():
        if widget.grid_info().get('column', 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="Real map to import:").grid(row=0, column=2)
    e_map_name = tk.Entry(root)
    e_map_name.grid(row=0, column=3)

    def load_map(event=None):
        '''Esta función cargará el mapa que queramos importar'''
        region = e_map_name.get().strip()
        try:
            airspace = AirSpace().load_real_map(region)
            global edited_G, G, current_display_mode, airspace_instance
            edited_G = airspace
            G = edited_G
            current_display_mode = "edited"
            airspace_instance = airspace
            set_graph(G)
            Plot(G)
            show_message(f"Successfully loaded {region} map")
            if e_map_name.winfo_exists():
                e_map_name.delete(0, 'end')
        except Exception as e:
            show_message(f"Error loading map: {str(e)}", is_error=True)
    e_map_name.bind('<Return>', load_map)
    tk.Button(
        root,
        text="Import Map",
        command=lambda: load_map(),
        cursor='hand2'
    ).grid(row=1, column=3)

def show_neighbors():
    '''Esta función nos muestra a todos los vecinos de un nodo'''
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_neighbor = tk.Entry(root)
    e_neighbor.grid(row=0, column=3)

    def highlight_neighbors(node_name):
        '''La función es la encargada de subrayar cada uno de los vecninos que debamos subrayar'''
        global fig, ax, canvas, G
        global current_visualization_mode, current_visualization_node
        current_visualization_mode = "neighbors"
        current_visualization_node = node_name
        ax.clear()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        node_name = node_name.strip()
        if not node_name:
            show_message("Enter a node name", is_error=True)
            return
        if is_real_map(G):
            node_point = next((p for p in G.nav_points if p['name'] == node_name), None)
            if not node_point:
                show_message(f"Node '{node_name}' doesn't exist", is_error=True)
                return
            connected_points = []
            for seg in G.nav_segments:
                if seg['origin_id'] == node_point['id']:
                    dest_point = next((p for p in G.nav_points if p['id'] == seg['dest_id']), None)
                    if dest_point:
                        connected_points.append(dest_point)
                elif seg['dest_id'] == node_point['id']:
                    origin_point = next((p for p in G.nav_points if p['id'] == seg['origin_id']), None)
                    if origin_point:
                        connected_points.append(origin_point)
            if not connected_points:
                show_message(f"Node '{node_name}' has no neighbors", is_error=True)
                return
            for point in G.nav_points:
                color = 'gray'
                if point['name'] == node_name:
                    color = 'blue'
                elif point in connected_points:
                    color = 'green'
                ax.plot(point['lon'], point['lat'], 'o', color=color, markersize=8)
                ax.text(point['lon'], point['lat'], point['name'], color='black', ha='left', va='bottom')
            for neighbor in connected_points:
                ax.plot([node_point['lon'], neighbor['lon']],
                        [node_point['lat'], neighbor['lat']],
                        'r-', linewidth=2)
        else:
            node = SearchNode(G, node_name)
            if not node:
                show_message(f"Node '{node_name}' doesn't exist", is_error=True)
                return
            if not node.neighbors:
                show_message(f"Node '{node_name}' has no neighbors", is_error=True)
                return
            for n in G.nodes:
                color = 'gray'
                if n == node:
                    color = 'blue'
                elif n in node.neighbors:
                    color = 'green'
                ax.plot(n.x, n.y, 'o', color=color, markersize=8)
                ax.text(n.x, n.y, n.name, color='black', ha='left', va='bottom')
            for neighbor in node.neighbors:
                seg = None
                for s in G.segments:
                    if (s.origin == node and s.destination == neighbor) or (
                            s.origin == neighbor and s.destination == node):
                        seg = s
                        break
                if seg:
                    dx = neighbor.x - node.x
                    dy = neighbor.y - node.y
                    length = math.sqrt(dx ** 2 + dy ** 2)
                    if length > 0:
                        dx /= length
                        dy /= length
                        ax.arrow(node.x, node.y,
                                 dx * 0.95 * length, dy * 0.95 * length,
                                 head_width=0.5, head_length=0.5,
                                 fc='red', ec='red',
                                 length_includes_head=True)
        if 'canvas' in globals() and canvas:
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=5, rowspan=20)

    def search_and_clear(event=None):
        '''Busca la entrada, corre la funicón de subrayar y elimina la entrada de texto'''
        node_name = e_neighbor.get().strip()
        highlight_neighbors(node_name)
        e_neighbor.delete(0, 'end')

    e_neighbor.bind('<Return>', search_and_clear)
    search_btn = tk.Button(
        root,
        text='Show Neighbors',
        command=lambda: search_and_clear(),
        cursor='hand2'
    )
    search_btn.grid(row=0, column=4)

def create_new_graph():
    '''Esta función crea un gráfico en blanco'''
    global edited_G, G, current_display_mode
    edited_G = Graph()
    G = edited_G
    current_display_mode = "edited"
    restore_main_view()
    show_message("Created new empty graph")

def confirm_new_graph():
    """Esta función le recuerda al usuario que de continuar
     perderá su antiguo gráfico, y le da la opción de hacer lo que él desee"""
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Confirm":
            widget.destroy()
    confirm_window = tk.Toplevel(root)
    confirm_window.title("Confirm")
    confirm_window.transient(root)
    confirm_window.grab_set()
    confirm_window.resizable(False, False)
    window_width = 460
    window_height = 180
    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    confirm_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    confirm_window.configure(bg="#FFC400")
    content_frame = tk.Frame(confirm_window, bg="#FFC400")
    content_frame.pack(padx=20, pady=15, fill="both", expand=True)
    warning_icon = tk.Label(content_frame, text="⚠️", font=("Arial", 18), bg="#FFC400", fg="#172B4D")
    warning_icon.grid(row=0, column=0, rowspan=2, sticky="n")
    header = tk.Label(content_frame, text="Are you sure you want to create a new graph?",
                      font=("Arial", 12, "bold"), bg="#FFC400", fg="#172B4D", anchor="w", justify="left")
    header.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
    message = tk.Label(content_frame,
                       text="All unsaved changes will be lost.\nWe recommend saving your previous graph first.",
                       font=("Arial", 10), bg="#FFC400", fg="#172B4D", justify="left", anchor="w")
    message.grid(row=1, column=1, sticky="w", padx=(10, 0))
    button_frame = tk.Frame(confirm_window, bg="#FFC400")
    button_frame.pack(pady=5)

    def on_yes_confirm():
        '''Confirma que está dispuesto a continuar con la creación de un nuevo gráfico'''
        confirm_window.destroy()
        create_new_graph()
    btn_style = {
        "bg": "#F1B300",
        "fg": "#172B4D",
        "font": ("Arial", 10, "bold"),
        "relief": tk.FLAT,
        "activebackground": "#E0A000",
        "padx": 10,
        "pady": 5}
    tk.Button(button_frame, text="Yes, continue", command=on_yes_confirm, **btn_style).pack(side=tk.RIGHT, padx=10)
    tk.Button(button_frame, text="No, cancel", command=confirm_window.destroy, **btn_style).pack(side=tk.LEFT, padx=10)
    confirm_window.wait_window()

def find_best_route():
    '''Esta función permitirá escoger una ruta aérea entre dos aeropuertos
    y mostrará la más corta'''
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()


def export_to_kml(graph, show_all=False):
    filename = filedialog.asksaveasfilename(
        defaultextension=".kml",
        filetypes=[("KML Files", "*.kml"), ("All Files", "*.*")],
        title="Save KML File As",
        initialfile="airspace_map.kml")
    if not filename:
        return
    kml_template = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Airspace Map</name>
    <description>Generated airspace map</description>
    {content}
</Document>
</kml>"""

    placemark_template = """<Placemark>
        <name>{name}</name>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
        <Style>
            <IconStyle>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
                </Icon>
            </IconStyle>
        </Style>
    </Placemark>"""

    airport_template = """<Placemark>
        <name>{name} Airport</name>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
        <Style>
            <IconStyle>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/pal3/icon54.png</href>
                </Icon>
            </IconStyle>
        </Style>
    </Placemark>"""

    line_template = """<Placemark>
        <name>{name}</name>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>{coords}</coordinates>
        </LineString>
        <Style>
            <LineStyle>
                <color>ff0000ff</color>
                <width>2</width>
            </LineStyle>
        </Style>
    </Placemark>"""

    path_line_template = """<Placemark>
        <name>Path: {name}</name>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>{coords}</coordinates>
        </LineString>
        <Style>
            <LineStyle>
                <color>ff00ff00</color>
                <width>4</width>
            </LineStyle>
        </Style>
    </Placemark>"""
    content = []
    if is_real_map(graph):
        if current_visualization_mode == "neighbors" and current_visualization_node:
            node_point = next((p for p in graph.nav_points if p['name'] == current_visualization_node), None)
            if node_point:
                content.append(placemark_template.format(
                    name=node_point['name'] + " (Center)",
                    lon=node_point['lon'],
                    lat=node_point['lat']))
                connected_points = []
                for seg in graph.nav_segments:
                    if seg['origin_id'] == node_point['id']:
                        dest_point = next((p for p in graph.nav_points if p['id'] == seg['dest_id']), None)
                        if dest_point:
                            connected_points.append(dest_point)
                            content.append(placemark_template.format(
                                name=dest_point['name'],
                                lon=dest_point['lon'],
                                lat=dest_point['lat']))
                            content.append(line_template.format(
                                name=f"{node_point['name']} to {dest_point['name']}",
                                coords=f"{node_point['lon']},{node_point['lat']},0 {dest_point['lon']},{dest_point['lat']},0"))
                    elif seg['dest_id'] == node_point['id']:
                        origin_point = next((p for p in graph.nav_points if p['id'] == seg['origin_id']), None)
                        if origin_point:
                            connected_points.append(origin_point)
                            content.append(placemark_template.format(
                                name=origin_point['name'],
                                lon=origin_point['lon'],
                                lat=origin_point['lat']))
                            content.append(line_template.format(
                                name=f"{origin_point['name']} to {node_point['name']}",
                                coords=f"{origin_point['lon']},{origin_point['lat']},0 {node_point['lon']},{node_point['lat']},0"))
        elif current_visualization_mode == "paths" and current_visualization_node:
            node_point = next((p for p in graph.nav_points if p['name'] == current_visualization_node), None)
            if node_point:
                visited = set()
                path_segments = set()
                queue = [node_point['id']]
                visited.add(node_point['id'])
                while queue:
                    current_id = queue.pop(0)
                    current_node = next((p for p in graph.nav_points if p['id'] == current_id), None)
                    if not current_node:
                        continue
                    for seg in [s for s in graph.nav_segments if s['origin_id'] == current_id]:
                        neighbor_id = seg['dest_id']
                        neighbor = next((p for p in graph.nav_points if p['id'] == neighbor_id), None)
                        if neighbor and neighbor_id not in visited:
                            path_segments.add((current_id, neighbor_id))
                            visited.add(neighbor_id)
                            queue.append(neighbor_id)
                for point in graph.nav_points:
                    if point['id'] in visited:
                        if point['id'] == node_point['id']:
                            # Main node
                            content.append(placemark_template.format(
                                name=point['name'] + " (Origin)",
                                lon=point['lon'],
                                lat=point['lat']))
                        else:
                            content.append(placemark_template.format(
                                name=point['name'],
                                lon=point['lon'],
                                lat=point['lat']))
                for seg in graph.nav_segments:
                    if (seg['origin_id'], seg['dest_id']) in path_segments:
                        origin = next((p for p in graph.nav_points if p['id'] == seg['origin_id']), None)
                        dest = next((p for p in graph.nav_points if p['id'] == seg['dest_id']), None)
                        if origin and dest:
                            content.append(line_template.format(
                                name=f"{origin['name']} to {dest['name']}",
                                coords=f"{origin['lon']},{origin['lat']},0 {dest['lon']},{dest['lat']},0"))
        else:
            for point in graph.nav_points:
                content.append(placemark_template.format(
                    name=point['name'],
                    lon=point['lon'],
                    lat=point['lat']))
            for seg in graph.nav_segments:
                origin = next((p for p in graph.nav_points if p['id'] == seg['origin_id']), None)
                dest = next((p for p in graph.nav_points if p['id'] == seg['dest_id']), None)
                if origin and dest:
                    content.append(line_template.format(
                        name=f"{origin['name']} to {dest['name']}",
                        coords=f"{origin['lon']},{origin['lat']},0 {dest['lon']},{dest['lat']},0"))
    else:
        if current_visualization_mode == "neighbors" and current_visualization_node:
            node = SearchNode(graph, current_visualization_node)
            if node:
                content.append(placemark_template.format(
                    name=node.name + " (Center)",
                    lon=node.x,
                    lat=node.y))
                for neighbor in node.neighbors:
                    content.append(placemark_template.format(
                        name=neighbor.name,
                        lon=neighbor.x,
                        lat=neighbor.y))
                    content.append(line_template.format(
                        name=f"{node.name} to {neighbor.name}",
                        coords=f"{node.x},{node.y},0 {neighbor.x},{neighbor.y},0"))
        elif current_visualization_mode == "paths" and current_visualization_node:
            node = SearchNode(graph, current_visualization_node)
            if node:
                visited = set()
                path_segments = set()
                queue = [node]
                visited.add(node.name)
                while queue:
                    current_node = queue.pop(0)
                    for seg in [s for s in graph.segments if s.origin == current_node]:
                        neighbor = seg.destination
                        if neighbor.name not in visited:
                            path_segments.add(seg)
                            visited.add(neighbor.name)
                            queue.append(neighbor)
                for n in graph.nodes:
                    if n.name in visited:
                        if n == node:
                            content.append(placemark_template.format(
                                name=n.name + " (Origin)",
                                lon=n.x,
                                lat=n.y))
                        else:
                            content.append(placemark_template.format(
                                name=n.name,
                                lon=n.x,
                                lat=n.y))
                for seg in path_segments:
                    content.append(line_template.format(
                        name=seg.name,
                        coords=f"{seg.origin.x},{seg.origin.y},0 {seg.destination.x},{seg.destination.y},0"))
        else:
            for node in graph.nodes:
                content.append(placemark_template.format(
                    name=node.name,
                    lon=node.x,
                    lat=node.y))
            for seg in graph.segments:
                content.append(line_template.format(
                    name=seg.name,
                    coords=f"{seg.origin.x},{seg.origin.y},0 {seg.destination.x},{seg.destination.y},0"))
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(kml_template.format(content='\n'.join(content)))
        show_message(f"Successfully exported to {filename}")
    except Exception as e:
        show_message(f"Error saving file: {str(e)}", is_error=True)

button(lambda: show_graph(), "Show original graph", 0, 0, width=20,pady=10)#, master=plotting_frame)
button(lambda: show_graph_1(), "Show edited graph", 1, 0, width=20,pady=10)#, master=plotting_frame)
button(lambda: confirm_new_graph(), "Crete new graph", 2, 0, width=20,pady=10)#, master=plotting_frame)
button(lambda: print_graph_info(), "Save the information", 3, 0, width=20,pady=10)#, master=plotting_frame)
button(lambda: [func() for func in (show_paths, find_closest_path_entries)], "Analyze paths", 4, 0, width=20,pady=10)#, master=plotting_frame)
button(show_neighbors, "Show node neighbors", 5, 0, width=20,pady=10)#, master=plotting_frame)
button(lambda: import_map(), 'Import a real map', 6, 0, width=20,pady=10)
button(lambda: export_to_kml(G), "Export to KML", 7, 0, width=20, pady=10)
if is_real_map(G):
    button(lambda: find_best_route(), 'Find the best route', 8, 0, width=20, pady=10)


def Entries():
    '''Cada una de las entradas de texto que usaremos en el menú principal
    de nuestra aplicación. si llevan tk.Label son únicamente texto,
    mientras que si llevan tk.Entry son entradas de texto donde debemos escribir.
    Si llevan tk.Button son botones para presionar y llevar a cabo una acción o comando.'''
    """global e_name, e_x, e_y, e_from, e_to, e_delete_n, e_delete_s, e_file"""# en ppi no cal
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()

    label("File Name",0, 2)
    e_file = tk.Entry(root)  # Primer entry
    e_file.grid(row=0, column=3,pady=10)

    def entry1(event=None):
        global G, edited_G, current_display_mode
        filename = e_file.get()
        try:
            new_graph = read_file(filename)
            if new_graph.nodes:
                edited_G = new_graph
                G = edited_G
                set_graph(G)
                current_display_mode = "edited"
                show_graph_1()
                show_message(f"Successfully loaded graph from {filename}")
                try:
                    e_file.delete(0, 'end')
                except tk.TclError:
                    pass
            else:
                show_message("No valid nodes found in file", is_error=True)
                e_file.delete(0, 'end')
        except FileNotFoundError:
            show_message(f"File not found: {e_file.get()}", is_error=True)
            e_file.delete(0, 'end')
        except Exception as e:
            show_message(f"Error loading file: {str(e)}", is_error=True)
    button(entry1, "Entry", 1, 3,width=12)

    label("New node name", 2, 2)
    e_name = tk.Entry(root)  # Nombre del nuevo nodo
    e_name.grid(row=2, column=3,pady=10)
    label("X",3,2)
    e_x = tk.Entry(root)  # Valor X del nuevo nodo
    e_x.grid(row=3, column=3,pady=10)
    label("Y",4, 2)
    e_y = tk.Entry(root)  # Valor Y del nuevo nodo
    e_y.grid(row=4, column=3,pady=10)
    label("From",6,2)
    e_from = tk.Entry(root)  # Nodo origen del nuevo segmento
    e_from.grid(row=6, column=3,pady=10)
    label("To",7,2)
    e_to = tk.Entry(root) #Nodo destino del nuevo segmento
    e_to.grid(row=7, column=3,pady=10)

    def add_node(event=None):
        global edited_G
        if is_real_map(edited_G):
            show_message("Cannot add segments to real maps", is_error=True)
            e_from.delete(0, 'end')
            e_to.delete(0, 'end')
            return
        e_name_from = e_from.get().strip()
        e_name_to = e_to.get().strip()
        if not e_name_from or not e_name_to:
            show_message("You must write both nodes first.", is_error=True)
            return
        node_from = SearchNode(edited_G, e_name_from)
        node_to = SearchNode(edited_G, e_name_to)
        if not node_from:
            show_message(f"The node '{e_name_from}' doesn't exists.", is_error=True)
            e_from.delete(0, 'end')
            return
        if not node_to:
            show_message(f"The node '{e_name_to}' doesn't exists.", is_error=True)
            e_to.delete(0, 'end')
            return
        e_seg = f"{e_name_from}{e_name_to}"
        segment_exists = any(
            (s.name == e_seg)
            for s in edited_G.segments)
        if segment_exists:
            show_message(f"It already exists a segment between {e_name_from} and {e_name_to}", is_error=True)
            e_from.delete(0, 'end')
            e_to.delete(0, 'end')
            return
        AddSegment(edited_G, e_seg, e_name_from, e_name_to)
        e_from.delete(0, 'end')
        e_to.delete(0, 'end')
        show_graph_1()
    button(add_node, "Add Node", 5, 3,width=12)

    def add_segment(event=None):
        '''Añadimos un segmento al gráfico'''
        global edited_G
        if is_real_map(edited_G):
            show_message("Cannot add segments to real maps", is_error=True)
            e_from.delete(0, 'end')
            e_to.delete(0, 'end')
            return
        e_name_from = e_from.get().strip()
        e_name_to = e_to.get().strip()
        if not e_name_from or not e_name_to:
            show_message("You must write both nodes first.", is_error=True)
            return
        node_from = SearchNode(edited_G, e_name_from)
        node_to = SearchNode(edited_G, e_name_to)
        if not node_from:
            show_message(f"The node '{e_name_from}' doesn't exists.", is_error=True)
            e_from.delete(0, 'end')
            return
        if not node_to:
            show_message(f"The node '{e_name_to}' doesn't exists.", is_error=True)
            e_to.delete(0, 'end')
            return
        e_seg = f"{e_name_from}{e_name_to}"
        segment_exists = any(
            (s.name == e_seg)
            for s in edited_G.segments)
        if segment_exists:
            show_message(f"It already exists a segment between {e_name_from} and {e_name_to}", is_error=True)
            e_from.delete(0, 'end')
            e_to.delete(0, 'end')
            return
        AddSegment(edited_G, e_seg, e_name_from, e_name_to)
        e_from.delete(0, 'end')
        e_to.delete(0, 'end')
        show_graph_1()
    button(add_segment, "Add Segment", 8, 3,width=12)
    label("Delete Node",9,2)
    e_delete_n = tk.Entry(root) #Nombre del nodo a borrar
    e_delete_n.grid(row=9, column=3,pady=15)

    def delete_node(event=None):
        '''Eliminamos nodos del gráfico'''
        global edited_G
        if is_real_map(edited_G):
            show_message("Cannot delete nodes from real maps", is_error=True)
            e_delete_n.delete(0, 'end')
            return
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
    button(delete_node, "Delete Node", 10, 3,width=12)
    label('Delete segment',11,2)
    e_delete_s = tk.Entry(root) #Nombre del segmento a borrar
    e_delete_s.grid(row=11, column=3,pady=15)

    def delete_segment(event=None):
        '''Eliminamos segmentos del gráfico'''
        global edited_G
        if is_real_map(edited_G):
            show_message("Cannot delete segments from real maps", is_error=True)
            e_delete_s.delete(0, 'end')
            return
        segment_name = e_delete_s.get().strip()
        if not segment_name:
            show_message("You must write the name of the segment you want to delete.", is_error=True)
            e_delete_s.delete(0, 'end')
            return
        segment_to_delete = None
        for seg in edited_G.segments:
            if seg.name == segment_name:
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
    button(delete_segment, 'Delete Segment', 14, 3,width=12)

    file_entries = [e_file]
    work_with_entry(file_entries, entry1)
    add_node_entries = [e_name, e_x, e_y]
    work_with_entry(add_node_entries, add_node)
    add_segment_entries = [e_from, e_to]
    work_with_entry(add_segment_entries, add_segment)
    delete_node_entries = [e_delete_n]
    work_with_entry(delete_node_entries, delete_node)
    delete_segment_entries = [e_delete_s]
    work_with_entry(delete_segment_entries, delete_segment)
    root.state('zoomed')
    label("", 0, 4),label("", 0, 6)#serves as a separator for the graph
Entries()

def close():
    '''Cerramos y destruimos la ventana'''
    p.close('all')
    root.destroy()
button(lambda: close(),"Exit", 0, 7,"red",width=5,pady=10)
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()