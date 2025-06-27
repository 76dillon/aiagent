def calculate(expression):
    try:
        return eval(expression)
    except (ValueError, SyntaxError, TypeError):
        return "Invalid expression"

if __name__ == "__main__":
    expression = "3 + 7 * 2"  # Hardcoded expression for testing
    print(calculate(expression))