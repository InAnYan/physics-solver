from typing import List, Dict

import spacy
from spacy import displacy

from src.spacy_pat_match_dsl.dsl import PatternsGrammar, lower, Optional, pos, lemma, lower_in, Or, And, Token, \
    lemma_in, lower_in_list, lemma_in_list

from physics_solver.types import *


def prefix(p: str, l: List[str]) -> List[str]:
    return [p + s for s in l]


def postfix(p: str, l: List[str]) -> List[str]:
    return [s + p for s in l]


def prefixes(ps: List[str], l: List[str]) -> List[str]:
    res = []
    for p in ps:
        res += [p + s for s in l]
    return res


def postfixes(ps: List[str], l: List[str]) -> List[str]:
    res = []
    for p in ps:
        res += [s + p for s in l]
    return res


basic_unit_names = ['meter', 'hour', 'minute', 'second', 'gram', 'candela', 'lux', 'revolution', 'hertz', 'newton',
                    'joule', 'ton']
prefixed_unit_names = basic_unit_names + prefixes(['kilo', 'centi', 'mega'], basic_unit_names)

compound_term_words = ['ampere force', 'wave propagation', 'optical power', 'focal length', 'luminous intensity',
                       'force of gravity', 'force of pressure', 'air pressure']

terms_and_vars = [('density', ro),
                  ('volume', V),
                  ('speed', v),
                  ('length', l),
                  ('moment', M),
                  ('force', F),
                  ('arm', d),
                  ('wavelength', lam),
                  ('power', P),
                  ('capacitance', c),
                  ('resistance', R),
                  ('current', I),
                  ('induction', B),
                  ('illumination', E),
                  ('height', h),
                  ('period', T),
                  ('frequency', nu),
                  ('weight', P),
                  ('mass', m),
                  ('work', A),
                  ('depth', h)]


class Patterns(PatternsGrammar):
    unit_name = lemma_in_list(prefixed_unit_names)
    modifier = lower_in('cubic', 'square')
    single_unit = Optional(modifier) + unit_name
    compound_unit = single_unit + lower('per') + single_unit
    UNIT = single_unit | compound_unit

    QUANTITY = pos('NUM') + UNIT

    single_term = lower_in_list(list(map(lambda x: x[0], terms_and_vars)))
    compound_term = Or(*[And(*[lower(w) for w in term.split()]) for term in compound_term_words])  # 'of force' is recognized as compound unit
    TERM = single_term | compound_term

    question_word = lower_in('what', 'determine', 'calculate')
    UNKNOWN = question_word + TERM

    positive_change_word = lemma_in('increase')
    negative_change_word = lemma_in('decrease', 'reduce')
    change_pattern = lower('by') + Optional(lower('factor') + lower('of')) + pos('NUM')
    POS_CHANGE = positive_change_word + change_pattern
    NEG_CHANGE = negative_change_word + change_pattern
    CHANGE_QUESTION = positive_change_word | negative_change_word | lower('change')

    special_unknown_word = lower_in('far', 'fast', 'often')
    SPECIAL_UNKNOWN = lower('how') + special_unknown_word

    COMPARISON = lower_in('greater', 'faster', 'bigger', 'larger') | lower_in('slower', 'less', 'smaller')
