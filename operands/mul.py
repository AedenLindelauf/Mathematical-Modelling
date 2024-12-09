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
    
    #recursie: check of alle childeren hetzelfde zijn
    #base case maken wanner je bij leaveas bent gekomen

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

        
        # a^b * a^c = a^(b+c)
        base_exponent = {}
        new_children_exponent = []
        for child in self.children:

            if isinstance(child, POW):
                base = child.children[0]
                exponent = child.children[1]

                #Equals method maken, die checkt of twee trees (dat een object is, hier base) hetzelfde zijn?
                #Alles eronder in soort set zetten die dat dan op zou kunnen slaan?
                if base.value in base_exponent:
                    base_exponent[base.value] = (base, ADD(base_exponent[base.value][1], exponent))
                else:
                    base_exponent[base.value] = (base, exponent)

            elif isinstance(child, VAR):
                base = child
                exponent = 1
                if base.value in base_exponent:
                    base_exponent[base.value] = (base, ADD(base_exponent[base.value][1], exponent))
                else:
                    base_exponent[base.value] = (base, exponent)

            else:
                new_children_exponent.append(child)

        for x, tuppel in base_exponent.items(): new_children_exponent.append(POW(tuppel[1], tuppel[0]))

        self.__class__ = MUL
        self.children = new_children_exponent
        #wat als het maar 1 power wordt? if len(new_child..) == 1: leaf maken, anders deze optie?

        #end of adding powers


        #a * (b + c)
        for i, child in enumerate(self.children):
            if isinstance(child, ADD):
                expension = []
                for grandchild in child.children:
                    expension.append(MUL(self.children[1 - i], grandchild))
                self.__class__ = ADD
                self.children = expension
                break
                
        
