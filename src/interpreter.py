from scope import Scope

MATH_OPS = ["+", "-", "*", "/"]

def interpret(tokens, parent_scope = None):
    result = []
    scope = Scope(parent_scope)

    tokens_type = type(tokens)
    if tokens_type == int or tokens_type == float:
        return tokens

    def eval(token):
        return interpret(token, scope)

    if type(tokens[0]) != list:
        tokens = [tokens]

    for token in tokens:
        if token[0] == "feed":
            result.append(f"feed {eval(token[1])}")
        elif token[0] == "bend":
            result.append(f"bend {eval(token[1])}")
        elif token[0] == "repeat":
            for i in range(eval(token[1])):
                local_result = eval(token[2])
                for line in local_result:
                    result.append(line)
        elif token[0] == "var":
            scope.set(token[1], eval(token[2]))
        elif token[0] in MATH_OPS:
            val_1, val_2 = eval(token[1]), eval(token[2])
            if token[0] == "+":
                return val_1 + val_2
            elif token[0] == "-":
                return val_1 - val_2
            elif token[0] == "*":
                return val_1 * val_2
            elif token[0] == "/":
                return val_1 / val_2
        elif type(token[0]) == str:
            return scope.get(tokens[0])
        else:
            raise Exception(f"Unknown token `{token[0]}`")

    return result