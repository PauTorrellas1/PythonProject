from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from Create_New_Graph import *
import tkinter as tk
from tkinter import messagebox
import threading
import heapq
from matplotlib.patches import ArrowStyle

root = tk.Tk()
current_display_mode = "edited"
message_label = None
clear_timer = None
fig = Figure(figsize=(8.5, 7), dpi=100)
ax = fig.add_subplot(111)
canvas = None