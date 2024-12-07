from operands.binary import BINARY
from operands.const import CONST
from operands.var import VAR

class POW(BINARY):
    def __str__(self): 
        res = ""

        if isinstance(self.children[0], (CONST, VAR) ):
            res += f"{self.children[0].__str__()}"
        else: res += f"( {self.children[0].__str__()} )"
        
        res += " ^ "

        if isinstance(self.children[1], (CONST, VAR) ):
            res += f"{self.children[1].__str__()}"
        else: res += f"( {self.children[1].__str__()} )"

        return res

    def simplify(self):
        if (self.children[0] is not None) and isinstance(self.children[0], BINARY): self.children[0].simplify()
        if (self.children[1] is not None) and isinstance(self.children[1], BINARY): self.children[1].simplify()
    
        # Check whether to the power of 1.
        self._check_identity_element(self.children[1], self.children[0], 1)

        # Check the cases a^0, 0^a or 0^0.
        if isinstance(self.children[0], CONST) and isinstance(self.children[1], CONST):
            if (self.children[0].value == 0) and (self.children[1].value == 0): raise Exception("0^0 undefined!!!")
            res = self.children[0].value ** self.children[1].value
            self.__class__ = CONST
            self.value = res
        elif isinstance(self.children[0], CONST) and ( (self.children[0].value == 0) or (self.children[0].value == 1) ):
            self.__class__ = CONST
            self.value = self.children[0].value
        elif isinstance(self.children[1], CONST) and ( self.children[1].value == 0 ):
            self.__class__ = CONST
            self.value = 1
