import sympy
import plotmath
import numpy


def function(f, domain=None):
    """Creates a symbolic function with additional capabilities.

    Args:
        f (str): A string representing the function expression.
        domain (tuple, optional): A tuple representing the domain (xmin, xmax) for plotting. Defaults to None.

    Returns:
        function: A function object with additional methods:
            - derivative(x=None, order=1): Computes the derivative of the function.
            - factor(): Factors the function expression.
            - expand(): Expands the function expression.
            - plot(domain=domain): Plots the function within the specified domain.

    Examples:
        >>> from casify import *
        >>> f = function("x**2 + 2*x + 1")
        >>> f(2)
        9
        >>> f.derivative()
        2*x + 2
        >>> f.factor()
        (x + 1)**2
        >>> g = function("(x + 1) * (x - 3)")
        >>> g.expand()
        x**2 - 2*x - 3
        >>> g.graph() # displays the graph of the function
    """
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
            ymin, ymax = domain
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


def Function(f, domain=None):
    """Alternative way to write `function`"""
    return function(f, domain)


def derivative(expr, var="x"):
    """Computes the derivative of an algebraic expression with respect to `x`.

    Args:
        expr (str): the algebraic expression to differentiate with respect to `x`.

    Returns:
        sympy.Expr: the derivative of the algebraic expression

    """
    expr = sympy.sympify(expr)
    return sympy.diff(expr, sympy.symbols(var))
