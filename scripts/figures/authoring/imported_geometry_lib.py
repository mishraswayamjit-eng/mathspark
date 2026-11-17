"""Shared pieces for the imported Grade 5 geometry figures (imported_geometry*.py).

Figure constructors, the shapes that repeat across questions, and the registry
the batch modules fill:

    add(key, figure=..., steps={step index: figure}, origin="rule" | "authored")
    skip(key, category, reason)

`key` is the short form of a question id: the first 8 characters of the uuid
for AIGEN_grade5_<uuid>, or "ch19_q004" for IPMTB_grade5_ch19_q004.

A figure's `note` may be a list of candidates, and a step may be a list of
alternative figures. The build keeps the first one whose numbers have all been
stated by that point (question, answer choices, steps so far), so a figure never
shows a number the child has not been given yet.
"""
import math

ENTRIES = {}
SKIPS = {}


def add(key, figure=None, steps=None, origin="rule", uses_options=False):
    if key in ENTRIES or key in SKIPS:
        raise SystemExit("%s defined twice" % key)
    ENTRIES[key] = {"figure": figure, "steps": steps or {}, "origin": origin, "uses_options": uses_options}


def skip(key, category, reason):
    """category: 'contradiction' (the question's own data disagree) or 'no-picture'."""
    if key in ENTRIES or key in SKIPS:
        raise SystemExit("%s defined twice" % key)
    SKIPS[key] = (category, reason)


def n(x):
    """A number as a child would write it: 12, 1.5, 60.75."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return ("%.4f" % x).rstrip("0").rstrip(".")


def _base(fig, note=None, hl=None):
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


# ── Constructors ─────────────────────────────────────────────────────────────

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


def T(shape, sides=None, angles=None, height=None, enclose=False, note=None, hl=None):
    fig = {"kind": "triangle", "shape": shape}
    if sides:
        fig["sides"] = {k: v for k, v in sides.items() if v}
    if angles:
        fig["angles"] = {k: v for k, v in angles.items() if v}
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


def A(layout, parts, note=None, hl=None):
    """parts: (label,) or (label, size in degrees to draw)."""
    out = []
    for p in parts:
        d = {"label": p[0]}
        if len(p) > 1 and p[1]:
            d["size"] = p[1]
        out.append(d)
    return _base({"kind": "angles", "layout": layout, "parts": out}, note, hl)


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


def BM(bars, note=None, hl=None):
    """bars: list of bars, each a list of (units, label[, tone])."""
    out = []
    for segs in bars:
        ss = []
        for s in segs:
            d = {"units": s[0]}
            if len(s) > 1 and s[1]:
                d["label"] = s[1]
            if len(s) > 2 and s[2]:
                d["tone"] = s[2]
            ss.append(d)
        out.append({"segments": ss})
    return _base({"kind": "barModel", "bars": out}, note, hl)


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


def tri_sides(base, left, right, lbase=None, lleft=None, lright=None, corners=None, right_at_b=False, note=None, hl=None):
    """A triangle drawn to its true shape from its three sides.
    Polygon corners run A, B, C, so edge e0 is AB (left), e1 is BC (base), e2 is CA (right)."""
    if right_at_b and abs(left * left + base * base - right * right) > 1e-6:
        raise SystemExit("%s, %s, %s has no right angle between the first two" % (base, left, right))
    return P(_tri_points(base, left, right), edges=[lleft, lbase, lright], corners=corners,
             right=[1] if right_at_b else None, note=note, hl=hl)


# How the renderer draws each fixed triangle, as (A, B, C) in degrees.
_DRAWN = {"scalene": (70.7, 46.8, 62.5), "isosceles": (45.8, 67.1, 67.1), "right": (47.6, 90.0, 42.4)}


def tri_angles(a, b, c, la=None, lb=None, lc=None, sides=None, note=None, hl=None, poly=False, tol=12.0):
    """A triangle with angle a at the top, b bottom left, c bottom right (degrees, the true sizes).

    Uses the renderer's own triangle (angle labels inside the corners) when its
    drawn shape is within `tol` degrees of the true one at every corner; otherwise
    draws the true shape as a polygon with the angles written at the corners.
    `sides` are labels keyed ab / bc / ca. `hl` uses the triangle's keys (a, b, c, ab, bc, ca).
    """
    if abs(a + b + c - 180) > 0.01:
        raise SystemExit("angles %s, %s, %s do not add up to 180" % (a, b, c))
    sides = sides or {}
    shape = None
    if not poly:
        for name in ("right", "isosceles", "scalene"):
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
    keys = {"a": None, "b": None, "c": None, "ab": "e0", "bc": "e1", "ca": "e2", "fill": "fill"}
    phl = [keys[k] for k in (hl or []) if keys.get(k)]
    return P(pts, edges=[sides.get("ab"), sides.get("bc"), sides.get("ca")], corners=[la, lb, lc],
             right=[1] if abs(b - 90) < 0.01 else None, note=note, hl=phl)


def hexagon(edges=None, note=None, hl=None):
    """A regular hexagon. Edges run clockwise from the top side."""
    h = 5 * math.sqrt(3) / 2
    pts = [(3.5, 6 - h), (8.5, 6 - h), (11, 6), (8.5, 6 + h), (3.5, 6 + h), (1, 6)]
    return P(pts, edges=edges, note=note, hl=hl)


def l_shape(length, breadth, cut_l, cut_b, llength, lbreadth, lcut, note=None, hl=None):
    """A rectangle with a rectangular piece taken out of its top right corner.
    The cut-out's size is written in the empty corner; the outer sides along the bottom and left."""
    s = 12.0 / max(length, breadth)
    L, B, cl, cb = length * s, breadth * s, cut_l * s, cut_b * s
    pts = [(0, 0), (L - cl, 0), (L - cl, cb), (L, cb), (L, B), (0, B)]
    return P(pts, edges=[None, None, None, None, llength, lbreadth], corners=[None, None, lcut, None, None, None], note=note, hl=hl)


def strip_frame(outer_l, outer_b, width, lwidth=None, lmid_top=None, lmid_left=None, note=None, hl=None):
    """A rectangle with a strip of the same width along all four sides (a path or border),
    marked off by four dashed lines. Edge e0 is the strip's width at the top left corner,
    e1 the middle of the top side, e10 the middle of the left side."""
    s = 12.0 / max(outer_l, outer_b)
    X, Y = outer_l * s, outer_b * s
    w = max(width * s, 1.0)          # keep a narrow strip wide enough to see
    pts = [(0, 0), (w, 0), (X - w, 0), (X, 0), (X, w), (X, Y - w), (X, Y), (X - w, Y), (w, Y), (0, Y), (0, Y - w), (0, w)]
    edges = [None] * 12
    edges[0] = lwidth
    edges[1] = lmid_top
    edges[10] = lmid_left
    return P(pts, edges=edges, dashed=[(1, 8), (2, 7), (11, 4), (10, 5)], note=note, hl=hl)
