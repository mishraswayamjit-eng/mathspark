"""Helpers for the authored-02 lessons (new Grade 5 questions, ids G5A_...).

Board ops are plain dicts in the shape of src/lib/teach/types.ts.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
IDS = os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-2.json")
OUT = os.path.join(ROOT, "data", "teach", "parts", "authored-02.json")


def load_questions():
    sys.path.append(os.path.join(ROOT, "scripts", "bank"))
    import bank  # noqa: E402  (scripts/bank/bank.py)
    with io.open(IDS, encoding="utf-8") as f:
        ids = json.load(f)
    found = {q["id"]: q for q in bank.load_bank(5) if q["id"] in set(ids)}
    return [found[i] for i in ids if i in found]


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


def GIVEN(id, text):
    return LB(id, text, "given")


def ANS(id, text):
    return W(id, text, "answer")


def ANSL(id, text):
    return LB(id, text, "answer")


def _target(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


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


def GROUP(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_target(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats):
    return {"origin": "authored", "beats": list(beats)}


def ANSC(id, text, result):
    """An answer line with its result ringed (the last time it appears): returns the two ops."""
    n = text.count(str(result))
    assert n >= 1, "%r is not in %r" % (result, text)
    return [ANS(id, text), CIRC(id, str(result), n)]


def ANSLC(id, text, result):
    """The same, for an answer line of words."""
    n = text.count(str(result))
    assert n >= 1, "%r is not in %r" % (result, text)
    return [ANSL(id, text), CIRC(id, str(result), n)]
