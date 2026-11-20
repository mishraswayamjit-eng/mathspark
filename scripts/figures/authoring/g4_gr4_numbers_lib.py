"""Shared helpers for the Grade 4 figure scripts g4_gr4_numbers.py, g4_gr4_squares.py, g4_gr4_decimals.py.

Every figure passes through `Part.add`, which checks each figure's numbers against what the
checker allows at that point (question text before answering; question, options and the steps
so far for a step figure). A figure whose numbers are not grounded is reported and left out,
so the part file on disk always passes the checker.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
for _p in (os.path.join(ROOT, "scripts", "bank"), os.path.join(ROOT, "scripts", "figures"), HERE):
    if _p not in sys.path:
        sys.path.append(_p)

import bank  # noqa: E402
import validate  # noqa: E402
from c_lib import pc, table, seg, bar, bm, nl, fb, ftree, rect  # noqa: E402,F401

PARTS = os.path.join(ROOT, "data", "question-figures", "parts")


def load(topic):
    return sorted((q for q in bank.load_bank(4) if q.get("node") == topic), key=lambda q: q["id"])


def qnums(q):
    return validate.numbers_in(q.get("questionText", ""))


def onums(q):
    out = set()
    for t in validate.option_texts(q):
        out |= validate.numbers_in(t)
    return out


def step_texts(q):
    return [(s.get("text") or "") for s in (q.get("stepByStep") or [])]


def allowed_at(q, i):
    """Numbers a figure for step i may show."""
    out = qnums(q) | onums(q)
    for t in step_texts(q)[: i + 1]:
        out |= validate.numbers_in(t)
    return out


def answer(q):
    return validate.correct_text(q)


def ind(n):
    """An integer with Indian commas: 362489 -> 3,62,489."""
    s = str(int(n))
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


def grid(rows, cols, shaded=None, note=None):
    fig = {"kind": "grid", "rows": rows, "cols": cols}
    if shaded:
        fig["shaded"] = [list(c) for c in shaded]
    if note:
        fig["note"] = note
    return fig


def line(lo, hi, step, points=None, hops=None, note=None, hl=None, ticks=None):
    fig = nl(lo, hi, step, points=points, hops=hops, note=note, hl=hl)
    if ticks:
        fig["tickLabels"] = ticks
    return fig


def journey(places, legs, note=None, hl=None):
    fig = {"kind": "journey", "places": places, "legs": legs}
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def ungrounded(fig, allowed):
    ctx = validate.check_figure(fig, "fig")
    if ctx.errors:
        return ctx.errors
    return validate.ungrounded(ctx.numbers, allowed)


class Part(object):
    def __init__(self, topic):
        self.topic = topic
        self.qs = load(topic)
        self.by_id = dict((q["id"], q) for q in self.qs)
        self.out = {}
        self.dropped = []
        self.path = os.path.join(PARTS, "g4-%s.json" % topic)

    def add(self, q, figure=None, steps=None, origin="authored", essential=False, uses_options=False):
        """steps: a list (one per step) or a dict {step index: figure}."""
        if isinstance(q, str):
            q = self.by_id[q]
        qid = q["id"]
        n = len(q.get("stepByStep") or [])
        entry = {"origin": origin}
        if figure is not None:
            allowed = qnums(q) | (onums(q) if uses_options else set())
            bad = [] if essential else ungrounded(figure, allowed)
            if essential:
                bad = validate.check_figure(figure, "fig").errors
            if bad:
                self.dropped.append("%s.figure: %s" % (qid, bad))
            else:
                entry["figure"] = figure
        if steps:
            if isinstance(steps, dict):
                steps = [steps.get(i) for i in range(n)]
            if len(steps) != n:
                self.dropped.append("%s.steps: %d given, question has %d" % (qid, len(steps), n))
                steps = None
            else:
                kept = []
                for i, fig in enumerate(steps):
                    if fig is None:
                        kept.append(None)
                        continue
                    bad = ungrounded(fig, allowed_at(q, i))
                    if bad:
                        self.dropped.append("%s.step[%d]: %s" % (qid, i, bad))
                        kept.append(None)
                    else:
                        kept.append(fig)
                if any(f is not None for f in kept):
                    entry["stepFigures"] = kept
        if essential and "figure" in entry:
            entry["essential"] = True
        if uses_options and "figure" in entry:
            entry["usesOptions"] = True
        if "figure" not in entry and "stepFigures" not in entry:
            return
        problems = validate.check_entry(qid, entry, q)
        if problems:
            self.dropped.append("%s: CHECKER %s" % (qid, problems))
            return
        if qid in self.out:
            self.dropped.append("%s: added twice" % qid)
        self.out[qid] = entry

    def write(self):
        ordered = dict((k, self.out[k]) for k in sorted(self.out))
        with io.open(self.path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(ordered, f, ensure_ascii=False, indent=1)
            f.write("\n")
        kinds = {}
        for e in ordered.values():
            k = (e.get("figure") or next(s for s in e["stepFigures"] if s))["kind"]
            kinds[k] = kinds.get(k, 0) + 1
        print("%s: %d of %d questions have a visual (%d with a figure before answering)" % (
            self.topic, len(ordered), len(self.qs), sum(1 for e in ordered.values() if "figure" in e)))
        print("  by kind: " + ", ".join("%s %d" % kv for kv in sorted(kinds.items())))
        print("  by rule %d, individually drawn %d, essential %d" % (
            sum(1 for e in ordered.values() if e["origin"] == "rule"),
            sum(1 for e in ordered.values() if e["origin"] == "authored"),
            sum(1 for e in ordered.values() if e.get("essential"))))
        if self.dropped:
            print("  LEFT OUT (%d):" % len(self.dropped))
            for d in self.dropped:
                print("    " + d)

    def review(self, ids=None):
        """Print question, figure and step figures side by side."""
        for qid in (ids or sorted(self.out)):
            q, e = self.by_id[qid], self.out.get(qid)
            if not e:
                print("### %s: no visual\n" % qid)
                continue
            print("### %s [%s]%s" % (qid, e["origin"], " ESSENTIAL" if e.get("essential") else ""))
            print("Q: " + q["questionText"])
            print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]) + "   ans " + q["correctAnswer"])
            print("  BEFORE: " + (json.dumps(e["figure"], ensure_ascii=False) if "figure" in e else "-"))
            figs = e.get("stepFigures") or []
            for i, t in enumerate(step_texts(q)):
                print("  S%d: %s" % (i, t))
                if i < len(figs) and figs[i] is not None:
                    print("      => " + json.dumps(figs[i], ensure_ascii=False))
            print()
