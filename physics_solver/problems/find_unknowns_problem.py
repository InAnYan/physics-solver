from typing import List

from physics_solver.formula_gps.configuration import FormulaGPSConfiguration
from physics_solver.formula_gps.formula import Formula
from physics_solver.formula_gps.formulas import formulas
from physics_solver.formula_gps.gps import FormulaGPS
from physics_solver.formula_gps.stop import FormulaGPSStop
from physics_solver.problems.given_variable import GivenVariable
from physics_solver.util.exceptions import SolverError
from physics_solver.problems.problem import Problem
from physics_solver.math.types import *


class FindUnknownsProblem(Problem):
    givens: List[GivenVariable]
    unknowns: List[Variable]

    def __init__(self, givens: List[GivenVariable], unknowns: List[Variable]):
        self.givens, self.unknowns = givens, unknowns

    def solve(self) -> List[Formula]:
        givens_set = set(map(lambda g: g.variable, self.givens))
        try:
            conf = FormulaGPSConfiguration(formulas, set([]))
            gps = FormulaGPS(conf)
            return gps.find(givens_set, set(self.unknowns))
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
