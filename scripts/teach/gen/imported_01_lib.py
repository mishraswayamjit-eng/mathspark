"""Small helpers for the imported-01 lessons (board ops, beats, stable picks, number formatting)."""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-01.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-01.json")

AI = "AIGEN_grade5_"
TB = "IPMTB_grade5_"


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


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, **spec):
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
            ops.extend(op)
        else:
            ops.append(op)
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats, **kw):
    out = {"origin": "authored"}
    if kw.get("check"):
        out["check"] = {"variable": kw["check"][0], "value": str(kw["check"][1])}
    flat = []
    for b in beats:
        if b is None:
            continue
        if isinstance(b, list):
            flat.extend(x for x in b if x is not None)
        else:
            flat.append(b)
    out["beats"] = flat
    return out


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


# ── Numbers ──────────────────────────────────────────────────────────────────

def num(v):
    """A number as it is written on the board: 115, 57.5."""
    if float(v) == int(v):
        return str(int(v))
    return ("%f" % float(v)).rstrip("0").rstrip(".")


def take_away_lines(prefix, total, a):
    """total − a done in two easy steps (tens, then ones). Returns (ops, words)."""
    tens, ones = (a // 10) * 10, a % 10
    mid, end = total - tens, total - a
    if ones == 0 or tens == 0:
        return [W(prefix + "a", "%d − %d = %d" % (total, a, end))], "%d minus %d is %d." % (total, a, end)
    ops = [W(prefix + "a", "%d − %d = %d" % (total, tens, mid)), W(prefix + "b", "%d − %d = %d" % (mid, ones, end))]
    words = "Take off %d first, which leaves %d. Then %d more, and we land on %d." % (tens, mid, ones, end)
    return ops, words


def count_up_lines(prefix, total, a):
    """total − a found by counting up from a to total. Returns (ops, words)."""
    end = total - a
    step = (10 - a % 10) % 10
    if step == 0:
        return [W(prefix + "a", "%d + %d = %d" % (a, end, total))], "From %d up to %d is %d." % (a, total, end)
    mid = a + step
    rest = total - mid
    ops = [W(prefix + "a", "%d + %d = %d" % (a, step, mid)), W(prefix + "b", "%d + %d = %d" % (mid, rest, total)),
           W(prefix + "c", "%d + %d = %d" % (step, rest, end))]
    words = "Count up from %d. A hop of %d reaches %d, then %d more reaches %d. The two hops together make %d." % (
        a, step, mid, rest, total, end)
    return ops, words


def half_lines(prefix, n):
    """n ÷ 2 by halving the tens and the ones separately. Returns (ops, words, half)."""
    half = n / 2.0
    tens, ones = (n // 10) * 10, n % 10
    if ones == 0:
        return [W(prefix + "a", "%d ÷ 2 = %s" % (n, num(half)))], "Half of %d is %s." % (n, num(half)), half
    ops = [W(prefix + "a", "%d ÷ 2 = %s" % (tens, num(tens / 2.0))), W(prefix + "b", "%d ÷ 2 = %s" % (ones, num(ones / 2.0))),
           W(prefix + "c", "%s + %s = %s" % (num(tens / 2.0), num(ones / 2.0), num(half)))]
    words = "Half of %d is %s, and half of %d is %s. Together that makes %s." % (
        tens, num(tens / 2.0), ones, num(ones / 2.0), num(half))
    return ops, words, half
