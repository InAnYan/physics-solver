from typing import List, Set

from physics_solver.formula_gps.formula import Formula


class FormulaGPSConfiguration:
    formulas: List[Formula]
    context: Set[str]

    def __init__(self, formulas: List[Formula], context: Set[str]):
        self.formulas, self.context = formulas, context
