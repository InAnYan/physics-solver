from dataclasses import dataclass

from sympy import Symbol, Number

@dataclass(frozen=True)
class VariableChange:
    variable: Symbol
    factor: Number

    def __str__(self) -> str:
        return f'\\({self.variable}\\) is changed by factor of \\({self.factor}\\)'
