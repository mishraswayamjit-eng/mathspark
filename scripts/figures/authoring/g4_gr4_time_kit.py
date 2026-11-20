"""Shared kit for the Grade 4 figure scripts g4_gr4_time.py, g4_gr4_data.py and g4_gr4_puzzles.py.

A script makes a Part for its topic, calls part.put(...) once per question, then part.write().
Every figure is run through the checker's own rules (validate.check_figure and the grounding
rule) before it is kept, and every finished entry through validate.check_entry. Anything the
checker would refuse is printed and left out, so the output file is always valid.
"""
import collections
import datetime
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
import validate  # noqa: E402

bank = validate.bank
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def weekday(y, m, d):
    """Full name of the weekday of a real date."""
    return DAYS[datetime.date(y, m, d).weekday()]


def ints(text):
    """The whole numbers written in a text, in order ('2,345' is 2345)."""
    return [int(x) for x in re.findall(r"\d+", re.sub(r"(?<=\d),(?=\d)", "", text))]


# ── Figure builders ──────────────────────────────────────────────────────────

def _base(fig, note, hl):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def T(rows, headers=None, note=None, hl=None):
    fig = {"kind": "table", "rows": [[str(c) for c in r] for r in rows]}
    if headers:
        fig["headers"] = [str(h) for h in headers]
    return _base(fig, note, hl)


def BC(pairs, unit=None, each=None, note=None, hl=None):
    fig = {"kind": "barChart", "bars": [{"label": str(a), "value": b} for a, b in pairs]}
    if unit:
        fig["unit"] = unit
    if each:
        fig["each"] = each
    return _base(fig, note, hl)


def BM(bars, note=None, hl=None):
    """bars: (label or None, [segments], brace or None). A segment is (units, label or None[, tone])."""
    out = []
    # `units` only sets widths (0.2 to 20): scale every bar alike so the widest piece is at most 12.
    widest = max(float(s[0]) for _, segs, _ in bars for s in segs)
    scale = 12.0 / widest if widest > 12 else 1.0
    for bi, (label, segs, brace) in enumerate(bars):
        ss = []
        for si, s in enumerate(segs):
            seg = {"units": max(0.2, round(float(s[0]) * scale, 2))}
            if s[1] is not None:
                seg["label"] = str(s[1])
            if len(s) > 2:
                seg["tone"] = s[2]
            elif s[1] is not None and str(s[1]).startswith("?"):
                seg["tone"] = "unknown"
            else:
                seg["tone"] = "abc"[bi % 3]
            ss.append(seg)
        bar = {"segments": ss}
        if label:
            bar["label"] = label
        if brace:
            bar["brace"] = brace
        out.append(bar)
    return _base({"kind": "barModel", "bars": out}, note, hl)


def NL(lo, hi, step=1, points=(), hops=(), ticks=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if ticks:
        fig["tickLabels"] = ticks
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    if hops:
        fig["hops"] = [({"from": h[0], "to": h[1], "label": h[2]} if len(h) > 2 and h[2] else {"from": h[0], "to": h[1]}) for h in hops]
    return _base(fig, note, hl)


def CL(hour, minute, angle=False, note=None, hl=None):
    fig = {"kind": "clock", "hour": hour, "minute": minute}
    if angle:
        fig["showAngle"] = True
    return _base(fig, note, hl)


def J(places, legs, note=None, hl=None):
    """legs: (top, bottom) per stretch, either may be None."""
    out = []
    for leg in legs:
        one = {}
        if leg and leg[0]:
            one["top"] = leg[0]
        if leg and len(leg) > 1 and leg[1]:
            one["bottom"] = leg[1]
        out.append(one)
    return _base({"kind": "journey", "places": list(places), "legs": out}, note, hl)


def V(left_title, right_title, left, both, right, note=None, hl=None):
    return _base({"kind": "venn", "leftTitle": left_title, "rightTitle": right_title,
                  "left": left, "both": both, "right": right}, note, hl)


def BAL(left, right, note=None, hl=None):
    return _base({"kind": "balance", "left": left, "right": right}, note, hl)


def FB(bars, shape=None, note=None, hl=None):
    """bars: (parts, shaded[, label])."""
    out = []
    for b in bars:
        one = {"parts": b[0], "shaded": b[1]}
        if len(b) > 2 and b[2]:
            one["label"] = b[2]
        out.append(one)
    fig = {"kind": "fractionBars", "bars": out}
    if shape:
        fig["shape"] = shape
    return _base(fig, note, hl)


def SET(total, groups=None, shaded=None, item=None, note=None, hl=None):
    fig = {"kind": "set", "total": total}
    if groups:
        fig["groups"] = groups
    if shaded is not None:
        fig["shadedGroups"] = shaded
    if item:
        fig["item"] = item
    return _base(fig, note, hl)


def ANG(layout, parts, note=None, hl=None):
    """parts: (label[, size])."""
    out = []
    for p in parts:
        one = {"label": p[0]}
        if len(p) > 1 and p[1]:
            one["size"] = p[1]
        out.append(one)
    return _base({"kind": "angles", "layout": layout, "parts": out}, note, hl)


def renote(fig, note=None, hl=None):
    """A copy of a figure with another note and highlight."""
    out = json.loads(json.dumps(fig))
    out.pop("note", None)
    out.pop("highlight", None)
    return _base(out, note, hl)


# ── A part file ──────────────────────────────────────────────────────────────

class Part(object):
    def __init__(self, topic):
        self.topic = topic
        self.qs = collections.OrderedDict((q["id"], q) for q in bank.load_bank(4) if q.get("node") == topic)
        self.out = collections.OrderedDict()
        self.problems = []
        self.path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)

    def q(self, qid):
        return self.qs[qid]

    def text(self, qid):
        return self.qs[qid].get("questionText", "")

    def steps(self, qid):
        return self.qs[qid].get("stepByStep") or []

    def answer(self, qid):
        return validate.correct_text(self.qs[qid])

    def opts(self, qid):
        return validate.option_texts(self.qs[qid])

    def allowed(self, qid, i=None, uses_options=False):
        """Numbers the checker lets a figure show: before answering (i None) or at step i."""
        q = self.qs[qid]
        out = validate.numbers_in(q.get("questionText", ""))
        if i is not None or uses_options:
            for t in validate.option_texts(q):
                out |= validate.numbers_in(t)
        if i is not None:
            for s in self.steps(qid)[:i + 1]:
                out |= validate.numbers_in(s.get("text", ""))
        return out

    def why_not(self, qid, fig, i=None, uses_options=False):
        """'' if the checker would take this figure here, else the reason."""
        ctx = validate.check_figure(fig, "f")
        if ctx.errors:
            return "; ".join(ctx.errors)
        extra = validate.ungrounded(ctx.numbers, self.allowed(qid, i, uses_options))
        return ("shows " + validate.fmt(extra)) if extra else ""

    def put(self, qid, before=None, steps=None, origin="authored", essential=False, uses_options=False):
        """steps: {step index: figure, or a list of figures (the first the checker allows is used)}."""
        if qid not in self.qs:
            self.problems.append("%s: not a question of %s" % (qid, self.topic))
            return
        if qid in self.out:
            self.problems.append("%s: given a figure twice" % qid)
            return
        n = len(self.steps(qid))
        entry = {"origin": origin}
        if before is not None:
            bad = "" if essential and not validate.check_figure(before, "f").errors else self.why_not(qid, before, None, uses_options)
            if bad:
                self.problems.append("%s figure: %s" % (qid, bad))
            else:
                entry["figure"] = before
        if steps:
            figs = []
            for i in range(n):
                cand = steps.get(i)
                alts = cand if isinstance(cand, list) else [cand]
                chosen, reasons = None, []
                for a in alts:
                    if a is None:
                        continue
                    bad = self.why_not(qid, a, i)
                    if not bad:
                        chosen = a
                        break
                    reasons.append(bad)
                if chosen is None and reasons:
                    self.problems.append("%s step %d: %s" % (qid, i, " | ".join(reasons)))
                figs.append(chosen)
            for i in steps:
                if i >= n:
                    self.problems.append("%s: step %d does not exist (%d steps)" % (qid, i, n))
            if any(f is not None for f in figs):
                entry["stepFigures"] = figs
        if uses_options:
            entry["usesOptions"] = True
        if essential:
            entry["essential"] = True
        if "figure" not in entry and "stepFigures" not in entry:
            self.problems.append("%s: nothing left to keep" % qid)
            return
        bad = validate.check_entry(qid, entry, self.qs[qid])
        if bad:
            self.problems.extend(bad)
            return
        self.out[qid] = entry

    def write(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with io.open(self.path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(self.out, f, ensure_ascii=False, indent=1)
            f.write("\n")
        kinds = collections.Counter()
        for e in self.out.values():
            kinds[e["figure"]["kind"] if "figure" in e else "(step figures only)"] += 1
        origin = collections.Counter(e["origin"] for e in self.out.values())
        nsteps = sum(1 for e in self.out.values() if "stepFigures" in e)
        print("%s: %d of %d questions have a visual; %d with a figure before answering; %d with step figures" % (
            self.topic, len(self.out), len(self.qs), sum(1 for e in self.out.values() if "figure" in e), nsteps))
        print("  by kind: " + ", ".join("%s %d" % kv for kv in kinds.most_common()))
        print("  by rule %d, individually drawn %d, essential %d" % (
            origin["rule"], origin["authored"], sum(1 for e in self.out.values() if e.get("essential"))))
        print("  no visual: " + ", ".join(i for i in self.qs if i not in self.out))
        if self.problems:
            print("\n%d THINGS LEFT OUT" % len(self.problems))
            for p in self.problems:
                print("  " + (p if len(p) < 260 else p[:260] + " ..."))
        print("wrote " + os.path.relpath(self.path, ROOT))
