from parser import parse
from interpreter import Interpreter

def main():
    tokens = None
    with open("input/script.wire", "r") as f:
        tokens = parse(f.read())

    interpreter = Interpreter()
    interpreter.eval(tokens)

    output = interpreter.compile()

    with open("output/script.wirec", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
