"""Small helpers for the imported-03 lessons (board ops, beats, numbers, stable picks)."""
import hashlib
import io
import json
import os
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-03.json")
SOURCE = os.path.join(ROOT, "data", "bank-import", "lessons", "in-03.json")


def source_ids():
    with io.open(SOURCE, encoding="utf-8") as f:
        return [q["id"] for q in json.load(f)]


# ── Numbers ──────────────────────────────────────────────────────────────────

def D(x):
    return Decimal(str(x))


def n(x):
    """A number as it is written on the board and said: 120, 5.3, 0.09 (no trailing zeros)."""
    if isinstance(x, Decimal):
        if x == x.to_integral_value():
            return str(int(x))
        return format(x.normalize(), "f")
    return str(x)


# ── Board ops ────────────────────────────────────────────────────────────────

def _t(text, nth=None):
    t = {"text": text}
    if nth and nth > 1:
        t["nth"] = nth
    return t


def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def GIVEN(id, text, label=True):
    return W(id, text, "given", label)


def ANS(id, text, label=False):
    return W(id, text, "answer", label)


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def RING(line, line_text, target):
    """Ring the LAST place `target` appears on the line (the result, not a number inside the sum)."""
    count = line_text.count(target)
    if count < 1:
        raise ValueError("%r is not on %r" % (target, line_text))
    return M(line, target, "circle", count)


def ANSR(id, text, target, label=False):
    """Write the answer line and ring the answer on it."""
    return [ANS(id, text, label), RING(id, text, target)]


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def NR(line, line_text, target, text, place="below"):
    """A note on the LAST place `target` appears on the line."""
    return N(line, target, text, place, line_text.count(target))


def WN(id, text, target, note):
    """Write a line of working and label its result."""
    return [W(id, text), NR(id, text, target, note)]


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_t(*t) if isinstance(t, tuple) else _t(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


# ── Beats and lessons ────────────────────────────────────────────────────────

def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = []
    for op in board:
        if op is None:
            continue
        if isinstance(op, list):
            ops.extend(o for o in op if o is not None)
        else:
            ops.append(op)
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats):
    return {"origin": "authored", "beats": [b for b in beats if b is not None]}


# ── Stable variety ───────────────────────────────────────────────────────────

def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    """One of `options`, the same every run for this question and salt."""
    return options[h(qid, salt) % len(options)]


def placed(qid, salt, right, others):
    """Choices with the right one in a stable but varied position. Returns (choices, index)."""
    others = list(others)
    pos = h(qid, salt) % (len(others) + 1)
    return others[:pos] + [right] + others[pos:], pos
