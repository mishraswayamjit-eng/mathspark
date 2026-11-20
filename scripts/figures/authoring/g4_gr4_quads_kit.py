"""Shared kit for the Grade 4 quadrilateral and circle figures (g4_gr4_quads.py, g4_gr4_circle.py).

A Part collects one QuestionVisual per question and writes the part file:

    part = Part("gr4_quads")
    part.add(qid, figure=fig, steps={0: fig, 2: [fig_a, fig_b]}, origin="rule")
    part.build()

Anywhere a figure is expected you may give a list of alternatives, and a figure's
`note` may itself be a list of alternative notes (None = no note). The build keeps
the first alternative whose numbers have all been stated by that point (question
text for the before-answering figure; question, answer choices and the steps so
far for a step figure), so a figure never shows a number the child has not met.
"""
import io
import json
import math
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.join(ROOT, "scripts", "figures"))
import bank  # noqa: E402
import validate  # noqa: E402  (read only: the checker's own number rules)

PARTS = os.path.join(ROOT, "data", "question-figures", "parts")


def n(x):
    """A number as a child would write it: 12, 1.5, 60.75."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return ("%.4f" % x).rstrip("0").rstrip(".")


# ── Constructors ─────────────────────────────────────────────────────────────

def _base(fig, note=None, hl=None):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def R(length=None, breadth=None, inside=None, square=False, prop=None, grid=None, note=None, hl=None):
    fig = {"kind": "rectangle"}
    if square:
        fig["square"] = True
    if length:
        fig["length"] = length
    if breadth:
        fig["breadth"] = breadth
    if inside:
        fig["inside"] = inside
    if prop and not square and not grid:
        fig["proportion"] = round(min(3.0, max(1.0, prop)), 2)
    if grid:
        fig["grid"] = {"cols": grid[0], "rows": grid[1]}
    return _base(fig, note, hl)


def T(shape, sides=None, angles=None, height=None, note=None, hl=None):
    fig = {"kind": "triangle", "shape": shape}
    if sides:
        fig["sides"] = {k: v for k, v in sides.items() if v}
    if angles:
        fig["angles"] = {k: v for k, v in angles.items() if v}
    if height:
        fig["height"] = height
    return _base(fig, note, hl)


def P(points, edges=None, corners=None, right=None, dashed=None, note=None, hl=None):
    fig = {"kind": "polygon", "points": [[round(x, 2), round(y, 2)] for x, y in points]}
    if edges and any(edges):
        fig["edges"] = list(edges)
    if corners and any(corners):
        fig["corners"] = list(corners)
    if right:
        fig["rightAngles"] = list(right)
    if dashed:
        fig["dashed"] = [({"from": d[0], "to": d[1], "label": d[2]} if len(d) > 2 else {"from": d[0], "to": d[1]}) for d in dashed]
    return _base(fig, note, hl)


def C(radius=None, diameter=None, note=None, hl=None):
    fig = {"kind": "circle"}
    if radius:
        fig["radius"] = radius
    if diameter:
        fig["diameter"] = diameter
    return _base(fig, note, hl)


def A(layout, parts, note=None, hl=None):
    out = []
    for p in parts:
        d = {"label": p[0]}
        if len(p) > 1 and p[1]:
            d["size"] = p[1]
        out.append(d)
    return _base({"kind": "angles", "layout": layout, "parts": out}, note, hl)


def BM(bars, note=None, hl=None):
    """bars: each a dict {segs: [(units, label, tone)], label, brace} or just a list of segs."""
    out = []
    for b in bars:
        if isinstance(b, list):
            b = {"segs": b}
        ss = []
        for s in b["segs"]:
            d = {"units": s[0]}
            if len(s) > 1 and s[1]:
                d["label"] = s[1]
            if len(s) > 2 and s[2]:
                d["tone"] = s[2]
            ss.append(d)
        bar = {"segments": ss}
        if b.get("label"):
            bar["label"] = b["label"]
        if b.get("brace"):
            bar["brace"] = b["brace"]
        out.append(bar)
    return _base({"kind": "barModel", "bars": out}, note, hl)


def NL(lo, hi, step, points=None, labels=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if labels:
        fig["tickLabels"] = labels
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    return _base(fig, note, hl)


def TABLE(headers, rows, note=None, hl=None):
    return _base({"kind": "table", "headers": list(headers), "rows": [list(r) for r in rows]}, note, hl)


def GRID(rows, cols, shaded=None, note=None):
    fig = {"kind": "grid", "rows": rows, "cols": cols}
    if shaded:
        fig["shaded"] = [list(c) for c in shaded]
    return _base(fig, note)


def CHART(bars, unit=None, note=None, hl=None):
    fig = {"kind": "barChart", "bars": [{"label": b[0], "value": b[1]} for b in bars]}
    if unit:
        fig["unit"] = unit
    return _base(fig, note, hl)


def CLOCK(hour, minute=0, note=None, hl=None):
    return _base({"kind": "clock", "hour": hour, "minute": minute}, note, hl)


# ── Shapes drawn true to their numbers ───────────────────────────────────────

_POLY_KEYS = {"length": ["e0"], "breadth": ["e3"], "border": ["e0", "e1", "e2", "e3"], "fill": ["fill"]}


def rect(L, W, ll=None, lb=None, inside=None, note=None, hl=None):
    """A rectangle L by W in true proportion, long side on top.

    Up to 3:1 this is the renderer's own rectangle (which can carry `inside`).
    A longer strip is drawn as a polygon so it keeps its true shape; a polygon
    has no inside text, so `inside` then moves to the note when no note is given.
    highlight keys are the rectangle's: length, breadth, border, fill.
    """
    ratio = float(L) / float(W)
    if ratio <= 3.0:
        return R(length=ll, breadth=lb, inside=inside, prop=ratio, note=note, hl=hl)
    s = 12.0 / L
    keys = []
    for k in hl or []:
        keys += _POLY_KEYS[k]
    return P([(0, 0), (12, 0), (12, W * s), (0, W * s)], edges=[ll, None, None, lb], note=note or inside, hl=keys)


def split_rect(L, W, which, a, b, ll=None, lb=None, la=None, lpb=None, note=None, hl=None):
    """A rectangle L by W cut by one dashed line, in true proportion.

    which='breadth': the breadth is cut into a (top) and b (bottom); the pieces are
                     labelled down the right side, the length along the top.
    which='length':  the length is cut into a (left) and b (right); the pieces are
                     labelled along the top, the breadth on the left.
    highlight keys: 'a', 'b' (the two pieces), 'length', 'breadth', 'fill'.
    """
    s = 12.0 / max(L, W)
    X, Y = L * s, W * s
    if which == "breadth":
        pts = [(0, 0), (X, 0), (X, a * s), (X, Y), (0, Y), (0, a * s)]
        edges = [ll, la, lpb, None, None, None]
        dashed = [(2, 5)]
        keys = {"a": ["e1"], "b": ["e2"], "length": ["e0"], "breadth": ["e1", "e2"], "fill": ["fill"]}
    else:
        pts = [(0, 0), (a * s, 0), (X, 0), (X, Y), (a * s, Y), (0, Y)]
        edges = [la, lpb, None, None, None, lb]
        dashed = [(1, 4)]
        keys = {"a": ["e0"], "b": ["e1"], "length": ["e0", "e1"], "breadth": ["e5"], "fill": ["fill"]}
    out = []
    for k in hl or []:
        out += keys[k]
    return P(pts, edges=edges, dashed=dashed, note=note, hl=out)


def square4(label, note=None, hl=True, size=8):
    """A square with the same label on all four sides (for perimeters)."""
    return P([(0, 0), (size, 0), (size, size), (0, size)], edges=[label] * 4, note=note,
             hl=["e0", "e1", "e2", "e3"] if hl else None)


def _fit(pts, size=11.0):
    """Move a shape (y up) into the 0-12 grid (y down), biggest side `size`."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    s = size / max(max(xs) - min(xs), max(ys) - min(ys))
    return [((x - min(xs)) * s, (max(ys) - y) * s) for x, y in pts]


def quad_angles(a, b, c, d, labels, s1=8.0, s2=5.0, note=None, hl=None):
    """A quadrilateral with its four angles drawn at their true sizes.

    Corners run bottom left (a), bottom right (b), top right (c), top left (d).
    `labels` are the four corner labels in that order.
    """
    if abs(a + b + c + d - 360) > 0.01:
        raise SystemExit("angles %s %s %s %s do not add up to 360" % (a, b, c, d))
    Bx, By = s1, 0.0
    t1 = math.radians(180 - b)
    Cx, Cy = Bx + s2 * math.cos(t1), By + s2 * math.sin(t1)
    ta = math.radians(a)
    tc = math.radians(360 - b - c)
    # A + t(cos ta, sin ta) = C + u(cos tc, sin tc)
    det = math.cos(ta) * (-math.sin(tc)) - (-math.cos(tc)) * math.sin(ta)
    t = (Cx * (-math.sin(tc)) - (-math.cos(tc)) * Cy) / det
    u = (math.cos(ta) * Cy - math.sin(ta) * Cx) / det
    if t <= 0.5 or u <= 0.5:
        raise SystemExit("angles %s %s %s %s: pick other side lengths" % (a, b, c, d))
    Dx, Dy = t * math.cos(ta), t * math.sin(ta)
    pts = _fit([(0.0, 0.0), (Bx, By), (Cx, Cy), (Dx, Dy)])
    right = [i for i, v in enumerate((a, b, c, d)) if abs(v - 90) < 0.01 and labels[i] and labels[i] != "?"]
    return P(pts, corners=labels, right=right, note=note, hl=hl)


def tri_sides(base, left, right, lbase=None, lleft=None, lright=None, corners=None, note=None, hl=None):
    """A triangle drawn to its true shape from its three sides.
    Corners run A (top), B (bottom left), C (bottom right): e0 = AB, e1 = BC, e2 = CA."""
    x = (left * left + base * base - right * right) / (2.0 * base)
    h2 = left * left - x * x
    if h2 <= 1e-9:
        raise SystemExit("sides %s, %s, %s do not make a triangle" % (base, left, right))
    pts = _fit([(x, math.sqrt(h2)), (0.0, 0.0), (base, 0.0)])
    return P(pts, edges=[lleft, lbase, lright], corners=corners, note=note, hl=hl)


def strip_frame(outer_l, outer_b, width, lwidth=None, lmid_top=None, lmid_left=None, note=None, hl=None):
    """A rectangle with a strip of the same width along all four sides (a path),
    marked off by four dashed lines. e0 is the strip's width at the top left corner,
    e1 the middle of the top side, e10 the middle of the left side."""
    s = 12.0 / max(outer_l, outer_b)
    X, Y = outer_l * s, outer_b * s
    w = width * s
    pts = [(0, 0), (w, 0), (X - w, 0), (X, 0), (X, w), (X, Y - w), (X, Y), (X - w, Y), (w, Y), (0, Y), (0, Y - w), (0, w)]
    edges = [None] * 12
    edges[0] = lwidth
    edges[1] = lmid_top
    edges[10] = lmid_left
    return P(pts, edges=edges, dashed=[(1, 8), (2, 7), (11, 4), (10, 5)], note=note, hl=hl)


def row_of_squares(k, top=None, left=None, note=None, hl=None):
    """k equal squares joined in one row, drawn as one outline with dashed joins (k at most 5).
    Edges e0..e(k-1) are the tops of the squares, left to right; e(2k+1) is the left side.
    `top` is one label for every top edge, or a list of k labels."""
    c = 12.0 / k
    pts = [(i * c, 0) for i in range(k + 1)] + [((k - i) * c, c) for i in range(k + 1)]
    edges = [None] * len(pts)
    tops = top if isinstance(top, list) else [top] * k
    for i in range(k):
        edges[i] = tops[i]
    edges[2 * k + 1] = left
    dashed = [(i, 2 * k + 1 - i) for i in range(1, k)]
    return P(pts, edges=edges, dashed=dashed, note=note, hl=hl)


# Fixed outlines for naming and property questions (0-12 grid, y down).
RECT_PTS = [(0, 0), (12, 0), (12, 7), (0, 7)]
SQUARE_PTS = [(0, 0), (8, 0), (8, 8), (0, 8)]
RHOMBUS_PTS = [(4.5, 0), (12, 0), (7.5, 6), (0, 6)]        # four sides of 7.5, leaning
DIAMOND_PTS = [(6, 0), (10, 6), (6, 12), (2, 6)]           # a rhombus standing on a corner
PARA_PTS = [(3, 0), (12, 0), (9, 5), (0, 5)]
TRAP_PTS = [(3, 0), (8, 0), (12, 5), (0, 5)]
KITE_PTS = [(6, 0), (9.5, 4), (6, 12), (2.5, 4)]
QUAD_PTS = [(2, 0), (10, 1), (12, 7), (0, 6)]


# ── The part file ────────────────────────────────────────────────────────────

def _variants(fig):
    """Every alternative of a figure, in order of preference."""
    if fig is None:
        return [None]
    if isinstance(fig, list):
        out = []
        for f in fig:
            out += _variants(f)
        return out
    notes = fig.get("note")
    if isinstance(notes, list):
        out = []
        for note in notes:
            f = dict(fig)
            if note:
                f["note"] = note
            else:
                del f["note"]
            out.append(f)
        return out
    return [fig]


class Part(object):
    def __init__(self, topic):
        self.topic = topic
        self.questions = [q for q in bank.load_bank(4) if q.get("node") == topic]
        self.by_id = {q["id"]: q for q in self.questions}
        self.entries = {}
        self.dropped = []
        self.path = os.path.join(PARTS, "g4-%s.json" % topic)

    def q(self, qid):
        return self.by_id[qid]

    def add(self, qid, figure=None, steps=None, origin="authored", essential=False, uses_options=False):
        if qid not in self.by_id:
            raise SystemExit("%s is not a question in %s" % (qid, self.topic))
        if qid in self.entries:
            raise SystemExit("%s defined twice" % qid)
        self.entries[qid] = {"figure": figure, "steps": steps or {}, "origin": origin,
                             "essential": essential, "uses_options": uses_options}

    def _pick(self, fig, allowed, where, free=False):
        for f in _variants(fig):
            if f is None:
                return None
            ctx = validate.check_figure(f, where)
            if ctx.errors:
                raise SystemExit("\n".join(ctx.errors))
            if free or not validate.ungrounded(ctx.numbers, allowed):
                return f
        self.dropped.append(where)
        return None

    def resolve(self, qid):
        e = self.entries[qid]
        q = self.by_id[qid]
        qn = validate.numbers_in(q.get("questionText", ""))
        on = set()
        for t in validate.option_texts(q):
            on |= validate.numbers_in(t)
        out = {"origin": e["origin"]}
        if e["figure"] is not None:
            allowed = qn | (on if e["uses_options"] else set())
            fig = self._pick(e["figure"], allowed, "%s.figure" % qid, free=e["essential"])
            if fig is not None:
                out["figure"] = fig
        own = q.get("stepByStep") or []
        steps = e["steps"]
        if isinstance(steps, list):
            steps = {i: f for i, f in enumerate(steps)}
        for i in steps:
            if i >= len(own):
                raise SystemExit("%s: step %d does not exist (the question has %d steps)" % (qid, i, len(own)))
        if steps and own:
            allowed = qn | on
            figs = []
            for i, s in enumerate(own):
                allowed = allowed | validate.numbers_in(s.get("text", ""))
                figs.append(self._pick(steps.get(i), allowed, "%s.stepFigures[%d]" % (qid, i)) if i in steps else None)
            if any(f is not None for f in figs):
                out["stepFigures"] = figs
        if e["essential"]:
            out["essential"] = True
        if e["uses_options"]:
            out["usesOptions"] = True
        if "figure" not in out and "stepFigures" not in out:
            return None
        return out

    def build(self):
        result = {}
        for q in self.questions:
            if q["id"] in self.entries:
                v = self.resolve(q["id"])
                if v is not None:
                    result[q["id"]] = v
        with io.open(self.path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
            f.write("\n")
        self.result = result
        return result

    def report(self):
        import collections
        r = self.result
        kinds = collections.Counter(v["figure"]["kind"] for v in r.values() if "figure" in v)
        print("%s: %d of %d questions have a visual; %d with a figure before answering, %d with step figures only" % (
            self.topic, len(r), len(self.questions), sum(1 for v in r.values() if "figure" in v),
            sum(1 for v in r.values() if "figure" not in v)))
        print("  before-answering figures by kind: " + ", ".join("%s %d" % kv for kv in kinds.most_common()))
        print("  by rule %d, individually drawn %d, essential %d" % (
            sum(1 for v in r.values() if v["origin"] == "rule"),
            sum(1 for v in r.values() if v["origin"] == "authored"),
            sum(1 for v in r.values() if v.get("essential"))))
        none = [q["id"] for q in self.questions if q["id"] not in r]
        print("  no visual (%d): %s" % (len(none), ", ".join(none)))
        if self.dropped:
            print("  alternatives all ungrounded, left out (%d): %s" % (len(self.dropped), ", ".join(self.dropped)))

    def show(self, ids=None):
        """Print question, figure and step figures side by side, for review."""
        for q in self.questions:
            qid = q["id"]
            if qid not in self.result or (ids and qid not in ids):
                continue
            v = self.result[qid]
            print("=" * 100)
            print("%s  [%s%s] ans=%s" % (qid, v["origin"], ", essential" if v.get("essential") else "", q["correctAnswer"]))
            print("Q: " + q["questionText"].replace("\n", " / "))
            print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
            print("FIGURE: " + (json.dumps(v["figure"], ensure_ascii=False) if "figure" in v else "-"))
            figs = v.get("stepFigures") or []
            for i, s in enumerate(q.get("stepByStep") or []):
                print("  S%d: %s   {%s}" % (i, s.get("text", ""), s.get("latex", "")))
                if i < len(figs) and figs[i] is not None:
                    print("      -> " + json.dumps(figs[i], ensure_ascii=False))
