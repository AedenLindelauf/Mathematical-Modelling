from tree import Tree
from node import *

def is_function(token : str) -> bool:
    return False

def is_operator(token : str) -> bool:
    return token in ("^", "*", "/", "+", "-")



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

            elif symbol.isdigit() or symbol == ".":
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
         
    def create_tree_directly(self, infix_notation : str) -> Tree:
        """
        Directly creates a tree from the infix notation given.
        """
        self.node_stack : list[NODE] = []
        self.operator_stack : list[str] = []
        current_number_token : list[str] = []

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

        if token.isdigit():
            int_token = int(token)
            node_stack.append(CONST(int_token))
        
        if token.isalpha():
            node_stack.append(VAR(token))
        
    return Tree(node_stack[0])


        