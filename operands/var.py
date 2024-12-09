from operands.node import NODE

class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value
    
    def simplify(self):
        return