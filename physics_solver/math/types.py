from typing import Tuple

from sympy import Number, Expr
from sympy.physics.units import Quantity

SingleUnit = Quantity
Quantity = Expr | Quantity
Unit = Quantity


def separate_num_and_unit(q: Quantity) -> Tuple[Number, Unit]:
    return q.as_coeff_Mul()
