"""Small helpers for writing measurement-speed lessons: beats, board ops, asks.

Used by measurement_speed_rules.py (generated families) and
measurement_speed_authored.py (one-off questions).
"""
import hashlib


def pick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id."""
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def given(id, text, label=True):
    op = {"op": "write", "id": id, "text": text, "tone": "given"}
    if label:
        op["label"] = True
    return op


def w(id, text):
    """A line of working that is plain maths (the checker verifies it)."""
    return {"op": "write", "id": id, "text": text}


def lab(id, text):
    """A line of words: a fact, a formula in words, a result with its unit."""
    return {"op": "write", "id": id, "text": text, "label": True}


def answer(id, text):
    return {"op": "write", "id": id, "text": text, "tone": "answer", "label": True}


def _target(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def ring(line, text):
    return mark(line, text, "circle")


def note(line, target, text, place=None, nth=None):
    op = {"op": "note", "line": line, "target": _target(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def strike(line, target, note_text=None, nth=None):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note_text:
        op["note"] = note_text
    return op


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_target(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def fig(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


# ── Beats and asks ───────────────────────────────────────────────────────────

def beat(say, *ops, **kw):
    b = {"say": say}
    if ops:
        b["board"] = list(ops)
    if kw.get("ask"):
        b["ask"] = kw["ask"]
    return b


def choose(key, right, others, if_not):
    """A 'choose' ask. The right choice is put at a place fixed by `key` (question id plus a salt)."""
    choices = list(others)
    at = pick(key, "place", list(range(len(choices) + 1)))
    choices.insert(at, right)
    return {"kind": "choose", "choices": choices, "answer": at, "ifNot": if_not}


def think():
    return {"kind": "think"}


def lesson(origin, beats):
    return {"origin": origin, "beats": beats}
