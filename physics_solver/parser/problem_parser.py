from typing import Tuple, List, Optional, Callable, TypeVar

from spacy.tokens import Doc, Span, Token
import spacy
import re

from physics_solver.exceptions import ParseError
from physics_solver.formulas import formulas
from physics_solver.parser.nlp import nlp
from physics_solver.parser.patterns import Patterns, terms_and_vars, compound_terms_and_vars, unit_names_and_vars
from physics_solver.problem import Problem
from physics_solver.problems.compare_problem import CompareProblem
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns import FindUnknownsProblem
from physics_solver.problems.relative_change_problem import RelativeChangeProblem, VariableChange
from physics_solver.types import *
from physics_solver.util import T_var, find_by_predicate, raise_obj

stop_words = ['the', 'a', 'an']


def remove_stop_words(text: str) -> str:
    for stop_word in stop_words:
        text = re.sub('\\b[' + stop_word[0] + stop_word[0].upper() + ']' + stop_word[1:] + '\\b', '', text)
    return text


def remove_too_many_spaces(text: str) -> str:
    return re.sub(r'\s{2,}', ' ', text)


def parse_english_problem(text: str) -> Tuple[Problem, Doc]:
    # TODO: Probably remove stop words step
    # TODO: Special question handling.
    doc = recognize_entities(text)
    problem = recognize_problem(doc)
    return problem, doc


def recognize_entities(text: str) -> Doc:
    text = remove_too_many_spaces(remove_stop_words(text))
    return nlp(text)


def recognize_problem(doc: Doc) -> Problem:
    if has_entity(doc, 'UNKNOWN') or has_entity(doc, 'SPECIAL_UNKNOWN'):
        # Find unknowns problem.
        unk_vars = find_unknowns(doc)

        givens = find_givens(doc)
        if not givens:
            raise ParseError()

        return FindUnknownsProblem(givens, unk_vars)
    elif has_entity(doc, 'CHANGE_QUESTION'):
        # Relative change problem.
        var = find_variable_under_change(doc)
        changes = find_changes(doc)
        if not changes:
            raise ParseError()

        return RelativeChangeProblem(var, changes)
    elif has_entity(doc, 'COMPARISON'):
        # Comparison problem.
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


def find_variable_under_change(doc: Doc) -> Variable:
    res, *rest = find_pairs(doc, 'TERM', 'CHANGE_QUESTION',
                            lambda x, _: deduce_variable_from_term(x.text))

    if rest:
        raise ParseError()

    return res


def find_changes(doc: Doc) -> List[VariableChange]:
    changes_1 = find_pairs(doc, 'TERM', 'POS_CHANGE',
                           lambda x, y: make_change(x, y, True))
    changes_2 = find_pairs(doc, 'TERM', 'NEG_CHANGE',
                           lambda x, y: make_change(x, y, False))

    return changes_1 + changes_2


def make_change(term: Span, change: Span, is_positive: bool) -> VariableChange:
    var = deduce_variable_from_term(term.text)
    factor = make_num(change[-1])
    if not is_positive:
        factor = 1 / factor
    return VariableChange(var, factor)


def find_unknowns(doc: Doc) -> List[Variable]:
    # TODO: Separate question for unknown and term.
    unknowns_ents = find_all(doc, 'UNKNOWN')
    unk_vars_1 = [deduce_variable_from_term(unk[2:].text) for unk in unknowns_ents]

    spec_ents = find_all(doc, 'SPECIAL_UNKNOWN')
    unk_vars_2 = list(map(lambda s: deduce_variable_from_special(s[1]), spec_ents))

    return unk_vars_1 + unk_vars_2


def deduce_variable_from_special(t: Token) -> Variable:
    if t.text == 'far':
        return Symbol('S')
    else:
        raise ParseError()


# TODO: Parsing BNF of entities as stage?


def has_entity(doc: Doc, name: str) -> bool:
    return any(map(lambda x: x.label_ == name, doc.ents))


def find_all(doc: Doc, name: str) -> List[Span]:
    return list(filter(lambda e: e.label_ == name, doc.ents))


def find_pairs(doc: Doc, first: str, second: str,
               on_pair: Callable[[Span, Span], T_var],
               on_single_second: Optional[Callable[[Span], T_var]] = None) -> List[T_var]:
    res = []
    i = 0

    while i < len(doc.ents):
        e = doc.ents[i]
        if e.label_ == first:
            term = e
            while i < len(doc.ents) and doc.ents[i].label_ == first:
                i += 1
            if i < len(doc.ents) and doc.ents[i].label_ == second:
                quantity = doc.ents[i]
                res.append(on_pair(term, quantity))
                i += 1
        elif e.label_ == second:
            if not on_single_second:
                raise ParseError()

            res.append(on_single_second(e))
            i += 1
        else:
            i += 1

    return res


def find_givens(doc: Doc) -> List[GivenVariable]:
    return find_pairs(doc, 'TERM', 'QUANTITY',
                      lambda x, y: make_given_variable(y, x),
                      lambda x: make_given_variable(x))


def make_given_variable(quantity: Span, term: Optional[Span] = None) -> GivenVariable:
    val = make_quantity(quantity)
    var = deduce_variable_from_term(term.text) if term else deduce_variable_from_quantity(val)
    return GivenVariable(var, val)


def make_quantity(quantity: Span) -> Quantity:
    num_token, *unit_tokens = quantity
    # TODO: Maybe bug with LIKE_NUM and two one three?
    return make_num(num_token) * make_unit(unit_tokens)


def make_num(num: Token) -> Number:
    # TODO: Add asserts where needed.
    # NOTE: Like num also catches 'one', 'two', etc.
    if not re.match('[0-9]+|[0-9]\\.[0-9]', num.text):
        raise ParseError()
    return float(num.text)


from sympy.physics.units import *
from sympy.physics.units.quantities import *
from sympy.physics.units.unitsystem import *
from sympy.physics.units.prefixes import *


# noinspection PyUnresolvedReferences
def make_unit(unit_tokens: Span | List[Token]) -> Unit:
    # TODO: Safety check.
    # TODO: There is no revolution unit.
    try:
        # TODO: Wrong squares and cubic.
        # TODO: Replace 3**v by v**3.
        text = unit_tokens.text if isinstance(unit_tokens, Span) else ' '.join(map(lambda t: t.text, unit_tokens))
        text = re.sub('per', '/', text)
        text = re.sub('square ([a-z]+)', '\g<1>**2', text)
        text = re.sub('cubic ([a-z]+)', '\g<1>**3', text)
        return eval(text)
    except SyntaxError or UnboundLocalError:
        raise ParseError()


def deduce_variable_from_term(text: str) -> Variable:
    def name_equals_text(t: Tuple[str, Variable]) -> bool:
        return t[0] == text

    by_single = find_by_predicate(name_equals_text, terms_and_vars)
    if by_single:
        return by_single[1]

    by_compound = find_by_predicate(name_equals_text, compound_terms_and_vars)
    if by_compound:
        return by_compound[1]

    raise ParseError()


def deduce_variable_from_quantity(quantity: Quantity) -> Variable:
    _, unit = separate_num_and_unit(quantity)

    var_unit = unit_to_var_expr(unit)
    if isinstance(var_unit, Quantity):
        return var_unit.args[0]

    by_formula = find_by_predicate(lambda f: var_unit.equals(f.expansion), formulas)
    if by_formula:
        return by_formula.var

    raise ParseError()


def unit_to_var_expr(unit: Unit) -> Expr:
    return unit.subs(unit_names_and_vars)
