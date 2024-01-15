from dataclasses import dataclass
from typing import Optional, Tuple

import sympy
from sympy import UnevaluatedExpr, Symbol

from physics_solver.util import formula_gps
from physics_solver.math.formula import Formula
from physics_solver.math.formulas import formulas
from physics_solver.problems.problem import Problem
from physics_solver.types.string_solution import StringSolution
from physics_solver.types.variable_change import VariableChange
from physics_solver.util.exceptions import SolverError
from physics_solver.util.printing import fraction


@dataclass(frozen=True)
class RelativeChangeProblem(Problem):
    y: Symbol
    changes: [VariableChange]

    def solve(self) -> Tuple[float, Formula]:
        changes_set = set(map(lambda c: c.variable, self.changes))
        for formula in formula_gps.applicable_formulas(formula_gps.Configuration(formulas, set([])), self.y):
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

    def solve_and_make_string_solution(self) -> StringSolution:
        solution = self.solve()
        (num, formula) = solution

        givens = []
        for change in self.changes:
            givens.append(f'\\({change.variable}_2 = {change.factor}{change.variable}_1\\)')

        unknowns = [f'\\({self.y}_2 / {self.y}_1 - ?\\)']

        step1 = fraction(str(self.y) + '_2', str(self.y) + '_1')

        first_subs = formula.expansion.subs([(c.variable, Sybmol(str(c.variable) + '_1')) for c in self.changes])

        second_subs = formula.expansion.subs([(c.variable, Symbol(str(c.variable) + '_2')) for c in self.changes])

        step2 = fraction(second_subs, first_subs)

        second_subs_change = formula.expansion.subs(
            [(c.variable, UnevaluatedExpr(c.factor * Symbol(c.variable.__str__() + '_1'))) for c in self.changes])
        step3 = fraction(second_subs_change, first_subs)

        steps = [f"\\({step1} = {step2} = {step3} = {num}\\)"]

        if num < 1:
            answer = f'the variable will decrease by a factor of {1 / num}'
        elif num == 1:
            answer = 'the variable will not change'
        else:
            answer = f'the variable will increase by a factor of {num}'

        return StringSolution(givens, unknowns, steps, answer)
