from tree import Tree
from expression import *
import verification

if __name__ == "__main__":
    e = Expression("(x+1)/2")
    test_tree = e.tree
    
    


    # expr = "( a * b * c ) ^ d"
    # expr = "a ^ (b ^ (c ^ d))"
    # expr = "3(a+3)"
    # expr = "a*a"
    # expr = "1*2 + 0*x"
    # expr = "1+2"
    # expr = "a(x + 1)"
    # expr = "x + 1 + 2x" 
    # expr = "3x^2 - 3x^2" 
    # expr = "x^2 + 1 + 2*x^2"
    # expr = "ab^2 + 2ab + 2*x^2 + 3*x^2 + x^5 + 2ab + 5 * ab^2"
    # expr = "(a+b)^2 + 2*((a+b)^2)"
    #expr = "0*a"
    #en 3(a+b)-3a-3b werkt nog niet, soort van wel maar hij doet de -variant niet weg.

    print(f"Input:\t {test_tree}")
    test_tree.simplify()
    print(f"Simplified:\t {test_tree}")