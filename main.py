from verify_expression import *
from tree import Tree
from node import *
from shunting_yard import *

if __name__ == "__main__":
    
    # post_fixer_1 = Post_Fixer("2 ^ ( 2 + x ^ 2 * y )")
    # test_tree = create_tree(post_fixer_1.postfix_notation)
    # print(test_tree)

    expr = "3 * xyzabc5def / 4"

    converter = SymbolicFunctionConverter()
    # Validate the function
    is_valid, message = converter.validate_function(expr)
    if not is_valid:
        print(f"Input:\t {expr}\n{message}")
    else:
        # Standardize the function
        standardized_expr = converter.standardize_function(expr)
        print(f"Input:\t {expr}\nCorrected input:", standardized_expr)

        # Convert to tree
        post_fixer_2 = Post_Fixer(standardized_expr)
        test_tree = create_tree(post_fixer_2.postfix_notation)
        # Simplify
        test_tree.simplify()
        print(f"Output:\t {test_tree}")