import re
from math import sin, cos, tan, asin, acos, atan, sqrt, log, log10
from random import random
from scope import Scope

PRIMITIVES = ["feed", "bend", "rotate"]
MATH_1_ARG_OPS = {"sin": sin, "cos": cos, "tan": tan, "asin": asin, "acos": acos, "atan": atan, "sqrt": sqrt, "log": log, "log10": log10, "abs": lambda a: a // 1}
MATH_2_ARG_OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b, "%": lambda a, b: a % b, "**": lambda a, b: a ** b, "//": lambda a, b: a // b}
LOGIC_OPS = {"==": lambda a, b: a == b, "!=": lambda a, b: a != b, ">": lambda a, b: a > b, "<": lambda a, b: a < b, ">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "and": lambda a, b: a and b, "or": lambda a, b: a or b, "ifelse": lambda a, b: b if a else b}

class Interpreter:
    def __init__(self):
        self.result = []

    def eval(self, tokens, parent_scope = None):
        scope = Scope(parent_scope)
        tokens_type = type(tokens)
        if tokens_type == int or tokens_type == float:
            return tokens
        is_valid_num = lambda x: re.search(r"^[0-9]+$", x) 
        # check for negative numbers
        if tokens_type == str and (is_valid_num(tokens) or (tokens[0] == "-" and is_valid_num(tokens[1:]))):
            return float(tokens)

        def _eval(token):
            return self.eval(token, scope)

        def eval_token(token):
            # variables
            if type(token) == str:
                return scope.get(tokens)
            method = token[0]
            if method == "var":
                key = token[1]
                # TODO: move array parsing to parser
                if type(token[2]) != int and token[2][0] == "[":
                    first = _eval(token[2][1:])
                    if len(token) > 3:
                        middle = [_eval(t) for t in token[3:-1]]
                        last = token[-1][:-1]
                        arr = [first, *middle, last]
                        scope.set(key, list(map(_eval, arr)))
                    else:
                        scope.set(key, _eval(first))
                    return
                scope.set(key, _eval(token[2]))
                return
            elif method == "get" or method == "set":
                key = token[1]
                index = int(_eval(token[2]))
                arr = scope.get(key)
                if type(arr) != list:
                    raise Exception(f"Cannot index non-array `{key}` of type `{type(arr)}`")
                if index >= len(arr):
                    raise Exception(f"Index out of bounds for `{key}`")
                if method == "get":
                    return arr[index]
                elif method == "set":
                    arr[index] = _eval(token[3])
            elif method == "len":
                key = token[1]
                arr = scope.get(key)
                if type(arr) != list:
                    raise Exception(f"Cannot get length of non-array `{key}` of type `{type(arr)}`")
                return len(arr)
            # functions
            elif method == "def":
                args = token[2]
                body = token[3]
                scope.set(token[1], (args, body))
            # primitives
            elif method in PRIMITIVES:
                self.result.append(f"{method} {_eval(token[1])}")
            elif method == "repeat":
                for _ in range(_eval(token[1])):
                    local_results = _eval(token[2])
                    for local_result in local_results:
                        if local_result != None:
                            self.result.append(local_result)
            # simple ops
            elif method in MATH_2_ARG_OPS:
                return MATH_2_ARG_OPS[method](_eval(token[1]), _eval(token[2]))
            elif method in MATH_1_ARG_OPS:
                return MATH_1_ARG_OPS[method](_eval(token[1]))
            elif method in LOGIC_OPS:
                return LOGIC_OPS[method](_eval(token[1]), _eval(token[2]))
            elif method == "rand":
                return random()

            # log to comments
            elif method == "log":
                self.result.append(f"# {_eval(token[1])}")

            # custom declared functions
            elif scope.get(method):
                arg_names, body = scope.get(method)
                if len(arg_names) != len(token[1:]):
                    raise Exception(f"Wrong number of arguments for `{method}`")
                function_scope = Scope(scope)
                for name, value in zip(arg_names, token[1:]):
                    function_scope.set(name, _eval(value))
                return self.eval(body, function_scope)
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
