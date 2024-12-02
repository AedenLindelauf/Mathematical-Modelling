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
        if isinstance(node, CONST ) or (node is None): return

        # This is basically to ensure the situation that 2*x + x = 2*x + 1*x = (2+1) * x
        if isinstance(node , VAR):
            v = node.value
            node.__class__ = MUL
            node.left = CONST(1)
            node.right = VAR(v)
            return

        self.preprocess(node.left)
        self.preprocess(node.right)

        if isinstance(node, MUL) and isinstance(node.right, CONST):
            node.left, node.right = node.right, node.left
    
        
    def postprocess(self, node):

        if isinstance(node, MUL):
            # Maybe is checking the right branch unnecessary because of preprocessing.
            # Check whether multiplied by 1.
            if not node._check_identity_element(self.left, self.right, 1):
                node._check_identity_element(self.right, self.left, 1)