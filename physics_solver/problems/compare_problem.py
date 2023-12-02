from enum import Enum, auto

from physics_solver.problem import Problem
from physics_solver.types import Quantity


class Ordering(Enum):
    EQ = auto()
    GT = auto()
    LT = auto()


class CompareProblem(Problem):
    x: Quantity
    y: Quantity

    def __init__(self, x: Quantity, y: Quantity):
        self.x, self.y = x, y

    def solve(self) -> Ordering:
        raise NotImplementedError()
