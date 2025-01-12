from tkinter import *
from tree import Tree
from sys import exit
from expression import Expression

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

        root.title("Symbolic Manipulations")
        root.geometry('800x250')
        root.configure(bg='lightgray')

        # all widgets will be here

        self.input_label = Label(root, text="Input:", font=("Helvetica", 12, "bold"), bg='lightgray')
        self.output_label = Label(root, text="Output:", font=("Helvetica", 12, "bold"), bg='lightgray')

        self.input_label.grid(row=0, column=0, sticky='E')
        self.output_label.grid(row=1, column=0, sticky='E')

        self.input_expr = Text(root, height=5, width=50)
        self.input_expr.grid(row=0, column=1, columnspan = 2, pady=(10, 10), sticky='W' )

        self.input_expr.bind('<KeyRelease>', self._on_update)
        self.input_expr.focus_set()    

        self.output_expr = Text(root, height=5, width=50)
        self.output_expr.grid(row=1, column=1, columnspan = 2, pady=(10, 10), sticky='W' )

        # Add a label widget in the frame
        label_input = Label(root)
        label_input.grid(row=0, column=3, columnspan=2 , padx=(10,10), pady=(10,10), sticky='W')

        # Define the figure size and plot the figure
        fig = matplotlib.figure.Figure(figsize=(2.5, 0.825), dpi=100, frameon=False)
        self.wx_label_input = fig.add_subplot(111)
        self.canvas_input = FigureCanvasTkAgg(fig, master=label_input)
        self.canvas_input.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas_input._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.wx_label_input.axis('off')

        # Set the visibility of the Canvas figure
        self.wx_label_input.get_xaxis().set_visible(False)
        self.wx_label_input.get_yaxis().set_visible(False)

        label_output = Label(root)
        label_output.grid(row=1, column=3, columnspan=2, padx=(10,10), pady=(10,10), sticky='W')

        # Define the figure size and plot the figure
        fig = matplotlib.figure.Figure(figsize=(2.5, 0.825), dpi=100, frameon=False)
        self.wx_label_output = fig.add_subplot(111)
        self.canvas_output = FigureCanvasTkAgg(fig, master=label_output)
        self.canvas_output.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas_output._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.wx_label_output.axis('off')

        # Set the visibility of the Canvas figure
        self.wx_label_output.get_xaxis().set_visible(False)
        self.wx_label_output.get_yaxis().set_visible(False)

        button_simplify = Button(root, text="Simplify", command=lambda: self._simplify(), font=("Helvetica", 10, "bold") )
        button_simplify.grid(row=2, column=1, columnspan=2)

        button_differentiate = Button(root, text="Differentiate", command=lambda: self._differentiate(), font=("Helvetica", 10, "bold"))
        self.diff_var = Text(root, height=1, width=1)
        self.diff_var.grid(row=2, column=3, sticky='W' , padx=(75, 0))
        self.diff_var.insert(END, "x")
        button_differentiate.grid(row=2, column=4)

        # https://stackoverflow.com/questions/75347277/my-terminal-is-still-running-after-my-tkinter-window-has-closed-and-i-cant-use-c
        root.protocol("WM_DELETE_WINDOW", lambda:on_closing_window())

        def on_closing_window():
            root.destroy()
            exit()

        # Execute Tkinter
        root.mainloop()

    def _on_update(self, event):
        # Get the Entry Input
        expr = self.input_expr.get("1.0","end-1c")

        try:
            expr = Expression(expr)
            tr = expr.tree
            tr.convert_to_common_operator_structure()

            tmptext = "$" + tr.latex() + "$"

            # Clear any previous Syntax from the figure
            self.wx_label_input.clear()
            self.wx_label_input.text(0.5, 0.5, tmptext, fontsize = 12, ha='center', transform=self.wx_label_input.transAxes)
            self.canvas_input.draw_idle()
            self.wx_label_input.axis('off')

        except Exception as e:
            print(e)
            self.wx_label_input.clear()
            self.wx_label_input.text(0.5, 0.5, "Invalid input...", fontsize = 12, ha='center', transform=self.wx_label_input.transAxes, color="red")
            self.canvas_input.draw_idle()
            self.wx_label_input.axis('off')
        

    def _simplify(self):
        
        expr = self.input_expr.get("1.0","end-1c")
        self.output_expr.delete(1.0, END)
        if not expr: return self.output_expr.insert(END, "0")
        self.wx_label_output.clear()
        
        try:
            expr = Expression(expr)
            tr = expr.tree
            tr.simplify()

            res = tr.__str__()

            self.output_expr.insert(END, res)
            self.output_expr.config(foreground="black")
        
            latex_res = tr.latex()
        
            tmptext = "$"+latex_res+"$"
            self.wx_label_output.text(0.5, 0.5, tmptext, fontsize = 12, ha='center', transform=self.wx_label_output.transAxes)
        
        except Exception as e:
            print(e)
            self.output_expr.insert(END, "Oops, an error occured...")
            self.output_expr.config(foreground="red")
        
        self.canvas_output.draw_idle()
        self.wx_label_output.axis('off')

    def _differentiate(self):
        expr = self.input_expr.get("1.0","end-1c")
        differentiation_variable = self.diff_var.get("1.0","end-1c")
        self.output_expr.delete(1.0, END)
        if not expr: return self.output_expr.insert(END, "0")
        self.wx_label_output.clear()
        
        try:
            expr = Expression(expr)
            tr = expr.tree
            print(tr)
            new_tr = tr.differentiate(differentiation_variable)
            print(new_tr)
            new_tr.simplify()
            print(new_tr)
            res = new_tr.__str__()

            self.output_expr.insert(END, res)
            self.output_expr.config(foreground="black")
        
            latex_res = new_tr.latex()
        
            tmptext = "$"+latex_res+"$"
            self.wx_label_output.text(0.5, 0.5, tmptext, fontsize = 12, ha='center', transform=self.wx_label_output.transAxes)
        
        except Exception as e:
            print(e)
            self.output_expr.insert(END, "Oops, an error occured...")
            self.output_expr.config(foreground="red")
        
        self.canvas_output.draw_idle()
        self.wx_label_output.axis('off')


if __name__ == "__main__":
    gui = GUI()