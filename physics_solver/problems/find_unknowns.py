from typing import List, Set

from physics_solver.exceptions import SolverError
from physics_solver.formulas import Formula, formulas
from physics_solver.problem import Problem
from physics_solver.types import *


class FindUnknownsProblem(Problem):
    givens: List[GivenVariable]
    unknowns: List[Variable]

    def __init__(self, givens: List[GivenVariable], unknowns: List[Variable]):
        self.givens, self.unknowns = givens, unknowns

    def solve(self) -> List[Formula]:
        givens_set = set(map(lambda g: g.variable, self.givens))
        try:
            return formula_gps(givens_set, set(self.unknowns))
        except FormulaGPSStop:
            raise SolverError('could not find unknowns')

    def __eq__(self, other) -> bool:
        if not isinstance(other, FindUnknownsProblem):
            return False

        return self.givens == other.givens and self.unknowns == other.unknowns

    def __str__(self) -> str:
        givens_str = f'[{", ".join(map(lambda x: x.__str__(), self.unknowns))}]'
        unknowns_str = f'[{", ".join(map(lambda x: x.__str__(), self.givens))}]'
        return f'Find {givens_str} if {unknowns_str}.'

    def __repr__(self) -> str:
        givens_str = f'[{", ".join(map(lambda x: x.__repr__(), self.unknowns))}]'
        unknowns_str = f'[{", ".join(map(lambda x: x.__repr__(), self.givens))}]'
        return f'Find {givens_str} if {unknowns_str}.'


class FormulaGPSStop(Exception):
    pass


def formula_gps(state: Set[Variable], goals: Set[Variable]) -> List[Formula]:
    return achieve_all(state, goals, [])[1]


def achieve_all(state: Set[Variable], goals: Set[Variable], stack: List[Variable]) -> Tuple[
    Set[Variable], List[Formula]]:
    res = []

    for goal in goals:
        (state, actions) = achieve(state, goal, stack)
        res += actions

    return state, res


def achieve(state: Set[Variable], goal: Variable, stack: List[Variable]) -> Tuple[Set[Variable], List[Formula]]:
    if goal in state:
        return state, []

    if goal in stack:
        raise FormulaGPSStop()

    for formula in formulas:
        if formula.var == goal:
            unknowns = formula.expansion.free_symbols.difference(state)
            try:
                (new_state, actions) = achieve_all(state, unknowns, stack + [goal])
                return new_state, actions + [formula]
            except FormulaGPSStop:
                pass

    raise FormulaGPSStop()
