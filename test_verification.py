import re

OPERATORS = ("^", "*", "/", "+", "-")
operator_pattern_creator = ["^["]
operator_pattern_creator.extend([f"\\{operator}" for operator in OPERATORS])
operator_pattern_creator.append("]{1}$")
operator_pattern_str = "".join(operator_pattern_creator)
OPERATOR_PATTERN = re.compile(operator_pattern_str)
print(OPERATOR_PATTERN.match("-"))




NUMBER_PATTERN = re.compile(r"(^[0-9]+(\.[0-9])?$)")


def is_numerical_value(token : str) -> bool:
    return bool(NUMBER_PATTERN.match(token))

def is_operator(token : str) -> bool:
    pass
if __name__ == "__main__":
    is_operator("+")
    # while True:
    #     test_string = input("test string: ")
    #     if is_numerical_value(test_string):
    #         print("hey")
    #     else:
    #         print("not hey")
    #         break