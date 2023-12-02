from typing import Tuple
from spacy.tokens import Doc
import spacy

from physics_solver.problem import Problem
from physics_solver.problems.convert_problem import ConvertProblem

nlp = spacy.load('en_core_web_sm')


def parse_english_problem(text: str) -> Tuple[Problem, Doc]:
    return (ConvertProblem(10, 1), nlp(text))
