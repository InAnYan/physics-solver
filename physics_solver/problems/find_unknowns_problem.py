from dataclasses import dataclass
from typing import List

from physics_solver.util import formula_gps
from physics_solver.math.formula import Formula
from physics_solver.math.formulas import formulas
from physics_solver.problems.problem import Problem
from physics_solver.the_types.given_variable import GivenVariable
from physics_solver.the_types.string_solution import StringSolution
from physics_solver.util.exceptions import SolverError
from physics_solver.util.printing import quantity_to_latex

from sympy import Symbol
import sympy


@dataclass(frozen=True)
class FindUnknownsProblem(Problem):
    givens: List[GivenVariable]
    unknowns: List[Symbol]

    def solve(self) -> List[Formula]:
        givens_set = {g.variable for g in self.givens}
        try:
            conf = formula_gps.Configuration(formulas, self.context)
            gps = formula_gps.GPS(conf)
            return gps.find(givens_set, set(self.unknowns))
        except formula_gps.Stop:
            raise SolverError('could not find unknowns')

    def solve_and_make_string_solution(self) -> StringSolution:
        solution = self.solve()

        givens = [str(g) for g in self.givens]

        unknowns = [f'\\({u} - ?\\)' for u in self.unknowns]

        steps = []
        state = self.givens.copy()
        for formula in solution:
            int_step = formula.expansion.subs([g.to_tuple() for g in state])
            value = sympy.simplify(int_step)
            state.append(GivenVariable(formula.var, value))
            if formula.parent:
                steps.append(f'From formula \\({formula.parent}\\) derive \\({formula}\\).')
            steps.append(
                f'\\({formula} = {sympy.latex(int_step).replace("frac", "dfrac")} = {quantity_to_latex(value)}\\)')

        answer = f'\\({quantity_to_latex(state[-1].value)}\\)'

        return StringSolution(givens, unknowns, steps, answer)
