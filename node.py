# Parent class for inheritance.
class NODE:
    def __init__(self): pass


# Operands
class BINARY(NODE):
    def __init__(self, left = None, right = None):
        self.left, self.right = left, right

    def __str__(self, op: str):
        return f"{self.left.__str__()} {op} {self.right.__str__()}"
    
    def simplify(self):
        
        # Just some random code to check if the code works.
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()


class ADD(BINARY):
    def __str__(self): return super().__str__("+")

    def simplify(self):            
        if (self.left is not None) and isinstance(self.left, BINARY): self.left.simplify()
        if (self.right is not None) and isinstance(self.right, BINARY): self.right.simplify()

        if isinstance(self.left, CONST) and isinstance(self.right, CONST):
            res = self.left.value + self.right.value
            self.__class__ = CONST
            self.value = res

class SUB(BINARY):
    def __str__(self): return super().__str__("-")

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
        
        if isinstance(self.left, CONST) and isinstance(self.right, MUL):
            if isinstance(self.right.left, CONST):
                self.left.value = self.left.value * self.right.left.value
                self.right = self.right.right

class DIV(BINARY):
    def __str__(self): return f"( {super().__str__('/')} )"

    def simplify(self):
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


# Variables
class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value




# Constants
class CONST(NODE):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)