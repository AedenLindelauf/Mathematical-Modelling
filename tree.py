from node import *

class Tree:
    def __init__(self, root: NODE):
        self.root = root

    def __str__(self):
        return self.root.__str__()
    
    def simplify(self): 
        self.root.simplify()