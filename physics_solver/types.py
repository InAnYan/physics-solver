import sympy
import sympy.physics

Formula = sympy.Eq
Quantity = sympy.physics.units.quantities.Quantity
Unit = Quantity  # That is SymPy peculiarity.
Variable = sympy.Symbol


class GivenVariable:
    var: Variable
    val: Quantity

    def __init__(self, var: Variable, val: Quantity):
        self.var, self.val = var, val


lam, M, F, l, t, v, S, ro, m, V, d, P, c, R, I, B, E, h, T, nu, A, h \
    = sympy.symbols('lam M F l t v S ro m V d P c R I B E h T nu A h')
