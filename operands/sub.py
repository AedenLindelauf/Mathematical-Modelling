from operands.binary import BINARY
from operands.const import CONST

class SUB(BINARY):
    def __str__(self): return super().__str__("-")

    def simplify(self):
        if (self.children[0] is not None) and isinstance(self.children[0], BINARY): self.children[0].simplify()
        if (self.children[1] is not None) and isinstance(self.children[1], BINARY): self.children[1].simplify()

        # Add constants.
        if isinstance(self.children[0], CONST) and isinstance(self.children[1], CONST):
            res = self.children[0].value - self.children[1].value
            self.__class__ = CONST
            self.value = res

    def differentiate(self, variable: str):
        # Same rules apply as for add.
        new_left = self.children[0].differentiate(variable)
        new_right = self.children[1].differentiate(variable)
        return SUB(new_right,new_left)
