from operands.binary import BINARY
from operands.const import CONST

class SUB(BINARY):
    def __str__(self): return super().__str__("-")

    def latex(self): return self.__str__()

    def simplify(self):
        self.children[0].simplify()
        self.children[1].simplify()

        # Add constants.
        if isinstance(self.children[0], CONST) and isinstance(self.children[1], CONST):
            res = self.children[0].value - self.children[1].value
            self.__class__ = CONST
            self.value = res
