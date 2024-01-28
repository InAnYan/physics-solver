from dataclasses import dataclass

from sympy.physics.units import convert_to, Unit

from physics_solver.math.types import *
from physics_solver.problems.problem import Problem
from physics_solver.the_types.given_variable import GivenVariable
from physics_solver.the_types.string_solution import StringSolution
from physics_solver.util.exceptions import SolverError
from physics_solver.util.printing import quantity_to_latex, unit_to_latex


@dataclass(frozen=True)
class ConvertProblem(Problem):
    given: GivenVariable
    target_unit: Unit

    def solve(self) -> Quantity:
        _, source_unit = separate_num_and_unit(self.given.value)
        if self.target_unit.equals(source_unit):
            return self.given.value

        res = convert_to(self.given.value, self.target_unit)
        # Notice that == operator checks for structural equality.
        if res == self.given.value:
            raise SolverError('the unit is incompatible with the given quantity')

        return res

    def solve_and_make_string_solution(self) -> StringSolution:
        solution = self.solve()

        givens = [self.given.__str__()]

        unknowns = [f'\\({self.given.variable}({unit_to_latex(self.target_unit)}) - ?\\)']

        steps = [f'\\({self.given.variable} = {quantity_to_latex(self.given.value)} = {quantity_to_latex(solution)}\\)']

        answer = f'\\({quantity_to_latex(solution)}\\)'

        return StringSolution(givens, unknowns, steps, answer)
