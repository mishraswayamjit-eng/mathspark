"""Small helpers for writing algebra lessons. Used by the other algebra_*.py files.

A lesson is built from beats: B("what the teacher says", op, op, ..., ask=choose(...)).
"""
import hashlib


def T(text, nth=1):
    """A place on a line."""
    return {"text": text, "nth": nth} if nth != 1 else {"text": text}


def _t(x):
    if isinstance(x, dict):
        return x
    if isinstance(x, tuple):
        return T(x[0], x[1])
    return T(x)


def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def given(id, text, label=False):
    return W(id, text, "given", label)


def answer(id, text, label=False):
    return W(id, text, "answer", label)


def arc(line, frm, *to):
    return {"op": "arc", "line": line, "from": _t(frm), "to": [_t(x) for x in to]}


def strike(line, target, note=None):
    op = {"op": "strike", "line": line, "target": _t(target)}
    if note:
        op["note"] = note
    return op


def note(line, target, text, place=None):
    op = {"op": "note", "line": line, "target": _t(target), "text": text}
    if place:
        op["place"] = place
    return op


def mark(line, target, shape="circle"):
    return {"op": "mark", "line": line, "target": _t(target), "shape": shape}


def both(line, text):
    return {"op": "both", "line": line, "text": text}


def divide(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_t(x) for x in targets]}
    if label:
        op["label"] = label
    return op


def choose(choices, right, if_not):
    """`right` is the index of the right choice."""
    return {"kind": "choose", "choices": list(choices), "answer": right, "ifNot": if_not}


THINK = {"kind": "think"}


def B(say, *ops, ask=None):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if ask is not None:
        beat["ask"] = ask
    return beat


def lesson(beats, var=None, value=None, origin="authored"):
    out = {"origin": origin}
    if var is not None:
        out["check"] = {"variable": var, "value": str(value)}
    out["beats"] = beats
    return out


def pick(qid, salt, options):
    """A stable choice among alternatives, so a family does not repeat itself."""
    h = hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


def shuffled(qid, salt, choices, right=0):
    """Rotate the choices in a stable way. Returns (choices, index of the right one)."""
    k = pick(qid, salt, list(range(len(choices))))
    rotated = choices[k:] + choices[:k]
    return rotated, rotated.index(choices[right])


def nth_at(line, text, pos):
    """Which occurrence of `text` starts at index `pos` of `line` (1-based)."""
    n, i = 0, -1
    while True:
        i = line.find(text, i + 1)
        if i < 0 or i > pos:
            break
        n += 1
        if i == pos:
            return n
    raise ValueError("%r is not at %d in %r" % (text, pos, line))
