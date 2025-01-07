from operands.node import NODE
from operands.fluid import FLUID
from operands.const import CONST
from operands.var import VAR
from operands.mul import MUL
from operands.add import ADD 
from operands.pow import POW
from operands.div import DIV
from copy import deepcopy

def check_expression_for_polynomial_notation(node: NODE) -> bool:
    if isinstance(node, DIV):
        return False # What needs to happen here with regard to the fraction notation of rational numbers???
        if not isinstance(node.children[0], CONST) or not isinstance(node.children[1], CONST):
            return False
    
    if isinstance(node, ADD):
        values = []
        for child in node.children:
            values.append(check_expression_for_polynomial_notation(child))
        return all(values)
            
    def is_power_var_to_int(node: POW) -> bool:
        return isinstance(node.children[0], VAR) and isinstance(node.children[1], CONST) and float(node.children[1].value).is_integer()
    
    def check_monomial(node: NODE) -> bool:
        for child in node.children:
            if isinstance(child, POW) and not is_power_var_to_int(child):
                    return False
            if isinstance(child, FLUID):
                return False
            if isinstance(child, DIV):
                return False
            #It also is not a SUB type because those don't occur anymore
        return True

    if isinstance(node, MUL):
        return check_monomial(node)
    
    if isinstance(node, POW) and not is_power_var_to_int(node):
        return False

    return True
        
def count_degree_of_polynomial_space(node: NODE) -> list[str]:
    vars = []
    if isinstance(node, VAR):
        return [node.value]
    if isinstance(node, CONST):
        return vars
    
    def descend(node: NODE):
        for child in node.children:
            if isinstance(child, VAR):
                if (not child.value in vars):
                    vars.append(child.value)
                continue
            if isinstance(child, FLUID):
                descend(child)
                continue
            if isinstance(child, POW):
                if isinstance(child.children[0], VAR) and not child.children[0].value in vars:
                    vars.append(child.children[0].value)

    descend(node)

    return vars

def sort_monomial(node: NODE):
    #If the simplify functions properly, and x * x always gets simplified to x^2, this should work perfectly. Otherwise its fucked
    vars = count_degree_of_polynomial_space(node)
    vars.sort()

    if isinstance(node, CONST) or isinstance(node, VAR) or isinstance(node, POW):
        return node
    d = dict.fromkeys(vars, -1)
    const = -1
    for i, child in enumerate(node.children):
        if isinstance(child, VAR):
            d[child.value] = i
            continue
        if isinstance(child, POW):
            d[child.children[0].value] = i
            continue
        if isinstance(child, CONST):
            if const > -1: raise Exception("Cannot have two constants in the same monomial")
            const = i
    
    new_children = []

    if const > -1:
        new_children.append(node.children[const])

    for var in vars: # Use vars instead of d.keys() because vars is ordered and d.keys is not
        new_children.append(node.children[d[var]])

    node.children = new_children

    return node

def compare_two_monomials(mon1: NODE, mon2: NODE) -> tuple[NODE, NODE]:
    # Check if the monomials start with scalar multipliers at the front

    if isinstance(mon1, CONST):
        new_mon1 = [mon1]
    if isinstance(mon2, CONST):
        new_mon2 = [mon2]
    
    if isinstance(mon1, VAR):
        new_mon1 = [mon1]
    if isinstance(mon2, VAR):
        new_mon2 = [mon2]

    if isinstance(mon1, POW):
        new_mon1 = [mon1]
    if isinstance(mon2, POW):
        new_mon2 = [mon2]

    if isinstance(mon1, MUL):
        new_mon1 = mon1.children
        if isinstance(new_mon1[0], CONST):
            new_mon1 = new_mon1[1:]
    if isinstance(mon2, MUL):
        new_mon2 = mon2.children
        if isinstance(new_mon2[0], CONST):
            new_mon2 = new_mon2[1:]
    
    # Then loop to find the greatest monomial

    for i in range(min(len(new_mon1), len(new_mon2))):
        if isinstance(new_mon1[i], VAR) and isinstance(new_mon2[i], VAR):
            if new_mon1[i].value == new_mon2[i].value:
                continue
            if new_mon1[i].value < new_mon2[i].value:
                return mon1, mon2
            return mon2, mon1
        if isinstance(new_mon1[i], VAR) and isinstance(new_mon2[i], POW):
            if new_mon1[i].value < new_mon2[i].children[0].value:
                return mon1, mon2
            return mon2, mon1
        if isinstance(new_mon1[i], POW) and isinstance(new_mon2[i], VAR):
            if new_mon1[i].children[0].value > new_mon2[i].value:
                return mon2, mon1
            return mon1, mon2
        if isinstance(new_mon1[i], POW) and isinstance(new_mon2[i], POW): # Finished
            if new_mon1[i].children[0].value == new_mon2[i].children[0].value:
                if new_mon1[i].children[1].value == new_mon2[i].children[1].value:
                    continue
                if new_mon1[i].children[1].value > new_mon2[i].children[1].value:
                    return mon1, mon2
                return mon2, mon1
            if new_mon1[i].children[0].value < new_mon2[i].children[0].value:
                return mon1, mon2
            return mon2, mon1
    
    #If the the shorter monomial has the first few factors of the other, the shorter monomial comes first
        
    if len(new_mon1) > len(new_mon2):
        return mon2, mon1
    return mon1, mon2

def change_to_lex_order(node: ADD) -> ADD: # Assume there are no dumb notations such as x*x*x but instead that has been simplified to x^3
    if not isinstance(node, ADD):
        return node
    
    vars = count_degree_of_polynomial_space(node)
    vars.sort()

    # Sort all the monomials
    for i, child in enumerate(node.children):
        node.children[i] = sort_monomial(child)

    children = node.children.copy()
    ordered_children = []

    for i in range(len(children) - 1):
        highest_lex_monomial = children[-1]
        for child in children:
            highest_lex_monomial, residual = compare_two_monomials(child, highest_lex_monomial)
        ordered_children.append(highest_lex_monomial)
        children.remove(highest_lex_monomial)
    
    ordered_children.append(children[0])

    node.children = list(ordered_children)

    return node

def count_polynomial_degree(node: NODE) -> int:
    # This function assumes that node has already been passed through check_expression_for_polynomial_notation()
    if isinstance(node, ADD):
        degrees = [0]
        for child in node.children:
            if isinstance(child, MUL):
                degree = 0
                for grandchild in child.children:
                    if isinstance(grandchild, VAR):
                        degree += 1
                    if isinstance(grandchild, POW):
                        degree += grandchild.children[1].value
                degrees.append(degree)
            if isinstance(child, POW):
                degrees.append(child.children[1].value)
            if isinstance(child, VAR):
                degrees.append(1)
            # If the child is CONST then it has degree 0, which doesn't need to be added to the degrees list
        return max(degrees)
    if isinstance(node, MUL):
        degree = 0
        for child in node.children:
            if isinstance(child, VAR):
                degree += 1
            if isinstance(child, POW):
                degree += child.children[1].value
        return degree
    if isinstance(node, POW):
        return node.children[1].value
    if isinstance(node, VAR):
        return 1
    return 0

def monomial_divides_monomial(dividend, divisor) -> bool:
    # Check all the possible options for which to return true, then return false
    if isinstance(divisor, CONST):
        return True
    if isinstance(divisor, VAR) and divisor.value in count_degree_of_polynomial_space(dividend):
        return True
    if isinstance(divisor, POW) and divisor.children[0].value in count_degree_of_polynomial_space(dividend) and not isinstance(dividend, VAR): # Don't need to check for dividend == CONST, because then polynomial space is []
        if isinstance(dividend, POW):
            return dividend.children[1].value >= divisor.children[1].value
        for child in dividend.children: # This assumes that dividend is of class MUL
            if isinstance(child, POW) and child.children[0].value == divisor.children[0].value and child.children[1].value >= divisor.children[1].value:
                return True
    if isinstance(divisor, MUL):
        values = []
        for child in divisor.children:
            print("Checking the loop of the mul monomial", dividend, child)
            values.append(monomial_divides_monomial(dividend, child))
        return all(values)
    
    return False

def find_long_monomial_diff(mon_big, mon_small):
    # Other trivial cases
    l = []
    for child in mon_big.children:
        if not isinstance(child, CONST):
            var = None
            degree_big = 0
            if isinstance(child, VAR):
                var = child.value
                degree_big = 1
            if isinstance(child, POW):
                var = child.children[0].value
                degree_big = child.children[1].value
            mutation_occured = False
            for baby in mon_small.children:
                if isinstance(baby, VAR) and var == baby.value:
                    mutation_occured = True
                    if degree_big - 1 == 1:
                        l.append(VAR(var))
                    if degree_big - 1 > 1:
                        l.append(POW(VAR(var), CONST(degree_big - 1)))
                if isinstance(baby, POW) and var == baby.children[0].value:
                    mutation_occured = True
                    print("Test")
                    if degree_big - baby.children[1].value == 1:
                        l.append(VAR(var))
                    if degree_big - baby.children[1].value > 1:
                        l.append(POW(VAR(var), CONST(degree_big - baby.children[1].value)))
            if not mutation_occured:
                l.append(child)
    if len(l) == 0:
        return VAR(1)
    if len(l) == 1:
        return l[0]
    return sort_monomial(MUL(*l))

def divide_monomials(dividend: NODE, divisor: NODE) -> NODE:
    if isinstance(divisor, CONST) and not isinstance(dividend, CONST) and not isinstance(dividend, VAR):
        for i in range(len(dividend.children)):
            if isinstance(dividend.children[i], CONST):
                dividend.children[i].value /= divisor.value
                return dividend
        
        divisor.children.insert(0, CONST(1/divisor.value))
        return divisor
    
    if isinstance(divisor, CONST) and (isinstance(dividend, CONST) or isinstance(dividend, VAR)):
        return DIV(dividend.value, divisor.value)

    if isinstance(divisor, VAR):
        if isinstance(dividend, VAR):
            if dividend.value == divisor.value:
                return 1
            return DIV(dividend.value, divisor.value)
        if isinstance(dividend, POW):
            if dividend.children[0].value == divisor.value:
                if dividend.children[1].value == 2:
                    return divisor
                dividend.children[1].value -= 1
                return dividend
        # dividend is of type MUL
        for i in range(len(dividend.children)):
            if isinstance(dividend.children[i], VAR) and dividend.children[i].value == divisor.value:
                dividend.children.pop(i)
                if len(dividend.children) == 1:
                    return dividend.children[0]
                return dividend
            if isinstance(dividend.children[i], POW) and dividend.children[i].children[0].value == divisor.value:
                if dividend.children[i].children[1].value == 2:
                    dividend.children[i] = VAR(dividend.children[i].children[0].value)
                    return dividend
                dividend.children[i].children[1].value -= 1
                return dividend
    
    if isinstance(divisor, POW):
        if isinstance(dividend, POW):
            diff = dividend.children[1].value - divisor.children[1].value
            if diff == 0:
                return 1
            if diff == 1:
                return VAR(dividend.children[0].value)
            dividend.children[1].value = diff
            return dividend
        for i in range(len(dividend.children)):
            if isinstance(dividend.children[i], POW) and dividend.children[i].children[0].value == divisor.children[0].value:
                diff = dividend.children[i].children[1].value - divisor.children[1].value
                if diff == 0:
                    dividend.children.pop(i)
                    if len(dividend.children) == 1:
                        return dividend.children[0]
                    return dividend
                if diff == 1:
                    dividend.children[i] = VAR(dividend.children[i].children[0].value)
                    return dividend
                dividend.children[i].children[1].value = diff
                return dividend

    print("Doing MUL") # In this case it can be assumed that dividend is also a MUL, because divisor divides dividend
    return find_long_monomial_diff(dividend, divisor)

def long_division(node: DIV):
    # Perform a couple of checks before starting the algorithm
    if not isinstance(node, DIV):
        print("Long division can only be performed on a DIV class")
        return node #AssertionError("Division algorithm can only occur on division class")
    if not check_expression_for_polynomial_notation(node.children[0]):
        print("Dividend must be a polynomial")
        return node #AssertionError("Numerator must be in polynomial form")
    if not check_expression_for_polynomial_notation(node.children[1]):
        print("Divisor must be a polynomial")
        return node #AssertionError("Denominator must be in polynomial form")
    if count_polynomial_degree(node.children[0]) <= count_polynomial_degree(node.children[1]):
        print("Dividend degree must exceed divisor degree")
        return node # Nothing else to do
    
    dividend = deepcopy(change_to_lex_order(node.children[0]))
    divisor = deepcopy(change_to_lex_order(node.children[1]))

    if not isinstance(dividend, ADD) and not isinstance(divisor, ADD):
        print("dividend or divisor should be a polynomial")
        return node

    print("Dividend:", dividend)
    print("Divisor:", divisor)

    print(monomial_divides_monomial(dividend, divisor), "Test")
    
    q = []
    r = None

    foremost_dividend_monomial = deepcopy(dividend.children[0]) if isinstance(dividend, ADD) else deepcopy(dividend)
    foremost_divisor_monomial = deepcopy(divisor.children[0]) if isinstance(divisor, ADD) else deepcopy(divisor)

    if monomial_divides_monomial(foremost_dividend_monomial, foremost_divisor_monomial):
        
        print("im:", divide_monomials(foremost_dividend_monomial, foremost_divisor_monomial))

    #divide_by = 




    

    

    
    

    
    