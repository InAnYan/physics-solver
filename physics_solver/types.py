from typing import Tuple

import sympy.physics

Expression = sympy.Expr
Number = sympy.Number
Quantity = sympy.physics.units.quantities.Quantity
Unit = Quantity  # That is SymPy peculiarity.
Variable = sympy.Symbol


def separate_num_and_unit(q: Quantity) -> Tuple[Number, Unit]:
    return q.as_coeff_Mul()


class GivenVariable:
    variable: Variable
    value: Quantity

    def __init__(self, var: Variable, val: Quantity):
        self.variable, self.value = var, val

    def __eq__(self, other) -> bool:
        if not isinstance(other, GivenVariable):
            return False

        return self.variable == other.variable and self.value == other.value

    def __str__(self) -> str:
        return f'\\({self.variable} = {self.value}\\)'

    def __repr__(self) -> str:
        return f'{self.variable} = {self.value}'


lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, p, D \
    = sympy.symbols('lam M F l t v S ro m V d P c R I B E h T nu A p D')


revolution = Quantity('revolution', abbrev='rev')
