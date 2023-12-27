from typing import Set, List, Tuple

from dataclasses import dataclass

from physics_solver.math.formula import Formula

from sympy import Symbol


IntermediateResult = Tuple[Set[Symbol], List[Formula]]


@dataclass
class Configuration:
    formulas: List[Formula]
    context: Set[str]


def applicable_formulas(conf: Configuration, goal: Symbol):
    for formula in conf.formulas:
        if formula.context.issubset(conf.context):
            if formula.var == goal:
                yield formula
            elif goal in formula.expansion.free_symbols:
                yield formula.solve_for(goal)


class Stop(Exception):
    pass


class GPS:
    conf: Configuration

    def __init__(self, conf: Configuration):
        self.conf = conf

    def find(self, state: Set[Symbol], goals: Set[Symbol]) -> List[Formula]:
        return self.achieve_all(state, goals, [])[1]

    def achieve_all(self, state: Set[Symbol], goals: Set[Symbol], stack: List[Symbol]) -> IntermediateResult:
        res = []

        for goal in goals:
            (_, actions) = self.achieve(state, goal, stack)
            res += actions

        return state, res

    def achieve(self, state: Set[Symbol], goal: Symbol, stack: List[Symbol]) -> IntermediateResult:
        if goal in state:
            return state, []

        if goal in stack:
            raise Stop()

        for formula in applicable_formulas(self.conf, goal):
            unknowns = formula.expansion.free_symbols.difference(state)
            try:
                (new_state, actions) = self.achieve_all(state, unknowns, stack + [goal])
                return new_state, actions + [formula]
            except Stop:
                pass

        raise Stop()
