# this is loosely based on peter norvig's lisp parser
def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    tokens = tokenize(program)
    return read_from_tokens(tokens)

def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)


def parse_hardcoded(str):
    return [["var", "num_times", 10], ["var", "bend_angle", ["/", 360, "num_times"]], ["repeat", "num_times", [["feed", 2], ["bend", "bend_angle"]], ["feed", 10]]]