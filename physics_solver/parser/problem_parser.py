import re
from typing import List, Optional, Callable

from spacy.tokens import Doc, Span, Token
from sympy import Expr

from sympy.physics.units.definitions.unit_definitions import *

from physics_solver.exceptions import ParseError
from physics_solver.formulas import formulas
from physics_solver.parser.nlp import nlp
from physics_solver.parser.patterns import terms_and_vars, compound_terms_and_vars, unit_names_and_vars
from physics_solver.problem import Problem
from physics_solver.problems.compare_problem import CompareProblem
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns import FindUnknownsProblem
from physics_solver.problems.relative_change_problem import RelativeChangeProblem, VariableChange
from physics_solver.types import *
from physics_solver.util import T_var, find_by_predicate


def remove_too_many_spaces(text: str) -> str:
    return re.sub(r'\s{2,}', ' ', text)


def recognize_entities(text: str) -> Doc:
    text = remove_too_many_spaces(text)
    return nlp(text)


def parse_english_document(doc: Doc) -> Problem:
    if has_entity(doc, 'UNKNOWN_QUESTION') or has_entity(doc, 'UNKNOWN_HOW_QUESTION'):
        # Find unknowns problem.
        unk_vars = find_unknowns(doc)

        givens = find_givens(doc)
        if not givens:
            raise ParseError('could not find given values')

        return FindUnknownsProblem(givens, unk_vars)
    elif has_entity(doc, 'CHANGE_VERB'):
        # Relative change problem.
        var = find_variable_under_change(doc)
        changes = find_changes(doc)
        if not changes:
            raise ParseError('could not find changes')

        return RelativeChangeProblem(var, changes)
    elif has_entity(doc, 'COMPARISON_VERB'):
        # Comparison problem.
        # TODO: THERE MAYBE ERROR NotEnough Values to unpack.
        x, y, *rest = find_all(doc, 'QUANTITY')
        if rest:
            raise ParseError('too many quantities to compare')

        return CompareProblem(make_given_variable(x), make_given_variable(y))
    elif has_entity(doc, 'UNIT'):
        # Conversion problem.
        # TODO: THERE MAYBE ERROR NotEnough Values to unpack.
        unit, *unit_rest = find_all(doc, 'UNIT')
        # TODO: THERE MAYBE ERROR NotEnough Values to unpack.
        given, *givens_rest = find_givens(doc)

        if unit_rest or givens_rest:
            raise ParseError('only one quantity and one unit are allowed')

        return ConvertProblem(given, make_unit(unit))
    else:
        raise ParseError('could not determine the problem type')


def find_variable_under_change(doc: Doc) -> Variable:
    # TODO: THERE MAYBE ERROR NotEnough Values to unpack.
    res, *rest = find_pairs(doc, 'TERM', 'CHANGE_VERB',
                            lambda x, _: deduce_variable_from_term(x.text))

    if rest:
        raise ParseError('only one variable in question is allowed')

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
    unk_ents_1 = find_all(doc, 'UNKNOWN_QUESTION')
    unk_vars_1 = [deduce_variable_from_term(e[3:].text) for e in unk_ents_1]

    unk_ents_2 = find_all(doc, 'UNKNOWN_HOW_QUESTION')
    unk_vars_2 = list(map(lambda special: deduce_variable_from_special(special[1]), unk_ents_2))

    return unk_vars_1 + unk_vars_2


def deduce_variable_from_special(token: Token) -> Variable:
    if token.text == 'far':
        return sympy.Symbol('S')
    else:
        raise ParseError('could not determine the unknown variable')


def has_entity(doc: Doc, name: str) -> bool:
    return any(map(lambda x: x.label_ == name, doc.ents))


def find_all(doc: Doc, name: str) -> List[Span]:
    return list(filter(lambda e: e.label_ == name, doc.ents))


def find_pairs(doc: Doc, fst: str, snd: str,
               on_pair: Callable[[Span, Span], T_var],
               on_single_second: Optional[Callable[[Span], T_var]] = None,
               **kwargs) -> List[T_var]:
    res = []
    i = 0

    while i < len(doc.ents):
        e = doc.ents[i]
        if e.label_ == fst:
            term = e
            while i < len(doc.ents) and doc.ents[i].label_ == fst:
                i += 1
            if i < len(doc.ents) and doc.ents[i].label_ == snd:
                quantity = doc.ents[i]
                res.append(on_pair(term, quantity))
                i += 1
        elif e.label_ == snd and not kwargs.get('ignore_snd'):
            if not on_single_second:
                raise ParseError('could not make a pair of entities')

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
    return make_num(num_token) * make_unit(unit_tokens)


def make_num(num: Token) -> Number:
    # NOTE: Like num also catches 'one', 'two', etc.
    if not re.match(r'[0-9]+|[0-9]\\.[0-9]', num.text):
        raise ParseError('not a number')
    return float(num.text)


# noinspection PyUnresolvedReferences
def make_unit(unit_tokens: Span | List[Token]) -> Unit:
    try:
        text = unit_tokens.text if isinstance(unit_tokens, Span) \
            else ' '.join(map(lambda token: token.text, unit_tokens))
        text = re.sub(r'per', '/', text)
        text = re.sub(r'square ([a-z]+)', r'\g<1>**2', text)
        text = re.sub(r'cubic ([a-z]+)', r'\g<1>**3', text)
        return eval(text)
    except SyntaxError or UnboundLocalError:
        raise ParseError('could not parse unit')


def deduce_variable_from_term(text: str) -> Variable:
    def name_equals_text(pair: Tuple[str, Variable]) -> bool:
        return pair[0] == text

    by_single = find_by_predicate(name_equals_text, terms_and_vars)
    if by_single:
        return by_single[1]

    by_compound = find_by_predicate(name_equals_text, compound_terms_and_vars)
    if by_compound:
        return by_compound[1]

    raise ParseError('could not deduce variable from term')


def deduce_variable_from_quantity(quantity: Quantity) -> Variable:
    _, unit = separate_num_and_unit(quantity)

    var_unit = unit_to_var_expr(unit)
    if isinstance(var_unit, Variable):
        return var_unit

    by_formula = find_by_predicate(lambda f: var_unit.equals(f.expansion), formulas)

    if by_formula:
        return by_formula.var

    raise ParseError('could not deduce variable from quantity')


def unit_to_var_expr(unit: Unit) -> Expr:
    s1 = unit.subs(unit_names_and_vars)
    s2 = s1.replace(lambda x: isinstance(x, Quantity), lambda x: x.args[0])
    return s2

