from operands.node import NODE

class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value
    
    def latex(self): return self.value
    
    def compare(leaf1, leaf2):
        if leaf1.__class__ != leaf2.__class__:
            return False
        if leaf1.value == leaf2.value:
            return True
        return False

    def simplify(self):
        return