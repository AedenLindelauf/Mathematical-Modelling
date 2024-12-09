from tree import Tree
from node import *
from verification import *

class Post_Fixer:
    """
    Can create the postfix notation of a mathematical expression.
    """
    OPERATOR_PRECEDENCES : dict[str, int] = {"^" : 4, "*" : 3, "/" : 3, "+" : 2, "-" : 2}
    OPERATOR_ASSOCIATIVITY : dict[str, int] = {"^" : "Right", "*" : "Left", "/" : "Left", "+" : "Left", "-" : "Left"}

    def __init__(self, infix_notation : str | None = None, verbose  : bool = False):
        self.infix_notation : str = infix_notation if infix_notation else "0"
        self.write_postfix_notation(self.infix_notation, verbose)

    
    def write_postfix_notation_old(self, expression_infix_notation : str, verbose : bool = False) -> None:
        """
        Uses the shunting yard algorithm to write the postfix notation for the expression
        """
        self.postfix_notation : list[str] = []
        self.operator_stack : list[str] = []

        for token in expression_infix_notation.split():
            if is_operator(token):
                self.add_to_operator_stack(token)
            elif is_function(token):
                pass
            elif token == "(":
                self.operator_stack.append(token)
            elif token == ")":
                self.pop_operators_inside_parenthesis()

            elif token.isdigit() or token.isalpha():
                self.postfix_notation.append(token)
        
            else:
                raise Exception(f"{token} not implemented")

            if verbose: print(self.postfix_notation, self.operator_stack)
        self.postfix_notation.extend(self.operator_stack[::-1])

    def too_many_operators(self) -> bool: #could use a better name
        token_count = len(self.operator_stack) + len(self.postfix_notation) - self.operator_stack.count("(")
        result : bool = 2 * self.operator_count > token_count - 1
        return result

    def write_postfix_notation(self, expression_infix_notation : str, verbose : bool = False) -> None: #make it so it can make a tree directly
        """
        Uses the shunting yard algorithm to write the postfix notation for the expression
        """
        self.postfix_notation : list[str] = []
        self.operator_stack : list[str] = []
        current_number_token : list[str] = []
        
        self.operator_count : int = 0

        for symbol in expression_infix_notation:
            #check if it is possible to clean the if statements
            if symbol.isspace():
                continue

            elif symbol.isdigit() or symbol == ".": # accepts to many points
                current_number_token.append(symbol)
                continue

            if current_number_token:
                self.postfix_notation.append(''.join(current_number_token))
                current_number_token = []
            
            if symbol == "-" and self.too_many_operators():
                self.postfix_notation.append("-1")
                self.add_to_operator_stack("*")

            elif is_operator(symbol):
                self.add_to_operator_stack(symbol)
                
            elif is_function(symbol):
                pass

            elif symbol == "(":
                self.open_parenthesis()
                
            elif symbol == ")":
                self.pop_operators_inside_parenthesis()

            elif symbol.isalpha():
                implied_multiplication_possible : bool = not self.too_many_operators()
                self.add_variable(symbol, implied_multiplication_possible)

            else:
                raise Exception(f"{symbol} not implemented")
            
            if verbose:
                print(f"{self.postfix_notation=}, {self.operator_stack=}")
                

        if current_number_token:
            self.postfix_notation.append(''.join(current_number_token))

        self.postfix_notation.extend(self.operator_stack[::-1])
    
    def open_parenthesis(self) -> None:
        if not self.too_many_operators():
            self.add_to_operator_stack("*")
        self.operator_stack.append("(")
         
    def create_tree_directly(self, infix_tokens : list[str]) -> Tree:
        """
        Directly creates a tree from the infix notation given.
        """
        self.node_stack : list[NODE] = []
        self.operator_stack : list[str] = []
        for token in infix_tokens:
            print(token)

    def add_variable(self, variable_name : str, implied_multiplication : bool) -> None:
        if implied_multiplication:
            self.add_to_operator_stack("*")
        self.postfix_notation.append(variable_name)
        
    def pop_operators_inside_parenthesis(self) -> None:
        # assert self.operator_stack[-1] != "(", "Empty parenthesis" has bug with (a)

        while True:
            top_operator = self.operator_stack.pop()
            if top_operator == "(":
                break
            self.postfix_notation.append(top_operator)
        
        
    def add_to_operator_stack(self, added_operator : str) -> None:
        self.operator_count += 1
        while True:
            if not self.operator_stack:
                break

            
            top_operator : str = self.operator_stack[-1]
            if top_operator == "(":
                break
            
            precendence_added_operator : int = self.OPERATOR_PRECEDENCES[added_operator]
            precendence_top_operator : int = self.OPERATOR_PRECEDENCES[top_operator]

            if precendence_top_operator < precendence_added_operator:
                break

            associativity_top_operator : str = self.OPERATOR_ASSOCIATIVITY[top_operator]       
            top_operator_is_left_associative : bool = associativity_top_operator == "Left"
            if precendence_top_operator > precendence_added_operator or top_operator_is_left_associative:
                self.postfix_notation.append(top_operator)
                self.operator_stack.pop()
                continue
            
        self.operator_stack.append(added_operator)

    
    def __repr__(self) -> str:
        return f"{self.postfix_notation}"

def create_tree(post_fix_notation : list[str]) -> Tree:
    OPERATOR_NODES = {"+" : ADD, "-" : SUB, "*" : MUL, "/" : DIV, "^" : POW}
    node_stack : list[NODE] = []

    for token in post_fix_notation:
        if is_operator(token):
            right_hand_side = node_stack.pop()
            left_hand_side = node_stack.pop()
            operator_node = OPERATOR_NODES[token]()
            operator_node.left = left_hand_side
            operator_node.right = right_hand_side
            node_stack.append(operator_node)

        if is_numerical_value(token):
            new_leaf = create_numerical_node(token)
            node_stack.append(new_leaf)
            
        
        if token.isalpha():
            node_stack.append(VAR(token))
        
    return Tree(node_stack[0])

def create_numerical_node(token : str) -> NODE:
    assert is_numerical_value(token), "Wait this is not a number."

    if "." in token:
        fraction_start = token.index(".")
        fractional_part = token[fraction_start+1:]
        initial_numerator = int(float(token) * 10 ** len(fractional_part))
        initial_denominator = 10 ** len(fractional_part)

        initial_denominator = 10 ** len(fractional_part)
        token_value = float(token)
        initial_numerator = int(token_value * initial_denominator)
        
        greatest_common_divisor = calculate_greatest_common_divisor(initial_denominator, initial_numerator)
        final_numerator = initial_numerator // greatest_common_divisor
        final_denominator = initial_denominator // greatest_common_divisor
        final_numerator = initial_numerator // greatest_common_divisor
        final_denominator = initial_denominator // greatest_common_divisor
        division_node = DIV()
        division_node.left = CONST(final_numerator)
        division_node.right = CONST(final_denominator)
        return division_node

    int_token = int(token)
    return CONST(int_token)


class Expression:
    def __init__(self, infix_expression : str):
        self.infix_expression = infix_expression
        self.tokenize()
        self.create_tree()

    def create_tree(self):
        for token in self.tokenized_expression:
            print(token)
        
        
    def tokenize(self) -> None:
        self.minus_counter          : str       = 0
        self.tokenized_expression   : list[str] = []
        self.letter_stack           : list[str] = []
        self.number_stack           : list[str] = []
        shifted_expression          : list[str] = self.infix_expression[1:] + " "
        self.minus_is_unary         : bool      = True

        for self.symbol, self.next_symbol in zip(self.infix_expression, shifted_expression):
            if is_letter(self.symbol):
                self.handle_letter()

            elif is_operator(self.symbol):
                self.handle_operator()

            elif is_numerical_part(self.symbol):
                self.handle_numerical_part()

            else:
                self.add_tokens(self.symbol)

            if self.next_symbol == "-":
                self.determine_minus_nature()

    def handle_numerical_part(self):
        self.number_stack.append(self.symbol)

        if is_numerical_part(self.next_symbol):
            return
        
        added_tokens : list[str] = ["".join(self.number_stack)]

        if is_letter(self.next_symbol) or self.next_symbol == "(":
            added_tokens.append("*")

        self.add_tokens(added_tokens)
        self.number_stack = []

    
    def add_tokens(self, tokens : str | list[str]) -> None:
        added_tokens : list[str] = list(tokens)
        if self.minus_counter:
            added_tokens = ["("]
            added_tokens.extend(["-1","*"] * self.minus_counter)
            added_tokens.extend(tokens)
            added_tokens.extend([")"] * self.minus_counter)
            self.minus_counter = 0
        self.tokenized_expression.extend(added_tokens)
    

    def handle_operator(self) -> None:
        if not self.minus_is_unary:
            self.add_tokens(self.symbol)
        
        elif self.symbol == "-":
            self.minus_counter += 1

    
    def determine_minus_nature(self) -> None:
        if is_operator(self.symbol) or self.symbol == "(":
            self.minus_is_unary = True
        
        else:
            self.minus_is_unary = False

    
    def handle_letter(self) -> None:
        self.letter_stack.append(self.symbol)

        if not is_letter(self.next_symbol):
            self.add_letter_stack()

    def add_letter_stack(self) -> None:
        possible_function = "".join(self.letter_stack)

        if is_function(possible_function):
            self.add_tokens(possible_function)
        
        else:
            added_tokens = list("*".join(self.letter_stack))
            self.add_tokens(added_tokens)

        self.letter_stack = []
        
    def tokenize_letter_stack(letter_stack : list[str]) -> list[str]:
        possible_function : str = "".join(letter_stack)
        if is_function(possible_function):
            return [possible_function]
        
        print("*".join(letter_stack))





# wrong place, works only for ints not polynomials
def calculate_greatest_common_divisor(a : int, b : int) -> int:
    bigger_value : int = max(a, b)
    smaller_value : int = min(a, b)
    if a == 0 or b == 0:
        return abs(bigger_value or smaller_value)
    _, remainder = division_with_remainder(bigger_value, smaller_value)
    return calculate_greatest_common_divisor(smaller_value, remainder)

def division_with_remainder(a : int, divider : int) -> tuple[int]:
    quotient = 0
    remainder = abs(a)
    sign_a = 1 if remainder == a else -1
    while remainder >= divider:
        remainder -= divider
        quotient += 1
    return sign_a * quotient, remainder       

if __name__ == "__main__":
    test_expression = Expression("-1.0xyz/-x")
