from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from Create_New_Graph import *
root = tk.Tk()
root.geometry("1350x800")
root.title("GUI")
plot_frame = tk.Frame(root,pady=10)
plot_frame.grid(row=10, column=0, columnspan=10)
def button(command,tex,row,column,abg="blue",width=None,master=root):
    tk.Button(master=master,
        text=tex,
        command=command,
        activebackground=abg,
        activeforeground="white",
        anchor="center",
        bd=3,
        bg="lightgray",
        cursor="hand2",
        disabledforeground="gray",
        fg="black",
        font=("Roboto", 12),
        height=1,
        highlightbackground="black",
        highlightcolor="green",
        highlightthickness=2,
        justify="center",
        overrelief="raised",
        padx=5,
        pady=5,
        width=width,
        wraplength=100).grid(row=row, column=column)
def label(text, row, column,master=root):
    tk.Label(master=master, text=text, padx=10,font=7).grid(row=row, column=column)
def not_valid(row,column):
    #not valid msg for not valid inputs
    lb = tk.Message(root, text="Not Valid", bg='red')
    lb.grid(row=row, column=column)
    # noinspection PyTypeChecker
    root.after(1000, lb.destroy)
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
G = CreateGraph_1()

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
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=3, columnspan=20, padx=10, pady=10)

plotting_frame = tk.LabelFrame(root, text="Plotting Frame")
plotting_frame.config (width=600, height=480)
plotting_frame.grid(row=0, column=0,columnspan=1, padx=5, pady=5,
sticky=tk.N+ tk.E+ tk.W + tk.S)
def show_graph():
    '''Mostramos el gráfico original con los datos proporcionados arriba'''
    G = CreateGraph_1()
    show_new_graph()
b_original = button(lambda: show_graph(),"Show original graph",0,1,width=15,master=plotting_frame)
def show_graph_1():
    '''Mostramos el nuevo gráfico editado con nuevos segmentos , nodos
    y con los segmentos o nodos que hayamos eliminado '''
    show_new_graph()
b_edited = button(lambda: show_graph_1(),"Show edited graph",1,1,width=15,master=plotting_frame)
b_create = button(lambda: create_new_graph(),"Crete new graph",2,1,width=15,master=plotting_frame)
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
b_save = button(lambda: print_graph_info(),"Save the information",3,1,width=15,master=plotting_frame)

label("File Name",0,2,master=plotting_frame)
e1=tk.Entry(master=plotting_frame)
e1.grid(row=0,column=3)
def try_plot():
    e = e1.get()
    if e=="":
        not_valid(0,3)
    else:
        try:
            # Attempt to open the file
            with open(e, 'r') as file:
                G = read_file(e)
                show_new_graph()
                #custom_plot(Plot(G))
        except FileNotFoundError:
            not_valid(0,3)
button(lambda: try_plot(), "Show Graph",0,4,master=plotting_frame)

label("Node Name",1,2,master=plotting_frame)
e2 = tk.Entry(master=plotting_frame)
e2.grid(row=1, column=3)
def try_plotnode():
    if SearchNode(G, e2.get()) is None:
        not_valid(1, 3)
    else:
        show_new_graph()
        #custom_plot(PlotNode(G,e2.get()))
button(try_plotnode, "Show Node", 1, 4, master=plotting_frame)


addnode_frame = tk.LabelFrame(root, text="Add Node")
addnode_frame.config (width=600, height=480)
addnode_frame.grid(row=0, column=1,columnspan=1, padx=5, pady=5,
sticky=tk.N+ tk.E+ tk.W + tk.S)

label("Name",2,5,master=plotting_frame)
en = tk.Entry(master=plotting_frame)
en.grid(row=2, column=6)

label("X",0,5,master=plotting_frame)
ex = tk.Entry(master=plotting_frame)
ex.grid(row=0, column=6)

label("Y",1,5,master=plotting_frame)
ey = tk.Entry(master=plotting_frame)
ey.grid(row=1, column=6)

def try_addnode():
    try:
        if ex.get()!=""!=ey.get():
            x=float(ex.get())
            y=float(ey.get())
            AddNode(G, Node(en.get(), x, y))
        else:
            not_valid(3, 6)
    except ValueError:
        not_valid(3, 6)
    en.delete(0, 'end')
    ex.delete(0, 'end')
    ey.delete(0, 'end')
button(lambda: try_addnode(), "Add Node", 3, 6,master=plotting_frame)


label("From",0,7)
e_from = tk.Entry(root)
e_from.grid(row=0, column=8)

label("To",1,7)
e_to = tk.Entry(root)
e_to.grid(row=1, column=8)

def try_addsegment():
    o=e_from.get()
    d=e_to.get()
    if SearchNode(G,o) is None or SearchNode(G,d) is None or Segment(o+d, o, d) in G.segments:
        not_valid(2, 8)
    else:
        AddSegment(G, o+d, o, d)
    e_to.delete(0, 'end')
    e_from.delete(0, 'end')
button(lambda: try_addsegment(), "Add Segment", 2, 8)


label("Delete Node",0,9)
e_delete_n = tk.Entry(root)
e_delete_n.grid(row=0, column=10)
def try_deletenode():
    if SearchNode(G,e_delete_n.get().strip()) is None:
        not_valid(0, 11)
    else:
        DeleteNode(G, e_delete_n.get().strip())
    e_delete_n.delete(0, 'end')
button(lambda: try_deletenode(), "Delete", 0, 11)

label("Delete Segment",1,9)
e_delete_s = tk.Entry(root)
e_delete_s.grid(row=1, column=10)
def try_deletesegment():
    if SearchSegment(G,e_delete_s.get().strip()) is None:
        not_valid(1, 11)
    else:
        DeleteSegment(G, e_delete_s.get().strip())
    e_delete_s.delete(0, 'end')
button(lambda: try_deletesegment(), "Delete", 1, 11)

plot_frame = tk.LabelFrame(root, text="Plot Frame")
plot_frame.config (width=600, height=480)
plot_frame.grid(row=1, column=0,columnspan=4, padx=5, pady=5,
sticky=tk.N+ tk.E+ tk.W + tk.S)

def close():
    p.close('all')
    root.destroy()
button(lambda: close(),"Exit", 0, 12,"red")
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()