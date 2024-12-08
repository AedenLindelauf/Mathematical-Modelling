from operands.node import NODE

class VAR(NODE):
    def __init__(self, val: str):
        super().__init__() # VAR also has the self.children attribute, to prevent potential errors. The list is empty so no strange things will occur
        self.value = val
    
    def __str__(self):
        return self.value
