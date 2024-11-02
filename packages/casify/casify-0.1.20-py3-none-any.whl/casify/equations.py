import sympy
import re
import sys


def get_func(expr):
    match = re.match(r"(\w+)\((-?\w+|-?\d+)\)", expr.strip())
    if match:
        func_name, arg = match.groups()
        return func_name, arg
    else:
        return False, False


def handle_expression(expr):
    func_name, arg = get_func(expr)
    if func_name:
        main_module = sys.modules["__main__"]
        main_globals = main_module.__dict__
        func = main_globals.get(func_name)

        return func(arg)
    else:
        return sympy.sympify(expr)


def solve(*equations, numerical=False, pprint=True):
    eqs = []
    # Parse the equations
    for eq in equations:
        if ">" in eq or "<" in eq or ">=" in eq or "<=" in eq:
            return solve_inequality(eq)
        elif "==" in eq:
            lhs, rhs = eq.split("==")
            lhs = handle_expression(lhs)
            rhs = handle_expression(rhs)

            eqs.append(sympy.Eq(lhs, rhs))

        elif "=" in eq:
            lhs, rhs = eq.split("=")
            lhs = handle_expression(lhs)
            rhs = handle_expression(rhs)

            eqs.append(sympy.Eq(lhs, rhs))

    if numerical:
        solutions = sympy.nsolve(eqs)
    else:
        solutions = sympy.solve(eqs)

    # Remove complex solutions from the solution set.
    real_solutions = []
    if isinstance(solutions, dict):
        real_solutions = {
            key: solutions.get(key) for key in solutions if solutions.get(key).is_real
        }
        real_solutions = [real_solutions]
    else:
        for sol in solutions:
            if not False in [sol.get(key).is_real for key in sol]:
                real_solutions.append(sol)

    if real_solutions == [] or real_solutions == {}:
        return "No solution"

    elif pprint:
        pprint_solution = ""
        for i, sol in enumerate(real_solutions):
            pprint_solution += (
                str(sol)
                .replace(":", " =")
                .replace("{", "")
                .replace("}", "")
                .replace(",", " ∧")
            )
            if i < len(real_solutions) - 1:
                pprint_solution += "    ∨    "

        return pprint_solution
    else:
        return real_solutions


def løs(*likninger, numerisk=False, pprint=True):
    løsning = solve(*likninger, numerical=numerisk, pprint=pprint)
    if løsning == "No solution":
        return "Ingen løsning"
    else:
        return løsning


def Løs(*likninger, numerisk=False, pprint=True):
    return løs(*likninger, numerisk=numerisk, pprint=pprint)


def Solve(*equations, numerical=False, pprint=True):
    return solve(*equations, numerical=numerical, pprint=pprint)


def solve_inequality(expr):
    solution = sympy.solve(expr)
    solution = str(solution)
    solution = solution.replace("|", " ∨ ").replace("&", " ∧ ")
    return solution
