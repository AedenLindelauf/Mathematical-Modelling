from operands.node import NODE

class CONST(NODE):
    def __init__(self, val):
        super().__init__() # CONST also has the self.children attribute, to prevent potential errors. The list is empty so no strange things will occur
        self.value = val

    def __str__(self):
        return str(self.value)
    
    def compare(leaf1, leaf2):
        if leaf1.__class__ != leaf2.__class__:
            return False
        elif leaf1.value == leaf2.value:
            return True
        return False

    def simplify(self):
        return