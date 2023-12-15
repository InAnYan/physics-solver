import sympy
from sympy.physics.units import newton, kilogram

lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, p, D, N, a, q \
    = sympy.symbols('\\lambda M F l t v S \\rho m V d P c R I B E h T \\nu A p D N a q')

g = 9.8 * newton / kilogram
