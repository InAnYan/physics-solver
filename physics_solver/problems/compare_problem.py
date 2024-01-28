from dataclasses import dataclass

from sympy.physics.units import convert_to

from physics_solver.math.types import separate_num_and_unit
from physics_solver.problems.problem import Problem
from physics_solver.the_types.given_variable import GivenVariable
from physics_solver.the_types.string_solution import StringSolution
from physics_solver.util.exceptions import SolverError
from physics_solver.util.ordering import Ordering
from physics_solver.util.printing import quantity_to_latex
from physics_solver.parser.patterns import great_comparison_words


@dataclass(frozen=True)
class CompareProblem(Problem):
    x: GivenVariable
    y: GivenVariable
    word: str

    def solve(self) -> Ordering:
        x_num, x_unit = separate_num_and_unit(self.x.value)
        y_num, y_unit = separate_num_and_unit(self.y.value)
        if x_unit.equals(y_unit):
            return Ordering.make(x_num, y_num)
        else:
            y2_num, y2_unit = separate_num_and_unit(convert_to(self.y.value, x_unit))
            if y2_unit.equals(y_unit):
                raise SolverError('the units are incompatible')
            return Ordering.make(x_num, y2_num)

    def solve_and_make_string_solution(self) -> StringSolution:
        solution = self.solve()

        givens = [f'\\({self.x.variable}_1 = {quantity_to_latex(self.x.value)}\\)',
                  f'\\({self.y.variable}_2 = {quantity_to_latex(self.y.value)}\\)']

        unknowns = [f'\\({self.x.variable}_1 \\; ? \\; {self.y.variable}_2\\)']

        if separate_num_and_unit(self.x.value)[1] == separate_num_and_unit(self.y.value):
            steps = []
        else:
            steps = [
                f'\\({self.y.variable}_2 = {quantity_to_latex(self.y.value)} = {quantity_to_latex(convert_to(self.y.value, separate_num_and_unit(self.x.value)[1]))}\\)']

        if self.word in great_comparison_words:
            answer = solution.human_str_for_greater().replace('greater', self.word)
        else:
            answer = solution.human_str_for_smaller().replace('smaller', self.word)

        return StringSolution(givens, unknowns, steps, answer)
