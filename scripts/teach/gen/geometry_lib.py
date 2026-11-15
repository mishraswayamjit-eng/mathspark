"""Small helpers for writing geometry lessons (teach mode). Used by the other geometry_* scripts.

A lesson is built from beats: B("what the teacher says", op, op, ..., ask=...).
Board ops are made with W (write), FIG (figure), mark, note, strike, both, divide, group, arc.
"""
import hashlib
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# scripts/teach/validate.py imports the figure checker under the name "validate", so it is
# loaded here under another name to keep the two apart.
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
teach_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(teach_check)


# ── Stable choices, so a family does not sound the same five times in a row ──

def hpick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id and a salt."""
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


def hnum(qid, salt, n):
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def fmt(v):
    """A number as it is written: 70, 93.5, 7.7."""
    f = Fraction(v).limit_denominator(1000)
    if f.denominator == 1:
        return str(f.numerator)
    return ("%.3f" % float(f)).rstrip("0").rstrip(".")


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def verify(text, values):
    """True if the line holds when each letter in `values` is replaced by its number."""
    s = text
    for letter, v in values.items():
        s = s.replace(letter, "(%s)" % v)
    return teach_check.check_line(s, None, None) is None


def LV(id, text, *value_sets, **kw):
    """A line with letters in it, written as a label because the lesson's keyed answer is
    not the letter's value. It is verified here instead: it must hold for every value set."""
    for values in value_sets:
        if not verify(text, values):
            raise ValueError("line does not hold: %r with %r" % (text, values))
    if not value_sets:
        raise ValueError("LV needs values to verify with: %r" % text)
    return W(id, text, tone=kw.get("tone"), label=True)


def FIG(id, **spec):
    return {"op": "figure", "id": id, "spec": spec}


def T(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": shape}


def note(line, target, text, place=None, nth=None):
    op = {"op": "note", "line": line, "target": T(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def strike(line, target, text=None, nth=None):
    op = {"op": "strike", "line": line, "target": T(target, nth)}
    if text:
        op["note"] = text
    return op


def both(line, text):
    return {"op": "both", "line": line, "text": text}


def divide(line, by):
    return {"op": "divide", "line": line, "by": by}


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": frm if isinstance(frm, dict) else T(frm),
            "to": [t if isinstance(t, dict) else T(t) for t in to]}


# ── Beats and asks ───────────────────────────────────────────────────────────

def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def ask(key, right, slips, if_not):
    """A choose-ask with the right choice placed by a stable hash, so it is not always first."""
    pos = hnum(key, "pos", len(slips) + 1)
    choices = list(slips)
    choices.insert(pos, right)
    return choose(choices, pos, if_not)


THINK = {"kind": "think"}


def lesson(beats, origin, check=None):
    out = {"origin": origin, "beats": beats}
    if check:
        out["check"] = {"variable": check[0], "value": str(check[1])}
    return out
