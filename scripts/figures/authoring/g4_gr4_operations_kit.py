"""Shared helpers for the Grade 4 figure scripts g4_gr4_operations.py and g4_gr4_units.py.

Small constructors for figure specs, a cleaner that runs the checker on every entry
before anything is written, and a side-by-side review printer.
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.join(ROOT, "scripts", "figures"))
import bank  # noqa: E402
import validate  # noqa: E402  (importing does not run it)

PARTS = os.path.join(ROOT, "data", "question-figures", "parts")
BAR_WIDTH = 290.0  # drawn width of the longest bar, in SVG units (see kinds/number.tsx)


def load(topic):
    qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
    qs.sort(key=lambda q: q["id"])
    return qs


def step_texts(q):
    return [(s.get("text") or "") for s in (q.get("stepByStep") or [])]


def answer_text(q):
    return validate.correct_text(q)


def num(text):
    """'1,224' -> 1224, '4.5' -> 4.5"""
    v = float(text.replace(",", ""))
    return int(v) if v == int(v) else v


def show(n):
    """A number as a child reads it: 8500, 4.5"""
    return ("%g" % n) if isinstance(n, float) else str(n)


# ── constructors ─────────────────────────────────────────────────────────────

def _base(fig, note=None, hl=None):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def seg(label=None, units=1, tone=None):
    s = {"units": units}
    if label:
        s["label"] = label
    if tone:
        s["tone"] = tone
    return s


def bar(segments, label=None, brace=None):
    b = {"segments": segments}
    if label:
        b["label"] = label
    if brace:
        b["brace"] = brace
    return b


def bm(bars, note=None, hl=None):
    """A bar model. Pieces are given in the question's own quantities (grams, rupees, ...)
    and rescaled here, all by the same factor, into the 0.2 to 20 range the type allows,
    so the picture stays in proportion."""
    biggest = max(float(s["units"]) for b in bars for s in b["segments"])
    scaled = []
    for b in bars:
        nb = dict(b)
        nb["segments"] = [dict(s, units=max(0.2, round(float(s["units"]) * 10.0 / biggest, 3))) for s in b["segments"]]
        scaled.append(nb)
    return _base({"kind": "barModel", "bars": scaled}, note, hl)


def fits(label, share):
    """Would this label sit inside a piece that is `share` of the bar's width?"""
    return len(label) * 6.4 <= BAR_WIDTH * share - 4


def equal_segs(n, label=None, tone="a", first_tone=None, first_label=None):
    """n equal pieces. The label goes on every piece when it fits, else on the first only."""
    every = label is not None and fits(label, 1.0 / n)
    out = []
    for i in range(n):
        text = label if (every or i == 0) else None
        t = tone
        if i == 0 and first_label is not None:
            text = first_label
        if i == 0 and first_tone is not None:
            t = first_tone
        out.append(seg(text, 1, t))
    return out


def nl(lo, hi, step, points=None, hops=None, note=None, hl=None, ticks=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if ticks:
        fig["tickLabels"] = ticks
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    if hops:
        fig["hops"] = [({"from": h[0], "to": h[1], "label": h[2]} if len(h) > 2 and h[2] else {"from": h[0], "to": h[1]}) for h in hops]
    return _base(fig, note, hl)


def table(rows, headers=None, note=None, hl=None):
    fig = {"kind": "table", "rows": rows}
    if headers:
        fig["headers"] = headers
    return _base(fig, note, hl)


def fb(bars, note=None, hl=None, shape=None):
    out = []
    for b in bars:
        d = {"parts": b[0], "shaded": b[1]}
        if len(b) > 2 and b[2]:
            d["label"] = b[2]
        out.append(d)
    fig = {"kind": "fractionBars", "bars": out}
    if shape:
        fig["shape"] = shape
    return _base(fig, note, hl)


def setf(total, groups=None, shaded=None, item=None, note=None, hl=None):
    fig = {"kind": "set", "total": total}
    if groups:
        fig["groups"] = groups
    if shaded is not None:
        fig["shadedGroups"] = shaded
    if item:
        fig["item"] = item
    return _base(fig, note, hl)


def pc(number, note=None, hl=None):
    return _base({"kind": "placeChart", "number": number}, note, hl)


def grid(rows, cols, note=None):
    return _base({"kind": "grid", "rows": rows, "cols": cols}, note)


def journey(places, legs, note=None, hl=None):
    return _base({"kind": "journey", "places": places, "legs": legs}, note, hl)


def step_figs(q, figs):
    """A stepFigures list for q from {step index: figure}; negative indexes count from the end."""
    n = len(q.get("stepByStep") or [])
    out = [None] * n
    for i, fig in figs.items():
        if fig is None:
            continue
        if not (-n <= i < n):
            raise ValueError("%s has %d steps, no step %d" % (q["id"], n, i))
        out[i] = fig
    return out


def entry(origin, figure=None, steps=None, essential=False, uses_options=False):
    e = {"origin": origin}
    if figure:
        e["figure"] = figure
    if steps and any(s is not None for s in steps):
        e["stepFigures"] = steps
    if essential:
        e["essential"] = True
    if uses_options:
        e["usesOptions"] = True
    return e


# ── checking, writing, reviewing ─────────────────────────────────────────────

def clean(qid, e, q, log):
    """Run the checker on one entry. A figure that breaks a rule is taken out (and logged
    so it can be fixed in the script); the rest of the entry stays. None if nothing is left."""
    for _ in range(8):
        problems = validate.check_entry(qid, e, q)
        if not problems:
            break
        changed = False
        for p in problems:
            log.append(p)
            m = re.match(re.escape(qid) + r"\.stepFigures\[(\d+)\]", p)
            if m:
                if e["stepFigures"][int(m.group(1))] is not None:
                    e["stepFigures"][int(m.group(1))] = None
                    changed = True
            elif p.startswith(qid + ".figure") and "figure" in e:
                del e["figure"]
                e.pop("essential", None)
                changed = True
        if "stepFigures" in e and not any(s is not None for s in e["stepFigures"]):
            del e["stepFigures"]
            changed = True
        if "figure" not in e and "stepFigures" not in e:
            return None
        if not changed:
            raise SystemExit("cannot repair %s: %s" % (qid, problems))
    return e


def finish(topic, questions, out, argv):
    """Clean every entry, write the part file, print the counts, and optionally review."""
    by_id = {q["id"]: q for q in questions}
    log = []
    final = {}
    for qid in sorted(out):
        e = clean(qid, out[qid], by_id[qid], log)
        if e is not None:
            final[qid] = e
    path = os.path.join(PARTS, "g4-%s.json" % topic)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(final, f, ensure_ascii=False, indent=1)
        f.write("\n")

    kinds = collections.Counter(e["figure"]["kind"] for e in final.values() if "figure" in e)
    step_kinds = collections.Counter()
    for e in final.values():
        for s in e.get("stepFigures", []):
            if s:
                step_kinds[s["kind"]] += 1
    print("%s: %d of %d questions have a visual" % (topic, len(final), len(questions)))
    print("  with a figure before answering: %d  %s" % (sum(kinds.values()), dict(kinds)))
    print("  step figures only: %d" % sum(1 for e in final.values() if "figure" not in e))
    print("  step figures drawn: %d  %s" % (sum(step_kinds.values()), dict(step_kinds)))
    print("  by rule: %d   individually drawn: %d   essential: %d" % (
        sum(1 for e in final.values() if e["origin"] == "rule"),
        sum(1 for e in final.values() if e["origin"] == "authored"),
        sum(1 for e in final.values() if e.get("essential"))))
    print("  wrote %s" % os.path.relpath(path, ROOT))
    if log:
        print("\n%d figures were taken out by the checker (fix these in the script):" % len(log))
        for p in log:
            print("  " + p)

    if len(argv) > 1 and argv[1] == "review":
        rx = re.compile(argv[2]) if len(argv) > 2 else None
        for qid in sorted(final):
            if rx and not rx.search(qid):
                continue
            review(by_id[qid], final[qid])
    if len(argv) > 1 and argv[1] == "missing":
        for q in questions:
            if q["id"] not in final:
                print("-- %s: %s" % (q["id"], q["questionText"].replace("\n", " / ")[:150]))


def brief(fig):
    if fig is None:
        return "-"
    if fig["kind"] == "barModel":
        bars = []
        for b in fig["bars"]:
            runs = []
            for s in b["segments"]:
                key = "%s(%g%s)" % (s.get("label", "_"), s["units"], "" if s.get("tone", "a") == "a" else "," + s["tone"])
                if runs and runs[-1][0] == key:
                    runs[-1][1] += 1
                else:
                    runs.append([key, 1])
            body = " | ".join(k if n == 1 else "%s x%d" % (k, n) for k, n in runs)
            bars.append("%s{%s}: [%s]" % (b.get("label", ""), b.get("brace", ""), body))
        extra = "".join("  %s=%s" % (k, json.dumps(fig[k], ensure_ascii=False)) for k in ("note", "highlight") if k in fig)
        return "BAR " + "  //  ".join(bars) + extra
    return json.dumps(fig, ensure_ascii=False, separators=(",", ":"))


def review(q, e):
    print("\n## %s  (%s%s) ans=%s" % (q["id"], e["origin"], ", essential" if e.get("essential") else "", q["correctAnswer"]))
    print("Q: " + q["questionText"].replace("\n", " / "))
    print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
    print("FIG: " + brief(e.get("figure")))
    figs = e.get("stepFigures") or []
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  s%d: %s   [%s]" % (i, (s.get("text") or "").replace("\n", " / "), (s.get("latex") or "").replace("\n", " ")))
        print("      " + brief(figs[i] if i < len(figs) else None))
