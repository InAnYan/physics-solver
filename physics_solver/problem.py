from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def solve(self) -> object:
        raise NotImplemented()

    @abstractmethod
    def equals(self, other) -> bool:
        raise NotImplemented()

    @abstractmethod
    def human_str_repr(self) -> str:
        raise NotImplemented()
