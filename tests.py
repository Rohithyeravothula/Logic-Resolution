from resolution import *


def test_function_parse():
    s="~F(x,y,John)"
    f=parse(s)[0]
    print(f.func)
    print(f.args)
    print(f.negation)

test_function_parse()
