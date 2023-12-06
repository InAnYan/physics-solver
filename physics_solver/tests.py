import unittest
from abc import abstractmethod, ABC

from sympy.physics.units import kilometer, hour, meter, second, minutes, grams, centimeter

from physics_solver.formulas import Formula
from physics_solver.problem import Problem
from physics_solver.parser.problem_parser import parse_english_problem
from physics_solver.problems.compare_problem import CompareProblem, Ordering
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns import FindUnknownsProblem, GivenVariable
from physics_solver.problems.relative_change_problem import RelativeChangeProblem, VariableChange
from physics_solver.types import *


# TODO: More tests. Add all problems from txt file.


class PhysicsGenericTest(ABC):
    @abstractmethod
    def perform(self, text: str, problem: Problem, solution: object):
        raise NotImplemented()

    def test_convert_1(self):
        text = 'The car is traveling at a speed of 108 kilometers per hour. Represent this speed in meters per second.'
        problem = ConvertProblem(GivenVariable(v, 108 * kilometer / hour), meter / second)
        solution = 30 * meter / second
        self.perform(text, problem, solution)

    def test_compare_1(self):
        text = 'Which speed is greater: 10 meters per second or 10 kilometers per hour?'
        problem = CompareProblem(10 * meter / second, 10 * kilometer / hour)
        solution = Ordering.GT
        self.perform(text, problem, solution)

    def test_compare_2(self):
        text = 'Which speed is slower: 72 kilometers per hour or 24 meters per second?'
        problem = CompareProblem(72 * kilometer / hour, 24 * meter / second)
        solution = Ordering.LT
        self.perform(text, problem, solution)

    def test_relative_change_1(self):
        text = ('How many times will the speed of wave propagation increase if the wavelength increases by 3 times and '
                'the period of oscillation remains unchanged?')
        problem = RelativeChangeProblem(v, [VariableChange(lam, 3)])
        solution = 3
        self.perform(text, problem, solution)

    def test_relative_change_2(self):
        text = ('How many times will the moment of a force change if the force is increased by a factor of 8 and the '
                'arm of the force is decreased by a factor of 4.')
        problem = RelativeChangeProblem(M, [VariableChange(F, 8), VariableChange(d, 1 / 4)])
        solution = 2
        self.perform(text, problem, solution)

    def test_find_unknowns_1(self):
        text = 'The car drove for 40 minutes at a speed of 144 kilometers per hour. How far did the car travel?'
        problem = FindUnknownsProblem([GivenVariable(t, 40 * minutes), GivenVariable(v, 144 * kilometer / hour)], [S])
        solution = [Formula(S, v * t)]
        self.perform(text, problem, solution)

    def test_find_unknowns_2(self):
        text = 'What is the density of a metal, 15 grams of which have a volume of 2 cubic centimeters?'
        problem = FindUnknownsProblem([GivenVariable(m, 15 * grams), GivenVariable(V, 2 * (centimeter ** 3))], [ro])
        solution = [Formula(ro, m / V)]
        self.perform(text, problem, solution)


# noinspection PyPep8Naming
class PhysicsParsingTest(unittest.TestCase, PhysicsGenericTest):
    def perform(self, text: str, problem: Problem, solution: object):
        (parsed, _) = parse_english_problem(text)
        self.assertTrue(parsed.equals(problem))


class PhysicsSolutionTest(unittest.TestCase, PhysicsGenericTest):
    def perform(self, text: str, problem: Problem, solution: object):
        self.assertEqual(solution, problem.solve())


if __name__ == '__main__':
    unittest.main()
