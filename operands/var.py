from operands.node import NODE
from operands.const import CONST

class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value
    
    def compare(leaf1, leaf2):
        if leaf1.__class__ != leaf2.__class__:
            return False
        if leaf1.value == leaf2.value:
            return True
        return False

    def simplify(self):
        return
    
    def differentiate(self, variable: str):
        # We differentiate with respect to variable.
        if self.value == variable:
            return CONST(1)
        else: 
            return CONST(0)