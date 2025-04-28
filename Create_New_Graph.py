import tkinter as tk
from graph import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

def create_new_graph():
    '''Creamos un nuevo gráfico en blanco'''
    global M_Graph
    M_Graph = Graph()

    def print_graph_info():
        """Muestra todos los nodos dentro del GUI"""
        def save_info():
            '''Guarda toda la información del grafo creado (nodos y segmentos) en un
            archivo que puede ser abierto y mostrado en grafo después'''
            with open('Graph information', 'w') as graph_info:
                if hasattr(M_Graph, 'nodes') and M_Graph.nodes:
                    for node in M_Graph.nodes:
                        graph_info.write(f'N,{node.name},{node.x},{node.y}\n')
                else:
                    print('There are not any nodes in the graph')
                if hasattr(M_Graph, 'segments') and M_Graph.segments:
                    for segment in M_Graph.segments:
                        graph_info.write(f'S,{segment.name},{segment.origin.name},{segment.destination.name}\n')
                else:
                    print('There are not any segments in the graph')

        global M_Graph
        info_window = tk.Toplevel(root)
        info_window.title("Graph Information")

        text_frame = tk.Frame(info_window)
        text_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        ''''Personalización y opciones de la ventana donde se muestra toda la información a guardar'''

        info_text = "=== GRAPH INFORMATION ===\n\n"

        if hasattr(M_Graph, 'nodes') and M_Graph.nodes:
            info_text += "NODES:\n"
            for node in M_Graph.nodes:
                info_text += f"- {node.name}: (x={node.x}, y={node.y})\n"
        else:
            info_text += "No nodes in the graph\n"

        info_text += "\n"
        if hasattr(M_Graph, 'segments') and M_Graph.segments:
            info_text += "SEGMENTS:\n"
            for segment in M_Graph.segments:
                segment.name = segment.origin.name+segment.destination.name
                dist = Distance(segment.origin, segment.destination)
                info_text += f"- {segment.name}: {segment.origin.name} -> {segment.destination.name} (Distance: {dist})\n"
        else:
            info_text += "No segments in the graph\n"
        '''Los nodos y segmentos guardados en el gráfico, ordenados alfabéticamente'''

        text_widget.insert(tk.END, info_text)

        save_button = tk.Button(info_window, text='Save the information',
                                command=lambda: [save_info(), info_window.destroy()])
        save_button.pack(pady=9)
        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack(pady=10)
        '''Botón de cerrar y botón de guardar la información'''

    root = tk.Tk()
    root.title('GUI_CREATE_GRAPH')

    def show_neighbors():
        '''Esta función muestra los vecinos del nodo que queramos '''
        root = tk.Tk()
        root.title('Node Neighbors Viewer')

        def Entries_neighbors():
            '''Aquí escribiremos el nombre del nodo del cual querámos analizar sus vecinos'''
            tk.Label(root, text="Insert the node whose neighbors you want to know").grid(row=1, column=2)
            e_name = tk.Entry(root)
            e_name.grid(row=1, column=3)

            def Add_neighbors_node():
                '''Mostramos todos los nodos vecinos del nodo escogido'''
                node_name = e_name.get().strip()
                if not node_name:
                    print("Error: You must enter a node name")
                    return
                node = SearchNode(M_Graph, node_name)
                if not node:
                    print(f"Error: Node '{node_name}' doesn't exist")
                    return
                if not node.neighbors:
                    print("Information: The introduced node doesn't have any neighbors")
                    root.destroy()
                    return
                PlotNode(M_Graph, node_name)
                root.destroy()

            tk.Button(root, text='Search Node',
                      command=Add_neighbors_node,
                      cursor='hand2').grid(row=13, column=3)

        Entries_neighbors()
        root.mainloop()

        Entries_neighbors()

    def show_new_graph():
        '''Mostramos el gráfico creado por nosotros, al principio completamente en blanco y vacío'''
        Plot(M_Graph)

    def button_new_graph():
        '''Botón que muestra el gráfico que hemos creado nosotros desde cero'''
        button_new_graph = tk.Button(root,
                            text="Show my new graph",
                            command=show_new_graph,
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
        button_new_graph.grid(row=0, column=1)

    def button_print_graph_info():
        ''''
        Este botón pretende guardar toda la información de un gráfico creado en un documento
        '''
        button_print_graph_info = tk.Button(root,
                            text="Save the information of the new graph",
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

        button_print_graph_info.grid(row=1, column=1)

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

        button_show_neighbors.grid(row=2, column=1)

    button_new_graph()
    button_print_graph_info()
    button_show_neighbors()

    def Entries_Create_Graph():
        '''Muestra de las distintas entradas que tiene el tk de crear un nuevo gráfico,
        son esecialmente las mismas que las de la interfaz, solo que estas actúan
        sobre un gráfico creado completamente por nosotros'''
        tk.Label(root, text="New node name").grid(row=2, column=2)
        tk.Label(root, text="X").grid(row=3, column=2)
        tk.Label(root, text="Y").grid(row=4, column=2)
        tk.Label(root, text="From").grid(row=6, column=2)
        tk.Label(root, text="To").grid(row=7, column=2)
        tk.Label(root, text="Delete Node").grid(row=9, column=2)
        tk.Label(root, text='Delete segment').grid(row=11, column=2)

        e_name = tk.Entry(root)  # New_node nombre
        e_x = tk.Entry(root)  # New_node valor x
        e_y = tk.Entry(root)  # New_node valor y
        e_from = tk.Entry(root)  # Origen new_segment
        e_to = tk.Entry(root)  # Destino new_segment
        e_delete_n = tk.Entry(root)  # Delete node
        e_delete_s = tk.Entry(root)  # Delete origin segment
        '''Las distinas entradas de texto'''

        e_name.grid(row=2, column=3)
        e_x.grid(row=3, column=3)
        e_y.grid(row=4, column=3)
        e_from.grid(row=6, column=3)
        e_to.grid(row=7, column=3)
        e_delete_n.grid(row=9, column=3)
        e_delete_s.grid(row=11, column=3)
        '''Posiciones de las entradas'''

        def add_node_new_graph():
            '''Añadimos un nodo nuevo a nuestro gráfico'''
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
            if SearchNode(M_Graph, name):
                print(f'Error: The node "{name}" already exists')
                return
            AddNode(M_Graph, Node(name, x, y))
            Plot(M_Graph)
            e_name.delete(0, 'end')
            e_x.delete(0, 'end')
            e_y.delete(0, 'end')

        def add_segment_new_graph():
            '''Añadimos un segmento nuevo a nuestro gráfico'''
            e_name_from = e_from.get().strip()  # Obtenemos de donde proviene
            e_name_to = e_to.get().strip()  # Obtenemos el nodo destinación
            if not e_name_from or not e_name_to:
                print("Error: You must write both nodes first.")
                return
            node_from = SearchNode(M_Graph, e_name_from)
            node_to = SearchNode(M_Graph, e_name_to)
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
                for s in M_Graph.segments)
            if segment_exists:
                print(f"Error: It already exists a segment between {e_name_from} and {e_name_to}")
                return
            AddSegment(M_Graph, e_seg, e_name_from, e_name_to)
            AddSegment(M_Graph, e_seg1, e_name_to, e_name_from)
            '''Añadimos estos segmentos a nuestro gráfico y fuente de información'''
            e_to.delete(0, 'end')
            e_from.delete(0, 'end')
            '''Limpiamos las entradas de texto'''
            Plot(M_Graph)

        def delete_node_new_graph():
            '''Eliminamos un nodo de nuestro gráfico'''
            node_name = e_delete_n.get().strip()
            if not node_name:
                print("Error: You must write the name of the node you want to delete.")
                e_delete_n.delete(0, 'end')
                return
            if not SearchNode(M_Graph, node_name):
                print(f"Error: The node '{node_name}' doesn't exists.")
                e_delete_n.delete(0, 'end')
                return
            DeleteNode(M_Graph, node_name)
            print(f"The node '{node_name}' was eliminated successfully.")
            e_delete_n.delete(0, 'end')
            Plot(M_Graph)

        def delete_segment_new_graph():
            '''Eliminamos un segmento de nuestro gráfico'''
            segment_name = e_delete_s.get().strip()
            if not segment_name:
                print("Error: You must write the name of the segment you want to delete.")
                e_delete_s.delete(0, 'end')
                return
            segment_to_delete = None
            for seg in M_Graph.segments:
                if seg.name == segment_name or seg.name == segment_name[::-1]:
                    segment_to_delete = seg
                    break
            if not segment_to_delete:
                print(f"Error: It doesn't exists any segment called '{segment_name}'")
                e_delete_s.delete(0, 'end')
                return
            DeleteSegment(M_Graph, segment_to_delete.name)
            print(f"Segment '{segment_to_delete.name}' deleted successfully.")
            e_delete_s.delete(0, 'end')
            Plot(M_Graph)

        tk.Button(root,
                      text="Add Node",
                      command=add_node_new_graph, cursor="hand2").grid(row=5, column=3)
        tk.Button(root, text="Add Segment",
                      command=add_segment_new_graph, cursor="hand2").grid(row=8, column=3)
        tk.Button(root, text="Delete Node",
                      command=delete_node_new_graph, cursor="hand2").grid(row=10, column=3)
        tk.Button(root, text='Delete Segment',
                      command=delete_segment_new_graph, cursor='hand2').grid(row=13, column=3)
        '''Los botones que llevan acabo todas estas acciones, cumplen la función de un enter'''

    Entries_Create_Graph()



    root.mainloop()