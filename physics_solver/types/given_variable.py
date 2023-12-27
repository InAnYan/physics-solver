from dataclasses import dataclass
from typing import Tuple

from sympy import UnevaluatedExpr, Symbol

from physics_solver.math.types import *
from physics_solver.util.printing import quantity_to_latex


@dataclass(frozen=True)
class GivenVariable:
    variable: Symbol
    value: Quantity

    def __str__(self) -> str:
        return f'\\({self.variable} = {quantity_to_latex(self.value)}\\)'

    def to_tuple(self) -> Tuple[Symbol, Quantity]:
        return self.variable, UnevaluatedExpr(self.value)
