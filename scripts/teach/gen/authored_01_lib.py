"""Helpers for the authored-01 lessons (new Grade 5 questions: algebra, angles, BODMAS, decimals).

Board ops are plain dicts in the shape of src/lib/teach/types.ts.
"""


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


def LANS(id, text):
    """An answer line that is words (or has two letters), so it is a label."""
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


def ARC(line, frm, to, frm_nth=1):
    """`to` is a list of texts, or of (text, nth) pairs."""
    tos = [_target(*t) if isinstance(t, tuple) else _target(t) for t in to]
    return {"op": "arc", "line": line, "from": _target(frm, frm_nth), "to": tos}


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIVIDE(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


def GROUP(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_target(*t) if isinstance(t, tuple) else _target(t) for t in targets]}
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


def LESSON(*beats, **kw):
    lesson = {"origin": "authored", "beats": list(beats)}
    if kw.get("check"):
        variable, value = kw["check"]
        lesson = {"origin": "authored", "check": {"variable": variable, "value": str(value)}, "beats": list(beats)}
    return lesson


def last_nth(text, sub):
    """Which occurrence of `sub` is the last one in `text` (for circling the result of a line)."""
    n = text.count(sub)
    assert n >= 1, "%r is not in %r" % (sub, text)
    return n


def ANSC(id, text, result):
    """An answer line with its result ringed: returns the two ops."""
    return [ANS(id, text), CIRC(id, str(result), last_nth(text, str(result)))]
