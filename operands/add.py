from operands.fluid import FLUID

class ADD(FLUID):
    def __str__(self):
        return " + ".join( [child.__str__() for child in self.children] )

    def simplify(self):
        from operands.node import NODE
        from operands.const import CONST
        
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
