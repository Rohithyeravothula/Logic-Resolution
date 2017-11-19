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


def bool_to_string(a):
    return list(map(lambda x: str(x).upper(), a))


def full_test(e=None):
    f=open("all_inputs.txt")
    data=f.read().split("\n\n")
    f.close()
    if e is None:
        e = len(data)
    count = 1
    for raw_case in data[-1*e:]:
        print("testing case {}".format(count))
        case = raw_case.split("\n")
        queries = int(case[0])
        ans = list(map(lambda x:x.upper(), case[-1*queries:]))
        inp = case[:-1*queries]
        f=open("input.txt", 'w')
        f.write("\n".join(inp))
        f.close()
        output = bool_to_string(main())
        if ans == output:
            print("success")
        else:
            print("fail")
            print(raw_case)
        count += 1


full_test()
