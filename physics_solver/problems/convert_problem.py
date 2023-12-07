from sympy.physics.units import convert_to

from physics_solver.util.exceptions import SolverError
from physics_solver.problems.problem import Problem
from physics_solver.util.types import Unit, GivenVariable, separate_num_and_unit, quantity_to_latex, unit_to_latex, Value


class ConvertProblem(Problem):
    given: GivenVariable
    target_unit: Unit

    def __init__(self, given: GivenVariable, target_unit: Unit):
        self.given, self.target_unit = given, target_unit

    def solve(self) -> Value:
        _, source_unit = separate_num_and_unit(self.given.value)
        if self.target_unit.equals(source_unit):
            return self.given.value

        res = convert_to(self.given.value, self.target_unit)
        # Notice that == operator checks for structural equality.
        if res == self.given.value:
            raise SolverError('the unit is incompatible with the given quantity')

        return res

    def __eq__(self, other) -> bool:
        if not isinstance(other, ConvertProblem):
            return False

        return self.given == other.given and self.target_unit == other.target_unit

    def __str__(self) -> str:
        return f'Convert {quantity_to_latex(self.given.value)} to \\({unit_to_latex(self.target_unit)}\\).'

    def __repr__(self) -> str:
        return f'Convert {self.given.value} to {self.target_unit}.'
