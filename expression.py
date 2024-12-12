from verification import *
from node import *
from tree import Tree

class Expression:
    OPERATOR_PRECEDENCES    : dict[str, int]    = {"^" : 4, "*" : 3, "/" : 3, "+" : 2, "-" : 2}
    OPERATOR_ASSOCIATIVITY  : dict[str, int]    = {"^" : "Right", "*" : "Left", "/" : "Left", "+" : "Left", "-" : "Left"}
    OPERATOR_NODES          : dict[str, NODE]   = {"+" : ADD, "-" : SUB, "*" : MUL, "/" : DIV, "^" : POW}

    def __init__(self, infix_expression : str):
        self.infix_expression = infix_expression.replace(" ","")

        if is_valid_expression(self.infix_expression):
            self.tokenize()
            self.create_tree()

    def create_tree(self):
        self.operator_stack : list[str]     = []
        self.node_stack     : list[NODE]    = []
        for self.token in self.tokenized_expression:
            if is_numerical_value(self.token):
                self._create_numerical_node()

            elif is_operator(self.token):
                self._add_operator_to_stack()
            
            elif is_variable(self.token):
                self.node_stack.append(VAR(self.token))
            
            elif is_function(self.token):
                raise NotImplementedError("Functions are not implemented yet!")
            
            elif self.token == "(":
                self.operator_stack.append(self.token)

            elif self.token == ")":
                self._pop_operators_in_parentheses()
        
        while self.operator_stack:
            added_operator = self.operator_stack.pop()
            self._add_operator_to_node_stack(added_operator)
        
        self.tree = self.node_stack[0]
    
    def _pop_operators_in_parentheses(self) -> None:
        
        while True:
            top_operator = self.operator_stack.pop()
            if top_operator == "(":
                break
            self._add_operator_to_node_stack(top_operator)

        
    def _create_numerical_node(self) -> None:
        if "." not in self.token:
            int_token = int(self.token)
            self.node_stack.append(CONST(int_token))
            return

        fraction_start = self.token.index(".")
        fractional_part = self.token[fraction_start+1:]

        if int(fractional_part) == 0:
            integer_part = int(self.token[:fraction_start])
            self.node_stack.append(CONST(integer_part))
            return

        initial_numerator = int(self.token.replace(".", ""))
        initial_denominator = 10 ** len(fractional_part)
        
        greatest_common_divisor = calculate_greatest_common_divisor(initial_denominator, initial_numerator)
        final_numerator = initial_numerator // greatest_common_divisor
        final_denominator = initial_denominator // greatest_common_divisor
        final_numerator = initial_numerator // greatest_common_divisor
        final_denominator = initial_denominator // greatest_common_divisor
        division_node = DIV()
        division_node.left = CONST(final_numerator)
        division_node.right = CONST(final_denominator)
        self.node_stack.append(division_node)

    def _add_operator_to_node_stack(self, operator : str) -> None:
        right_hand_side = self.node_stack.pop()
        left_hand_side = self.node_stack.pop()
        operator_node = self.OPERATOR_NODES[operator]()
        operator_node.left = left_hand_side
        operator_node.right = right_hand_side
        self.node_stack.append(operator_node)

    def _add_operator_to_stack(self):
        while True:
            if not self.operator_stack:
                break

            top_operator : str = self.operator_stack[-1]

            if top_operator == "(":
                break
            
            precendence_added_operator : int = self.OPERATOR_PRECEDENCES[self.token]
            precendence_top_operator : int = self.OPERATOR_PRECEDENCES[top_operator]

            if precendence_top_operator < precendence_added_operator:
                break

            associativity_top_operator : str = self.OPERATOR_ASSOCIATIVITY[top_operator]       
            top_operator_is_left_associative : bool = associativity_top_operator == "Left"

            if precendence_top_operator > precendence_added_operator or top_operator_is_left_associative:
                added_operator = self.operator_stack.pop()
                self._add_operator_to_node_stack(added_operator)

                

        self.operator_stack.append(self.token)
        
        
    def tokenize(self) -> None:
        self.minus_counter          : int       = 0
        self.tokenized_expression   : list[str] = []
        self.letter_stack           : list[str] = []
        self.number_stack           : list[str] = []
        shifted_expression          : list[str] = self.infix_expression[1:] + " "
        self.minus_is_unary         : bool      = True

        for self.symbol, self.next_symbol in zip(self.infix_expression, shifted_expression):
            if self.symbol.isspace():
                continue

            elif is_letter(self.symbol):
                self.handle_letter()

            elif is_operator(self.symbol):
                self.handle_operator()

            elif is_numerical_part(self.symbol):
                self.handle_numerical_part()

            else:
                self.add_tokens(self.symbol)

            
            if self.next_symbol == "-":
                self.determine_minus_nature()
            
            elif not is_operator(self.symbol) and self.symbol != "(" and (is_letter(self.next_symbol) or self.next_symbol == "("):
                self.add_tokens("*")
                


    def handle_numerical_part(self):
        self.number_stack.append(self.symbol)

        if is_numerical_part(self.next_symbol):
            return
        
        added_tokens : list[str] = ["".join(self.number_stack)]


        self.add_tokens(added_tokens)
        self.number_stack = []

    
    def add_tokens(self, tokens : str | list[str]) -> None:
        added_tokens : list[str] = list(tokens)

        self.minus_is_unary = False

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
    bigger_value    : int = max(a, b)
    smaller_value   : int = min(a, b)
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
    e = Expression("(1)")
    print(e.tree)