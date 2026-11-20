"""Small helpers for writing Grade 4 lessons (time and calendar; also used by data handling).

Board ops, beats, asks, figures borrowed from the question's own figure file, and the
writer that puts a part file on disk.
"""
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def pick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id."""
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def given(id, text):
    """The question, in short, as the first line on the board."""
    return {"op": "write", "id": id, "text": text, "tone": "given", "label": True}


def given_m(id, text):
    """A given line that is plain maths (checked)."""
    return {"op": "write", "id": id, "text": text, "tone": "given"}


def w(id, text):
    """A line of working that is plain maths (the checker verifies it)."""
    return {"op": "write", "id": id, "text": text}


def lab(id, text):
    """A line of words: a fact, a label, a result with its unit."""
    return {"op": "write", "id": id, "text": text, "label": True}


def ans(id, text, ring=None):
    """The final answer, written and ringed."""
    return [{"op": "write", "id": id, "text": text, "tone": "answer", "label": True},
            {"op": "mark", "line": id, "target": {"text": ring or text}, "shape": "circle"}]


def _target(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def box(line, text, nth=None):
    return mark(line, text, "box", nth)


def ring(line, text, nth=None):
    return mark(line, text, "circle", nth)


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


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": _target(frm), "to": [_target(t) for t in to]}


_FIGS = {}


def fig(topic, qid, which="main", id="f1"):
    """A figure op using the question's own figure: 'main', or the number of a step figure."""
    if topic not in _FIGS:
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        with io.open(path, encoding="utf-8") as f:
            _FIGS[topic] = json.load(f)
    entry = _FIGS[topic][qid]
    if which == "main" and not entry.get("figure"):
        return None   # this question has step figures only; the lesson goes without
    spec = entry["figure"] if which == "main" else entry["stepFigures"][which]
    if not spec:
        raise ValueError("%s has no figure %r" % (qid, which))
    return {"op": "figure", "id": id, "spec": spec}


def figspec(spec, id="f1"):
    return {"op": "figure", "id": id, "spec": spec}


# ── Beats and asks ───────────────────────────────────────────────────────────

def beat(say, *ops, **kw):
    b = {"say": say}
    flat = []
    for op in ops:
        if op is None:
            continue
        if isinstance(op, list):
            flat.extend(op)
        else:
            flat.append(op)
    if flat:
        b["board"] = flat
    if kw.get("ask"):
        b["ask"] = kw["ask"]
    return b


def choose(right, others, if_not):
    """A 'choose' ask. The right choice is put at a place fixed by its own words."""
    choices = list(others)
    at = pick(right + "|" + if_not, "place", list(range(len(choices) + 1)))
    choices.insert(at, right)
    return {"kind": "choose", "choices": choices, "answer": at, "ifNot": if_not}


def think():
    return {"kind": "think"}


# ── Writing the part ─────────────────────────────────────────────────────────

def topic_questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def write_part(topic, lessons):
    """lessons: {question id: (origin, beats)}. Writes data/teach/parts/g4-<topic>.json."""
    qs = topic_questions(topic)
    ids = [q["id"] for q in qs]
    stray = [k for k in lessons if k not in ids]
    if stray:
        sys.exit("not in %s: %s" % (topic, ", ".join(stray)))
    out = {}
    for qid in ids:
        if qid in lessons:
            origin, beats = lessons[qid]
            out[qid] = {"origin": origin, "beats": beats}
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [i for i in ids if i not in out]
    print("wrote %s: %d lessons, %d questions still without one" % (os.path.relpath(path, ROOT), len(out), len(missing)))
    for m in missing[:12]:
        print("  missing", m)
