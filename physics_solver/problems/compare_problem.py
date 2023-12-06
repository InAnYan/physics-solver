from __future__ import annotations

from enum import Enum, auto

from sympy.physics.units import convert_to

from physics_solver.exceptions import SolverError
from physics_solver.problem import Problem
from physics_solver.types import Quantity, separate_num_and_unit


class Ordering(Enum):
    EQ = auto()
    GT = auto()
    LT = auto()

    @staticmethod
    def make(a: object, b: object) -> Ordering:
        if a == b:
            return Ordering.EQ
        elif a > b:
            return Ordering.GT
        else:
            return Ordering.LT


class CompareProblem(Problem):
    x: Quantity
    y: Quantity

    def __init__(self, x: Quantity, y: Quantity):
        self.x, self.y = x, y

    def solve(self) -> Ordering:
        x_num, x_unit = separate_num_and_unit(self.x)
        y_num, y_unit = separate_num_and_unit(self.y)
        if x_unit.equals(y_unit):
            return Ordering.make(x_num, y_num)
        else:
            y2_num, y2_unit = separate_num_and_unit(convert_to(self.y, x_unit))
            if y2_unit.equals(y_unit):
                raise SolverError('the units are incompatible')
            return Ordering.make(x_num, y2_num)

    # TODO: Structural equality or semantic?
    def equals(self, other) -> bool:
        if not isinstance(other, CompareProblem):
            return False

        return self.x.equals(other.x) and self.y.equals(other.y)

    def human_str_repr(self) -> str:
        # TODO: Latex output.
        # TODO: Proper quantity output. Probably make quantity a custom class?
        return f'Compare two quantities: \\({self.x}\\) and \\({self.y}\\).'
