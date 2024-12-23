from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.node import NODE
from operands.add import ADD
from operands.pow import POW
from copy import deepcopy

class MUL(FLUID):
    def __str__(self):
        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.__str__()}" )
            else: string.append( f"( {child.__str__()} )" )
        
        return " * ".join(string)
    
    def latex(self):
        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.__str__()}" )
            else: string.append( f"( {child.__str__()} )" )
        
        return r" \cdot ".join(string)

    def decompose(self):
            """
            Returns the const (1 if not present) and the remaining term.
            """
            f = deepcopy(self) # f is constructed as f = a * g
            a = CONST(1)

            for index in range(len(f.children)):
                item = f.children[index]
                if isinstance(item, CONST):
                    a = item
                    # Swap element at index "index" and last index. 
                    f.children[index] = f.children[-1]
                    f.children[-1] = item
                    # Remove last element.
                    f.children.pop()
                    break
            return a, f


    def compare(tree1, tree2):
        if tree1.__class__ != tree2.__class__: 
            return False
        tree1children = tree1.children.copy()
        tree2children = tree2.children.copy()
        for child1 in tree1children:
            if child1.compare(CONST(1)):
                continue
            something_removed = False
            for child2 in tree2children:
                if child1.compare(child2):
                    tree2children.remove(child2)
                    something_removed = True 
                    break
            if not something_removed:
                return False
        if tree2children:
            for leftover in tree2children:
                if not leftover.compare(CONST(1)):
                    return False
            return True
        else: 
            return True



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
        if len(new_children) == 1: 
             self.__class__ = CONST
             self.value = const_prod.value
             return # No other simplifcations applicable to CONST.
        elif new_children[0].value == 1:
            pass
        else:
             self.children = new_children
        
        if self.decompose()[0].value == 0:
            self.__class__ = CONST
            self.value = 0


        #a * (b + c) ===================================================

        #eerst het probleem van die a *(a*1) oplossen, kan weg als *1 weg is.
        for child in self.children:
            if isinstance(child, MUL):
                self.children.remove(child)
                for grandchild in child.children:
                    self.children.append(grandchild)


        expansion = []

        for i, child in enumerate(self.children):
            
            if isinstance(child, ADD):
                for grandchild in child.children:
                    other_factors = self.children.copy()[:i] + self.children.copy()[i+1:] #everything except the expansion term
                    expanded = MUL(*(other_factors + [grandchild]))
                    expansion.append(expanded)
                self.__class__ = ADD
                self.children = expansion
                return

        #END OF a * (b + c) ===================================================            

    #door deze twee (boven en onder) om te draaien kunnen we expansion en samenvoegen van machten 
    #prioritiseren ofniet?


        # a^b * a^c = a^(b+c)
        base_exponent = {}
        new_children_exponent = []

        for child in self.children:
            if not isinstance(child, POW):
                base = child
                exponent = CONST(1)
                added = False
                #het wordt hier ergens niet goed toegevoegd
                for saved_base in base_exponent:
                    if base.compare(saved_base):
                        base_exponent[saved_base] = ADD(base_exponent[saved_base], exponent)
                        added = True
                        break
                if not added:
                    base_exponent[base] = exponent
                # for base, exponent in base_exponent.items(): print("si", base,exponent)
            else:
                base = child.children[0]
                exponent = child.children[1]
                added = False
                for saved_base in base_exponent:
                    if base.compare(saved_base):
                        base_exponent[saved_base] = ADD(base_exponent[saved_base], exponent)
                        added = True
                        break
                if not added:
                    base_exponent[base] = exponent

        for base, exponent in base_exponent.items():
            if exponent.__class__ == CONST:
                if exponent.value == 1:
                    new_children_exponent.append(base)
                else: 
                    new_children_exponent.append(POW(base, exponent))
            else:
                new_children_exponent.append(POW(base, exponent))

        if len(new_children_exponent) == 1:
            for base, exponent in base_exponent.items():
                self.__class__ = POW
                self.children = [base, exponent]
                # self = POW(exponent, base)
                return
                #is dit zo goed?
        else: 
            self.__class__ = MUL
            self.children = new_children_exponent
        #wat als het maar 1 power wordt? if len(new_child..) == 1: leaf maken, anders deze optie?

        #end of adding powers




             

                
        
