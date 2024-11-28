from node import *

class Tree:
    def __init__(self, root: NODE):
        self.root = root

    def __str__(self):
        return self.root.__str__()
    
    def simplify(self): 
        self.preprocess(self.root)
        self.root.simplify()
    
    def differentiate(self, variable: str = "x"):
        self.preprocess(self.root)
        return Tree(self.root.differentiate(variable))

    def preprocess(self, node):
        if isinstance(node, (CONST, VAR) ) or (node is None): return
        if isinstance(node, MUL) and isinstance(node.right, CONST):
            node.left, node.right = node.right, node.left
        
        self.preprocess(node.left)
        self.preprocess(node.right)