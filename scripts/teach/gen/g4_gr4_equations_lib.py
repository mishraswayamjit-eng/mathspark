"""Small helpers for writing Grade 4 equations lessons. Used by the other g4_gr4_equations_*.py files.

A lesson is built from beats: B("what the teacher says", op, op, ..., ask=choose(...)).
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

TOPIC = "gr4_equations"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


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


def L(id, text):
    """A line of words."""
    return W(id, text, None, True)


_TV = None


def _teach_validate():
    """The lesson checker, loaded under its own name (it imports another module called validate)."""
    global _TV
    if _TV is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
        _TV = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_TV)
    return _TV


def E(id, text, vals, tone=None):
    """A line of maths the checker cannot read (a capital letter, a star, two unknowns, or an
    unknown that is not the keyed answer). It goes on the board as a label, but only after it
    has been checked here: every unknown is replaced by its value and the line must be true."""
    probe = text
    for k, v in vals.items():
        probe = probe.replace(k, "(%s)" % v)
    matter = _teach_validate().check_line(probe, None, None)
    if matter:
        raise ValueError("%r with %r %s" % (text, vals, matter))
    return W(id, text, tone, True)


def fig(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def balance(id, left, right):
    return fig(id, {"kind": "balance", "left": left, "right": right})


def bars(id, *rows, note=None):
    """A bar model. Each row is (label, [(units, label, tone), ...]) or (label, [...], brace)."""
    out = []
    for row in rows:
        bar = {"segments": [dict(units=u, label=l, tone=t) if l is not None else dict(units=u, tone=t)
                            for (u, l, t) in row[1]]}
        if row[0]:
            bar["label"] = row[0]
        if len(row) > 2:
            bar["brace"] = row[2]
        out.append(bar)
    spec = {"kind": "barModel", "bars": out}
    if note:
        spec["note"] = note
    return fig(id, spec)


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
    return {"kind": "choose", "choices": [str(c) for c in choices], "answer": right, "ifNot": if_not}


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


def spread_answers(qid, script):
    """Rotate each hand-written ask in a stable way, so the right choice is not always first."""
    for i, beat in enumerate(script["beats"]):
        ask = beat.get("ask")
        if not ask or ask.get("kind") != "choose":
            continue
        choices = ask["choices"]
        right = choices[ask["answer"]]
        k = pick(qid, "spread%d" % i, list(range(len(choices))))
        ask["choices"] = choices[k:] + choices[:k]
        ask["answer"] = ask["choices"].index(right)
