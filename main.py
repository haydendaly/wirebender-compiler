# todo use formal parser
def parser(str):
    return [["repeat", 2, [["feed", 2], ["bend", 3.6]], ["feed", 10]]]

class Scope:
    def __init__(self, parent_scope = None):
        self.variables = {}
        self.parent_scope = parent_scope

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent_scope:
            return self.parent_scope.get(name)
        return None

    def set(self, name, value):
        if name in self.variables:
            # throw an err
            raise Exception(f"Variable `{name}` already exists in scope")
        self.variables[name] = value

def interpreter(tokens):
    result = []
    scope = Scope()

    for token in tokens:
        if token[0] == "feed":
            result.append(f"feed {token[1]}")
        elif token[0] == "bend":
            result.append(f"bend {token[1]}")
        elif token[0] == "repeat":
            for i in range(token[1]):
                local_result = interpreter(token[2])
                for line in local_result:
                    result.append(line)
        elif token[0] == "var":
            scope.set(token[1], token[2])
    return result

if __name__ == "__main__":
    output = None
    with open("script.txt", "r") as f:
        tokens = parser(f.read())
        output = interpreter(tokens)
    with open("output.txt", "w") as f:
        for line in output:
            f.write(line)
            f.write("\n")
        f.write("\n".join(output))
