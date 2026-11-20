"""Small helpers for writing Grade 4 triangle lessons (teach mode).

A lesson is built from beats: B("what the teacher says", op, op, ..., ask=...).
Board ops: W (write; a line of plain maths is verified here, a line with words is a label),
ANS (the answer line, ringed), FIG / tri / QF (figures), mark, note, strike, group, arc.
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TOPIC = "gr4_triangles"

# scripts/teach/validate.py imports the figure checker under the name "validate", so it is
# loaded here under another name to keep the two apart.
_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
teach_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(teach_check)

sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


_FIGS = None


def question_figures():
    global _FIGS
    if _FIGS is None:
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)
        _FIGS = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                _FIGS = json.load(f)
    return _FIGS


# ── Stable choices, so a family does not sound the same five times in a row ──

def hnum(qid, salt, n):
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def hpick(qid, salt, options):
    return options[hnum(qid, salt, len(options))]


# ── Board ops ────────────────────────────────────────────────────────────────

_WORDS = re.compile(r"[A-Za-z]{2,}|[A-Za-z]\b")


def W(id, text, tone=None, label=None):
    """Write a line. A line with words in it is a label; a line of plain maths must be true."""
    if label is None:
        label = bool(_WORDS.search(re.sub(r"\bof\b", "", text))) or "°" in text
    if not label:
        matter = teach_check.check_line(text, None, None)
        if matter and "not plain maths" in matter:
            label = True   # a list such as "3, 5, 7"
        elif matter:
            raise ValueError("line %r %s" % (text, matter))
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def G(id, text):
    """The question, as the first thing on the board."""
    return W(id, text, tone="given")


def T(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": shape}


def ANS(id, text, ring=None):
    """The answer line, written large and ringed."""
    return [W(id, text, tone="answer"), mark(id, ring or text, "circle")]


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


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": frm if isinstance(frm, dict) else T(frm),
            "to": [t if isinstance(t, dict) else T(t) for t in to]}


# ── Figures ──────────────────────────────────────────────────────────────────

def FIG(**spec):
    return {"op": "figure", "id": "", "spec": spec}


def tri(shape="scalene", a=None, b=None, c=None, ab=None, bc=None, ca=None, height=None, note=None, hl=None,
        enclose=None):
    """A triangle. a is the top corner, b bottom left, c bottom right; ab, bc, ca are the sides."""
    spec = {"kind": "triangle", "shape": shape}
    angles = {k: v for k, v in (("a", a), ("b", b), ("c", c)) if v}
    sides = {k: v for k, v in (("ab", ab), ("bc", bc), ("ca", ca)) if v}
    if angles:
        spec["angles"] = angles
    if sides:
        spec["sides"] = sides
    if height:
        spec["height"] = height
    if note:
        spec["note"] = note
    if hl:
        spec["highlight"] = hl
    if enclose:
        spec["enclose"] = True
    return {"op": "figure", "id": "", "spec": spec}


def QF(qid, **changes):
    """The question's own figure (from data/question-figures), with fields changed if asked."""
    entry = question_figures().get(qid) or {}
    spec = entry.get("figure")
    if not spec:
        raise ValueError("no figure for %s" % qid)
    spec = json.loads(json.dumps(spec))
    for k, v in changes.items():
        if v is None:
            spec.pop(k, None)
        else:
            spec[k] = v
    return {"op": "figure", "id": "", "spec": spec}


def has_figure(qid):
    return bool((question_figures().get(qid) or {}).get("figure"))


# ── Beats and asks ───────────────────────────────────────────────────────────

def B(say, *ops, **kw):
    beat = {"say": say}
    flat = []
    for op in ops:
        if isinstance(op, (list, tuple)):
            flat.extend(op)
        elif op is not None:
            flat.append(op)
    if flat:
        beat["board"] = flat
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def ch(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def ask(key, right, slips, if_not):
    """A choose-ask with the right choice placed by a stable hash, so it is not always first."""
    pos = hnum(key, "pos", len(slips) + 1)
    choices = list(slips)
    choices.insert(pos, right)
    return ch(choices, pos, if_not)


THINK = {"kind": "think"}


def lesson(beats, origin="authored"):
    n = 0
    for beat in beats:
        for op in beat.get("board", []):
            if op.get("op") == "figure":
                n += 1
                op["id"] = "f%d" % n
    return {"origin": origin, "beats": beats}
