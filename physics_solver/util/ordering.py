from __future__ import annotations

from enum import Enum, auto


class Ordering(Enum):
    EQ = auto()
    GT = auto()
    LT = auto()

    @staticmethod
    def make(a: object, b: object) -> Ordering:
        if a == b:
            return Ordering.EQ
        elif a > b:
            return Ordering.GT
        else:
            return Ordering.LT

    def human_str_for_greater(self) -> str:
        if self == Ordering.EQ:
            return 'the values are equal'
        elif self == Ordering.GT:
            return 'the first value is greater'
        else:
            return 'the second value is greater'

    def human_str_for_smaller(self) -> str:
        return self.dumb_revert().human_str_for_greater().replace('greater', 'smaller')

    def dumb_revert(self) -> Ordering:
        if self == Ordering.GT:
            return Ordering.LT
        if self == Ordering.LT:
            return Ordering.GT
        else:
            return self
