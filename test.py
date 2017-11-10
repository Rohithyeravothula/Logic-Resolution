from resolution import *


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
        x = parse(x)[0]
        y = parse(y)[0]
        print(x, y)
        print(unification(x, y, {}))


def methods():
    # function_is_constant()
    # function_parse()
    function_unification()
methods()
# print(is_constant("John"))