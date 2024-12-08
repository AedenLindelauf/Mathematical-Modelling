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
            if isinstance(child, NODE) and (child is not None) and len(child.children) > 1: # i.e. the child is not a leaf
                child.simplify()

        # Multiply constants
        list_of_constants = [i for i in range(len(self.children)) if isinstance(self.children[i], CONST)]
        if (len(list_of_constants) > 1):
            res = 1
            for i in list_of_constants: res *= self.children[i].value
            if len(list_of_constants) == len(self.children):
                self.__class__ = CONST
                self.value = res
            elif len(list_of_constants) <= len(self.children) - 1:
                first_constant = list_of_constants.pop(0) # Possible because len(list_of_constants) >= 2
                self.children[first_constant].value = res
                for index in list_of_constants: self.children.pop(index)

        # checking for multiplication by 0
        for child in self.children:
            if isinstance(child, CONST) and (child.value == 0):
                self.__class__ = CONST
                self.value = 0
                return 
