from operands.node import *
from operands.binary import BINARY
from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.mul import MUL
from operands.div import DIV
from operands.add import ADD 
from operands.sub import SUB
from copy import deepcopy

class Tree:
    def __init__(self, root: NODE):
        self.root = root
        self.preprocess(root)

    def __str__(self):
        return self.root.__str__()
    
    def simplify(self):
        self.preprocess(self.root)
        self.convert_to_common_operator_structure()
        
        old = deepcopy(self.root)
        # for i in range(10):
        #     self.root.simplify()

        self.root.simplify()
        iterations = 1

        while(not old.compare(self.root)):
            old = deepcopy(self.root)
            self.root.simplify()
            iterations += 1

        self.postprocess(self.root)
        # print(f"Num of iterations: {iterations}")

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
            node.children = [a, MUL(CONST(-1), b)] 

        # Multiply everything by one. The simplification should solve this.


        self.preprocess(node.children[0])
        self.preprocess(node.children[1])

    def postprocess(self, node):
        "1 * f => f and -1 * c = -c"
        if isinstance(node, MUL):
            new_children = []
            for item in node.children:
                if not(isinstance(item, CONST) and item.value == 1):
                    new_children.append(item)
            if len(new_children) == 1:
                node.__class__ = new_children[0].__class__
                node.value = new_children[0].value
                return
            else:
                node.children = new_children

            # Now check for -1 * const * f(x).
            new_children = []
            c = 1
            for item in node.children:
                if isinstance(item, CONST):
                    c *= item.value
                else:
                    new_children.append(item)

            if c != 1: new_children.append(CONST(c))

            if len(new_children) == 1:
                node.__class__ = new_children[0].__class__
                node.value = new_children[0].value
            else:
                node.children = new_children

        if not isinstance(node, (VAR, CONST)):
            for child in node.children:
                self.postprocess(child)