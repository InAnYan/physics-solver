from abc import ABC, abstractmethod
from typing import Set, Optional


class Problem(ABC):
    context: Set[str]

    def __init__(self, context: Optional[Set[str]]):
        self.context = context if context else set([])

    @abstractmethod
    def solve(self) -> object:
        raise NotImplemented()

    # Structural equality.
    def __eq__(self, other) -> bool:
        if not isinstance(other, Problem):
            return False

        return self.context == other.context

    # With latex.
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplemented()

    # Without latex.
    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplemented()
