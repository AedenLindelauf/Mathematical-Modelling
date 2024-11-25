from node import *

class Tree:
    def __init__(self, root: NODE):
        self.root = root

    def __str__(self):
        return self.root.__str__()
    
    def simplify(self): 
        self.root.simplify()


if __name__ == "__main__":
    root = ADD()
    root.left = CONST(1)
    root.right = DIV()
    root.right.left = DIV()
    root.right.left.left = CONST(2)
    root.right.left.right = VAR("z")
    
    root.right.right = DIV()
    root.right.right.left = CONST(3)
    root.right.right.right = MUL()
    root.right.right.right.left = CONST(5)
    root.right.right.right.right = VAR("y")


    T = Tree(root)
    print(f"Original expression:\t {T}")
    T.simplify()
    print(f"Simplified expression:\t {T}")