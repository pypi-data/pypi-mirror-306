import sympy
import plotmath
import numpy

from .function import function, derivative


def funksjon(f, definisjonsmengde=None):
    """Oppretter en symbolsk funksjon med innebygde metoder.

    Args:
        f (str): En streng som representerer funksjonsuttrykket.
        definisjonsmengde (tuple, valgfritt): En tuple som representerer definisjonsmengden (xmin, xmax) for plotting. Standard er `None`.

    Returns:
        function: Et funksjonsobjekt med ekstra metoder:
            - derivert(x=None, order=1): Beregner den deriverte av funksjonen.
            - faktoriser(): Faktoriserer funksjonsuttrykket.
            - utvid(): Utvider funksjonsuttrykket.
            - graf(definisjonsmengden=None): Plotter grafen funksjonen innenfor definisjonsmengden. Definisjonsmengden er valgfri og har standardverdi som [-6, 6].

    Eksempler:
        >>> from casify import *
        >>> f = funksjon("x**2 + 2*x + 1")
        >>> f(2)
        9
        >>> f.derivert()
        2*x + 2
        >>> f.faktoriser()
        (x + 1)**2
        >>> g = funksjon("(x + 1) * (x - 3)")
        >>> g.utvid()
        x**2 - 2*x - 3
        >>> g.graf() # plotter grafen til g
    """
    return function(f, domain=definisjonsmengde)


def Funksjon(f, definisjonsmengde=None):
    """Alternativ skrivemåte for `funksjon`."""
    return funksjon(f, definisjonsmengde)


def derivert(uttrykk, var="x"):
    """Regner ut den deriverte av et algebraisk uttrykk med hensyn på `x`

    Args:
        uttrykk (str): det algebraisk uttrykke som skal deriveres med hensyn på `x`.

    Returns:
        sympy.Expr: den deriverte av det algebraiske uttrykket.

    """
    return derivative(uttrykk, var)
