from parser import parse
from interpreter import interpret

def main():
    output = None
    with open("input/script.wire", "r") as f:
        tokens = parse(f.read())
        output = interpret(tokens)
    with open("output/script.wirec", "w") as f:
        for line in output:
            f.write(line)
            f.write("\n")
        f.write("\n".join(output))

if __name__ == "__main__":
    main()