from typing import TypeVar, Callable, List, Optional, Tuple, Iterable

T_var = TypeVar('T_var')
U_var = TypeVar('U_var')


def raise_obj(obj: object):
    raise obj


def find_by_predicate(pred: Callable[[T_var], bool], lst: List[T_var]) -> Optional[T_var]:
    # Source: https://stackoverflow.com/questions/8534256/find-first-element-in-a-sequence-that-matches-a-predicate.
    return next((x for x in lst if pred(x)), None)


def map_fst(lst: List[Tuple[T_var, U_var]]) -> List[T_var]:
    return list(map(lambda x: x[0], lst))


def are_lists_equal(a: list, b: list,
                    eq: Optional[Callable[[object, object], bool]] = lambda x, y: x.equals(y)) -> bool:
    i = 0
    while i < len(a):
        if i >= len(b):
            return False

        if not eq(a[i], b[i]):
            return False

        i += 1

    if i < len(b):
        return False
    else:
        return True


def concat(lists: List[List[T_var]]) -> List[T_var]:
    return [x for l in lists for x in l]


def lmap(f: Callable[[T_var], U_var], lst: Iterable[T_var]) -> List[U_var]:
    return list(map(f, lst))
