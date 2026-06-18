
import sys

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def main():
    if len(sys.argv) != 4:
        print("Usage: python calculator.py <operation> <num1> <num2>")
        print("Operations: add, sub, mul, div")
        sys.exit(1)

    op, x_str, y_str = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        x = float(x_str)
        y = float(y_str)
    except ValueError:
        print("Both numbers must be valid numeric values.")
        sys.exit(1)

    try:
        if op == "add":
            result = add(x, y)
        elif op == "sub":
            result = sub(x, y)
        elif op == "mul":
            result = mul(x, y)
        elif op == "div":
            result = div(x, y)
        else:
            print(f"Unsupported operation: {op}")
            sys.exit(1)
        print(result)
    except ZeroDivisionError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
