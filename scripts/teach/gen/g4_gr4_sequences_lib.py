"""Small helpers for writing Grade 4 lessons as Python data (used by g4_gr4_sequences*
and g4_gr4_puzzles*).

A lesson is a list of beats; lesson() turns it into a TeachScript (see
src/lib/teach/types.ts). Choices in an ask are given as (right, [others]) and
are put in a stable shuffled order, so the right one is not always first.
"""
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def questions(topic):
    return {q["id"]: q for q in bank.load_bank(4) if q.get("node") == topic}


def part_path(topic):
    return os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)


_FIGS = {}


def qfig(topic, qid):
    """The question's own figure spec (read only), or None."""
    if topic not in _FIGS:
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        _FIGS[topic] = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                _FIGS[topic] = json.load(f)
    entry = _FIGS[topic].get(qid) or {}
    spec = entry.get("figure")
    return json.loads(json.dumps(spec)) if spec else None


def stable(qid, salt=""):
    return int(hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest(), 16)


def pick(qid, salt, options):
    """One of a few phrasings, always the same one for the same question."""
    return options[stable(qid, salt) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def w(line_id, text, tone=None, label=False):
    op = {"op": "write", "id": line_id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def g(line_id, text, label=False):
    """The question as printed."""
    return w(line_id, text, "given", label)


def lab(line_id, text):
    """A line of words (not checked as maths)."""
    return w(line_id, text, None, True)


def ans(line_id, text, ring_text=None, label=False):
    """The final answer line, ringed."""
    return [w(line_id, text, "answer", label), mk(line_id, ring_text or text, "circle")]


def T(text, nth=1):
    t = {"text": text}
    if nth != 1:
        t["nth"] = nth
    return t


def nt(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": T(target, nth), "text": text, "place": place}


def mk(line, target, shape="underline", nth=1):
    return {"op": "mark", "line": line, "target": T(target, nth), "shape": shape}


def ring(line, target, nth=1):
    return mk(line, target, "circle", nth)


def box(line, target, nth=1):
    return mk(line, target, "box", nth)


def st(line, target, note_text=None, nth=1):
    op = {"op": "strike", "line": line, "target": T(target, nth)}
    if note_text:
        op["note"] = note_text
    return op


def grp(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [T(*t) if isinstance(t, tuple) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def fig(fig_id, spec):
    return {"op": "figure", "id": fig_id, "spec": spec}


def tbl(fig_id, rows, note=None, headers=None):
    spec = {"kind": "table", "rows": [[str(c) for c in r] for r in rows]}
    if headers:
        spec["headers"] = headers
    if note:
        spec["note"] = note
    return fig(fig_id, spec)


def seq(terms, tail=None):
    """A sequence as a line of words: '2, 7, 14, ?'."""
    s = ", ".join(str(t) for t in terms)
    return s + (", " + tail if tail else "")


def jumps(line, labels, first=1, place="below"):
    """The '+3, +3, +3' a teacher writes between neighbours: one note at each comma."""
    return [nt(line, ",", lab_, place, first + i) for i, lab_ in enumerate(labels)]


# ── Asks and beats ───────────────────────────────────────────────────────────

def ch(right, others, if_not):
    return {"kind": "choose", "_right": right, "_others": list(others), "ifNot": if_not}


TH = {"kind": "think"}


def b(say, *ops, **kw):
    beat = {"say": say}
    flat = []
    for op in ops:
        if isinstance(op, list):
            flat.extend(op)
        elif op is not None:
            flat.append(op)
    if flat:
        beat["board"] = flat
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def lesson(qid, beats, origin="authored", check=None):
    out = []
    for i, bt in enumerate(beats):
        bt = dict(bt)
        ask = bt.get("ask")
        if ask and ask.get("kind") == "choose":
            choices = [ask["_right"]] + ask["_others"]
            order = sorted(range(len(choices)), key=lambda k: stable(qid, "ask%d.%d" % (i, k)))
            bt["ask"] = {"kind": "choose", "choices": [choices[k] for k in order],
                         "answer": order.index(0), "ifNot": ask["ifNot"]}
        out.append(bt)
    script = {"origin": origin}
    if check:
        script["check"] = {"variable": check[0], "value": str(check[1])}
    script["beats"] = out
    return script


def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


# ── Building a part ──────────────────────────────────────────────────────────

def build(topic, rules, authored):
    """rules: list of functions (q) -> beats or None.  authored: {qid: beats or function(q) -> beats}."""
    qs = questions(topic)
    out = {}
    missing = []
    for qid in sorted(qs):
        q = qs[qid]
        script = None
        if qid in authored:
            beats = authored[qid]
            if callable(beats):
                beats = beats(q)
            script = lesson(qid, beats, "authored")
        else:
            for rule in rules:
                beats = rule(q)
                if beats:
                    script = lesson(qid, beats, "rule")
                    break
        if script:
            out[qid] = script
        else:
            missing.append(qid)
    extra = sorted(set(authored) - set(qs))
    path = part_path(topic)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    n_rule = sum(1 for s in out.values() if s["origin"] == "rule")
    print("wrote %s: %d lessons (%d rule, %d authored) of %d questions" % (
        os.path.relpath(path, ROOT), len(out), n_rule, len(out) - n_rule, len(qs)))
    if extra:
        print("authored ids not in this topic:", ", ".join(extra))
    if missing:
        print("%d without a lesson yet: %s" % (len(missing), " ".join(missing)))
