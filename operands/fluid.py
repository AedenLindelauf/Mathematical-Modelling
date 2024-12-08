from operands.node import NODE

class FLUID(NODE):
    def __init__(self, *args):
        children = [arg for arg in args]
        if len(children) < 2: raise Exception("Fluid nodes need two or more operands!") # Not really necessary, just a sanity check
        super().__init__(*children)

    # In this function we find all the "adjacent" similar operators (so all +'s or *'s)
    def find_all_similar_adjacent_operators(self) -> list[NODE]:
        subtrees = [self]
        def descend(node: NODE):
            if isinstance(node, self.__class__):
                subtrees.append(node)
                for child in node.children:
                    descend(child)

        for child in self.children:
            descend(child)
        
        return subtrees
    
    # Here the actual transmutation of the tree happens
    def convert_to_common_operator_structure(self):
        subtrees = self.find_all_similar_adjacent_operators()
        children_changed = 0
        original_number_of_children = len(self.children)
        for tree in subtrees:
            for i in range(len(tree.children)):
                if not isinstance(tree.children[i], self.__class__):
                    if children_changed < original_number_of_children:
                        self.children[children_changed] = tree.children[i]
                        children_changed += 1
                    else:
                        self.children.append(tree.children[i])
        
        from operands.binary import BINARY
        for child in self.children:
            if isinstance(child, (BINARY, FLUID) ):
                child.convert_to_common_operator_structure() # Top-down approach

