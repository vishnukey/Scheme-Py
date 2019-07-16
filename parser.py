import re

def OPEN_PAREN():
    return ('(', None)

def CLOSE_PAREN():
    return (')', None)

def NUM(data):
    return ('NUM', data)

def STRING(data):
    return ('STRING', data)

def IDENTIFIER(data):
    return ('IDENTIFIER', data)

def BOOL(data):
    return ('BOOL', data)

def read_until(str_iter, matcher):
    char = next(str_iter)
    out = ''
    while not matcher.match(char):
        out += char
        char = next(str_iter)
    return (out, char)

def __tokenize__(str_iter):
    tokens = []
    try:
        char = next(str_iter)
        while True:
            if char == "(":
                tokens.append(OPEN_PAREN())
            elif char == ")":
                tokens.append(CLOSE_PAREN())
            elif char == '"':
                string, end = read_until(str_iter, re.compile('"'))
                tokens.append(STRING(string))
            elif re.compile("\\d").match(char):
                num, end = read_until(str_iter, re.compile("[ \t\n)]"))
                maybe_int = char + num
                tokens.append(NUM(maybe_int))
                if end == ')':
                    char = end
                    continue
            elif char == '#':
                value = next(str_iter)
                if value == 't':
                    tokens.append(BOOL('true'))
                elif value == 'f':
                    tokens.append(BOOL('false'))
                else:
                    raise ArgumentException("Not a boolean")
            else:
                iden, end = read_until(str_iter, re.compile("[ \t\n]"))
                tokens.append(IDENTIFIER(char + iden))
            whitespace, char = read_until(str_iter, re.compile("[^ \t\n]"))
    except StopIteration as si:
        return tokens

def __parse__(token_iter):
    ast = []
    try:
        kind, payload = next(token_iter)
        while True:
            if kind == '(':
                ast.append(__parse__(token_iter))
            elif kind == ')':
                return ast
            elif kind == 'IDENTIFIER':
                ast.append(payload)
            elif kind == 'NUM':
                ast.append(float(payload))
            elif kind == 'STRING':
                ast.append(payload)
            elif kind == 'BOOL':
                ast.append(True if payload == "true" else False if payload == "false" else None)
            else:
                raise ArgumentException("Unknown type %s" % kind)
            kind, payload = next(token_iter)
    except StopIteration as si:
        return ast

def tokenize(program):
    return __tokenize__(program.__iter__())

def parse(tokens):
    return __parse__(tokens.__iter__())
