# Parent class for inheritance.
class NODE:
    def __init__(self, *args): 
        self.children = [arg for arg in args]

    def simplify():
        pass


# Operators
class BINARY(NODE):
    def __init__(self, left = None, right = None):
        super().__init__(right, left) # Need to switch them around because for some reason python switches them around in the iterator

    def __str__(self, op: str):
        return f"{self.children[0].__str__()} {op} {self.children[1].__str__()}"
    
    def convert_to_common_operator_structure(self):
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
    
class FLUID(NODE):
    def __init__(self, *args):
        children = [arg for arg in args]
        if len(children) < 2: raise Exception("Fluid nodes need two or more operands!") # Not really necessary, just a sanity check
        super().__init__(*children)

    # In this function we find all the "adjacent" similar operators (so all +'s or *'s)
    def find_all_similar_adjacent_operators(self) -> list[NODE]:
        subtrees = [self]
        def descend(node: NODE):
            if isinstance(node, self.__class__):
                subtrees.append(node)
                for child in node.children:
                    descend(child)

        for child in self.children:
            descend(child)
        
        return subtrees
    
    # Here the actual transmutation of the tree happens
    def convert_to_common_operator_structure(self):
        subtrees = self.find_all_similar_adjacent_operators()
        children_changed = 0
        original_number_of_children = len(self.children)
        for tree in subtrees:
            for i in range(len(tree.children)):
                if not isinstance(tree.children[i], self.__class__):
                    if children_changed < original_number_of_children:
                        self.children[children_changed] = tree.children[i]
                        children_changed += 1
                    else:
                        self.children.append(tree.children[i])
        
        for child in self.children:
            if isinstance(child, (BINARY, FLUID) ):
                child.convert_to_common_operator_structure() # Top-down approach



class ADD(FLUID):
    def __init__(self, *args):
        super().__init__(*args)
        
    def __str__(self): 
        string = ""
        for child in self.children:
            string += child.__str__()
            string +=  " + "
        return string[:-3]

    def simplify(self):
        # If the child has children, simplify the children
        for child in self.children:
            if isinstance(child, NODE) and (child is not None) and len(child.children) > 1: 
                child.simplify()

        # Add constants.
        list_of_constants = [i for i in range(len(self.children)) if isinstance(self.children[i], CONST)]
        if (len(list_of_constants) > 1):
            res = sum([self.children[i].value for i in list_of_constants])
            if len(list_of_constants) == len(self.children):
                self.__class__ = CONST
                self.value = res
            elif len(list_of_constants) <= len(self.children) - 1:
                first_constant = list_of_constants.pop(0) # Possible because len(list_of_constants) >= 2
                self.children[first_constant].value = res
                list_of_constants.reverse()
                for index in list_of_constants: self.children.pop(index)

        # Check for adding a zero
        for child in self.children:
            if isinstance(child, CONST) and (child.value == 0):
                self.children.remove(child)
                if len(self.children) == 1: # If there is only one child left we need to do something
                    self = self.children[0]

        # Check for adding polynomials.


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

class MUL(FLUID):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        string = ""

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string += f"{child.__str__()}"
            else: string += f"( {child.__str__()} )"
            
            string += " * "

        return string[:-3]
    
    
    def simplify(self):
        # If the child has children, simplify the children
        for child in self.children:
            if isinstance(child, NODE) and (child is not None) and len(child.children) > 1: # i.e. the child is not a leaf
                child.simplify()

        # Multiply constants
        list_of_constants = [i for i in range(len(self.children)) if isinstance(self.children[i], CONST)]
        if (len(list_of_constants) > 1):
            res = 1
            for i in list_of_constants: res *= self.children[i].value
            if len(list_of_constants) == len(self.children):
                self.__class__ = CONST
                self.value = res
            elif len(list_of_constants) <= len(self.children) - 1:
                first_constant = list_of_constants.pop(0) # Possible because len(list_of_constants) >= 2
                self.children[first_constant].value = res
                for index in list_of_constants: self.children.pop(index)

        # checking for multiplication by 0
        for child in self.children:
            if isinstance(child, CONST) and (child.value == 0):
                self.__class__ = CONST
                self.value = 0
                return 

class DIV(BINARY):
    def __str__(self): return f"( {super().__str__('/')} )"

    def simplify(self):
        if (self.children[0] is not None) and isinstance(self.children[0], BINARY): self.children[0].simplify()
        if (self.children[1] is not None) and isinstance(self.children[1], BINARY): self.children[1].simplify()

        # https://www.youtube.com/watch?v=5vpdzRbfTIM

        # A fraction (a/b)/c can be written as a/(bc).
        if isinstance(self.children[0], DIV):
            ll, lr, r = self.children[0].children[0], self.children[0].children[1], self.children[1]
            self.children[0] = ll

            # If the denominator is a fraction, then we have (a/b)/(c/d) => (a)/((bc)/d) => (ad)/(bc)
            # Otherwise we have (a/b)/c => a/(bc).
            if isinstance(self.children[1], DIV):
                self.children[0] = MUL(ll, r.children[1])
                self.children[1] = MUL(lr, r.children[0])
            else: self.children[1] = MUL(lr, r)
        
        # Dividing by a fraction is multiplying by the reciprocal.
        if isinstance(self.children[1], DIV):

            left = MUL(self.children[0], self.children[1].children[1])
            right = self.children[1].children[0]

            self.children[0], self.children[1] = left, right

        # CONST division needs to be worked on, this is just the easy case
        if isinstance(self.children[0], CONST) and isinstance(self.children[1], CONST) and self.children[0].value % self.children[1].value == 0:
            self.__class__ = CONST
            self.value = int(self.children[0].value / self.children[1].value)
            return

        # Check whether divided by 1.
        self._check_identity_element(self.children[1], self.children[0], 1)

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


# Variables
class VAR(NODE):
    def __init__(self, val: str):
        super().__init__() # VAR also has the self.children attribute, to prevent potential errors. The list is empty so no strange things will occur
        self.value = val
    
    def __str__(self):
        return self.value




# Constants
class CONST(NODE):
    def __init__(self, val):
        super().__init__() # CONST also has the self.children attribute, to prevent potential errors. The list is empty so no strange things will occur
        self.value = val

    def __str__(self):
        return str(self.value)