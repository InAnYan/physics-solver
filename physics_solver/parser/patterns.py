from typing import List, Dict

from physics_solver.parser.pat_match_util import prefixes, postfix, belongs, optional, lower, pos, make_patterns


def make_change_pattern(words: List[str]) -> List[Dict]:
    return belongs(words) + optional(lower('factor') + lower('of')) + pos('NUM')


basic_unit_names = ['meter', 'hour', 'minute', 'second', 'gram', 'candela', 'lux', 'revolution', 'hertz', 'newton',
                    'joule', 'ton']
prefixed_unit_names = basic_unit_names + prefixes(['kilo', 'centi', 'mega'], basic_unit_names)
unit_names = prefixed_unit_names + postfix('s', prefixed_unit_names)

unit_modifier = ['cubic', 'square']

unit_single_pattern = optional(belongs(unit_modifier)) + belongs(unit_names)
unit_compound_pattern = unit_single_pattern + lower('per') + unit_single_pattern

quantity_single_unit_pattern = pos('NUM') + unit_single_pattern
quantity_compound_unit_pattern = pos('NUM') + unit_compound_pattern

terms = ['density', 'volume', 'speed', 'length', 'moment', 'force', 'arm', 'wavelength', 'power', 'capacitance',
         'resistance', 'current', 'induction', 'illumination', 'height', 'period', 'frequency', 'weight', 'mass',
         'work', 'depth']

term_single_pattern = belongs(terms)

questions = ['what', 'determine', 'calculate']

bare_unknown_pattern = belongs(questions)
unknown_single_pattern = bare_unknown_pattern + term_single_pattern

positive_change_words = ['increase']
negative_change_words = ['decrease', 'reduce']

positive_change_pattern = make_change_pattern(positive_change_words)
negative_change_pattern = make_change_pattern(negative_change_words)

change_question_pattern = belongs(positive_change_words + negative_change_words + ['change'])

positive_comparison_words = ['greater', 'faster', 'bigger', 'larger']
negative_comparison_words = ['slower', 'less', 'smaller']

comparison_pattern = belongs(positive_comparison_words + negative_comparison_words)

special_unknowns = ['far', 'fast', 'often']

special_unknowns_pattern = lower('how') + belongs(special_unknowns)

simple_patterns = make_patterns([
    ('UNIT', unit_single_pattern),
    ('UNIT', unit_compound_pattern),
    ('QUANTITY', quantity_single_unit_pattern),
    ('QUANTITY', quantity_compound_unit_pattern),
    ('TERM', term_single_pattern),
    ('POS_CHANGE', positive_change_pattern),
    ('NEG_CHANGE', negative_change_pattern),
    ('CHANGE_QUESTION', change_question_pattern),
    ('SPECIAL_UNKNOWN', special_unknowns_pattern),
    ('UNKNOWN', unknown_single_pattern),
    ('COMPARISON', comparison_pattern)])

compound_terms = ['ampere force', 'wave propagation', 'optical power', 'focal length', 'luminous intensity',
                  'force of gravity', 'force of pressure', 'air pressure']

term_compound_patterns = [{'label': 'TERM', 'pattern': [{'LOWER': w} for w in t.split()]} for t in compound_terms]
unknown_compound_patterns = [{'label': 'UNKNOWN', 'pattern': bare_unknown_pattern + [{'LOWER': w} for w in t.split()]}
                             for t in compound_terms]

patterns = simple_patterns + term_compound_patterns + unknown_compound_patterns
