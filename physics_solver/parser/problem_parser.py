from typing import Tuple, List, Dict
from spacy.tokens import Doc
import spacy
import re

from physics_solver.parser.patterns import patterns
from physics_solver.problem import Problem
from physics_solver.problems.convert_problem import ConvertProblem


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

"""
unit_names = {lower: 'meter'} | {lower: 'hour'};
unit_modifier = 'cubic' | 'square';
single_unit = unit_modifier unit_name;
compound_unit = single_unit 'per' single_unit;
UNIT = single_unit | compound_unit;
QUANTITY = {pos:'NUM'} UNIT;
single_terms = 'speed' | 'distance';
compound_terms = 'ampere' {lower: 'force'} | {lower: 'wave'} {lower: 'propagation'};
TERM = single_terms | compound_terms;
question_words = 'what' | 'calculate';
UNKNOWN = question_words TERM;
positive_change_words = 'increase';
negative_change_words = 'decrease' | 'calculate';
change_pattern = 'factor'?' 'of'? {pos: 'NUM'};
POS_CHANGE = positive_change_words change_pattern;
NEG_CHANGE = negative_change_words change_pattern;
CHANGE_QUESTION = positive_change_words | negative_change_words | 'change';
special_unknown_words = 'fast' | 'far';
SPECIAL_UNKNOWN = 'how' special_unknown_words;
COMPARISON = 'greater' | 'slower';
"""

"""
program = definition*;
definition = (fragment | entity) '=' ors;
ors = ands ('|' ands)*;
ands = and ands*;
and = string | fragment | entity | dict;
dict = '{' dict_pair (',' dict_pair)* '}';
dict_pair = fragment ':' string;


TOKENS: string, fragment, entity;
"""


nlp = spacy.load('en_core_web_sm')
nlp.remove_pipe('ner')
ruler = nlp.add_pipe('entity_ruler')

ruler.add_patterns(patterns)


def parse_english_problem(text: str) -> Tuple[Problem, Doc]:
    # After nlp call remove term1 term2 quantity -> term1 quantity
    text = remove_too_many_spaces(remove_stop_words(text))
    doc = nlp(text)
    print(f'\n\n TEXT:  {text}  \n\n')
    for t in doc:
        print(f'{t} | {t.pos_}')
    # Trailing terms (or ignore terms without quantity) in find unknown
    return (ConvertProblem(10, 1), doc)
