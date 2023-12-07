from typing import Tuple

from physics_solver.output.printing import quantity_to_latex
from physics_solver.math.types import Variable, Value


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
