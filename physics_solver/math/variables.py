import sympy
from sympy.physics.units import newton, kilogram

lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, p, D, N, a \
    = sympy.symbols('lam M F l t v S ro m V d P c R I B E h T nu A p D N a')

g = 9.8 * newton / kilogram
