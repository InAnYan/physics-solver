from physics_solver.problem import Problem
from physics_solver.types import Variable


class VariableChange:
    var: Variable
    factor: float

    def __init__(self, var: Variable, factor: float):
        self.var, self.factor = var, factor


class RelativeChangeProblem(Problem):
    y: Variable
    changes: [VariableChange]

    def __init__(self, y: Variable, changes: [VariableChange]):
        self.y, self.changes = y, changes

    def solve(self) -> float:
        raise NotImplementedError()
