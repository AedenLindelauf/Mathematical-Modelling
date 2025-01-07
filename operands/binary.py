from operands.node import NODE
from operands.const import CONST
from operands.var import VAR

class BINARY(NODE):
    def __init__(self, left = None, right = None):
        super().__init__(left, right) # Need to switch them around because for some reason python switches them around in the iterator

    def __str__(self, op: str):
        return f"{self.children[0].__str__()} {op} {self.children[1].__str__()}"
    
    def convert_to_common_operator_structure(self):
        from operands.fluid import FLUID
        if isinstance(self.children[0], (BINARY, FLUID)):
            self.children[0].convert_to_common_operator_structure()
        if isinstance(self.children[1], (BINARY, FLUID)):
            self.children[1].convert_to_common_operator_structure()

    def _check_identity_element(self, a: NODE, b: NODE, element: int) -> bool:
        # If zero is added, ignore it.
        if isinstance(a, CONST) and (a.value == element):
            if isinstance(b, (CONST, VAR) ):
                self.__class__ = b.__class__
                self.value = b.value

            else: # Binary operation
                self.__class__ = b.__class__
                self.children[0] = b.children[0]
                self.children[1] = b.children[1]
            
            return True
        return False

