from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Set

from physics_solver.types.string_solution import StringSolution


@dataclass(frozen=True)
class Problem(ABC):
    context: Set[str] = field(default_factory=set, kw_only=True)

    @abstractmethod
    def solve_and_make_string_solution(self) -> StringSolution:
        raise NotImplemented()
