import re


class Predicate:
    pass


class Variable(Predicate):
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return self.val

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return str.__hash__(str(self))


class Constant(Variable):
    def __init__(self, val):
        Variable.__init__(self, val)


class Function(Predicate):
    # func is a string, args are either variables or constants, and negation is boolean
    def __init__(self, func, args, negation):
        self.func = func
        self.args = args  # list of arguments could be constants or variables
        self.negation = negation

    def __str__(self):
        v = "{}({})".format(self.func, ", ".join(list(map(lambda x: str(x), self.args))))
        if self.negation:
            return "~{}".format(v)
        return v

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Sentence:
    def __init__(self, predicates):
        """
        :param predicates: list of functions only
        """
        self.predicates = predicates


class KB:
    def __init__(self, sentences):
        self.sentences = sentences
        self.constants = None
        self.variables = None
        self.func_indexes = None  # refer mid2 ppt 5 slide 7


def is_constant(inp):
    # print(inp)
    if inp[0].isupper() and "(" not in inp and ")" not in inp:
        return True
    return False


def is_variable(inp):
    if inp[0].islower() and "(" not in inp and ")" not in inp:
        return True
    return False


def strip_spaces(inp_list):
    """
    has side effect
    :param inp_list: 
    :return: 
    """
    l=len(inp_list)
    for i in range(0, l):
        inp_list[i] = inp_list[i].strip()



def get_predicate(inp):
    negation = False
    if inp[0] == "~" or inp[0] == '~':
        negation = True
        inp = inp[1:]
    brace_open = inp.index("(")
    brace_close = inp.index(")")
    func = inp[0:brace_open]
    arg_str = inp[brace_open + 1:brace_close].split(",")
    strip_spaces(arg_str)
    args = []
    for formated_string in arg_str:
        if is_constant(formated_string):
            args.append(Constant(formated_string))
        elif is_variable(formated_string):
            args.append(Variable(formated_string))
        else:
            print("unable to understand {}".format(formated_string))
    return Function(func, args, negation)


def parse(inp):
    predicates_str = re.split('\|', inp)
    strip_spaces(predicates_str)
    constants = []
    functions = []
    for formated_str in predicates_str:
        if is_constant(formated_str):
            constants.append(formated_str)
        else:
            functions.append(get_predicate(formated_str))
    return functions


def unify_variable(var, x, z):
    """
    :param var: a variable
    :param x: could be variable or constant
    :param z: substitution, a map from variable to constant substitutions
    :return: returns substitution
    """
    if var in z:
        return unification(z[var], x, z)
    elif x in z:
        return unification(var, z[x], z)
    else:
        # ToDo: implement occur check
        z[var] = x
        return z


def unification(x, y, z):
    """

    :param x: can be variable, constant, function, function name, list of arguments
    :param y: can be variable, constant, function, function name, list of arguments
    :param z: substitution set till now, a map of variable to value
    :return: returns a substitution
    """
    if z is None:
        return None
    elif x == y: # ToDo: define comparision for classes
        return z
    elif isinstance(x, Constant) and isinstance(y, Constant) and x!=y:
        return None
    elif isinstance(x, Variable):
        return unify_variable(x, y, z)
    elif isinstance(y, Variable):
        return unify_variable(y, x, z)
    elif isinstance(x, Function) and isinstance(y, Function):
        return unification(x.args, y.args, unification(x.func, y.func, z))
    elif isinstance(x, list) and isinstance(y, list):
        return unification(x[1:], y[1:], unification(x[0], y[0], z))
    else:
        return None


def main():
    f = open("input.txt")
    data = f.readlines()

    queries = []
    query_count = int(data[0])
    query_strings = data[1:query_count+1]
    for q in query_strings:
        queries.append(parse(q))

    kb=[]
    kb_strings = data[query_count+2:]
    for k in kb_strings:
        kb.append(parse(k))

    print(kb)
    print(queries)
    substution = unification(kb[0][1], kb[1][0], {})
    print(substution)



if __name__ == '__main__':
    main()
