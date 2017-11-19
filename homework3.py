import re
import copy
from collections import deque
import time

# ToDo: make sure this is 60
time_limit = 1*60 # 1 minute of each query


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
        if other is not None:
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return str.__hash__(str(self))

    def negate(self):
        self.negation = not self.negation


class Sentence:
    def __init__(self, predicates):
        """
        :param predicates: list of functions only
        """
        self.predicates = predicates

    def __str__(self):
        return str(self.predicates)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return str.__hash__(str(self))


"""
functions table => 
key = function
val =>
 sentences where function is positive
 sentences where function is negative

while choosing to resolve choose function with minimum variables
"""


class TableValues():
    def __init__(self, positives, negatives):
        self.positives = positives
        self.negatives = negatives


class KB:
    def __init__(self, sentences):
        self.sentences = sentences
        self.kb = {}
        for sent in self.sentences:
            for func in sent.predicates:
                if func.func in self.kb:
                    if func.negation:
                        self.kb[func.func].negatives.append(sent)
                    else:
                        self.kb[func.func].positives.append(sent)
                else:
                    if func.negation:
                        self.kb[func.func] = TableValues([], [sent])
                    else:
                        self.kb[func.func] = TableValues([sent], [])

    def __str__(self):
        return str(self.kb)

    def __repr__(self):
        return str(self)

    def print_kb(self):
        for k in self.kb:
            print(k)
            positives = self.kb[k].positives
            negatives = self.kb[k].negatives
            print("positives")
            for p in positives:
                print("\t {}".format(p))
            print("negatives")
            for n in negatives:
                print("\t {}".format(n))

    def tell(self, sentence):
        # print("sentence {}".format(sentence))
        for func in sentence.predicates:
            if func.func in self.kb:
                if func.negation:
                    self.kb[func.func].negatives.append(sentence)
                else:
                    self.kb[func.func].positives.append(sentence)
            else:
                if func.negation:
                    self.kb[func.func] = TableValues([], [sentence])
                else:
                    self.kb[func.func] = TableValues([sentence], [])

    def ask(self, query):
        pass


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
    l = len(inp_list)
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
    return Sentence(functions)


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
    elif x == y:  # ToDo: define comparision for classes
        return z
    elif x.__class__ == Constant and y.__class__ == Constant and x != y:
        return None
    elif x.__class__ == Variable:
        return unify_variable(x, y, z)
    elif y.__class__ == Variable:
        return unify_variable(y, x, z)
    elif x.__class__ == Function and y.__class__ == Function:
        return unification(x.args, y.args, unification(x.func, y.func, z))
    elif isinstance(x, list) and isinstance(y, list):
        return unification(x[1:], y[1:], unification(x[0], y[0], z))
    else:
        return None


def build_predicates():
    f = open("input.txt")
    data = f.readlines()
    f.close()

    queries = []
    query_count = int(data[0])
    query_strings = data[1:query_count + 1]
    for q in query_strings:
        queries.append(parse(q))

    kb = []
    kb_strings = data[query_count + 2:]
    for k in kb_strings:
        kb.append(parse(k))

    return queries, kb


def search_resolver(kb, func, negation):
    """
    :param kb: knowledgebase
    :param func: function variable
    :param negation: search for negation
    :return: all resolvers
    """
    for k in kb:
        if k == func:
            if negation:
                return kb[k].negatives
            return kb[k].positives


def substitute(predicates, substitution):
    """
    :param predicates: list of predicates/Functions
    :param substitution: map of variable to value
    :return: substituted predicates
    """
    subs_functions = []
    # print("substitution: {}".format(substitution), predicates)
    for funks in predicates:
        subs_args = []
        for var in funks.args:
            if var in substitution:
                subs_args.append(substitution[var])
            else:
                subs_args.append(var)
        subs_functions.append(Function(funks.func, subs_args, funks.negation))
    return subs_functions


# def divide_function(sentence, left_func):
#     # print("hello", sentence, left_func)
#     func = []
#     y = None
#     count = 0
#     for i in sentence.predicates:
#         if i.func == left_func.func and i.negation != left_func.negation and count == 0:
#             y = i
#             count += 1
#         else:
#             func.append(i)
#     return y, func


def reduce_cycles(substitution):
    if substitution is not None:
        count = 1
        cycle_limit = 100
        while count < cycle_limit:
            exists = False
            for k in substitution:
                if substitution[k] in substitution:
                    substitution[k] = substitution[substitution[k]]
                    exists = True
            if not exists:
                break


def pick_next(stack):
    if len(stack) == 0:
        return None
    min_args = len(stack[0])
    min_res = 0
    stack_length = len(stack)
    for i in range(0, stack_length):
        # ToDo: fix this
        if min_args > len(stack[i]):
            min_args = len(stack[i])
            min_res = i
    r = stack[min_res]
    # print(stack, min_res)
    del stack[min_res]
    return r


def get_ordered_sentence(sentence):
    pred = copy.deepcopy(sentence.predicates)
    # print(pred)
    pred = sorted(pred, key=lambda x: str(x))
    return Sentence(pred)


def resolve(question, knowledgebase):
    query_predicate = question.predicates[0]
    query_predicate.negate()
    knowledgebase.tell(Sentence(question.predicates))
    resolution_queue = deque([question.predicates])  # stack contains predicates in list form and not sentence form
    visited = {str(question)}
    ans = False
    iteration = 0
    iteration_limit = 4000
    start_time = time.time()
    while len(resolution_queue) != 0 and iteration < iteration_limit:
        if time.time() - start_time >= time_limit:
            break
        # if iteration % 10 == 0:
        #     print("done {} iterations".format(iteration))
        iteration += 1
        current = pick_next(resolution_queue)
        # unif_x, x_rest = current[0], current[1:]
        current_length = len(current)
        for i in range(0, current_length):

            unif_x = current[i]
            x_rest = current[0:i] + current[i + 1:]

            resolve_sentences = search_resolver(knowledgebase.kb, unif_x.func, not unif_x.negation)
            # print("knowledgebase: {}".format(knowledgebase))
            # print("resolution sentences: {}".format(resolve_sentences))
            for resolver in resolve_sentences:

                resolver_predicates = resolver.predicates
                resolver_length = len(resolver_predicates)
                for resolver_index in range(0, resolver_length):
                    if resolver_predicates[resolver_index].func == unif_x.func and resolver_predicates[resolver_index].negation != unif_x.negation:
                        unif_y = resolver_predicates[resolver_index]
                        y_rest = resolver_predicates[0:resolver_index] + resolver_predicates[resolver_index+1:resolver_length]

                        # unif_y, y_rest = divide_function(resolver, unif_x)
                        substitution = unification(unif_x, unif_y, {})
                        reduce_cycles(substitution)
                        # print("unification: {} {} {} {} {}".format(current, resolver, unif_x, unif_y, substitution))
                        if substitution is not None and len(x_rest) == 0 and len(y_rest) == 0:
                            ans = True
                            break
                        elif substitution is not None:
                            resolved = substitute(list(set(x_rest + y_rest)), substitution)
                            # print("resolved: {}".format(resolved))
                            resolved_sentence = Sentence(resolved)
                            resolved_sentence_str = str(get_ordered_sentence(resolved_sentence))
                            if resolved_sentence_str not in visited:
                                resolution_queue.append(resolved)
                                knowledgebase.tell(resolved_sentence)
                                visited.add(resolved_sentence_str)
                                # else:
                                #     print("<<<<<<<<<<<< found in visited {}".format(resolved_sentence))
                                # print("current stack: {} ".format(resolution_queue))
                                # print("current visited: {}".format(visited))
                    if ans:
                        break
            if ans:
                break
        if ans:
            break
            # print(len(resolution_queue), iteration)
            # print("\n\n")
    # print("ans found: {}".format(ans)
    return ans


def write_output(answers):
    f = open("output.txt", 'w')
    s = ""
    for a in answers:
        if a:
            s += "TRUE\n"
        else:
            s += "FALSE\n"
    s = s[:-1]
    f.write(s)
    f.close()


def main():
    query_predicates, kb_sentences = build_predicates()
    kb = KB(kb_sentences)
    # kb.print_kb()
    answers = []
    for query in query_predicates:
        try:
            kb_copy = copy.deepcopy(kb)
            # print(query)
            answers.append(resolve(query, kb_copy))
        except:
            answers.append(False)
    write_output(answers)
    # print(answers)
    return answers


if __name__ == '__main__':
    main()


# ToDo: check test case where ans is masked inside the KB
