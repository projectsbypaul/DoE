from __future__ import annotations
from itertools import zip_longest, product
from typing import List
import random

def interleave_records(groups: List[List[dict]]) -> List[dict]:
    interleaved = []
    for rowset in zip_longest(*groups):
        for rec in rowset:
            if rec is not None:
                interleaved.append(rec)
    return interleaved

def schedule_by_design(design_recs, outers):
    rows = []
    if not outers:
        return list(design_recs)
    names = [f.name for f in outers]
    values = [f.levels for f in outers]
    for rec in design_recs:
        for combo in product(*values):
            row = dict(rec)
            for n, v in zip(names, combo):
                row[n] = v
            rows.append(row)
    return rows

def schedule_nested(design_recs, outers):
    rows = []
    if not outers:
        return list(design_recs)
    names = [f.name for f in outers]
    values = [f.levels for f in outers]
    for combo in product(*values):
        for rec in design_recs:
            row = dict(rec)
            for n, v in zip(names, combo):
                row[n] = v
            rows.append(row)
    return rows

def schedule_interleave_first(design_recs, outers, base_rng: int):
    
    if not outers:
        return list(design_recs)
    first = outers[0]; rest = outers[1:]
    rows = []
    rest_names = [f.name for f in rest]
    rest_values = [f.levels for f in rest]
    rest_product = list(product(*rest_values)) if rest_values else [()]
    for rest_combo in rest_product:
        groups = []
        for a in first.levels:
            rng = random.Random(hash((a, rest_combo, base_rng)) % (10**9))
            local = list(design_recs)
            rng.shuffle(local)
            group = []
            for rec in local:
                row = dict(rec); row[first.name] = a
                for n, v in zip(rest_names, rest_combo):
                    row[n] = v
                group.append(row)
            groups.append(group)
        rows.extend(interleave_records(groups))
    return rows