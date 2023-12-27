import sympy
from sympy import Expr

from physics_solver.math.types import *


def quantity_to_latex(q: Quantity) -> str:
    num, unit = q.as_coeff_Mul()
    return f'{float(num):g} \\; {unit_to_latex(unit)}'


def unit_to_latex(q: Unit) -> str:
    return f'{sympy.latex(q.replace(lambda e: isinstance(e, SingleUnit), lambda e: e.abbrev))}'.replace('frac', 'dfrac')


def fraction(a: str | Expr, b: str | Expr) -> str:
    res = '\\dfrac{'

    if isinstance(a, str):
        res += a
    else:
        res += sympy.latex(a)

    res += '}{'

    if isinstance(b, str):
        res += b
    else:
        res += sympy.latex(b)

    res += '}'

    return res
