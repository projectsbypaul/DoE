# entry_points/run_taguchi.py
from __future__ import annotations

from TaguchiOrthogonal.parsing import parse_spec
from TaguchiOrthogonal.assembly import build_design, write_schedule
from TaguchiOrthogonal.outer_setup import (
    schedule_by_design,
    schedule_nested,
    schedule_interleave_first,
)

class RunTaguchi:
    @staticmethod
    def run_taguchi(
        *,
        spec: str,
        design: str = "AUTO",
        subset_size: int | None = None,
        add_center: bool = False,
        order: str = "by-design",
        out: str = "schedule.csv",
        base_rng: int = 1234,
    ) -> None:
        """
        Entry-point wrapper so you can call:
          main.py taguchi schedule --spec <file> ...
        """
        inner_factors, outer_factors = parse_spec(spec)

        design_recs, chosen_design, _ = build_design(
            inner_factors=inner_factors,
            design=design,
            subset_size=subset_size,
            add_center=add_center,
            base_rng=base_rng,
        )

        if order == "by-design":
            rows = schedule_by_design(design_recs, outer_factors)
        elif order == "nested":
            rows = schedule_nested(design_recs, outer_factors)
        else:
            rows = schedule_interleave_first(design_recs, outer_factors, base_rng)

        inner_names = [f.name for f in inner_factors]
        outer_names = [f.name for f in outer_factors]
        write_schedule(rows, out, inner_names, outer_names)

        n_inner = len(design_recs)
        n_outer = 1
        for f in outer_factors:
            n_outer *= len(f.levels)
        total = n_inner * n_outer

        print(f"Wrote {out}")
        print(f"Design: {chosen_design}  | inner points (incl center if any): {n_inner}")
        print(f"Outer combos: {n_outer}  | TOTAL runs: {total}")
        if outer_factors:
            print("Outer factors: " + ", ".join(f"{f.name}({len(f.levels)})" for f in outer_factors))
