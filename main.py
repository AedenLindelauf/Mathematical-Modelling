from verify_expression import *
from tree import Tree
from shunting_yard import *

if __name__ == "__main__":
    # Right now it doesn't work because of circular imports.
    expr = "1^(2 * 1)"
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
        post_fixer = Post_Fixer(standardized_expr)
        test_tree = create_tree(post_fixer.postfix_notation)
        print("Tree before differentiation: ", test_tree)
        differentiated_tree = test_tree.differentiate()
        print("Tree after differentiation, before conversion: ", differentiated_tree)
        # Convert to common-operator-based structure
        differentiated_tree.convert_to_common_operator_structure()
        # Simplify
        differentiated_tree.simplify()

        print(f"Output:\t {differentiated_tree}")
        

