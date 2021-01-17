from typing import Optional, Tuple
from node import Node


# function to check if str is float
def is_float(string):
    if string.find("$") == 0:
        substring = string.replace("$", "", 1)
        try:
            float(substring)
            return True
        except ValueError:
            return False
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


# function to check if str is not a math expression
def is_word(expression: str):
    no_operators = expression.count("+") == 0 and \
                   expression.count("-") == 0 and \
                   expression.count("*") == 0 and \
                   expression.count("/") == 0
    operator_first = expression.find("+") == 0 or \
                     expression.find("*") == 0 or \
                     expression.find("/") == 0
    operator_last = expression.rfind("+") == len(expression) - 1 or \
                    expression.rfind("-") == len(expression) - 1 or \
                    expression.rfind("*") == len(expression) - 1 or \
                    expression.rfind("/") == len(expression) - 1
    return no_operators or operator_first or operator_last


class ChadCalculator:
    def __init__(self):
        self.result = "no result"

    def calculate(self, expression: str):
        if type(expression) != str:
            print("error: not a string")
            return

        # preformatting the expression
        expression = expression.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")

        # warnings
        if len(expression) == 0:
            print("error: no expression")
            return
        if is_float(expression):
            self.result = float(expression)
            return
        if is_word(expression):
            print("error: no operations")
            return
        if expression.count("(") != expression.count(")"):
            print("error: bad syntax (parentheses not matching)")
            return

        root = self.__parse_tree__(expression)
        root = self.__simplify__(root)
        self.result = self.__perform__(root.left, root.right, root.data)
        if is_float(self.result):
            self.result = float(self.result)

        return

    # function to simplify trees
    def __simplify__(self, node: Node):
        # checking if simplification needed
        if not is_float(node.left):
            if is_word(node.left):
                node.left = "error: not a valid expression"
            else:
                node.left = self.__solve_branch__(node.left)

        # checking if simplification needed
        if not is_float(node.right):
            if is_word(node.right):
                node.right = "error: not a valid expression"
            else:
                node.right = self.__solve_branch__(node.right)

        return node

    # function to solve tree branches recursively
    def __solve_branch__(self, branch: str):
        subroot = self.__parse_tree__(branch)

        # wanna simplify branches recursively?
        while not is_float(subroot.left) or not is_float(subroot.right):
            self.__simplify__(subroot)

        return self.__perform__(subroot.left, subroot.right, subroot.data)

    # function to split strings around operators
    def __parse__(self, expression: str, operator: str) -> Optional[Tuple[str, str]]:
        operator_index = expression.rfind(operator)  # starting from the right to satisfy commutativity
        if operator_index == -1:
            return None
        return expression[:operator_index], expression[operator_index + 1:]

    # function to create nodes
    def __parse_tree__(self, expression: str) -> Node:
        root, subexpression1, subexpression2 = None, None, None

        # checking for parentheses
        if "(" in expression:
            left_bracket_index = expression.find("(")
            right_bracket_index = expression.rfind(")")
            bracket = expression[left_bracket_index + 1:right_bracket_index]  # the insides of brackets

            if is_float(bracket):
                solved_bracket = bracket
            else:
                bracket_tree = self.__parse_tree__(bracket)  # evaluating the bracket
                bracket_tree = self.__simplify__(bracket_tree)
                solved_bracket = self.__perform__(bracket_tree.left, bracket_tree.right, bracket_tree.data)

            if "-" in solved_bracket:
                solved_bracket = solved_bracket.replace("-", "$")

            expression = expression.replace("(" + bracket + ")", solved_bracket)  # replacing brackets with result

        # checking for negative number
        if expression.find("-") == 0:
            expression = expression.replace("-", "$", 1)

        # realizing the order of operations
        if "+" in expression:
            subexpression1, subexpression2 = self.__parse__(expression, "+")
            root = Node("+")
        elif "-" in expression:
            subexpression1, subexpression2 = self.__parse__(expression, "-")
            root = Node("-")
        elif "*" in expression:
            subexpression1, subexpression2 = self.__parse__(expression, "*")
            root = Node("*")
        elif "/" in expression:
            subexpression1, subexpression2 = self.__parse__(expression, "/")
            root = Node("/")
        elif "$" in expression:
            subexpression1, subexpression2 = self.__parse__(expression, "$")
            if subexpression1 == "-" or subexpression1 == "$":
                subexpression1 = "-1"
            elif subexpression1 == "":
                subexpression1 = "1"
            subexpression2 = "-" + subexpression2
            root = Node("*")
        elif is_float(expression):
            subexpression1, subexpression2 = "1", expression
            root = Node("*")

        root.left = subexpression1
        root.right = subexpression2

        return root

    # function to perform operations
    def __perform__(self, term1: str, term2: str, operator: str):
        # accounting for different errors
        if term1 == "error: division by zero" or term2 == "error: division by zero":  # handling division by zero
            return "error: division by zero"
        elif term1 == "error: not a valid expression" or term2 == "error: not a valid expression":  # handling non-valid expressions
            return "error: not a valid expression"
        else:
            if term1.find("$") == 0:
                term1 = term1.replace("$", "-")
            if term2.find("$") == 0:
                term2 = term2.replace("$", "-")

            if operator == "+":
                return str(float(term1) + float(term2))
            elif operator == "-":
                return str(float(term1) - float(term2))
            elif operator == "*":
                return str(float(term1) * float(term2))
            elif operator == "/":
                try:  # handling division by zero
                    float(term1) / float(term2)
                except ZeroDivisionError:
                    return "error: division by zero"
                else:
                    return str(float(term1) / float(term2))
