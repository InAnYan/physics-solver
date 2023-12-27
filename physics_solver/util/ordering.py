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

    def make_human_str(self) -> str:
        if self == Ordering.EQ:
            return 'the values are equal'
        elif self == Ordering.GT:
            return 'the first value is greater'
        else:
            return 'the second value is greater'
