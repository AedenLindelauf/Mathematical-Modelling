from operands.binary import BINARY
from operands.const import CONST
from operands.var import VAR
from copy import deepcopy

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
        from operands.mul import MUL

        self.children[0].simplify()
        self.children[1].simplify()

        # Assume we have a^c.
        a = self.children[0]
        c = self.children[1]
    
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

        # Implement (a ... b) ^ c = (a ^ c) * ... * (b ^ c).
        if isinstance(a, MUL):
            for index in range(len(a.children)):
                a.children[index] = POW( deepcopy(c), a.children[index] )
            self.__class__ = MUL
            self.children = a.children

        # Check the case where we have (a^b)^c = a^(b * c).
        if isinstance(self.children[0], POW):
            a = self.children[0].children[0]
            b = self.children[0].children[1]
            c = self.children[1]
            self.children[0] = a
            self.children[1] = MUL(b, c)
        
        # Check the case where we have a^(b^c) = a^(b * c).
        if isinstance(self.children[1], POW):
            b = self.children[1].children[0]
            c = self.children[1].children[1]
            self.children[1] = MUL(b, c)