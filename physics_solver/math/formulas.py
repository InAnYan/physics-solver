from sympy import sin

from physics_solver.math.formula import Formula
from physics_solver.math.variables import *

formulas = [
    Formula(P, (I ** 2) * R),
    Formula(v, S / t),
    Formula(D, 1 / F, context={'converging'}),
    Formula(v, lam / T),
    Formula(M, F * d),
    Formula(ro, m / V),
    Formula(F, B * I * l * sin(a)),
    Formula(E, I / (h ** 2)),
    Formula(T, t / N),
    Formula(nu, N / t),
    Formula(T, 1 / nu),
    Formula(nu, 1 / T),
    Formula(F, m * g),
    Formula(P, m * g),
    Formula(S, S ** 2, context={'square'}),  # A hack.
    Formula(p, F / S),
    Formula(A, F * S),
    Formula(F, q * B * v * sin(a)),
    Formula(A, F * h)  # Another hack, because of ambiguity.
]
