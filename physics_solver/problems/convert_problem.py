from physics_solver.problem import Problem
from physics_solver.types import Quantity, Unit


class ConvertProblem(Problem):
    q: Quantity
    u: Unit

    def __init__(self, q: Quantity, u: Quantity):
        self.q, self.u = q, u

    def solve(self) -> Quantity:
        return None
