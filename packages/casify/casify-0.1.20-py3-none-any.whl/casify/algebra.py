import sympy


def factor(expr):
    expr = sympy.sympify(expr)
    return sympy.factor(expr)


def expand(expr):
    expr = sympy.sympify(expr)
    return sympy.expand(expr)


def faktoriser(uttrykk):
    return factor(uttrykk)


def utvid(uttrykk):
    return expand(uttrykk)


def Faktoriser(uttrykk):
    return factor(uttrykk)


def Utvid(uttrykk):
    return expand(uttrykk)
