import re
from typing import List, Optional

from spacy.tokens import Doc, Span, Token
from sympy import Symbol

from physics_solver.math.formulas import formulas
from physics_solver.math.types import *
from physics_solver.math.variables import nu
from physics_solver.parser.nlp import nlp
from physics_solver.parser.patterns import terms_and_vars, compound_terms_and_vars, unit_names_and_vars
from physics_solver.problems.compare_problem import CompareProblem
from physics_solver.problems.convert_problem import ConvertProblem
from physics_solver.problems.find_unknowns_problem import FindUnknownsProblem
from physics_solver.problems.problem import Problem
from physics_solver.problems.relative_change_problem import RelativeChangeProblem, VariableChange
from physics_solver.types.given_variable import GivenVariable
from physics_solver.util.exceptions import ParseError
from physics_solver.util.functions import find_by_predicate

from sympy.physics.units import *
from physics_solver.math.additional_units import *


def remove_too_many_spaces(text: str) -> str:
    return re.sub(r'\s{2,}', ' ', text)


def recognize_entities(text: str) -> Doc:
    text = remove_too_many_spaces(text)
    return nlp(text)


def parse_english_document(doc: Doc) -> Problem:
    given_variables = []
    changes = []
    unknowns = []
    context = []
    variable_under_change = None
    unit = None
    comparison = None
    i = 0

    while i < len(doc.ents):
        cur_ent = doc.ents[i]
        if cur_ent.label_ == 'CONTEXT':
            context.append(cur_ent.text)
            i += 1
        elif cur_ent.label_ == 'UNKNOWN_QUESTION':
            i += 1
            if i < len(doc.ents) and doc.ents[i].label_ == 'TERM':
                unknowns.append(deduce_variable_from_term(doc.ents[i].text))
                i += 1
        elif cur_ent.label_ == 'UNKNOWN_HOW_QUESTION':
            unknowns.append(deduce_variable_from_special(cur_ent[1]))
            i += 1
        elif cur_ent.label_ == 'QUANTITY':
            val = parse_quantity_entity(cur_ent)
            var = deduce_variable_from_quantity(val)
            given_variables.append(GivenVariable(var, val))
            i += 1
        elif cur_ent.label_ == 'TERM':
            term = cur_ent
            while i < len(doc.ents) and doc.ents[i].label_ == 'TERM':
                i += 1
            if i == len(doc.ents):
                continue
            snd = doc.ents[i]
            if snd.label_ == 'QUANTITY':
                var = deduce_variable_from_term(term.text)
                val = parse_quantity_entity(snd)
                given_variables.append(GivenVariable(var, val))
                i += 1
            elif snd.label_ == 'CHANGE_VERB':
                if variable_under_change is not None:
                    raise ParseError('only one variable in question is allowed')
                variable_under_change = deduce_variable_from_term(term.text)
                i += 1
            elif snd.label_ == 'POS_CHANGE' or snd.label_ == 'NEG_CHANGE':
                changes.append(parse_change(term, snd, snd.label_ == 'POS_CHANGE'))
                i += 1
        elif cur_ent.label_ == 'UNIT':
            if unit:
                raise ParseError('too many unit entities')
            unit = parse_unit_entity(cur_ent)
            i += 1
        elif cur_ent.label_ == 'COMPARISON_WORD':
            if comparison:
                raise ParseError('too many comparison words')
            comparison = cur_ent.text
            i += 1
        else:
            raise ParseError('unexpected entity')

    context = set(context)

    if variable_under_change:
        if given_variables:
            raise ParseError('no given variables are allowed in relative change problem')
        elif unknowns:
            raise ParseError('no unknowns are allowed in relative change problem')
        elif comparison:
            raise ParseError('no comparison is allowed in relative change problem')

        return RelativeChangeProblem(variable_under_change, changes, context=context)
    elif unit:
        if unknowns:
            raise ParseError('no unknowns are allowed in conversion problem')
        elif changes or variable_under_change:
            raise ParseError('no changes are allowed in conversion problem')
        elif comparison:
            raise ParseError('no comparison is allowed in conversion problem')
        elif len(given_variables) != 1:
            raise ParseError('too many given variables')

        return ConvertProblem(given_variables[0], unit, context=context)
    elif comparison:
        if unknowns:
            raise ParseError('no unknowns are allowed in comparison problem')
        elif changes or variable_under_change:
            raise ParseError('no changes are allowed in comparison problem')
        elif len(given_variables) != 2:
            raise ParseError('wrong quantities count (expected 2)')

        return CompareProblem(given_variables[0], given_variables[1], comparison, context=context)
    elif unknowns:
        if changes or variable_under_change:
            raise ParseError('no changes are allowed in calculation problem')
        elif comparison:
            raise ParseError('no comparison is allowed in calculation problem')
        elif unit:
            raise ParseError('no conversion is allowed in calculation problem')

        return FindUnknownsProblem(given_variables, unknowns, context=context)
    else:
        raise ParseError('could not determine problem type')


def parse_change(term: Span, change: Span, is_positive: bool) -> VariableChange:
    var = deduce_variable_from_term(term.text)
    factor = parse_number(change[-1].text)
    if not is_positive:
        factor = 1 / factor
    return VariableChange(var, factor)


def parse_given_variable(quantity: Span, term: Optional[Span] = None) -> GivenVariable:
    val = parse_quantity_entity(quantity)
    var = deduce_variable_from_term(term.text) if term else deduce_variable_from_quantity(val)
    return GivenVariable(var, val)


def parse_quantity_entity(quantity: Span) -> Quantity:
    num_token, *unit_tokens = quantity
    return parse_number(num_token.text) * parse_unit_entity(unit_tokens)


def parse_number(text: str) -> Number:
    # NOTE: Like num also catches 'one', 'two', etc.
    if not re.match(r'[0-9]+|[0-9]\\.[0-9]', text):
        raise ParseError('not a number')
    return float(text)


def parse_unit_entity(unit_tokens: Span | List[Token]) -> Unit:
    try:
        text = unit_tokens.text if isinstance(unit_tokens, Span) \
            else ' '.join(map(lambda token: token.text, unit_tokens))
        text = re.sub(r'per', '/', text)
        text = re.sub(r'square ([a-z]+)', r'\g<1>**2', text)
        text = re.sub(r'cubic ([a-z]+)', r'\g<1>**3', text)
        return eval(text)
    except SyntaxError or UnboundLocalError:
        raise ParseError('could not parse unit')


def deduce_variable_from_term(text: str) -> Symbol:
    if text.find('of') != -1:
        text = text[:text.find('of')].strip()

    def name_equals_text(pair: Tuple[str, Symbol]) -> bool:
        return pair[0] == text

    by_single = find_by_predicate(name_equals_text, terms_and_vars)
    if by_single:
        return by_single[1]

    by_compound = find_by_predicate(name_equals_text, compound_terms_and_vars)
    if by_compound:
        return by_compound[1]

    raise ParseError('could not deduce variable from term')


def deduce_variable_from_special(token: Token) -> Symbol:
    if token.text == 'far':
        return Symbol('S')
    elif token.text == 'often':
        return nu
    else:
        raise ParseError('could not determine the unknown variable')


def deduce_variable_from_quantity(quantity: Quantity) -> Symbol:
    _, unit = separate_num_and_unit(quantity)

    var_unit = unit_to_var_expr(unit)
    if isinstance(var_unit, Symbol):
        return var_unit

    by_formula = find_by_predicate(lambda f: var_unit.equals(f.expansion), formulas)

    if by_formula:
        return by_formula.var

    raise ParseError('could not deduce variable from quantity')


def unit_to_var_expr(unit: Unit) -> Expr:
    s1 = unit.subs(unit_names_and_vars)
    s2 = s1.replace(lambda x: isinstance(x, Quantity), lambda x: x.args[0])
    return s2
