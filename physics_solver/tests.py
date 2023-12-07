import unittest
from abc import abstractmethod, ABC

from sympy import sin
from sympy.physics.units import kilometer, hour, meter, second, minutes, grams, centimeter, candela, lux, hertz, \
    kilogram, g, newton, joule

from physics_solver.formula_gps.formula import Formula
from physics_solver.math.additional_units import revolution, ton, kilojoule
from physics_solver.parser.problem_parser import recognize_entities, parse_english_document
from physics_solver.problems.given_variable import GivenVariable
from physics_solver.problems.problem import Problem
from physics_solver.problems.compare_problem import CompareProblem, Ordering
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns_problem import FindUnknownsProblem
from physics_solver.problems.relative_change_problem import RelativeChangeProblem, VariableChange
from physics_solver.math.variables import *


# TODO: More tests. Add all problems from txt file.


class PhysicsGenericTest(ABC):
    @abstractmethod
    def perform(self, text: str, problem: Problem, solution: object):
        raise NotImplemented()

    def test_convert_1(self):
        text = 'The car is traveling at a speed of 108 kilometers per hour. Represent this speed in meters per second.'
        problem = ConvertProblem(GivenVariable(v, 108.0 * kilometer / hour), meter / second)
        solution = 30.0 * meter / second
        self.perform(text, problem, solution)

    def test_compare_1(self):
        text = 'Which speed is greater: 10 meters per second or 10 kilometers per hour?'
        problem = CompareProblem(GivenVariable(v, 10.0 * meter / second), GivenVariable(v, 10.0 * kilometer / hour))
        solution = Ordering.GT
        self.perform(text, problem, solution)

    def test_compare_2(self):
        text = 'Which speed is slower: 72 kilometers per hour or 24 meters per second?'
        problem = CompareProblem(GivenVariable(v, 72.0 * kilometer / hour), GivenVariable(v, 24.0 * meter / second))
        solution = Ordering.LT
        self.perform(text, problem, solution)

    def test_compare_3(self):
        text = ('A sprinter runs at 480 meters per minute, and a boy on a bicycle rides at 27 kilometers per hour.'
                'Which of these athletes is moving faster?')
        problem = CompareProblem(GivenVariable(v, 480.0 * meter / minutes), GivenVariable(v, 27.0 * kilometer / hour))
        solution = Ordering.GT
        self.perform(text, problem, solution)

    def test_relative_change_1(self):
        text = ('How many times will the speed of wave propagation increase if the wavelength increases by 3 times and '
                'the period of oscillation remains unchanged?')
        problem = RelativeChangeProblem(v, [VariableChange(lam, 3.0)])
        solution = (3, Formula(v, lam / T))
        self.perform(text, problem, solution)

    def test_relative_change_2(self):
        text = ('How many times will the moment of a force change if the force is increased by a factor of 8 and the '
                'arm of the force is decreased by a factor of 4.')
        problem = RelativeChangeProblem(M, [VariableChange(F, 8.0), VariableChange(d, 1 / 4)])
        solution = (2, Formula(M, F * d))
        self.perform(text, problem, solution)

    def test_relative_change_3(self):
        text = ('How many times should the resistance of a heater be reduced so that its power increases by a factor '
                'of 2 at a constant voltage?')
        problem = RelativeChangeProblem(R, [VariableChange(P, 2.0)])
        solution = (2.0, Formula(R, P / (I ** 2), parent=Formula(P, (I ** 2) * R)))
        self.perform(text, problem, solution)

    def test_relative_change_4(self):
        text = ('How many times will the ampere force acting on a conductor with a current placed in a magnetic field '
                'increase if the length of the conductor is reduced by 1.5 times, the current in the conductor is '
                'reduced by 2 times, and the magnetic induction is increased by 9 times?')
        problem = RelativeChangeProblem(F, [VariableChange(B, 9), VariableChange(l, 1 / 1.5), VariableChange(I, 1 / 2)])
        solution = (3.0, Formula(F, B * I * l * sin(a)))
        self.perform(text, problem, solution)

    def test_find_unknowns_1(self):
        text = 'The car drove for 40 minutes at a speed of 144 kilometers per hour. How far did the car travel?'
        problem = FindUnknownsProblem([GivenVariable(t, 40.0 * minutes), GivenVariable(v, 144.0 * kilometer / hour)],
                                      [S])
        solution = [Formula(S, v * t, parent=Formula(v, S / t))]
        self.perform(text, problem, solution)

    def test_find_unknowns_2(self):
        text = 'What is the density of a metal, 15 grams of which have a volume of 2 cubic centimeters?'
        problem = FindUnknownsProblem([GivenVariable(m, 15.0 * grams), GivenVariable(V, 2.0 * (centimeter ** 3))], [ro])
        solution = [Formula(ro, m / V)]
        self.perform(text, problem, solution)

    def test_find_unknowns_3(self):
        text = ('What is the density of plastic used to make a body weighing 24 grams and having a volume of '
                '20 cubic centimeters?')
        problem = FindUnknownsProblem([GivenVariable(m, 24.0 * grams), GivenVariable(V, 20.0 * (centimeter ** 3))],
                                      [ro])
        solution = [Formula(ro, m / V)]
        self.perform(text, problem, solution)

    def test_find_unknowns_4(self):
        text = 'What is the optical power of a collecting lens with a focal length of 40 centimeters?'
        problem = FindUnknownsProblem([GivenVariable(F, 40.0 * centimeter)], [D], context={'collecting'})
        solution = [Formula(D, 1 / F, context={'collecting'})]
        self.perform(text, problem, solution)

    def test_find_unknowns_5(self):
        text = ('The light intensity of a point light source is 180 candela. What is the illumination of the floor '
                'under this source if it is located at a height of 3 meters?')
        problem = FindUnknownsProblem([GivenVariable(I, 180.0 * candela), GivenVariable(h, 3.0 * meter)], [E])
        solution = [Formula(E, I / (h ** 2))]
        self.perform(text, problem, solution)

    def test_find_unknowns_6(self):
        text = ('The corridor at night is illuminated by a single lamp hanging at a height of 2.5 meters. What is the '
                'light intensity of this lamp if the illumination of the floor under it is 40 lux?')
        problem = FindUnknownsProblem([GivenVariable(h, 2.5 * meter), GivenVariable(E, 40.0 * lux)], [I])
        solution = [Formula(I, E * (h ** 2), parent=Formula(E, I / (h ** 2)))]
        self.perform(text, problem, solution)

    def test_find_unknowns_7(self):
        text = 'The airplane flew 1200 kilometers in 2 hours. At what speed did the airplane fly?'
        problem = FindUnknownsProblem([GivenVariable(S, 1200.0 * kilometer), GivenVariable(t, 2.0 * hour)], [v])
        solution = [Formula(v, S / t)]
        self.perform(text, problem, solution)

    def test_find_unknowns_8(self):
        text = 'A train is traveling at a speed of 180 kilometers per hour. How far does it travel in 2 hours?'
        problem = FindUnknownsProblem([GivenVariable(v, 180.0 * kilometer / hour), GivenVariable(t, 2.0 * hour)], [S])
        solution = [Formula(S, v * t, parent=Formula(v, S / t))]
        self.perform(text, problem, solution)

    def test_find_unknowns_9(self):
        text = 'A cyclist is moving at a speed of 400 meters per second. How far will he travel in 5 seconds?'
        problem = FindUnknownsProblem([GivenVariable(v, 400.0 * meter / second), GivenVariable(t, 5.0 * second)], [S])
        solution = [Formula(S, t * v, parent=Formula(v, S / t))]
        self.perform(text, problem, solution)

    def test_find_unknowns_10(self):
        text = 'A rotating bicycle wheel makes 90 revolutions in 0.5 minutes. With what period does the wheel rotate?'
        problem = FindUnknownsProblem([GivenVariable(N, 90.0 * revolution), GivenVariable(t, 0.5 * minutes)], [T])
        solution = [Formula(T, t / N)]
        self.perform(text, problem, solution)

    def test_find_unknowns_11(self):
        text = 'How often does the drum of a washing machine rotate if it makes 1600 revolutions in 2 minutes?'
        problem = FindUnknownsProblem([GivenVariable(N, 1600.0 * revolution), GivenVariable(t, 2.0 * minutes)], [nu])
        solution = [Formula(nu, N / t)]
        self.perform(text, problem, solution)

    def test_find_unknowns_12(self):
        text = ('The shaft of an electric motor rotates at 480 revolutions per minute. What is the period of its '
                'rotation?')
        problem = FindUnknownsProblem([GivenVariable(nu, 480.0 * revolution / minutes)], [T])
        solution = [Formula(T, 1 / nu)]
        self.perform(text, problem, solution)

    def test_find_unknowns_13(self):
        text = 'A compact disk in a CD drive makes 1 revolution in 0.01 seconds. How often does it rotate?'
        problem = FindUnknownsProblem([GivenVariable(N, 1.0 * revolution), GivenVariable(t, 0.01 * second)], [nu])
        solution = [Formula(nu, N / t)]
        self.perform(text, problem, solution)

    def test_find_unknowns_14(self):
        text = ('The percussion unit of a hammer drill oscillates at a frequency of 2.5 hertz. What is the period of'
                ' oscillation of the percussion mechanism?')
        problem = FindUnknownsProblem([GivenVariable(nu, 2.5 * hertz)], [T])
        solution = [Formula(T, 1 / nu)]
        self.perform(text, problem, solution)

    def test_find_unknowns_15(self):
        text = 'What is the force of gravity on a girl weighing 50 kilograms?'
        problem = FindUnknownsProblem([GivenVariable(m, 50.0 * kilogram)], [F])
        solution = [Formula(F, m * g)]
        self.perform(text, problem, solution)

    def test_find_unknowns_16(self):
        text = 'What is the force of gravity on a car weighing 800 kilograms?'
        problem = FindUnknownsProblem([GivenVariable(m, 800.0 * kilogram)], [F])
        solution = [Formula(F, m * g)]
        self.perform(text, problem, solution)

    def test_find_unknowns_17(self):
        text = 'What is the weight of a boy if his mass is 60 kilograms?'
        problem = FindUnknownsProblem([GivenVariable(m, 60.0 * kilogram)], [P])
        solution = [Formula(P, m * g)]
        self.perform(text, problem, solution)

    def test_find_unknowns_18(self):
        text = 'What is the weight of a bicycle if its mass is 60 kilograms?'
        problem = FindUnknownsProblem([GivenVariable(m, 60.0 * kilogram)], [P])
        solution = [Formula(P, m * g)]
        self.perform(text, problem, solution)

    def test_find_unknowns_19(self):
        text = 'What is the mass of a body subject to a gravity of 350 newtons?'
        problem = FindUnknownsProblem([GivenVariable(F, 350.0 * newton)], [m])
        solution = [Formula(m, F / g, parent=Formula(F, m * g))]
        self.perform(text, problem, solution)

    def test_find_unknowns_20(self):
        text = ('What is the pressure exerted on a 400 square centimeter support by a body whose mass is '
                '12 kilograms?')
        problem = FindUnknownsProblem([GivenVariable(S, 400.0 * (centimeter ** 2)), GivenVariable(m, 12.0 * kilogram)],
                                      [p])
        solution = [Formula(F, m * g),
                    Formula(p, F / S)]
        self.perform(text, problem, solution)

    def test_find_unknowns_21(self):
        text = ('What is the work done by a force of 5000 newtons applied to a trolley, if the trolley traveled '
                '150 meters under the action of this force?')
        problem = FindUnknownsProblem([GivenVariable(F, 5000.0 * newton), GivenVariable(S, 150.0 * meter)], [A])
        solution = [Formula(A, F * S)]
        self.perform(text, problem, solution)

    def test_find_unknowns_22(self):
        text = ('To raise a marble column weighing 3.78 tons from the bottom of a lake, 95.2 kilojoules of work was '
                'done. Determine the depth of the lake.')
        problem = FindUnknownsProblem([GivenVariable(m, 3.78 * ton), GivenVariable(A, 95.2 * kilojoule)], [h])
        solution = [Formula(F, m * g),
                    Formula(h, A / F, parent=Formula(A, F * h))]
        self.perform(text, problem, solution)


class PhysicsParsingTest(unittest.TestCase, PhysicsGenericTest):
    def perform(self, text: str, problem: Problem, solution: object):
        doc = recognize_entities(text)
        parsed = parse_english_document(doc)
        self.assertEqual(problem, parsed)


class PhysicsSolutionTest(unittest.TestCase, PhysicsGenericTest):
    def perform(self, text: str, problem: Problem, solution: object):
        self.assertEqual(solution, problem.solve())


if __name__ == '__main__':
    unittest.main()
