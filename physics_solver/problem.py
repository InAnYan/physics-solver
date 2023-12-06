from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def solve(self) -> object:
        raise NotImplemented()

    # Structural equality.
    @abstractmethod
    def __eq__(self, other) -> bool:
        raise NotImplemented()

    # With latex.
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplemented()

    # Without latex.
    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplemented()
