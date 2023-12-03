from typing import List, Dict, Tuple, Callable


def prefix(p: str, l: List[str]) -> List[str]:
    return [p + s for s in l]


def postfix(p: str, l: List[str]) -> List[str]:
    return [s + p for s in l]


def prefixes(ps: List[str], l: List[str]) -> List[str]:
    res = []
    for p in ps:
        res += [p + s for s in l]
    return res


def postfixes(ps: List[str], l: List[str]) -> List[str]:
    res = []
    for p in ps:
        res += [s + p for s in l]
    return res


def optional(l: List[Dict]) -> List[Dict]:
    return [d | {'OP': '?'} for d in l]


def belongs(l: List[str], m: str = 'LOWER') -> List[Dict]:
    return [{m: {'IN': l}}]


def lower(s: str) -> List[Dict]:
    return prop_is('LOWER', s)


def pos(s: str) -> List[Dict]:
    return prop_is('POS', s)


def prop_is(x: str, y: str) -> List[Dict]:
    return [{x: y}]


def lmap(f, l):
    return list(map(f, l))


def make_patterns(l: List[Tuple[str, List[Dict]]]) -> List[Dict]:
    return [{'label': name, 'pattern': pattern} for (name, pattern) in l]

