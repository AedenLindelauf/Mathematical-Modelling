from tree import Tree
from node import *
from shunting_yard import *

if __name__ == "__main__":
    
    post_fixer_1 = Post_Fixer("2 ^ ( 2 + x ^ 2 * y )")
    test_tree = create_tree(post_fixer_1.postfix_notation)
    print(test_tree)