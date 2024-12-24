from expression import Expression
from colorama import Fore, Back, Style, init
from os import system
import pandas


def TEST(simplify: bool):

    if simplify:
        test_cases_df = pandas.read_excel("TESTCASES_SIMPLIFICATION.xlsx",
                                          header=0, dtype={'INPUT': str, 'OUTPUT': str})
    else:
        test_cases_df = pandas.read_excel("TESTCASES_DIFFERENTIATION.xlsx", 
                                          header=0, dtype={'INPUT': str, 'OUTPUT': str})

    if simplify:
        print("====== TESTING SIMPLIFICATION FUNCTIONALITY ======\n")
    else:
        print("====== TESTING DIFFERENTIATION FUNCTIONALITY =====\n")

    prev_failed = False
    for index in range(len(test_cases_df)):
        
        try:
            test_case = test_cases_df['INPUT'].iloc[index]
            answer = test_cases_df['OUTPUT'].iloc[index]

            input_expr  = Expression(test_case)
            input_as_text = input_expr.__str__()
            answer      = Expression(answer)

            if simplify:
                input_expr.simplify()
            else:
                raise NotImplementedError("Differentiation not yet implemented...")

            if input_expr.tree.root.compare(answer.tree.root):
                print(Fore.GREEN + f'Passed test {index + 1}', end=' || ')
                print(f"Test case: {test_case} - Input as tree: {input_as_text}")
                prev_failed = False
            else:
                if not prev_failed:
                    print("--------------------------------------------------")
                print(Fore.RED + Style.BRIGHT + f'Failed test {index+1}')
                print(f"Test case:\t\t{test_case}")
                print(f"Input Expression:\t{input_as_text}")
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

if __name__ == "__main__":
    init(autoreset=True)
    system("cls")

    TEST(True)