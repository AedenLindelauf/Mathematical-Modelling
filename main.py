from tree import Tree
from expression import *

if __name__ == "__main__":
    e = Expression("(x+1)/2")
    test_tree = e.tree

    e = MUL(CONST(1), CONST(2))
    print(e.latex())

    print(f"Input:\t {test_tree}")
    test_tree.simplify()
    print(f"Output:\t {test_tree}")