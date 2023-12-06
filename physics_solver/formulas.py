from typing import List

from physics_solver.types import *


class Formula:
    var: Variable
    expansion: Expression
    # TODO: Context.

    def __init__(self, var: Variable, expansion: Expression):
        self.var, self.expansion = var, expansion


# TODO: Formulas list.
formulas: List[Formula] = [Formula(v, S/t)]
