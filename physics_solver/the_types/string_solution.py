from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StringSolution:
    givens: List[str]
    unknowns: List[str]
    steps: List[str]
    answer: str
