from operands.fluid import FLUID
from operands.var import VAR
from operands.pow import POW
from copy import deepcopy

class ADD(FLUID):
    def __str__(self):
        return " + ".join( [child.__str__() for child in self.children] )
    
    def compare(tree1, tree2):
        if tree1.__class__ != tree2.__class__: 
            return False
        # alles in een list zetten, en dan kijken of het in die andere list zit, zo ja, haal dat eruit. Als empty list overblijft dan is het gelijk. 
        # een manier om 'injectivity' te checken. Dit werkt, alleen is computation time aanvaardbaar?
        # een snellere methode zou Hashen zijn, dan kan je sorten, maar dat is best complex
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
            

        # a + b*d + c + a
        # c + a + b*d + a 
        # dit moet gezien worden als hetzelfde


        #binary case:
        # tree1leaf1 = tree1.children[0]
        # tree1leaf2 = tree1.children[1]
        # tree2leaf1 = tree2.children[0]
        # tree2leaf2 = tree2.children[1]

        # if tree1leaf1.compare(tree2leaf1) and tree1leaf2.compare(tree2leaf2):
        #     print("case1")
        #     return True
        # elif tree1leaf1.compare(tree2leaf2) and tree1leaf2.compare(tree2leaf1):
        #     print("case2")
        #     return True
        # return False


        

    def simplify(self):
        from operands.node import NODE
        from operands.const import CONST
        from operands.mul import MUL
 
        # If the child has children, simplify the children
        for child in self.children:
            child.simplify()

        # ===========================================================================================
        # ====================================== Add constants ======================================
        # ===========================================================================================
        # Add constants. Checking for zero is obsolete since it is taken in the loop.
        new_children = [] # Keeps track of the children that are not constants.
        const_sum = 0     # Keeps track of the sum of the values of CONST children.
        for child in self.children:
             
             # If the child is a constant, update the const_sum value, otherwise 
             # append the child to the new_children array which takes O(1) amortized time.
             if isinstance(child, CONST): const_sum += child.value
             else: new_children.append(child)
        
        
        # If there is only one child, then it has to be a constant since it is the only node we always add.
        # Otherwise there are more constants.
        if new_children: 
             self.children = new_children
             if const_sum != 0: self.children.append(CONST(const_sum))
        else:
             self.__class__ = CONST
             self.value = const_sum
             return

        # ===========================================================================================
        # =========================================== END ===========================================
        # ===========================================================================================
       


        # ===========================================================================================
        # ========================== a * f + b * f = (a+b) * f, a,b \in \Q ==========================
        # ===========================================================================================

        # Keep track of the new children.
        new_children = []

        # Preprocessing: Make everything a MUL class.
        for i in range(len(self.children)):
            
            # Constants are already added so we can remove them.
            if isinstance(self.children[i], CONST): 
                new_children.append(self.children[i])
                self.children.pop(i) # can be made faster. Only executed once.
            
            elif not isinstance(self.children[i], MUL):
                temp = self.children[i]
                self.children[i] = MUL(None, None) # Make dummy MUL object.
                self.children[i].children = [CONST(1), temp]

            # It has to be a MUL class now.
            else: # Check if there is a constant in MUL object otherwise set it to 1.
                contains_const = False
                for index in range(len(self.children[i].children)):
                    if isinstance(self.children[i].children[index], CONST): 
                        contains_const = True
                        break

                if not contains_const: 
                    self.children[i].children.append(CONST(1))

        # Everything is a MUL class.
        i: int = len(self.children) - 1
        while i > 0:
            # We can assume that there is only one constant because of the other simplifcations.
            # Find the index of the constant to ignore it. If there is not constant, make it 1.
            f = self.children[i]
            # f can be written as f = a * p where a \in \Q a constant. 
            a, p = f.decompose()

            for j in range(i-1, -1, -1):
                g = self.children[j]
                # g can be written as g = b * q where b \in \Q a constant.
                b, q = g.decompose()

                if p.compare(q):
                    # We can add them.
                    # Swap the j-th entry with the i-1th entry and remove 
                    # the i-th entry since we add the i-1th and ith entry.
                    self.children[j]= self.children[i-1]
                    if isinstance(p, MUL):
                        self.children[i-1] = p
                        self.children[i-1].children.append( CONST(a.value + b.value) )
                    else:
                        self.children[i-1] = MUL(CONST(a.value + b.value), p)
                    i -= 1
                    self.children.pop()

            # After the for loop, we have added the items that are the same type.
            # So we push the last element to the new_children type. 
            new_children.append(self.children[-1])
            self.children.pop()
            i -= 1

        # If there is still one more element in the array, then we need to copy it as well.
        if len(self.children) == 1: new_children.append(self.children[0])
        
        if len(new_children) > 1:
            self.children = new_children
        else:
            self.__class__ = new_children[0].__class__
            self.children = new_children
                    

        
        # ===========================================================================================
        # =========================================== END ===========================================
        # ===========================================================================================
                        
               