"""Helpers for the imported-05 lessons: board ops, beats, and number text."""
import hashlib
import io
import json
import os
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "data", "bank-import", "lessons", "in-05.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-05.json")


def batch():
    with io.open(SRC, encoding="utf-8") as f:
        return {q["id"]: q for q in json.load(f)}


# ── Number text ──────────────────────────────────────────────────────────────

def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


def num(x):
    """A plain number with no trailing zeros: 4.20 -> 4.2, 8.00 -> 8."""
    x = D(x)
    if x == x.to_integral_value():
        return str(int(x))
    return format(x.normalize(), "f")


def mon(x):
    """Money: a whole number of rupees, or two places (more only if the value needs them)."""
    x = D(x)
    if x == x.to_integral_value():
        return str(int(x))
    q = x.quantize(Decimal("0.01"))
    if q == x:
        return format(q, "f")
    return format(x.normalize(), "f")


def rs(x):
    return "₹" + mon(x)


# ── Board ops ────────────────────────────────────────────────────────────────

def _t(text, nth=None):
    t = {"text": text}
    if nth and nth > 1:
        t["nth"] = nth
    return t


def W(id, text, label=False, tone=None):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def GIVEN(id, text, label=False):
    return W(id, text, label, "given")


def ANS(id, text, label=False):
    return W(id, text, label, "answer")


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def RING(line, text, nth=None):
    return M(line, text, "circle", nth)


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_t(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def table(headers, rows, note=None):
    spec = {"kind": "table", "rows": rows}
    if headers:
        spec["headers"] = headers
    if note:
        spec["note"] = note
    return spec


def bar(segments, brace=None):
    """segments: (units, label, tone) tuples."""
    b = {"segments": [{"units": u, "label": l, "tone": t} for (u, l, t) in segments]}
    if brace:
        b["brace"] = brace
    return {"kind": "barModel", "bars": [b]}


# ── Beats and lessons ────────────────────────────────────────────────────────

def ask(right, others, if_not):
    """A 'choose' ask, with the right choice put in a stable but varied place."""
    others = list(others)
    key = (right + "|" + "|".join(others)).encode("utf-8")
    pos = int(hashlib.md5(key).hexdigest()[:8], 16) % (len(others) + 1)
    choices = others[:pos] + [right] + others[pos:]
    return {"kind": "choose", "choices": choices, "answer": pos, "ifNot": if_not}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats):
    return {"origin": "authored", "beats": [b for b in beats if b is not None]}
