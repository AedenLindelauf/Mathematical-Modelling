from tree import Tree
from node import *
from shunting_yard import *

if __name__ == "__main__":
    print()
    post_fixer_1 = Post_Fixer("------1")
    print(post_fixer_1.postfix_notation)
    test_tree = create_tree(post_fixer_1.postfix_notation)
    