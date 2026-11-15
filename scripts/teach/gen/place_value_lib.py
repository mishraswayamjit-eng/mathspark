"""Small helpers shared by the place-value lesson scripts (teach mode).

A lesson is built from beats: b(say, op, op, ..., ask=ch([...], ifNot)).
Choices are always written with the right one FIRST; finish() then moves it to a
position picked by a stable hash of the question id, so the right answer is not
always the first button.
"""
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of, option_texts  # noqa: E402,F401

PART = os.path.join(ROOT, "data", "teach", "parts", "place-value.json")


def h(qid, salt=""):
    """A stable number from a question id."""
    return int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, choices):
    """One of a few phrasings, the same every run for the same question."""
    return choices[h(qid, salt) % len(choices)]


# ── Board ops ────────────────────────────────────────────────────────────────

def _w(i, text, tone, lab):
    op = {"op": "write", "id": i, "text": text}
    if tone:
        op["tone"] = tone
    if lab:
        op["label"] = True
    return op


def w(i, text):
    return _w(i, text, None, False)


def wl(i, text):
    return _w(i, text, None, True)


def g(i, text):
    return _w(i, text, "given", False)


def gl(i, text):
    return _w(i, text, "given", True)


def a(i, text):
    return _w(i, text, "answer", False)


def al(i, text):
    return _w(i, text, "answer", True)


def _t(text, nth=1):
    t = {"text": text}
    if nth != 1:
        t["nth"] = nth
    return t


def ul(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "underline"}


def ring(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "circle"}


def box(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "box"}


def nt(line, target, text, place="below", nth=1):
    op = {"op": "note", "line": line, "target": _t(target, nth), "text": text}
    if place != "above":
        op["place"] = place
    return op


def x(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def arc(line, frm, tos):
    def t(v):
        return _t(v[0], v[1]) if isinstance(v, tuple) else _t(v)
    return {"op": "arc", "line": line, "from": t(frm), "to": [t(v) for v in tos]}


def grp(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_t(v[0], v[1]) if isinstance(v, tuple) else _t(v) for v in targets]}
    if label:
        op["label"] = label
    return op


def fig(i, spec):
    return {"op": "figure", "id": i, "spec": spec}


def pchart(number, hi=None, note=None):
    spec = {"kind": "placeChart", "number": str(number)}
    if hi:
        spec["highlight"] = ["d%d" % k for k in hi]
    if note:
        spec["note"] = note
    return spec


def tbl(headers, rows, hi=None, note=None):
    spec = {"kind": "table", "rows": rows}
    if headers:
        spec["headers"] = headers
    if hi:
        spec["highlight"] = ["r%d" % k for k in hi]
    if note:
        spec["note"] = note
    return spec


def nline(lo, hi, step, points=None, hops=None, labels=None, note=None):
    spec = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if labels:
        spec["tickLabels"] = labels
    if points:
        spec["points"] = [{"at": p[0], "label": p[1]} if isinstance(p, tuple) else {"at": p} for p in points]
    if hops:
        spec["hops"] = [{"from": f, "to": t, "label": lab} if lab else {"from": f, "to": t} for f, t, lab in hops]
    if note:
        spec["note"] = note
    return spec


# ── Beats and asks ───────────────────────────────────────────────────────────

def ch(choices, if_not):
    """A choose ask. The FIRST choice is the right one; finish() shuffles it."""
    return {"kind": "choose", "choices": list(choices), "answer": 0, "ifNot": if_not}


THINK = {"kind": "think"}


def b(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def finish(qid, origin, beats):
    """Move the right choice of each ask to a stable, varied position."""
    out = []
    for i, beat in enumerate(beats):
        beat = dict(beat)
        ask = beat.get("ask")
        if ask and ask.get("kind") == "choose":
            choices = list(ask["choices"])
            right = choices[0]
            rest = choices[1:]
            if h(qid, "flip%d" % i) % 2:
                rest.reverse()
            pos = h(qid, "pos%d" % i) % len(choices)
            choices = rest[:pos] + [right] + rest[pos:]
            beat["ask"] = {"kind": "choose", "choices": choices, "answer": pos, "ifNot": ask["ifNot"]}
        out.append(beat)
    return {"origin": origin, "beats": out}


# ── Places ───────────────────────────────────────────────────────────────────

# Index 0 is the units place.
PLACE_NAMES = ["units", "tens", "hundreds", "thousands", "ten-thousands", "lakhs", "ten-lakhs", "crores"]


def place_index(name):
    name = name.strip().lower().replace(" ", "-")
    if name == "ones":
        name = "units"
    return PLACE_NAMES.index(name)


def nth_digit(number, index_from_left):
    """Which occurrence (1-based) of its own digit the digit at this position is."""
    s = str(number)
    return s[:index_from_left + 1].count(s[index_from_left])


def nth_of(line, target, at):
    """Which occurrence (1-based) of `target` on `line` starts at character `at`.

    Raises if overlapping and non-overlapping counting disagree, so a mark can
    never land on the wrong copy.
    """
    assert line[at:at + len(target)] == target, (line, target, at)
    over = [i for i in range(len(line)) if line.startswith(target, i)]
    non, i = [], 0
    while True:
        i = line.find(target, i)
        if i < 0:
            break
        non.append(i)
        i += len(target)
    if at not in non or over.index(at) != non.index(at):
        raise ValueError("ambiguous target %r on %r" % (target, line))
    return non.index(at) + 1


def load_questions():
    return [q for q in load_grade5() if topic_of(q) == "place-value"]


def key_text(q):
    idx = "ABCD".find(q.get("correctAnswer", ""))
    return option_texts(q)[idx]


def write_part(lessons):
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
