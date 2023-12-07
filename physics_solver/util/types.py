from typing import Tuple

import sympy.physics

Expression = sympy.Expr
Number = sympy.Number
Value = sympy.physics.units.quantities.Quantity
Unit = Value  # That is SymPy peculiarity.
Variable = sympy.Symbol


def separate_num_and_unit(q: Value) -> Tuple[Number, Unit]:
    return q.as_coeff_Mul()


class GivenVariable:
    variable: Variable
    value: Value

    def __init__(self, var: Variable, val: Value):
        self.variable, self.value = var, val

    def __eq__(self, other) -> bool:
        if not isinstance(other, GivenVariable):
            return False

        return self.variable == other.variable and self.value == other.value

    def __str__(self) -> str:
        return f'\\({self.variable} = {quantity_to_latex(self.value)}\\)'

    def __repr__(self) -> str:
        return f'{self.variable} = {self.value}'

    def to_tuple(self) -> Tuple[Variable, Value]:
        return self.variable, self.value


lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, p, D \
    = sympy.symbols('lam M F l t v S ro m V d P c R I B E h T nu A p D')


revolution = Value('revolution', abbrev='rev')


def quantity_to_latex(q: Value) -> str:
    num, unit = q.as_coeff_Mul()
    return f'{float(num):g} \\; {unit_to_latex(unit)}'


def unit_to_latex(q: Unit) -> str:
    return f'{sympy.latex(q.replace(lambda e: isinstance(e, Value), lambda e: e.abbrev))}'.replace('frac', 'dfrac')
