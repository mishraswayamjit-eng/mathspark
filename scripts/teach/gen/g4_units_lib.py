"""Small helpers for writing Grade 4 lessons: beats, board ops, asks, and the file writer.

Used by g4_units.py and g4_counting.py and their helper files.

A lesson is written as a list of beats:

    LESSONS["<question id>"] = [
        b("What the teacher says.", g("q", "the question, short"), u("q", "a piece")),
        b("A question for the child?", ask=c("the right choice", ["a slip", "another slip"], "What to look at again.")),
        b("The answer.", a("ans", "42500 g")),
        ...
    ]
"""
import hashlib
import io
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "teach"))
import bank  # noqa: E402


def pick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id."""
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def g(id, text, label=True):
    """The question as printed (first line on the board)."""
    op = {"op": "write", "id": id, "text": text, "tone": "given"}
    if label:
        op["label"] = True
    return op


def w(id, text):
    """A line of plain maths. The checker verifies it."""
    return {"op": "write", "id": id, "text": text}


def l(id, text):
    """A line with words or units in it."""
    return {"op": "write", "id": id, "text": text, "label": True}


def a(id, text, ring=None):
    """The final answer, ringed."""
    return [{"op": "write", "id": id, "text": text, "tone": "answer", "label": True},
            {"op": "mark", "line": id, "target": {"text": ring or text}, "shape": "circle"}]


def _t(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def u(line, text, nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "underline"}


def box(line, text, nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "box"}


def ring(line, text, nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "circle"}


def n(line, target, text, place=None, nth=None):
    op = {"op": "note", "line": line, "target": _t(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def x(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def grp(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_t(t) if isinstance(t, str) else _t(*t) for t in targets]}
    if label:
        op["label"] = label
    return op


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": _t(frm), "to": [_t(t) for t in to]}


def fig(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


_FIGS = {}


def qfig(topic, qid, step=None):
    """The figure already drawn for a question (read only): its main figure, or the one for a step."""
    if topic not in _FIGS:
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        with io.open(path, encoding="utf-8") as f:
            _FIGS[topic] = json.load(f)
    entry = _FIGS[topic].get(qid) or {}
    spec = entry.get("figure") if step is None else (entry.get("stepFigures") or [None] * (step + 1))[step]
    if not spec:
        raise KeyError("no figure for %s step %s" % (qid, step))
    return spec


# ── Beats and asks ───────────────────────────────────────────────────────────

def b(say, *ops, **kw):
    beat = {"say": say}
    flat = []
    for op in ops:
        if op is None:
            continue
        if isinstance(op, list):
            flat.extend(op)
        else:
            flat.append(op)
    if flat:
        beat["board"] = flat
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def c(right, others, if_not):
    """A 'choose' ask. Where the right choice sits is fixed later from the question id."""
    return {"kind": "choose", "_right": right, "_others": list(others), "ifNot": if_not}


def think():
    return {"kind": "think"}


# ── Finishing and writing ────────────────────────────────────────────────────

_UNIT_WORD = re.compile(r"[A-Za-z]+")


def _same_unit_slip(text):
    """For a label line like '1200 ml − 350 ml = 850 ml' (one unit throughout), check the sum."""
    if "=" not in text or "?" in text or "≈" in text:
        return None
    words = set(_UNIT_WORD.findall(text))
    if len(words) != 1 or not all(_UNIT_WORD.search(side) for side in text.split("=")):
        return None
    bare = _UNIT_WORD.sub("", text).replace("−", "-").replace("×", "*").replace("÷", "/").replace(",", "")
    if not re.fullmatch(r"[0-9.+\-*/()= ]+", bare):
        return None
    try:
        sides = [eval(re.sub(r"\d+(?:\.\d+)?", lambda m: "Fraction('%s')" % m.group(0), s), {"Fraction": Fraction})
                 for s in bare.split("=")]
    except Exception:
        return None
    if any(v != sides[0] for v in sides):
        return "is not true: the sides are %s" % ", ".join(str(float(v)) for v in sides)
    return None


def _unclear_target(line_text, target):
    """True if a mark's target would land somewhere unintended: the piece of text it names
    appears more than once (and no nth says which), or sits inside a longer number or word."""
    text = target["text"]
    if "nth" not in target and line_text.count(text) > 1:
        return True
    at = -1
    for _ in range(target.get("nth", 1)):
        at = line_text.find(text, at + 1)
    if at < 0:
        return False
    before = line_text[at - 1] if at > 0 else " "
    after = line_text[at + len(text)] if at + len(text) < len(line_text) else " "
    first, last = text[0], text[-1]
    if first.isdigit() and (before.isdigit() or before == "."):
        return True
    if last.isdigit() and (after.isdigit() or (after == "." and at + len(text) + 1 < len(line_text)
                                               and line_text[at + len(text) + 1].isdigit())):
        return True
    if first.isalpha() and before.isalpha() and len(text) < 4:
        return True
    return False


def finish(qid, beats, origin):
    out = []
    lines = {}
    for beat in beats:
        for op in beat.get("board", []):
            if op.get("op") == "write":
                lines[op["id"]] = op["text"]
                continue
            targets = [op[k] for k in ("target", "from") if k in op] + list(op.get("to", [])) + list(op.get("targets", []))
            for t in targets:
                if op.get("line") in lines and _unclear_target(lines[op["line"]], t):
                    print("  CHECK %s: mark on %r in \"%s\" may land on the wrong place" % (qid, t, lines[op["line"]]))
    for i, beat in enumerate(beats):
        beat = dict(beat)
        ask = beat.get("ask")
        if ask and ask.get("kind") == "choose" and "_right" in ask:
            choices = list(ask["_others"])
            at = pick(qid, "place%d" % i, list(range(len(choices) + 1)))
            choices.insert(at, ask["_right"])
            beat["ask"] = {"kind": "choose", "choices": choices, "answer": at, "ifNot": ask["ifNot"]}
        for op in beat.get("board", []):
            if op.get("op") == "write" and op.get("label"):
                slip = _same_unit_slip(op["text"])
                if slip:
                    raise ValueError("%s: label line \"%s\" %s" % (qid, op["text"], slip))
        out.append(beat)
    return {"origin": origin, "beats": out}


def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def option_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def write_part(topic, lessons):
    """Write data/teach/parts/g4-<topic>.json in the bank's question order."""
    qs = questions(topic)
    ids = [q["id"] for q in qs]
    stray = [k for k in lessons if k not in ids]
    if stray:   # questions since removed from the bank
        print("skipped, no longer in %s: %s" % (topic, stray))
    ordered = {qid: lessons[qid] for qid in ids if qid in lessons}
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d lessons of %d questions" % (os.path.relpath(path, ROOT), len(ordered), len(ids)))
