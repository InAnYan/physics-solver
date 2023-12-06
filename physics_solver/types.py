from typing import Tuple

import sympy
import sympy.physics
from sympy import Number

Expression = sympy.Expr
Number = sympy.Number
Quantity = sympy.physics.units.quantities.Quantity
Unit = Quantity  # That is SymPy peculiarity.
Variable = sympy.Symbol


def separate_num_and_unit(q: Quantity) -> Tuple[Number, Unit]:
    # TODO: Types don't match. Possible bug.
    return q.as_coeff_Mul()


class GivenVariable:
    var: Variable
    val: Quantity

    def __init__(self, var: Variable, val: Quantity):
        self.var, self.val = var, val

    def equals(self, other) -> bool:
        if not isinstance(other, GivenVariable):
            return False

        return self.var.equals(other.var) and self.val.equals(other.val)

    def human_str_repr(self) -> str:
        # TODO: Proper quantity printing.
        return f'\\({self.var} = {self.val}\\)'


lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, h, p, D \
    = sympy.symbols('lam M F l t v S ro m V d P c R I B E h T nu A h p D')

revolution = Quantity('revolution', abbrev='rev')
