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

    cnt = 0
    prev_failed = False
    for index in range(len(test_cases_df)):
        
        try:
            test_case = test_cases_df['INPUT'].iloc[index]
            answer = test_cases_df['OUTPUT'].iloc[index]

            input_expr  = Expression(test_case)
            input_as_text = input_expr.__str__()
            answer      = Expression(answer)
            answer.tree.convert_to_common_operator_structure()

            if simplify:
                input_expr.simplify()
            else:
                input_expr.differentiate("x")
                input_expr.tree.convert_to_common_operator_structure()
                input_expr.simplify()

            if input_expr.tree.root.compare(answer.tree.root):
                print(Fore.GREEN + 'Passed test {:>3}'.format(index+1), end=' || ')
                print(Fore.MAGENTA + "Test case: ", end='')
                print(f"{test_case}", end='')
                print(Fore.YELLOW + ' - Input as tree: ', end='')
                print(f"{input_as_text}")
                prev_failed = False
                cnt += 1
            else:
                if not prev_failed:
                    print("--------------------------------------------------")
                print(Fore.RED + Style.BRIGHT + 'Failed test {:>3}'.format(index+1) )
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
            print(f"ERROR OCCURED - {test_case}")
            print("--------------------------------------------------")
            prev_failed = True

    color = Fore.WHITE  
    if cnt == len(test_cases_df):
        color = Fore.GREEN
    else: color = Fore.RED
    
    print(Style.BRIGHT + color + f"\nPassed {cnt}/{len(test_cases_df)} cases")
    print("================= END OF TESTING =================\n\n")

if __name__ == "__main__":
    init(autoreset=True)
    system("cls")

    TEST(True)