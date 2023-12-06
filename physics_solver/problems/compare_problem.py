from __future__ import annotations

from enum import Enum, auto

from sympy.physics.units import convert_to

from physics_solver.exceptions import SolverError
from physics_solver.problem import Problem
from physics_solver.types import Quantity, separate_num_and_unit, GivenVariable


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
    x: GivenVariable
    y: GivenVariable

    # We store GivenVariable there instead of just Quantity for StringSolution.

    def __init__(self, x: GivenVariable, y: GivenVariable):
        self.x, self.y = x, y

    def solve(self) -> Ordering:
        x_num, x_unit = separate_num_and_unit(self.x.value)
        y_num, y_unit = separate_num_and_unit(self.y.value)
        if x_unit.equals(y_unit):
            return Ordering.make(x_num, y_num)
        else:
            y2_num, y2_unit = separate_num_and_unit(convert_to(self.y.value, x_unit))
            if y2_unit.equals(y_unit):
                raise SolverError('the units are incompatible')
            return Ordering.make(x_num, y2_num)

    def __eq__(self, other) -> bool:
        if not isinstance(other, CompareProblem):
            return False

        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f'Compare two quantities: \\({self.x.value}\\) and \\({self.y.value}\\).'

    def __repr__(self) -> str:
        return f'Compare two quantities: {self.x.value} and {self.y.value}.'
