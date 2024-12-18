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
    # expr = "6^6-a+a+a(c+d)-ac-ad+a*a-a*a"

    # expr = "3(a+3)+5"
    # expr = "(a+b)(c+d)(x+y+z)d"
    # expr = "a*(b+a)^2" 
    # expr="(a+b/c)(b/c+a)"
    # expr = "a*a"
    # expr = "1*2 + 0*x"
    # expr = "1+3+a+ab+ba+a+1"
    # expr = "a(x + 1)"
    # expr = "a(a+b+c)+a*a"
    # expr = "x^2 + x^2"
    # expr = "x+x"
    # expr = "ab+ac+ab"
    # expr = "16b^4 +a+2*2*4^a*4^a+3*6+a+b*b^3"
    # expr = "a*(a+d)+b"
    # expr = "a*b"
    # expr = "x^2 + 1 + x^2"
    # expr = "ab^2 + 2ab + 2*x^2 + 3*x^2 + x^5 + 2ab + 5 * ab^2"
    # expr = "(a+b)^2 + 1*((a+b)^2)"
    # expr = "0*a"
    # expr = "a+1*1*1*1a+a*1"
    # expr = "-5"
    # expr = "a4b/(2^3*2*t+t)+ab4/(t+(8+8)t)"
    # expr = "a-a"
    # expr = "3(a+b)+3a+300b"
    # expr = "3x-3x"
    #nog ideen
    #en 3(a+b)-3a-3b werkt nog niet, soort van wel maar hij doet de -variant niet weg.
    
    print(f"Input:\t {test_tree}")
    test_tree.simplify()
    print(f"Output:\t {test_tree}")