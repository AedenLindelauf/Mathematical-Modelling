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
        
    def print_all_paths_to_nodes(self) -> list[int]:
        l = []
        print("hello")
        if isinstance(self, (CONST, VAR)): 
            return l
        
        def descend(node: NODE, lst: list[int]):
            if isinstance(node, (CONST, VAR)):
                print("Adding list ", lst, " because found node ", node.value)
                l.append(lst)
            if isinstance(node, BINARY): 
                lst1 = lst.copy() + [0]
                lst2 = lst.copy() + [1]
                descend(node.left, lst1)
                print("Descending left, with list ", lst1, " because found node", node.__str__)
                descend(node.right, lst2)
                print("Descending right, with list ", lst2, " because found node", node.__str__)
        
        if isinstance(self, BINARY):
            descend(self.left, [0])
            descend(self.right, [1])

        print(l)

        return l
    
def find_first(node: NODE, type, exclude = ()) -> list[int]:
    if isinstance(node, type):
        return []
    if isinstance(node, (CONST, VAR)):
        return [-1]
    if exclude != () and isinstance(node, exclude):
        return [-1]
        
    def descend(node: NODE, lst: list[int]):
        if isinstance(node, type):
            return lst
        if isinstance(node, exclude):
            return
        if isinstance(node, BINARY): # This assumes that node is not in exclude
            lst1 = lst.copy() + [0]
            lst2 = lst.copy() + [1]
            l = descend(node.left, lst1)
            if l is not None:
                return l
            r = descend(node.right, lst2)
            if r is not None:
                return r

    if isinstance(node, BINARY):
        l = descend(node.left, [0])
        if l is not None: return l
        r = descend(node.right, [1])
        if r is not None: return r
            
    return [-1]

def find_all(node: NODE, type, exclude: tuple = ()) -> list[list[int]]:
    paths = []
    if isinstance(node, type):
        return paths
    if isinstance(node, (CONST, VAR)):
        return [[-1]]
    if exclude is not () and isinstance(node, exclude):
        return [[-1]]
        
    def descend(node: NODE, lst: list[int]):
        if isinstance(node, type):
            paths.append(lst)
            return
        if isinstance(node, exclude):
            return
        if isinstance(node, BINARY): # This assumes that node is not in exclude
            lst1 = lst.copy() + [0]
            lst2 = lst.copy() + [1]
            descend(node.left, lst1)
            descend(node.right, lst2)

    if isinstance(node, BINARY):
        descend(node.left, [0])
        descend(node.right, [1])
            
    return paths

def find_all_tiered(node: NODE, type, exclude: tuple = ()) -> list[list[int]]:
    paths = []
    if isinstance(node, type):
        return paths
    if isinstance(node, (CONST, VAR)):
        return [[-1]]
    if exclude is not () and isinstance(node, exclude):
        return [[-1]]
        
    def descend(node: NODE, lst: list[int]):
        if isinstance(node, type):
            paths.append(lst)
            return
        if isinstance(node, exclude):
            return
        if isinstance(node, BINARY): # This assumes that node is not in exclude
            lst1 = lst.copy() + [0]
            lst2 = lst.copy() + [1]
            descend(node.left, lst1)
            descend(node.right, lst2)

    if isinstance(node, BINARY):
        descend(node.left, [0])
        descend(node.right, [1])
            
    return paths


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
    
    def divide_by_const(self):
        # Call only when actually dividing by a constant
        # We are in the situation where self.right is constant.
        # Remember that the children self.left and self.right have already been simplified!
        if isinstance(self.left, CONST):
            solution = self.left.value / self.right.value
            self.__class__ = CONST
            self.value = solution
            return
        if isinstance(self.left, MUL): # It is always the case that a const is placed before a variable or another mul
            path = find_first(self.left, CONST, (DIV, ADD, SUB, POW))
            if path == [-1] or path == []:
                return
            other_const_node = self.left
            for step in path:
                if step == 0: other_const_node = other_const_node.left
                if step == 1: other_const_node = other_const_node.right
            if isinstance(other_const_node, CONST): # sanity check
                other_const_node.value = other_const_node.value / self.right.value
                # For some reason it is paramount that right be copied first and then left!
                self.right = self.left.right
                self.left = self.left.left
                self.__class__ = MUL
        if isinstance(self.left, POW) or isinstance(self.left, VAR):
            return # Nothing that can be further simplified
        if isinstance(self.left, ADD):
            pass # This needs some discussion maybe
        if isinstance(self.left, SUB):
            pass # Same for subtraction

    def divide_by_var(self):
        # Call only when actually dividing by a variable
        # We are in the situation where self.right is variable.
        # Remember that the children self.left and self.right have already been simplified!
        if isinstance(self.left, VAR):
            if self.left.value == self.right.value:
                self.__class__ = CONST
                self.value = 1
            
        

    #def divide_long(self):
        # First check whether long division is possible on this division node
        #if (self.left is not None) and isinstance(self.left, BINARY): pass
        #if (self.right is not None) and isinstance(self.right, BINARY): pass
    #    pass


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

        if isinstance(self.right, CONST): 
            self.divide_by_const()
        #if isinstance(self.right, VAR):


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




# Constants
class CONST(NODE):
    def __init__(self, val):
        self.value = val

    def __str__(self):
        return str(self.value)