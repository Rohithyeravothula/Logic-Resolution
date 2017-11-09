import re


class Predicate:
    pass


class Variable(Predicate):
    def __init__(self, val):
        self.val = val


class Constant(Variable):
    def __init__(self, val):
        Variable.__init__(self, val)


class Function(Predicate):
    def __init__(self, func, args, negation):
        self.func = func
        self.args = args  # list of arguments could be constants or variables
        self.negation = negation

    def __str__(self):
        v = "{}({})".format(self.func, ", ".join(self.args))
        if self.negation:
            return "~{}".format(v)
        return v

    def __repr__(self):
        return str(self)


class Sentence:
    def __init__(self, predicates):
        self.predicates = predicates


class KB:
    def __init__(self, sentences):
        self.sentences = sentences
        self.constants = None
        self.variables = None
        self.func_indexes = None  # refer mid2 ppt 5 slide 7


def is_constant(inp):
    if inp[0].upper() and "(" not in inp:
        return True
    return False


def is_variable(inp):
    if inp[0].lower():
        return True
    return False


def get_predicate(inp):
    negation = False
    if inp[0] == "~" or inp[0] == '~':
        negation = True
        inp = inp[1:]
    brace_open = inp.index("(")
    brace_close = inp.index(")")
    func = inp[0:brace_open]
    args = inp[brace_open + 1:brace_close].split(",")
    return Function(func, args, negation)


def parse(inp):
    pred_str = re.split('\|', inp)
    constants = []
    functions = []
    for poss_pre in pred_str:
        if is_constant(poss_pre):
            constants.append(inp)
        else:
            functions.append(get_predicate(poss_pre))
    return functions


f = open("input.txt")
data = f.readlines()
kb = []
for d in data:
    parse(d)
    kb.append(parse(d))

print(kb)
