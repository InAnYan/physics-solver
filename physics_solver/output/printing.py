import sympy

from physics_solver.math.types import Value, Unit


def quantity_to_latex(q: Value) -> str:
    num, unit = q.as_coeff_Mul()
    return f'{float(num):g} \\; {unit_to_latex(unit)}'


def unit_to_latex(q: Unit) -> str:
    return f'{sympy.latex(q.replace(lambda e: isinstance(e, Value), lambda e: e.abbrev))}'.replace('frac', 'dfrac')
