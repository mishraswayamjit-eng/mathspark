"""Helpers for the imported-17 lessons (number series; speed, distance and time).

Board ops are plain dicts in the shape of src/lib/teach/types.ts.
"""
import hashlib

MINUS = "−"


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
    op = {"op": "group", "line": line, "targets": [_target(*t) if isinstance(t, tuple) else _target(t) for t in targets]}
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


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def count_upto(text, sub, pos):
    """Which occurrence of `sub` (counted the way str.count does) starts at `pos`."""
    n = 0
    i = text.find(sub)
    while i != -1:
        n += 1
        if i == pos:
            return n
        if i > pos:
            break
        i = text.find(sub, i + len(sub))
    n = 0
    i = text.find(sub)
    while i != -1:
        n += 1
        if i == pos:
            return n
        i = text.find(sub, i + 1)
    raise ValueError("%r is not at %d in %r" % (sub, pos, text))


class Series(object):
    """A series written on one line, so a mark can point at its k-th term."""

    def __init__(self, id, terms, tail=""):
        self.id = id
        self.terms = [str(t) for t in terms]
        self.text = ", ".join(self.terms) + tail
        self.starts = []
        pos = 0
        for t in self.terms:
            self.starts.append(pos)
            pos += len(t) + 2

    def nth(self, k):
        return count_upto(self.text, self.terms[k], self.starts[k])

    def given(self):
        return GIVEN(self.id, self.text)

    def label(self, tone=None):
        return LB(self.id, self.text, tone)

    def note(self, k, text, place="above"):
        return NOTE(self.id, self.terms[k], text, place, self.nth(k))

    def mark(self, k, shape="circle"):
        return MARK(self.id, self.terms[k], shape, self.nth(k))

    def strike(self, k, note=None):
        return STRIKE(self.id, self.terms[k], note, self.nth(k))


def say_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]
