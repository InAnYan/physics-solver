import operator
from typing import List, Tuple, Set

import sympy

from physics_solver.exceptions import SolverError
from physics_solver.formulas import Formula, formulas
from physics_solver.problem import Problem
from physics_solver.types import *
from physics_solver.util import are_lists_equal


class FindUnknownsProblem(Problem):
    givens: List[GivenVariable]
    unknowns: List[Variable]

    def __init__(self, givens: List[GivenVariable], unknowns: List[Variable]):
        self.givens, self.unknowns = givens, unknowns

    def solve(self) -> List[Formula]:
        givens_set = set(map(lambda g: g.var, self.givens))
        try:
            return formula_gps(givens_set, set(self.unknowns))
        except FormulaGPSStop:
            raise SolverError('could not find unknowns')

    def equals(self, other) -> bool:
        if not isinstance(other, FindUnknownsProblem):
            return False

        return (are_lists_equal(self.givens, other.givens) and
                are_lists_equal(self.unknowns, other.unknowns, operator.eq))

    def human_str_repr(self) -> str:
        givens_str = f'[{", ".join(map(lambda x: x.human_str_repr(), self.unknowns))}]'
        unknowns_str = f'[{", ".join(map(lambda x: x.human_str_repr(), self.givens))}]'
        return f'Find {givens_str} if {unknowns_str}.'


class FormulaGPSStop(Exception):
    pass


def formula_gps(state: Set[Variable], goals: Set[Variable]) -> List[Formula]:
    # TODO: Recursive subgoal problem.
    return achieve_all(state, goals)[1]


def achieve_all(state: Set[Variable], goals: Set[Variable]) -> Tuple[Set[Variable], List[Formula]]:
    res = []

    for goal in goals:
        (state, actions) = achieve(state, goal)
        res += actions

    return state, res


def achieve(state: Set[Variable], goal: Variable) -> Tuple[Set[Variable], List[Formula]]:
    if goal in state:
        return state, []

    for formula in formulas:
        if formula.var == goal:
            unknowns = formula.expansion.free_symbols.difference(state)
            try:
                (new_state, actions) = achieve_all(state, unknowns)
                return new_state, actions + [formula]
            except FormulaGPSStop:
                pass

    raise FormulaGPSStop()
