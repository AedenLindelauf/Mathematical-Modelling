from copy import deepcopy
from operands.fluid import FLUID

class MUL(FLUID):
    def __str__(self):
        from operands.const import CONST
        from operands.var import VAR
        
        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.__str__()}" )
            else: string.append( f"( {child.__str__()} )" )
        
        return " * ".join(string)
    
    def latex(self):
        from operands.const import CONST
        from operands.var import VAR

        string = []

        for child in self.children:
            if isinstance(child, (CONST, VAR) ):
                string.append( f"{child.latex()}" )
            else: string.append( f"( {child.latex()} )" )
        
        return r" \cdot ".join(string)

    def decompose(self):
            """
            Returns the const (1 if not present) and the remaining term.
            """
            from operands.const import CONST

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
        from operands.const import CONST
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
        from operands.div import DIV
        from operands.fluid import FLUID
        from operands.const import CONST
        from operands.var import VAR
        from operands.node import NODE
        from operands.add import ADD
        from operands.pow import POW

        
        # Check if any of the children is also a MUL class, otherwise take this into account in the current MUL object.
        # This has to be done since we to convert (2x)/y to 2(x/y).
        index_to_be_removed =[] # This will be slow but can be made faster later. 
        length = len(self.children)
        for i in range(length):
            child = self.children[i]
            if isinstance(child, MUL):
                index_to_be_removed.append(i)
                for elt in child.children:
                    self.children.append(elt)

        index_to_be_removed = index_to_be_removed[::-1] # Decreasing order to not screw up indices in removal.
        for i in index_to_be_removed: self.children.pop(i)

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
            self.children = []
            return

        

        #eerst het probleem van die a *(a*1) oplossen, kan weg als *1 weg is.
        if isinstance(self, (CONST, VAR)):
            return 

        for child in self.children:
            if isinstance(child, MUL):
                self.children.remove(child)
                for grandchild in child.children:
                    self.children.append(grandchild)

        
        #a * (b + c) ===================================================
        expansion = []
        
        for i, child in enumerate(self.children):
            
            if isinstance(child, ADD):
                for grandchild in child.children:
                    other_factors = self.children.copy()[:i] + self.children.copy()[i+1:] #everything except the expansion term
                    expanded = MUL(*(deepcopy(other_factors + [grandchild])))
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
                for child in self.children: child.simplify()
                return
                #is dit zo goed?
        else: 
            self.__class__ = MUL
            self.children = new_children_exponent
        #wat als het maar 1 power wordt? if len(new_child..) == 1: leaf maken, anders deze optie?

        #end of adding powers


        # ===========================================================================================
        # ========================= Check if one of children is a fraction ==========================
        # ===========================================================================================

        # Move everything inside one fraction.
        # Leave constants out of div.
        
        div_present = False
        index_of_div = None

        for i in range(len(self.children)):
            if isinstance(self.children[i], DIV):
                div_present = True
                index_of_div = i
                break

        if div_present:
            new_children = [self.children[index_of_div]]
            self.children.pop(index_of_div)
            # There should be one constant.

            for i in range(len(self.children)):
                child = self.children[i]
                if isinstance(child, DIV):
                    new_children[0].children[0] = MUL( child.children[0], new_children[0].children[0] )
                    new_children[0].children[1] = MUL( child.children[1], new_children[0].children[1] )
                else:
                    new_children[0].children[0] = MUL(child, new_children[0].children[0])
            
            if len(new_children) == 1:
                child = new_children[0]
                self.__class__ = new_children[0].__class__
                if isinstance(child, (VAR, CONST)):
                    self.value = child.value
                    return
                else:
                    self.children = new_children[0].children
            else:
                self.children = new_children
        
        # If the child has children, simplify the children
        for child in self.children: 
            child.simplify()
        
        
        
        
    def differentiate(self, variable: str):
        from operands.pow import POW
        from operands.mul import MUL
        from operands.add import ADD
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