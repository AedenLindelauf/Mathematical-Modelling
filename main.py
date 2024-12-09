from verify_expression import *
from tree import Tree
from shunting_yard import *

if __name__ == "__main__":

    expr = "( a * b * c ) ^ d"
    expr = "a ^ (b ^ (c ^ d))"

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
        # Convert to common-operator-based structure
        test_tree.convert_to_common_operator_structure()
        # Simplify
        test_tree.simplify()
        print(f"Output:\t {test_tree}")