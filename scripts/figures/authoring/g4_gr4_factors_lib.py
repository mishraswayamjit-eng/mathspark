"""Shared helpers for the Grade 4 figure scripts g4_gr4_factors.py, g4_gr4_sequences.py and g4_gr4_counting.py.

Every figure is tested with the checker's own rules (scripts/figures/validate.py) before it
is kept: a before-answering figure that shows a number the question does not state is left
out, and so is a step figure that shows a number not stated by that step. What was left out
is printed, so nothing fails silently.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "figures"))
import validate  # noqa: E402

bank = validate.bank


# ── Numbers and text ─────────────────────────────────────────────────────────

def nums(text):
    """The numbers the checker reads in a piece of text."""
    return validate.numbers_in(text)


def n(x):
    """A number as a child writes it: 12, 0.75 (never 12.0)."""
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        return str(x)
    return ("%.4f" % x).rstrip("0").rstrip(".")


def ints(text):
    """Whole numbers in the order written. '4,729' is one number; '64,81,100' is three."""
    out = []
    for m in re.finditer(r"\d+(?:,\d{3})*(?!\d)|\d+", text):
        tok = m.group(0)
        if "," in tok and not re.match(r"^\d{1,2}(,\d{3})+$", tok):
            out.extend(int(p) for p in tok.split(","))
        elif "," in tok:
            # "64,100" could be a list too: treat as one number only when written like 4,729
            out.append(int(tok.replace(",", "")))
        else:
            out.append(int(tok))
    return out


def cut(s, limit=70):
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


def join_and(items):
    items = [str(x) for x in items]
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def steps_of(q):
    return q.get("stepByStep") or []


def step_text(q, i):
    return steps_of(q)[i].get("text", "")


def stated(q, i):
    """Numbers written in the step texts up to and including step i."""
    out = set()
    for s in steps_of(q)[:i + 1]:
        out |= nums(s.get("text", ""))
    return out


def allowed_at(q, i):
    """The numbers the checker lets a figure for step i show."""
    out = nums(q.get("questionText", ""))
    for t in validate.option_texts(q):
        out |= nums(t)
    return out | stated(q, i)


def why_not(q, fig, allowed):
    ctx = validate.check_figure(fig, "f")
    if ctx.errors:
        return "; ".join(ctx.errors)
    extra = validate.ungrounded(ctx.numbers, allowed)
    if extra:
        return "shows " + validate.fmt(extra)
    return ""


def ok_at(q, i, fig):
    return fig is not None and not why_not(q, fig, allowed_at(q, i))


def before_allowed(q, uses_options=False):
    out = nums(q.get("questionText", ""))
    if uses_options:
        for t in validate.option_texts(q):
            out |= nums(t)
    return out


def key_text(q):
    return validate.correct_text(q)


# ── Small figure builders ────────────────────────────────────────────────────

def table(rows, note=None, headers=None, hl=None):
    fig = {"kind": "table", "rows": [[str(c) for c in r] for r in rows]}
    if headers:
        fig["headers"] = headers
    if note:
        fig["note"] = cut(note)
    if hl:
        fig["highlight"] = hl
    return fig


def wrap(cells, width=5):
    """Rows of at most `width` cells, as even as they can be."""
    cells = [str(c) for c in cells]
    rows = -(-len(cells) // width)
    per = -(-len(cells) // rows)
    return [cells[i:i + per] for i in range(0, len(cells), per)]


def with_note(fig, note=None, hl=None):
    out = dict(fig)
    out.pop("note", None)
    out.pop("highlight", None)
    if note:
        out["note"] = cut(note)
    if hl:
        out["highlight"] = hl
    return out


def venn(left_title, right_title, left, both, right, note=None, hl=None):
    fig = {"kind": "venn", "leftTitle": left_title, "rightTitle": right_title,
           "left": left, "both": both, "right": right}
    return with_note(fig, note, hl)


def number_line(lo, hi, step, ticks="none", points=None, hops=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step, "tickLabels": ticks}
    if points:
        fig["points"] = points
    if hops:
        fig["hops"] = hops
    return with_note(fig, note, hl)


def tick_step(lo, hi, unit):
    """A tick gap that is a multiple of `unit` and gives at most 40 ticks."""
    k = 1
    while (hi - lo) / float(unit * k) > 40:
        k += 1
    return unit * k


# ── One topic's output ───────────────────────────────────────────────────────

class Part(object):
    def __init__(self, topic):
        self.topic = topic
        self.Q = {}
        for q in bank.load_bank(4):
            if q.get("node") == topic:
                self.Q[q["id"]] = q
        self.E = {}
        self.log = []
        self.path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)

    def ids(self, prefix=""):
        return sorted(k for k in self.Q if k.startswith(prefix))

    def pick(self, q, i, cands):
        """The first candidate figure the checker allows at step i (None if none)."""
        if cands is None:
            return None
        if isinstance(cands, dict):
            cands = [cands]
        for c in cands:
            if c is not None and ok_at(q, i, c):
                return c
        real = [c for c in cands if c is not None]
        if real:
            self.log.append("%s step %d: figure left out (%s)" % (q["id"], i, why_not(q, real[0], allowed_at(q, i))))
        return None

    def add(self, qid, figure=None, steps=None, origin="rule", uses_options=False, essential=False):
        """figure: one figure or a list of candidates. steps: a list (one slot per step) or
        {step index: figure}; each slot is a figure, a list of candidates, or None."""
        q = self.Q[qid]
        count = len(steps_of(q))
        if isinstance(steps, dict):
            for k in steps:
                if not (0 <= k < count):
                    self.log.append("%s: no step %d" % (qid, k))
            arr = [steps.get(i) for i in range(count)]
        elif steps is None:
            arr = [None] * count
        else:
            arr = list(steps)
            if len(arr) != count:
                self.log.append("%s: %d step figures for %d steps; left out" % (qid, len(arr), count))
                arr = [None] * count
        arr = [self.pick(q, i, f) for i, f in enumerate(arr)]

        before = None
        if figure is not None:
            cands = [figure] if isinstance(figure, dict) else list(figure)
            allowed = before_allowed(q, uses_options)
            for c in cands:
                if essential:
                    if not validate.check_figure(c, "f").errors:
                        before = c
                        break
                elif not why_not(q, c, allowed):
                    before = c
                    break
            if before is None:
                self.log.append("%s: before-figure left out (%s)" % (qid, why_not(q, cands[0], allowed)))

        entry = {"origin": origin}
        if before is not None:
            entry["figure"] = before
        if any(f is not None for f in arr):
            entry["stepFigures"] = arr
        if uses_options and before is not None:
            entry["usesOptions"] = True
        if essential and before is not None:
            entry["essential"] = True
        if "figure" not in entry and "stepFigures" not in entry:
            self.log.append("%s: nothing left to draw" % qid)
            return
        problems = validate.check_entry(qid, entry, q)
        if problems:
            self.log.extend(problems)
            return
        if qid in self.E:
            self.log.append("%s: given a figure twice" % qid)
            return
        self.E[qid] = entry

    def save(self):
        out = {}
        for qid in sorted(self.E):
            out[qid] = self.E[qid]
        with io.open(self.path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
            f.write("\n")
        kinds = {}
        for e in out.values():
            fig = e.get("figure")
            if fig is None:
                fig = next(f for f in e["stepFigures"] if f is not None)
                key = fig["kind"] + " (steps only)"
            else:
                key = fig["kind"]
            kinds[key] = kinds.get(key, 0) + 1
        print("%s: %d of %d questions have a visual (%d with a before-answering figure, %d with step figures)" % (
            self.topic, len(out), len(self.Q), sum(1 for e in out.values() if "figure" in e),
            sum(1 for e in out.values() if "stepFigures" in e)))
        print("  by rule %d, individually drawn %d, essential %d" % (
            sum(1 for e in out.values() if e["origin"] == "rule"),
            sum(1 for e in out.values() if e["origin"] == "authored"),
            sum(1 for e in out.values() if e.get("essential"))))
        for k in sorted(kinds):
            print("  %3d  %s" % (kinds[k], k))
        if self.log:
            print("  %d notes:" % len(self.log))
            for line in self.log:
                print("    " + line)
        print("  wrote " + os.path.relpath(self.path, ROOT))
