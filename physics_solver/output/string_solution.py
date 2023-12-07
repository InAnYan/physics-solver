from typing import List, Tuple

import sympy
from sympy import Expr
from sympy.physics.units import convert_to

from physics_solver.formula_gps.formula import Formula
from physics_solver.math.types import Value, separate_num_and_unit, Variable
from physics_solver.output.printing import unit_to_latex, quantity_to_latex
from physics_solver.problems.given_variable import GivenVariable
from physics_solver.problems.problem import Problem
from physics_solver.problems.compare_problem import CompareProblem, Ordering
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns_problem import FindUnknownsProblem
from physics_solver.problems.relative_change_problem import RelativeChangeProblem
from physics_solver.util.functions import lmap


class StringSolution:
    givens: List[str]
    unknowns: List[str]
    steps: List[str]
    answer: str

    def __init__(self, problem: Problem, solution: object):
        if isinstance(problem, ConvertProblem):
            solution: Value
            self.init_convert_problem(problem, solution)
        elif isinstance(problem, CompareProblem):
            solution: Ordering
            self.init_compare_problem(problem, solution)
        elif isinstance(problem, RelativeChangeProblem):
            solution: Tuple[float, Formula]
            self.init_relative_change_problem(problem, solution)
        elif isinstance(problem, FindUnknownsProblem):
            solution: List[Formula]
            self.init_find_unknowns_problem(problem, solution)
        else:
            raise NotImplemented()

    def init_convert_problem(self, problem: ConvertProblem, solution: Value):
        self.givens = [problem.given.__str__()]
        self.unknowns = [f'\\({problem.given.variable}({unit_to_latex(problem.target_unit)}) - ?\\)']
        # TODO: Think about ConvertProblem StringSolution.steps.
        self.steps = [
            f'\\({problem.given.variable} = {quantity_to_latex(problem.given.value)} = {quantity_to_latex(solution)}\\)']
        self.answer = f'\\({quantity_to_latex(solution)}\\)'

    def init_compare_problem(self, problem: CompareProblem, solution: Ordering):
        self.givens = [f'\\({problem.x.variable}_1 = {quantity_to_latex(problem.x.value)}\\)',
                       f'\\({problem.y.variable}_2 = {quantity_to_latex(problem.y.value)}\\)']
        self.unknowns = [f'\\({problem.x.variable}_1 \\; ? \\; {problem.y.variable}_2\\)']
        if separate_num_and_unit(problem.x.value)[1] == separate_num_and_unit(problem.y.value):
            self.steps = []
        else:
            self.steps = [
                f'\\({problem.y.variable}_2 = {quantity_to_latex(problem.y.value)} = {quantity_to_latex(convert_to(problem.y.value, separate_num_and_unit(problem.x.value)[1]))}\\)']
        if solution == Ordering.EQ:
            self.answer = 'the values are equal'
        elif solution == Ordering.GT:
            self.answer = 'the first value is greater'
        else:
            self.answer = 'the second value is greater'

    def init_relative_change_problem(self, problem: RelativeChangeProblem, solution: Tuple[float, Formula]):
        (num, formula) = solution

        self.givens = []
        for change in problem.changes:
            self.givens.append(f'\\({change.variable}_2 = {change.factor}{change.variable}_1\\)')

        self.unknowns = [f'\\({problem.y}_2 / {problem.y}_1 - ?\\)']

        step1 = fraction(problem.y.__str__() + '_2', problem.y.__str__() + '_1')

        first_subs = formula.expansion.subs(lmap(lambda c: (c.variable, Variable(c.variable.__str__() + '_1')),
                                                 problem.changes))
        second_subs = formula.expansion.subs(lmap(lambda c: (c.variable, Variable(c.variable.__str__() + '_2')),
                                                  problem.changes))
        step2 = fraction(second_subs, first_subs)

        second_subs_change = formula.expansion.subs(
            lmap(lambda c: (c.variable, c.factor * Variable(c.variable.__str__() + '_1')),
                 problem.changes))
        step3 = fraction(second_subs_change, first_subs)

        self.steps = [f"\\({step1} = {step2} = {step3} = {num}\\)"]

        if num < 1:
            self.answer = f'the variable will decrease by a factor of {1 / num}'
        elif num == 1:
            self.answer = 'the variable will not change'
        else:
            self.answer = f'the variable will increase by a factor of {num}'

    def init_find_unknowns_problem(self, problem: FindUnknownsProblem, solution: List[Formula]):
        self.givens = lmap(lambda g: g.__str__(), problem.givens)

        self.unknowns = lmap(lambda u: f'\\({u} - ?\\)', problem.unknowns)

        self.steps = []
        state = problem.givens.copy()
        for formula in solution:
            value = sympy.simplify(formula.expansion.subs(lmap(lambda g: g.to_tuple(), state)))
            state.append(GivenVariable(formula.var, value))
            if formula.parent:
                self.steps.append(f'From formula \\({formula.parent}\\) derive \\({formula}\\).')
            self.steps.append(f'\\({formula} = {quantity_to_latex(value)}\\)')

        self.answer = f'\\({quantity_to_latex(state[-1].value)}\\)'


def fraction(a: str | Expr, b: str | Expr) -> str:
    res = '\\dfrac{'

    if isinstance(a, str):
        res += a
    else:
        res += sympy.latex(a)

    res += '}{'

    if isinstance(b, str):
        res += b
    else:
        res += sympy.latex(b)

    res += '}'

    return res
