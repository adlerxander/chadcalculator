from chad_calculator import ChadCalculator


def main():
    # calculations
    solve("7.1+13+5+10+15+1", 51.1)  # addition
    solve("5-3-1-16", -15)  # subtraction
    solve("-3-5", -8)  # negative
    solve("2-3+6+2-2", 5)  # addition and subtraction
    solve("2+2*2", 6)  # multiplication
    solve("2-3/2*4+7", 3)  # division
    solve("(2-(1+4)/2)*2", -1)  # parentheses
    # exceptions
    solve("", "no result")  # no expression
    solve("21", 21)  # float input
    solve("lol", "no result")  # no operations
    solve(2 + 1, "no result")  # not a string
    solve("2+((1+3)", "no result")  # parentheses syntax
    solve("5/(3*2-6)", "error: division by zero")  # division by zero
    solve("1+%", "error: not a valid expression")  # non-valid expression

    # while True:
    #     expression = input()
    #     if expression == "exit":
    #         break
    #     else:
    #         calc = ChadCalculator()
    #         calc.calculate(expression)
    #         print(calc.result)

    solve("-(-2)", 2)  # SooS
    # TODO understand git (install fork)

    print("chad calculates!")


def solve(expression, result):
    calc = ChadCalculator()
    calc.calculate(expression)
    success = calc.result == result
    if not success:
        raise Exception("wrong calculations")
    print(calc.result, "\t", success)


if __name__ == '__main__':
    main()
