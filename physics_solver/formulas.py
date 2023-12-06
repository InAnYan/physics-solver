from typing import List

from physics_solver.types import *
from physics_solver.util import concat, lmap


class Formula:
    var: Variable
    expansion: Expression

    # TODO: Context.

    def __init__(self, var: Variable, expansion: Expression):
        self.var, self.expansion = var, expansion

    def __str__(self) -> str:
        return f'\\({self.var} = {self.expansion}\\)'

    def __repr__(self):
        return f'{self.var} = {self.expansion}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Formula):
            return False

        return self.var == other.var and self.expansion == other.expansion


def make_formulas_list(*strs: str) -> List[Formula]:
    return concat(lmap(make_formulas, strs))


def make_formulas(src: str) -> List[Formula]:
    var_str, exp_str = src.split('=')
    var = sympy.sympify(var_str)
    exp = sympy.sympify(exp_str)
    eq = sympy.Eq(var, exp)

    res = [Formula(var, exp)]

    for s in exp.free_symbols:
        for r in sympy.solve(eq, s):
            res.append(Formula(s, r))

    return res


formulas: List[Formula] = make_formulas_list(
    "v = Symbol('S') / t",
    'v = lam / T',
    'M = F * d',
    'ro = m / V')
