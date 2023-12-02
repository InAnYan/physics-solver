from typing import List

from physics_solver.problem import Problem


class StringSolution:
    givens: List[str]
    unknowns: List[str]
    steps: List[str]
    answer: str

    def __init__(self, problem: Problem, solution: object):
        self.givens = ['\\(v = 10\\)', '\\(t = 2\\)']
        self.unknowns = ['\\(S - ?\\)']
        self.steps = ['\\(S = v*t = 20\\)']
        self.answer = '\\(20\\)'
