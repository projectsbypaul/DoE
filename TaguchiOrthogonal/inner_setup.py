from __future__ import annotations
from typing import Any, List, Tuple

L9_IDX = [
    (0, 0, 0),
    (0, 1, 1),
    (0, 2, 2),
    (1, 0, 1),
    (1, 1, 2),
    (1, 2, 0),
    (2, 0, 2),
    (2, 1, 0),
    (2, 2, 1),
]

def make_l9(factors):
    if len(factors) != 3 or any(len(f.levels) != 3 for f in factors):
        raise ValueError("L9 requires exactly 3 inner factors with 3 levels each.")
    A, B, C = factors
    return [(A.levels[i], B.levels[j], C.levels[k]) for (i, j, k) in L9_IDX]

def make_grid(factors):
    if len(factors) != 3:
        raise ValueError("Currently supports exactly 3 inner factors.")
    A, B, C = factors
    return [(a, b, c) for a in A.levels for b in B.levels for c in C.levels]

def center_from_levels(levels):
    n = len(levels)
    if all(isinstance(v, (int, float)) for v in levels):
        if n % 2 == 1:
            return levels[n//2]
        else:
            return 0.5 * (float(levels[n//2 - 1]) + float(levels[n//2]))
    else:
        return levels[n//2]

def make_center(factors):
    return tuple(center_from_levels(f.levels) for f in factors)

def main():
    pass

if __name__ == '__main__':
    main()