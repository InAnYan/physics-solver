from physics_solver.formula_gps.configuration import FormulaGPSConfiguration
from physics_solver.math.types import Variable


def applicable_formulas(conf: FormulaGPSConfiguration, goal: Variable):
    for formula in conf.formulas:
        if formula.context.issubset(conf.context):
            if formula.var == goal:
                yield formula
            elif goal in formula.expansion.free_symbols:
                yield formula.solve_for(goal)
