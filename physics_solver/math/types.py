from typing import Tuple

import sympy.physics

Expression = sympy.Expr
Number = sympy.Number
Value = sympy.physics.units.quantities.Quantity
Unit = Value
Variable = sympy.Symbol


def separate_num_and_unit(q: Value) -> Tuple[Number, Unit]:
    return q.as_coeff_Mul()
