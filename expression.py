from verification import *
from operands.add import ADD
from operands.sub import SUB
from operands.mul import MUL
from operands.div import DIV
from operands.node import NODE
from operands.pow import POW
from operands.var import VAR
from operands.const import CONST
from tree import Tree

class Expression:
    """
    Class that constructs a binary tree based on a mathematical expression in infix notation. Get tree with the .tree atribute.
    """
    OPERATOR_PRECEDENCES    : dict[str, int]    = {"^" : 4, "*" : 3, "/" : 3, "+" : 2, "-" : 2}
    OPERATOR_ASSOCIATIVITY  : dict[str, int]    = {"^" : "Right", "*" : "Left", "/" : "Left", "+" : "Left", "-" : "Left"}
    OPERATOR_NODES          : dict[str, NODE]   = {"+" : ADD, "-" : SUB, "*" : MUL, "/" : DIV, "^" : POW}

    def __init__(self, infix_expression : str):
        self.infix_expression = infix_expression.replace(" ","")

        if is_valid_expression(self.infix_expression):
            self.tokenize()
            self.create_tree()

    def create_tree(self):
        """
        Creates the binary tree by looping over the tokens in the tokenized version of the infix expression. Based on the shunting yard algorithm.
        """
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
        
        self.tree = Tree(self.node_stack[0])
    
    def _pop_operators_in_parentheses(self) -> None:
        """
        Two matching paretheses have been found so the operations in between these brackets are added to the node stack.
        """
        
        while True:
            top_operator = self.operator_stack.pop()
            if top_operator == "(":
                break
            self._add_operator_to_node_stack(top_operator)

        
    def _create_numerical_node(self) -> None:
        """
        The current token being considered is a numerical value. If the token is an integer (also when everything after the decimal point is zero) a constant node is added to the node stack, else if 
        the number is a float value it is stored in a division node (1.2 -> DIV(left = 6, right = 5)).
        """
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
        division_node = DIV(CONST(final_numerator), 
                            CONST(final_denominator))
        self.node_stack.append(division_node)

    def _add_operator_to_node_stack(self, operator : str) -> None:
        """
        The operator that is put in is added to the node stack with current right most node as its right child and the one before that as its left child, these are both popped from the node stack in 
        the process.
        """
        right_hand_side = self.node_stack.pop()
        left_hand_side = self.node_stack.pop()
        operator_node = self.OPERATOR_NODES[operator](left_hand_side, right_hand_side)
        self.node_stack.append(operator_node)

    def _add_operator_to_stack(self):
        """
        The current token considered is an operator if there are operators in the stack that take precedence over the added operator they are added to the node stack.
        """
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
        """
        creates a tokenized version of the infix expression.

        Examples:
        self.infix_expression = "x+1" -> self.tokenized_expression = ["x", "+", "1"]
        self.infix_expression ="xyz/-x" -> self.tokenized_expression = ['x', '*', 'y', '*', 'z', '/', '(', '-1', '*', 'x', ')']
        """
        self.unary_minus_counter          : int       = 0
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
            
            elif not is_operator(self.symbol) and self.symbol != "(" and not is_letter(self.symbol) and (is_letter(self.next_symbol) or self.next_symbol == "("): # Long bool might fix later
                self.add_tokens("*")
            


    def handle_numerical_part(self):
        """
        The current symbol considered in making the tokenized expression is part of a numerical value. If it is the last part of this numerical value it is added to the tokenized expression.
        """
        self.number_stack.append(self.symbol)

        if is_numerical_part(self.next_symbol):
            return
        
        added_tokens : list[str] = ["".join(self.number_stack)]


        self.add_tokens(added_tokens)
        self.number_stack = []

    
    def add_tokens(self, tokens : str | list[str]) -> None:
        """
        Add the tokens put in to the tokenized expression. If there were n unary minuses before it n "-1", "*" are added before the new token. 
        """
        added_tokens : list[str] = list(tokens)

        self.minus_is_unary = False # Not necessarily true, but if there is a unary minus it will be changed to true again  

        if self.unary_minus_counter:
            added_tokens = ["("]
            added_tokens.extend(["-1","*"] * self.unary_minus_counter)
            added_tokens.extend(tokens)
            added_tokens.extend([")"] * self.unary_minus_counter)
            self.unary_minus_counter = 0

        self.tokenized_expression.extend(added_tokens)
    

    def handle_operator(self) -> None:
        """
        The current symbol considered in making the tokenized expression is an operator. If it is not a unary minus sign it is just added to the tokenized expression. Otherwise, it is counted as an unary
        minus which will be handled when the next token is added.
        """
        if not self.minus_is_unary:
            self.add_tokens(self.symbol)
        
        elif self.symbol == "-":
            self.unary_minus_counter += 1

    
    def determine_minus_nature(self) -> None:
        """
        The next symbol considered in making the tokenized expresssion is a minus sign. This determines if it is unary or binary. 
        """
        if is_operator(self.symbol) or self.symbol == "(":
            self.minus_is_unary = True
        
        else:
            self.minus_is_unary = False

    
    def handle_letter(self) -> None:
        """
        The current symbol considered in making the tokenized expression is a letter. If it is the next symbol is not a letter the stack of letters is added to the tokenized expression accordingly.
        """
        self.letter_stack.append(self.symbol)

        if not is_letter(self.next_symbol):
            self.add_letter_stack()

    def add_letter_stack(self) -> None:
        """
        The letters in the letter stack are added to the tokenized expression. If it is regocnized as function it is added as a whole. Otherwise, the letters are added seperatly with "*" in between them.
        """
        possible_function = "".join(self.letter_stack)

        if is_function(possible_function):
            self.add_tokens(possible_function)
        
        else:
            added_tokens = list("*".join(self.letter_stack))
            self.add_tokens(added_tokens)

        self.letter_stack = []
        



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
    e = Expression("xyz/-x")
    print(e.tokenized_expression)