import operator
from typing import List

from physics_solver.formulas import Formula
from physics_solver.problem import Problem
from physics_solver.types import Variable, GivenVariable
from physics_solver.util import are_lists_equal


class FindUnknownsProblem(Problem):
    givens: List[GivenVariable]
    unknowns: List[Variable]

    def __init__(self, givens: List[GivenVariable], unknowns: List[Variable]):
        self.givens, self.unknowns = givens, unknowns

    def solve(self) -> List[Formula]:
        raise NotImplementedError()

    def equals(self, other) -> bool:
        if not isinstance(other, FindUnknownsProblem):
            return False

        return (are_lists_equal(self.givens, other.givens) and
                are_lists_equal(self.unknowns, other.unknowns, operator.eq))

    def human_str_repr(self) -> str:
        givens_str = f'[{", ".join(map(lambda x: x.human_str_repr(), self.unknowns))}]'
        unknowns_str = f'[{", ".join(map(lambda x: x.human_str_repr(), self.givens))}]'
        return f'Find {givens_str} if {unknowns_str}.'
