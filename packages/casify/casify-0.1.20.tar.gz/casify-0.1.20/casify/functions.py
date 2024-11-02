import sympy
import plotmath
import numpy


def function(f, domain=None):
    f_expr = sympy.sympify(f)

    def func(x):
        return f_expr.subs("x", x)

    # Derivative function
    def derivative(x=None, order=1):
        if x is not None:
            return sympy.diff(f_expr, "x", order).subs("x", x)
        else:
            return sympy.diff(f_expr, "x", order)

    func.derivative = derivative  # Attach the derivative function
    func.derivert = derivative

    def factor():
        return sympy.factor(f_expr)

    func.factor = factor
    func.faktoriser = factor

    def expand():
        return sympy.expand(f_expr)

    func.expand = expand
    func.utvid = expand

    def plot(domain=domain):
        numpy_func = sympy.lambdify("x", f_expr, "numpy")
        if domain is not None:
            xmin, xmax = domain
            x_vals = numpy.linspace(xmin, xmax, 1024)
            codomain = (numpy.min(numpy_func(x_vals)), numpy.max(numpy_func(x_vals)))
            ymin, ymax = codomain
            ymin = int(ymin - 1)
            ymax = int(ymax + 1)
        else:
            xmin, xmax = (-6, 6)
            ymin, ymax = (-6, 6)
        plotmath.plot(
            functions=[numpy_func],
            fn_labels=None,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
        )
        plotmath.show()

    func.graf = plot
    func.graph = plot

    return func


def funksjon(f):
    return function(f)


def Funksjon(f):
    return funksjon(f)


def Function(f):
    return function(f)


def derivative(expr, var="x"):
    expr = sympy.sympify(expr)
    return sympy.diff(expr, sympy.symbols(var))


def derivert(expr, var="x"):
    return derivative(expr, var)


def integral(expr, var="x"):
    expr = sympy.sympify(expr)
    return sympy.integrate(expr, sympy.symbols(var))
