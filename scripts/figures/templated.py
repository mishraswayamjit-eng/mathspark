"""Figures and computed solutions for the templated Grade 5 questions.

    python -X utf8 scripts/figures/templated.py

Reads data/mathspark_complete_seed.json and writes
data/question-figures/parts/templated.json  ({ "<question id>": QuestionVisual }, origin "rule").

Everything here is computed from the question's own text by regex and
arithmetic: one rule per question template. No AI, no hand-written entries.

A rule is conservative:
  - the question text must match its template exactly (re.fullmatch);
  - the answer the rule computes must equal the answer key, otherwise the
    question is skipped and counted;
  - every entry is run through validate.check_entry before it is kept.

Questions that already have steps get `stepFigures` (one per existing step).
Questions with no steps (source auto_generated_v2) get computed `steps`.
"""
import collections
import io
import json
import math
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate  # noqa: E402  (the checker next to this file)

ROOT = validate.ROOT
SEED = validate.SEED
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "templated.json")


class Skip(Exception):
    """The question matched a template but the rule will not answer for it."""


RULES = []


def rule(name):
    def wrap(fn):
        RULES.append((name, fn))
        return fn
    return wrap


# ── Helpers ──────────────────────────────────────────────────────────────────

def n(x):
    """A number as a child would write it: 12, 31.5 (never 12.0)."""
    if isinstance(x, Fraction):
        x = int(x) if x.denominator == 1 else float(x)
    if isinstance(x, float) and x == int(x):
        x = int(x)
    if isinstance(x, int):
        return str(x)
    return ("%.4f" % x).rstrip("0").rstrip(".")


def key_text(q):
    return validate.correct_text(q).strip()


def need(q, value):
    """Skip unless the answer key is exactly this number."""
    if validate.numbers_in(key_text(q)) != {float(value)}:
        raise Skip("computed answer differs from the key")


def need_text(q, *texts):
    """Skip unless the answer key is one of these strings (spaces ignored)."""
    got = key_text(q).replace(" ", "")
    if got not in [t.replace(" ", "") for t in texts]:
        raise Skip("computed answer differs from the key")


def own_steps(q, count=None):
    steps = q.get("stepByStep") or []
    if count is not None and len(steps) != count:
        raise Skip("unexpected number of steps")
    return steps


def grounded(q, upto, *values):
    """True when every value is stated in the question, the choices, or the steps up to index `upto`."""
    allowed = validate.numbers_in(q.get("questionText", ""))
    for t in validate.option_texts(q):
        allowed |= validate.numbers_in(t)
    for s in (q.get("stepByStep") or [])[:upto + 1]:
        allowed |= validate.numbers_in(s.get("text", ""))
    allowed |= validate.CONSTANTS
    return all(float(v) in allowed for v in values)


def proportion(length, breadth):
    return round(max(1.0, min(3.0, float(length) / float(breadth))), 2)


def rect_base(l, b):
    """A rectangle drawn with its longer side across the top, whichever the question calls the length.

    Returns (figure fields, squares across, squares down).
    """
    across, down = max(l, b), min(l, b)
    return ({"kind": "rectangle", "length": "%s cm" % n(across), "breadth": "%s cm" % n(down),
             "proportion": proportion(across, down)}, across, down)


def scale_units(values, top=10.0):
    """Bar-piece widths in honest proportion, the largest drawn `top` wide."""
    biggest = float(max(values))
    return [round(max(0.2, top * float(v) / biggest), 2) for v in values]


M = re.fullmatch
NUM = r"(\d+(?:\.\d+)?)"


def num(s):
    f = float(s)
    return int(f) if f == int(f) else f


# ── Family: area and perimeter (no steps in the bank: computed steps) ────────

@rule("geometry: area of a triangle")
def g_tri_area(q):
    m = M(r"Find the area of a triangle with base %s cm and height %s cm\." % (NUM, NUM), q["questionText"].strip())
    if not m or own_steps(q):
        return None
    b, h = num(m.group(1)), num(m.group(2))
    prod, area = b * h, Fraction(b * h, 2) if isinstance(b * h, int) else b * h / 2
    need(q, float(area))
    base = {"kind": "triangle", "shape": "scalene", "sides": {"bc": "%s cm" % n(b)}, "height": "%s cm" % n(h)}
    return {
        "figure": dict(base, note="Area = ?"),
        "steps": [
            {"text": "A triangle is half of the rectangle drawn around it. So the area of a triangle is half of base × height.",
             "figure": dict(base, enclose=True, highlight=["bc", "height"], note="Half of the rectangle around it")},
            {"text": "First multiply the base by the height: %s × %s = %s." % (n(b), n(h), n(prod)),
             "figure": dict(base, enclose=True, note="%s × %s = %s for the whole rectangle" % (n(b), n(h), n(prod)))},
            {"text": "Now take half: %s ÷ 2 = %s. The area of the triangle is %s sq. cm." % (n(prod), n(area), n(area)),
             "figure": dict(base, enclose=True, highlight=["fill"], note="½ × %s × %s = %s sq. cm" % (n(b), n(h), n(area)))},
        ],
    }


@rule("geometry: perimeter of a rectangle")
def g_rect_perimeter(q):
    m = M(r"Find the perimeter of a rectangle with length %s cm and breadth %s cm\." % (NUM, NUM), q["questionText"].strip())
    if not m or own_steps(q):
        return None
    l, b = num(m.group(1)), num(m.group(2))
    need(q, 2 * (l + b))
    base, across, down = rect_base(l, b)
    return {
        "figure": dict(base, note="Perimeter = ?"),
        "steps": [
            {"text": "The perimeter is the distance all the way round the edge. A rectangle has 2 lengths and 2 breadths.",
             "figure": dict(base, highlight=["border"], note="Walk all the way round the edge")},
            {"text": "Add one length and one breadth: %s + %s = %s cm. That is halfway round." % (n(l), n(b), n(l + b)),
             "figure": dict(base, highlight=["length", "breadth"], note="%s + %s = %s cm" % (n(l), n(b), n(l + b)))},
            {"text": "Double it to go all the way round: 2 × %s = %s cm. The perimeter is %s cm." % (n(l + b), n(2 * (l + b)), n(2 * (l + b))),
             "figure": dict(base, highlight=["border"], note="2 × %s = %s cm" % (n(l + b), n(2 * (l + b))))},
        ],
    }


@rule("geometry: area of a rectangle")
def g_rect_area(q):
    m = M(r"Find the area of a rectangle with length %s cm and breadth %s cm\." % (NUM, NUM), q["questionText"].strip())
    if not m or own_steps(q):
        return None
    l, b = num(m.group(1)), num(m.group(2))
    need(q, l * b)
    base, across, down = rect_base(l, b)
    squares = dict(base)
    if isinstance(l, int) and isinstance(b, int) and across <= 12:
        squares["grid"] = {"cols": across, "rows": down}
    return {
        "figure": dict(base, inside="Area = ?"),
        "steps": [
            {"text": "Area is the space inside the shape, counted in unit squares. There are %s squares in each row and %s rows, so area = length × breadth." % (n(across), n(down)),
             "figure": dict(squares, highlight=["length", "breadth"])},
            {"text": "Multiply: %s × %s = %s. The area of the rectangle is %s sq. cm." % (n(l), n(b), n(l * b), n(l * b)),
             "figure": dict(squares, highlight=["fill"], note="%s × %s = %s sq. cm" % (n(l), n(b), n(l * b)))},
        ],
    }


@rule("geometry: perimeter of a square")
def g_square_perimeter(q):
    m = M(r"Find the perimeter of a square with side %s cm\." % NUM, q["questionText"].strip())
    if not m or own_steps(q):
        return None
    s = num(m.group(1))
    need(q, 4 * s)
    base = {"kind": "rectangle", "square": True, "length": "%s cm" % n(s)}
    return {
        "figure": dict(base, note="Perimeter = ?"),
        "steps": [
            {"text": "The perimeter is the distance all the way round the edge. A square has 4 sides, and they are all the same length.",
             "figure": dict(base, highlight=["border"], note="4 equal sides")},
            {"text": "So multiply the side by 4: 4 × %s = %s cm. The perimeter is %s cm." % (n(s), n(4 * s), n(4 * s)),
             "figure": dict(base, highlight=["border"], note="4 × %s = %s cm" % (n(s), n(4 * s)))},
        ],
    }


@rule("geometry: area of a square")
def g_square_area(q):
    m = M(r"Find the area of a square with side %s cm\." % NUM, q["questionText"].strip())
    if not m or own_steps(q):
        return None
    s = num(m.group(1))
    need(q, s * s)
    base = {"kind": "rectangle", "square": True, "length": "%s cm" % n(s)}
    squares = dict(base)
    if isinstance(s, int) and s <= 12:
        squares["grid"] = {"cols": s, "rows": s}
    return {
        "figure": dict(base, inside="Area = ?"),
        "steps": [
            {"text": "Area is the space inside the shape. In a square the length and the breadth are the same, so area = side × side.",
             "figure": dict(squares, highlight=["length"])},
            {"text": "Multiply: %s × %s = %s. The area of the square is %s sq. cm." % (n(s), n(s), n(s * s), n(s * s)),
             "figure": dict(squares, highlight=["fill"], note="%s × %s = %s sq. cm" % (n(s), n(s), n(s * s)))},
        ],
    }


# ── Family: angles (computed steps) ──────────────────────────────────────────

@rule("angles: supplementary / complementary")
def a_pair(q):
    m = M(r"Find the (supplementary|complementary) angle of %s°\." % NUM, q["questionText"].strip())
    if not m or own_steps(q):
        return None
    word, a = m.group(1), num(m.group(2))
    whole = 180 if word == "supplementary" else 90
    if not 0 < a < whole:
        raise Skip("angle out of range")
    other = whole - a
    need(q, other)
    layout = "onLine" if whole == 180 else "inRightAngle"
    shape = "a straight line" if whole == 180 else "a right angle"
    before = {"kind": "angles", "layout": layout, "parts": [{"label": "%s°" % n(a), "size": a}, {"label": "?"}]}
    after = {"kind": "angles", "layout": layout, "highlight": ["p1"],
             "parts": [{"label": "%s°" % n(a), "size": a}, {"label": "%s°" % n(other), "size": other}],
             "note": "%s° − %s° = %s°" % (whole, n(a), n(other))}
    return {
        "figure": before,
        "steps": [
            {"text": "%s angles fit together to make %s. So the two angles add up to %s°." % (word.capitalize(), shape, whole),
             "figure": dict(before, note="The two angles together make %s°" % whole)},
            {"text": "Take away the angle you know: %s° − %s° = %s°. The %s angle is %s°." % (whole, n(a), n(other), word, n(other)),
             "figure": after},
        ],
    }


# ── Family: one-unknown equations (computed steps) ───────────────────────────

@rule("equation: ax + b = c (no steps)")
def e_linear(q):
    m = M(r"Find the value of x: (\d+)x \+ (\d+) = (\d+)", q["questionText"].strip())
    if not m or own_steps(q):
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if a < 2 or c <= b or (c - b) % a:
        raise Skip("does not divide exactly")
    x = (c - b) // a
    need(q, x)
    return {
        "figure": {"kind": "balance", "left": "%dx + %d" % (a, b), "right": str(c)},
        "steps": [
            {"text": "Think of a balance: %dx + %d on one side and %d on the other. It stays level as long as you do the same thing to both sides." % (a, b, c),
             "figure": {"kind": "balance", "left": "%dx + %d" % (a, b), "right": str(c), "note": "Both sides weigh the same"}},
            {"text": "Take %d away from both sides: %d − %d = %d. Now %dx = %d." % (b, c, b, c - b, a, c - b),
             "figure": {"kind": "balance", "left": "%dx" % a, "right": str(c - b), "highlight": ["right"], "note": "Take %d off both sides" % b}},
            {"text": "%dx means %d times x. Divide both sides by %d: %d ÷ %d = %d. So x = %d." % (a, a, a, c - b, a, x, x),
             "figure": {"kind": "balance", "left": "x", "right": str(x), "highlight": ["left", "right"], "note": "Check: %d × %d + %d = %d" % (a, x, b, c)}},
        ],
    }


# ── Family: order of operations (computed steps, no picture) ─────────────────

@rule("bodmas: a + b × c − d (no steps)")
def b_plus_times_minus(q):
    m = M(r"Simplify: (\d+) \+ (\d+) × (\d+) − (\d+)", q["questionText"].strip())
    if not m or own_steps(q):
        return None
    a, b, c, d = [int(g) for g in m.groups()]
    ans = a + b * c - d
    need(q, ans)
    return {
        "steps": [
            {"text": "Multiplying comes before adding and taking away. So work out %d × %d first: %d × %d = %d." % (b, c, b, c, b * c)},
            {"text": "Now the sum reads %d + %d − %d. Work from left to right: %d + %d = %d." % (a, b * c, d, a, b * c, a + b * c)},
            {"text": "Last, %d − %d = %d. The answer is %d." % (a + b * c, d, ans, ans)},
        ],
    }


# ── Family: simple interest (computed steps) ─────────────────────────────────

@rule("simple interest: interest / amount")
def si(q):
    text = q["questionText"].strip()
    m = M(r"Find the simple interest on Rs\.(\d+) at (\d+)% per annum for (\d+) years\.", text)
    want_amount = False
    if not m:
        m = M(r"Rs\.(\d+) is invested at (\d+)% simple interest\. What is the amount after (\d+) years\?", text)
        want_amount = True
    if not m or own_steps(q):
        return None
    p, r, t = [int(g) for g in m.groups()]
    if (p * r) % 100 or t < 2:
        raise Skip("yearly interest is not a whole number of rupees")
    yearly = p * r // 100
    interest = yearly * t
    need(q, p + interest if want_amount else interest)
    steps = [
        {"text": "Simple interest adds the same amount every year. %d%% means %d out of every 100, so one year's interest is %d × %d ÷ 100 = Rs.%d." % (r, r, p, r, yearly)},
        {"text": "There are %d years, so the interest is %d × %d = Rs.%d%s" % (
            t, yearly, t, interest, "." if want_amount else ". The simple interest is Rs.%d." % interest)},
    ]
    entry = {"steps": steps}
    if want_amount:
        steps.append({"text": "The amount is the money put in plus the interest: %d + %d = Rs.%d. The amount is Rs.%d." % (p, interest, p + interest, p + interest)})
        entry["figure"] = {"kind": "barModel", "note": "%d%% interest each year for %d years" % (r, t), "bars": [
            {"brace": "Amount = ?", "segments": [{"units": 2, "label": "Rs.%d" % p, "tone": "a"}, {"units": 2, "label": "interest ?", "tone": "unknown"}]}]}
        if t <= 8:
            widths = scale_units([p] + [yearly] * t)
            years = [{"units": w, "label": "Rs.%d" % yearly, "tone": "b"} for w in widths[1:]]
            first = {"units": widths[0], "label": "Rs.%d" % p, "tone": "a"}
            steps[0]["figure"] = {"kind": "barModel", "highlight": ["b0s1"], "note": "One year's interest is Rs.%d" % yearly, "bars": [
                {"segments": [first, years[0]]}]}
            steps[1]["figure"] = {"kind": "barModel", "note": "%d years of interest: Rs.%d" % (t, interest), "bars": [
                {"segments": [first] + years}]}
            steps[2]["figure"] = {"kind": "barModel", "note": "%d + %d = Rs.%d" % (p, interest, p + interest), "bars": [
                {"brace": "Rs.%d" % (p + interest), "segments": [first] + years}]}
    elif t <= 12:
        entry["figure"] = {"kind": "barModel", "note": "Each piece is %d%% of Rs.%d, one per year" % (r, p), "bars": [
            {"brace": "Interest = ?", "segments": [{"units": 1, "label": "?", "tone": "unknown"} for _ in range(t)]}]}
        steps[0]["figure"] = {"kind": "barModel", "highlight": ["b0s0"], "note": "One year's interest is Rs.%d" % yearly, "bars": [
            {"segments": [{"units": 1, "label": "Rs.%d" % yearly, "tone": "a"}] + [{"units": 1, "label": "?", "tone": "unknown"} for _ in range(t - 1)]}]}
        steps[1]["figure"] = {"kind": "barModel", "note": "%d × %d = Rs.%d" % (yearly, t, interest), "bars": [
            {"brace": "Rs.%d" % interest, "segments": [{"units": 1, "label": "Rs.%d" % yearly, "tone": "a"} for _ in range(t)]}]}
    return entry


# ── Family: percentage of a quantity (computed steps) ────────────────────────

@rule("percentage of a quantity")
def pct(q):
    text = q["questionText"].strip()
    m = M(r"Out of (\d+) students, (\d+)% are girls\. How many girls are there\?", text)
    if m:
        total, p, whole, part, close = int(m.group(1)), int(m.group(2)), "%s students", "girls", "There are %s girls."
    else:
        m = M(r"A test has (\d+) marks\. A student scored (\d+)%\. How many marks did the student score\?", text)
        if m:
            total, p, whole, part, close = int(m.group(1)), int(m.group(2)), "%s marks", "scored", "The student scored %s marks."
        else:
            m = M(r"What is (\d+)% of (\d+)\?", text)
            if not m:
                return None
            p, total, whole, part, close = int(m.group(1)), int(m.group(2)), "%s", None, "The answer is %s."
    if own_steps(q):
        return None
    if (total * p) % 100 or not 0 < p < 100:
        raise Skip("percentage does not come out whole")
    ans = total * p // 100

    def bar(label, note=None, hi=False):
        fig = {"kind": "barModel", "bars": [{"brace": whole % total, "segments": [
            {"units": round(p / 10.0, 2), "label": label, "tone": "unknown" if label.endswith("?") else "a"},
            {"units": round((100 - p) / 10.0, 2), "tone": "b"}]}]}
        if note:
            fig["note"] = note
        if hi:
            fig["highlight"] = ["b0s0"]
        return fig

    need(q, ans)
    tag = "%d%% = ?" % p
    steps = [{"text": "%d%% means %d out of every 100. Picture the whole %s as a bar, with %d%% of it shaded." % (p, p, (whole % total) if part else "number %d" % total, p),
              "figure": bar(tag, "The whole bar is 100%")}]
    if total % 100 == 0:
        one = total // 100
        steps.append({"text": "First find 1%%: %d ÷ 100 = %d." % (total, one), "figure": bar(tag, "1%% of %d is %d" % (total, one))})
        steps.append({"text": "%d%% is %d lots of that: %d × %d = %d. %s" % (p, p, one, p, ans, close % ans),
                      "figure": bar(str(ans), "%d × %d = %d" % (one, p, ans), True)})
    else:
        steps.append({"text": "Multiply by %d, then divide by 100: %d × %d = %d." % (p, total, p, total * p), "figure": bar(tag)})
        steps.append({"text": "%d ÷ 100 = %d. %s" % (total * p, ans, close % ans),
                      "figure": bar(str(ans), "%d × %d ÷ 100 = %d" % (total, p, ans), True)})
    return {"figure": bar(tag), "steps": steps}


# ── Family: HCF and LCM of two numbers (computed steps) ──────────────────────

def factors(x):
    return [d for d in range(1, x + 1) if x % d == 0]


def listed(values):
    return ", ".join(str(v) for v in values)


@rule("HCF / LCM of two numbers (no steps)")
def hcf_lcm(q):
    m = M(r"Find the (HCF|LCM) of (\d+) and (\d+)\.", q["questionText"].strip())
    if not m or own_steps(q):
        return None
    kind, a, b = m.group(1), int(m.group(2)), int(m.group(3))
    if a == b or min(a, b) < 2:
        raise Skip("degenerate pair")
    h = math.gcd(a, b)
    l = a * b // h
    if kind == "HCF":
        need(q, h)
        fa, fb = factors(a), factors(b)
        both = [d for d in fa if d in fb]
        steps = [
            {"text": "A factor divides a number exactly. The factors of %d are %s." % (a, listed(fa))},
            {"text": "The factors of %d are %s." % (b, listed(fb))},
            {"text": "The numbers in both lists are %s. The biggest of these is %d, so the HCF of %d and %d is %d." % (listed(both), h, a, b, h)},
        ]
        only_a, only_b = listed([d for d in fa if d not in both]), listed([d for d in fb if d not in both])
        if only_a and only_b and max(len(only_a), len(only_b), len(listed(both))) <= 40:
            steps[2]["figure"] = {"kind": "venn", "leftTitle": "Factors of %d" % a, "rightTitle": "Factors of %d" % b,
                                  "left": only_a, "both": listed(both), "right": only_b, "highlight": ["both"],
                                  "note": "Biggest shared factor: %d" % h}
        if len(steps[0]["text"]) > 220 or len(steps[1]["text"]) > 220 or len(steps[2]["text"]) > 220:
            raise Skip("factor lists too long")
        return {"steps": steps}
    need(q, l)
    big, small = max(a, b), min(a, b)
    jumps = l // big
    if jumps == 1:
        return {"steps": [
            {"text": "The LCM is the smallest number that both %d and %d divide into exactly." % (a, b)},
            {"text": "%d ÷ %d = %d exactly, so %d is already a multiple of %d. The LCM of %d and %d is %d." % (big, small, big // small, big, small, a, b, l)},
        ]}
    if jumps <= 8:
        mult = [big * i for i in range(1, jumps + 1)]
        line = {"kind": "numberLine", "min": 0, "max": l, "step": big,
                "hops": [{"from": big * i, "to": big * (i + 1)} for i in range(jumps)]}
        return {"steps": [
            {"text": "The LCM is the smallest number that both %d and %d divide into exactly. Count up in jumps of the bigger number, %d: %s." % (a, b, big, listed(mult)),
             "figure": dict(line, note="Jumps of %d" % big)},
            {"text": "Check each one: can %d divide it exactly? %d is the first that works: %d × %d = %d, and it is also %d × %d." % (small, l, small, l // small, l, big, jumps),
             "figure": dict(line, points=[{"at": l, "label": str(l)}], highlight=["p0"], note="%d × %d = %d and %d × %d = %d" % (big, jumps, l, small, l // small, l))},
            {"text": "So the LCM of %d and %d is %d." % (a, b, l)},
        ]}
    if h == 1:
        return {"steps": [
            {"text": "The LCM is the smallest number that both %d and %d divide into exactly." % (a, b)},
            {"text": "%d and %d share no factor except 1. When that happens, the LCM is simply the two numbers multiplied." % (a, b)},
            {"text": "%d × %d = %d. The LCM of %d and %d is %d." % (a, b, l, a, b, l)},
        ]}
    return {"steps": [
        {"text": "The LCM is the smallest number that both %d and %d divide into exactly. A quick way: multiply the two numbers, then divide by their HCF." % (a, b)},
        {"text": "The biggest number that divides both %d and %d is %d, so the HCF is %d." % (a, b, h, h)},
        {"text": "%d × %d = %d, and %d ÷ %d = %d. The LCM of %d and %d is %d." % (a, b, a * b, a * b, h, l, a, b, l)},
    ]}


# ── Family: adding and subtracting like fractions (computed steps) ───────────

@rule("like fractions: a/n ± b/n (no steps)")
def like_fractions(q):
    m = M(r"What is (\d+)/(\d+) ([+−-]) (\d+)/(\d+)\?", q["questionText"].strip())
    if not m or own_steps(q):
        return None
    a, d1, op, b, d2 = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    if d1 != d2 or d1 < 2:
        return None  # left to the unlike-fractions rule below
    plus = op == "+"
    top = a + b if plus else a - b
    if top <= 0 or a > d1 or b > d1:
        return None
    raw = "%d/%d" % (top, d1)
    simple = Fraction(top, d1)
    simple_text = "%d/%d" % (simple.numerator, simple.denominator) if simple.denominator != 1 else str(simple.numerator)
    key = key_text(q).replace(" ", "")
    if key not in (raw, simple_text):
        raise Skip("computed answer differs from the key")
    drawable = d1 <= 24

    def bars(*items, **extra):
        return dict({"kind": "fractionBars", "bars": [{"parts": d1, "shaded": s, "label": "%d/%d" % (s, d1)} for s in items]}, **extra)

    steps = [
        {"text": "Both fractions have %d at the bottom, so every piece is the same size. You only need to %s the top numbers." % (d1, "add" if plus else "subtract")},
        {"text": "%d %s %d = %d, and the bottom number stays %d. So the answer is %s." % (a, "+" if plus else "−", b, top, d1, raw)},
    ]
    if drawable:
        steps[0]["figure"] = bars(a, b, note="Same-sized pieces: %d in each whole" % d1)
        if top <= d1:
            steps[1]["figure"] = bars(top, highlight=["b0"], note="%d %s %d = %d pieces" % (a, "+" if plus else "−", b, top))
    if key != raw:
        g = math.gcd(top, d1)
        steps.append({"text": "Make it simpler: %d and %d both divide by %d. %s = %s. The answer is %s." % (top, d1, g, raw, simple_text, simple_text)})
    entry = {"steps": steps}
    if drawable:
        entry["figure"] = bars(a, b)
    return entry


@rule("fractions: a/n ± b/m, one bottom number a multiple of the other (no steps)")
def unlike_fractions(q):
    m = M(r"What is (\d+)/(\d+) ([+−-]) (\d+)/(\d+)\?", q["questionText"].strip())
    if not m or own_steps(q):
        return None
    a, d1, op, b, d2 = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    plus = op == "+"
    sign = "+" if plus else "−"
    if min(d1, d2) < 2 or a > d1 or b > d2:
        raise Skip("outside the simple case")
    steps = []
    if d1 != d2:
        big, small = max(d1, d2), min(d1, d2)
        if big % small:
            raise Skip("bottom numbers are not multiples of each other")
        k = big // small
        if d1 == small:
            old, a = "%d/%d" % (a, d1), a * k
            new_text = "%d/%d" % (a, big)
        else:
            old, b = "%d/%d" % (b, d2), b * k
            new_text = "%d/%d" % (b, big)
        steps.append({"text": "The bottom numbers are different, so first make the pieces the same size. %d × %d = %d, so multiply the top and bottom of %s by %d: %s = %s." % (small, k, big, old, k, old, new_text)})
        d1 = big
    top = a + b if plus else a - b
    if top < 0:
        raise Skip("negative result")
    result = Fraction(top, d1)
    result_text = str(result.numerator) if result.denominator == 1 else "%d/%d" % (result.numerator, result.denominator)
    raw = "%d/%d" % (top, d1)
    need_text(q, result_text)
    if top == 0:
        steps.append({"text": "Look at the two fractions: %d/%d − %d/%d. You are taking away exactly what you started with, so nothing is left: %d − %d = 0. The answer is 0." % (a, d1, b, d1, a, b)})
        return {"steps": steps}
    if raw == result_text:
        steps.append({"text": "Now the pieces are the same size, so work with the top numbers: %d %s %d = %d. The bottom stays %d. The answer is %s." % (a, sign, b, top, d1, raw)})
    else:
        g = math.gcd(top, d1)
        steps.append({"text": "Now the pieces are the same size, so work with the top numbers: %d %s %d = %d. The bottom stays %d, giving %s." % (a, sign, b, top, d1, raw)})
        steps.append({"text": "Make it simpler: %d and %d both divide by %d. %s = %s. The answer is %s." % (top, d1, g, raw, result_text, result_text)})
    if d1 <= 24 and top <= d1 and len(steps) >= 2:
        steps[0]["figure"] = {"kind": "fractionBars", "note": "Now both are cut into %d equal pieces" % d1, "bars": [
            {"parts": d1, "shaded": a, "label": "%d/%d" % (a, d1)}, {"parts": d1, "shaded": b, "label": "%d/%d" % (b, d1)}]}
        steps[1]["figure"] = {"kind": "fractionBars", "highlight": ["b0"], "bars": [{"parts": d1, "shaded": top, "label": raw}]}
    return {"steps": steps}


# ── Family: fractions with steps already in the bank (step figures) ─────────

def frac_bar(parts, shaded, label):
    return {"parts": parts, "shaded": shaded, "label": label}


@rule("fractions: a/b of N")
def f_of_quantity(q):
    m = M(r"What is (\d+)/(\d+) of (\d+)\?", q["questionText"].strip())
    if not m:
        return None
    a, b, total = int(m.group(1)), int(m.group(2)), int(m.group(3))
    own_steps(q, 2)
    if not (0 < a < b <= 12) or total % b:
        raise Skip("not a proper fraction of a whole number of groups")
    one = total // b
    need(q, one * a)
    if not grounded(q, 0, one) or not grounded(q, 1, one * a):
        raise Skip("steps do not state the working")

    def bar(label=None, **extra):
        segs = []
        for i in range(b):
            seg = {"units": 1, "tone": "a" if i < a else "b"}
            if label:
                seg["label"] = label
            segs.append(seg)
        return dict({"kind": "barModel", "bars": [{"brace": str(total), "segments": segs}]}, **extra)

    hi = ["b0s%d" % i for i in range(a)] if a <= 8 else []
    if total <= 60:
        figs = [
            {"kind": "set", "total": total, "groups": b, "note": "%d shared into %d equal groups: %d in each" % (total, b, one)},
            {"kind": "set", "total": total, "groups": b, "shadedGroups": a, "highlight": ["shaded"],
             "note": "%d groups of %d: %d × %d = %d" % (a, one, one, a, one * a)},
        ]
    else:
        figs = [bar(str(one), note="%d ÷ %d = %d in each piece" % (total, b, one)),
                bar(str(one), note="%d pieces: %d × %d = %d" % (a, one, a, one * a), **({"highlight": hi} if hi else {}))]
    return {"figure": bar(note="%d/%d of %d = ?" % (a, b, total)), "stepFigures": figs}


@rule("fractions: equivalent fraction, missing top number")
def f_missing(q):
    m = M(r"Find the missing number: (\d+)/(\d+) = \?/(\d+)", q["questionText"].strip())
    if not m:
        return None
    a, b, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    own_steps(q, 2)
    if d % b or not (0 < a <= b) or d > 24 or d == b:
        raise Skip("not a simple scaling, or too many pieces to draw")
    k = d // b
    need(q, a * k)
    if not grounded(q, 0, k) or not grounded(q, 1, a * k):
        raise Skip("steps do not state the working")
    before = {"kind": "fractionBars", "bars": [frac_bar(b, a, "%d/%d" % (a, b)), frac_bar(d, 0, "?/%d" % d)]}
    return {
        "figure": before,
        "stepFigures": [
            dict(before, highlight=["b1"], note="Each piece is cut into %d: %d × %d = %d pieces" % (k, b, k, d)),
            {"kind": "fractionBars", "highlight": ["b1"], "note": "Same amount shaded: %d × %d = %d" % (a, k, a * k),
             "bars": [frac_bar(b, a, "%d/%d" % (a, b)), frac_bar(d, a * k, "%d/%d" % (a * k, d))]},
        ],
    }


@rule("fractions: gives away a/b of N, how many left")
def f_left(q):
    m = M(r"([A-Z][a-z]+) has (\d+) marbles\. \1 gives (\d+)/(\d+) of them to a friend\. How many marbles does \1 have left\?", q["questionText"].strip())
    if not m:
        return None
    total, a, b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    own_steps(q, 2)
    if not (0 < a < b <= 12) or total % b:
        raise Skip("not a proper fraction of a whole number of groups")
    given = total // b * a
    left = total - given
    need(q, left)
    if not grounded(q, 0, given) or not grounded(q, 1, left):
        raise Skip("steps do not state the working")
    pieces = [{"units": 1, "tone": "a" if i < a else "unknown"} for i in range(b)]

    def two(left_label, **extra):
        return dict({"kind": "barModel", "bars": [{"brace": "%d marbles" % total, "segments": [
            {"units": a, "label": "%d given" % given, "tone": "a"},
            {"units": b - a, "label": left_label, "tone": "unknown" if left_label == "?" else "b"}]}]}, **extra)

    return {
        "figure": {"kind": "barModel", "note": "%d/%d given away. How many are left?" % (a, b),
                   "bars": [{"brace": "%d marbles" % total, "segments": pieces}]},
        "stepFigures": [
            two("?", highlight=["b0s0"], note="%d/%d of %d = %d" % (a, b, total, given)),
            two("%d left" % left, highlight=["b0s1"], note="%d − %d = %d" % (total, given, left)),
        ],
    }


@rule("fractions: which is greater")
def f_compare(q):
    m = M(r"Which is greater: (\d+)/(\d+) or (\d+)/(\d+)\?", q["questionText"].strip())
    if not m:
        return None
    a, b, c, d = [int(g) for g in m.groups()]
    own_steps(q, 3)
    if not (0 < a <= b and 0 < c <= d) or max(b, d) > 24:
        raise Skip("improper fraction or too many pieces to draw")
    l = b * d // math.gcd(b, d)
    x, y = a * (l // b), c * (l // d)
    if x == y:
        need_text(q, "They are equal")
    else:
        need_text(q, "%d/%d" % ((a, b) if x > y else (c, d)))
    if not grounded(q, 0, l) or not grounded(q, 1, x, y):
        raise Skip("steps do not state the working")
    first, second = "%d/%d" % (a, b), "%d/%d" % (c, d)
    before = {"kind": "fractionBars", "bars": [frac_bar(b, a, first), frac_bar(d, c, second)]}
    if l <= 24:
        same = {"kind": "fractionBars", "bars": [frac_bar(l, x, "%d/%d" % (x, l)), frac_bar(l, y, "%d/%d" % (y, l))]}
    else:
        same = {"kind": "fractionBars", "bars": [frac_bar(b, a, "%s = %d/%d" % (first, x, l)), frac_bar(d, c, "%s = %d/%d" % (second, y, l))]}
    if x == y:
        last = dict(same, note="%d and %d are the same, so the fractions are equal" % (x, y))
    else:
        last = dict(same, highlight=["b0" if x > y else "b1"], note="%d is more than %d" % (max(x, y), min(x, y)))
    # No figure before answering: bars drawn to scale would show which fraction is bigger.
    return {
        "stepFigures": [
            dict(before, note="Pieces of different sizes. Cut both into %d" % l),
            dict(same, note="Now every piece is the same size"),
            last,
        ],
    }


@rule("fractions: a/n + b/n with steps")
def f_add_like(q):
    m = M(r"Simplify: (\d+)/(\d+) \+ (\d+)/(\d+)", q["questionText"].strip())
    if not m:
        return None
    a, d1, b, d2 = [int(g) for g in m.groups()]
    own_steps(q, 2)
    if d1 != d2 or not (0 < a <= d1 and 0 < b <= d1) or d1 > 24:
        raise Skip("unlike or improper fractions, or too many pieces to draw")
    top = a + b
    result = Fraction(top, d1)
    result_text = str(result.numerator) if result.denominator == 1 else "%d/%d" % (result.numerator, result.denominator)
    need_text(q, result_text)
    if not grounded(q, 0, top):
        raise Skip("steps do not state the working")
    raw = "%d/%d" % (top, d1)
    before = {"kind": "fractionBars", "bars": [frac_bar(d1, a, "%d/%d" % (a, d1)), frac_bar(d1, b, "%d/%d" % (b, d1))]}
    if top <= d1:
        first = {"kind": "fractionBars", "highlight": ["b0"], "note": "%d + %d = %d pieces shaded" % (a, b, top), "bars": [frac_bar(d1, top, raw)]}
    else:
        first = dict(before, note="%d + %d = %d pieces: more than one whole" % (a, b, top))
    second = None
    if result_text != raw and grounded(q, 1, result.numerator, result.denominator):
        if result.denominator == 1 and result.numerator == 1:
            second = {"kind": "fractionBars", "highlight": ["b0"], "note": "Every piece is shaded: one whole", "bars": [frac_bar(d1, d1, "%s = 1" % raw)]}
        elif result.numerator < result.denominator:
            second = {"kind": "fractionBars", "highlight": ["b1"], "note": "The same amount, in bigger pieces",
                      "bars": [frac_bar(d1, top, raw), frac_bar(result.denominator, result.numerator, result_text)]}
    return {"figure": before, "stepFigures": [first, second]}


# ── Family: place value (step figures) ───────────────────────────────────────

PLACES = {"units": 1, "tens": 10, "hundreds": 100, "thousands": 1000, "ten-thousands": 10000}


def digit_index(number, place, digit):
    """Index from the left of the digit sitting in `place`, or Skip if the question misdescribes it."""
    power = len(str(PLACES[place])) - 1
    if power >= len(number):
        raise Skip("number has no such place")
    idx = len(number) - 1 - power
    if number[idx] != digit:
        raise Skip("digit is not in the place the question names")
    return idx


@rule("place value: value of a digit")
def pv_digit(q):
    m = M(r"In the number (\d+), what is the place value of the digit (\d) in the (units|tens|hundreds|thousands|ten-thousands) place\?", q["questionText"].strip())
    if not m:
        return None
    number, digit, place = m.group(1), m.group(2), m.group(3)
    own_steps(q, 2)
    if len(number) > 9:
        raise Skip("number too long for the chart")
    idx = digit_index(number, place, digit)
    value = int(digit) * PLACES[place]
    need(q, value)
    if not grounded(q, 1, PLACES[place], value):
        raise Skip("steps do not state the working")
    chart = {"kind": "placeChart", "number": number, "highlight": ["d%d" % idx]}
    return {
        "figure": dict(chart),
        "stepFigures": [
            dict(chart, note="The %s sits in the %s column" % (digit, place)),
            dict(chart, note="%s × %d = %d" % (digit, PLACES[place], value)),
        ],
    }


@rule("place value: how many times one place value is another")
def pv_times(q):
    m = M(r"In the number (\d+), the place value of (\d) \(in (units|tens|hundreds|thousands|ten-thousands) place\) is how many times the place value of (\d) \(in (units|tens|hundreds|thousands|ten-thousands) place\)\?", q["questionText"].strip())
    if not m:
        return None
    number, d1, p1, d2, p2 = m.groups()
    own_steps(q, 2)
    if len(number) > 9 or d2 == "0":
        raise Skip("cannot divide by a zero place value")
    i1, i2 = digit_index(number, p1, d1), digit_index(number, p2, d2)
    v1, v2 = int(d1) * PLACES[p1], int(d2) * PLACES[p2]
    ratio = Fraction(v1, v2)
    need(q, float(ratio))
    if not grounded(q, 0, v1, v2) or not grounded(q, 1, float(ratio)):
        raise Skip("steps do not state the working")
    chart = {"kind": "placeChart", "number": number, "highlight": sorted({"d%d" % i1, "d%d" % i2})}
    return {
        "figure": dict(chart),
        "stepFigures": [
            dict(chart, note="%s in %s is %d. %s in %s is %d." % (d1, p1, v1, d2, p2, v2)),
            dict(chart, note="%d ÷ %d = %s" % (v1, v2, n(ratio))),
        ],
    }


# ── Family: money (step figures) ─────────────────────────────────────────────

@rule("money: cost of one")
def m_unit_cost(q):
    m = M(r"If (\d+) ([a-z ]+) cost Rs\.(\d+), what is the cost of one ([a-z ]+)\?", q["questionText"].strip())
    if not m:
        return None
    count, total = int(m.group(1)), int(m.group(3))
    own_steps(q, 2)
    if count < 2 or total % count:
        raise Skip("does not divide exactly")
    one = total // count
    need(q, one)
    if count > 12:
        raise Skip("too many pieces to draw")
    if not grounded(q, 1, one):
        raise Skip("steps do not state the working")

    def bar(label, tone, **extra):
        return dict({"kind": "barModel", "bars": [{"brace": "Rs.%d" % total,
                     "segments": [{"units": 1, "label": label, "tone": tone} for _ in range(count)]}]}, **extra)

    before = bar("?", "unknown", note="%d equal pieces, one for each %s" % (count, m.group(4)))
    return {
        "figure": before,
        "stepFigures": [
            dict(before, note="Share Rs.%d equally into %d pieces" % (total, count)),
            bar("Rs.%d" % one, "a", highlight=["b0s0"], note="%d ÷ %d = %d" % (total, count, one)),
        ],
    }


@rule("money: total cost")
def m_total(q):
    m = M(r"([A-Z][a-z]+) buys (\d+) ([a-z ]+) at Rs\.(\d+) each\. What is the total cost\?", q["questionText"].strip())
    if not m:
        return None
    count, price = int(m.group(2)), int(m.group(4))
    own_steps(q, 2)
    need(q, count * price)
    if not 2 <= count <= 12:
        raise Skip("too many pieces to draw")
    if not grounded(q, 1, count * price):
        raise Skip("steps do not state the working")

    def bar(brace, **extra):
        return dict({"kind": "barModel", "bars": [{"brace": brace,
                     "segments": [{"units": 1, "label": "Rs.%d" % price, "tone": "a"} for _ in range(count)]}]}, **extra)

    return {
        "figure": bar("Total = ?"),
        "stepFigures": [
            bar("Total = ?", note="%d pieces of Rs.%d, one for each of the %s" % (count, price, m.group(3))),
            bar("Rs.%d" % (count * price), highlight=["b0"], note="%d × %d = %d" % (price, count, count * price)),
        ],
    }


@rule("money: change after buying")
def m_change(q):
    m = M(r"([A-Z][a-z]+) buys (\d+) ([a-z ]+) at Rs\.(\d+) each and pays Rs\.(\d+)\. How much change does \1 get back\?", q["questionText"].strip())
    if not m:
        return None
    count, price, paid = int(m.group(2)), int(m.group(4)), int(m.group(5))
    own_steps(q, 2)
    cost = count * price
    change = paid - cost
    if change <= 0:
        raise Skip("no change to give")
    need(q, change)
    if not grounded(q, 0, cost) or not grounded(q, 1, change):
        raise Skip("steps do not state the working")
    widths = scale_units([cost, change])

    def bar(cost_label, change_label, units, **extra):
        return dict({"kind": "barModel", "bars": [{"brace": "Paid Rs.%d" % paid, "segments": [
            {"units": units[0], "label": cost_label, "tone": "a"},
            {"units": units[1], "label": change_label, "tone": "unknown" if "?" in change_label else "b"}]}]}, **extra)

    return {
        "figure": bar("%d × Rs.%d" % (count, price), "change ?", [1, 1]),
        "stepFigures": [
            bar("Rs.%d" % cost, "change ?", [1, 1], highlight=["b0s0"], note="%d × %d = %d" % (price, count, cost)),
            bar("Rs.%d" % cost, "Rs.%d" % change, widths, highlight=["b0s1"], note="%d − %d = %d" % (paid, cost, change)),
        ],
    }


@rule("money: selling price after a profit or loss")
def m_profit_loss(q):
    text = q["questionText"].strip()
    m = M(r"([A-Z][a-z]+) buys an? ([a-z ]+) for Rs\.(\d+) and sells it at a (profit) of (\d+)%\. What is the selling price\?", text) or \
        M(r"([A-Z][a-z]+) bought an? ([a-z ]+) for Rs\.(\d+) and sold it at a (loss) of (\d+)%\. What is the selling price\?", text)
    if not m:
        return None
    cp, kind, p = int(m.group(3)), m.group(4), int(m.group(5))
    own_steps(q, 2)
    if (cp * p) % 100 or not 0 < p < 100:
        raise Skip("percentage does not come out whole")
    change = cp * p // 100
    sp = cp + change if kind == "profit" else cp - change
    need(q, sp)
    if not grounded(q, 0, change) or not grounded(q, 1, sp):
        raise Skip("steps do not state the working")
    whole, part = 10.0, round(p / 10.0, 2)

    def model(change_label, sp_label, **extra):
        if kind == "profit":
            selling = [{"units": whole, "label": "Rs.%d" % cp, "tone": "a"},
                       {"units": part, "label": change_label, "tone": "unknown" if "?" in change_label or "%" in change_label else "b"}]
        else:
            selling = [{"units": round(whole - part, 2), "label": sp_label, "tone": "unknown" if sp_label == "?" else "a"},
                       {"units": part, "label": change_label, "tone": "b"}]
        sell_bar = {"label": "Selling price", "segments": selling}
        if kind == "profit":
            sell_bar["brace"] = sp_label
        return dict({"kind": "barModel", "bars": [
            {"label": "Cost price", "segments": [{"units": whole, "label": "Rs.%d" % cp, "tone": "a"}]}, sell_bar]}, **extra)

    tag = "%d%%" % p
    return {
        "figure": model(tag, "?", note="%s of %d%% on the cost price" % (kind.capitalize(), p)),
        "stepFigures": [
            model("Rs.%d" % change, "?", highlight=["b1s1"], note="%d%% of Rs.%d = Rs.%d" % (p, cp, change)),
            model("Rs.%d" % change, "Rs.%d" % sp, highlight=["b1"] if kind == "profit" else ["b1s0"],
                  note="%d %s %d = %d" % (cp, "+" if kind == "profit" else "−", change, sp)),
        ],
    }


# ── Family: shapes and angles that already have steps (step figures) ────────

@rule("geometry with steps: rectangle or square, area or perimeter")
def g_with_steps(q):
    text = q["questionText"].strip()
    m = M(r"Find the (area|perimeter) of a rectangle with length (\d+) cm and (?:width|breadth) (\d+) cm\.", text)
    square = False
    if not m:
        m = M(r"Find the (area|perimeter) of a square with side (\d+) cm\.", text)
        square = True
    if not m or not own_steps(q):
        return None
    own_steps(q, 2)
    what = m.group(1)
    l = int(m.group(2))
    b = l if square else int(m.group(3))
    ans = l * b if what == "area" else 2 * (l + b)
    need(q, ans)
    if not grounded(q, 1, ans):
        raise Skip("steps do not state the working")
    if square:
        base = {"kind": "rectangle", "square": True, "length": "%d cm" % l}
        across, down = l, l
    else:
        base, across, down = rect_base(l, b)
    if what == "area":
        squares = dict(base)
        if across <= 12:
            squares["grid"] = {"cols": across, "rows": down}
        return {"figure": dict(base, inside="Area = ?"),
                "stepFigures": [
                    dict(squares, highlight=["length"] if square else ["length", "breadth"], note="Area = %s" % ("side × side" if square else "length × breadth")),
                    dict(squares, highlight=["fill"], note="%d × %d = %d sq. cm" % (l, b, ans))]}
    if square:
        working = "%d + %d + %d + %d = %d cm" % (l, l, l, l, ans)
    else:
        working = "%d + %d + %d + %d = %d cm" % (l, b, l, b, ans)
    return {"figure": dict(base, note="Perimeter = ?"),
            "stepFigures": [
                dict(base, highlight=["border"], note="Perimeter = all the sides added together"),
                dict(base, highlight=["border"], note=working)]}


@rule("geometry with steps: area of a triangle")
def g_tri_with_steps(q):
    m = M(r"Find the area of a triangle with base (\d+) cm and height (\d+) cm\.", q["questionText"].strip())
    if not m or not own_steps(q):
        return None
    own_steps(q, 2)
    b, h = int(m.group(1)), int(m.group(2))
    area = Fraction(b * h, 2)
    need(q, float(area))
    if not grounded(q, 1, float(area)):
        raise Skip("steps do not state the working")
    base = {"kind": "triangle", "shape": "scalene", "sides": {"bc": "%d cm" % b}, "height": "%d cm" % h}
    return {"figure": dict(base, note="Area = ?"),
            "stepFigures": [
                dict(base, enclose=True, highlight=["bc", "height"], note="The triangle is half of the rectangle around it"),
                dict(base, enclose=True, highlight=["fill"], note="½ × %d × %d = %s sq. cm" % (b, h, n(area)))]}


@rule("geometry with steps: circumference of a circle")
def g_circumference(q):
    m = M(r"Find the circumference of a circle with radius (\d+) cm\. \(Use π = 22/7\)", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 2)
    r = int(m.group(1))
    c = Fraction(2 * 22 * r, 7)
    need(q, float(c))
    if not grounded(q, 1, float(c)):
        raise Skip("steps do not state the working")
    return {"figure": {"kind": "circle", "radius": "%d cm" % r, "note": "Circumference = ?"},
            "stepFigures": [
                {"kind": "circle", "radius": "%d cm" % r, "highlight": ["edge", "radius"], "note": "The circumference is the distance round the edge"},
                {"kind": "circle", "radius": "%d cm" % r, "highlight": ["edge"], "note": "2 × 22/7 × %d = %s cm" % (r, n(c))}]}


@rule("angles with steps")
def a_with_steps(q):
    text = q["questionText"].strip()
    if not own_steps(q):
        return None
    m = M(r"Two angles are (supplementary|complementary)\. If one angle is (\d+)°, find the other\.", text)
    if m:
        own_steps(q, 2)
        whole = 180 if m.group(1) == "supplementary" else 90
        a = int(m.group(2))
        if not 0 < a < whole:
            raise Skip("angle out of range")
        need(q, whole - a)
        layout = "onLine" if whole == 180 else "inRightAngle"
        before = {"kind": "angles", "layout": layout, "parts": [{"label": "%d°" % a, "size": a}, {"label": "?"}]}
        return {"figure": before, "stepFigures": [
            dict(before, note="Together the two angles make %d°" % whole),
            {"kind": "angles", "layout": layout, "highlight": ["p1"], "note": "%d° − %d° = %d°" % (whole, a, whole - a),
             "parts": [{"label": "%d°" % a, "size": a}, {"label": "%d°" % (whole - a), "size": whole - a}]}]}
    m = M(r"Two angles on a straight line are x° and (\d+)°\. Find x\.", text)
    if m:
        own_steps(q, 2)
        a = int(m.group(1))
        if not 0 < a < 180:
            raise Skip("angle out of range")
        need(q, 180 - a)
        before = {"kind": "angles", "layout": "onLine", "parts": [{"label": "x°"}, {"label": "%d°" % a, "size": a}]}
        return {"figure": before, "stepFigures": [
            dict(before, note="Angles on a straight line add up to 180°"),
            {"kind": "angles", "layout": "onLine", "highlight": ["p0"], "note": "180° − %d° = %d°" % (a, 180 - a),
             "parts": [{"label": "x = %d°" % (180 - a), "size": 180 - a}, {"label": "%d°" % a, "size": a}]}]}
    m = M(r"In a triangle, two angles are (\d+)° and (\d+)°\. Find the third angle\.", text)
    if m:
        own_steps(q, 2)
        a, b = int(m.group(1)), int(m.group(2))
        if a + b >= 180:
            raise Skip("not a triangle")
        third = 180 - a - b
        need(q, third)
        shape = "right" if b == 90 else "scalene"
        before = {"kind": "triangle", "shape": shape, "angles": {"a": "?", "b": "%d°" % b, "c": "%d°" % a}}
        return {"figure": before, "stepFigures": [
            dict(before, note="The three angles of a triangle add up to 180°"),
            {"kind": "triangle", "shape": shape, "highlight": ["a"], "note": "180° − %d° − %d° = %d°" % (a, b, third),
             "angles": {"a": "%d°" % third, "b": "%d°" % b, "c": "%d°" % a}}]}
    m = M(r"Two straight lines cross\. One angle formed is (\d+)°\. Find the vertically opposite angle\.", text)
    if m:
        own_steps(q, 2)
        a = int(m.group(1))
        if not 0 < a < 180:
            raise Skip("angle out of range")
        need(q, a)

        def cross(opposite, **extra):
            return dict({"kind": "angles", "layout": "crossing", "parts": [
                {"label": "%d°" % a, "size": a}, {"label": "p"}, {"label": opposite}, {"label": "q"}]}, **extra)

        return {"figure": cross("?"), "stepFigures": [
            cross("?", highlight=["p0", "p2"], note="Angles facing each other across the crossing are equal"),
            cross("%d°" % a, highlight=["p2"], note="The opposite angle is also %d°" % a)]}
    return None


# ── Family: measurement (step figures) ───────────────────────────────────────

@rule("measurement: bags of the same weight")
def me_bags(q):
    m = M(r"([A-Z][a-z]+) has (\d+) bags of ([a-z ]+), each weighing (\d+) kg (\d+) g\. What is the total weight in grams\?", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 2)
    count, kg, g = int(m.group(2)), int(m.group(4)), int(m.group(5))
    if not 2 <= count <= 12 or g >= 1000:
        raise Skip("too many bags to draw")
    one = kg * 1000 + g
    need(q, one * count)
    if not grounded(q, 0, one) or not grounded(q, 1, one * count):
        raise Skip("steps do not state the working")

    def bar(label, brace, **extra):
        return dict({"kind": "barModel", "bars": [{"brace": brace,
                     "segments": [{"units": 1, "label": label, "tone": "a"} for _ in range(count)]}]}, **extra)

    return {"figure": bar("%d kg %d g" % (kg, g), "Total = ? g"),
            "stepFigures": [
                bar("%d g" % one, "Total = ? g", highlight=["b0s0"], note="%d kg %d g = %d g" % (kg, g, one)),
                bar("%d g" % one, "%d g" % (one * count), highlight=["b0"], note="%d × %d = %d g" % (one, count, one * count))]}


# ── Family: equations with steps (balance) ───────────────────────────────────

@rule("equation with steps: ax ± b = c")
def e_with_steps(q):
    m = M(r"Solve: (\d+)x ([+−-]) (\d+) = (\d+)", q["questionText"].strip())
    if not m:
        return None
    steps = own_steps(q, 2)
    a, op, b, c = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    plus = op == "+"
    rhs = c - b if plus else c + b
    if a < 2 or rhs <= 0 or rhs % a:
        raise Skip("does not divide exactly")
    x = rhs // a
    need(q, x)
    expect = ("Subtract %d from both sides" if plus else "Add %d to both sides") % b
    if steps[0]["text"].strip() != expect or steps[1]["text"].strip() != "Divide both sides by %d" % a:
        raise Skip("steps are not the usual two moves")
    sign = "+" if plus else "−"
    undo = "−" if plus else "+"
    right1 = str(rhs) if grounded(q, 0, rhs) else "%d %s %d" % (c, undo, b)
    return {
        "figure": {"kind": "balance", "left": "%dx %s %d" % (a, sign, b), "right": str(c)},
        "stepFigures": [
            {"kind": "balance", "left": "%dx" % a, "right": right1, "highlight": ["right"],
             "note": ("Take %d off both sides to keep it level" if plus else "Add %d to both sides to keep it level") % b},
            {"kind": "balance", "left": "x", "right": str(x), "highlight": ["left", "right"],
             "note": "Split both sides into %d equal shares" % a},
        ],
    }


# ── Family: squares and square roots (step figures) ──────────────────────────

@rule("squares: √x + a = b")
def s_root_equation(q):
    m = M(r"If √x \+ (\d+) = (\d+), find x\.", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 2)
    a, b = int(m.group(1)), int(m.group(2))
    if b <= a:
        raise Skip("no positive root")
    r = b - a
    need(q, r * r)
    if not grounded(q, 0, r) or not grounded(q, 1, r * r):
        raise Skip("steps do not state the working")
    return {
        "figure": {"kind": "balance", "left": "√x + %d" % a, "right": str(b)},
        "stepFigures": [
            {"kind": "balance", "left": "√x", "right": str(r), "highlight": ["right"], "note": "Take %d off both sides: %d − %d = %d" % (a, b, a, r)},
            {"kind": "balance", "left": "x", "right": str(r * r), "highlight": ["left", "right"], "note": "%d × %d = %d" % (r, r, r * r)},
        ],
    }


@rule("squares: square root of a perfect square")
def s_root(q):
    m = M(r"Find the square root of (\d+)\.", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 2)
    sq = int(m.group(1))
    r = math.isqrt(sq)
    if r * r != sq:
        raise Skip("not a perfect square")
    need(q, r)
    if not grounded(q, 1, r):
        raise Skip("steps do not state the working")
    before = {"kind": "rectangle", "square": True, "length": "?", "inside": "Area = %d" % sq}
    return {
        "figure": before,
        "stepFigures": [
            dict(before, highlight=["length"], note="Which side length gives a square of area %d?" % sq),
            {"kind": "rectangle", "square": True, "length": str(r), "inside": "Area = %d" % sq, "highlight": ["length"],
             "note": "%d × %d = %d" % (r, r, sq)},
        ],
    }


@rule("squares: square of a number")
def s_square(q):
    m = M(r"Find the square of (\d+)\.", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 2)
    s = int(m.group(1))
    need(q, s * s)
    if not grounded(q, 1, s * s):
        raise Skip("steps do not state the working")
    base = {"kind": "rectangle", "square": True, "length": str(s)}
    squares = dict(base)
    if s <= 12:
        squares["grid"] = {"cols": s, "rows": s}
    return {
        "figure": dict(base, inside="?"),
        "stepFigures": [
            dict(squares, highlight=["length"], note="%d rows of %d small squares" % (s, s)),
            dict(squares, highlight=["fill"], note="%d × %d = %d" % (s, s, s * s)),
        ],
    }


# ── Family: sharing in a ratio (step figures) ────────────────────────────────

@rule("ratio: share a quantity in the ratio a:b")
def r_share(q):
    text = q["questionText"].strip()
    m = M(r"Divide (\d+) in the ratio (\d+):(\d+)\. What is the (smaller|larger) share\?", text)
    if m:
        total, a, b, which, item = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), ""
    else:
        m = M(r"([A-Z][a-z]+) has (\d+) ([a-z]+) and divides them in the ratio (\d+):(\d+)\. How many \3 are in the (smaller|larger) group\?", text)
        if not m:
            return None
        total, item, a, b, which = int(m.group(2)), " " + m.group(3), int(m.group(4)), int(m.group(5)), m.group(6)
    own_steps(q, 2)
    if a == b or a + b > 12 or total % (a + b) or min(a, b) < 1:
        raise Skip("ratio does not share the total exactly")
    unit = total // (a + b)
    wanted = max(a, b) if which == "larger" else min(a, b)
    ans = unit * wanted
    need(q, ans)
    if not grounded(q, 1, ans):
        raise Skip("steps do not state the working")
    brace = ("%d%s" % (total, item))[:24]
    pieces = [{"units": 1, "tone": "a" if i < a else "b"} for i in range(a + b)]
    first_wanted = a == wanted
    after = {"kind": "barModel", "highlight": ["b0s0" if first_wanted else "b0s1"],
             "note": "The %s share is %d" % (which, ans),
             "bars": [{"brace": brace, "segments": [
                 dict({"units": a, "tone": "a"}, **({"label": str(ans)} if first_wanted else {})),
                 dict({"units": b, "tone": "b"}, **({} if first_wanted else {"label": str(ans)}))]}]}
    before = {"kind": "barModel", "note": "Ratio %d:%d. The %s share = ?" % (a, b, which),
              "bars": [{"brace": brace, "segments": pieces}]}
    return {
        "figure": before,
        "stepFigures": [
            dict(before, note="%d equal parts on one side, %d on the other" % (a, b)),
            after,
        ],
    }


# ── Family: speed, distance and time (step figures) ──────────────────────────

@rule("speed: one journey")
def sp_single(q):
    text = q["questionText"].strip()
    own = q.get("stepByStep") or []
    m = M(r"A [a-z]+ travels (\d+) km at a speed of (\d+) km/hr\. How long does the journey take\?", text)
    if m:
        d, s = int(m.group(1)), int(m.group(2))
        if d % s:
            raise Skip("does not divide exactly")
        ans, before, after, work = d // s, ("%d km" % d, "%d km/hr, ? h" % s), ("%d km" % d, "%d km/hr, %d h" % (s, d // s)), "%d ÷ %d = %d hours" % (d, s, d // s)
        formula = "Time = distance ÷ speed"
    else:
        m = M(r"A [a-z]+ travels at (\d+) km/hr for (\d+) hours\. What distance does it cover\?", text)
        if m:
            s, t = int(m.group(1)), int(m.group(2))
            ans, before, after, work = s * t, ("? km", "%d km/hr, %d h" % (s, t)), ("%d km" % (s * t), "%d km/hr, %d h" % (s, t)), "%d × %d = %d km" % (s, t, s * t)
            formula = "Distance = speed × time"
        else:
            m = M(r"A [a-z]+ covers (\d+) km in (\d+) hours\. Find its speed\.", text)
            if not m:
                return None
            d, t = int(m.group(1)), int(m.group(2))
            if d % t:
                raise Skip("does not divide exactly")
            ans, before, after, work = d // t, ("%d km" % d, "? km/hr, %d h" % t), ("%d km" % d, "%d km/hr, %d h" % (d // t, t)), "%d ÷ %d = %d km/hr" % (d, t, d // t)
            formula = "Speed = distance ÷ time"
    if len(own) != 2:
        raise Skip("unexpected number of steps")
    need(q, ans)
    if not grounded(q, 1, ans):
        raise Skip("steps do not state the working")

    def road(labels, **extra):
        return dict({"kind": "journey", "places": ["Start", "End"], "legs": [{"top": labels[0], "bottom": labels[1]}]}, **extra)

    return {"figure": road(before), "stepFigures": [road(before, note=formula), road(after, highlight=["l0"], note=work)]}


@rule("speed: average speed over three stretches")
def sp_average(q):
    m = M(r"[A-Z][a-z]+ covers (\d+) km at (\d+) km/hr, (\d+) km at (\d+) km/hr, and (\d+) km at (\d+) km/hr\. What is (?:his|her) average speed\?", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 4)
    v = [int(g) for g in m.groups()]
    dist, speed = v[0::2], v[1::2]
    if any(d % s for d, s in zip(dist, speed)):
        raise Skip("does not divide exactly")
    times = [d // s for d, s in zip(dist, speed)]
    if sum(dist) % sum(times):
        raise Skip("does not divide exactly")
    ans = sum(dist) // sum(times)
    need(q, ans)
    if not grounded(q, 0, *times) or not grounded(q, 1, sum(dist)) or not grounded(q, 2, sum(times)) or not grounded(q, 3, ans):
        raise Skip("steps do not state the working")
    places = ["Start", "A", "B", "End"]
    given = [{"top": "%d km" % d, "bottom": "%d km/hr" % s} for d, s in zip(dist, speed)]
    timed = [{"top": "%d km" % d, "bottom": "%d h" % t} for d, t in zip(dist, times)]
    return {
        "figure": {"kind": "journey", "places": places, "legs": given, "note": "Average speed = ?"},
        "stepFigures": [
            {"kind": "journey", "places": places, "legs": timed, "note": "Time for each stretch = distance ÷ speed"},
            {"kind": "journey", "places": places, "legs": timed, "note": "Total distance = %d km" % sum(dist)},
            {"kind": "journey", "places": places, "legs": timed, "note": "Total time = %d hours" % sum(times)},
            {"kind": "journey", "places": ["Start", "End"], "legs": [{"top": "%d km" % sum(dist), "bottom": "%d h" % sum(times)}],
             "highlight": ["l0"], "note": "%d ÷ %d = %d km/hr" % (sum(dist), sum(times), ans)},
        ],
    }


# ── Family: HCF with steps (factor trees) ────────────────────────────────────
# The bank's own steps for these are terse ("Find factors of 75 and 45." / "HCF = 15"),
# so the only numbers a step figure may show are the two numbers and the HCF.
# A factor tree needs nothing else: the renderer works the tree out itself.

@rule("HCF with steps: factor trees")
def hcf_with_steps(q):
    m = M(r"Find the HCF of (\d+) and (\d+)\.", q["questionText"].strip())
    if not m or not own_steps(q):
        return None
    own_steps(q, 2)
    a, b = int(m.group(1)), int(m.group(2))
    if a == b or not (4 <= a <= 1000 and 4 <= b <= 1000):
        raise Skip("numbers outside the factor-tree range")
    h = math.gcd(a, b)
    need(q, h)
    if not grounded(q, 1, h):
        raise Skip("steps do not state the working")
    return {"stepFigures": [
        {"kind": "factorTree", "number": a, "highlight": ["primes"], "note": "Break %d into its prime factors" % a},
        {"kind": "factorTree", "number": b, "highlight": ["primes"],
         "note": ("%d and %d share no prime factor, so the HCF is 1" % (a, b)) if h == 1 else
                 ("Now %d. The primes both trees share multiply to %d" % (b, h))},
    ]}


# ── Family: ages in a ratio (step figures) ───────────────────────────────────

@rule("ages: two ages in a ratio")
def age_ratio(q):
    m = M(r"The ages of ([A-Z][a-z]+) and ([A-Z][a-z]+) are in the ratio (\d+):(\d+)\. If \2 is (\d+) years old, how old is \1\?", q["questionText"].strip())
    if not m:
        return None
    own_steps(q, 3)
    first, second, a, b, age = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
    if not (1 <= a <= 12 and 1 <= b <= 12) or age % b or len(first) > 18 or len(second) > 18:
        raise Skip("ratio does not fit the age exactly")
    unit = age // b
    need(q, unit * a)
    if not grounded(q, 1, unit) or not grounded(q, 2, unit * a):
        raise Skip("steps do not state the working")

    def model(label, brace, **extra):
        def segs(count, tone):
            return [dict({"units": 1, "tone": tone}, **({"label": label} if label else {})) for _ in range(count)]
        return dict({"kind": "barModel", "bars": [
            {"label": first, "brace": brace, "segments": segs(a, "unknown" if brace == "?" else "a")},
            {"label": second, "brace": "%d years" % age, "segments": segs(b, "b")}]}, **extra)

    return {
        "figure": model(None, "?", note="Ratio %d:%d. Every piece is the same size" % (a, b)),
        "stepFigures": [
            model(None, "?", note="%d equal parts for %s, %d for %s" % (a, first, b, second)),
            model(str(unit), "?", highlight=["b1"], note="One part: %d ÷ %d = %d" % (age, b, unit)),
            model(str(unit), "%d years" % (unit * a), highlight=["b0"], note="%d × %d = %d" % (a, unit, unit * a)),
        ],
    }


# ── RULES ABOVE THIS LINE ────────────────────────────────────────────────────

def is_templated(q):
    src = q.get("source", "")
    return q.get("topicId") == "grade5" and (src == "auto_generated_v2" or src.startswith("variant_generator_phase"))


def main():
    with io.open(SEED, encoding="utf-8") as f:
        questions = [q for q in json.load(f)["questions"] if is_templated(q)]

    out = {}
    by_rule = collections.Counter()
    skipped = collections.Counter()
    dropped = []
    unmatched = collections.Counter()
    total_by_topic = collections.Counter()
    done_by_topic = collections.defaultdict(collections.Counter)

    for q in questions:
        topic = q.get("subTopic", "")
        total_by_topic[topic] += 1
        entry = None
        matched = False
        for name, fn in RULES:
            try:
                entry = fn(q)
            except Skip as why:
                skipped["%s: %s" % (name, why)] += 1
                matched = True
                break
            if entry:
                matched = True
                break
        if not entry:
            if not matched:
                unmatched[topic] += 1
            continue
        entry["origin"] = "rule"
        problems = validate.check_entry(q["id"], entry, q)
        if problems:
            dropped.append((name, problems[0]))
            continue
        out[q["id"]] = entry
        by_rule[name] += 1
        done_by_topic[topic]["any"] += 1
        for key in ("figure", "stepFigures", "steps"):
            if key in entry:
                done_by_topic[topic][key] += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("{\n")
        ids = sorted(out)
        for i, qid in enumerate(ids):
            f.write("  %s: %s%s\n" % (json.dumps(qid), json.dumps(out[qid], ensure_ascii=False), "," if i < len(ids) - 1 else ""))
        f.write("}\n")

    no_steps = [q for q in questions if not (q.get("stepByStep") or [])]
    print("templated questions: %d (%d have no steps of their own)" % (len(questions), len(no_steps)))
    print("entries written:     %d" % len(out))
    print("  with a figure before answering: %d" % sum(1 for e in out.values() if "figure" in e))
    print("  with step figures:              %d" % sum(1 for e in out.values() if "stepFigures" in e))
    print("  with computed steps:            %d of %d" % (sum(1 for e in out.values() if "steps" in e), len(no_steps)))
    print("\nby rule")
    for name, c in by_rule.most_common():
        print("  %4d  %s" % (c, name))
    print("\nby sub-topic   total | entry | figure | stepFigures | steps")
    for topic, total in total_by_topic.most_common():
        d = done_by_topic[topic]
        print("  %4d | %4d | %4d | %4d | %4d  %s" % (total, d["any"], d["figure"], d["stepFigures"], d["steps"], topic))
    print("\nmatched a template but skipped: %d" % sum(skipped.values()))
    for why, c in skipped.most_common():
        print("  %4d  %s" % (c, why))
    print("\ndropped by the checker: %d" % len(dropped))
    for name, problem in dropped[:40]:
        print("  [%s] %s" % (name, problem))
    print("\nno rule matched: %d" % sum(unmatched.values()))
    for topic, c in unmatched.most_common():
        print("  %4d  %s" % (c, topic))


if __name__ == "__main__":
    main()
