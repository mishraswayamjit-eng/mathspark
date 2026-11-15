"""Small helpers shared by the arithmetic lesson scripts (board ops, beats, stable picks)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

PART = os.path.join(ROOT, "data", "teach", "parts", "arithmetic.json")


def questions():
    return {q["id"]: q for q in load_grade5() if topic_of(q) == "arithmetic"}


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


def GIVEN(id, text, label=False):
    return W(id, text, "given", label)


def ANS(id, text, label=False):
    return W(id, text, "answer", label)


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


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


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _t(frm),
            "to": [_t(*t) if isinstance(t, tuple) else _t(t) for t in to]}


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


CLEAR = {"op": "clear"}


# ── Beats and lessons ────────────────────────────────────────────────────────

def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


THINK = {"kind": "think"}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats, **kw):
    out = {"origin": kw.get("origin", "authored")}
    if kw.get("check"):
        out["check"] = {"variable": kw["check"][0], "value": str(kw["check"][1])}
    out["beats"] = [b for b in beats if b is not None]
    return out


# ── Stable variety ───────────────────────────────────────────────────────────

def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    """One of `options`, the same every run for this question and salt."""
    return options[h(qid, salt) % len(options)]


def placed(qid, salt, right, others):
    """Choices with the right one put in a stable but varied position. Returns (choices, index)."""
    others = list(others)
    pos = h(qid, salt) % (len(others) + 1)
    choices = others[:pos] + [right] + others[pos:]
    return choices, pos


def nth_at(line, sub, start=0):
    """Which occurrence (1-based) of `sub` on `line` is the first one at or after `start`."""
    at = line.find(sub, start)
    if at < 0:
        raise ValueError("%r is not on the line %r after %d" % (sub, line, start))
    n, i = 0, 0
    while True:
        j = line.find(sub, i)
        if j < 0 or j > at:
            break
        n += 1
        if j == at:
            break
        i = j + len(sub)
    return n
