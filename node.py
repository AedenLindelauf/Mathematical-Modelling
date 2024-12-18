# Parent class for inheritance.
from verification import *
from typing import Self

class NODE:
    def __init__(self): pass

    def __mul__(self, other):
        converted_other = self.convert_other(other)
        return MUL(self, converted_other)
    
    def __rmul__(self, other):
        converted_other = self.convert_other(other)
        return MUL(converted_other, self)
    
    def __add__(self, other):
        converted_other = self.convert_other(other)
        return ADD(self, converted_other)
    
    def __radd__(self, other):
        converted_other = self.convert_other(other)
        return ADD(converted_other, self)
    
    def __sub__(self, other):
        converted_other = self.convert_other(other)
        return SUB(self, converted_other)
    
    def __rsub__(self, other):
        converted_other = self.convert_other(other)
        return SUB(converted_other, self)

    def __div__(self, other):
        converted_other = self.convert_other(other)
        return DIV(self, converted_other)
    
    def __rdiv__(self, other):
        converted_other = self.convert_other(other)
        return DIV(converted_other, self)
    
    @staticmethod
    def convert_other(other : Self | int | str) -> Self:
        if isinstance(other, NODE):
            return other
        
        elif isinstance(other, int):
            return CONST(other)
        
        elif isinstance(other, str) and is_variable(other):
            return VAR(other)

        else:
            raise NotImplementedError(f"Cannot do that operation with a NODE and a {other.__class__.__name__}")
    




# Operands
class BINARY(NODE):
    def __init__(self, left = None, right = None):
        self.left, self.right = left, right

    def __str__(self, op: str):
        return f"{self.left.__str__()} {op} {self.right.__str__()}"
    
    def __repr__(self):
        return f"{self.__class__.__name__}(left = {self.left}, right = {self.right})"
    
    def simplify(self):
        
        # Just some random code to check if the code works.
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()

    def _check_identity_element(self, a: NODE, b: NODE, element: int) -> bool:
        # If zero is added, ignore it.
        if isinstance(a, CONST) and (a.value == element):
            if isinstance(b, (CONST, VAR) ):
                self.__class__ = b.__class__
                self.value = b.value

            else: # Binary operation
                self.__class__ = b.__class__
                self.left = b.left
                self.right = b.right
            
            return True
        return False


class ADD(BINARY):
    def __str__(self): return super().__str__("+")

    def simplify(self):            
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()

        # Add constants.
        if isinstance(self.left, CONST) and isinstance(self.right, CONST):
            res = self.left.value + self.right.value
            self.__class__ = CONST
            self.value = res

        # Maybe is checking the right branch unnecessary because of preprocessing.
        # Check whether 0 is added.
        if not self._check_identity_element(self.left, self.right, 0):
            self._check_identity_element(self.right, self.left, 0)

        # Check for adding polynomials.


class SUB(BINARY):
    def __str__(self): return super().__str__("-")

    def simplify(self):            
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()

        # Add constants.
        if isinstance(self.left, CONST) and isinstance(self.right, CONST):
            res = self.left.value - self.right.value
            self.__class__ = CONST
            self.value = res

class MUL(BINARY):
    def __str__(self): 
        res = ""
        
        if isinstance(self.left, (CONST, VAR) ):
            res += f"{self.left.__str__()}"
        else: res += f"( {self.left.__str__()} )"
        
        res += " * "

        if isinstance(self.right, (CONST, VAR) ):
            res += f"{self.right.__str__()}"
        else: res += f"( {self.right.__str__()} )"

        return res
    
    def simplify(self):
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()
        
        if isinstance(self.left, CONST) and isinstance(self.right, CONST):
            res = self.left.value * self.right.value
            self.__class__ = CONST
            self.value = res
            return
        
        if isinstance(self.left, CONST) and isinstance(self.right, MUL):
            if isinstance(self.right.left, CONST):
                self.left.value = self.left.value * self.right.left.value
                self.right = self.right.right
                return

        # Maybe is checking the right branch unnecessary because of preprocessing.
        # Check whether multiplied by 1.
        if not self._check_identity_element(self.left, self.right, 1):
            self._check_identity_element(self.right, self.left, 1)

        if isinstance(self.left, CONST) and (self.left.value == 0):
            self.__class__ = CONST
            self.value = 0
            return 

        if isinstance(self.right, CONST) and (self.right.value == 0):
            self.__class__ = CONST
            self.value = 0 
            return

class DIV(BINARY):
    def __str__(self): return f"( {super().__str__('/')} )"

    def simplify(self):
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()

        # https://www.youtube.com/watch?v=5vpdzRbfTIM

        # A fraction (a/b)/c can be written as a/(bc).
        if isinstance(self.left, DIV):
            ll, lr, r = self.left.left, self.left.right, self.right
            self.left = ll

            # If the denominator is a fraction, then we have (a/b)/(c/d) => (a)/((bc)/d).
            # Otherwise we have (a/b)/c => a/(bc).
            if isinstance(self.right, DIV):
                self.right = DIV(MUL(lr, r.left), r.right)

            else: self.right = MUL(lr, r)
        
        # Dividing by a fraction is multiplying by the reciprocal.
        if isinstance(self.right, DIV):

            left = MUL(self.left, self.right.right)
            right = self.right.left

            self.left, self.right = left, right

        # Check whether divided by 1.
        self._check_identity_element(self.right, self.left, 1)


class POW(BINARY):
    def __str__(self): 
        res = ""

        if isinstance(self.left, (CONST, VAR) ):
            res += f"{self.left.__str__()}"
        else: res += f"( {self.left.__str__()} )"
        
        res += " ^ "

        if isinstance(self.right, (CONST, VAR) ):
            res += f"{self.right.__str__()}"
        else: res += f"( {self.right.__str__()} )"

        return res

    def simplify(self):
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()
    
        # Check whether to the power of 1.
        self._check_identity_element(self.right, self.left, 1)

        # Check the cases a^0, 0^a or 0^0.
        if isinstance(self.left, CONST) and isinstance(self.right, CONST):
            if (self.left.value == 0) and (self.right.value == 0): raise Exception("0^0 undefined!!!")
            res = self.left.value ** self.right.value
            self.__class__ = CONST
            self.value = res
        elif isinstance(self.left, CONST) and ( (self.left.value == 0) or (self.left.value == 1) ):
            self.__class__ = CONST
            self.value = self.left.value
        elif isinstance(self.right, CONST) and ( self.right.value == 0 ):
            self.__class__ = CONST
            self.value = 1


# Variables
class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"{self.__class__.__name__}(val = {self.value})"




# Constants
class CONST(NODE):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(val = {self.value})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, CONST):
            return self.value == other.value
        
        return self.value == other
        

if __name__ == "__main__":
    print("a" * DIV(1, 2))