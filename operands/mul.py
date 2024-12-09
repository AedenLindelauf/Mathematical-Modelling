from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.node import NODE

class MUL(FLUID):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.__str__()}" )
            else: string.append( f"( {child.__str__()} )" )
        
        return " * ".join(string)
    

    def simplify(self):
        # If the child has children, simplify the children
        for child in self.children:
            child.simplify()

        # Multiply constants. Checking for zero is obsolete since it is taken in the loop.
        const_prod = CONST(1)     # Keeps track of the sum of the values of CONST children.
        new_children = [const_prod] # Keeps track of the children.
        for child in self.children:
             
             # If the child is a constant, update the const_prod value, otherwise 
             # append the child to the new_children array which takes O(1) amortized time.
             if isinstance(child, CONST): const_prod.value *= child.value
             else: new_children.append(child)
        
        # If there is only one child, then it has to be a constant since it is the only node we always add.
        # Otherwise there are more constants.
        if const_prod.value == 0: 
             self.__class__ = CONST
             self.value = 0
        else:
             self.children = new_children