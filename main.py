from tree import Tree
from expression import *
from longdivision import *
from copy import deepcopy

if __name__ == "__main__":
    e = Expression("(x^10 - 1) / (x+y)") 
    test_tree = e.tree
    
    print("Input:", test_tree.root)
    #test_tree.simplify()
    test_tree.convert_to_common_operator_structure()
    test_tree.root = change_to_lex_order(test_tree.root)
    tester = deepcopy(test_tree.root)
    result = long_division(tester)
    print("Long division result, quotient is", result[0], "remainder is", result[1])
    print(f"Output:\t {test_tree}")