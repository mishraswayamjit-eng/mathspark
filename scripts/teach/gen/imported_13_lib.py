"""Helpers for the imported-13 lessons: board ops, beats, and number text."""
import hashlib
import io
import json
import os
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "data", "bank-import", "lessons", "in-13.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-13.json")

P = "AIGEN_grade5_"


def batch():
    with io.open(SRC, encoding="utf-8") as f:
        return {q["id"]: q for q in json.load(f)}


# ── Number text ──────────────────────────────────────────────────────────────

def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


def gi(n):
    """A whole number with Indian grouping: 3000 -> 3,000; 454321 -> 4,54,321."""
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


def mon(x):
    """Money: whole rupees with commas (1,200), or two decimal places (67.50)."""
    x = D(x)
    if x == x.to_integral_value():
        return gi(int(x))
    return format(x.quantize(Decimal("0.01")), "f")


def rs(x):
    return "₹" + mon(x)


def paise_words(x):
    """67.50 -> '67 rupees 50 paise' (for a note on the board, so it can be said)."""
    x = D(x)
    whole = int(x)
    paise = int((x - whole) * 100)
    return "%d rupees %d paise" % (whole, paise)


def lakh_words(n):
    """660000 -> '6 lakh 60 thousand'; 399980 -> '3 lakh 99 thousand 980'; 700000 -> '7 lakh'."""
    n = int(n)
    lakh, rest = divmod(n, 100000)
    thousand, last = divmod(rest, 1000)
    words = ["%d lakh" % lakh]
    if thousand:
        words.append("%d thousand" % thousand)
    if last:
        words.append(str(last))
    return " ".join(words)


def pick(qid, salt, options):
    """One of the options, chosen by a stable hash of the question id."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest()[:8], 16)
    return options[h % len(options)]


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


def chart(number, *digits):
    """A place-value chart of the number, with the digits at these positions (from the left) lit."""
    spec = {"kind": "placeChart", "number": str(number)}
    if digits:
        spec["highlight"] = ["d%d" % d for d in digits]
    return spec


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
    flat = []
    for b in beats:
        if b is None:
            continue
        if isinstance(b, list):
            flat.extend(x for x in b if x is not None)
        else:
            flat.append(b)
    return {"origin": "authored", "beats": flat}
