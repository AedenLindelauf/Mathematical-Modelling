def is_function(token : str) -> bool:
    return False

def is_operator(token : str) -> bool:
    return token in ("^", "*", "/", "+", "-")



class Expression:
    """
    A mathematical expression
    """
    OPERATOR_PRECEDENCES : dict[str, int] = {"^" : 4, "*" : 3, "/" : 3, "+" : 2, "-" : 2}
    OPERATOR_ASSOCIATIVITY : dict[str, int] = {"^" : "Right", "*" : "Left", "/" : "Left", "+" : "Left", "-" : "Left"}

    def __init__(self, infix_notation : str | None = None, postfix_notation : str | None = None, auto_simplify : bool = False):
        self.infix_notation : str = infix_notation if infix_notation else "0"
        self.write_postfix_notation(self.infix_notation)
        
        if postfix_notation:
            assert postfix_notation == self.postfix_notation, "Infix and Postfix notations are for different expressions"
        
        if auto_simplify:
            self.simplify()
        

    def write_postfix_notation(self, expression_infix_notation : str, verbose : bool = False) -> None:
        """
        Uses the shunting yard algorithm to write the postfix notation for the expression
        """
        self.postfix_notation : str = ""
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

            elif token.isdigit():
                self.postfix_notation += f"{token} "
            
            else:
                raise Exception(f"{token} not implemented")

            if verbose: print(self.postfix_notation, self.operator_stack)
        self.postfix_notation += " ".join(self.operator_stack[::-1])
    
    def pop_operators_inside_parenthesis(self) -> None:
        assert "(" in self.operator_stack, "Mismatched parenthesis"

        while True:
            top_operator = self.operator_stack.pop()
            if top_operator == "(":
                break
            self.postfix_notation += f"{top_operator} "
            

    def add_to_operator_stack(self, added_operator : str) -> None:
        while True:
            if not self.operator_stack:
                break

            precendence_added_operator : int = self.OPERATOR_PRECEDENCES[added_operator]
            top_operator = self.operator_stack[-1]
            if top_operator == "(":
                break

            precendence_top_operator : int = self.OPERATOR_PRECEDENCES[top_operator]

            if precendence_top_operator < precendence_added_operator:
                break

            associativity_top_operator : str = self.OPERATOR_ASSOCIATIVITY[top_operator]       
            top_operator_is_left_associative : bool = associativity_top_operator == "Left"
            if precendence_top_operator > precendence_added_operator or top_operator_is_left_associative:
                self.postfix_notation += f"{top_operator} "
                self.operator_stack.pop()
                continue
            
        self.operator_stack.append(added_operator)

    def simplify(self, verbose = False) -> None:
        token_stack = []
        for token in self.postfix_notation.split():
            if verbose: print(token, token_stack)
            if is_operator(token):
                right_hand_side = token_stack.pop()
                left_hand_side = token_stack.pop()
                token_stack.append(do_operation(token, left_hand_side, right_hand_side))
                continue
            token_stack.append(token)
        self.infix_notation = " ".join(token_stack)
    
    def __repr__(self) -> str:
        return self.infix_notation


def do_operation(operator : str, left_hand_side : str, right_hand_side : str) -> str:
    if left_hand_side.isdigit() and right_hand_side.isdigit():
        return do_operation_on_ints(operator, int(left_hand_side), int(right_hand_side))
    
    at_least_1_is_a_fraction = is_fraction(left_hand_side) or is_fraction(right_hand_side)
    if at_least_1_is_a_fraction:
        return do_operation_on_fractions(operator, left_hand_side, right_hand_side)

    return f"{left_hand_side}{operator}{right_hand_side}"


def do_operation_on_ints(operator : str, left_hand_side : int, right_hand_side : int) -> str:
    match operator:
        case "+":
            result_int = left_hand_side + right_hand_side
            return f"{result_int}"
        case "-":
            result_int = left_hand_side - right_hand_side
            return f"{result_int}"
        case "*":
            result_int = left_hand_side * right_hand_side
            return f"{result_int}"
        case "/":
            fraction = f"{left_hand_side}{operator}{right_hand_side}"
            return simplify_fraction(fraction)
        case _:
            return f"{left_hand_side}{operator}{right_hand_side}"


def do_operation_on_fractions(operator : str, left_hand_side : str, right_hand_side : str) -> str:
    numerator_left_hand_side, denominator_left_hand_side = left_hand_side.split("/") if is_fraction(left_hand_side) else (left_hand_side, 1)
    numerator_right_hand_side, denominator_right_hand_side = right_hand_side.split("/") if is_fraction(right_hand_side) else (right_hand_side, 1)
    match operator:
        case "+":
            numerator = Expression(f"{numerator_left_hand_side} * {denominator_right_hand_side} + {numerator_right_hand_side} * {denominator_left_hand_side}")
            numerator.simplify()
            denominator = Expression(f"{denominator_left_hand_side} * {denominator_right_hand_side}")
            denominator.simplify()
        case "-":
            numerator = Expression(f"{numerator_left_hand_side} * {denominator_right_hand_side} - {numerator_right_hand_side} * {denominator_left_hand_side}")
            numerator.simplify()
            denominator = Expression(f"{denominator_left_hand_side} * {denominator_right_hand_side}")
            denominator.simplify()
        case "*":
            numerator = Expression(f"{numerator_left_hand_side} * {numerator_right_hand_side}")
            numerator.simplify()
            denominator = Expression(f"{denominator_left_hand_side} * {denominator_right_hand_side}")
            denominator.simplify()
        case "/":
            numerator = Expression(f"{numerator_left_hand_side} * {denominator_right_hand_side}")
            numerator.simplify()
            denominator = Expression(f"{denominator_left_hand_side} * {numerator_right_hand_side}")
            denominator.simplify()
        case _:
            return f"{left_hand_side}{operator}{right_hand_side}"
        
    fraction = f"{numerator}/{denominator}"
    return simplify_fraction(fraction)

def simplify_fraction(fraction : str) -> str:
    assert is_fraction(fraction), f"{fraction} is not a fraction."
    numerator, denominator = fraction.split("/")
    if numerator.isdigit() and denominator.isdigit():
        numerator_int, denominator_int = int(numerator), int(denominator)
        greatest_common_divisor = calculate_greatest_common_divisor(numerator_int, denominator_int)
        
        reduced_numerator = numerator_int // greatest_common_divisor
        
        reduced_denominator = denominator_int // greatest_common_divisor
        return f"{reduced_numerator}/{reduced_denominator}" if reduced_denominator != 1 else f"{reduced_numerator}"

def is_fraction(token : str) -> bool:
    if "/" not in token:
        return False
    if len(token.split("/")) != 2:
        return False
    return True

def calculate_greatest_common_divisor(a : int, b : int) -> int:
    bigger_value = max(a, b)
    smaller_value = min(a, b)
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

            
e = Expression()
print(e.postfix_notation)
e.simplify()
print(e)

e2 = Expression("( 2 - 2 ) * 3")
print(e2.postfix_notation)
