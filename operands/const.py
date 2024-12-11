from operands.node import NODE

class CONST(NODE):
    def __init__(self, val):
        super().__init__() # CONST also has the self.children attribute, to prevent potential errors. The list is empty so no strange things will occur
        self.value = val

    def __str__(self):
        return str(self.value)