import re

class SymbolicFunctionConverter:
    def __init__(self):
        # Regular expression for valid symbols (variables, numbers, operators, and parentheses)
        self.valid_characters = re.compile(r"^[a-zA-Z0-9+\-*/^() ]+$")
        # Regular expression to match numbers or valid variable names (e.g., "x", "y")
        self.operand_pattern = re.compile(r"[a-zA-Z0-9]+")


    def validate_function(self, func):
        # Pattern for valid characters (letters, numbers, +, -, *, /, ^, (, ), and spaces)
        valid_characters = re.compile(r'^[a-zA-Z0-9\+\-\*/\^()\s]*$')
        func = func.replace(" ", "")

        # Check for invalid characters
        if not valid_characters.match(func):
            return False, "Invalid: The function contains invalid characters. Only letters, numbers, +, -, *, /, ^, (, and ) are allowed."
        
        # Check if the function starts or ends with an invalid character (operator or empty spot)
        if func[0] in "+*/^" or func[-1] in "+-*/^":
            return False, "Invalid: function cannot start or end with an operator."
        
        # Check for invalid combinations of consecutive operators or invalid placement of operators
        consecutive_operator_pattern = re.compile(r'[+\*/\^]{2,}')
        if consecutive_operator_pattern.search(func):
            return False, "Invalid: function cannot contain consecutive operators."

        # Check for operator immediately before a closing parenthesis or after an opening parenthesis
        if re.search(r'[\+\-\*/\^]\)', func):  # Operator before a closing parenthesis
            return False, "Invalid: An operator cannot be placed before a closing parenthesis."
        if re.search(r'\([+\-\*/\^]', func):  # Operator after an opening parenthesis
            return False, "Invalid: An operator cannot be placed immediately after an opening parenthesis."

        if re.search(r'-[\+\*\/\^]+', func):  
            return False, "Invalid: Invalid negative sign placement (e.g., -^, -*, -/ are not allowed)."

        # Check for correct parentheses
        stack = []
        for char in func:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False, "Invalid: Unmatched closing parenthesis."
                stack.pop()
        
        # Check if there are unmatched opening parentheses left in the stack
        if stack:
            return False, "Invalid: Unmatched opening parenthesis."
        
        return True, "Valid function."


    def standardize_function(self, func):
        """Converts the symbolic function to a standard form."""
        # Remove spaces
        func = func.replace(" ", "")
        
        # Add explicit multiplication for cases like "3x" -> "3*x" or "2(x+1)" -> "2*(x+1)"
        func = re.sub(r"([\da-zA-Z)])([a-zA-Z(])", r"\1*\2", func)
        func = re.sub(r"([a-zA-Z)])([\da-zA-Z(])", r"\1*\2", func)
        
        # Normalize parentheses spacing and operator spacing
        func = re.sub(r"(?<!\s)([\+\-\*/\^()])", r" \1", func)  # Space before operators
        func = re.sub(r"([\+\-\*/\^()])(?!\s)", r"\1 ", func)   # Space after operators

        # Remove double spaces
        func = re.sub(r"\s+", " ", func).strip()
        
        return func



# if __name__ == "__main__":
    
#     # post_fixer_1 = Post_Fixer("2 ^ ( 2 + x ^ 2 * y )")
#     # test_tree = create_tree(post_fixer_1.postfix_notation)
#     # print(test_tree)

#     expr = "( 2 - 1 ) ^ a * ( 0 ^ 5 )( 3x + y + 0 ) ^ 2 * 1 * ( ( z / 1 ) + 1 )"

#     converter = SymbolicFunctionConverter()
#     # Validate the function
#     is_valid, message = converter.validate_function(expr)
#     if not is_valid:
#         print(f"Input:\t {expr}\n{message}")
#     else:
#         # Standardize the function
#         standardized_expr = converter.standardize_function(expr)
#         print(f"Input:\t {expr}\nCorrected input:", standardized_expr)

#         # Convert to tree
#         post_fixer_2 = Post_Fixer(standardized_expr)
#         test_tree = create_tree(post_fixer_2.postfix_notation)
#         # Simplify
#         test_tree.simplify()
#         print(f"Output:\t {test_tree}")