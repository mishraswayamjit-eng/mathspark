"""Figures for the Grade 4 topic gr4_circle (radius, diameter, circumference, area).

    python -X utf8 scripts/figures/authoring/g4_gr4_circle.py            # write the part file, print a summary
    python -X utf8 scripts/figures/authoring/g4_gr4_circle.py show       # also print every figure beside its question
    python -X utf8 scripts/figures/authoring/g4_gr4_circle.py show ID..  # only these questions

Writes data/question-figures/parts/g4-gr4_circle.json.

The contract's circle carries a radius, a diameter and a note, nothing else. So:
  - circles packed in a rectangle are drawn as the rectangle cut into the squares
    that hold one circle each;
  - circles that touch, or share a centre, are drawn as a bar along the line through
    their centres, each piece a radius or a diameter in true proportion;
  - questions about chords between marked points have no figure.
"""
import re
import sys

from g4_gr4_quads_kit import Part, R, T, C, BM, NL, CHART, CLOCK, rect, square4, tri_sides

part = Part("gr4_circle")
add = part.add

# ══ Rule: area or circumference from the radius ══════════════════════════════

CIRC = re.compile(r"^A circle has a radius of (\d+) cm\. What is its (area|circumference)\? \(Use π = 22/7\)$")


def answer_number(q):
    text = [o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]][0]
    return int(re.search(r"\d+", text.replace(",", "")).group(0))


def run_rules():
    for q in part.questions:
        m = CIRC.match(q["questionText"].strip())
        if not m:
            continue
        r, what = int(m.group(1)), m.group(2)
        own = q["stepByStep"]
        ans = answer_number(q)
        lr = "%d cm" % r
        last = len(own) - 1
        if what == "area":
            if ans * 7 != 22 * r * r:
                raise SystemExit("%s: the key is not 22/7 × %d × %d" % (q["id"], r, r))
            figure = C(radius=lr, note="Area = ?")
            steps = {0: C(radius=lr, note="Area = π × %d × %d" % (r, r), hl=["radius"]),
                     last: C(radius=lr, note="22/7 × %d × %d = %d cm²" % (r, r, ans), hl=["fill"])}
        else:
            if ans * 7 != 2 * 22 * r:
                raise SystemExit("%s: the key is not 2 × 22/7 × %d" % (q["id"], r))
            figure = C(radius=lr, note="Circumference = ?", hl=["edge"])
            steps = {0: C(radius=lr, note="Circumference = 2 × π × %d" % r, hl=["edge", "radius"]),
                     last: C(radius=lr, note="2 × 22/7 × %d = %d cm" % (r, ans), hl=["edge"])}
        add(q["id"], figure=figure, steps=steps, origin="rule")


run_rules()

# ══ Drawn one by one ═════════════════════════════════════════════════════════

# ── Parts of a circle ────────────────────────────────────────────────────────

add("EXT_G4_FP_2020_006",
    steps={
        0: C(diameter="diameter", note="A diameter goes straight through the centre", hl=["diameter"]),
        3: C(diameter="diameter", note="From one point, only 1 straight line passes through the centre", hl=["diameter"]),
    })

add("EXT_G4_WS2_CH21_001",
    figure=C(radius="?", note="From the centre to a point on the circle", hl=["radius"]),
    steps={
        0: C(radius="?", note="Join the centre to any point on the circle", hl=["radius"]),
        1: C(radius="?", note="Every such line has the same length", hl=["radius"]),
        2: C(radius="radius", note="This distance is the radius", hl=["radius"]),
    })

add("EXT_G4_WS2_CH21_002",
    figure=C(radius="radius", diameter="diameter"),
    steps={
        0: C(diameter="diameter", note="A diameter goes across the circle through the centre", hl=["diameter"]),
        1: C(radius="radius", diameter="diameter", note="The centre cuts it into two pieces, each a radius", hl=["radius"]),
        2: C(radius="radius", diameter="diameter", note="Diameter = 2 × radius", hl=["diameter"]),
    })

add("EXT_G4_WS2_CH21_003",
    steps={
        1: C(diameter="longest chord", note="The longest chord passes through the centre", hl=["diameter"]),
        2: C(diameter="diameter", note="A chord through the centre is a diameter", hl=["diameter"]),
    })

add("Q_CH21_004",
    steps={
        1: C(diameter="longest chord", note="A chord is longest when it passes through the centre", hl=["diameter"]),
        2: C(diameter="diameter", note="A chord through the centre is the diameter", hl=["diameter"]),
    })

add("EXT_G4_WS2_CH21_005",
    figure=C(note="The curved line that goes all the way round", hl=["edge"]),
    steps={
        0: C(note="The boundary is the curved line all the way round", hl=["edge"]),
        2: C(note="The boundary is called the circumference", hl=["edge"]),
    })

add("Q_CH21_001",
    figure=C(radius="same distance", note="Every point on the circle is this far from one fixed point"),
    steps={
        0: C(radius="r", note="Every point on the circle is the same distance from the middle", hl=["edge"]),
        1: C(radius="r", note="The compass point stays here while the pencil goes round", hl=["radius"]),
        2: C(radius="r", note="The fixed point in the middle is called the centre"),
    })

add("Q_CH21_005",
    steps={
        1: C(diameter="diameter", note="Every diameter cuts the circle into two matching halves", hl=["diameter"]),
    })

add("Q_CH21_014",
    figure=C(diameter="diameter", note="The diameter cuts the circle into two equal parts"),
    steps={
        0: C(diameter="diameter", note="A diameter passes through the centre", hl=["diameter"]),
        1: C(diameter="diameter", note="Each part is exactly half of the circle"),
        2: C(diameter="diameter", note="Half of a circle is a semicircle"),
    })

add("Q_CH21_019",
    steps={
        0: C(radius="radius", note="A radius can go to any point on the circle", hl=["radius"]),
        1: C(diameter="diameter", note="A diameter can point in any direction", hl=["diameter"]),
    })

# ── Radius and diameter ──────────────────────────────────────────────────────

add("EXT_G4_WS2_CH21_004",
    figure=C(radius="7 cm", diameter="?"),
    steps={
        0: C(radius="7 cm", diameter="?", note="The diameter is twice the radius", hl=["diameter"]),
        1: C(radius="7 cm", diameter="2 × 7 cm", hl=["diameter"]),
        2: C(radius="7 cm", diameter="14 cm", hl=["diameter"]),
    })

add("Q_CH21_003",
    figure=C(radius="9.5 cm", diameter="?"),
    steps={
        0: C(radius="9.5 cm", diameter="?", note="The diameter is as long as two radii", hl=["diameter"]),
        1: C(radius="9.5 cm", diameter="2 × 9.5 cm", hl=["diameter"]),
        2: C(radius="9.5 cm", diameter="19 cm", hl=["diameter"]),
    })

add("G4A_CIRCLE_001",
    figure=C(radius="?", diameter="18 cm"),
    steps={
        0: C(radius="?", diameter="18 cm", note="The diameter is two radii", hl=["radius"]),
        1: C(radius="18 ÷ 2 cm", diameter="18 cm", hl=["radius"]),
        2: C(radius="9 cm", diameter="18 cm", hl=["radius"]),
    })

add("G4A_CIRCLE_002",
    figure=C(radius="?", diameter="12 cm", note="The compass opens from the centre to the circle"),
    steps={
        0: C(radius="?", diameter="12 cm", note="Needle at the centre, pencil on the circle: the radius", hl=["radius"]),
        1: C(radius="12 ÷ 2 cm", diameter="12 cm", note="The radius is half the diameter", hl=["radius"]),
        2: C(radius="6 cm", diameter="12 cm", hl=["radius"]),
    })

add("G4A_CIRCLE_003",
    figure=C(radius="8 cm", note="How long is the longest chord?"),
    steps={
        0: C(radius="8 cm", diameter="?", note="The longest chord is the diameter", hl=["diameter"]),
        1: C(radius="8 cm", diameter="2 × 8 cm", hl=["diameter"]),
        2: C(radius="8 cm", diameter="16 cm", hl=["diameter"]),
    })

add("G4A_CIRCLE_004",
    figure=C(radius="6 cm", note="P is 4 cm from the centre. Where is P?"),
    steps={
        0: C(radius="6 cm", note="Points on the circle are exactly 6 cm from the centre", hl=["edge"]),
        1: NL(0, 8, 1, points=[(0, "centre"), (4, "P"), (6, "circle")], note="Distance from the centre: 4 is less than 6", hl=["p1"]),
        2: NL(0, 8, 1, points=[(0, "centre"), (4, "P"), (6, "circle")], note="P is closer than the circle, so P is inside", hl=["p1"]),
    })

add("G4A_CIRCLE_005",
    figure=C(radius="7 cm", note="O is the centre. A and B are on the circle. OA = 7 cm"),
    steps={
        0: C(radius="7 cm", note="OA joins the centre to the circle: a radius", hl=["radius"]),
        1: C(radius="7 cm", note="OB joins the centre to the circle too: a radius"),
        2: C(radius="7 cm", note="All radii are equal, so OB = 7 cm", hl=["radius"]),
    })

add("G4A_CIRCLE_012",
    figure=BM([{"label": "Radius", "segs": [(1, "radius", "a")]},
               {"label": "Diameter", "segs": [(1, "radius", "a"), (1, "12 cm more", "b")]}]),
    steps={
        0: BM([{"label": "Diameter", "segs": [(1, "radius", "a"), (1, "radius", "a")]}], note="The diameter is two radii"),
        1: BM([{"label": "Diameter", "segs": [(1, "radius", "a"), (1, "12 cm", "b")]}], note="We are told: diameter = radius + 12 cm"),
        2: BM([{"label": "Diameter", "segs": [(1, "radius", "a"), (1, "radius", "a")]},
               {"label": "Diameter", "segs": [(1, "radius", "a"), (1, "12 cm", "b")]}],
              note="The second radius must be the 12 cm", hl=["b0s1", "b1s1"]),
        3: C(radius="12 cm", diameter="24 cm", note="Check: 24 − 12 = 12"),
    })

add("G4A_CIRCLE_013",
    figure=C(radius="6 cm", note="Which length cannot be a chord?"),
    steps={
        0: C(radius="6 cm", diameter="2 × 6 cm", note="The longest chord is the diameter", hl=["diameter"]),
        1: C(radius="6 cm", diameter="12 cm", note="A chord can be up to 12 cm long, never longer", hl=["diameter"]),
        2: NL(0, 14, 1, points=[(4, "4 cm"), (9, "9 cm"), (12, "12 cm"), (13, "13 cm")],
              note="13 cm is longer than the 12 cm diameter", hl=["p3"]),
    })

add("G4A_CIRCLE_016",
    figure=C(radius="3 cm", note="Its diameter is the radius of a big circle"),
    steps={
        0: C(radius="3 cm", diameter="6 cm", note="Small circle: diameter = 2 × 3", hl=["diameter"]),
        1: C(radius="6 cm", note="Big circle: its radius is 6 cm", hl=["radius"]),
        2: C(radius="6 cm", diameter="12 cm", note="Big circle: diameter = 2 × 6", hl=["diameter"]),
    })

# ── Circles in a row, touching, or sharing a centre (bars along the line of centres) ──

add("G4A_CIRCLE_006",
    figure=BM([[(2, "radius 3 cm", "a")] * 4], note="Four touching circles. First centre to last centre = ?"),
    steps={
        0: BM([[(1, "3 cm", "c")] + [(1, "3 cm", "a")] * 6 + [(1, "3 cm", "c")]],
              note="Neighbouring centres are two radii apart: 3 + 3 cm", hl=["b0s1", "b0s2"]),
        1: BM([[(1, "3 cm", "c")] + [(1, "3 cm", "a")] * 6 + [(1, "3 cm", "c")]],
              note="First centre to fourth centre: 3 gaps", hl=["b0s1", "b0s2", "b0s3", "b0s4", "b0s5", "b0s6"]),
        2: BM([[(1, "3 cm", "c")] + [(1, "3 cm", "a")] * 6 + [(1, "3 cm", "c")]],
              note="3 gaps of 3 + 3 cm make 18 cm", hl=["b0s1", "b0s2", "b0s3", "b0s4", "b0s5", "b0s6"]),
    })

add("G4A_CIRCLE_007",
    figure=BM([{"segs": [(1, "bangle", "a")] * 6, "brace": "?"}], note="Each bangle has radius 4 cm"),
    steps={
        0: C(radius="4 cm", diameter="2 × 4 cm", note="Each bangle is one diameter wide", hl=["diameter"]),
        1: BM([{"segs": [(1, "2 × 4", "a")] * 6, "brace": "6 × 2 × 4 cm"}], note="6 bangles in the row"),
        2: BM([{"segs": [(1, "2 × 4", "a")] * 6, "brace": "48 cm"}], note="The row is 48 cm long"),
    })

add("G4A_CIRCLE_010",
    figure=BM([{"segs": [(5, "5 cm", "a"), (3, "3 cm", "b")], "brace": "?"}], note="Centre to centre, through the point where the coins touch"),
    steps={
        0: BM([{"segs": [(5, "5 cm", "a"), (3, "3 cm", "b")], "brace": "?"}], note="The line joining the centres passes through the touching point"),
        1: BM([{"segs": [(5, "5 cm", "a"), (3, "3 cm", "b")], "brace": "?"}], note="One radius, then the other radius", hl=["b0s0", "b0s1"]),
        2: BM([{"segs": [(5, "5 cm", "a"), (3, "3 cm", "b")], "brace": "5 + 3 cm"}]),
        3: BM([{"segs": [(5, "5 cm", "a"), (3, "3 cm", "b")], "brace": "8 cm"}]),
    })

add("G4A_CIRCLE_011",
    figure=BM([{"label": "Big radius", "segs": [(9, "9 cm", "a")]},
               {"label": "Small radius", "segs": [(5, "5 cm", "b"), (4, "?", "unknown")]}],
              note="Two circles with the same centre. Width of the ring = ?"),
    steps={
        0: BM([{"label": "Big radius", "segs": [(9, "9 cm", "a")]},
               {"label": "Small radius", "segs": [(5, "5 cm", "b"), (4, "?", "unknown")]}],
              note="Out from the centre: 5 cm to the small circle, 9 cm to the big"),
        1: BM([{"label": "Big radius", "segs": [(9, "9 cm", "a")]},
               {"label": "Small radius", "segs": [(5, "5 cm", "b"), (4, "9 − 5 cm", "unknown")]}],
              note="The ring is the gap between them", hl=["b1s1"]),
        2: BM([{"label": "Big radius", "segs": [(9, "9 cm", "a")]},
               {"label": "Small radius", "segs": [(5, "5 cm", "b"), (4, "4 cm", "c")]}], hl=["b1s1"]),
    })

add("G4A_CIRCLE_019",
    figure=BM([{"label": "Big radius", "segs": [(10, "10 cm", "a")]},
               {"label": "Small radius", "segs": [(7, "?", "unknown"), (3, "3 cm", "b")]}],
              note="Both end at the point where the circles touch"),
    steps={
        0: BM([{"label": "Big radius", "segs": [(10, "10 cm", "a")]},
               {"label": "Small radius", "segs": [(7, "?", "unknown"), (3, "3 cm", "b")]}],
              note="Both centres and the touching point lie on one straight line"),
        1: BM([{"label": "Big radius", "segs": [(10, "10 cm", "a")]},
               {"label": "Small radius", "segs": [(7, "?", "unknown"), (3, "3 cm", "b")]}],
              note="Big centre: 10 cm from that point. Small centre: 3 cm", hl=["b0s0", "b1s1"]),
        2: BM([{"label": "Big radius", "segs": [(10, "10 cm", "a")]},
               {"label": "Small radius", "segs": [(7, "10 − 3 cm", "unknown"), (3, "3 cm", "b")]}], hl=["b1s0"]),
        3: BM([{"label": "Big radius", "segs": [(10, "10 cm", "a")]},
               {"label": "Small radius", "segs": [(7, "7 cm", "c"), (3, "3 cm", "b")]}], hl=["b1s0"]),
    })

_ROW = [(2, "2 cm", "a"), (2, "2 cm", "a"), (3, "3 cm", "b"), (3, "3 cm", "b"), (4, "4 cm", "c"), (4, "4 cm", "c")]
add("G4A_CIRCLE_020",
    figure=BM([[(4, "radius 2 cm", "a"), (6, "radius 3 cm", "b"), (8, "radius 4 cm", "c")]],
              note="Three touching circles in a row. First centre to last = ?"),
    steps={
        0: BM([_ROW], note="First centre to the edge of its circle: one radius, 2 cm", hl=["b0s1"]),
        1: BM([_ROW], note="Across the whole middle circle: its diameter, 2 × 3 cm", hl=["b0s2", "b0s3"]),
        2: BM([_ROW], note="Edge of the last circle to its centre: one radius, 4 cm", hl=["b0s4"]),
        3: BM([_ROW], note="2 + 3 + 3 + 4 = 12 cm", hl=["b0s1", "b0s2", "b0s3", "b0s4"]),
    })

add("G4A_CIRCLE_017",
    figure=T("equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, note="A, B, C: centres of touching circles of radius 4 cm"),
    steps={
        0: T("equilateral", sides={"ab": "4 + 4 cm", "bc": "?", "ca": "?"}, note="Each side joins two centres: radius + radius", hl=["ab"]),
        1: T("equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"}, note="3 such sides: 3 × 8 = 24 cm", hl=["ab", "bc", "ca"]),
    })

add("G4A_CIRCLE_031",
    figure=C(diameter="24 cm", note="A small circle inside touches it and passes through its centre"),
    steps={
        0: C(radius="12 cm", diameter="24 cm", note="Big circle: radius = 24 ÷ 2", hl=["radius"]),
        1: BM([{"label": "Big radius", "segs": [(1, None, "a"), (1, None, "a")], "brace": "12 cm"}],
              note="Touching point to big centre: a diameter of the small circle"),
        2: BM([{"label": "Big radius", "segs": [(1, "12 ÷ 2 cm", "a"), (1, "12 ÷ 2 cm", "a")], "brace": "12 cm"}],
              note="The small centre is halfway along", hl=["b0s1"]),
        3: BM([{"label": "Big radius", "segs": [(1, "6 cm", "a"), (1, "6 cm", "a")], "brace": "12 cm"}],
              note="Small centre to big centre: 6 cm", hl=["b0s1"]),
    })

add("G4A_CIRCLE_032",
    figure=tri_sides(9, 7, 8, lbase="9 cm", lleft="7 cm", lright="8 cm", note="The corners are the centres of the three coins"),
    steps={
        0: tri_sides(9, 7, 8, lbase="9 cm", lleft="7 cm", lright="8 cm", note="Each side is two radii. 7 + 8 + 9 counts each radius twice",
                     hl=["e0", "e1", "e2"]),
        2: tri_sides(9, 7, 8, lbase="9 cm", lleft="7 cm", lright="8 cm", note="The two smaller coins have the closest centres, 7 cm apart",
                     hl=["e0"]),
        3: tri_sides(9, 7, 8, lbase="9 cm", lleft="7 cm", lright="8 cm", corners=["r = 3 cm", "r = 4 cm", "r = 5 cm"],
                     note="Check: 3 + 4 = 7, 3 + 5 = 8 and 4 + 5 = 9"),
    })

add("G4A_CIRCLE_033",
    steps={
        0: BM([{"segs": [(7, "7 cm", "a"), (7, "7 cm", "a")], "brace": "one straight part"}], note="Centre to centre: two radii"),
        2: C(radius="7 cm", note="Two half circles make one whole circle", hl=["edge"]),
    })

# ── Circles packed in a rectangle (one circle in each square) ────────────────

add("EXT_G4_FP_2022_033",
    figure=R(grid=(4, 2), note="One circle fits in each square. Radius = 7 cm. Area = ?"),
    steps={
        0: C(radius="7 cm", diameter="2 × 7 cm", note="The diameter is twice the radius", hl=["diameter"]),
        1: R(grid=(4, 2), length="4 diameters", note="The length holds 4 circles side by side", hl=["length"]),
        2: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="The breadth holds 2 circles", hl=["breadth"]),
        3: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="Area = length × breadth = 1568 sq.cm", hl=["fill"]),
    })

add("PYQ_2019_Q15",
    figure=R(grid=(4, 2), note="One circle fits in each square. Radius = 6 cm. Perimeter = ?"),
    steps={
        0: C(radius="6 cm", diameter="12 cm", note="Diameter = 2 × 6", hl=["diameter"]),
        1: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="The length holds 4 circles, the breadth holds 2",
             hl=["length", "breadth"]),
        2: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="Round the rectangle: 2 × (4 + 2) diameters", hl=["border"]),
        3: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="Perimeter = 144 cm", hl=["border"]),
    })

add("G4A_CIRCLE_018",
    figure=R(grid=(5, 2), note="One circle in each square. Perimeter = 84 cm. Radius = ?"),
    steps={
        0: R(grid=(5, 2), length="5 diameters", breadth="2 diameters", note="Length = 5 diameters, width = 2 diameters"),
        1: R(grid=(5, 2), length="5 diameters", breadth="2 diameters", note="Length + width = 84 ÷ 2", hl=["length", "breadth"]),
        2: BM([{"segs": [(1, None, "a")] * 5 + [(1, None, "b")] * 2, "brace": "84 ÷ 2 cm"}], note="Length + width is 7 diameters"),
        3: C(radius="3 cm", diameter="6 cm", note="The radius is half the diameter", hl=["radius"]),
    })

add("G4A_CIRCLE_026",
    figure=R(grid=(4, 3), note="One circle in each square. Area = 432 sq cm. Radius = ?"),
    steps={
        0: R(grid=(4, 3), note="12 equal little squares share 432 sq cm"),
        1: R(square=True, length="6 cm", breadth="6 cm", inside="36 sq cm", note="One little square: 6 × 6 = 36"),
        2: C(diameter="6 cm", note="The side of the little square is the diameter", hl=["diameter"]),
        3: C(radius="3 cm", diameter="6 cm", note="The radius is half the diameter", hl=["radius"]),
    })

add("G4A_CIRCLE_014",
    figure=rect(20, 8, "20 cm", "8 cm", note="Round biscuits of radius 2 cm, in straight rows"),
    steps={
        0: C(radius="2 cm", diameter="2 × 2 cm", note="Each biscuit is one diameter wide", hl=["diameter"]),
        1: R(grid=(5, 1), length="20 cm", note="5 biscuits fit along the 20 cm length"),
        2: R(grid=(5, 2), length="20 cm", breadth="8 cm", note="2 rows fit across the 8 cm width"),
        3: R(grid=(5, 2), length="20 cm", breadth="8 cm", note="5 × 2 = 10 biscuits", hl=["fill"]),
    })

add("G4A_CIRCLE_024",
    figure=R(square=True, grid=(3, 3), length="24 cm", note="First tray: 3 rows of 3. Second tray: 4 rows of 4"),
    steps={
        0: R(square=True, grid=(3, 3), length="24 cm", note="First tray: 3 plates share the 24 cm", hl=["length"]),
        1: C(radius="4 cm", diameter="24 ÷ 3 cm", note="A plate in the first tray", hl=["radius"]),
        2: R(square=True, grid=(4, 4), length="24 cm", note="Second tray: 4 plates share the 24 cm", hl=["length"]),
        3: C(radius="3 cm", diameter="24 ÷ 4 cm", note="A plate in the second tray", hl=["radius"]),
        4: BM([{"label": "First tray", "segs": [(4, "4 cm", "a")]}, {"label": "Second tray", "segs": [(3, "3 cm", "b")]}],
              note="Compare the radii: 4 − 3"),
    })

add("G4A_CIRCLE_008",
    figure=R(square=True, length="10 cm", note="A circle inside just touches all four sides. Radius = ?"),
    steps={
        0: R(square=True, length="10 cm", note="The circle reaches from one side to the opposite side", hl=["length"]),
        1: C(diameter="10 cm", note="So its diameter is the side of the square", hl=["diameter"]),
        2: C(radius="10 ÷ 2 cm", diameter="10 cm", note="The radius is half the diameter", hl=["radius"]),
        3: C(radius="5 cm", diameter="10 cm", hl=["radius"]),
    })

add("G4A_CIRCLE_009",
    figure=C(radius="6 cm", note="A square fits round it, touching. Perimeter of the square = ?"),
    steps={
        0: C(radius="6 cm", diameter="12 cm", note="Side of the square = diameter = 2 × 6", hl=["diameter"]),
        1: square4("12 cm", note="4 equal sides: 4 × 12 = 48 cm"),
    })

add("G4A_CIRCLE_021",
    figure=C(note="Circumference = 88 cm. The circle fits exactly inside a square", hl=["edge"]),
    steps={
        0: C(radius="r", note="Circumference = 2 × 22/7 × r", hl=["edge"]),
        1: C(radius="14 cm", note="The radius is 14 cm", hl=["radius"]),
        2: C(radius="14 cm", diameter="28 cm", note="Side of the square = diameter = 2 × 14", hl=["diameter"]),
        3: R(square=True, length="28 cm", note="The side of the square is 28 cm"),
    })

add("G4A_CIRCLE_022",
    figure=R(square=True, length="14 cm", note="A circle of radius 7 cm is cut out of this sheet"),
    steps={
        0: R(square=True, length="14 cm", breadth="14 cm", note="Square: 14 × 14", hl=["fill"]),
        1: C(radius="7 cm", note="Circle: 22/7 × 7 × 7 = 154 sq cm", hl=["fill"]),
    })

# ── Circumference and area ───────────────────────────────────────────────────

add("EXT_G4_FP_2021_024",
    figure=C(radius="r", note="As numbers: area = 3 × circumference"),
    steps={
        0: C(radius="r", note="Area = π × r × r. Circumference = 2 × π × r"),
        1: C(radius="r", note="3 × circumference = 3 × 2 × π × r = 6 × π × r", hl=["edge"]),
        2: C(radius="r", note="π × r × r = 6 × π × r, so r = 6", hl=["radius"]),
        3: C(radius="6", hl=["radius"]),
    })

add("EXT_G4_FP_2022_020",
    figure=C(radius="r", note="Circumference and area are the same number"),
    steps={
        0: C(radius="r", note="Circumference = 2 × π × r. Area = π × r × r"),
        1: C(radius="2 cm", note="2 × π × r = π × r × r, so r = 2", hl=["radius"]),
        2: C(radius="2 cm", diameter="2 × 2 cm", note="The diameter is twice the radius", hl=["diameter"]),
        3: C(radius="2 cm", diameter="4 cm", hl=["diameter"]),
    })

add("EXT_G4_FP_2023_033",
    figure=C(radius="?", note="Circumference = 132 cm. Area = ?", hl=["edge"]),
    steps={
        0: C(radius="r", note="Circumference = 2 × 22/7 × r = 44/7 × r", hl=["edge"]),
        1: C(radius="21 cm", note="r = 132 × 7 ÷ 44 = 21 cm", hl=["radius"]),
        2: C(radius="21 cm", note="Area = π × 21 × 21", hl=["fill"]),
        3: C(radius="21 cm", note="22/7 × 21 × 21 = 1386 sq. cm", hl=["fill"]),
    })

add("EXT_G4_FP_2025_015",
    figure=rect(14, 8, "14 cm", "8 cm", note="A circle's circumference equals this perimeter. Radius = ?", hl=["border"]),
    steps={
        0: rect(14, 8, "14 cm", "8 cm", note="Perimeter = 2 × (14 + 8)", hl=["border"]),
        1: C(radius="r", note="Circumference = 44 cm = 44/7 × r", hl=["edge"]),
        2: C(radius="r", note="r = 44 × 7 ÷ 44", hl=["radius"]),
        3: C(radius="7 cm", hl=["radius"]),
    })

add("G4A_CIRCLE_015",
    figure=C(radius="7 cm", note="The same wire is bent into a square. Side = ?", hl=["edge"]),
    steps={
        0: C(radius="7 cm", note="Wire = circumference = 2 × 22/7 × 7 = 44 cm", hl=["edge"]),
        1: R(square=True, length="?", note="The same 44 cm goes round the square", hl=["border"]),
        2: R(square=True, length="?", note="4 equal sides: 44 ÷ 4", hl=["length"]),
        3: R(square=True, length="11 cm", hl=["length"]),
    })

add("G4A_CIRCLE_025",
    figure=BM([{"segs": [(1, "?", "a")] * 3, "brace": "132 cm"}], note="Each piece is bent into a circle. Radius = ?"),
    steps={
        0: BM([{"segs": [(1, "44 cm", "a")] * 3, "brace": "132 cm"}], note="One piece: 132 ÷ 3"),
        1: C(radius="r", note="Circumference of one circle = 2 × 22/7 × r = 44", hl=["edge"]),
        2: C(radius="7 cm", note="A radius of 7 cm fits: 2 × 22/7 × 7 = 44", hl=["radius"]),
    })

add("G4A_CIRCLE_027",
    figure=C(radius="7 m", note="A path 7 m wide runs all the way round this pond"),
    steps={
        0: BM([{"segs": [(7, "pond 7 m", "a"), (7, "path 7 m", "b")], "brace": "7 + 7 m"}], note="Radius of the big circle: pond and path together"),
        1: C(radius="7 + 7 m", note="Pond and path together: 616 sq m", hl=["fill"]),
        2: C(radius="7 m", note="Pond alone: 22/7 × 7 × 7 = 154 sq m", hl=["fill"]),
        3: BM([{"label": "Big circle", "segs": [(1, "pond 154", "a"), (3, "path ?", "unknown")], "brace": "616 sq m"}],
              note="Take the pond out of the big circle"),
        4: BM([{"label": "Big circle", "segs": [(1, "pond 154", "a"), (3, "path 462", "b")], "brace": "616 sq m"}],
              note="616 − 154 = 462 sq m", hl=["b0s1"]),
    })

add("G4A_CIRCLE_028",
    figure=BM([{"label": "Old circumference", "segs": [(1, "old", "a")]},
               {"label": "New circumference", "segs": [(1, "old", "a"), (1, "88 cm more", "b")]}],
              note="The radius is made twice as long"),
    steps={
        0: BM([{"label": "Old circumference", "segs": [(1, "old", "a")]},
               {"label": "New circumference", "segs": [(1, "old", "a"), (1, "old", "a")]}],
              note="Double the radius gives double the circumference"),
        1: BM([{"label": "Old circumference", "segs": [(1, "88 cm", "a")]},
               {"label": "New circumference", "segs": [(1, "88 cm", "a"), (1, "88 cm more", "b")]}],
              note="The extra part is as long as the old circumference", hl=["b0s0"]),
        2: C(radius="14 cm", note="Circumference 88 cm: the radius is 14 cm", hl=["edge"]),
        3: C(radius="28 cm", note="Check: new radius 28 cm, circumference 88 cm longer", hl=["edge"]),
    })

add("G4A_CIRCLE_034",
    figure=C(radius="7 cm", note="The tip of the hour hand moves round this circle", hl=["edge"]),
    steps={
        0: C(radius="7 cm", note="Once round: 2 × 22/7 × 7 = 44 cm", hl=["edge"]),
        1: CLOCK(12, 0, note="Once round takes 12 hours, so 24 hours is 2 rounds", hl=["hour"]),
        2: C(radius="7 cm", note="2 rounds: 2 × 44 = 88 cm", hl=["edge"]),
    })

add("Q_CH21_006",
    figure=C(radius="21 cm", note="Circumference = ?", hl=["edge"]),
    steps={
        0: C(radius="21 cm", diameter="42 cm", note="Diameter = 2 × 21", hl=["diameter"]),
        3: C(radius="21 cm", diameter="42 cm", note="22/7 × 42 = 132 cm", hl=["edge"]),
    })

add("Q_CH21_007",
    figure=C(diameter="14 cm", note="Circumference = ?", hl=["edge"]),
    steps={
        0: C(diameter="14 cm", note="Circumference = π × diameter = 22/7 × 14", hl=["edge", "diameter"]),
        2: C(diameter="14 cm", note="22 × 2 = 44 cm", hl=["edge"]),
    })

_PARTS = [{"label": "Circumference", "segs": [(11, "22 parts", "a")]}, {"label": "Diameter", "segs": [(3.5, "7 parts", "b")]}]   # drawn 22 : 7
add("Q_CH21_008",
    figure=C(radius="?", note="Circumference = 440 m", hl=["edge"]),
    steps={
        0: BM([dict(_PARTS[0], brace="440 m"), _PARTS[1]], note="Circumference = 22/7 × diameter"),
        1: BM([dict(_PARTS[0], brace="440 m"), _PARTS[1]], note="One part = 440 ÷ 22", hl=["b0"]),
        2: C(diameter="140 m", note="The diameter is 7 parts: 140 m", hl=["diameter"]),
        3: C(radius="70 m", diameter="140 m", note="The radius is half of 140 m", hl=["radius"]),
    })

add("Q_CH21_009",
    figure=C(diameter="?", note="Circumference = 176 m", hl=["edge"]),
    steps={
        0: BM([dict(_PARTS[0], brace="176 m"), _PARTS[1]], note="Circumference = 22/7 × diameter"),
        1: BM([dict(_PARTS[0], brace="176 m"), _PARTS[1]], note="One part = 176 ÷ 22", hl=["b0"]),
        2: BM([dict(_PARTS[0], brace="176 m"), _PARTS[1]], note="The diameter is 7 of these parts", hl=["b1"]),
        3: C(diameter="56 m", hl=["diameter"]),
    })

add("Q_CH21_010",
    figure=C(radius="7 cm", note="Area = ?"),
    steps={
        0: C(radius="7 cm", note="Area = π × radius × radius. First 7 × 7", hl=["radius"]),
        2: C(radius="7 cm", note="22/7 × 7 × 7 = 154 cm²", hl=["fill"]),
    })

add("Q_CH21_011",
    figure=C(diameter="14 cm", note="Area = ?"),
    steps={
        0: C(radius="7 cm", diameter="14 cm", note="Radius = 14 ÷ 2", hl=["radius"]),
        3: C(radius="7 cm", diameter="14 cm", note="22/7 × 7 × 7 = 154 cm²", hl=["fill"]),
    })

add("Q_CH21_012",
    figure=C(radius="35 m", note="One lap is once round the track. 3 laps = ?", hl=["edge"]),
    steps={
        0: C(radius="35 m", diameter="2 × 35 m", note="First the diameter", hl=["diameter"]),
        1: C(radius="35 m", diameter="70 m", note="One lap = 22/7 × 70 = 220 m", hl=["edge"]),
        2: BM([{"segs": [(1, "220 m", "a")] * 3, "brace": "660 m"}], note="3 laps: 3 × 220"),
    })

add("Q_CH21_015",
    figure=C(diameter="28 cm", note="How many full turns to cover 440 cm?", hl=["edge"]),
    steps={
        0: C(diameter="28 cm", note="One rotation = circumference = π × diameter", hl=["edge", "diameter"]),
        1: C(diameter="28 cm", note="22/7 × 28 = 22 × 4 = 88 cm", hl=["edge"]),
        2: BM([{"segs": [(1, "88 cm", "a")] * 5, "brace": "440 cm"}], note="Lots of 88 cm in 440 cm: 440 ÷ 88 = 5"),
        3: BM([{"segs": [(1, "88 cm", "a")] * 5, "brace": "440 cm"}], note="5 complete rotations", hl=["b0"]),
    })

add("Q_CH21_017",
    figure=C(radius="?", note="Area = 616 cm²", hl=["fill"]),
    steps={
        0: C(radius="r", note="Area = 22/7 × r × r", hl=["fill"]),
        4: C(radius="14 cm", note="14 × 14 = 196, so the radius is 14 cm", hl=["radius"]),
    })

add("Q_CH21_018",
    figure=C(radius="7 cm", note="Which number is larger: circumference or area?"),
    steps={
        0: C(radius="7 cm", diameter="14 cm", note="Circumference = 22/7 × 14 = 44", hl=["edge"]),
        1: C(radius="7 cm", note="Area = 22/7 × 7 × 7 = 154", hl=["fill"]),
        2: CHART([("Circumference", 44), ("Area", 154)], note="154 is greater than 44", hl=["b1"]),
    })

add("Q_CH21_020",
    figure=C(diameter="14 cm", note="Cut along the diameter. Perimeter of one half = ?"),
    steps={
        0: C(diameter="14 cm", note="Whole circle: 22/7 × 14 = 44 cm", hl=["edge"]),
        1: C(diameter="14 cm", note="Curved edge of the half: 44 ÷ 2 = 22 cm", hl=["edge"]),
        2: C(diameter="14 cm", note="Straight edge: the diameter, 14 cm", hl=["diameter"]),
        3: C(diameter="14 cm", note="22 + 14 = 36 cm", hl=["edge", "diameter"]),
    })


if __name__ == "__main__":
    part.build()
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        part.show(set(sys.argv[2:]))
    part.report()
    print("wrote %s" % part.path)
