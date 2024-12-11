from tkinter import *
from tree import Tree
from node import *
from shunting_yard import *
from sys import exit

from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self):
        # https://www.tutorialspoint.com/how-to-display-latex-in-real-time-in-a-text-box-in-tkinter
        # Use TkAgg in the backend of tkinter application
        matplotlib.use('TkAgg') 

        root = Tk()

        root.title("Amazing mathematica copy")
        root.geometry('800x250')
        root.configure(bg='lightgray')

        # all widgets will be here

        self.input_label = Label(root, text="Input:", font=("Helvetica", 12, "bold"), bg='lightgray')
        self.output_label = Label(root, text="Output:", font=("Helvetica", 12, "bold"), bg='lightgray')

        self.input_label.grid(row=0, column=0, sticky='E')
        self.output_label.grid(row=1, column=0, sticky='E')

        self.input_expr = Text(root, height=5, width=50)
        self.input_expr.grid(row=0, column=1, columnspan = 2, pady=(10, 10), sticky='W' )

        self.output_expr = Text(root, height=5, width=50)
        self.output_expr.grid(row=1, column=1, columnspan = 2, pady=(10, 10), sticky='W' )

        # Create a Frame object
        frame = Frame(root)
        frame.grid(row=1, column=3, columnspan=2)

        # Add a label widget in the frame
        label = Label(frame)
        label.pack()

        # Define the figure size and plot the figure
        fig = matplotlib.figure.Figure(figsize=(2, 1), dpi=100, frameon=False)
        matplotlib.pyplot.axis('off')
        self.wx = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=label)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.wx.axis('off')

        # Set the visibility of the Canvas figure
        self.wx.get_xaxis().set_visible(False)
        self.wx.get_yaxis().set_visible(False)

        button_simplify = Button(root, text="Simplify", command=lambda: self._simplify(), font=("Helvetica", 10, "bold") )
        button_simplify.grid(row=2, column=1)

        button_differentiate = Button(root, text="Differentiate", command=lambda: self._differentiate(), font=("Helvetica", 10, "bold"))
        button_differentiate.grid(row=2, column=2)

        # https://stackoverflow.com/questions/75347277/my-terminal-is-still-running-after-my-tkinter-window-has-closed-and-i-cant-use-c
        root.protocol("WM_DELETE_WINDOW", lambda:on_closing_window())

        def on_closing_window():
            root.destroy()
            exit()

        # Execute Tkinter
        root.mainloop()

    def _simplify(self):
        def graph(text):
            # Get the Entry Input
            tmptext = self.input_expr.get("1.0","end-1c")
            tmptext = "$"+tmptext+"$"
            # Clear any previous Syntax from the figure
            self.wx.clear()
            self.wx.text(0.5, 0.5, tmptext, fontsize = 12, ha='center', transform=self.wx.transAxes)
            self.canvas.draw_idle()
            self.wx.axis('off')
        graph("")

        # expr = self.input_expr.get("1.0","end-1c")
        # self.output_expr.delete(1.0, END)
        # if not expr: return self.output_expr.insert(END, "0")
        
        # post_fixer = Post_Fixer(expr)
        # test_tree = create_tree(post_fixer.postfix_notation)
        # test_tree.simplify()
        # res = test_tree.__str__()
        # self.output_expr.insert(END, res)


    def _differentiate(self, expr: str):
        pass