from homework3 import *


def function_parse():
    """
    ~F(x,y,John)
    :return:
    """

    s="G(Albert, z, John)"
    f=parse(s)[0]
    print(f.func)
    print(f.args)
    print(f.negation)


def function_is_constant():
    s="John"
    t="x"
    print(is_constant(s))
    print(is_constant(t))
    print(is_variable(s))
    print(is_variable(t))


def function_unification(e=None):
    f=open("unification_tests.txt", 'r')
    data=f.read().split("\n\n")
    if e is None:
        e=len(data)
    for d in data[0:e]:
        x,y = d.split('\n')
        x = parse(x).predicates[0]
        y = parse(y).predicates[0]
        print(x, y)
        print(unification(x, y, {}))

# def function_equality():
inp="H(John) | G(John)"
s1 = parse(inp)
s2 = parse(inp)

# print(s1, s2)
visited = {str(get_ordered_sentence(s1))}
print(str(get_ordered_sentence(s2)) in visited)
# print(s1 == s2)
# p = s1.predicates
# print(p.sort())


def methods():
    # function_is_constant()
    # function_parse()
    function_unification(1)
# methods()
# print(is_variable("Joe"))
# print(isinstance(Variable("Joe"), Constant))

