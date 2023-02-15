from parser import parse
from interpreter import Interpreter

def main():
    tokens = None
    with open("input/script.wire", "r") as f:
        raw = f.read().replace("\n", " ").replace("\t", " ")
        # wrapped in list to make it a list of tokens
        raw = f"({raw})"
        tokens = parse(raw)

    interpreter = Interpreter()
    interpreter.eval(tokens)

    output = interpreter.compile()

    with open("output/script.wirec", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
