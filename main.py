class Token:
    def __init__(line):
        tokens = line.split(" ")
        self.type = tokens[0]
        self.args = tokens[1:]
        self.children = []
        pass

    def __tostring__():
        return self.type + " " + " ".join(self.args)

# todo use formal parser
def parser(str):
    tokens = [line.split(" ") for line in str.splitlines()]

    i = 0
    lines = str.splitlines()
    tokens = []
    while i < len(lines):
        token = new Token(lines[i])
        if token.type == "repeat":
            i += 1
            while lines[i] != "end":
                token.children.append(new Token(lines[i]))
                i += 1

        tokens.append(token)

    tokens_as_strs = map(lambda x: x.__tostring__(), tokens)
    return "\n".join(map(lambda x: new Token(x), tokens))

def interpreter(tokens):
    return output

if __name__ == "__main__":
    output = None
    with open("script.txt", "r") as f:
        tokens = parser(f.read())
        output = interpreter(tokens)
    with open("output.txt", "w") as f:
        f.write(output)
