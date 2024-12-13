from operands.fluid import FLUID
from operands.var import VAR
from operands.pow import POW

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

       
        
        #constant*(iets) bij elkaar optellen
        adding_together = {}
        
        for child in self.children:       
            if isinstance(child, MUL):
                for i, grandchild in enumerate(child.children):
                #if isinstance != var(x), dan kan je buiten haakjes halen?
                    if isinstance(grandchild, CONST):
                        other_factors = child.children[:i] + child.children[i+1:]
                        if len(other_factors) != 1:
                            other_factors = MUL(*(other_factors))
                        else:
                            other_factors = other_factors[0]
                        #print(other_factors, grandchild)
                        added = False
                        for expression in adding_together:
                            if other_factors.compare(expression):
                                adding_together[expression] = ADD(adding_together[expression], grandchild)
                                added = True
                        if not added:
                            adding_together[other_factors] = grandchild
                        break
            else:    #if isinstance(child, VAR) or isinstance(child, POW): #is dit in nog meer situaties?
                added = False
                for expression in adding_together:
                    if child.compare(expression):
                        adding_together[expression] = ADD(adding_together[expression], CONST(1))
                        added = True
                if not added:
                    adding_together[child] = CONST(1)
                #hier moet dan een 1 komen voor var, check if in dic, anders-> en dat toevoegen aan dic
        
        



    # if isinstance(child, ADD):
    #             for grandchild in child.children:
    #                 other_factors = self.children[:i] + self.children[i+1:] #everything except the expansion term
    #                 expanded = MUL(*(other_factors + [grandchild]))
    #                 expansion.append(expanded)
    #             self.__class__ = ADD
    #             self.children = expansion
    #             break
                 #if there is a constant, check of in dic, anders: voeg rest toe aan dic -> rest:const
#alle (ietsjes) in een list zetten, en met dubbele forloop kijken welke allemaal hetzelfde zijn?

            
        new_children = []
        if len(adding_together) != 1:
            for expression, constant in adding_together.items():
                if isinstance(constant, CONST):
                    if constant.value == 1:
                        new_children.append(expression)
                else:
                    new_children.append(MUL(constant, expression))
            self.__class__ = ADD
            self.children = new_children
        else:
            for expression, constant in adding_together.items():
                #constant.simplify() of constant.add()
                new_children.append(constant)
                new_children.append(expression)
            self.__class__ = MUL
            self.children = new_children

        

                        
               