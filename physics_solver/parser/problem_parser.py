from typing import Tuple, List, Optional

from spacy.tokens import Doc, Span, Token
import spacy
import re

from physics_solver.exceptions import ParseError
from physics_solver.parser.patterns import Patterns, terms_and_vars
from physics_solver.problem import Problem
from physics_solver.problems.compare_problem import CompareProblem
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns import FindUnknownsProblem
from physics_solver.types import *


def optional(d: list | dict) -> list | dict:
    if isinstance(d, list):
        return list(map(optional, d))
    else:
        return d | {'OP': '?'}


stop_words = ['the', 'a', 'an']


def remove_stop_words(text: str) -> str:
    for stop_word in stop_words:
        text = re.sub('\\b[' + stop_word[0] + stop_word[0].upper() + ']' + stop_word[1:] + '\\b', '', text)
    return text


def remove_too_many_spaces(text: str) -> str:
    return re.sub(r'\s{2,}', ' ', text)


nlp = spacy.load('en_core_web_sm')
nlp.remove_pipe('ner')
ruler = nlp.add_pipe('entity_ruler')

patterns = Patterns()

ruler.add_patterns(patterns.generate_patterns_for_ruler())


def parse_english_problem(text: str) -> Tuple[Problem, Doc]:
    # TODO: After nlp call remove term1 term2 quantity -> term1 quantity
    # TODO: Probably remove stop words step
    # TODO: Special question handling.
    text = remove_too_many_spaces(remove_stop_words(text))
    doc = nlp(text)
    return parse_problem_impl(doc), doc


def parse_problem_impl(doc: Doc) -> Problem:
    if has_entity(doc, 'UNKNOWN'):
        # Find unknowns problem.
        unknowns = find_all(doc, 'UNKNOWN')

        unk_vars = [deduce_variable_from_term(unk[1:].text) for unk in unknowns]

        givens = find_givens(doc)
        if not givens:
            raise ParseError()

        return FindUnknownsProblem(givens, unk_vars)
    elif has_entity(doc, 'SPECIAL_QUESTION'):
        # Find unknowns problem.
        # TODO: Special questions.
        # TODO: Combine special questions and basic unknowns.
        # TODO: rename UNKNOWN to UNKNOWN_QUESTION.
        raise NotImplemented()
    elif has_entity(doc, 'CHANGE_QUESTION'):
        # Relative change problem.
        raise NotImplemented()
    elif has_entity(doc, 'COMPARISON'):
        x, y, *rest = find_all(doc, 'QUANTITY')
        if rest:
            raise ParseError()

        return CompareProblem(make_quantity(x), make_quantity(y))
    elif has_entity(doc, 'UNIT'):
        # Conversion problem.
        unit, *unit_rest = find_all(doc, 'UNIT')
        given, *givens_rest = find_givens(doc)

        if unit_rest or givens_rest:
            raise ParseError()

        return ConvertProblem(given, make_unit(unit))
    else:
        raise ParseError()


def has_entity(doc: Doc, name: str) -> bool:
    return any(map(lambda x: x.label_ == name, doc.ents))


def find_all(doc: Doc, name: str) -> List[Span]:
    return list(filter(lambda e: e.label_ == name, doc.ents))


def find_givens(doc: Doc) -> List[GivenVariable]:
    res = []
    i = 0

    while i < len(doc.ents):
        e = doc.ents[i]
        if e.label_ == 'TERM':
            term = e
            while i < len(doc.ents) and doc.ents[i].label_ == 'TERM':
                i += 1
            if i < len(doc.ents) and doc.ents[i].label_ == 'QUANTITY':
                quantity = doc.ents[i]
                res.append(make_given_variable(quantity, term))
                i += 1
        elif e.label_ == 'QUANTITY':
            res.append(make_given_variable(e))
            i += 1
        else:
            i += 1

    return res


def make_given_variable(quantity: Span, term: Optional[Span] = None) -> GivenVariable:
    val = make_quantity(quantity)
    var = deduce_variable_from_term(term.text) if term else deduce_variable_from_quantity(quantity)
    return GivenVariable(var, val)


def make_quantity(quantity: Span) -> Quantity:
    num_token, *unit_tokens = quantity
    # TODO: Maybe bug with LIKE_NUM and two one three?
    return make_num(num_token) * make_unit(unit_tokens)


def make_num(num: Token) -> float:
    return float(num.text)


from sympy.physics.units import *
from sympy.physics.units.quantities import *
from sympy.physics.units.unitsystem import *
from sympy.physics.units.prefixes import *


# noinspection PyUnresolvedReferences
def make_unit(unit_tokens: Span) -> Unit:
    # TODO: Safety check.
    # TODO: We allow things like kilosecond. Which can produce error.
    # TODO: There is no revolution unit.
    try:
        return eval(unit_tokens.text.replace('per', ' / ').replace('square', '2 ** ').replace('cubic', '3 ** '))
    except SyntaxError or UnboundLocalError:
        raise ParseError()


def deduce_variable_from_term(text: str) -> Variable:
    # TODO: What about compound terms?
    try:
        return next(var for (name, var) in terms_and_vars if name == text)
    except StopIteration:
        # TODO: Is it right to raise Parse error?
        raise ParseError()


"""
class Dummy:
def __init__(self, text):
    self.text = text
    
make_unit(Dummy('meters per second'))
"""


def deduce_variable_from_quantity(quantity: Quantity) -> Variable:
    unit = sympy.Mul(*quantity.args[1:])

    # TODO: Term, variable, unit duplication.
    if isinstance(unit, Quantity):
        if unit == meter or unit == kilometer or unit == centimeter:
            return S
        elif unit == hour or unit == minute or unit == second:
            return t
        elif unit == newton:
            return F
        else:
            raise ParseError()
    elif isinstance(unit, sympy.Mul):
    # TODO: It supports only two arguments.
    # And probably only deletion.

    else:
        raise ParseError()
