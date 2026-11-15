"""Shared helpers for the fractions teach-mode lessons (scripts/teach/gen/fractions_*.py)."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of, option_texts  # noqa: E402,F401

OUT = os.path.join(ROOT, "data", "teach", "parts", "fractions.json")


def questions():
    return sorted([q for q in load_grade5() if topic_of(q) == "fractions"], key=lambda q: q["id"])


# ── Stable variety ───────────────────────────────────────────────────────────

def _h(qid, salt):
    return int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)


def pick(qid, salt, options):
    """One of `options`, always the same one for the same question."""
    return options[_h(qid, salt) % len(options)]


# ── How the teacher says a fraction ──────────────────────────────────────────

_COMMON = {(1, 2): "one half", (1, 3): "one third", (2, 3): "two thirds", (1, 4): "one quarter", (3, 4): "three quarters"}


def fr(a, b):
    return _COMMON.get((a, b), "%d over %d" % (a, b))


def cap(s):
    return s[:1].upper() + s[1:]


_SMALL = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths",
          10: "tenths", 11: "elevenths", 12: "twelfths", 13: "thirteenths", 14: "fourteenths", 15: "fifteenths",
          16: "sixteenths", 17: "seventeenths", 18: "eighteenths", 19: "nineteenths"}
_TENS = {2: "twent", 3: "thirt", 4: "fort", 5: "fift", 6: "sixt", 7: "sevent", 8: "eight", 9: "ninet"}
_ONES = {1: "firsts", 2: "seconds", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 7: "sevenths", 8: "eighths", 9: "ninths"}


def pieces(n):
    """The name of pieces of size 1/n: 8 -> 'eighths', 24 -> 'twenty-fourths'."""
    if n in _SMALL:
        return _SMALL[n]
    if 20 <= n < 100:
        t, o = divmod(n, 10)
        return _TENS[t] + ("ieths" if o == 0 else "y-" + _ONES[o])
    return "equal pieces"


# ── Board operations ─────────────────────────────────────────────────────────

def W(i, text, tone=None, label=False):
    d = {"op": "write", "id": i, "text": text}
    if tone:
        d["tone"] = tone
    if label:
        d["label"] = True
    return d


def T(text, nth=1):
    d = {"text": text}
    if nth > 1:
        d["nth"] = nth
    return d


def TA(line, sub, pos):
    """The target for the occurrence of `sub` that starts at index `pos` of `line`."""
    assert line[pos:pos + len(sub)] == sub, (line, sub, pos)
    return T(sub, line.count(sub, 0, pos) + 1)


def MARK(line, text, shape="underline", nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": shape}


def MARKT(line, target, shape="underline"):
    return {"op": "mark", "line": line, "target": target, "shape": shape}


def NOTE(line, text, note, place=None, nth=1):
    d = {"op": "note", "line": line, "target": T(text, nth), "text": note}
    if place:
        d["place"] = place
    return d


def NOTET(line, target, note, place=None):
    d = {"op": "note", "line": line, "target": target, "text": note}
    if place:
        d["place"] = place
    return d


def STRIKE(line, text, note=None, nth=1):
    d = {"op": "strike", "line": line, "target": T(text, nth)}
    if note:
        d["note"] = note
    return d


def STRIKET(line, target, note=None):
    d = {"op": "strike", "line": line, "target": target}
    if note:
        d["note"] = note
    return d


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIVIDE(line, by):
    return {"op": "divide", "line": line, "by": by}


def GROUP(line, targets, label=None):
    d = {"op": "group", "line": line, "targets": targets}
    if label:
        d["label"] = label
    return d


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": frm, "to": to}


def FIG(i, spec):
    return {"op": "figure", "id": i, "spec": spec}


def bars(*items, **kw):
    """fractionBars from (parts, shaded, label) tuples."""
    spec = {"kind": "fractionBars", "bars": []}
    for parts, shaded, label in items:
        b = {"parts": parts, "shaded": shaded}
        if label:
            b["label"] = label
        spec["bars"].append(b)
    spec.update(kw)
    return spec


# ── Beats and asks ───────────────────────────────────────────────────────────

def B(say, *board, **kw):
    beat = {"say": say}
    if board:
        beat["board"] = list(board)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def CH(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


THINK = {"kind": "think"}


def choose(qid, salt, right, others, if_not):
    """A choose-ask with the right choice in a position that depends on the question."""
    items = [right] + [o for o in others if o != right]
    seen = []
    for it in items:
        if it not in seen:
            seen.append(it)
    k = _h(qid, salt) % len(seen)
    order = seen[k:] + seen[:k]
    return CH(order, order.index(right), if_not)


def lesson(beats, origin, check=None):
    d = {"origin": origin}
    if check:
        d["check"] = {"variable": check[0], "value": str(check[1])}
    d["beats"] = beats
    return d
