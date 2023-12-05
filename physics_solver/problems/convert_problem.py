from physics_solver.problem import Problem
from physics_solver.types import Unit, Quantity, GivenVariable


class ConvertProblem(Problem):
    g: GivenVariable
    u: Unit

    def __init__(self, g: GivenVariable, u: Unit):
        self.g, self.u = g, u

    def solve(self) -> Quantity:
        # TODO: raise NotImplemented()
        return None
