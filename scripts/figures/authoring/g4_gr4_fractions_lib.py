"""Shared helpers for the Grade 4 fractions and ratio figure scripts.

A figure is only kept where every number it shows is already stated at that point
(the same test scripts/figures/validate.py applies). Each step may be given several
candidate figures, richest first; the first one that passes is used, else no figure.
"""
import collections
import copy
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.join(ROOT, "scripts", "figures"))
import bank  # noqa: E402
import validate  # noqa: E402  (read-only: check_figure, numbers_in, CONSTANTS)

PARTS = os.path.join(ROOT, "data", "question-figures", "parts")


def load(node):
    qs = [q for q in bank.load_bank(4) if q.get("node") == node]
    qs.sort(key=lambda q: q["id"])
    return qs


# ── Figure constructors ──────────────────────────────────────────────────────

def w(fig, note=None, hl=None):
    """A copy of a figure with a different note and highlight."""
    out = copy.deepcopy(fig)
    out.pop("note", None)
    out.pop("highlight", None)
    if note:
        out["note"] = note
    if hl:
        out["highlight"] = list(hl)
    return out


def fb(bars, note=None, hl=None, shape=None):
    """Fraction bars: each bar is (parts, shaded) or (parts, shaded, label)."""
    out = []
    for b in bars:
        d = {"parts": b[0], "shaded": b[1]}
        if len(b) > 2 and b[2]:
            d["label"] = b[2]
        out.append(d)
    fig = {"kind": "fractionBars", "bars": out}
    if shape:
        fig["shape"] = shape
    return w(fig, note, hl)


def seg(label=None, units=1, tone=None):
    s = {"units": units}
    if label:
        s["label"] = label
    if tone:
        s["tone"] = tone
    return s


def segs(count, label=None, tone=None, units=1):
    return [seg(label, units, tone) for _ in range(count)]


def bar(segments, label=None, brace=None):
    b = {"segments": segments}
    if label:
        b["label"] = label
    if brace:
        b["brace"] = brace
    return b


def bm(bars, note=None, hl=None):
    return w({"kind": "barModel", "bars": bars}, note, hl)


def table(headers, rows, note=None, hl=None):
    fig = {"kind": "table", "rows": rows}
    if headers:
        fig["headers"] = headers
    return w(fig, note, hl)


def setf(total, groups=None, shaded=None, item=None, note=None, hl=None):
    fig = {"kind": "set", "total": total}
    if groups:
        fig["groups"] = groups
    if shaded is not None:
        fig["shadedGroups"] = shaded
    if item:
        fig["item"] = item
    return w(fig, note, hl)


def balance(left, right, note=None, hl=None):
    return w({"kind": "balance", "left": left, "right": right}, note, hl)


def nline(lo, hi, step, points=None, hops=None, ticks=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if ticks:
        fig["tickLabels"] = ticks
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    if hops:
        fig["hops"] = [({"from": h[0], "to": h[1], "label": h[2]} if len(h) > 2 and h[2] else {"from": h[0], "to": h[1]}) for h in hops]
    return w(fig, note, hl)


def ft(n, d):
    return "%d/%d" % (n, d)


# ── Grounding ────────────────────────────────────────────────────────────────

class Q(object):
    """One bank question with the numbers a figure may show at each point."""

    def __init__(self, q):
        self.q = q
        self.id = q["id"]
        self.text = q["questionText"].strip()
        self.steps = q.get("stepByStep") or []
        self.n = len(self.steps)
        self.qnums = validate.numbers_in(q.get("questionText", ""))
        self.onums = set()
        for t in validate.option_texts(q):
            self.onums |= validate.numbers_in(t)
        self.answer = validate.correct_text(q)

    def allowed(self, i):
        out = self.qnums | self.onums
        for s in self.steps[:i + 1]:
            out = out | validate.numbers_in(s.get("text", ""))
        return out

    def extra(self, fig, allowed):
        """Numbers the figure shows that are not allowed. Raises if the figure is malformed."""
        ctx = validate.check_figure(fig, self.id)
        if ctx.errors:
            raise ValueError("%s: %s\n%s" % (self.id, "; ".join(ctx.errors), json.dumps(fig, ensure_ascii=False)))
        return validate.ungrounded(ctx.numbers, allowed)


FALLBACKS = collections.Counter()


def entry(Qq, figure=None, steps=None, origin="authored", uses_options=False, essential=False):
    """Build a QuestionVisual. `steps` items are None, a figure, or a list of candidates."""
    e = {"origin": origin}
    if figure is not None:
        allowed = Qq.qnums | (Qq.onums if uses_options else set())
        bad = [] if essential else Qq.extra(figure, allowed)
        if bad:
            raise ValueError("%s figure shows %s, not in the question" % (Qq.id, bad))
        e["figure"] = figure
    if steps is not None:
        if len(steps) > Qq.n:
            raise ValueError("%s: %d step figures for %d steps" % (Qq.id, len(steps), Qq.n))
        figs = []
        for i in range(Qq.n):
            cands = steps[i] if i < len(steps) else None
            if cands is None:
                figs.append(None)
                continue
            if isinstance(cands, dict):
                cands = [cands]
            chosen = None
            for k, c in enumerate(cands):
                if c is None:
                    break
                if not Qq.extra(c, Qq.allowed(i)):
                    chosen = c
                    if k:
                        FALLBACKS["used candidate %d" % (k + 1)] += 1
                    break
            if chosen is None:
                FALLBACKS["no figure fits"] += 1
            figs.append(chosen)
        if any(f is not None for f in figs):
            e["stepFigures"] = figs
    if uses_options:
        e["usesOptions"] = True
    if essential:
        e["essential"] = True
    if "figure" not in e and "stepFigures" not in e:
        return None
    return e


def write(name, out):
    path = os.path.join(PARTS, name)
    os.makedirs(PARTS, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return path


def brief(fig):
    if fig is None:
        return "-"
    f = dict(fig)
    kind = f.pop("kind")
    tail = ""
    if f.get("note"):
        tail += "  note=%r" % f["note"]
    if f.get("highlight"):
        tail += "  hl=%s" % ",".join(f["highlight"])
    if kind == "barModel":
        rows = []
        for b in f["bars"]:
            run, prev = [], None
            for s in b["segments"]:
                key = (s.get("label", ""), s["units"], s.get("tone", "")[:1])
                if prev and prev[0] == key:
                    prev[1] += 1
                else:
                    prev = [key, 1]
                    run.append(prev)
            body = " | ".join("%s%s:%g%s" % ("%dx " % n if n > 1 else "", k[0] or "_", k[1], k[2]) for k, n in run)
            rows.append("%s[%s]{%s}" % (b.get("label", ""), body, b.get("brace", "")))
        return "BM " + " ; ".join(rows) + tail
    if kind == "fractionBars":
        return "FB%s " % ("(circle)" if f.get("shape") == "circle" else "") + " ; ".join(
            "%d/%d%s" % (b["shaded"], b["parts"], " '%s'" % b["label"] if b.get("label") else "") for b in f["bars"]) + tail
    if kind == "table":
        return "TABLE %s :: %s" % (" , ".join(f.get("headers", [])), " ; ".join(" , ".join(r) for r in f["rows"])) + tail
    return "%s %s" % (kind, json.dumps(f, ensure_ascii=False, separators=(",", ":")))


def report(node, questions, out, rule_of, show=None):
    """Print the counts the brief asks for, and optionally entries for review."""
    kinds = collections.Counter()
    for e in out.values():
        kinds[e["figure"]["kind"] if "figure" in e else "(steps only)"] += 1
    print("%s: %d of %d questions have a visual; %d have a figure before answering" % (
        node, len(out), len(questions), sum(1 for e in out.values() if "figure" in e)))
    print("  by kind of the before-answering figure: %s" % dict(kinds.most_common()))
    step_kinds = collections.Counter()
    filled = total = 0
    for e in out.values():
        for f in e.get("stepFigures", []):
            total += 1
            if f:
                filled += 1
                step_kinds[f["kind"]] += 1
    print("  step figures: %d of %d steps drawn: %s" % (filled, total, dict(step_kinds.most_common())))
    print("  by rule: %d, individually drawn: %d, essential: %d" % (
        sum(1 for e in out.values() if e["origin"] == "rule"),
        sum(1 for e in out.values() if e["origin"] == "authored"),
        sum(1 for e in out.values() if e.get("essential"))))
    print("  rules: %s" % dict(collections.Counter(rule_of.values()).most_common()))
    print("  fallbacks: %s" % dict(FALLBACKS))
    if show:
        by_id = {q["id"]: q for q in questions}
        ids = sorted(out) if show == "all" else [i for i in sorted(out) if show in i or show == rule_of.get(i)]
        for qid in ids:
            q, e = by_id[qid], out[qid]
            print("\n== %s (%s) ans=%s %s" % (qid, e["origin"], q["correctAnswer"], validate.correct_text(q)))
            print("   Q: %s" % q["questionText"].replace("\n", " / "))
            print("   O: %s" % " | ".join(o["text"] for o in q["options"]))
            print("   FIG: %s" % brief(e.get("figure")))
            sf = e.get("stepFigures") or [None] * len(q.get("stepByStep") or [])
            for s, f in zip(q.get("stepByStep") or [], sf):
                print("   s%s: %s" % (s.get("step"), s.get("text", "")))
                print("       -> %s" % brief(f))
