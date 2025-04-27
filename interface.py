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

def show_graph():
    G = CreateGraph_1() #Si quitamos este G = CreateGraph_1() los cambios que hagamos (por ej. añadir nodo o borrar nodos) se quedan guardados en el show graph
    Plot(G)

def show_graph_1():
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
                    graph_info.write(f'S,{segment.name},{segment.na.name},{segment.nb.name}\n')
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
            dist = Distance(segment.na, segment.nb)
            info_text += f"- {segment.name}: {segment.na.name} -> {segment.nb.name} (Distance: {dist})\n"
    else:
        info_text += "No segments in the graph\n"
    text_widget.insert(tk.END, info_text)

    save_button = tk.Button(info_window, text='Save the information', command=lambda: [save_info(), info_window.destroy()])
    save_button.pack(pady=9)
    close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
    close_button.pack(pady=10)

def show_neighbors():
    root = tk.Tk()
    root.title('GUI_SHOW_NEIGHBOURS')

    def Entries_neighbors():
        tk.Label(root, text="Insert the node whose neighbors you want to know").grid(row=1, column=2)
        e_name = tk.Entry(root)  # Node nombre
        e_name.grid(row=1, column=3)

        def Add_neighbors_node():
            e_node_name = e_name.get().strip()
            PlotNode(G, e_node_name)

        tk.Button(root, text='Search Node',
                command=Add_neighbors_node, cursor='hand2').grid(row=13, column=3)

    Entries_neighbors()

root = tk.Tk()
G = CreateGraph_1()
root.title("GUI")


def button1():
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
        G = read_file(e1.get())
        e1.delete(0, 'end')
        Plot(G)

    def entry2():
        G = CreateGraph_1()
        PlotNode(G, e2.get())

    def add_node():
        global G
        name = e_name.get().strip()
        x = float(e_x.get())
        y = float(e_y.get())
        if SearchNode(G, name):
            print('Ese nodo ya existe, escribe otro distinto')
        else:
            AddNode(G, Node(name, x, y))
            Plot(G)
            e_name.delete(0, 'end')
            e_x.delete(0, 'end')
            e_y.delete(0, 'end')

    def add_segment():
        global G
        e_name_from = e_from.get().strip()  # Get the "from" node name
        e_name_to = e_to.get().strip()  # Get the "to" node name
        e_seg = f"{e_name_from}{e_name_to}" # Create segment name
        e_seg1 = f"{e_name_to}{e_name_from}"

        # Call AddSegment with the segment name and node names
        AddSegment(G, e_seg, e_name_from, e_name_to)
        AddSegment(G, e_seg1, e_name_to, e_name_from)

        # Clear the entry fields
        e_to.delete(0, 'end')
        e_from.delete(0, 'end')

        # Plot the updated graph
        Plot(G)

    def delete_node():
        global G
        DeleteNode(G, e_delete_n.get())
        e_delete_n.delete(0, 'end')
        Plot(G)

    def delete_segment():
        global G
        e_delete_s.get()
        DeleteSegment(G, e_delete_s.get())
        e_delete_s.delete(0, 'end')
        Plot(G)

    def button3():
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
    
Entries()

root.mainloop()