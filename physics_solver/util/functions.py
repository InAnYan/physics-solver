from typing import Callable, List, Optional, Tuple, Iterable

from physics_solver.util.type_vars import T_var, U_var


def raise_obj(obj: object):
    raise obj


def find_by_predicate(pred: Callable[[T_var], bool], lst: List[T_var]) -> Optional[T_var]:
    # Source: https://stackoverflow.com/questions/8534256/find-first-element-in-a-sequence-that-matches-a-predicate.
    return next((x for x in lst if pred(x)), None)


def map_fst(lst: List[Tuple[T_var, U_var]]) -> List[T_var]:
    return list(map(lambda x: x[0], lst))


def concat(lists: List[List[T_var]]) -> List[T_var]:
    return [x for l in lists for x in l]


def lmap(f: Callable[[T_var], U_var], lst: Iterable[T_var]) -> List[U_var]:
    return list(map(f, lst))
