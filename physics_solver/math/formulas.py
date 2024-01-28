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
    (A, F * h),  # Another hack, because of ambiguity.
    (n, sol / v),
    (E, m * (sol ** 2)),
    (m, plank * v / sol ** 2),
    (m, plank / (sol * lam)),
    (p, m * sol),
    (E, plank * sol / lam),
    (v, 2 * pi * R / T),
    (nu, 1 / T),
    (v, 2 * pi * nu),
    (omega, phi / t),
    (omega, 2 * pi / T),
    (omega, 2 * pi * nu),
    (v, omega * R),
    (F, -k * x),
    (F, -k * S),
    (h, v * t + g * t * t / 2),
    (v, sqrt(g * R)),
    (A, F * S * cos(a)),
    (N, A / t),
    (E, m * v * v / 2),
    (E, m * g * h),
    (E, k * x * x / 2),
    (p, ro * g * h),
    (F, ro * g * V),
    (I, U / R),
    (B, M / (I * S)),
    (P, U * U / R),
    (P, I * U),
    (Phi, B * S * cos(a)),
    (F, B * I * l * sin(a)),
]

context_formulas = [
    Formula(D, 1 / F, context={'converging'}),
    Formula(S, S ** 2, context={'square'}),  # A hack.
]

formulas = [Formula(*args) for args in formulas_bare] + context_formulas