from physics_solver.problem import Problem
from physics_solver.types import Variable, Number
from physics_solver.util import are_lists_equal


class VariableChange:
    var: Variable
    factor: Number

    def __init__(self, var: Variable, factor: Number):
        self.var, self.factor = var, factor

    def equals(self, other) -> bool:
        if not isinstance(other, VariableChange):
            return False

        return self.var.equals(other.var) and self.factor == other.factor

    def human_str_repr(self) -> str:
        return f'\\({self.var}\\) is changed by factor of \\({self.factor}\\)'


class RelativeChangeProblem(Problem):
    y: Variable
    changes: [VariableChange]

    def __init__(self, y: Variable, changes: [VariableChange]):
        self.y, self.changes = y, changes

    def solve(self) -> float:
        raise NotImplementedError()

    def equals(self, other) -> bool:
        if not isinstance(other, RelativeChangeProblem):
            return False

        return self.y.equals(other.y) and are_lists_equal(self.changes, other.changes)

    def human_str_repr(self) -> str:
        return f'How \\({self.y}\\) would change if {", ".join(map(lambda x: x.human_str_repr(), self.changes))}.'
