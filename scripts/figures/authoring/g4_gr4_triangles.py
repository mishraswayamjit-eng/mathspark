"""Figures for the Grade 4 Triangles questions (node gr4_triangles).

    python -X utf8 scripts/figures/authoring/g4_gr4_triangles.py                 # write the part file, print the summary
    python -X utf8 scripts/figures/authoring/g4_gr4_triangles.py review [a] [b]  # also print questions beside their figures
    python -X utf8 scripts/figures/authoring/g4_gr4_triangles.py review <id part>
    python -X utf8 scripts/figures/authoring/g4_gr4_triangles.py skips

Writes data/question-figures/parts/g4-gr4_triangles.json.

Triangles with stated angles or sides are drawn to their true shape (tri_angles,
tri_sides, right_tri in the kit). Corners: A at the top, B bottom left, C bottom right.
"""
import math
import re
import sys

from g4_gr4_angles_kit import (Book, deg, cm, n, line, T, P, R, BM, NL, tri_angles, tri_sides, right_tri, rect_diag)

book = Book("gr4_triangles")
add = book.add
skip = book.skip

SUM = "The three angles of a triangle add up to 180°"


# ══ Rules: families that differ only in their numbers ════════════════════════

def third_angle(qid, x, y, style, origin="rule"):
    """Two angles x and y given (bottom left and bottom right); find the third (top)."""
    z = 180 - x - y
    if book.answer_number(qid) != z:
        raise SystemExit("%s: the key is not %s" % (qid, z))
    if max(x, y) > 90:
        # An obtuse angle sits at the top so the triangle stands on its longest side;
        # the unknown is then the bottom right corner.
        big, small = max(x, y), min(x, y)
        sizes, known, ask = (big, small, z), ["a", "b"], "c"

        def tri(last, note=None, hl=None):
            return tri_angles(big, small, z, deg(big), deg(small), last, note=note, hl=hl)
    else:
        sizes, known, ask = (z, x, y), ["b", "c"], "a"

        def tri(last, note=None, hl=None):
            return tri_angles(z, x, y, last, deg(x), deg(y), note=note, hl=hl)
    before = tri("?")
    found = tri(deg(z), hl=[ask], note="180° − %s − %s = %s" % (deg(x), deg(y), deg(z)))
    if style == "add-rule-take":      # add the two; the rule; take away
        steps = {0: tri("?", hl=known, note="Add the two angles you know: %s and %s" % (deg(x), deg(y))),
                 1: tri("?", note="? + %s + %s = 180°" % (deg(x), deg(y))),
                 2: found}
    elif style == "rule-answer":
        steps = {0: tri("?", note=SUM), 1: found}
    else:                             # the rule; add the two; take away
        steps = {0: tri("?", note=SUM),
                 1: tri("?", hl=known, note="%s + %s = %s" % (deg(x), deg(y), deg(x + y))),
                 2: tri(deg(z), hl=[ask], note="180° − %s = %s" % (deg(x + y), deg(z)))}
    add(qid, figure=before, steps=steps, origin=origin)


def parts_word(k):
    return "1 part" if k == 1 else "%d parts" % k


def ratio_angles(qid, ratio):
    """Angles in the ratio p:q:r; find the largest. Drawn to the true shape."""
    total = sum(ratio)
    unit = 180.0 / total
    big = max(ratio)
    if book.answer_number(qid) != big * unit:
        raise SystemExit("%s: the key is not %s" % (qid, big * unit))
    sum_note = "%s = %d parts" % (" + ".join(str(k) for k in ratio), total)
    if big * unit > 90:
        # An obtuse angle sits at the top so the triangle stands on its longest side.
        i = ratio.index(big)
        ratio = [big] + ratio[:i] + ratio[i + 1:]
    sizes = [k * unit for k in ratio]
    words = [parts_word(k) for k in ratio]
    key = "abc"[ratio.index(big)]
    degrees = [deg(s) for s in sizes]
    mixed = [deg(s) if k == big else parts_word(k) for k, s in zip(ratio, sizes)]
    last = "Largest: %d × %s = %s" % (big, deg(unit), deg(big * unit))
    add(qid, origin="rule",
        figure=tri_angles(sizes[0], sizes[1], sizes[2], *words),
        steps={0: tri_angles(sizes[0], sizes[1], sizes[2], *words, note=sum_note),
               1: tri_angles(sizes[0], sizes[1], sizes[2], *words, note="One part = 180° ÷ %d = %s" % (total, deg(unit))),
               2: [tri_angles(sizes[0], sizes[1], sizes[2], *degrees, hl=[key], note=last),
                   tri_angles(sizes[0], sizes[1], sizes[2], *mixed, hl=[key], note=last)]})


def area_rule(qid, base, height):
    """Area from base and height. The contract's triangle with a dashed height has one
    fixed shape, so it is a general triangle, not drawn to the two lengths."""
    area = base * height / 2.0
    if book.answer_number(qid) != area:
        raise SystemExit("%s: the key is not %s" % (qid, area))
    b, h = cm(base), cm(height)
    add(qid, origin="rule",
        figure=T("scalene", sides={"bc": b}, height=h, note="Area = ?"),
        steps={0: T("scalene", sides={"bc": b}, height=h, enclose=True, hl=["bc", "height"], note="The triangle is half of the rectangle around it"),
               1: T("scalene", sides={"bc": b}, height=h, enclose=True, note="Rectangle: %s × %s = %s" % (n(base), n(height), n(base * height))),
               2: T("scalene", sides={"bc": b}, height=h, enclose=True, hl=["fill"], note="Half of %s is %s square cm" % (n(base * height), n(area)))})


RULES = [
    (re.compile(r"^Two angles of a triangle are (\d+)° and (\d+)°\. What is the third angle\?$"), 3,
     lambda qid, m: third_angle(qid, int(m.group(1)), int(m.group(2)), "add-rule-take")),
    (re.compile(r"^If two angles of a triangle are (\d+)° and (\d+)°, the third angle is:$"), 3,
     lambda qid, m: third_angle(qid, int(m.group(1)), int(m.group(2)), "add-rule-take")),
    (re.compile(r"^In a triangle, two angles are (\d+)° and (\d+)°\. Find the third angle\.$"), 2,
     lambda qid, m: third_angle(qid, int(m.group(1)), int(m.group(2)), "rule-answer")),
    (re.compile(r"^Angles of a triangle are in the ratio (\d+):(\d+):(\d+)\. Find the largest angle\.$"), 3,
     lambda qid, m: ratio_angles(qid, [int(m.group(1)), int(m.group(2)), int(m.group(3))])),
    (re.compile(r"^Find the area of a triangle with base (\d+) cm and height (\d+) cm\.$"), 3,
     lambda qid, m: area_rule(qid, int(m.group(1)), int(m.group(2)))),
]

GENERATED = re.compile(r"^(Q_CH\d+_\d+_V\d+|PH3_.*|EXT_G4_WS2_CH19_004)$")
for _qid in sorted(book.questions):
    if not GENERATED.match(_qid):
        continue
    _q = book.q(_qid)
    for _pattern, _expected, _build in RULES:
        _m = _pattern.match(_q["questionText"].strip())
        if _m:
            if len(_q.get("stepByStep") or []) != _expected:
                raise SystemExit("%s: expected %d steps" % (_qid, _expected))
            _build(_qid, _m)
            break

# The hand-written original of the family: same picture, its own step order.
third_angle("Q_CH19_003", 35, 65, "rule-add-take", origin="authored")


# ══ Angles of a triangle ═════════════════════════════════════════════════════

add("EXT_G4_FP_2020_035",
    figure=tri_angles(66, 48, 66, "?", "48°", "66°", note="What kind of triangle is it?"),
    steps={0: tri_angles(66, 48, 66, "?", "48°", "66°", hl=["b", "c"], note="Add the two angles you know: 48° and 66°"),
           1: tri_angles(66, 48, 66, "?", "48°", "66°", note="? = 180° − 48° − 66°"),
           2: tri_angles(66, 48, 66, "66°", "48°", "66°", hl=["a", "c"], note="48°, 66° and 66°: two of them are equal"),
           3: tri_angles(66, 48, 66, "66°", "48°", "66°", hl=["ab", "bc"], note="Two equal angles, so two equal sides: isosceles")})


def iso_pair(qid, x, y, s_try, s_third, s_show):
    """A pair from the answer choices is tried: the third angle equals the first. Steps only."""
    z = 180 - x - y
    if z != x:
        raise SystemExit("%s: %s, %s is not an isosceles pair" % (qid, x, y))
    add(qid,
        steps={s_try: tri_angles(z, x, y, "?", deg(x), deg(y), hl=["b", "c"], note="Try the pair %s and %s" % (deg(x), deg(y))),
               s_third: tri_angles(z, x, y, "?", deg(x), deg(y), note="? = 180° − %s − %s" % (deg(x), deg(y))),
               s_show: tri_angles(z, x, y, deg(z), deg(x), deg(y), hl=["a", "b"], note="%s, %s and %s: two are equal, so it is isosceles" % (deg(x), deg(y), deg(z)))})


iso_pair("EXT_G4_FP_2022_019", 63, 54, 0, 1, 2)
iso_pair("EXT_G4_FP_2024_030", 68, 44, 0, 1, 2)
iso_pair("PYQ_2019_Q34", 55, 70, 0, 1, 2)

add("EXT_G4_WS2_CH19_001",
    figure=T("scalene", angles={"a": "a", "b": "b", "c": "c"}, note="a + b + c = ?"),
    steps={0: line([("b", 47), ("a", 71), ("c", 62)], note="Put the three corners side by side: a straight line"),
           2: line([("b", 47), ("a", 71), ("c", 62)], note="A straight line is half of 360°: 180°"),
           3: T("scalene", angles={"a": "a", "b": "b", "c": "c"}, hl=["a", "b", "c"], note="a + b + c = 180°")})

add("G4A_TRIANGLES_002",
    figure=tri_angles(35, 90, 55, "35°", "90°", "55°", note="What kind of triangle is it?"),
    steps={0: tri_angles(35, 90, 55, "35°", "90°", "55°", note="The biggest angle is 90°"),
           1: tri_angles(35, 90, 55, "35°", "90°", "55°", note="An angle of 90° is a right angle"),
           2: tri_angles(35, 90, 55, "35°", "90°", "55°", note="One right angle: a right-angled triangle")})

add("G4A_TRIANGLES_005",
    figure=tri_angles(100, 40, 40, "100°", "40°", "40°", note="Which name describes it best?"),
    steps={0: tri_angles(100, 40, 40, "100°", "40°", "40°", hl=["a"], note="100° is more than 90°: obtuse-angled"),
           1: tri_angles(100, 40, 40, "100°", "40°", "40°", hl=["ab", "ca"], note="Two equal angles of 40°, so two equal sides"),
           2: tri_angles(100, 40, 40, "100°", "40°", "40°", note="An obtuse-angled isosceles triangle")})

add("G4A_TRIANGLES_007",
    figure=tri_angles(30, 90, 60, "small", None, "2 × small", note="Right-angled. One acute angle is twice the other."),
    steps={0: tri_angles(30, 90, 60, "small", None, "2 × small", note="The two acute angles together make 90°"),
           1: tri_angles(30, 90, 60, "1 part", None, "2 parts", note="1 part + 2 parts = 3 parts make 90°"),
           2: tri_angles(30, 90, 60, "30°", None, "60°", note="The acute angles are 30° and 60°"),
           3: tri_angles(30, 90, 60, "30°", None, "60°", note="The smallest angle is 30°")})

add("G4A_TRIANGLES_009",
    figure=T("equilateral", angles={"a": "?", "b": "?", "c": "?"}, note="All three angles are equal. Add any two of them."),
    steps={0: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, note="180° shared among three equal angles: 60° each"),
           1: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, hl=["a", "b"], note="60° + 60° = 120°"),
           2: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, hl=["a", "b"], note="Any two angles add up to 120°")})

add("G4A_TRIANGLES_012",
    figure=tri_angles(108, 36, 36, "3 × small", "small", "small", note="Isosceles. Find the angle between the equal sides."),
    steps={0: tri_angles(108, 36, 36, "3 parts", "1 part", "1 part", note="1 part, 1 part and 3 parts"),
           1: tri_angles(108, 36, 36, "3 parts", "1 part", "1 part", note="180° shared into five parts: 36° each"),
           2: tri_angles(108, 36, 36, "3 parts", "36°", "36°", hl=["a"], note="The angle between the equal sides: 3 × 36° = 108°"),
           3: tri_angles(108, 36, 36, "108°", "36°", "36°", hl=["a"], note="That angle is 108°")})

_THREE = "Together the three angles make 180°"
add("G4A_TRIANGLES_013",
    figure=BM([("First", [(2, "?", "unknown")]),
               ("Second", [(2, "?", "unknown"), (1, "20°", "b")]),
               ("Third", [(2, "?", "unknown"), (1, "20°", "b"), (1, "20°", "b")])], note=_THREE),
    steps={0: BM([("First", [(2, "first", "a")]),
                  ("Second", [(2, "first", "a"), (1, "20°", "b")]),
                  ("Third", [(2, "first", "a"), (1, "20°", "b"), (1, "20°", "b")])], hl=["b2"],
                 note="Third = first + 20° + 20° = first + 40°"),
           1: BM([("First", [(2, "first", "a")]),
                  ("Second", [(2, "first", "a"), (1, "20°", "b")]),
                  ("Third", [(2, "first", "a"), (1, "20°", "b"), (1, "20°", "b")])], hl=["b0s0", "b1s0", "b2s0"],
                 note="Take 20° and 40° away from 180°: three equal pieces are left"),
           2: BM([("First", [(2, "40°", "a")]),
                  ("Second", [(2, "40°", "a"), (1, "20°", "b")]),
                  ("Third", [(2, "40°", "a"), (1, "20°", "b"), (1, "20°", "b")])], hl=["b0"],
                 note="Each equal piece is the first angle: 40°"),
           3: tri_angles(80, 40, 60, "80°", "40°", "60°", note="The third angle is 40° + 40° = 80°"),
           4: tri_angles(80, 40, 60, "80°", "40°", "60°", hl=["a"], note="The largest angle is 80°")})

add("G4A_TRIANGLES_015",
    steps={3: tri_angles(45, 90, 45, "45°", "90°", "45°", hl=["ab", "bc"], note="90°, 45° and 45°: right-angled and isosceles")})

add("G4A_TRIANGLES_018",
    steps={0: tri_angles(120, 30, 30, "4 parts", "1 part", "1 part", note="First case: the parts are 1, 1 and 4"),
           1: tri_angles(120, 30, 30, "120°", "30°", "30°", hl=["a"], note="120° is obtuse, so this case is not allowed"),
           2: tri_angles(20, 80, 80, "1 part", "4 parts", "4 parts", note="Second case: the parts are 1, 4 and 4"),
           3: tri_angles(20, 80, 80, "20°", "80°", "80°", note="20°, 80° and 80°: no angle is obtuse"),
           4: tri_angles(20, 80, 80, "20°", "80°", "80°", hl=["a"], note="The smallest angle is 20°")})

add("G4A_TRIANGLES_019",
    steps={0: tri_angles(100, 40, 40, "?", "40°", "40°", note="40° is one of the equal angles: ? = 180° − 40° − 40°"),
           1: tri_angles(40, 70, 70, "40°", "?", "?", note="40° is the different angle: the equal angles share the rest"),
           2: tri_angles(40, 70, 70, "40°", "70°", "70°", note="One triangle is 40°, 40°, 100°. The other is 40°, 70°, 70°."),
           3: tri_angles(100, 40, 40, "100°", "40°", "40°", hl=["a"], note="Largest angles: 100° and 70°. 100° − 70° = 30°")})

add("G4A_TRIANGLES_022",
    steps={0: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, note="Three equal angles would be 60° each"),
           2: tri_angles(59, 60, 61, "59°", "60°", "61°", note="59° + 60° + 61° = 180°, and all three are different"),
           3: tri_angles(59, 60, 61, "59°", "60°", "61°", hl=["a"], note="The smallest angle can be as big as 59°")})

add("G4A_TRIANGLES_023",
    steps={0: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, note="Largest angle is exactly 60°. Two smallest make 120°."),
           1: tri_angles(40, 70, 70, "40°", "70°", "70°", hl=["b", "c"], note="Two angles here are 60° or more, not exactly one")})

add("G4A_TRIANGLES_027",
    steps={1: T("right", angles={"b": "90°"}, note="The two acute angles together make 90°"),
           2: tri_angles(18, 90, 72, "1 part", "90°", "4 parts", note="1 part + 4 parts = 5 parts make 90°"),
           3: tri_angles(18, 90, 72, "18°", "90°", "72°", note="The angles are 18°, 72° and 90°"),
           4: tri_angles(18, 90, 72, "18°", "90°", "72°", hl=["a"], note="The smallest angle is 18°")})

_ABC = "Angle A (top) is 50°. Angle B (left) is the biggest. Angle C = ?"
add("G4A_TRIANGLES_029",
    figure=tri_angles(50, 80, 50, "50°", "biggest", "?", note=_ABC),
    steps={0: tri_angles(50, 80, 50, "50°", "biggest", "?", note="Isosceles: two of the angles are equal"),
           1: tri_angles(50, 80, 50, "50°", "biggest", "?", hl=["a", "c"], note="B is bigger than both, so the equal pair is A and C"),
           2: tri_angles(50, 80, 50, "50°", "80°", "50°", note="B would be 180 − 50 − 50 = 80°, bigger than 50°"),
           3: tri_angles(50, 80, 50, "50°", "80°", "50°", hl=["c"], note="Angle C = angle A = 50°")})

add("G4A_TRIANGLES_030",
    figure=BM([("Bigger", [(4, "?", "unknown"), (3, "30°", "b")]), ("Smaller", [(4, "?", "unknown")])],
              note="These two angles of the triangle add up to 110°"),
    steps={0: BM([("Bigger", [(4, "?", "unknown"), (3, "30°", "b")]), ("Smaller", [(4, "?", "unknown")])], hl=["b0s0", "b1s0"],
                 note="Take away the extra 30°: two equal shares are left"),
           1: BM([("Bigger", [(4, "40°", "a"), (3, "30°", "b")]), ("Smaller", [(4, "40°", "a")])],
                 note="The two angles are 40° and 40° + 30° = 70°"),
           2: tri_angles(70, 40, 70, "?", "40°", "70°", note="Third angle: ? = 180° − 110°"),
           3: tri_angles(70, 40, 70, "70°", "40°", "70°", hl=["a", "c"], note="40°, 70° and 70°: two of them are equal"),
           4: tri_angles(70, 40, 70, "70°", "40°", "70°", hl=["ab", "bc"], note="Two equal angles: an isosceles triangle")})

add("PYQ_2016_Q22",
    steps={0: tri_angles(20, 80, 80, "?", "80°", "80°", note="Case 1: 80° is one of the equal pair"),
           1: tri_angles(80, 50, 50, "80°", "?", "?", note="Case 2: 80° is on its own. The other two share 100°."),
           2: tri_angles(80, 50, 50, "80°", "50°", "50°", hl=["b", "c"], note="They are equal: each is half of 100°, which is 50°")})

add("PYQ_2018_Q40",
    steps={1: tri_angles(66, 57, 57, "66°", "57°", "57°", note="Case one: 57°, 57° and 180 − 57 − 57 = 66°"),
           2: tri_angles(57, 61.5, 61.5, "57°", "?", "?", note="Case two: the other two share 180 − 57 = 123° equally"),
           3: tri_angles(57, 61.5, 61.5, "57°", "61.5°", "61.5°", hl=["b", "c"], note="Half of 123 is 61.5")})

add("Q_CH19_001",
    figure=T("equilateral", angles={"a": "?", "b": "?", "c": "?"}, note="All three angles are equal"),
    steps={0: T("equilateral", angles={"a": "?", "b": "?", "c": "?"}, note=SUM),
           1: T("equilateral", angles={"a": "?", "b": "?", "c": "?"}, note="Share 180° equally among the 3 angles"),
           2: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, note="180 ÷ 3 = 60: each angle is 60°")})

add("Q_CH19_004",
    figure=tri_angles(107, 28, 45, "?", "28°", "45°", note="What type of triangle is it?"),
    steps={0: tri_angles(107, 28, 45, "?", "28°", "45°", hl=["b", "c"], note="28 + 45 = 73°"),
           1: tri_angles(107, 28, 45, "107°", "28°", "45°", hl=["a"], note="180 − 73 = 107°"),
           2: tri_angles(107, 28, 45, "107°", "28°", "45°", hl=["a"], note="107° is more than 90°: an obtuse angle"),
           3: tri_angles(107, 28, 45, "107°", "28°", "45°", note="One obtuse angle: an obtuse-angled triangle")})

add("Q_CH19_006",
    steps={2: tri_angles(30, 75, 75, "30°", "75°", "75°", hl=["b", "c"], note="Two angles are both 75°, and 30 + 75 + 75 = 180"),
           3: tri_angles(30, 75, 75, "30°", "75°", "75°", hl=["ab", "ca"], note="30°, 75°, 75°: an isosceles triangle")})

add("Q_CH19_007",
    figure=tri_angles(27, 90, 63, "27°", None, "?", note="A right-angled triangle. Find the other acute angle."),
    steps={0: tri_angles(27, 90, 63, "27°", None, "?", note="The two acute angles together make 180 − 90 = 90°"),
           1: tri_angles(27, 90, 63, "27°", None, "?", note="? = 90 − 27 = 63"),
           2: tri_angles(27, 90, 63, "27°", None, "63°", note="The other acute angle is 63°")})

add("Q_CH19_008",
    figure=T("right", angles={"a": "?", "c": "?"}, note="Right-angled and isosceles: the two ? angles are equal"),
    steps={0: T("right", angles={"a": "?", "b": "90°", "c": "?"}, note="The other two angles together make 180 − 90 = 90°"),
           1: T("right", angles={"a": "?", "b": "90°", "c": "?"}, hl=["a", "c"], note="They are equal, so each is half of 90°"),
           2: T("right", angles={"a": "45°", "b": "90°", "c": "45°"}, hl=["a", "c"], note="Each equal angle is 45°")})

add("Q_CH19_009",
    steps={0: T("equilateral", angles={"a": "60°", "b": "60°", "c": "60°"}, note="Equilateral: every angle is 60°, so none can be 90°")})

add("Q_CH19_010",
    steps={2: tri_angles(150, 15, 15, "150°", "15°", "15°", note="150° is obtuse, but two angles are equal: isosceles"),
           3: tri_angles(120, 40, 20, "120°", "40°", "20°", note="120° is obtuse and all three angles are different")})

add("Q_CH19_011",
    figure=tri_angles(55, 55, 70, "third", "55°", "70°", note="Find the exterior angle next to the third angle"),
    steps={0: tri_angles(55, 55, 70, "55°", "55°", "70°", hl=["a"], note="Third interior angle: 180 − 55 − 70 = 55°"),
           1: line([("55°", 55), ("?",)], hl=["p1"], note="The exterior angle and 55° lie on a straight line"),
           2: line([("55°", 55), ("125°", 125)], hl=["p1"], note="180 − 55 = 125°, the same as 55 + 70")})

add("Q_CH19_012",
    figure=tri_angles(80, 50, 50, "?", "50°", None, note="The exterior angle at the bottom right corner is 130°"),
    steps={0: tri_angles(80, 50, 50, "?", "50°", None, hl=["a", "b"], note="The two opposite interior angles add up to 130°"),
           1: tri_angles(80, 50, 50, "80°", "50°", None, hl=["a"], note="130 − 50 = 80"),
           2: tri_angles(80, 50, 50, "80°", "50°", "50°", note="Check: 180 − 130 = 50°, and 50 + 50 + 80 = 180")})

add("Q_CH19_013",
    figure=tri_angles(40, 70, 70, "?", "70°", "70°"),
    steps={0: tri_angles(40, 70, 70, "?", "70°", "70°", hl=["b", "c"], note="The two base angles: 70 + 70 = 140°"),
           1: tri_angles(40, 70, 70, "?", "70°", "70°", hl=["a"], note="? = 180 − 140 = 40"),
           2: tri_angles(40, 70, 70, "40°", "70°", "70°", hl=["a"], note="The vertex angle is 40°")})

add("Q_CH19_014",
    figure=tri_angles(50, 65, 65, "50°", "?", "?", note="The two base angles marked ? are equal"),
    steps={0: tri_angles(50, 65, 65, "50°", "?", "?", hl=["b", "c"], note="The base angles together: 180 − 50 = 130°"),
           1: tri_angles(50, 65, 65, "50°", "?", "?", hl=["b", "c"], note="They are equal, so each is half of 130°"),
           2: tri_angles(50, 65, 65, "50°", "65°", "65°", hl=["b", "c"], note="Each base angle is 65°")})

add("Q_CH19_022",
    figure=tri_angles(60, 40, 80, "60°", "40°", "80°", note="Which side is the longest?"),
    steps={0: tri_angles(60, 40, 80, "60°", "40°", "80°", note="The longest side is opposite the largest angle"),
           1: tri_angles(60, 40, 80, "60°", "40°", "80°", hl=["ab"], note="Largest angle 80°: the side opposite it is longest")})


# ══ Naming triangles ═════════════════════════════════════════════════════════

_ALL = ["ab", "bc", "ca"]
add("EXT_G4_WS2_CH19_002",
    figure=T("equilateral", note="All three sides are the same length"),
    steps={0: T("isosceles", hl=["ab", "ca"], note="Two equal sides make an isosceles triangle"),
           1: T("equilateral", hl=_ALL, note="All three sides equal: the name means equal sides"),
           2: T("equilateral", hl=_ALL, note="An equilateral triangle")})

add("EXT_G4_WS2_CH19_003",
    figure=T("isosceles", hl=["ab", "ca"], note="The two highlighted sides are the same length"),
    steps={0: T("equilateral", hl=_ALL, note="All three sides equal make an equilateral triangle"),
           1: T("isosceles", hl=["ab", "ca"], note="Exactly two equal sides, like two equal legs"),
           2: T("isosceles", hl=["ab", "ca"], note="An isosceles triangle")})

add("EXT_G4_WS2_CH19_006",
    figure=T("right", angles={"b": "90°"}, note="One angle is 90°"),
    steps={0: T("right", angles={"b": "90°"}, hl=["b"], note="An angle of exactly 90° is a right angle"),
           2: T("right", angles={"b": "90°"}, note="A right-angled triangle")})

add("G4A_TRIANGLES_003",
    figure=T("scalene", note="All three sides have different lengths"),
    steps={0: T("isosceles", hl=["ab", "ca"], note="Two equal sides make an isosceles triangle"),
           1: T("scalene", note="This triangle has no equal sides at all"),
           2: T("scalene", note="Three different sides: a scalene triangle")})

add("Q_CH19_015",
    figure=T("right", angles={"b": "90°"}, hl=["ca"], note="What is the highlighted side called?"),
    steps={0: T("right", angles={"b": "90°"}, hl=["ca"], note="The side opposite the 90° angle is the longest side"),
           1: T("right", angles={"b": "90°"}, sides={"ca": "hypotenuse"}, hl=["ca"])})

add("Q_CH19_016",
    figure=T("scalene", note="A scalene triangle: all three sides are different"),
    steps={1: T("isosceles", height="fold line", hl=["height", "ab", "ca"], note="A fold through a corner matches only if those sides are equal"),
           2: T("scalene", note="No two sides are equal, so no fold line works")})


# ══ Sides and perimeter ══════════════════════════════════════════════════════

def flat(a, b, c, note, unit=" cm"):
    """Two short sides laid end to end above the long side, to compare lengths."""
    k = 20.0 / max(a + b, c, 20)
    return BM([[(a * k, "%s%s" % (n(a), unit), "a"), (b * k, "%s%s" % (n(b), unit), "b")], [(c * k, "%s%s" % (n(c), unit), "c")]], note=note)


add("G4A_TRIANGLES_001",
    figure=tri_sides(8, 5, 5, "8 cm", "5 cm", "5 cm", note="What kind of triangle is it?"),
    steps={0: tri_sides(8, 5, 5, "8 cm", "5 cm", "5 cm", note="5 + 5 = 10 cm, more than 8 cm: the sides do meet"),
           1: tri_sides(8, 5, 5, "8 cm", "5 cm", "5 cm", hl=["ab", "ca"], note="Exactly two sides are equal: 5 cm and 5 cm"),
           2: tri_sides(8, 5, 5, "8 cm", "5 cm", "5 cm", hl=["ab", "ca"], note="An isosceles triangle")})

add("G4A_TRIANGLES_004",
    figure=tri_sides(6, 9, 9, "6 cm", "9 cm", "9 cm", note="Perimeter = ?"),
    steps={0: tri_sides(6, 9, 9, "6 cm", "9 cm", "9 cm", note="The three sides are 9 cm, 9 cm and 6 cm"),
           1: tri_sides(6, 9, 9, "6 cm", "9 cm", "9 cm", hl=_ALL, note="9 + 9 + 6 = 24"),
           2: tri_sides(6, 9, 9, "6 cm", "9 cm", "9 cm", hl=_ALL, note="The perimeter is 24 cm")})

add("G4A_TRIANGLES_006",
    steps={0: flat(3, 4, 5, "3 + 4 = 7 is more than 5: the short sides can meet"),
           1: flat(7, 8, 14, "7 + 8 = 15 is more than 14: this set works too"),
           2: flat(4, 5, 9, "4 + 5 = 9: the short sides lie flat along the long one")})

add("G4A_TRIANGLES_008",
    figure=tri_sides(12, 14, 14, "12 cm", "?", "?", note="Perimeter = 40 cm. The two sides marked ? are equal."),
    steps={0: tri_sides(12, 14, 14, "12 cm", "?", "?", hl=["ab", "ca"], note="40 − 12 = 28 cm for the two equal sides"),
           1: tri_sides(12, 14, 14, "12 cm", "?", "?", hl=["ab", "ca"], note="28 ÷ 2 = 14"),
           2: tri_sides(12, 14, 14, "12 cm", "14 cm", "14 cm", hl=["ab", "ca"], note="Each equal side is 14 cm")})

add("G4A_TRIANGLES_010",
    figure=T("scalene", sides={"bc": "10 cm", "ab": "7 cm", "ca": "?"}, note="The third side is a whole number of centimetres"),
    steps={0: T("scalene", sides={"bc": "10 cm", "ab": "7 cm", "ca": "?"}, hl=["ab", "bc"], note="7 + 10 = 17"),
           1: flat(7, 10, 17, "At exactly 17 cm the two sides lie flat along it"),
           2: tri_sides(16, 7, 10, "16 cm", "7 cm", "10 cm", note="16 is the greatest whole number less than 17"),
           3: tri_sides(16, 7, 10, "16 cm", "7 cm", "10 cm", hl=["bc"], note="The greatest third side is 16 cm")})

add("G4A_TRIANGLES_011",
    steps={0: tri_sides(7, 3, 5, "7", "3", "5", note="3 + 5 = 8 is more than 7: a triangle"),
           1: flat(3, 5, 10, "3 + 5 = 8 is less than 10: the sticks cannot meet", unit=""),
           2: flat(3, 7, 10, "3 + 7 = 10 is only equal to 10: they lie flat", unit=""),
           3: tri_sides(10, 5, 7, "10", "5", "7", note="5 + 7 = 12 is more than 10: a triangle")})

add("G4A_TRIANGLES_014",
    steps={0: flat(12, 12, 26, "If 12 cm is an equal side: 12, 12 and 26"),
           1: flat(12, 12, 26, "12 + 12 = 24 is less than 26: it cannot close"),
           2: tri_sides(12, 19, 19, "12 cm", "?", "?", hl=["ab", "ca"], note="If 12 cm is the different side, the others share the rest"),
           3: tri_sides(12, 19, 19, "12 cm", "19 cm", "19 cm", hl=["ab", "ca"], note="12 + 19 is more than 19: the triangle closes")})

add("G4A_TRIANGLES_016",
    figure=BM([(None, [(1, "?", "unknown"), (1, "?", "unknown"), (1, "?", "unknown")], "12 cm")],
              note="Three whole-number pieces that can make a triangle"),
    steps={1: tri_sides(5, 3, 4, "5 cm", "3 cm", "4 cm", note="Longest side 5 cm: 2, 5, 5 or 3, 4, 5 (drawn here)"),
           2: T("equilateral", sides={"ab": "4 cm", "bc": "4 cm", "ca": "4 cm"}, note="Longest side 4 cm: 4 cm, 4 cm and 4 cm")})

add("G4A_TRIANGLES_017",
    figure=T("scalene", sides={"bc": "11 cm", "ab": "6 cm", "ca": "?"}, note="The third side is a whole number of centimetres"),
    steps={0: T("scalene", sides={"bc": "11 cm", "ab": "6 cm", "ca": "?"}, hl=["ca"], note="Longer than the difference: 11 − 6"),
           1: T("scalene", sides={"bc": "11 cm", "ab": "6 cm", "ca": "?"}, hl=["ca"], note="Shorter than the sum: 11 + 6"),
           2: NL(5, 17, 1, [(6, "shortest"), (16, "longest")], note="More than 5 cm, less than 17 cm: 6 cm up to 16 cm"),
           3: NL(5, 17, 1, [(6, "shortest"), (16, "longest")], note="Count the whole numbers from 6 to 16"),
           4: NL(5, 17, 1, [(6, "shortest"), (16, "longest")], note="16 − 6 + 1 = 11 different lengths")})

add("G4A_TRIANGLES_020",
    steps={1: flat(5, 5, 11, "Try 5 cm, 5 cm and 11 cm"),
           2: flat(5, 5, 11, "5 + 5 = 10 cm is shorter than 11 cm: it cannot close"),
           3: tri_sides(5, 11, 11, "5 cm", "11 cm", "11 cm", note="So the sides are 5 cm, 11 cm and 11 cm"),
           4: tri_sides(5, 11, 11, "5 cm", "11 cm", "11 cm", hl=_ALL, note="5 + 11 + 11 = 27 cm")})

add("G4A_TRIANGLES_021",
    steps={0: T("equilateral", note="3, 3, 3 and 4, 4, 4 and 8, 8, 8 all make triangles"),
           2: flat(4, 4, 8, "4 + 4 = 8: the short sticks only lie flat"),
           3: flat(3, 4, 8, "3 + 4 = 7 is shorter than 8: no triangle")})

# Five triangles in a row: up, down, up, down, up. Corners: three along the top, four along the bottom.
_H = 4 * math.sqrt(3) / 2
_ROW = [(2, 0), (6, 0), (10, 0), (12, _H), (8, _H), (4, _H), (0, _H)]
_SHARED = [(5, 0), (5, 1), (4, 1), (4, 2)]
_EDGE = [None, None, None, None, None, None, "4 cm"]
_OUTSIDE = ["e0", "e1", "e2", "e3", "e4", "e5", "e6"]
add("G4A_TRIANGLES_024",
    figure=P(_ROW, edges=_EDGE, dashed=_SHARED, note="Five triangles in a row. Dashed lines are shared sides."),
    steps={1: P(_ROW, edges=_EDGE, dashed=_SHARED, note="4 places where two neighbours share a side"),
           2: P(_ROW, edges=_EDGE, dashed=_SHARED, note="Each shared side hides 2 of the 15 sides: 8 hidden"),
           3: P(_ROW, edges=_EDGE, dashed=_SHARED, hl=_OUTSIDE, note="Count the sides on the outside, then multiply by 4 cm"),
           4: P(_ROW, edges=_EDGE, dashed=_SHARED, hl=_OUTSIDE, note="The perimeter is 28 cm")})

add("G4A_TRIANGLES_025",
    figure=tri_sides(7, 5, 6, "7 cm", "5 cm", "6 cm", note="One example. Find the smallest triangle of this kind."),
    steps={0: flat(1, 2, 3, "1 + 2 = 3: the two shorter sides lie flat"),
           1: tri_sides(4, 2, 3, "4 cm", "2 cm", "3 cm", note="2 + 3 is longer than 4: a real triangle"),
           2: tri_sides(4, 2, 3, "4 cm", "2 cm", "3 cm", hl=_ALL, note="2 + 3 + 4 = 9"),
           3: tri_sides(4, 2, 3, "4 cm", "2 cm", "3 cm", hl=_ALL, note="The smallest perimeter is 9 cm")})

add("G4A_TRIANGLES_026",
    steps={1: BM([[(15, "other two: 15 cm", "a")], [(15, "longest: 15 cm", "c")]], note="15 cm and 15 cm: only equal, so they lie flat"),
           2: BM([[(16, "other two: 16 cm", "a")], [(14, "longest: 14 cm", "c")]], note="16 cm is more than 14 cm: the sides can meet"),
           3: tri_sides(14, 14, 2, "14 cm", "14 cm", "2 cm", note="14 cm, 14 cm and 2 cm make a real triangle"),
           4: tri_sides(14, 14, 2, "14 cm", "14 cm", "2 cm", hl=["bc"], note="The longest side can be 14 cm")})

add("G4A_TRIANGLES_028",
    figure=T("scalene", sides={"bc": "9 cm", "ca": "4 cm", "ab": "?"}, note="The perimeter is a multiple of 7"),
    steps={0: NL(5, 13, 1, [(5, "more than"), (13, "less than")], note="The third side is more than 5 cm and less than 13 cm"),
           1: NL(19, 25, 1, [(19, "least"), (25, "most")], note="Third side 6 cm to 12 cm, so perimeter 19 cm to 25 cm"),
           2: NL(19, 25, 1, [(21, "multiple of 7")], hl=["p0"], note="The only multiple of 7 from 19 to 25 is 21"),
           3: T("scalene", sides={"bc": "9 cm", "ca": "4 cm", "ab": "?"}, hl=["ab"], note="? = 21 − 9 − 4 = 8"),
           4: tri_sides(9, 8, 4, "9 cm", "8 cm", "4 cm", hl=["ab"], note="The third side is 8 cm")})

add("EXT_G4_FP_2023_001",
    figure=T("scalene", sides={"bc": "20 cm", "ab": "15 cm", "ca": "?"}, note="The third side is not given"),
    steps={0: T("scalene", sides={"bc": "20 cm", "ab": "15 cm", "ca": "?"}, hl=["ab", "bc"], note="Add the two sides you know: 20 cm and 15 cm"),
           1: T("scalene", sides={"bc": "20 cm", "ab": "15 cm", "ca": "?"}, hl=["ca"], note="The third side must be shorter than 35 cm"),
           2: T("scalene", sides={"bc": "20 cm", "ab": "15 cm", "ca": "?"}, hl=_ALL, note="So the perimeter is less than 35 + 35 = 70 cm"),
           3: flat(20, 15, 37, "For 72 cm the third side is 37 cm: too long to reach across")})

# Two equal triangles joined along one whole side make a four-sided shape.
_S = 6 * math.sqrt(3) / 2
_RHOMBUS = [(3, 0), (9, 0), (6, _S), (0, _S)]
add("PYQ_2017_Q10",
    figure=P(_RHOMBUS, dashed=[(0, 2)], note="Each triangle's perimeter is 24 cm. The dashed side is shared."),
    steps={0: T("equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"}, note="3 equal sides: 24 ÷ 3 = 8 cm each"),
           1: P(_RHOMBUS, dashed=[(0, 2, "inside")], note="The joined sides lie inside: not part of the boundary"),
           2: P(_RHOMBUS, dashed=[(0, 2)], hl=["e0", "e1", "e2", "e3"], note="6 sides in all, take away the 2 joined: 4 outside"),
           3: P(_RHOMBUS, edges=["8 cm", "8 cm", "8 cm", "8 cm"], dashed=[(0, 2)], hl=["e0", "e1", "e2", "e3"], note="4 × 8 = 32 cm")})

add("PYQ_2017_Q36",
    steps={1: {"kind": "table", "headers": ["Equal sides", "Third side"],
               "rows": [["11, 11", "1"], ["10, 10", "3"], ["9, 9", "5"], ["8, 8", "7"], ["7, 7", "9"], ["6, 6", "11"]],
               "note": "Two equal sides and an odd third side make 23"},
           2: tri_sides(11, 6, 6, "11", "6", "6", note="6, 6, 11 just fits: 12 is more than 11"),
           3: flat(5, 5, 13, "5, 5, 13: the equal sides cannot reach across 13", unit=""),
           4: {"kind": "table", "headers": ["Equal sides", "Third side"],
               "rows": [["11, 11", "1"], ["10, 10", "3"], ["9, 9", "5"], ["8, 8", "7"], ["7, 7", "9"], ["6, 6", "11"]],
               "note": "6 different isosceles triangles"}})

add("Q_CH19_002",
    figure=T("equilateral", sides={"bc": "7 cm"}, note="An equilateral triangle. Perimeter = ?"),
    steps={0: T("equilateral", sides={"ab": "7 cm", "bc": "7 cm", "ca": "7 cm"}, note="3 equal sides: each side is 7 cm"),
           1: T("equilateral", sides={"ab": "7 cm", "bc": "7 cm", "ca": "7 cm"}, hl=_ALL, note="7 + 7 + 7 = 3 × 7 = 21 cm")})

add("Q_CH19_005",
    steps={1: flat(2, 5, 9, "2 + 5 = 7 is less than 9: the short sides cannot meet"),
           2: flat(1, 5, 6, "1 + 5 = 6: the short sides lie flat along the long one"),
           3: tri_sides(12, 6, 8, "12 cm", "6 cm", "8 cm", note="6 + 8 = 14 is more than 12: a triangle")})

add("Q_CH19_017",
    figure=tri_sides(15, 8, 11, "15 cm", "8 cm", "11 cm", note="Perimeter = ?"),
    steps={0: tri_sides(15, 8, 11, "15 cm", "8 cm", "11 cm", hl=_ALL, note="The perimeter is the sum of the three sides"),
           1: tri_sides(15, 8, 11, "15 cm", "8 cm", "11 cm", hl=["ab", "ca"], note="8 + 11 = 19"),
           2: tri_sides(15, 8, 11, "15 cm", "8 cm", "11 cm", hl=_ALL, note="19 + 15 = 34 cm")})

add("Q_CH19_018",
    figure=tri_sides(15, 9, 12, "?", "9 cm", "12 cm", note="Perimeter = 36 cm"),
    steps={0: tri_sides(15, 9, 12, "?", "9 cm", "12 cm", hl=_ALL, note="The three sides add up to 36 cm"),
           1: tri_sides(15, 9, 12, "?", "9 cm", "12 cm", hl=["ab", "ca"], note="12 + 9 = 21 cm"),
           2: tri_sides(15, 9, 12, "15 cm", "9 cm", "12 cm", hl=["bc"], note="36 − 21 = 15 cm")})

add("Q_CH19_024",
    figure=T("equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, note="Perimeter = 45 cm"),
    steps={0: T("equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, hl=_ALL, note="3 equal sides together make 45 cm"),
           1: T("equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, note="45 ÷ 3 = 15"),
           2: T("equilateral", sides={"ab": "15 cm", "bc": "15 cm", "ca": "15 cm"}, note="Each side is 15 cm")})


# ══ Area ═════════════════════════════════════════════════════════════════════

add("EXT_G4_FP_2021_037",
    figure=T("scalene", sides={"bc": "6 cm"}, height="4 cm", note="Area = ?"),
    steps={0: T("scalene", sides={"bc": "6 cm"}, height="4 cm", enclose=True, hl=["bc", "height"], note="Base × height: 6 × 4 = 24"),
           1: T("scalene", sides={"bc": "6 cm"}, height="4 cm", enclose=True, hl=["fill"], note="The triangle is half of that: 24 ÷ 2 = 12"),
           2: T("scalene", sides={"bc": "6 cm"}, height="4 cm", hl=["fill"], note="The area is 12 sq.cm")})

add("EXT_G4_FP_2022_018",
    figure=right_tri(19, 16, "19 cm", "16 cm", note="Area = ?"),
    steps={0: rect_diag(19, 16, "19 cm", "16 cm", note="Base × height: 19 × 16 = 304"),
           1: rect_diag(19, 16, "19 cm", "16 cm", note="The triangle is half of this rectangle: 152"),
           2: right_tri(19, 16, "19 cm", "16 cm", hl=["fill"], note="The area is 152 cm.sq.")})

add("EXT_G4_FP_2025_014",
    figure=R(square=True, length="9 cm", note="Which triangle has the same area as this square?"),
    steps={0: R(square=True, length="9 cm", inside="Area = 9 × 9", hl=["fill"]),
           2: T("scalene", sides={"bc": "27"}, height="6", enclose=True, hl=["bc", "height"], note="Base 27 and height 6: 27 × 6 = 162"),
           3: T("scalene", sides={"bc": "27"}, height="6", enclose=True, hl=["fill"], note="Half of 162 is 81, the same as the square")})

add("Q_CH19_019",
    figure=right_tri(8, 6, "8 cm", "6 cm", note="Area = ?"),
    steps={0: right_tri(8, 6, "8 cm", "6 cm", hl=["ab", "bc"], note="One leg is the base, the other is the height"),
           1: rect_diag(8, 6, "8 cm", "6 cm", note="Base times height: 6 × 8 = 48"),
           2: rect_diag(8, 6, "8 cm", "6 cm", note="The triangle is half of that rectangle: 48 ÷ 2 = 24")})

add("Q_CH19_025",
    figure=right_tri(12, 7, "12 cm", "?", note="Area = 42 cm²"),
    steps={0: right_tri(12, 7, "12 cm", "?", hl=["ab", "bc"], note="Area = ½ × base × height"),
           1: right_tri(12, 7, "12 cm", "h", note="Half of 12 is 6, so 42 = 6 × h"),
           2: right_tri(12, 7, "12 cm", "7 cm", hl=["ab"], note="h = 42 ÷ 6 = 7 cm")})


# ══ Left without a picture ═══════════════════════════════════════════════════

skip("EXT_G4_FP_2021_035", "adding up the sets in the answer choices: arithmetic, and a drawn set would point at the answer")
skip("Q_CH19_020", "a median: no figure kind draws a line from a corner to the middle of the opposite side")
skip("Q_CH19_021", "counting medians: no figure kind draws a median")
skip("Q_CH19_023", "a triangle with two right angles cannot be drawn; the reasoning is the sum 90° + 90°")

book.finish(sys.argv)
