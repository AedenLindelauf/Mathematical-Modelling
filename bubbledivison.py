from expression import Expression
from tree import Tree
from node import *

def bubble_division(node : NODE) -> Tree:
    if not isinstance(node, BINARY):
        return node
    
    node.left = bubble_division(node.left)
    node.right = bubble_division(node.right)

    if not isinstance(node.left, DIV) and not isinstance(node.right, DIV):
        return node

    if isinstance(node, POW):
        return node
    
    new_node : DIV = DIV()

    if isinstance(node, DIV):
        if isinstance(node.left, DIV):
            new_node.left = node.left.left
            new_node.right = node.left.right

        else:
            new_node.left = node.left
            new_node.right = CONST(1)

        if isinstance(node.right, DIV):
            new_node.left *= node.right.right
            new_node.right *= node.right.left
        
        else:
            new_node.right *= node.right

    
    if isinstance(node, MUL):
        if isinstance(node.left, DIV):
            new_node.left = node.left.left
            new_node.right = node.left.right

        else:
            new_node.left = node.left
            new_node.right = CONST(1)
        
        if isinstance(node.right, DIV):
            new_node.right *= node.right.right
            new_node.left *= node.right.left

        else:
            new_node.left *= node.right
    
    if isinstance(node, (ADD, SUB)):
        new_node.left = type(node)()
        
        if isinstance(node.left, DIV):
            new_node.left.left = node.left.left
            new_node.left.right = node.left.right
            new_node.right = node.left.right
        
        else:
            new_node.left.left = node.left
            new_node.left.right = CONST(1)
            new_node.right = CONST(1)

        if isinstance(node.right, DIV):
            new_node.left.right *= node.right.left 
            new_node.left.left *= node.right.right 
            new_node.right *= node.right.right
        
        else:
            new_node.left.right *= node.right

    
    return new_node
        


if __name__ == "__main__":
    expression = Expression("x/y-x")
    tree = expression.tree
    print(bubble_division(tree.root))
