from typing import Set, List

from physics_solver.formula_gps.applicable_formulas import applicable_formulas
from physics_solver.formula_gps.configuration import FormulaGPSConfiguration
from physics_solver.formula_gps.formula import Formula
from physics_solver.formula_gps.intermediate_result import IntermediateResult
from physics_solver.formula_gps.stop import FormulaGPSStop
from physics_solver.math.types import Variable


class FormulaGPS:
    conf: FormulaGPSConfiguration

    def __init__(self, conf: FormulaGPSConfiguration):
        self.conf = conf

    def find(self, state: Set[Variable], goals: Set[Variable]) -> List[Formula]:
        return self.achieve_all(state, goals, [])[1]

    def achieve_all(self, state: Set[Variable], goals: Set[Variable], stack: List[Variable]) -> IntermediateResult:
        res = []

        for goal in goals:
            (_, actions) = self.achieve(state, goal, stack)
            res += actions

        return state, res

    def achieve(self, state: Set[Variable], goal: Variable, stack: List[Variable]) -> IntermediateResult:
        if goal in state:
            return state, []

        if goal in stack:
            raise FormulaGPSStop()

        for formula in applicable_formulas(self.conf, goal):
            unknowns = formula.expansion.free_symbols.difference(state)
            try:
                (new_state, actions) = self.achieve_all(state, unknowns, stack + [goal])
                return new_state, actions + [formula]
            except FormulaGPSStop:
                pass

        raise FormulaGPSStop()
