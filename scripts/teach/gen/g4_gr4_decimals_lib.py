"""Small helpers shared by the Grade 4 decimals lesson scripts (rules and hand-written lessons).

A lesson is built from beats; a beat is what the teacher says plus what the board does.
Nothing here knows any maths answers: the checker verifies every maths line.
"""
import hashlib
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TOPIC = "gr4_decimals"
FIG_PATH = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)

_FIGS = None


def figure_of(qid, step=None):
    """A figure already drawn for this question (read only): the one shown before answering,
    or the one for step number `step` (0-based)."""
    global _FIGS
    if _FIGS is None:
        with io.open(FIG_PATH, encoding="utf-8") as f:
            _FIGS = json.load(f)
    entry = _FIGS[qid]
    spec = entry["figure"] if step is None else entry["stepFigures"][step]
    assert spec, "no such figure for %s (%s)" % (qid, step)
    return json.loads(json.dumps(spec))


# ── Stable variety ───────────────────────────────────────────────────────────

def pick(qid, salt, options):
    """One of `options`, always the same one for the same question and salt."""
    h = int(hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None, label=False):
    """A line of maths (checked by the validator)."""
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def WL(id, text):
    """A line of words (a label; not checked as maths)."""
    return W(id, text, label=True)


def GIVEN(id, text):
    """The question as printed, in words."""
    return W(id, text, tone="given", label=True)


def GM(id, text):
    """The question as printed, when it is pure maths (it has a ? so it is shown, not checked)."""
    return W(id, text, tone="given")


def ANS(id, text, label=False):
    return W(id, text, tone="answer", label=label)


def _target(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def MARK(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def UL(line, text, nth=None):
    return MARK(line, text, "underline", nth)


def RING(line, text, nth=None):
    return MARK(line, text, "circle", nth)


def BOX(line, text, nth=None):
    return MARK(line, text, "box", nth)


def NOTE(line, text, note, place=None, nth=None):
    op = {"op": "note", "line": line, "target": _target(text, nth), "text": note}
    if place:
        op["place"] = place
    return op


def STRIKE(line, text, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _target(text, nth)}
    if note:
        op["note"] = note
    return op


def GROUP(line, texts, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else _target(t) for t in texts]}
    if label:
        op["label"] = label
    return op


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _target(frm), "to": [_target(t) for t in to]}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def CHART(id, number, note=None, highlight=None):
    """A place-value chart for a number written as a string, e.g. '536.429'."""
    spec = {"kind": "placeChart", "number": number}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return FIG(id, spec)


def TABLE(id, headers, rows, note=None, highlight=None):
    spec = {"kind": "table", "rows": rows, "headers": headers}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return FIG(id, spec)


# ── Beats ────────────────────────────────────────────────────────────────────

def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


THINK = {"kind": "think"}


def choose(qid, salt, right, others, if_not):
    """A choose-ask with the right choice placed by a stable hash, so it is not always first."""
    n = len(others) + 1
    at = pick(qid, "at" + salt, list(range(n)))
    choices = list(others)
    choices.insert(at, right)
    return {"kind": "choose", "choices": choices, "answer": at, "ifNot": if_not}


def lesson(beats, origin):
    return {"origin": origin, "beats": beats}


class T(object):
    """One hand-written lesson, built a beat at a time.

        t = T("G4A_DECIMALS_001")
        t.say("...", GIVEN("q", "..."))
        t.ask("...", "right choice", ["a slip", "another slip"], "what to look at again", <ops>)
        t.done(LESSONS)
    """

    def __init__(self, qid):
        self.qid = qid
        self.beats = []

    def say(self, text, *ops):
        self.beats.append(B(text, *ops))
        return self

    def ask(self, text, right, others, if_not, *ops):
        salt = "b%d" % len(self.beats)
        self.beats.append(B(text, *ops, ask=choose(self.qid, salt, right, others, if_not)))
        return self

    def think(self, text, *ops):
        self.beats.append(B(text, *ops, ask=THINK))
        return self

    def done(self, into):
        assert self.qid not in into, "two lessons for %s" % self.qid
        into[self.qid] = lesson(self.beats, "authored")
