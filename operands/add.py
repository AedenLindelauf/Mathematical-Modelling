from operands.fluid import FLUID

class ADD(FLUID):
    def __init__(self, *args):
        super().__init__(*args)
        
    def __str__(self):
        return " + ".join( [child.__str__() for child in self.children] )

    def simplify(self):
        from operands.node import NODE
        from operands.const import CONST
        # If the child has children, simplify the children
        for child in self.children:
            if isinstance(child, NODE) and (child is not None) and len(child.children) > 1: 
                child.simplify()

        # Add constants.
        list_of_constants = [i for i in range(len(self.children)) if isinstance(self.children[i], CONST)]
        if (len(list_of_constants) > 1):
            res = sum([self.children[i].value for i in list_of_constants])
            if len(list_of_constants) == len(self.children):
                self.__class__ = CONST
                self.value = res
            elif len(list_of_constants) <= len(self.children) - 1:
                first_constant = list_of_constants.pop(0) # Possible because len(list_of_constants) >= 2
                self.children[first_constant].value = res
                list_of_constants.reverse()
                for index in list_of_constants: self.children.pop(index)

        # Check for adding a zero
        for child in self.children:
            if isinstance(child, CONST) and (child.value == 0):
                self.children.remove(child)
                if len(self.children) == 1: # If there is only one child left we need to do something
                    self = self.children[0]


