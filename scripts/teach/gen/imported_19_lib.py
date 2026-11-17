"""Small helpers for the imported-19 lessons (board ops, beats, stable picks)."""
import hashlib
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-19.json")
SOURCE = os.path.join(ROOT, "data", "bank-import", "lessons", "in-19.json")


def source_ids():
    with io.open(SOURCE, encoding="utf-8") as f:
        return [q["id"] for q in json.load(f)]


def num(v):
    """A whole number as it is written and said: 961, 1,024, 10,000."""
    s = str(int(v))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return ",".join(groups + [tail])


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


def L(id, text):
    """A line of words."""
    return W(id, text, None, True)


def GIVEN(id, text, label=True):
    return W(id, text, "given", label)


def ANS(id, text, label=False):
    return W(id, text, "answer", label)


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def ANSR(id, text, target, label=False):
    """Write the answer line and ring the LAST place `target` appears on it."""
    count = text.count(target)
    if count < 1:
        raise ValueError("%r is not on %r" % (target, text))
    return [ANS(id, text, label), M(id, target, "circle", count)]


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
    return {"op": "arc", "line": line, "from": _t(*frm) if isinstance(frm, tuple) else _t(frm),
            "to": [_t(*t) if isinstance(t, tuple) else _t(t) for t in to]}


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def TRI(shape="scalene", angles=None, sides=None, highlight=None):
    spec = {"kind": "triangle", "shape": shape}
    if angles:
        spec["angles"] = dict(zip("abc", angles)) if isinstance(angles, (list, tuple)) else angles
    if sides:
        spec["sides"] = sides
    if highlight:
        spec["highlight"] = highlight
    return spec


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


def lesson(*beats, **kw):
    out = {"origin": "authored"}
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
    """Choices with the right one in a stable but varied position. Returns (choices, index)."""
    others = list(others)
    pos = h(qid, salt) % (len(others) + 1)
    return others[:pos] + [right] + others[pos:], pos


def ask(qid, salt, right, others, if_not):
    choices, idx = placed(qid, salt, right, others)
    return choose(choices, idx, if_not)
