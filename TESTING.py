from expression import Expression
from colorama import Fore, Back, Style, init
from os import system
import pandas

init(autoreset=True)

test_cases_simplification_df = pandas.read_excel("TESTCASES_SIMPLIFICATION.xlsx", 
                                                 header=0, dtype={'INPUT': str, 'OUTPUT': str})

test_cases_simplification = []

system("cls")
print("====== TESTING SIMPLIFICATION FUNCTIONALITY ======\n")

prev_failed = False
for index in range(len(test_cases_simplification_df)):
    try:
        test_case = test_cases_simplification_df['INPUT'].iloc[index]
        answer = test_cases_simplification_df['OUTPUT'].iloc[index]

        input_expr  = Expression(test_case)
        answer      = Expression(answer)
        input_text  = input_expr.__str__()
        input_expr.simplify()

        if (test_case != input_expr.__str__()) and input_expr.tree.root.compare(answer.tree.root):
            print(Fore.GREEN + f'Passed test {index + 1}')
            prev_failed = False
        else:
            if not prev_failed:
                print("--------------------------------------------------")
            print(Fore.RED + Style.BRIGHT + f'Failed test {index+1}')
            print(f"Test case:\t\t{test_case}")
            print(f"Expected output:\t{answer}")
            print(f"Given output:\t\t{input_expr}")
            print("--------------------------------------------------")
            prev_failed = True
    except:
        if not prev_failed:
            print("--------------------------------------------------")
        print(Fore.RED + Style.BRIGHT + f'Failed test {index+1}')
        print("ERROR OCCURED")
        print("--------------------------------------------------")
        prev_failed = True

print("\n================= END OF TESTING =================\n\n")