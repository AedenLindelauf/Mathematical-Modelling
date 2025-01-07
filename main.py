from tree import Tree
from expression import *

if __name__ == "__main__":
    e = Expression("(x+1)/2")
    test_tree = e.tree

    e = MUL(CONST(1), CONST(2))
    print(e.latex())

    
    # expr = "( a * b * c ) ^ d"
    expr = "a*1+a"
    # expr = "2a-2a"
    # expr = "a ^ (b ^ (c ^ d))"
    expr = "3(a+3)"
    # expr = "a*a"
    # expr = "1*2 + 0*x"
    # expr = "1+2"
    # expr = "1-1"
    # expr = "a*(x + 1)"
    # expr = "x + 1 + 2x" 
    # expr = "3x^2 - 3x^2" 
    expr = "x^2 + 1 + 2*x^2"
    expr = "2*x^2"
    # expr = "6^6-a+a+a(c+d)-ac-ad+a*a-a*a"

    # expr = "3(a+3)+5"
    # expr = "(a+b)(c+d)(x+y+z)d"
    # expr = "a*(b+a)^2" 
    # expr="(a+b/c)(b/c+a)"
    # expr = "a*a"
    # expr = "1*2 + 0*x"
    # expr = "1+3+a+ab+ba+a+1"
    # expr = "a(x + 1)"
    # expr = "a*(a+b+c)+a*a"
    # expr = "-(a+b)"
    # expr = "x^2 + x^2"
    # expr = "x+x"
    # expr = "ab+ac+ab"
    # expr = "(abc^2d)^10"
    # expr = "(ab)*(ab)"
    # expr = "(ab^2)^3"
    # expr = "a*(a*b)*b"
    # expr = "16b^4 +a+2*2*4^a*4^a+3*6+a+b*b^3"
    # expr = "a*(a+d)+b"
    # expr = "a*b"
    # expr = "x^2 + 1 + x^2"
    # expr = "ab^2 + 2ab + 2*x^2 + 3*x^2 + x^5 + 2ab + 5 * ab^2"
    # expr = "(a+b)^2 + 1*((a+b)^2)"
    # expr = "0*a"
    # expr = "a+1*1*1*1a+a*1"
    # expr = "-5"
    # expr = "a*4*b/(2^3*2*t+t)+a*b*4/(t+(8+8)*t)"
    # expr = "a-a"
    # expr = "3(a+b)+3a+300b"
    # expr = "3x-3x"
    # expr = "(a+b)^(6/2)"
    # expr = "(b + a ) * ( a + b )* (a+b) "
    # expr = "(b + a )^8 "
    # expr = "2^x *2^(x+1)"
    # expr = "(2*a)*a"
    # expr = "10a-2a"
    # expr = "-a +a"
    expr = "3(a+b)-3a-3b"
    expr = "3x-3x"
    expr = "3(a+b)-3a-3b"
    expr = "a*2a"
    expr = "a * (x/y)"
    expr = "2 * (x/y)"
    expr = "x/y + (2x)/y"
    expr = "a * s * (x/y) * b * (1/b)"
    expr = "a * a"
    expr = "3x-3x"
    expr = "(a+b)^2+(a+b)^2+3*(a+b)^2"
    expr = "(a+b)^1 * (a+b)^-2"
    expr = "a/x +1/x"
    expr = "(a+b)a + (a+b)a"
    # expr = "(a+b)^2 + (a+b)^2"
    expr = "(a+b)(a+b) + (a+b)(a+b)"

    #en 3(a+b)-3a-3b werkt nog niet, soort van wel maar hij doet de -variant niet weg.
    

    e = Expression(expr)
    test_tree = e.tree
    print(f"Input:\t {test_tree}")
    test_tree.simplify()
    print(f"Output:\t {test_tree}")




from tree import Tree
from expression import *
import verification
from longdivision import *
from copy import deepcopy

if __name__ == "__main__":
    #expressions tested
    #x^3/x
    #x^2/x
    #x/x
    #x/2
    #x/y
    #xy/x
    #x^2*y/x
    #x^3*y/x
    #x^3*y^2/x
    #x^5/x^5
    #x^5/x^4
    #x^5/x^3
    #x^5*y^2/x^5
    #x^5*y^2/x^4
    #x^5*y^2/x^3
    #a^100*b^1000*c^10000*x^2*y^2/x^3
    #a*x^5*y^3/a*x^4*y
    #a*x^5*y/x^4*y
    #These should be all the cases


    e = Expression("(x^2 - 1) / (x+1)") 
    test_tree = e.tree
    

    
    print(f"Input:\t {test_tree}")
    #test_tree.simplify()
    test_tree.convert_to_common_operator_structure()
    print(check_expression_for_polynomial_notation(test_tree.root))
    test_tree.root = change_to_lex_order(test_tree.root)
    tester = deepcopy(test_tree.root)
    long_division(tester)
    print("Root at 0 and then 1:", test_tree.root.children[0], test_tree.root.children[1])
    print(monomial_divides_monomial(test_tree.root.children[0], test_tree.root.children[1]), "bruh")
    print(divide_monomials(test_tree.root.children[0], test_tree.root.children[1]))
    print(divide_monomials(test_tree.root.children[0], test_tree.root.children[1]))
    print(f"Output:\t {test_tree}")