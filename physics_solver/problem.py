from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def solve(self) -> object:
        raise NotImplemented()
