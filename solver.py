from itertools import product
from collections import OrderedDict
from tabulate import tabulate
import sys
import pprint

pp = pprint.PrettyPrinter(indent=2)

operators = ["=", ">", "+", "&", "~", "(", ")"]  # do not change the order


def check_precendence(c):
    if c in operators[:5]:
        return operators.index(c) + 1

    else:
        return 0


def gen_table(prepostion, alpha_order=False):
    values = OrderedDict()
    opers = []

    for p in prepostion:
        if p.isalpha() and p not in opers:
            opers.append(p)

    if alpha_order:
        opers = sorted(opers)

    tf = list(product([True, False], repeat=len(opers)))
    for i, x in enumerate(opers):
        values[x] = []
        for e, n in enumerate(tf):
            values[x].append(n[i])

    return values


def peek(stack):
    if stack:
        return stack[len(stack) - 1]

    else:
        return None


def get(table, operand):
    if type(operand) is list:
        return operand

    else:
        return table.get(operand)


def scanner(prepostion):
    # basic scanner that checks for errors
    for i, x in enumerate(prepostion):
        if not x.isalpha() and not x.isdigit() and x not in operators:
            print(prepostion)
            print("{:>{spaces}}".format("^", spaces=i + 1))
            print("invalid operator")
            exit()
        elif x.isdigit():
            print(prepostion)
            print("{:>{spaces}}".format("^", spaces=i + 1))
            print("no digits allowed in the statement")
            exit()

    stack = []
    for x in prepostion:
        if x is "(":
            stack.append("(")
        elif x is ")":
            stack.pop()

    if stack:
        print("bad brackets")
        exit()


def solver(prepostion, alpha_order=False):
    scanner(prepostion)

    def calculate():
        operation = operator_stack.pop()
        if operation == "~":
            operand = operand_stack.pop()
            l = _not(get(table, operand))
            operand_stack.append(l)
        elif operation == "&":
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            l = _and(get(table, operand1), get(table, operand2))
            operand_stack.append(l)
        elif operation == "+":
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            l = _or(get(table, operand1), get(table, operand2))
            operand_stack.append(l)
        elif operation == "=":
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            l = biconditional(get(table, operand1), get(table, operand2))
            operand_stack.append(l)
        elif operation == ">":
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            l = implies(get(table, operand1), get(table, operand2))
            operand_stack.append(l)

    operand_stack = []
    operator_stack = []
    table = gen_table(prepostion, alpha_order)

    for current in prepostion:
        if current.isalpha():
            operand_stack.append(current)
        else:
            if len(operator_stack) == 0:
                operator_stack.append(current)
            elif current == "(":
                operator_stack.append(current)
            elif current == ")":
                while (peek(operator_stack) != "("):
                    calculate()
                operator_stack.pop()
            else:
                # that means that there's already something in stack
                while check_precendence(peek(operator_stack)) >= check_precendence(
                    current
                ):
                    calculate()
                operator_stack.append(current)

    while len(operator_stack) != 0:
        calculate()
    # print(table.get("res"))

    return table, operand_stack


def _and(left, right):
    return [x and y for x, y in zip(left, right)]


def _or(left, right):
    return [x or y for x, y in zip(left, right)]


def implies(left, right):
    return [(not x) or y for x, y in zip(left, right)]


def biconditional(left, right):
    return [x == y for x, y in zip(left, right)]


def _not(table):
    return [not x for x in table]


if __name__ == "__main__":
    prepostion = input("Enter a prepostion: ")
    prepostion = prepostion.strip()
    # removing all spaces
    prepostion.replace(" ", "")

    alpha_order = False
    if "-a" in sys.argv:
        alpha_order = True

    table, operand_stack = solver(prepostion, alpha_order)

    headers = list(table.keys())
    headers.append(prepostion)
    print()

    print(tabulate(zip(*table.values(), operand_stack[0]), headers=headers))
    print()
