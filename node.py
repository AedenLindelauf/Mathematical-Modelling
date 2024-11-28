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

    def differentiate(self, variable):

        if (self.left is not None) and isinstance(self.left, BINARY): self.left.differentiate(variable)
        if (self.right is not None) and isinstance(self.left, BINARY): self.right.differentiate(variable)

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

    def differentiate(self, variable: str) -> BINARY:
        new_left = self.left.differentiate(variable)
        new_right = self.right.differentiate(variable)
        return ADD(new_left, new_right)

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

    def differentiate(self, variable: str):
        new_left = self.left.differentiate(variable)
        new_right = self.right.differentiate(variable)
        return SUB(new_left, new_right)

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
    
    # Applying the product rule (f * g)' = f * g' + f' * g
    def differentiate(self, variable: str):
        # First we assign some variables
        f, g = self.left, self.right
        f_derivative = self.left.differentiate(variable)
        g_derivative = self.right.differentiate(variable)
        
        new_left = MUL(f, g_derivative)
        new_right = MUL(f_derivative, g)
        return ADD(new_left, new_right)

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

    # We apply the quotient rule (f / g)'= (f' * g - f * g') / ( g ^ 2)
    def differentiate(self, variable):
        f = self.left
        g = self.right
        f_derivative = f.differentiate(variable)
        g_derivative = g.differentiate(variable)
        new_right = POW(g, 2)
        new_left_left = MUL(f_derivative, g)
        new_left_right = MUL(f, g_derivative)
        new_left = SUB(new_left_left, new_left_right)
        return DIV(new_left, new_right)

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

    # Apply power rule if exponent is constant, else raise error not implemented
    def differentiate(self, variable: str):
        if isinstance(self.left, CONST) and ( (self.left.value == 0) and (self.right.value == 0)):
            raise Exception("0^0 undefined!")
        # Power rule: (a^b)' = a' * b * a ^ (b - 1)
        elif isinstance(self.right, CONST):
            a = self.left
            b = self.right
            new_b = CONST(b.value - 1)
            a_derivative = self.left.differentiate(variable)
            new_left = MUL(a_derivative, b)
            new_right = POW(a, new_b)
            return MUL(new_left, new_right)  
        else:
            raise Exception("Not implemented")

        



# Variables
class VAR(NODE):
    def __init__(self, val: str):
        self.value = val
    
    def __str__(self):
        return self.value
    
    # The derivative of a variable is 1 only if we differentiate with respect to that variable.
    def differentiate(self, variable: str) -> BINARY:
        if self.value == variable:
            return CONST(1)
        else:
            return CONST(0)


# Constants
class CONST(NODE):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)
    
    # The derivative of a constant is always 0
    def differentiate(self, variable: str) -> BINARY:
        return CONST(0)