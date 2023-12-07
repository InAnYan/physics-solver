from __future__ import annotations

from typing import List, Optional, Set

from physics_solver.math.types import *
from physics_solver.util.functions import concat, lmap


class Formula:
    var: Variable
    expansion: Expression
    parent: Optional[Formula]
    context: Set[str]

    def __init__(self, var: Variable, expansion: Expression, **kwargs):
        self.var, self.expansion, self.parent, self.context \
            = var, expansion, kwargs.get('parent'), kwargs.get('context') if 'context' in kwargs else set([])

    def solve_for(self, var: Variable) -> Formula:
        res = sympy.solve(self.as_eq(), var)
        assert len(res) == 1
        return Formula(var, res[0],
                       parent=self, context=self.context)

    def as_eq(self) -> sympy.Eq:
        return sympy.Eq(self.var, self.expansion)

    def __str__(self) -> str:
        return f'{self.var} = {self.expansion}'

    def __repr__(self):
        return f'{self.var} = {self.expansion}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Formula):
            return False

        return self.var == other.var and self.expansion == other.expansion


def make_formulas_list(*strs: str | Tuple[str, List[str]]) -> List[Formula]:
    return lmap(make_formula, strs)


def make_formula(src_or_tuple: str | Tuple[str, List[str]]) -> Formula:
    src, context = None, None
    if isinstance(src_or_tuple, tuple):
        src, context = src_or_tuple
    else:
        src, context = src_or_tuple, []

    var, exp = parse_formula_str(src)

    return Formula(var, exp, context=set(context))


def parse_formula_str(src: str) -> Tuple[Variable, Expression]:
    var_str, exp_str = src.split('=')
    var = sympy.sympify(var_str)
    assert var.is_Symbol
    exp = sympy.sympify(exp_str)
    return var, exp
