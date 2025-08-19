from __future__ import annotations
from typing import Any, List, Tuple
import json, os
import numpy as np
import csv, os

from .inner_setup import make_l9, make_grid, make_center

def maximin_subset(points, k: int, base_rng: int = 1234):
    if np is None:
        raise RuntimeError("numpy is required for SUBSET design")
    if k >= len(points):
        return list(points)
    import random
    pts = np.array([[float(x) for x in p] for p in points], dtype=float)
    minv = pts.min(axis=0); maxv = pts.max(axis=0)
    denom = (maxv - minv); denom[denom == 0] = 1.0
    norm = (pts - minv) / denom
    rng = random.Random(base_rng)
    first = rng.randrange(len(points))
    chosen = [first]
    def dist2(a, b):
        d = norm[a] - norm[b]
        return float((d*d).sum())
    while len(chosen) < k:
        best_j = None; best_val = -1.0
        for j in range(len(points)):
            if j in chosen: continue
            mind2 = min(dist2(j, i) for i in chosen)
            if mind2 > best_val:
                best_val = mind2; best_j = j
        chosen.append(best_j)  # type: ignore
    return [points[i] for i in chosen]

def build_design(inner_factors, design: str, subset_size, add_center: bool, base_rng: int):
    chosen = design
    if chosen == "AUTO":
        if all(len(f.levels) == 3 for f in inner_factors):
            chosen = "L9"
        else:
            chosen = "GRID"
    if chosen == "L9":
        base_points = make_l9(inner_factors); label = "OA"
    else:
        grid = make_grid(inner_factors)
        if chosen == "SUBSET":
            if subset_size is None:
                raise ValueError("--subset-size is required for SUBSET")
            base_points = maximin_subset(grid, subset_size, base_rng=base_rng); label = "SUB"
        else:
            base_points = grid; label = "GRID"
    center_tuple = None
    if add_center:
        center_tuple = make_center(inner_factors)
    design_recs = []
    for idx, (v, b, p) in enumerate(base_points, start=1):
        design_recs.append({
            "group_id": f"{label}{idx}",
            "design_point": f"{label}{idx}",
            inner_factors[0].name: v,
            inner_factors[1].name: b,
            inner_factors[2].name: p
        })
    if add_center and center_tuple is not None:
        v, b, p = center_tuple
        design_recs.append({
            "group_id": "CENTER",
            "design_point": "CENTER",
            inner_factors[0].name: v,
            inner_factors[1].name: b,
            inner_factors[2].name: p
        })
    return design_recs, chosen, center_tuple

# doe_spec/assembly.py
def write_schedule(rows: list, out_path: str, inner_names: list, outer_names: list,
                   delimiter: str = ";", excel_mode: str = "decimal-comma", sep_header: bool = True):
    import csv, os
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    def fmt_cell(v):
        if excel_mode == "decimal-comma" and isinstance(v, (int, float)):
            # format without scientific notation; replace dot with comma
            s = f"{v:.15g}".replace(".", ",")
            return s
        elif excel_mode == "textify-dotted" and isinstance(v, (int, float)):
            s = f"{v}"
            # force text so Excel won’t date-parse 1.5
            return "'" + s
        return v

    fieldnames = ["run_id", "group_id", "design_point"] + inner_names + outer_names
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        # Excel hint for delimiter (helps some installs)
        if sep_header and delimiter == ";":
            f.write("sep=;\n")
        w.writeheader()
        for i, rec in enumerate(rows, start=1):
            rec = {k: fmt_cell(v) for k, v in dict(rec).items()}
            rec["run_id"] = i
            w.writerow(rec)
