from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.node import NODE
from operands.add import ADD
from operands.pow import POW

class MUL(FLUID):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.__str__()}" )
            else: string.append( f"( {child.__str__()} )" )
        
        return " * ".join(string)
    
    def compare(tree1, tree2):
        if tree1.__class__ != tree2.__class__: 
            return False
        tree1children = tree1.children.copy()
        tree2children = tree2.children.copy()
        for child1 in tree1children:
            something_removed = False
            for child2 in tree2children:
                if child1.compare(child2):
                    tree2children.remove(child2)
                    something_removed = True 
                    break
            if not something_removed:
                return False
        
        return tree2children == []

    def simplify(self):

        # If the child has children, simplify the children
        for child in self.children:
            child.simplify()
        
        # Multiply constants. Checking for zero is obsolete since it is taken in the loop.
        const_prod = CONST(1)     # Keeps track of the sum of the values of CONST children.
        new_children = [const_prod] # Keeps track of the children.
        for child in self.children:
             # If the child is a constant, update the const_prod value, otherwise 
             # append the child to the new_children array which takes O(1) amortized time.
             if isinstance(child, CONST): const_prod.value *= child.value
             else: new_children.append(child)

        # If there is only one child, then it has to be a constant since it is the only node we always add.
        # Otherwise there are more constants.
        if const_prod.value == 0: 
             self.__class__ = CONST
             self.value = 0
        else:
             self.children = new_children
        

        # a^b * a^c = a^(b+c)
        base_exponent = {}
        new_children_exponent = []
        for child in self.children:

            if not isinstance(child, POW):
                base = child
                exponent = CONST(1)
                added = False
                
                for saved_base in base_exponent:
                    if base.compare(saved_base):
                        base_exponent[saved_base] = ADD(base_exponent[saved_base], exponent)
# .simplify toevoegen hier? 
                        added = True
                        break
                if not added:
                    base_exponent[base] = exponent
            else:
                base = child.children[0]
                exponent = child.children[1]
                added = False
                for saved_base in base_exponent:
                    if base.compare(saved_base):
                        base_exponent[saved_base] = ADD(base_exponent[saved_base], exponent)
# .simplify toevoegen hier?
                        added = True
                        break
                if not added:
                    base_exponent[base] = exponent


        for base, exponent in base_exponent.items():
            if exponent.__class__ == CONST:
                if exponent.value == 1:
                    new_children_exponent.append(base)
                else: 
                    new_children_exponent.append(POW(exponent, base))
            else:
                new_children_exponent.append(POW(exponent, base))
        
        if len(new_children_exponent) == 1:
            for base, exponent in base_exponent.items():
                self = POW(exponent, base)
                #is dit zo goed?
        else: 
            self.__class__ = MUL
            self.children = new_children_exponent
        #wat als het maar 1 power wordt? if len(new_child..) == 1: leaf maken, anders deze optie?

        #end of adding powers


        #a * (b + c)
        expansion = []

        for i, child in enumerate(self.children):

            if isinstance(child, ADD):
                for grandchild in child.children:
                    other_factors = self.children.copy()[:i] + self.children.copy()[i+1:] #everything except the expansion term
                    expanded = MUL(*(other_factors + [grandchild]))
                    expansion.append(expanded)
                self.__class__ = ADD
                self.children = expansion
                break
     
    def differentiate(self, variable: str):
        # We only implement differentiation for the binary tree. If there are more than 2 children, we raise an error.
        if len(self.children) > 2:
            raise AssertionError("Not implemented for non-binary trees")
        # We use the product rule: (f * g)' = f * g' + f' * g.
        f = self.children[0]
        g = self.children[1]

        f_derivative = f.differentiate(variable)
        g_derivative = g.differentiate(variable)

        new_left = MUL(f, g_derivative)
        new_right = MUL(f_derivative, g)
        return ADD(new_left, new_right)

                
        
