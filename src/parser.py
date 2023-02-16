# this is loosely based on peter norvig's lisp parser
def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(raw):
    # remove comments
    lines = raw.split("\n")
    semi_parsed = " ".join(list(filter(lambda s: s and s[0] != '#', lines)))
    parsed = semi_parsed.replace("\t", " ")
    # wrapped in list to make it a list of tokens
    program = f"({parsed})"
    return read_tokens(tokenize(program))

def read_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('Unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        segment = []
        while tokens[0] != ')':
            segment.append(read_tokens(tokens))
        tokens.pop(0)
        return segment
    elif ')' == token:
        raise SyntaxError('Unexpected `)`')
    else:
        return atom(token)

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)
