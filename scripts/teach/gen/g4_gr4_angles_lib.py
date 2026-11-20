"""Small helpers for writing Grade 4 angles lessons (teach mode). Used by the other
g4_gr4_angles_* scripts. (Copied from the Grade 5 geometry helper.)

A lesson is built from beats: B("what the teacher says", op, op, ..., ask=...).
Board ops are made with W (write), L (a line of words), FIG (figure), mark, note, strike.
"""
import hashlib
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
# scripts/teach/validate.py imports the figure checker under the name "validate", so it is
# loaded here under another name to keep the two apart.
_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
teach_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(teach_check)


def hpick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id and a salt."""
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


def hnum(qid, salt, n):
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def L(id, text, tone=None):
    """A line of words (or of maths with a degree sign, which the checker reads as words)."""
    return W(id, text, tone=tone, label=True)


def G(id, text):
    """The question, as the first line on the board."""
    return W(id, text, tone="given", label=True)


def A(id, text):
    """The final answer line."""
    return W(id, text, tone="answer", label=True)


def FIG(id, **spec):
    return {"op": "figure", "id": id, "spec": spec}


def angles(id, layout, parts, note=None, highlight=None):
    """An angles figure. parts: (label, size) pairs or (label,) for the unknown."""
    spec = {"kind": "angles", "layout": layout,
            "parts": [({"label": p[0], "size": p[1]} if len(p) > 1 and p[1] is not None else {"label": p[0]}) for p in parts]}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return {"op": "figure", "id": id, "spec": spec}


def clock(id, hour, minute, show=True, note=None, highlight=None):
    spec = {"kind": "clock", "hour": hour, "minute": minute}
    if show:
        spec["showAngle"] = True
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return {"op": "figure", "id": id, "spec": spec}


def compass(id, facing, turns=None, end=False, note=None, highlight=None):
    """turns: list of (degrees, 'c' or 'a')."""
    spec = {"kind": "compass", "facing": facing}
    if turns:
        spec["turns"] = [{"degrees": d, "direction": "clockwise" if w == "c" else "anticlockwise"} for d, w in turns]
    if end:
        spec["showEnd"] = True
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return {"op": "figure", "id": id, "spec": spec}


def T(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": shape}


def ring(line, text, nth=None):
    return mark(line, text, "circle", nth)


def box(line, text, nth=None):
    return mark(line, text, "box", nth)


def note(line, target, text, place=None, nth=None):
    op = {"op": "note", "line": line, "target": T(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def strike(line, target, text=None, nth=None):
    op = {"op": "strike", "line": line, "target": T(target, nth)}
    if text:
        op["note"] = text
    return op


def both(line, text):
    return {"op": "both", "line": line, "text": text}


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def ask(key, right, slips, if_not):
    """A choose-ask with the right choice placed by a stable hash, so it is not always first."""
    pos = hnum(key, "pos", len(slips) + 1)
    choices = list(slips)
    choices.insert(pos, right)
    return choose(choices, pos, if_not)


THINK = {"kind": "think"}


def lesson(beats, origin="authored", check=None):
    out = {"origin": origin, "beats": beats}
    if check:
        out["check"] = {"variable": check[0], "value": str(check[1])}
    return out
