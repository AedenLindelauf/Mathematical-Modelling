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

    def simplify(self):
        # If the child has children, simplify the children
        for child in self.children:
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

            if not isinstance(child, POW):
                base = child
                exponent = 1
                added = False
                for bases in base_exponent:
                    if base.compare(bases):
                        base_exponent[base.value] = (base, ADD(base_exponent[base.value][1], exponent))
# .simplify toevoegen hier?
                        added = True
                        break
                if not added:
                    base_exponent[base.value] = (base, exponent)

            #wat als je gw alleen(a+b) hebt, zonder macht, of constant? deze hierboven veranderen naar general case? is er uberhaupt een else case? ja wnr er niet 2 dingen hetzelfde zijn. maar dat kan ook hierboven
            else:
                base = child.children[0]
                exponent = child.children[1]
                added = False
                #het adden gaat fout, want je kan base_exponent[base] niet opzoeken
                for bases in base_exponent:
                    if base.compare(bases):
                        base_exponent[base] = (base, ADD(base_exponent[base][1], exponent))
# .simplify toevoegen hier?
                        added = True
                        break
                if not added:
                    base_exponent[base] = (base, exponent)



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
                
        
