from sympy.physics.units import convert_to

from physics_solver.exceptions import SolverError
from physics_solver.problem import Problem
from physics_solver.types import Unit, Quantity, GivenVariable, separate_num_and_unit


class ConvertProblem(Problem):
    given: GivenVariable
    target_unit: Unit

    def __init__(self, given: GivenVariable, target_unit: Unit):
        self.given, self.target_unit = given, target_unit

    def solve(self) -> Quantity:
        _, source_unit = separate_num_and_unit(self.given.val)
        if self.target_unit.equals(source_unit):
            return self.given.val

        res = convert_to(self.given.val, self.target_unit)
        # Notice that == operator checks for structural equality.
        if res == self.given.val:
            raise SolverError('the unit is incompatible with the given quantity')

        return res

    def equals(self, other) -> bool:
        if not isinstance(other, ConvertProblem):
            return False

        return self.given.equals(other.given) and self.target_unit.equals(other.target_unit)

    def human_str_repr(self) -> str:
        return f'Convert {self.given.val} to \\({self.target_unit}\\).'
