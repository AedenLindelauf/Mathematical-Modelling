from operands.node import NODE

class CONST(NODE):
    def __init__(self, val):
        # The commented code below could be used later to define constants like pi+1 or 2*pi.
        # super().__init__() 
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