from verify_expression import *
from tree import Tree
from shunting_yard import *

if __name__ == "__main__":

    # expr = "( a * b * c ) ^ d"
    # expr = "a ^ (b ^ (c ^ d))"
    expr = "3(a+3)"
    expr = "a*a"
    #expr = "0*a"
    #In de add zitten echt nog wel fouten! Multiply werkt als het goed is.
    
    #en 3(a+b)-3a-3b werkt nog niet, soort van wel maar hij doet de -variant niet weg.

    converter = SymbolicFunctionConverter()
    # Validate the function
    is_valid, message = converter.validate_function(expr)


    # Bij power of variable moet er nog een case worden gefixt.
        # Ik heb 2 inputs, maar roep het op met variable.compare(variable). Moet 1tje self worden oid?
        #deze laatste is groot ding. Voornamelijk bij welk situaties het gebruikt moet worden.
        # ziet die tree1 als variable voor self?
        #!!!! Je zou simplify in de compare function kunnen gooien?? zodat 2^3 en 8 hetzelfde zouden kunnen worden gezien? anders is dat iig nooit zo
        #!! exp1.__class__ == exp2.__class__   Dit wordt overal gebruikt, maar kan dat ik ook een keer niet true zijn terwijl ze wel gelijk zijn?
        #wat moet ie met(a+b) * (a+b) doen? expanden? of kwadraat optellen bij elkaar?
    #code kan stuk netter, veel if statements

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

        

        # expr_compare1 = "(b + a + (b+a)*(b+a) + a + 2^2)"
        # expr_compare2 = "(a + b + (a+b)*(b+a) + a + 2^f)"
        # # Standardize the function
        # standardized_expr1 = converter.standardize_function(expr_compare1)
        # standardized_expr2 = converter.standardize_function(expr_compare2)
        # print(f"Corrected input 1: {standardized_expr1}\nCorrected input 2:", standardized_expr2)

        # # Convert to tree
        # post_fixer_o = Post_Fixer(standardized_expr1)
        # post_fixer_t = Post_Fixer(standardized_expr2)
        # test_tree_o = create_tree(post_fixer_o.postfix_notation)
        # test_tree_t = create_tree(post_fixer_t.postfix_notation)

        # # Convert to common-operator-based structure
        # test_tree_o.convert_to_common_operator_structure()
        # test_tree_t.convert_to_common_operator_structure()

        
        # result = test_tree_o.root.compare(test_tree_t.root)
        # print(result)
