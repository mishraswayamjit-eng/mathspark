"""Small helpers for writing squares-patterns lessons as Python data.

A lesson is a list of beats; lesson() turns it into a TeachScript (see
src/lib/teach/types.ts). Choices in an ask are given as (right, [others]) and
are put in a stable shuffled order, so the right one is not always first.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

TOPIC = "squares-patterns"
PART = os.path.join(ROOT, "data", "teach", "parts", "squares-patterns.json")
GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def questions():
    return {q["id"]: q for q in load_grade5() if topic_of(q) == TOPIC}


def stable(qid, salt=""):
    return int(hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest(), 16)


def pick(qid, salt, options):
    """One of a few phrasings, always the same one for the same question."""
    return options[stable(qid, salt) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def W(line_id, text, tone=None, label=False):
    op = {"op": "write", "id": line_id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def given(line_id, text, label=False):
    return W(line_id, text, "given", label)


def answer(line_id, text, label=False):
    return W(line_id, text, "answer", label)


def words(line_id, text):
    return W(line_id, text, None, True)


def T(text, nth=1):
    t = {"text": text}
    if nth != 1:
        t["nth"] = nth
    return t


def note(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": T(target, nth), "text": text, "place": place}


def mark(line, target, shape="underline", nth=1):
    return {"op": "mark", "line": line, "target": T(target, nth), "shape": shape}


def ring(line, target, nth=1):
    return mark(line, target, "circle", nth)


def strike(line, target, note_text=None, nth=1):
    op = {"op": "strike", "line": line, "target": T(target, nth)}
    if note_text:
        op["note"] = note_text
    return op


def both(line, text):
    return {"op": "both", "line": line, "text": text}


def divide(line, by):
    return {"op": "divide", "line": line, "by": by}


def group(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [T(*t) if isinstance(t, tuple) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def fig(fig_id, spec):
    return {"op": "figure", "id": fig_id, "spec": spec}


def grid(fig_id, rows, cols=None, caption=None, dots=False):
    spec = {"kind": "grid", "rows": rows, "cols": cols if cols is not None else rows}
    if dots:
        spec["dots"] = True
    if caption:
        spec["note"] = caption
    return fig(fig_id, spec)


def table(fig_id, headers, rows, caption=None, highlight=None):
    spec = {"kind": "table", "headers": headers, "rows": rows}
    if caption:
        spec["note"] = caption
    if highlight:
        spec["highlight"] = highlight
    return fig(fig_id, spec)


def seq_text(terms, tail=None):
    """A sequence as a line of words: '2, 7, 14, …'."""
    s = ", ".join(str(t) for t in terms)
    return s + (", " + tail if tail else "")


def jumps(line, labels, first=1, place="below"):
    """The '+3, +3, +3' a teacher writes between neighbours: one note at each comma."""
    return [note(line, ",", lab, place, first + i) for i, lab in enumerate(labels)]


# ── Asks and beats ───────────────────────────────────────────────────────────

def choose(right, others, if_not):
    return {"kind": "choose", "_right": right, "_others": list(others), "ifNot": if_not}


THINK = {"kind": "think"}


def beat(say, *ops, **kw):
    b = {"say": say}
    flat = []
    for op in ops:
        if isinstance(op, list):
            flat.extend(op)
        elif op is not None:
            flat.append(op)
    if flat:
        b["board"] = flat
    if kw.get("ask"):
        b["ask"] = kw["ask"]
    return b


def lesson(qid, beats, origin="authored", check=None):
    out = []
    for i, b in enumerate(beats):
        b = dict(b)
        ask = b.get("ask")
        if ask and ask.get("kind") == "choose":
            choices = [ask["_right"]] + ask["_others"]
            order = sorted(range(len(choices)), key=lambda k: stable(qid, "ask%d.%d" % (i, k)))
            b["ask"] = {"kind": "choose", "choices": [choices[k] for k in order],
                        "answer": order.index(0), "ifNot": ask["ifNot"]}
        out.append(b)
    script = {"origin": origin}
    if check:
        script["check"] = {"variable": check[0], "value": str(check[1])}
    script["beats"] = out
    return script


def times_split(n):
    """n × n broken into n × tens + n × ones, for a two-digit n that is not a multiple of 10."""
    tens, ones = (n // 10) * 10, n % 10
    return tens, ones, n * tens, n * ones
