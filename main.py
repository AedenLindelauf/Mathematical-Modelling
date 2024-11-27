from tree import Tree
from node import *
from shunting_yard import *

if __name__ == "__main__":
    
    # post_fixer_1 = Post_Fixer("2 ^ ( 2 + x ^ 2 * y )")
    # test_tree = create_tree(post_fixer_1.postfix_notation)
    # print(test_tree)

    expr = "2 * ( x + y ) ^ 2 * 4"

    post_fixer_2 = Post_Fixer(expr)
    test_tree = create_tree(post_fixer_2.postfix_notation)
    test_tree.simplify()
    print(f"Input:\t {expr}\nOutput:\t {test_tree}")