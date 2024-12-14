from operands.node import *
from operands.binary import BINARY
from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.mul import MUL
from operands.add import ADD 
from operands.sub import SUB

class Tree:
    def __init__(self, root: NODE):
        self.root = root
        self.preprocess(root)

    def __str__(self):
        return self.root.__str__()
    
    def simplify(self): 
        self.preprocess(self.root)
        self.root.simplify()
        #self.root.simplify()
        #self.root.simplify()
        # self.root.simplify()


    def convert_to_common_operator_structure(self):
        # Start the conversion process
        if isinstance(self.root, (BINARY, FLUID) ):
            self.root.convert_to_common_operator_structure()

    def preprocess(self, node):
        # This function still assumes that the tree is binary (as it was initially created)
        if isinstance(node, (CONST, VAR) ) or (node is None): return
        if isinstance(node, MUL) and isinstance(node.children[1], CONST):
            node.children[0], node.children[1] = node.children[1], node.children[0]
        
        # Change every SUB(a,b) node into ADD(a, MUL(CONST(-1), b))
        if isinstance(node, SUB):
            a = node.children[0]
            b = node.children[1]
            node.__class__ = ADD
            node.children[0] = a
            node.children[1] = MUL(CONST(-1), b)


        self.preprocess(node.children[0])
        self.preprocess(node.children[1])