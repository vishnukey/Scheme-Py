import parser

def run(program):
    tokens = parser.tokenize(program.__iter__())
    ast = parser.parse(tokens.__iter__())
    final_val = None
    for expr in ast:
        final_val = scheme_eval(expr)
    return final_val

def scheme_eval(expr):
    if type(expr) == type(list()):
        func, *args = expr
        return scheme_apply(func, args)
    else:
        return expr

def scheme_apply(func, args):
    if func == 'displayln':
        for arg in args:
            print(scheme_eval(arg), end='')
        print()
        return None
    if func == "+":
        sum = 0
        for arg in args:
            sum += scheme_eval(arg)
        return sum
    if func == "-":
        diff = args[0]
        for arg in args[1:]:
            diff -= scheme_eval(arg)
        return diff
    if func == "*":
        prod = 1
        for arg in args:
            prod *= scheme_eval(arg)
        return prod
    if func == "/":
        quotient = args[0]
        for arg in args[1:]:
            quotient /= scheme_eval(arg)
        return quotient
