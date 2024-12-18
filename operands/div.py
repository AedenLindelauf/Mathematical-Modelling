from operands.binary import BINARY

class DIV(BINARY):
    def __str__(self): return f"( {super().__str__('/')} )"

    def compare(tree1, tree2):
        if tree1.__class__ != tree2.__class__: 
            return False
        
        if ( tree1.children[0].compare(tree2.children[0]) ) and ( tree1.children[1].compare(tree2.children[1]) ):
            return True
        return False
        
        #zou heel kort kunnen met: return ( tree1.children[0].compare(tree1.children[0]) ) and ( tree1.children[1].compare(tree1.children[1]) )

    #simplification of fractions

    def simplify(self):
        from operands.mul import MUL
        from operands.const import CONST

        self.children[0].simplify()
        self.children[1].simplify()

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

        # Check whether division by 0.
        if isinstance(self.children[1], CONST) and (self.children[1].value == 0) : raise ZeroDivisionError()
