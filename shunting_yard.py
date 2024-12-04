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

    def __init__(self, infix_notation : str | None = None):
        self.infix_notation : str = infix_notation if infix_notation else "0"
        self.write_postfix_notation(self.infix_notation)
        
    def write_postfix_notation(self, expression_infix_notation : str, verbose : bool = False) -> None:
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
    
    def pop_operators_inside_parenthesis(self) -> None:
        assert "(" in self.operator_stack, "Mismatched parenthesis"

        while True:
            top_operator = self.operator_stack.pop()
            if top_operator == "(":
                break
            self.postfix_notation.append(top_operator)
            

    def add_to_operator_stack(self, added_operator : str) -> None:
        while True:
            if not self.operator_stack:
                break

            
            top_operator = self.operator_stack[-1]
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
            operator_node = OPERATOR_NODES[token](node_stack.pop(), node_stack.pop()) # Need to feed the children into the initialization
            node_stack.append(operator_node)

        if token.isdigit():
            int_token = int(token)
            node_stack.append(CONST(int_token))
        
        if token.isalpha():
            node_stack.append(VAR(token))
        
    return Tree(node_stack[0])
