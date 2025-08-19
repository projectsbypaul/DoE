# parsing.py
from dataclasses import dataclass
from typing import Any, List

def _norm(s: str) -> str:
    # strip BOM, zero-width chars, non-breaking spaces, regular whitespace
    return s.replace("\ufeff", "").replace("\u200b", "").replace("\xa0", " ").strip()

def parse_value(token: str) -> Any:
    t = _norm(token)
    if not t:
        return None
    t = t.replace(",", ".")  # decimal comma -> dot
    try:
        if "." not in t and "e" not in t.lower():
            return int(t)
    except Exception:
        pass
    try:
        return float(t)
    except Exception:
        return t  # keep as string

@dataclass
class Factor:
    name: str
    levels: List[Any]
    def __post_init__(self):
        vals = [v for v in self.levels if v is not None and f"{v}".strip() != ""]
        if len(vals) < 2:
            raise ValueError(f"{self.name}: need >=2 values, got {self.levels}")
        if all(isinstance(v, (int, float)) for v in vals):
            vals = sorted(vals)
        self.levels = vals

def parse_spec(path: str):
    inner_factors: List[Factor] = []
    outer_factors: List[Factor] = []
    # utf-8-sig auto-strips BOM at start of file
    with open(path, "r", encoding="utf-8-sig") as f:
        rows = [line.rstrip("\r\n") for line in f if line.strip()]

    # detect & skip header robustly
    if rows:
        first_col = _norm(rows[0].split(";", 1)[0]).lower()
        if first_col == "param_type":
            rows = rows[1:]

    for line in rows:
        parts = [ _norm(c) for c in line.split(";") ]
        if len(parts) < 2:
            continue
        ptype, name, *rest = parts
        values = [ parse_value(x) for x in rest if _norm(x) != "" ]
        if ptype.lower().startswith("inner"):
            inner_factors.append(Factor(name=name, levels=values))
        elif ptype.lower().startswith("outer"):
            outer_factors.append(Factor(name=name, levels=values))
        else:
            raise ValueError(f"Unknown PARAM_TYPE '{ptype}' in line: {line}")

    if len(inner_factors) != 3:
        raise ValueError(f"Expected exactly 3 inner factors; got {len(inner_factors)}")
    return inner_factors, outer_factors
