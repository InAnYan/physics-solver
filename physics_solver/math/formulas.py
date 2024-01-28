from sympy import sin, sqrt, cos

from physics_solver.math.formula import Formula
from physics_solver.math.variables import *

formulas_bare = [
    (P, (I ** 2) * R),
    (v, S / t),
    (v, lam / T),
    (M, F * d),
    (ro, m / V),
    (F, B * I * l * sin(a)),
    (E, I / (h ** 2)),
    (T, t / N),
    (nu, N / t),
    (T, 1 / nu),
    (nu, 1 / T),
    (F, m * g),
    (P, m * g),
    (p, F / S),
    (A, F * S),
    (F, q * B * v * sin(a)),
    (A, F * h)  # Another hack, because of ambiguity.
]

context_formulas = [
    Formula(D, 1 / F, context={'converging'}),
    Formula(S, S ** 2, context={'square'}),  # A hack.
]

formulas = [Formula(*args) for args in formulas_bare] + context_formulas
