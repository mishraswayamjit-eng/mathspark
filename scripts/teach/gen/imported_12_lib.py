"""Helpers for the imported-12 lessons (multiplication and division stories, percent and money).

Board ops are plain dicts in the shape of src/lib/teach/types.ts. Every line of
working is written through E() or A(), which compute the right-hand side, so a
line cannot be mistyped into something false.
"""
import hashlib
import re
from fractions import Fraction

MINUS = "−"


# ── Numbers ──────────────────────────────────────────────────────────────────

def n(x):
    """A whole number the way the child sees it: plain up to 9999, Indian commas above."""
    x = Fraction(x)
    if x.denominator != 1:
        return ("%f" % float(x)).rstrip("0").rstrip(".")
    x = int(x)
    s = str(x)
    if x < 10000:
        return s
    head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return ",".join(groups + [tail])


def val(expr):
    """The exact value of a line of plain maths."""
    s = expr.replace(",", "").replace("₹", "")
    s = s.replace("% of", "/100*").replace("×", "*").replace("÷", "/").replace(MINUS, "-")
    s = re.sub(r"\d+(?:\.\d+)?", lambda m: "Fraction('%s')" % m.group(0), s)
    return eval(s, {"Fraction": Fraction})


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    return op


def LB(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text, "label": True}
    if tone:
        op["tone"] = tone
    return op


def G(id, text):
    """The question, in words, as the first thing on the board."""
    return LB(id, text, "given")


def GM(id, text):
    """The question when it is a line of maths."""
    return W(id, text, "given")


def E(id, expr):
    """A line of working: the sum, an equals sign, and its computed value."""
    return W(id, "%s = %s" % (expr, n(val(expr))))


def _target(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


def last_nth(text, sub):
    """Which occurrence (counted as str.count counts) is the last one."""
    return text.count(sub)


def nth_at(text, sub, pos):
    """Which occurrence of `sub` (counted without overlaps, as str.count does) starts at `pos`."""
    count = 0
    i = text.find(sub)
    while i != -1:
        count += 1
        if i == pos:
            return count
        i = text.find(sub, i + len(sub))
    raise ValueError("%r is not a clean match at %d in %r" % (sub, pos, text))


def MARK(line, text, shape="circle", nth=1):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def CIRC(line, text, nth=1):
    return MARK(line, text, "circle", nth)


def UL(line, text, nth=1):
    return MARK(line, text, "underline", nth)


def BOX(line, text, nth=1):
    return MARK(line, text, "box", nth)


def NOTE(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": _target(target, nth), "text": str(text), "place": place}


def STRIKE(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note:
        op["note"] = note
    return op


def A(id, expr):
    """The answer line, computed, with its result ringed. Use as *A(...)."""
    res = n(val(expr))
    text = "%s = %s" % (expr, res)
    assert text.endswith(res)
    # The ring goes round the result: the last place that text appears.
    count = 0
    i = text.find(res)
    while i != -1:
        count += 1
        if i == len(text) - len(res):
            break
        i = text.find(res, i + len(res))
    if i != len(text) - len(res):
        # Overlapping earlier match: ring the whole line instead.
        return [W(id, text, "answer"), CIRC(id, text)]
    return [W(id, text, "answer"), CIRC(id, res, count)]


def AL(id, text, ring):
    """An answer that is words (a label), with part of it ringed. Use as *AL(...)."""
    return [LB(id, text, "answer"), CIRC(id, ring)]


def CH(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def B(say, *ops, **kw):
    beat = {"say": say}
    flat = []
    for op in ops:
        if isinstance(op, list):
            flat.extend(op)
        else:
            flat.append(op)
    if flat:
        beat["board"] = flat
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats):
    flat = []
    for b in beats:
        if isinstance(b, list):
            flat.extend(b)
        else:
            flat.append(b)
    return {"origin": "authored", "beats": flat}


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def shuffled(qid, salt, right, others):
    """Choices with the right one at a stable, id-dependent place. Returns (choices, index)."""
    at = pick(qid, salt, list(range(len(others) + 1)))
    choices = list(others)
    choices.insert(at, right)
    return choices, at


# ── Multiplying by splitting one number ──────────────────────────────────────

def split_times(a, b, p1, sign, p2, ids, lead, mid=None, end=None, final=False):
    """Three beats that teach a × b with b split as p1 + p2 or p1 − p2.

    `lead` is what the teacher says as the split is written. `mid` and `end`
    replace the default words for the two products and for putting them together.
    """
    assert sign in ("+", MINUS)
    assert (p1 + p2 if sign == "+" else p1 - p2) == b, (a, b, p1, p2)
    x, y = a * p1, a * p2
    z = a * b
    split = "%s × %s = %s × %s %s %s × %s" % (n(a), n(b), n(a), n(p1), sign, n(a), n(p2))
    if mid is None:
        mid = "%s times %s is %s, and %s times %s is %s." % (n(a), n(p1), n(x), n(a), n(p2), n(y))
    if end is None:
        if sign == "+":
            end = "Now put the two pieces together. %s plus %s is %s." % (n(x), n(y), n(z))
        else:
            end = "Now take the second piece from the first. %s minus %s is %s." % (n(x), n(y), n(z))
    last = "%s %s %s" % (n(x), sign, n(y))
    at1 = len("%s × %s = %s × " % (n(a), n(b), n(a)))
    at2 = len(split) - len(n(p2))
    return [
        B(lead, W(ids + "s", split), UL(ids + "s", n(p1), nth_at(split, n(p1), at1)),
          UL(ids + "s", n(p2), nth_at(split, n(p2), at2))),
        B(mid, E(ids + "a", "%s × %s" % (n(a), n(p1))), E(ids + "b", "%s × %s" % (n(a), n(p2)))),
        B(end, A(ids, last) if final else E(ids, last)),
    ]
