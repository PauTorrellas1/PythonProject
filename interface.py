from path import *

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
    '''Shows graph with clean cost labels'''
    global fig, ax, canvas
    ax.clear()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#AA336A')
    ax.set_axisbelow(True)

    # Draw segments and costs
    for seg in G.segments:
        ax.plot([seg.origin.x, seg.destination.x],
                [seg.origin.y, seg.destination.y],
                'blue', linewidth=1.5, zorder=1)

        # Cost label styling
        ax.text((seg.origin.x + seg.destination.x) / 2 + 0.2,
                (seg.origin.y + seg.destination.y) / 2 + 0.2,
                f"{seg.cost:.2f}",
                color='black', fontsize=8, zorder=3)

    # Draw nodes
    for node in G.nodes:
        ax.plot(node.x, node.y, 'ko', markersize=3)
        ax.text(node.x, node.y, node.name, fontsize=7, color= 'black')

    if canvas is None:
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
    """Muestra todos los nodos y segmentos de un archivo guardado dentro del GUI"""
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
    #Opciones de visualización de la ventana donde observamos todos los nodos y segmentos del gráfico
    #Aquí podremos ver toda la información que vayamos a guardar y asegurarnos que esta esté bien guardada
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
    #Mostramos toda la información guardada, es decir, los Nodos y sus posiciones,
    #y los segmentos y sus nombres, los respectivos nodos que los forman y el
    #coste de cada uno de ellos
    save_button = tk.Button(info_window, text='Save the information', command=lambda: [save_info(), info_window.destroy()])
    save_button.pack(pady=9)
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=10)


def show_neighbors():
    '''Esta función nos muestra a todos los vecinos de un nodo'''
    for widget in root.winfo_children():
        if widget.grid_info().get("column", 0) in [2, 3, 4]:
            widget.destroy()
    tk.Label(root, text="Node to analyze:").grid(row=0, column=2)
    e_neighbor = tk.Entry(root)
    e_neighbor.grid(row=0, column=3)

    def search_and_clear(event=None):
        '''Limpiamos la entrada de texto donde escribimos el nodoa estudiar'''
        node_name = e_neighbor.get().strip()
        highlight_neighbors(node_name)
        e_neighbor.delete(0, 'end')

    def highlight_neighbors(node_name):
        '''Esta función resalta los vecinos de un nodo'''
        global fig, ax, canvas, G
        ax.clear()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)

        node_name = node_name.strip()
        if not node_name:
            show_message("Enter a node name", is_error=True)
            return

        node = SearchNode(G, node_name)  # Use the current graph G
        if not node:
            show_message(f"Node '{node_name}' doesn't exist", is_error=True)
            return

        if not node.neighbors:
            show_message(f"Node '{node_name}' has no neighbors", is_error=True)
            return

        # Draw all nodes first
        for n in G.nodes:
            color = 'gray'
            if n == node:
                color = 'blue'
            elif n in node.neighbors:
                color = 'green'
            ax.plot(n.x, n.y, 'o', color=color, markersize=8)
            ax.text(n.x, n.y, n.name, color='black', ha='left', va='bottom')

        # Draw connections to neighbors
        for neighbor in node.neighbors:
            seg = None
            for s in G.segments:
                if (s.origin == node and s.destination == neighbor) or (s.origin == neighbor and s.destination == node):
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
    """Muestra un aviso para confirmar que el usuario realmente quiere abrir el grafo,
    y recomendarle que guarde la información si no desea perderla"""
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

def Buttons():
    def button_show_original_graph():
        '''Botón para mostrar el gráfico original'''
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
        '''Botón para mostrar el gráfico editado por nosotros'''
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
        '''Aquí creamos un nuevo gráfico a nuestro gusto. Esta opción abre una ventana nueva de tk
        donde podemos personalizar nuestro gráfico como queramos. Es esencialmente lo mismo que
        la ventana anterior pero con la diferencia que este gráfico está creado desde cero por nosotros mismos'''
        button_create_new_graph = tk.Button(root,
                                            text="Create new graph",
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
        '''Botón para ver la información del grafo y posteriormente,
        si lo desea, guardarla'''
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
        '''Botón que lleva a la opcion de analizar los caminos, ya sean
        los caminos posibles desde un nodo deseado,
        o el camino más corto entre un nodo y otro'''
        button_show_paths = tk.Button(root,
                                      text="Analyze paths",
                                      command=lambda: [func() for func in (show_paths, find_closest_path_entries)],
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
        '''Botón para ver los vecinos de un nodo'''
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
    Si llevan tk.Button son botones para presionar y llevar a cabo una acción o comando.'''
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
    e_name = tk.Entry(root) #Nombre del nuevo nodo
    e_x = tk.Entry(root) #Valor X del nuevo nodo
    e_y = tk.Entry(root) #Valor Y del nuevo nodo
    e_from = tk.Entry(root) #Nodo origen del nuevo segmento
    e_to = tk.Entry(root) #Nodo destino del nuevo segmento
    e_delete_n = tk.Entry(root) #Nombre del nodo a borrar
    e_delete_s = tk.Entry(root) #Nombre del segmento a borrar

    e_file.grid(row=0, column=3)
    e_name.grid(row=1, column=3)
    e_x.grid(row=2, column=3)
    e_y.grid(row=3, column=3)
    e_from.grid(row=5, column=3)
    e_to.grid(row=6, column=3)
    e_delete_n.grid(row=8, column=3)
    e_delete_s.grid(row=10, column=3)

    def entry1(event=None):
        '''Lee el texto de un documento determinado y nos muestra dicho gráfico'''
        global G, edited_G, current_display_mode
        try:
            new_graph = read_map_file(e_file.get())
            if new_graph.nodes:
                edited_G = new_graph
                G = edited_G
                set_graph(G)  # Make sure to update the graph reference in path.py
                current_display_mode = "edited"
                show_graph_1()
                show_message(f"Successfully loaded graph from {e_file.get()}")
                e_file.delete(0, 'end')
            else:
                show_message("No valid nodes found in file", is_error=True)
                e_file.delete(0, 'end')
        except FileNotFoundError:
            show_message(f"File not found: {e_file.get()}", is_error=True)
            e_file.delete(0, 'end')
        except Exception as e:
            show_message(f"Error loading file: {str(e)}", is_error=True)

    def add_node(event=None):
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
            # Limpiamos las entradas de texto
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

    def add_segment(event=None):
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
        #Creamos el nombre del segmento (vector)
        #a partir del nodo destino del nodo final
        #Creamos el otro vector (AB - BA)
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
        #Añadimos estos segmentos a nuestro gráfico y fuente de información
        e_to.delete(0, 'end')
        e_from.delete(0, 'end')
        show_graph_1()

    def delete_node(event=None):
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

    def delete_segment(event=None):
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
    tk.Button(root, text="Entry", command=entry1, cursor="hand2").grid(row=0, column=4)
    tk.Button(root, text="Add Node", command=add_node, cursor="hand2").grid(row=4, column=3)
    tk.Button(root, text="Add Segment", command=add_segment, cursor="hand2").grid(row=7, column=3)
    tk.Button(root, text="Delete Node", command=delete_node, cursor="hand2").grid(row=9, column=3)
    tk.Button(root, text='Delete Segment', command=delete_segment, cursor='hand2').grid(row=13, column=3)
    #Botones para llevar acabo acciones determinadas anteriormente, el cursor
    #se transforma en una mano (hand2) al pasar por encima
    root.state('zoomed')

Buttons()
Entries()

root.mainloop()