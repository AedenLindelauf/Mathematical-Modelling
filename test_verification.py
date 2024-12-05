import re

OPERATORS = ("^", "*", "/", "+", "-")
operator_pattern_creator = ["^["]
operator_pattern_creator.extend([f"\\{operator}" for operator in OPERATORS])
operator_pattern_creator.append("]{1}$")
operator_pattern_str = "".join(operator_pattern_creator)
OPERATOR_PATTERN = re.compile(operator_pattern_str)
NUMBER_PATTERN = re.compile(r"(^[0-9]+(\.[0-9])?$)")
INVALID_ChARACTERS_PATTERN = re.compile(r'[^a-zA-Z0-9\+\-\*/\^()\s]')


def is_numerical_value(token : str) -> bool:
    return bool(NUMBER_PATTERN.match(token))

def is_operator(token : str) -> bool:
    return bool(OPERATOR_PATTERN.match(token))

def constists_of_valid_characters(expression : str, return_invalid_characters : bool = False) -> bool | tuple[bool, list[str]]:
    invalid_characters_used = INVALID_ChARACTERS_PATTERN.findall(expression)

    if not invalid_characters_used:
        return True
    
    return False, invalid_characters_used if return_invalid_characters else False


if __name__ == "__main__":
    while True:
        test_string = input("test string: ")
        if constists_of_valid_caracters(test_string):
            print("hey")
        else:
            print("not hey")
            break