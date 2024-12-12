class InvalidCharacterError(Exception):
    pass

class OperatorPlacementError(Exception):
    pass

class ParenthesisError(Exception):
    pass

class EmptyError(Exception):
    pass

OPERATORS = {"^", "*", "/", "+", "-"}

temp_letters = []
for letter_order in range(ord("a"), ord("z") + 1):
    lower_case = chr(letter_order)
    upper_case = lower_case.upper()
    temp_letters.extend((lower_case, upper_case))
LETTERS = set(temp_letters)

def is_numerical_part(symbol : str) -> bool:
    if symbol.isdigit():
        return True
    
    if symbol in (".", "-"):
        return True
    
    return False

def is_function(token : str) -> bool:
    return False

def is_letter(symbol : str) -> bool:
    return symbol in LETTERS

def is_variable(token : str) -> bool:
    if is_function(token):
        return False
    
    return not bool(set(token) - set(LETTERS))

def is_numerical_value(token : str) -> bool:
    if "." in {token[0], token[-1]}:
        return False
    
    if token[-1] == "-":
        return False

    for index, symbol in enumerate(token):
        if not is_numerical_part(symbol):
            return False
        
        if index > 0 and symbol == "-":
            return False

    return True

def is_operator(token : str) -> bool:
    return token in OPERATORS

def consists_of_valid_characters(expression : str, raise_error : bool = False) -> bool:
    invalid_characters_used = []
    for symbol in expression:
        if is_letter(symbol):
            continue

        if is_numerical_part(symbol):
            continue

        if is_operator(symbol):
            continue

        if symbol in ("(", ")"):
            continue

        if not raise_error:
            return False
        
        invalid_characters_used.append(symbol)

    if not invalid_characters_used:
        return True
    
    if raise_error:
        message_end = "is not a valid character" if len(invalid_characters_used) == 1 else "are not valid characters"
        raise InvalidCharacterError(f"{", ".join(invalid_characters_used)} {message_end}.")

def starts_with_binary_operator(expression : str, raise_error_if_true : bool = False, raise_error_if_false : bool = False) -> bool:
    assert not (raise_error_if_true and raise_error_if_false), "Like this it will always raise an error."

    binary_operator_at_start = expression[0] in (OPERATORS - {"-"})

    if binary_operator_at_start and raise_error_if_true:
        raise OperatorPlacementError(f"An expression cannot start with the operator {expression[0]}.")
        

    if raise_error_if_false:
        raise OperatorPlacementError(f"For some reason an operator needs to be at the start of the expression.")
    
    return binary_operator_at_start

def ends_with_binary_operator(expression : str, raise_error_if_true : bool = False, raise_error_if_false : bool = False) -> bool:
    assert not (raise_error_if_true and raise_error_if_false), "Like this it will always raise an error."

    binary_operator_at_end = is_operator(expression[-1])

    if binary_operator_at_end and raise_error_if_true:
        raise OperatorPlacementError(f"An expression cannot end with the operator {expression[-1]}.")
        

    if raise_error_if_false:
        raise OperatorPlacementError(f"For some reason an operator needs to be at the end of the expression.")
    
    return binary_operator_at_end   

def has_consecutive_operators(expression : str, raise_error : bool = False) -> bool:
    consecutive_operators : list[str] = []
    shifted_expression : str = expression[1:] + " "

    for symbol, next_symbol in zip(expression, shifted_expression):
        if is_operator(symbol) and next_symbol in (OPERATORS - {"-"}):
            consecutive_operators.append(f"{symbol}{next_symbol}")

    if not consecutive_operators:
        return False
    
    if raise_error:
        raise OperatorPlacementError(f"Cannot have these operators consecutivively [{", ".join(consecutive_operators)}]")

    return True

def has_operator_after_parenthesis(expression : str, raise_error : bool = False):
    parenthesis_operator_combos : list[str] = []
    shifted_expression : str = expression[1:] + " "
    
    for symbol, next_symbol in zip(expression, shifted_expression):
        if symbol == "(" and next_symbol in (OPERATORS - {"-"}):
            parenthesis_operator_combos.append(f"{symbol}{next_symbol}")

    if not parenthesis_operator_combos:
        return False
    
    if raise_error:
        raise OperatorPlacementError(f"Cannot have these operators right after a opening parenthesis like [{", ".join(parenthesis_operator_combos)}]")
    
    return True

def has_matching_paretheses(expression : str, raise_error : bool = False):
    current_expected_pairs : int = 0

    for symbol in expression:
        if symbol not in ("(", ")"):
            continue

        current_expected_pairs += 1 if symbol == "(" else -1

        if current_expected_pairs >=0:
            continue

        if raise_error:
            raise ParenthesisError("Unnmatched closing parenthesis")
        
        return False
    
    if current_expected_pairs and raise_error:
        raise ParenthesisError("Unnmatched opening parenthesis")
    
    return not bool(current_expected_pairs)

def has_empty_parentheses(expression : str, raise_error : bool = False):
    shifted_expression : str = expression[1:] + " "
    for symbol, next_symbol in zip(expression, shifted_expression):
        if not f"{symbol}{next_symbol}" == "()":
            continue
        
        if raise_error:
            raise ParenthesisError("Cannot have paretheses with nothing in them.")
        
        return True
    
    return False


def is_empty(expression : str, raise_error : bool = False):
    if expression:
        return False

    if raise_error:
        raise EmptyError("No expression was given.")
    
    return True

def is_valid_expression(expression : str, raise_errors : bool = True) -> bool:
    if is_empty(expression, raise_errors):
        return False
    
    if not consists_of_valid_characters(expression, raise_errors):
        return False
    
    if starts_with_binary_operator(expression, raise_error_if_true = raise_errors):
        return False
    
    if ends_with_binary_operator(expression, raise_error_if_true = raise_errors):
        return False
    
    if has_consecutive_operators(expression, raise_errors):
        return False
    
    if has_operator_after_parenthesis(expression, raise_errors):
        return False
    
    if not has_matching_paretheses(expression, raise_errors):
        return False
    
    if has_empty_parentheses(expression, raise_errors):
        return False
    
    return True


if __name__ == "__main__":
    print(is_valid_expression("(1)"))








