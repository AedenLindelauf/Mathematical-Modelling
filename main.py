from tree import Tree
from node import *
from shunting_yard import *
from GUI import GUI

if __name__ == "__main__":
    
    # post_fixer_1 = Post_Fixer("2 ^ ( 2 + x ^ 2 * y )")
    # test_tree = create_tree(post_fixer_1.postfix_notation)
    # print(test_tree)

    # expr = "( 2 - 1 ) ^ a * ( 0 ^ 5 ) * ( 1 * x + y + 0 ) ^ 2 * 1 * ( ( z / 1 ) ^ 1 )"

    # post_fixer_2 = Post_Fixer(expr)
    # test_tree = create_tree(post_fixer_2.postfix_notation)
    # test_tree.simplify()
    # print(f"Input:\t {expr}\nOutput:\t {test_tree}")

    primary_expr = "( 2 * x + 1 ) / ( x ^ 4 + x ^ 3 )"
    post_fixer_diff_test = Post_Fixer(primary_expr)
    test_tree_diff = create_tree(post_fixer_diff_test.postfix_notation)
    derivative_tree = test_tree_diff.differentiate()
    derivative_tree.simplify()

    test_expr = "( 0 * x )"
    post_fixer_test = Post_Fixer(test_expr)
    test_tree = create_tree(post_fixer_test.postfix_notation)
    test_tree.simplify()
    
    
    
    print(derivative_tree)