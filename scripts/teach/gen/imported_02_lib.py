"""Board ops and beat helpers for the imported-02 lessons."""


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


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
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


def num(v):
    """A number as it is written on the board: 3915 -> '3,915', 870000 -> '8,70,000', 60.75 -> '60.75'."""
    if isinstance(v, float) and v != int(v):
        s = ("%f" % v).rstrip("0").rstrip(".")
        whole, frac = s.split(".")
        return num(int(whole)) + "." + frac
    n = int(v)
    s = str(n)
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
