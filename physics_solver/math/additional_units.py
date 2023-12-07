from sympy.core.numbers import One
from sympy.physics.units import hertz, second, mass, kilogram, Quantity, kilo, joule
from sympy.physics.units.systems import SI

from physics_solver.math.types import Value

revolutions = revolution = Value('revolution', abbrev='rev')
SI.set_quantity_dimension(revolution, 1)
SI.set_quantity_scale_factor(hertz, revolution / second)

tons = ton = Value('ton', abbrev='ton')
SI.set_quantity_dimension(ton, mass)
SI.set_quantity_scale_factor(ton, 1000 * kilogram)

kilojoules = kilojoule = Value('kilojoule', abbrev='kJ')
kilojoule.set_global_relative_scale_factor(kilo, joule)
