import re

class InvalidCharacterError(Exception):
    pass

class OperatorPlacementError(Exception):
    pass

class ParenthesisError(Exception):
    pass

class EmptyError(Exception):
    pass

OPERATORS = ("^", "*", "/", "+", "-")
operator_pattern_creator = ["^["]
operators_in_pattern = "".join([f"\\{operator}" for operator in OPERATORS])
operator_pattern_creator.append(operators_in_pattern)
operator_pattern_creator.append("]{1}$")
operator_pattern_str = "".join(operator_pattern_creator)
IS_OPERATOR_PATTERN = re.compile(operator_pattern_str)

NUMBER_PATTERN = re.compile(r"(^-?[0-9]+(\.[0-9]+)?$)")

invalid_characters_str = f'[^a-zA-Z0-9{operators_in_pattern}()\\s\\.]'
INVALID_CHARACTERS_PATTERN = re.compile(invalid_characters_str)

operators_in_pattern_excluding_minus = [f"\\{operator}" for operator in OPERATORS if operator != "-"]
operators_excluding_minus_pattern_str = "".join(operators_in_pattern_excluding_minus)
start_or_end_operator_pattern_str = f"^[{operators_excluding_minus_pattern_str}]|[{operators_in_pattern}]$"
START_OR_END_OPERATOR_PATTERN = re.compile(start_or_end_operator_pattern_str)

consecutive_operator_pattern_str = f"[{operators_excluding_minus_pattern_str}]{{2,}}|\\-[{operators_excluding_minus_pattern_str}]"
CONSECUTIVE_OPERATOR_PATTERN = re.compile(consecutive_operator_pattern_str)

parenthesis_operator_pattern_str = f"\\([{operators_excluding_minus_pattern_str}]"
PARENTHESIS_OPERATOR_PATTERN = re.compile(parenthesis_operator_pattern_str)

PARENTHESES_PATTERN = re.compile(r"[\(\)]")

def is_function(token : str) -> bool:
    return True

def is_numerical_value(token : str) -> bool:
    return bool(NUMBER_PATTERN.match(token))

def is_operator(token : str) -> bool:
    return token in OPERATORS

def consists_of_valid_characters(expression : str, raise_error : bool = False) -> bool:
    invalid_characters_used = INVALID_CHARACTERS_PATTERN.findall(expression)
    if not invalid_characters_used:
        return True
    
    if raise_error:
        message_end = "is not a valid character" if len(invalid_characters_used) == 1 else "are not valid characters"
        raise InvalidCharacterError(f"{", ".join(invalid_characters_used)} {message_end}.")
    
    return False

def starts_or_ends_with_binary_operator(expression : str, raise_error_if_true : bool = False, raise_error_if_false : bool = False) -> bool:
    assert not (raise_error_if_true and raise_error_if_false), "Like this it will always raise an error."
    operators_at_start_or_end = list(START_OR_END_OPERATOR_PATTERN.finditer(expression))

    if operators_at_start_or_end and raise_error_if_true:
        wrong_start_placement_warning = f"An expression cannot start with the operator {operators_at_start_or_end[0].group()}. " if operators_at_start_or_end[0].start() == 0 else ""
        wrong_end_placement_warning = f"An expression cannot end with the operator {operators_at_start_or_end[-1].group()}." if operators_at_start_or_end[-1].start() > 0 else ""
        raise OperatorPlacementError(f"{wrong_start_placement_warning}{wrong_end_placement_warning}")
    
    if raise_error_if_false:
        raise OperatorPlacementError(f"For some reason an operator needs to be at the start or end of the expression.")
    
    return bool(operators_at_start_or_end)

def has_consecutive_operators(expression : str, raise_error : bool = False) -> bool:
    consecutive_operators = CONSECUTIVE_OPERATOR_PATTERN.findall(expression)

    if not consecutive_operators:
        return False
    
    if raise_error:
        raise OperatorPlacementError(f"Cannot have these operators consecutivively ({", ".join(consecutive_operators)})")

    return True

def has_operator_after_parenthesis(expression : str, raise_error : bool = False):
    parenthesis_operator_combos : list[str] = PARENTHESIS_OPERATOR_PATTERN.findall(expression)

    if not parenthesis_operator_combos:
        return False
    
    if raise_error:
        raise OperatorPlacementError(f"Cannot have these operators right after a parenthesis like [{", ".join(parenthesis_operator_combos)}]")
    
    return True

def has_matching_paretheses(expression : str, raise_error : bool = False):
    parentheses : list[str] = PARENTHESES_PATTERN.findall(expression)
    current_expected_pairs : int = 0

    for symbol in parentheses:
        current_expected_pairs += 1 if symbol == "(" else -1

        if current_expected_pairs >=0:
            continue

        if raise_error:
            raise ParenthesisError("Unnmatched closing parenthesis")
        
        return False
    
    if current_expected_pairs and raise_error:
        raise ParenthesisError("Unnmatched opening parenthesis")
    
    return not bool(current_expected_pairs)

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
    
    if starts_or_ends_with_binary_operator(expression, raise_error_if_true = raise_errors):
        return False
    
    if has_consecutive_operators(expression, raise_errors):
        return False
    
    if has_operator_after_parenthesis(expression, raise_errors):
        return False
    
    if not has_matching_paretheses(expression, raise_errors):
        return False
    
    return True


if __name__ == "__main__":
    print(is_numerical_value("-1.01"))