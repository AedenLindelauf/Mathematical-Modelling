from operands.fluid import FLUID

class ADD(FLUID):
    def __str__(self):
        return " + ".join( [child.__str__() for child in self.children] )
    
    def compare(tree1, tree2):
        if tree1.__class__ != tree2.__class__: 
            return False
        # alles in een list zetten, en dan kijken of het in die andere list zit, zo ja, haal dat eruit. Als empty list overblijft dan is het gelijk. 
        # een manier om 'injectivity' te checken. Dit werkt, alleen is computation time aanvaardbaar?
        # een snellere methode zou Hashen zijn, dan kan je sorten, maar dat is best complex
        tree1children = tree1.children
        tree2children = tree2.children
        print(tree1children, tree2children)
        for child1 in tree1children:
            print(tree2children)
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
        
        # If the child has children, simplify the children
        for child in self.children:
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


