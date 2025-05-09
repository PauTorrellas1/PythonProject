from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from Create_New_Graph import *

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
print ("Probando el grafo...")

def show_new_graph():
    '''Embed the graph plot inside the Tkinter GUI'''
    global G, fig, ax

    # Clear previous plot (if any)
    for widget in root.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.destroy()

    # Create a new figure
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Plot the graph (default style)
    for segment in G.segments:
        x_vals = [segment.origin.x, segment.destination.x]
        y_vals = [segment.origin.y, segment.destination.y]
        ax.plot(x_vals, y_vals, 'b-', linewidth=1)
        ax.text(
            (x_vals[0] + x_vals[1]) / 2,
            (y_vals[0] + y_vals[1]) / 2,
            segment.cost,
            fontsize=8
        )

    # Plot nodes (default style)
    for node in G.nodes:
        ax.plot(node.x, node.y, 'ro', markersize=8)
        ax.text(node.x, node.y, node.name, fontsize=10)

    # Set labels and grid
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=5, rowspan=20, padx=10, pady=10)

def show_graph():
    '''Mostramos el gráfico original con los datos proporcionados arriba'''
    G = CreateGraph_1()
    Plot(G)

def show_graph_1():
    '''Mostramos el nuevo gráfico editado con nuevos segmentos , nodos
    y con los segmentos o nodos que hayamos eliminado '''
    Plot(G)


def print_graph_info():
    """Muestra todos los nodos y segmentos dentro del GUI"""
    def save_info():
        '''Guarda toda la información de los nodos y segmentos en un archivo que se puede abrir después'''
        with open('Graph information', 'w') as graph_info:
            if hasattr(G, 'nodes') and G.nodes:
                for node in G.nodes:
                    graph_info.write(f'N,{node.name},{node.x},{node.y}\n')
            else:
                print('There are not any nodes in the graph')
            if hasattr(G, 'segments') and G.segments:
                for segment in G.segments:
                    graph_info.write(f'S,{segment.name},{segment.origin.name},{segment.destination.name}\n')
            else:
                print('There are not any segments in the graph')

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
    '''Add input field and button to search for neighbors'''
    # Clear previous widgets (if needed)
    for widget in root.winfo_children():
        if widget.grid_info().get("column") == 2 or widget.grid_info().get("column") == 3:
            widget.destroy()

    # Add input field and button
    tk.Label(root, text="Insert the node whose neighbors you want to know").grid(row=1, column=2)
    e_name = tk.Entry(root)
    e_name.grid(row=1, column=3)


    def Entries_neighbors():
        '''Aquí escribiremos el nombre del nodo del cual querámos analizar sus vecinos'''
        tk.Label(root, text="Insert the node whose neighbors you want to know").grid(row=1, column=2)
        e_name = tk.Entry(root)
        e_name.grid(row=1, column=3)

        def Add_neighbors_node():
            '''Highlight the selected node and its neighbors in the main graph'''
            global G, fig, ax

            node_name = e_name.get().strip()
            if not node_name:
                print("Error: You must enter a node name")
                return

            node = SearchNode(G, node_name)
            if not node:
                print(f"Error: Node '{node_name}' doesn't exist")
                return

            if not node.neighbors:
                print("Information: The introduced node doesn't have any neighbors")
                return

            # Clear the current plot
            ax.clear()

            # Replot all segments (in gray for non-neighbors)
            for segment in G.segments:
                x_vals = [segment.origin.x, segment.destination.x]
                y_vals = [segment.origin.y, segment.destination.y]
                ax.plot(x_vals, y_vals, 'gray', linewidth=1, alpha=0.5)
                ax.text(
                    (x_vals[0] + x_vals[1]) / 2,
                    (y_vals[0] + y_vals[1]) / 2,
                    segment.cost,
                    fontsize=8
                )

            # Highlight segments connected to the selected node (in blue)
            for neighbor in node.neighbors:
                seg = next((s for s in G.segments if
                            (s.origin == node and s.destination == neighbor) or
                            (s.origin == neighbor and s.destination == node)), None)
                if seg:
                    x_vals = [seg.origin.x, seg.destination.x]
                    y_vals = [seg.origin.y, seg.destination.y]
                    ax.plot(x_vals, y_vals, 'b-', linewidth=2)

            # Replot all nodes (in gray for non-neighbors)
            for n in G.nodes:
                ax.plot(n.x, n.y, 'o', color='gray', markersize=8)
                ax.text(n.x, n.y, n.name, fontsize=10, color='gray')

            # Highlight the selected node (in red)
            ax.plot(node.x, node.y, 'ro', markersize=10)
            ax.text(node.x, node.y, node.name, fontsize=10, color='blue')

            # Highlight neighbors (in blue)
            for neighbor in node.neighbors:
                ax.plot(neighbor.x, neighbor.y, 'bo', markersize=8)
                ax.text(neighbor.x, neighbor.y, neighbor.name, fontsize=10, color='blue')

            # Refresh the canvas
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=5, rowspan=20, padx=10, pady=10)

        tk.Button(
            root,
            text='Search Node',
            command=Add_neighbors_node,
            cursor='hand2'
        ).grid(row=2, column=3)

    Entries_neighbors()
    root.mainloop()

    Entries_neighbors()

root = tk.Tk()
G = CreateGraph_1()
root.title("GUI")
show_new_graph()


def button1():
    '''Mostramos el gráfico original con la información propporcionada'''
    button1 = tk.Button(root,
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

    button1.grid(row=0, column=1)
def button2():
    '''Mostramos el nuevo gráfico editado por nosotros'''
    button2 = tk.Button(root,
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

    button2.grid(row=1, column=1)
def button4():
    '''Creamos un nuevo gráfico a nuestro gusto. Esta opción abre una ventana nueva de tk
    donde podemos personalizar nuestro gráfico como queramos. Es esencialmente lo mismo que
    la ventana anterior con la diferencia que este gráfico está creado desde cero por nostros mismos'''
    button4 = tk.Button(root,
                       text="Crete new graph",
                       command=create_new_graph,
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
    button4.grid(row=2, column=1)

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

button1()
button2()
button4()
button_save_graph_info()
button_show_neighbors()

def Entries():
    '''Cada una de las entradas de texto que usaremos en el menú principal
    de nuestra aplicación. si llevan tk.Label son únicamente texto,
    mientras que si llevan tk.Entry son entradas de texto donde debemos escribir.
    Si llevan tk.Button son botones para presionar y llevar acabo una acción o comando.'''
    tk.Label(root, text="File Name").grid(row=0, column=2)
    #tk.Label(root, text="Origin Name").grid(row=1, column=2)
    tk.Label(root, text="New node name").grid(row=2, column=2)
    tk.Label(root, text="X").grid(row=3, column=2)
    tk.Label(root, text="Y").grid(row=4, column=2)
    tk.Label(root, text="From").grid(row=6, column=2)
    tk.Label(root, text="To").grid(row=7, column=2)
    tk.Label(root, text="Delete Node").grid(row=9, column=2)
    tk.Label(root, text='Delete segment').grid(row=11, column=2)


    e1 = tk.Entry(root) #Primer entry
    e2 = tk.Entry(root) #Segundo entry
    e_name = tk.Entry(root) #New_node nombre
    e_x = tk.Entry(root) #New_node valor x
    e_y = tk.Entry(root) #New_node valor y
    e_from = tk.Entry(root) #Origen new_segment
    e_to = tk.Entry(root) #Destino new_segment
    e_delete_n = tk.Entry(root) #Delete node
    e_delete_s = tk.Entry(root) #Delete origin segment

    e1.grid(row=0, column=3)
    #e2.grid(row=1, column=3)
    e_name.grid(row=2, column=3)
    e_x.grid(row=3, column=3)
    e_y.grid(row=4, column=3)
    e_from.grid(row=6, column=3)
    e_to.grid(row=7, column=3)
    e_delete_n.grid(row=9, column=3)
    e_delete_s.grid(row=11, column=3)

    def entry1():
        '''Lee el texto de un documento determinado y nos muestra dicho gráfico'''
        global G
        try:
            G = read_file(e1.get())
            Plot(G)
        except FileNotFoundError:
            print(f"Error: Archive not found")
        except Exception as e:
            print(f"Another error: {e}")

    '''def entry2():
        G = CreateGraph_1()
        PlotNode(G, e2.get())'''

    def add_node():
        '''Añadimos un nodo al gráfico, marcando el nombre del nodo
        y sus cordenadas. Si ese nodo ya existe el código nos lo hará saber'''
        global G
        name = e_name.get().strip()
        x_str = e_x.get().strip()
        y_str = e_y.get().strip()
        if not name or not x_str or not y_str:
            print("Error: All the entries must be filled")
            return
        try:
            x = float(x_str)
            y = float(y_str)
        except ValueError:
            print("Error: The coordinates must be numbers, they can't be letters or weird symbols")
            return
        if SearchNode(G, name):
            print(f'Error: The node "{name}" already exists')
            return
        AddNode(G, Node(name, x, y))
        show_new_graph()
        e_name.delete(0, 'end')
        e_x.delete(0, 'end')
        e_y.delete(0, 'end')

    def add_segment():
        '''Añadimos un segmento al gráfico entre dos puntos, ya sean antiguos
        o creados con la función de AddNode'''
        global G
        e_name_from = e_from.get().strip()  # Obtenemos de donde proviene
        e_name_to = e_to.get().strip()  # Obtenemos el nodo destinación
        if not e_name_from or not e_name_to:
            print("Error: You must write both nodes first.")
            return
        node_from = SearchNode(G, e_name_from)
        node_to = SearchNode(G, e_name_to)
        if not node_from:
            print(f"Error:The node '{e_name_from}' doesn't exists. Create it first.")
            return
        if not node_to:
            print(f"Error: The node '{e_name_to}' doesn't exists. Create it first.")
            return
        e_seg = f"{e_name_from}{e_name_to}"
        '''Creamos el nombre del segmento (vector) 
                a partir del nodo destino  del nodo final'''
        e_seg1 = f"{e_name_to}{e_name_from}"
        '''Creamos el otro vector (AB - BA)'''
        segment_exists = any(
            (s.name == e_seg or s.name == e_seg1)
            for s in G.segments)
        if segment_exists:
            print(f"Error: It already exists a segment between {e_name_from} and {e_name_to}")
            return
        AddSegment(G, e_seg, e_name_from, e_name_to)
        AddSegment(G, e_seg1, e_name_to, e_name_from)
        '''Añadimos estos segmentos a nuestro gráfico y fuente de información'''
        e_to.delete(0, 'end')
        e_from.delete(0, 'end')
        '''Limpiamos las entradas de texto'''
        show_new_graph()

    def delete_node():
        '''Eliminamos nodos del gráfico, ya sean creados por nosotros o anteriores'''
        global G
        node_name = e_delete_n.get().strip()
        if not node_name:
            print("Error: You must write the name of the node you want to delete.")
            e_delete_n.delete(0, 'end')
            return
        if not SearchNode(G, node_name):
            print(f"Error: The node '{node_name}' doesn't exists.")
            e_delete_n.delete(0, 'end')
            return
        DeleteNode(G, node_name)
        print(f"The node '{node_name}' was eliminated successfully.")
        e_delete_n.delete(0, 'end')
        show_new_graph()

    def delete_segment():
        '''La misma función que delete_node, solo que en lugar de eliminar
        nodos esta función elimina segmentos'''
        global G
        segment_name = e_delete_s.get().strip()
        if not segment_name:
            print("Error: You must write the name of the segment you want to delete.")
            e_delete_s.delete(0, 'end')
            return
        segment_to_delete = None
        for seg in G.segments:
            if seg.name == segment_name or seg.name == segment_name[::-1]:
                segment_to_delete = seg
                break
        if not segment_to_delete:
            print(f"Error: It doesn't exists any segment called '{segment_name}'")
            e_delete_s.delete(0, 'end')
            return
        DeleteSegment(G, segment_to_delete.name)
        print(f"Segment '{segment_to_delete.name}' deleted successfully.")
        e_delete_s.delete(0, 'end')
        show_new_graph()

    def button3():
        '''Botón de entry para crear el gráfico a partir de un documento de texto'''
        button3 = tk.Button(root,
                            text="Entry",
                            command=entry1,
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

        button3.grid(row=0, column=4)
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


    button3()
    #button4()
    #De esta manera no sale el segundo entry, innecesario por el momento

    tk.Button(root,
              text="Add Node",
              command=add_node, cursor="hand2").grid(row=5, column=3)
    tk.Button(root, text="Add Segment",
              command=add_segment, cursor="hand2").grid(row=8, column=3)
    tk.Button(root, text="Delete Node",
              command=delete_node, cursor="hand2").grid(row=10, column=3)
    tk.Button(root, text='Delete Segment',
              command=delete_segment, cursor='hand2').grid(row=13, column=3)
    '''Botones para llevar acabo acciones determinadas anteriormente, el cursor
    se transforma en una mano (hand2) al pasar por encima'''
    root.geometry('1200x600')
Entries()

root.mainloop()