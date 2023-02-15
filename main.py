# todo use formal parser
def parser(str):
    return [["var", "num_times", 10], ["repeat", "num_times", [["feed", 2], ["bend", 3.6]], ["feed", 10]]]

MATH_OPS = ["+", "-", "*", "/"]

class Scope:
    def __init__(self, parent_scope = None):
        self.variables = {}
        self.parent_scope = parent_scope

    def get(self, name):
        if type(name) != str:
            return name
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

def interpreter(tokens, parent_scope = None):
    result = []
    scope = Scope(parent_scope)

    for token in tokens:
        if token[0] == "feed":
            result.append(f"feed {scope.get(token[1])}")
        elif token[0] == "bend":
            result.append(f"bend {scope.get(token[1])}")
        elif token[0] == "repeat":
            for i in range(scope.get(token[1])):
                local_result = interpreter(token[2], parent_scope)
                for line in local_result:
                    result.append(line)
        elif token[0] == "var":
            scope.set(token[1], scope.get(token[2]))

    return result

if __name__ == "__main__":
    output = None
    with open("input/script.wire", "r") as f:
        tokens = parser(f.read())
        output = interpreter(tokens)
    with open("output/script.wirec", "w") as f:
        for line in output:
            f.write(line)
            f.write("\n")
        f.write("\n".join(output))
