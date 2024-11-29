from tkinter import *
from tree import Tree
from node import *
from shunting_yard import *

class GUI:
    def __init__(self):
        root = Tk()

        root.title("Amazing mathematica copy")
        root.geometry('500x250')
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

        button_simplify = Button(root, text="Simplify", command=lambda: self._simplify(), font=("Helvetica", 10, "bold") )
        button_simplify.grid(row=2, column=1)

        button_differentiate = Button(root, text="Differentiate", command=lambda: self._differentiate(), font=("Helvetica", 10, "bold"))
        button_differentiate.grid(row=2, column=2)


        # Execute Tkinter
        root.mainloop()

    def _simplify(self):
        expr = self.input_expr.get("1.0","end-1c")
        self.output_expr.delete(1.0, END)
        if not expr: return self.output_expr.insert(END, "0")
        
        post_fixer = Post_Fixer(expr)
        test_tree = create_tree(post_fixer.postfix_notation)
        test_tree.simplify()
        res = test_tree.__str__()
        self.output_expr.insert(END, res)


    def _differentiate(self, expr: str):
        pass