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