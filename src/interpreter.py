from scope import Scope

PRIMITIVES = ["feed", "bend", "rotate"]
MATH_OPS = ["+", "-", "*", "/"]

class Interpreter:
    def __init__(self):
        self.result = []
        pass

    def eval(self, tokens, parent_scope = None):
        scope = Scope(parent_scope)

        tokens_type = type(tokens)
        if tokens_type == int or tokens_type == float:
            return tokens

        def _eval(token):
            return self.eval(token, scope)

        def eval_token(token):
            # variables
            if type(token) == str:
                return scope.get(tokens)

            method = token[0]
            if method == "var":
                scope.set(token[1], _eval(token[2]))
            elif method == "def":
                args = token[2]
                body = token[3]
                scope.set(token[1], (args, body))
            # primitives
            elif method in PRIMITIVES:
                self.result.append(f"{method} {_eval(token[1])}")
            elif method == "repeat":
                for i in range(_eval(token[1])):
                    local_results = _eval(token[2])
                    for local_result in local_results:
                        if local_result != None:
                            self.result.append(local_result)
            # compiler eval
            elif method in MATH_OPS:
                val_1, val_2 = _eval(token[1]), _eval(token[2])
                if method == "+":
                    return val_1 + val_2
                elif method == "-":
                    return val_1 - val_2
                elif method == "*":
                    return val_1 * val_2
                elif method == "/":
                    return val_1 / val_2
            # custom declared functions
            elif scope.get(method):
                arg_names, body = scope.get(method)
                if len(arg_names) != len(token[1:]):
                    raise Exception(f"Wrong number of arguments for `{method}`")

                function_scope = Scope(scope)
                for name, value in zip(arg_names, token[1:]):
                    function_scope.set(name, _eval(value))
                returns = self.eval(body, function_scope)
                return returns
            else:
                raise Exception(f"Unknown token `{method}`")

        if type(tokens[0]) == list:
            returns = []
            for token in tokens:
                returns.append(eval_token(token))
            return returns
        return eval_token(tokens)

    def compile(self):
        as_str = ""
        for line in self.result:
            as_str += line + "\n"
        return as_str
