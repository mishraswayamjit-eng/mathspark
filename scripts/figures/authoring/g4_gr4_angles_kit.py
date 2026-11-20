"""Shared pieces for the Grade 4 Angles and Triangles figures
(g4_gr4_angles.py and g4_gr4_triangles.py).

A Book holds one topic's questions and the figures written for them:

    book = Book("gr4_angles")
    book.add(qid, figure=..., steps={step index: figure}, origin="rule" | "authored")
    book.skip(qid, reason)
    book.finish()          # checks every entry, writes the part file, prints the summary

A figure (or a step's figure) may be a list of alternatives, and a figure's `note`
may be a list of candidate notes (None = no note). The Book keeps the first one whose
numbers have all been stated by that point (question text for the before-answering
figure; question, answer choices and the steps so far for a step figure), so a figure
never shows a number the child has not been given yet.

The figure constructors (A, T, P, CLOCK, COMPASS, BM, tri_sides, tri_angles) follow the
Grade 5 helpers in imported_geometry_lib.py, copied here so that file is not touched.
"""
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.join(ROOT, "scripts", "figures"))
import bank  # noqa: E402
import validate  # noqa: E402

PARTS = os.path.join(ROOT, "data", "question-figures", "parts")


def n(x):
    """A number as a child would write it: 12, 1.5, 60.75."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return ("%.4f" % x).rstrip("0").rstrip(".")


def deg(x):
    return "%s°" % n(x)


def cm(x):
    return "%s cm" % n(x)


# ── Constructors ─────────────────────────────────────────────────────────────

def _base(fig, note=None, hl=None):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def A(layout, parts, note=None, hl=None):
    """parts: (label,) or (label, size in degrees to draw)."""
    out = []
    for p in parts:
        d = {"label": p[0]}
        if len(p) > 1 and p[1]:
            d["size"] = p[1]
        out.append(d)
    return _base({"kind": "angles", "layout": layout, "parts": out}, note, hl)


def line(parts, note=None, hl=None):
    return A("onLine", parts, note, hl)


def corner(parts, note=None, hl=None):
    return A("inRightAngle", parts, note, hl)


def cross(parts, note=None, hl=None):
    return A("crossing", parts, note, hl)


def around(parts, note=None, hl=None):
    return A("aroundPoint", parts, note, hl)


def single(label, size, note=None, hl=None):
    return A("single", [(label, size)], note, hl)


def unknown(left, label="?"):
    """The unknown part of a straight line or right angle. The renderer shares out what
    is left, but not when less than 8° is left: then the true size is given so the
    drawing stays honest (the size is never shown as a number)."""
    return (label, left) if left < 8 else (label,)


def T(shape, sides=None, angles=None, height=None, enclose=False, note=None, hl=None):
    fig = {"kind": "triangle", "shape": shape}
    if sides:
        s = {k: v for k, v in sides.items() if v}
        if s:
            fig["sides"] = s
    if angles:
        a = {k: v for k, v in angles.items() if v}
        if a:
            fig["angles"] = a
    if height:
        fig["height"] = height
    if enclose:
        fig["enclose"] = True
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


def R(length=None, breadth=None, inside=None, square=False, note=None, hl=None):
    fig = {"kind": "rectangle"}
    if square:
        fig["square"] = True
    if length:
        fig["length"] = length
    if breadth:
        fig["breadth"] = breadth
    if inside:
        fig["inside"] = inside
    return _base(fig, note, hl)


def CLOCK(hour, minute=0, angle=False, note=None, hl=None):
    fig = {"kind": "clock", "hour": hour, "minute": minute}
    if angle:
        fig["showAngle"] = True
    return _base(fig, note, hl)


def COMPASS(facing, turns=None, end=False, note=None, hl=None):
    fig = {"kind": "compass", "facing": facing}
    if turns:
        fig["turns"] = [{"degrees": d, "direction": way} for d, way in turns]
    if end:
        fig["showEnd"] = True
    return _base(fig, note, hl)


CW = "clockwise"
ACW = "anticlockwise"


def BM(bars, note=None, hl=None):
    """bars: each a list of segments, or (label, segments) or (label, segments, brace).
    A segment is (units, label[, tone])."""
    out = []
    for bar in bars:
        label = brace = None
        segs = bar
        if isinstance(bar, tuple):
            label, segs = bar[0], bar[1]
            brace = bar[2] if len(bar) > 2 else None
        ss = []
        for s in segs:
            d = {"units": s[0]}
            if len(s) > 1 and s[1]:
                d["label"] = s[1]
            if len(s) > 2 and s[2]:
                d["tone"] = s[2]
            ss.append(d)
        b = {"segments": ss}
        if label:
            b["label"] = label
        if brace:
            b["brace"] = brace
        out.append(b)
    return _base({"kind": "barModel", "bars": out}, note, hl)


def NL(lo, hi, step, points=None, labels=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if labels:
        fig["tickLabels"] = labels
    if points:
        fig["points"] = [({"at": p[0], "label": p[1]} if len(p) > 1 and p[1] else {"at": p[0]}) for p in points]
    return _base(fig, note, hl)


# ── Shapes drawn true to the question's numbers ──────────────────────────────

def _fit(pts, size=10.0):
    """Move a shape into the 0-12 grid, y running down, biggest side `size`."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    s = size / max(w, h)
    return [((x - min(xs)) * s, (max(ys) - y) * s) for x, y in pts]


def _tri_points(base, left, right):
    """Corners A (top), B (bottom left), C (bottom right): BC = base, AB = left, CA = right."""
    x = (left * left + base * base - right * right) / (2.0 * base)
    h2 = left * left - x * x
    if h2 <= 1e-9:
        raise SystemExit("sides %s, %s, %s do not make a triangle" % (base, left, right))
    return _fit([(x, math.sqrt(h2)), (0.0, 0.0), (base, 0.0)])


TRI_KEYS = {"a": None, "b": None, "c": None, "ab": "e0", "bc": "e1", "ca": "e2", "fill": "fill"}


def tri_sides(base, left, right, lbase=None, lleft=None, lright=None, note=None, hl=None):
    """A triangle drawn to its true shape from its three sides.
    `hl` uses the triangle's keys: ab (left side), bc (base), ca (right side)."""
    phl = [TRI_KEYS[k] for k in (hl or []) if TRI_KEYS.get(k)]
    return P(_tri_points(base, left, right), edges=[lleft, lbase, lright], note=note, hl=phl)


# How the renderer draws each fixed triangle, as (A, B, C) in degrees.
_DRAWN = {"scalene": (70.7, 46.8, 62.5), "isosceles": (45.8, 67.1, 67.1), "right": (47.6, 90.0, 42.4),
          "equilateral": (60.0, 60.0, 60.0)}


def tri_angles(a, b, c, la=None, lb=None, lc=None, sides=None, note=None, hl=None, tol=8.0):
    """A triangle with angle a at the top, b bottom left, c bottom right (the true sizes).

    Uses the renderer's own triangle (angle labels inside the corners) when its drawn
    shape is within `tol` degrees of the true one at every corner; otherwise draws the
    true shape as a polygon with the angles written at the corners.
    `sides` are labels keyed ab / bc / ca. `hl` uses the triangle's keys."""
    if abs(a + b + c - 180) > 0.01:
        raise SystemExit("angles %s, %s, %s do not add up to 180" % (a, b, c))
    sides = sides or {}
    shape = None
    for name in ("equilateral", "right", "isosceles", "scalene"):
        if name == "equilateral" and not (abs(a - 60) < 0.01 and abs(b - 60) < 0.01):
            continue
        if name == "right" and abs(b - 90) > 0.01:
            continue
        if name == "isosceles" and abs(b - c) > 0.01:
            continue
        ref = _DRAWN[name]
        if max(abs(a - ref[0]), abs(b - ref[1]), abs(c - ref[2])) <= tol:
            shape = name
            break
    if shape:
        return T(shape, sides=sides, angles={"a": la, "b": lb, "c": lc}, note=note, hl=hl)
    ra, rb, rc = (math.radians(v) for v in (a, b, c))
    pts = _tri_points(math.sin(ra), math.sin(rc), math.sin(rb))
    phl = [TRI_KEYS[k] for k in (hl or []) if TRI_KEYS.get(k)]
    return P(pts, edges=[sides.get("ab"), sides.get("bc"), sides.get("ca")], corners=[la, lb, lc],
             right=[1] if abs(b - 90) < 0.01 else None, note=note, hl=phl)


def right_tri(base, height, lbase=None, lheight=None, lhyp=None, note=None, hl=None):
    """A right-angled triangle drawn to its true shape: upright side on the left, base
    along the bottom, right angle marked at the bottom left.
    `hl` uses the triangle's keys: ab (upright), bc (base), ca (slanted side)."""
    s = 10.0 / max(base, height)
    pts = [(0, 0), (0, height * s), (base * s, height * s)]
    phl = [TRI_KEYS[k] for k in (hl or []) if TRI_KEYS.get(k)]
    return P(pts, edges=[lheight, lbase, lhyp], right=[1], note=note, hl=phl)


def rect_diag(base, height, lbase=None, lheight=None, note=None, hl=None):
    """The rectangle around a right-angled triangle, with the triangle's slanted side
    as a dashed diagonal. Edge e2 is the base (bottom), e3 the upright (left)."""
    s = 10.0 / max(base, height)
    pts = [(0, 0), (base * s, 0), (base * s, height * s), (0, height * s)]
    return P(pts, edges=[None, None, lbase, lheight], dashed=[(0, 2)], note=note, hl=hl)


# ── The book ─────────────────────────────────────────────────────────────────

def _expand(fig):
    """All concrete alternatives of a figure spec, in order of preference."""
    if fig is None:
        return [None]
    if isinstance(fig, (list, tuple)):
        out = []
        for f in fig:
            out += _expand(f)
        return out
    if isinstance(fig.get("note"), (list, tuple)):
        out = []
        for note in fig["note"]:
            d = {k: v for k, v in fig.items() if k != "note"}
            if note:
                d["note"] = note
            out.append(d)
        return out
    return [fig]


class Book(object):
    def __init__(self, node):
        self.node = node
        self.questions = {q["id"]: q for q in bank.load_bank(4) if q.get("node") == node}
        self.entries = {}
        self.skips = {}

    def q(self, qid):
        return self.questions[qid]

    def answer(self, qid):
        return validate.correct_text(self.questions[qid])

    def answer_number(self, qid):
        nums = sorted(validate.numbers_in(self.answer(qid)))
        return nums[0] if len(nums) == 1 else None

    def _pick(self, spec, allowed, where):
        cands = _expand(spec)
        first = None
        for cand in cands:
            if cand is None:
                return None
            ctx = validate.check_figure(cand, where)
            if ctx.errors:
                raise SystemExit("\n".join(ctx.errors))
            extra = validate.ungrounded(ctx.numbers, allowed)
            if not extra:
                return cand
            if first is None:
                first = extra
        raise SystemExit("%s: no alternative is grounded (first shows %s)" % (where, validate.fmt(first)))

    def add(self, qid, figure=None, steps=None, origin="authored", uses_options=False):
        if qid not in self.questions:
            raise SystemExit("%s is not a question of %s" % (qid, self.node))
        if qid in self.entries or qid in self.skips:
            raise SystemExit("%s defined twice" % qid)
        q = self.questions[qid]
        qnums = validate.numbers_in(q.get("questionText", ""))
        onums = set()
        for t in validate.option_texts(q):
            onums |= validate.numbers_in(t)
        entry = {"origin": origin}
        if figure is not None:
            fig = self._pick(figure, qnums | (onums if uses_options else set()), "%s.figure" % qid)
            if fig is not None:
                entry["figure"] = fig
                if uses_options:
                    entry["usesOptions"] = True
        own = q.get("stepByStep") or []
        if steps:
            for i in steps:
                if not (0 <= i < len(own)):
                    raise SystemExit("%s: step %d does not exist (the question has %d steps)" % (qid, i, len(own)))
            allowed = qnums | onums
            figs = []
            for i, s in enumerate(own):
                allowed = allowed | validate.numbers_in(s.get("text", ""))
                figs.append(self._pick(steps[i], allowed, "%s.stepFigures[%d]" % (qid, i)) if i in steps else None)
            if any(f is not None for f in figs):
                entry["stepFigures"] = figs
        if "figure" not in entry and "stepFigures" not in entry:
            raise SystemExit("%s: nothing to draw" % qid)
        problems = validate.check_entry(qid, entry, q)
        if problems:
            raise SystemExit("\n".join(problems))
        self.entries[qid] = entry

    def skip(self, qid, reason):
        if qid not in self.questions:
            raise SystemExit("%s is not a question of %s" % (qid, self.node))
        if qid in self.entries or qid in self.skips:
            raise SystemExit("%s defined twice" % qid)
        self.skips[qid] = reason

    # ── Output ──

    def path(self):
        return os.path.join(PARTS, "g4-%s.json" % self.node)

    def write(self):
        ids = sorted(self.entries)
        with io.open(self.path(), "w", encoding="utf-8", newline="\n") as f:
            f.write("{\n")
            for k, qid in enumerate(ids):
                f.write("  %s: %s%s\n" % (json.dumps(qid), json.dumps(self.entries[qid], ensure_ascii=False),
                                         "," if k < len(ids) - 1 else ""))
            f.write("}\n")

    def summary(self):
        import collections
        total = len(self.questions)
        kinds = collections.Counter()
        steps_only = 0
        for e in self.entries.values():
            if "figure" in e:
                kinds[e["figure"]["kind"]] += 1
            else:
                steps_only += 1
        rule = sum(1 for e in self.entries.values() if e["origin"] == "rule")
        print("%s: %d of %d questions have a visual (%d with a figure before answering, %d with step figures only)" % (
            self.node, len(self.entries), total, len(self.entries) - steps_only, steps_only))
        print("  before-answering figure by kind: " + ", ".join("%s %d" % kv for kv in kinds.most_common()))
        print("  by rule %d, individually drawn %d, essential %d" % (
            rule, len(self.entries) - rule, sum(1 for e in self.entries.values() if e.get("essential"))))
        print("  left without a picture on purpose: %d" % len(self.skips))
        undecided = sorted(set(self.questions) - set(self.entries) - set(self.skips))
        if undecided:
            print("  NOT YET DECIDED (%d): %s" % (len(undecided), ", ".join(undecided)))

    def review(self, a=0, b=None, only=None):
        """Print question, figure and step figures side by side."""
        ids = sorted(self.entries)
        if only:
            ids = [i for i in ids if only in i]
        for qid in ids[a:b]:
            q = self.questions[qid]
            e = self.entries[qid]
            print("## %s [%s] ans=%s (%s)" % (qid, e["origin"], q["correctAnswer"], self.answer(qid)))
            print("Q: " + q["questionText"].replace("\n", " / "))
            print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
            print("FIG: " + (json.dumps(e["figure"], ensure_ascii=False) if "figure" in e else "(none)"))
            figs = e.get("stepFigures") or []
            for i, s in enumerate(q.get("stepByStep") or []):
                print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
                if i < len(figs) and figs[i] is not None:
                    print("      -> " + json.dumps(figs[i], ensure_ascii=False))

    def finish(self, argv):
        self.write()
        if len(argv) > 1 and argv[1] == "review":
            a = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 0
            b = int(argv[3]) if len(argv) > 3 and argv[3].isdigit() else None
            only = argv[2] if len(argv) > 2 and not argv[2].isdigit() else None
            self.review(a, b, only)
        elif len(argv) > 1 and argv[1] == "skips":
            for qid in sorted(self.skips):
                print("%s: %s" % (qid, self.skips[qid]))
        self.summary()
        print("wrote %s" % os.path.relpath(self.path(), ROOT))
