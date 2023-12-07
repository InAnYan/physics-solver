from typing import Optional, Tuple

import sympy

from physics_solver.formula_gps.formula import Formula
from physics_solver.formula_gps.formulas import formulas
from physics_solver.util.exceptions import SolverError
from physics_solver.problems.problem import Problem
from physics_solver.math.types import Variable, Number


class VariableChange:
    variable: Variable
    factor: Number

    def __init__(self, var: Variable, factor: Number):
        self.variable, self.factor = var, factor

    def __eq__(self, other) -> bool:
        if not isinstance(other, VariableChange):
            return False

        return self.variable == other.variable and self.factor == other.factor

    def __str__(self) -> str:
        return f'\\({self.variable}\\) is changed by factor of \\({self.factor}\\)'

    def __repr__(self) -> str:
        return f'{self.variable} is changed by factor of {self.factor}'


class RelativeChangeProblem(Problem):
    y: Variable
    changes: [VariableChange]

    def __init__(self, y: Variable, changes: [VariableChange]):
        self.y, self.changes = y, changes

    def solve(self) -> Tuple[float, Formula]:
        changes_set = set(map(lambda c: c.variable, self.changes))
        for formula in formulas:
            if changes_set.issubset(formula.expansion.free_symbols):
                res = self.solve_by_formula(formula)
                if res:
                    return res, formula

        raise SolverError('could not find necessary formula')

    def solve_by_formula(self, formula: Formula) -> Optional[float]:
        e1 = formula.expansion
        e2 = formula.expansion.subs(map(lambda c: (c.variable, c.factor * c.variable), self.changes))
        expr = sympy.simplify(e2 / e1)
        return float(expr) if expr.is_Number else None

    def __eq__(self, other) -> bool:
        if not isinstance(other, RelativeChangeProblem):
            return False

        return self.y == other.y and self.changes == other.changes

    def __str__(self) -> str:
        return f'How \\({self.y}\\) would change if {", ".join(map(lambda x: x.__str__(), self.changes))}.'

    def __repr__(self) -> str:
        return f'How {self.y} would change if {", ".join(map(lambda x: x.__repr__(), self.changes))}.'
