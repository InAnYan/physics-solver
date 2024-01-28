import sympy
from sympy.physics.units import newton, kilogram, joule, second, meter

lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, p, D, N, a, q, omega, phi, k, x, U, Phi, n \
    = sympy.symbols('\\lambda M F l t v S \\rho m V d P c R I B E h T \\nu A p D N a q \\omega \\phi k x U \\Phi n')

g = 9.8 * newton / kilogram
plank = 6.63 * (10 ** (-34)) * joule * second
sol = 3 * (10 ** 8) * meter / second
pi = 3.14