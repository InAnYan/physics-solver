import spacy

from physics_solver.parser.patterns import Patterns

nlp = spacy.load('en_core_web_sm')
nlp.remove_pipe('ner')
ruler = nlp.add_pipe('entity_ruler')

patterns = Patterns()

ruler.add_patterns(patterns.generate_patterns_for_ruler())
