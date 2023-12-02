from typing import List

from physics_solver.problem import Problem
from physics_solver.types import Variable, Quantity, Formula


class GivenVariable:
    var: Variable
    val: Quantity

    def __init__(self, var: Variable, val: Quantity):
        self.var, self.val = var, val


class FindUnknownsProblem(Problem):
    givens: [GivenVariable]
    unknowns: [Variable]

    def __init__(self, givens: [GivenVariable], unknowns: [Variable]):
        self.givens, self.unknowns = givens, unknowns

    def solve(self) -> List[Formula]:
        raise NotImplementedError()
