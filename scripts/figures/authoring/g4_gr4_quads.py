"""Figures for the Grade 4 topic gr4_quads (quadrilaterals: area, perimeter, properties).

    python -X utf8 scripts/figures/authoring/g4_gr4_quads.py            # write the part file, print a summary
    python -X utf8 scripts/figures/authoring/g4_gr4_quads.py show       # also print every figure beside its question
    python -X utf8 scripts/figures/authoring/g4_gr4_quads.py show ID..  # only these questions

Writes data/question-figures/parts/g4-gr4_quads.json.

The generated families (plain area and perimeter of a rectangle or square) are drawn
by rule from the numbers in the question. Everything else is drawn one by one.
"""
import re
import sys

from g4_gr4_quads_kit import (Part, R, T, P, C, A, BM, TABLE, GRID, CHART, rect, split_rect, square4,
                              quad_angles, strip_frame, row_of_squares, RECT_PTS, SQUARE_PTS, RHOMBUS_PTS,
                              DIAMOND_PTS, PARA_PTS, TRAP_PTS, KITE_PTS, QUAD_PTS)

part = Part("gr4_quads")
add = part.add

# ══ Rules: the generated families ════════════════════════════════════════════

RECT_A = re.compile(r"^Find the (area|perimeter) of a rectangle with length (\d+) cm and (?:width|breadth) (\d+) cm\.$")
RECT_B = re.compile(r"^A rectangle is (\d+) cm long and (\d+) cm wide\. What is its (area|perimeter)\?$")
SQ_A = re.compile(r"^Each side of a square is (\d+) cm long\. What is the (area|perimeter) of the square\?$")
SQ_B = re.compile(r"^Find the (area) of a square with side (\d+) cm\.$")
SPLIT = re.compile(r"Split (\d+) into (\d+) and (\d+)")
GROUPS = re.compile(r"(\d+) × (\d+) means (\d+) groups of (\d+)")


def answer_number(q):
    text = [o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]][0]
    return int(re.search(r"\d+", text.replace(",", "")).group(0))


def area_unit(q):
    last = q["stepByStep"][-1]["text"]
    if "cm²" in last:
        return "cm²"
    if "sq.cm" in last:
        return "sq.cm"
    return "sq cm"


def area_rule(q, L, W, square):
    own = q["stepByStep"]
    ans = answer_number(q)
    if ans != L * W:
        raise SystemExit("%s: the key %s is not %s × %s" % (q["id"], ans, L, W))
    unit = area_unit(q)
    ll, lb = "%d cm" % L, "%d cm" % W

    def whole(inside=None, note=None, hl=None, both=True):
        if square:
            return R(square=True, length=ll, breadth=ll if both else None, inside=inside, note=note, hl=hl)
        return rect(L, W, ll, lb, inside=inside, note=note, hl=hl)

    steps = {}
    split = None
    for i, s in enumerate(own):
        t = s["text"]
        m = SPLIT.search(t)
        g = GROUPS.search(t)
        if i == len(own) - 1:
            steps[i] = whole(inside="%d %s" % (ans, unit), note="%d × %d = %d %s" % (L, W, ans, unit), hl=["fill"])
        elif g and L <= 12 and W <= 12:
            steps[i] = R(length=ll, breadth=lb, square=square, grid=(L, W), note="%d columns of %d unit squares" % (L, W))
        elif m:
            X, a, b = (int(v) for v in m.groups())
            which = "breadth" if X == W else ("length" if X == L else None)
            if which is None or a + b != X:
                continue
            other = L if which == "breadth" else W
            rest = t[m.end():].lstrip(". ").strip()
            kw = dict(ll=ll, lb=lb, la="%d cm" % a, lpb="%d cm" % b)
            if rest.startswith("Multiply"):
                split = (which, a, b, other, kw)
                steps[i] = split_rect(L, W, which, a, b, note="First part: %d × %d" % (other, a), hl=["a"], **kw)
            else:
                note = rest.rstrip(".")
                if len(note) > 70 or not note:
                    note = "%d × %d and %d × %d" % (a, other, b, other)
                steps[i] = split_rect(L, W, which, a, b, note=note, **kw)
        elif split and t.startswith("Now multiply"):
            which, a, b, other, kw = split
            steps[i] = split_rect(L, W, which, a, b, note="Second part: %d × %d" % (other, b), hl=["b"], **kw)
        elif i == 0:
            steps[i] = whole(note="Area = %d × %d" % (L, W), hl=["length", "breadth"])
    add(q["id"], figure=whole(inside="Area = ?", both=False), steps=steps, origin="rule")


def rect_perimeter_rule(q, L, W):
    own = q["stepByStep"]
    P_ = 2 * (L + W)
    if answer_number(q) != P_:
        raise SystemExit("%s: the key is not 2 × (%s + %s)" % (q["id"], L, W))
    ll, lb = "%d cm" % L, "%d cm" % W
    half = L + W
    steps = {}
    for i, s in enumerate(own):
        t = s["text"].lower()
        last = i == len(own) - 1
        if "formula" in t:
            steps[i] = rect(L, W, ll, lb, note="Perimeter = 2 × (length + width)", hl=["border"])
        elif last and "double" in t:
            steps[i] = rect(L, W, ll, lb, note=["2 × %d = %d cm" % (half, P_), "Perimeter = %d cm" % P_], hl=["border"])
        elif last and "answer" in t:
            steps[i] = rect(L, W, ll, lb, note="2 × (%d + %d) = %d cm" % (L, W, P_), hl=["border"])
        elif last:
            steps[i] = rect(L, W, ll, lb, note="Perimeter = %d cm" % P_, hl=["border"])
        elif "add" in t:
            steps[i] = rect(L, W, ll, lb, note=["%d + %d = %d cm" % (L, W, half), "%d + %d is halfway round" % (L, W)],
                            hl=["length", "breadth"])
        elif "double" in t:
            steps[i] = rect(L, W, ll, lb, note=["Double %d: 2 × %d" % (half, half), "Two lengths and two breadths"], hl=["border"])
    add(q["id"], figure=rect(L, W, ll, lb, note="Perimeter = ?", hl=["border"]), steps=steps, origin="rule")


def square_perimeter_rule(q, S):
    own = q["stepByStep"]
    P_ = 4 * S
    if answer_number(q) != P_:
        raise SystemExit("%s: the key is not 4 × %s" % (q["id"], S))
    ll = "%d cm" % S
    steps = {}
    for i, s in enumerate(own):
        t = s["text"]
        if i == len(own) - 1:
            steps[i] = square4(ll, note="4 × %d = %d cm" % (S, P_))
        elif "4 equal sides" in t:
            steps[i] = square4(ll, note="4 equal sides: perimeter = 4 × %d" % S)
        elif "groups of" in t:
            steps[i] = square4(ll, note="%d + %d + %d + %d" % (S, S, S, S))
    add(q["id"], figure=R(square=True, length=ll, note="Perimeter = ?", hl=["border"]), steps=steps, origin="rule")


def run_rules():
    for q in part.questions:
        text = q["questionText"].strip()
        m = RECT_A.match(text)
        if m:
            what, L, W = m.group(1), int(m.group(2)), int(m.group(3))
        else:
            m = RECT_B.match(text)
            if m:
                L, W, what = int(m.group(1)), int(m.group(2)), m.group(3)
        if m:
            if what == "area":
                area_rule(q, L, W, False)
            else:
                rect_perimeter_rule(q, L, W)
            continue
        m = SQ_A.match(text)
        if m:
            S, what = int(m.group(1)), m.group(2)
        else:
            m = SQ_B.match(text)
            if m:
                what, S = m.group(1), int(m.group(2))
        if m:
            if what == "area":
                area_rule(q, S, S, True)
            else:
                square_perimeter_rule(q, S)


run_rules()

# ══ Drawn one by one ═════════════════════════════════════════════════════════

# ── Past papers ──────────────────────────────────────────────────────────────

add("EXT_G4_FP_2020_017",
    figure=rect(8, 6, "8 ft", "?", note="The length is 2 more than the width. Area = ?"),
    steps={
        0: rect(8, 6, "8 ft", "8 − 2 ft", note="The width is 2 less than the length", hl=["breadth"]),
        1: rect(8, 6, "8 ft", "8 − 2 ft", note="Area = length × width", hl=["length", "breadth"]),
        2: rect(8, 6, "8 ft", "8 − 2 ft", inside="48 sq ft", hl=["fill"]),
    })

add("EXT_G4_FP_2020_028",
    figure=rect(16, 12, "16 cm", "12 cm", note="The same wire is bent into a square. Side = ?"),
    steps={
        0: rect(16, 12, "16 cm", "12 cm", note=["16 + 12 = 28 cm", "16 + 12"], hl=["length", "breadth"]),
        1: rect(16, 12, "16 cm", "12 cm", note=["Whole wire = 2 × 28 cm", "Double it to get the whole wire"], hl=["border"]),
        2: R(square=True, length="?", note="56 cm shared among 4 equal sides", hl=["border"]),
        3: R(square=True, length="14 cm", note="56 ÷ 4 = 14 cm", hl=["length"]),
    })

add("EXT_G4_FP_2021_038",
    figure=rect(3, 2, "3a", "2a", note="a is the side of a square with perimeter 28 cm. Area = ?"),
    steps={
        0: R(square=True, length="a", note="4 equal sides: a = 28 ÷ 4", hl=["border"]),
        1: rect(3, 2, "21 cm", "14 cm", note="3 × 7 = 21 cm and 2 × 7 = 14 cm", hl=["length", "breadth"]),
        2: split_rect(21, 14, "breadth", 10, 4, ll="21 cm", la="10 cm", lpb="4 cm", note="21 × 10 = 210 and 21 × 4 = 84"),
        3: rect(3, 2, "21 cm", "14 cm", inside="294 cm²", note="294 is not among the choices", hl=["fill"]),
    })

add("EXT_G4_FP_2022_013",
    figure=R(square=True, length="?", note="Perimeter = 132 cm. Area = ?", hl=["border"]),
    steps={
        0: R(square=True, length="132 ÷ 4 cm", note="4 equal sides share 132 cm", hl=["length"]),
        1: split_rect(33, 33, "breadth", 30, 3, ll="33 cm", la="30 cm", note="First part: 33 × 30", hl=["a"]),
        2: split_rect(33, 33, "breadth", 30, 3, ll="33 cm", la="30 cm", lpb="3 cm", note="Second part: 33 × 3", hl=["b"]),
        4: R(square=True, length="33 cm", breadth="33 cm", inside="1089 sq cm", hl=["fill"]),
    })

add("EXT_G4_FP_2023_012",
    figure=T("equilateral", sides={"ab": "12 cm", "bc": "12 cm", "ca": "12 cm"},
             note="A square has the same perimeter. Area of the square = ?"),
    steps={
        0: T("equilateral", sides={"ab": "12 cm", "bc": "12 cm", "ca": "12 cm"},
             note=["Perimeter = 3 × 12 = 36 cm", "Perimeter = 3 × 12 cm"], hl=["ab", "bc", "ca"]),
        1: R(square=True, length="?", note="Same perimeter, shared among 4 equal sides", hl=["border"]),
        2: [R(square=True, length="9 cm", breadth="9 cm", note="Area = 9 × 9", hl=["length", "breadth"]),
            R(square=True, length="side", breadth="side", note="Area = side × side", hl=["length", "breadth"])],
        3: R(square=True, inside="81 sq.cm", hl=["fill"]),
    })

add("EXT_G4_FP_2024_011",
    figure=T("equilateral", sides={"ab": "16 cm", "bc": "16 cm", "ca": "16 cm"},
             note="A square has the same perimeter. Area of the square = ?"),
    steps={
        0: T("equilateral", sides={"ab": "16 cm", "bc": "16 cm", "ca": "16 cm"},
             note=["Perimeter = 3 × 16 = 48 cm", "Perimeter = 3 × 16 cm"], hl=["ab", "bc", "ca"]),
        1: R(square=True, length="48 ÷ 4 cm", note="48 cm shared among 4 equal sides", hl=["border"]),
        2: R(square=True, inside="144 cm.sq", note="Area = side × side", hl=["fill"]),
    })

add("EXT_G4_FP_2024_024",
    figure=R(grid=(4, 2), note="One circle fits in each square. Radius = 4 cm. Area = ?"),
    steps={
        0: C(radius="4 cm", diameter="2 × 4 cm", note="The diameter is twice the radius", hl=["diameter"]),
        1: R(grid=(4, 2), length="4 diameters", note="The length holds 4 circles side by side", hl=["length"]),
        2: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="The breadth holds 2 circles", hl=["breadth"]),
        3: R(grid=(4, 2), length="4 diameters", breadth="2 diameters", note="Area = length × breadth = 512 cm.sq", hl=["fill"]),
    })

add("EXT_G4_FP_2024_032",
    figure=rect(22, 16, "length", "breadth", note="Perimeter = 76 cm"),
    steps={
        0: rect(22, 16, "length", "breadth", note="length + breadth = 76 ÷ 2", hl=["length", "breadth"]),
        1: TABLE(["Pair", "Sum"], [["22 + 16", "38"], ["11 + 27", "38"], ["29 + 9", "38"]], note="These three all fit"),
        2: TABLE(["Pair", "Sum"], [["22 + 16", "38"], ["11 + 27", "38"], ["29 + 9", "38"], ["24 + 16", "?"]], hl=["r3"]),
        3: TABLE(["Pair", "Sum"], [["22 + 16", "38"], ["11 + 27", "38"], ["29 + 9", "38"], ["24 + 16", "40"]],
                 note="40 is not 38, so this pair does not fit", hl=["r3"]),
    })

add("EXT_G4_FP_2025_028",
    figure=rect(14, 12, "?", "12 cm", note="Perimeter = 52 cm. Area = ?"),
    steps={
        0: rect(14, 12, "?", "12 cm", note="length + breadth = 52 ÷ 2", hl=["length", "breadth"]),
        1: rect(14, 12, "?", "12 cm", note="length = half the perimeter − 12", hl=["length"]),
        2: split_rect(14, 12, "breadth", 10, 2, ll="14 cm", la="10 cm", lpb="2 cm", note="14 × 10 = 140 and 14 × 2 = 28"),
        3: rect(14, 12, "14 cm", "12 cm", inside="168 cm sq", hl=["fill"]),
    })

add("PYQ_2016_Q24",
    figure=R(grid=(4, 1), length="4 cm", breadth="1 cm", note="Cut into 4 equal squares"),
    steps={
        0: square4("1 cm", note="One square: 4 sides of 1 cm, so 4 cm", size=5),
        1: R(grid=(4, 1), length="4 cm", breadth="1 cm", note="Four squares: 4 × 4 cm"),
        2: rect(4, 1, "4 cm", "1 cm", note="Rectangle: 2 × (4 + 1) = 10 cm", hl=["border"]),
    })

add("PYQ_2018_Q39",
    figure=R(grid=(3, 1), length="3 cm", breadth="1 cm", note="Cut into 3 square pieces"),
    steps={
        0: R(grid=(3, 1), length="3 cm", breadth="1 cm", note="Each square is 4 cm round. Three squares: 3 × 4 cm"),
        1: rect(3, 1, "3 cm", "1 cm", note="Rectangle: 2 × (3 + 1) cm", hl=["border"]),
    })

add("PYQ_2016_Q29",
    steps={
        1: R(square=True, length="12 ÷ 4 cm", note="Square: 12 cm shared among 4 sides", hl=["border"]),
        2: T("equilateral", sides={"ab": "12 ÷ 3 cm"}, note="Triangle: 12 cm shared among 3 sides", hl=["ab", "bc", "ca"]),
        3: BM([{"label": "Square side", "segs": [(3, "3 cm", "a")]}, {"label": "Triangle side", "segs": [(4, "4 cm", "b")]}],
              note="More sides to share among, so each side is shorter"),
    })

add("PYQ_2017_Q21",
    figure=R(grid=(2, 1), length="length", breadth="breadth", note="The length is 2 breadths"),
    steps={
        0: P([(0, 0), (6, 0), (12, 0), (12, 6), (6, 6), (0, 6)], edges=["b"] * 6,
             note="Round the rectangle: 4 breadths and 2 more breadths", hl=["e0", "e1", "e2", "e3", "e4", "e5"]),
        1: P([(0, 0), (6, 0), (12, 0), (12, 6), (6, 6), (0, 6)], edges=["b"] * 6,
             note="Perimeter = 6 breadths, so it is a multiple of 6", hl=["e0", "e1", "e2", "e3", "e4", "e5"]),
        4: rect(46, 23, "46 cm", "23 cm", note="6 × 23 = 138 cm", hl=["border"]),
    })

add("PYQ_2017_Q35",
    figure=R(square=True, length="?", note="Perimeter = 14 cm", hl=["border"]),
    steps={
        0: square4("?", note="4 equal sides: 14 ÷ 4"),
        1: square4("3.5 cm", note="3.5 cm is 3 cm and half a centimetre"),
        3: square4("3 cm 5 mm", note="Half a centimetre is 5 mm"),
    })

add("PYQ_2019_Q30",
    figure=row_of_squares(3, note="Each square has a perimeter of 36 cm"),
    steps={
        0: R(square=True, length="?", note="One square: its equal sides share 36 cm", hl=["border"]),
        1: row_of_squares(3, top="side", left="side", note="3 sides long and 1 side wide"),
        2: row_of_squares(3, top="side", left="side", note="Perimeter = 2 × (3 sides + 1 side)",
                          hl=["e0", "e1", "e2", "e3", "e4", "e5", "e6", "e7"]),
        3: row_of_squares(3, note="Perimeter of the rectangle = 72 cm", hl=["e0", "e1", "e2", "e3", "e4", "e5", "e6", "e7"]),
    })

# ── Worksheet questions ──────────────────────────────────────────────────────

add("EXT_G4_WS2_CH20_003",
    figure=P(RECT_PTS),
    steps={
        0: A("single", [("90°", 90)], note="A right angle is a square corner"),
        1: P(RECT_PTS, right=[0, 1, 2, 3], note="Every corner of a rectangle is a square corner"),
        2: P(RECT_PTS, right=[0, 1, 2, 3], note="4 right angles"),
    })

add("EXT_G4_WS2_CH20_004",
    figure=P(QUAD_PTS, corners=["A", "B", "C", "D"]),
    steps={
        0: P(QUAD_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2)], note="A diagonal joins two opposite corners"),
        1: P(QUAD_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2), (1, 3)], note="Two opposite pairs: A and C, B and D"),
        2: P(QUAD_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2), (1, 3)], note="2 diagonals"),
    })

add("EXT_G4_WS2_CH20_005",
    figure=quad_angles(80, 90, 100, 90, ["80°", "90°", "100°", "?"]),
    steps={
        0: quad_angles(80, 90, 100, 90, ["80°", "90°", "100°", "?"], note="The four angles add up to 360°"),
        1: quad_angles(80, 90, 100, 90, ["80°", "90°", "100°", "?"], note="80° + 90° + 100°"),
        2: quad_angles(80, 90, 100, 90, ["80°", "90°", "100°", "?"], note="? = 360° − (80° + 90° + 100°)"),
        3: quad_angles(80, 90, 100, 90, ["80°", "90°", "100°", "90°"], note="The fourth angle is 90°"),
    })

# ── Hand-written: properties and names ───────────────────────────────────────

add("G4A_QUADS_001",
    figure=P(RHOMBUS_PTS, edges=["s", "s", "s", "s"], note="All four sides are equal. No corner is a right angle"),
    steps={
        1: P(SQUARE_PTS, edges=["s", "s", "s", "s"], right=[0, 1, 2, 3], note="A square has four right angles, so it does not fit"),
        2: P(RHOMBUS_PTS, edges=["s", "s", "s", "s"], note="Four equal sides, no right angles: a rhombus"),
    })

PARA70 = [(1.71, 0), (10.71, 0), (9, 4.7), (0, 4.7)]   # sides 9 and 5, bottom left angle 70°
add("G4A_QUADS_002",
    figure=P(PARA70, corners=[None, None, "?", "70°"]),
    steps={
        0: P(PARA70, corners=[None, None, "?", "70°"], note="Angles next to each other: 70° + ? = 180°", hl=["e2"]),
        1: P(PARA70, corners=[None, None, "?", "70°"], note="? = 180° − 70°", hl=["e2"]),
        2: P(PARA70, corners=[None, None, "110°", "70°"], note="70° + 110° = 180°", hl=["e2"]),
    })

add("G4A_QUADS_003",
    figure=P(RHOMBUS_PTS, edges=["?", None, None, None], note="Rhombus. Perimeter = 52 cm"),
    steps={
        0: P(RHOMBUS_PTS, edges=["side"] * 4, note="4 equal sides: 4 × side = 52 cm", hl=["e0", "e1", "e2", "e3"]),
        1: P(RHOMBUS_PTS, edges=["side"] * 4, note="side = 52 ÷ 4", hl=["e0"]),
        2: P(RHOMBUS_PTS, edges=["13 cm"] * 4, note="4 × 13 = 52 cm"),
    })

add("G4A_QUADS_009",
    steps={
        0: P(SQUARE_PTS, right=[0, 1, 2, 3], note="A square always has four right angles"),
        1: P(DIAMOND_PTS, note="A rhombus can lean over, like a diamond"),
        2: P(PARA_PTS, note="A parallelogram can lean over too"),
    })

add("G4A_QUADS_022",
    steps={
        0: P(RHOMBUS_PTS, edges=["s"] * 4, note="A leaning rhombus: four equal sides, no right angles"),
        1: P(RECT_PTS, right=[0, 1, 2, 3], note="A long rectangle: four right angles, sides not all equal"),
        2: P(KITE_PTS, edges=["short", "long", "long", "short"], note="A kite: the equal sides are next to each other"),
        3: P(RHOMBUS_PTS, edges=["s"] * 4, note="In every rhombus the opposite sides are parallel", hl=["e0", "e2"]),
    })

add("G4A_QUADS_023",
    steps={
        0: P(SQUARE_PTS, right=[0, 1, 2, 3], note="Four right angles: a square"),
        1: quad_angles(100, 100, 100, 60, ["100°", "100°", "100°", "60°"], s1=6.0, s2=6.0, note="Three obtuse angles are possible"),
        2: quad_angles(90, 90, 80, 100, ["90°", "90°", "80°", "100°"], note="Two right angles and one acute angle are possible"),
    })

add("Q_CH20_001",
    figure=P(QUAD_PTS),
    steps={
        0: P(QUAD_PTS, dashed=[(0, 2)], note="One diagonal cuts the shape into 2 triangles"),
        1: P(QUAD_PTS, dashed=[(0, 2)], note="Each triangle has 180°: 2 × 180°"),
        2: P(QUAD_PTS, note="The four angles add up to 360°"),
    })

RECT8 = [(0, 0), (6, 0), (12, 0), (12, 3.5), (12, 7), (6, 7), (0, 7), (0, 3.5)]   # corners and side midpoints
add("Q_CH20_002",
    figure=P(RECT_PTS, note="A rectangle that is not a square"),
    steps={
        0: P(RECT8, dashed=[(7, 3)], note="Fold top onto bottom: the halves match"),
        1: P(RECT8, dashed=[(7, 3), (1, 5)], note="Fold left onto right: the halves match again"),
        2: P(RECT_PTS, dashed=[(0, 2)], note="Corner to corner: the halves do not land on each other"),
        3: P(RECT8, dashed=[(7, 3), (1, 5)], note="2 axes of symmetry"),
    })

add("Q_CH20_017",
    figure=P(PARA_PTS),
    steps={
        0: P(PARA_PTS, note="Opposite sides run the same way and never meet", hl=["e0", "e2"]),
        1: P(PARA_PTS, edges=["a", "b", "a", "b"], note="Each side is as long as the side facing it"),
        2: P(PARA_PTS, edges=["a", "b", "a", "b"], note="Opposite sides are parallel and equal", hl=["e0", "e2"]),
    })

add("Q_CH20_018",
    figure=P(DIAMOND_PTS, note="A rhombus"),
    steps={
        0: P(DIAMOND_PTS, dashed=[(0, 2), (1, 3)], note="A rhombus folds onto itself in 2 ways"),
        1: P(DIAMOND_PTS, dashed=[(0, 2), (1, 3)], note="The fold lines are its two diagonals"),
    })

add("Q_CH20_019",
    steps={
        0: P(RECT_PTS, right=[0, 1, 2, 3], note="A rectangle: four right angles"),
        1: P(SQUARE_PTS, edges=["s"] * 4, right=[0, 1, 2, 3], note="A square: four right angles and four equal sides"),
        2: P(RHOMBUS_PTS, edges=["s"] * 4, note="A slanted rhombus has no right angles: not a square"),
    })

add("Q_CH20_020",
    figure=P(TRAP_PTS, note="Exactly one pair of parallel sides", hl=["e0", "e2"]),
    steps={
        0: P(PARA_PTS, note="A parallelogram has two pairs of parallel sides", hl=["e0", "e2"]),
        1: P(KITE_PTS, note="A kite usually has no parallel sides at all"),
        2: P(TRAP_PTS, note="One pair of parallel sides; the other two are not", hl=["e0", "e2"]),
    })

add("Q_CH20_021",
    figure=P(KITE_PTS, note="A kite"),
    steps={
        0: P(KITE_PTS, edges=["short", "long", "long", "short"], note="Two short sides together, two long sides together"),
        1: P(KITE_PTS, edges=["short", "long", "long", "short"], dashed=[(0, 2)], note="Fold along this line: one half lands on the other"),
        2: P(KITE_PTS, edges=["short", "long", "long", "short"], dashed=[(1, 3)], note="This fold puts a short side on a long side"),
        3: P(KITE_PTS, dashed=[(0, 2)], note="1 axis of symmetry"),
    })

add("Q_CH20_022",
    figure=quad_angles(90, 85, 110, 75, ["90°", "85°", "110°", "?"]),
    steps={
        0: quad_angles(90, 85, 110, 75, ["90°", "85°", "110°", "?"], note="The four angles add up to 360°"),
        1: quad_angles(90, 85, 110, 75, ["90°", "85°", "110°", "?"], note="90° + 85° + 110°"),
        2: quad_angles(90, 85, 110, 75, ["90°", "85°", "110°", "?"], note="? = 360° − (90° + 85° + 110°)"),
        3: quad_angles(90, 85, 110, 75, ["90°", "85°", "110°", "75°"], note="The fourth angle is 75°"),
    })

add("Q_CH20_025",
    figure=P(SQUARE_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2), (1, 3)], note="The diagonals AC and BD"),
    steps={
        0: P(SQUARE_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2), (1, 3)], note="Like a rectangle: AC and BD are equal"),
        1: P(SQUARE_PTS, corners=["A", "B", "C", "D"], dashed=[(0, 2), (1, 3)], note="Like a rhombus: they cut each other in half at 90°"),
    })

# ── Hand-written: perimeter and area ─────────────────────────────────────────

add("G4A_QUADS_004",
    figure=R(square=True, length="25 cm", note="Lace all around the edge: ₹3 for every centimetre", hl=["border"]),
    steps={
        0: square4("25 cm", note="Lace = 25 + 25 + 25 + 25 = 100 cm"),
        1: square4("25 cm", note="100 cm at ₹3 each: 100 × 3 = ₹300"),
    })

add("G4A_QUADS_005",
    figure=R(square=True, length="18 cm", note="The same wire makes a rectangle: length = 2 × breadth"),
    steps={
        0: square4("18 cm", note="Wire = 18 + 18 + 18 + 18 = 72 cm"),
        1: P([(0, 0), (6, 0), (12, 0), (12, 6), (6, 6), (0, 6)], edges=["b"] * 6,
             note="Round the rectangle: 6 breadths = 72 cm", hl=["e0", "e1", "e2", "e3", "e4", "e5"]),
        2: rect(2, 1, "2 × 12 cm", "12 cm", note="72 ÷ 6 = 12 cm for the breadth", hl=["length"]),
        3: rect(2, 1, "2 × 12 cm", "12 cm", note="Area = length × breadth", hl=["length", "breadth"]),
        4: rect(2, 1, "2 × 12 cm", "12 cm", inside="288 cm²", hl=["fill"]),
    })

add("G4A_QUADS_006",
    figure=strip_frame(24, 18, 2, lwidth="2 m", lmid_top="20 m", lmid_left="14 m", note="Garden inside, path all around. Area of the path = ?"),
    steps={
        0: strip_frame(24, 18, 2, lwidth="2 m", lmid_top="20 m", lmid_left="14 m",
                       note="2 m on each side: add 4 m to the length and to the width"),
        1: rect(24, 18, "20 + 4 m", "14 + 4 m", note="Garden with the path: 432 m²", hl=["fill"]),
        2: rect(20, 14, "20 m", "14 m", note="Garden alone: 20 × 14", hl=["fill"]),
        3: strip_frame(24, 18, 2, lwidth="2 m", lmid_top="20 m", lmid_left="14 m", note="Path = 432 − (20 × 14) = 152 m²"),
    })

add("G4A_QUADS_007",
    figure=rect(6, 4, "6 m", "4 m", note="Square tiles of side 50 cm cover the floor"),
    steps={
        0: R(grid=(12, 1), length="6 m", note="Two tiles make 1 m, so 6 × 2 tiles along the length"),
        1: rect(6, 4, "6 m", "4 m", note="4 × 2 rows of tiles along the 4 m width", hl=["breadth"]),
        2: rect(6, 4, "6 m", "4 m", note="Tiles = tiles in a row × number of rows", hl=["fill"]),
        3: rect(6, 4, "6 m", "4 m", inside="96 tiles", hl=["fill"]),
    })

HALVED = [(0, 0), (6, 0), (12, 0), (12, 12), (6, 12), (0, 12)]
add("G4A_QUADS_008",
    figure=P(HALVED, edges=[None, None, None, None, None, "12 cm"], dashed=[(1, 4)], note="One straight cut makes two equal rectangles"),
    steps={
        0: P(HALVED, edges=["half of 12 cm", None, None, None, None, "12 cm"], dashed=[(1, 4)],
             note="Each rectangle: 12 cm long, half of 12 cm wide", hl=["e0", "e5"]),
        1: P(HALVED, edges=["half of 12 cm", None, None, None, None, "12 cm"], dashed=[(1, 4)],
             note="Add the four sides of one rectangle", hl=["e0", "e4", "e5"]),
        2: P(HALVED, edges=["half of 12 cm", None, None, None, None, "12 cm"], dashed=[(1, 4)],
             note="Perimeter of each rectangle = 36 cm", hl=["e0", "e4", "e5"]),
    })

add("G4A_QUADS_010",
    figure=rect(20, 15, "20 cm", "15 cm", note="Length 5 cm longer, width 5 cm shorter. Area?"),
    steps={
        0: rect(20, 15, "20 cm", "15 cm", note="Area at the start: 20 × 15", hl=["fill"]),
        1: rect(25, 10, "20 + 5 cm", "15 − 5 cm", note="New length and new width", hl=["length", "breadth"]),
        2: rect(25, 10, "25 cm", "10 cm", note="New area: 25 × 10", hl=["fill"]),
    })

add("G4A_QUADS_011",
    figure=rect(12, 9, "12 m", "9 m", note="Carpet ₹150 per sq m. Wall strip ₹40 per m"),
    steps={
        0: rect(12, 9, "12 m", "9 m", note="Carpet covers the floor: 12 × 9 sq m, at ₹150 each", hl=["fill"]),
        1: rect(12, 9, "12 m", "9 m", note="Strip goes round: 2 × (12 + 9) m, at ₹40 each", hl=["border"]),
    })

add("G4A_QUADS_012",
    figure=rect(30, 20, "30 m", "20 m", note="A post every 5 m, with one at each corner", hl=["border"]),
    steps={
        0: rect(30, 20, "30 m", "20 m", note="Distance around: 2 × (30 + 20) = 100 m", hl=["border"]),
        1: rect(30, 20, "30 m", "20 m", note="Gaps of 5 m: 100 ÷ 5 = 20 gaps", hl=["border"]),
    })

add("G4A_QUADS_013",
    steps={
        1: rect(19, 1, "19 cm", "1 cm", note="Thinnest: 19 × 1 = 19 sq cm"),
        2: rect(11, 9, "11 cm", "9 cm", note="Closest sides: 11 × 9 = 99 sq cm", hl=["fill"]),
    })

add("G4A_QUADS_014",
    figure=R(square=True, length="15 cm", note="Same wire, new rectangle: length 4 cm more than 15 cm"),
    steps={
        0: square4("15 cm", note="Wire = 15 + 15 + 15 + 15 = 60 cm"),
        1: rect(19, 11, "19 cm", "?", note="Length + breadth = half of 60 cm", hl=["length", "breadth"]),
        3: R(square=True, length="15 cm", breadth="15 cm", note="Square: 15 × 15", hl=["fill"]),
    })

# The park, with the two paths marked by dashed lines. 30 by 20, paths 2 wide.
_s = 12.0 / 30
_X, _Y, _w = 12.0, 20 * _s, 2 * _s
CROSS = [(0, 0), (_X / 2 - _w / 2, 0), (_X / 2 + _w / 2, 0), (_X, 0), (_X, _Y / 2 - _w / 2), (_X, _Y / 2 + _w / 2),
         (_X, _Y), (_X / 2 + _w / 2, _Y), (_X / 2 - _w / 2, _Y), (0, _Y), (0, _Y / 2 + _w / 2), (0, _Y / 2 - _w / 2)]
CROSS_DASH = [(1, 8), (2, 7), (11, 4), (10, 5)]
CROSS_EDGES = [None, "2 m", None, None, None, None, None, None, None, None, "2 m", None]
add("G4A_QUADS_015",
    figure=P(CROSS, edges=CROSS_EDGES, dashed=CROSS_DASH, note="Park 30 m by 20 m. Two paths cross in the middle"),
    steps={
        0: P(CROSS, edges=CROSS_EDGES, dashed=CROSS_DASH, note="Path along the length: 30 × 2", hl=["e10", "e4"]),
        1: P(CROSS, edges=CROSS_EDGES, dashed=CROSS_DASH, note="Path across the width: 20 × 2", hl=["e1", "e7"]),
        2: P(CROSS, edges=CROSS_EDGES, dashed=CROSS_DASH, note="The middle square, 2 × 2, belongs to both paths"),
        3: P(CROSS, edges=CROSS_EDGES, dashed=CROSS_DASH, note="30 × 2 + 20 × 2 − 2 × 2 = 96 sq m"),
    })

add("G4A_QUADS_016",
    figure=strip_frame(11, 11, 1, lwidth="1 m", lmid_top="?", note="Path all around a square garden. Path area = 40 sq m"),
    steps={
        0: strip_frame(11, 11, 1, lwidth="1 m", lmid_top="?", note="Each corner of the path is a square, 1 m by 1 m", hl=["e0", "e2", "e5", "e8"]),
        1: strip_frame(11, 11, 1, lwidth="1 m", lmid_top="?", note="Take the corners from 40 sq m: the four strips are left",
                       hl=["e1", "e4", "e7", "e10"]),
        2: strip_frame(11, 11, 1, lwidth="1 m", lmid_top="?", note="Each strip has the same area", hl=["e1"]),
        3: strip_frame(11, 11, 1, lwidth="1 m", lmid_top="9 m", note="9 sq m and 1 m wide, so the strip is 9 m long", hl=["e1"]),
    })

add("G4A_QUADS_017",
    figure=R(length="length", breadth="breadth", inside="24 sq cm", note="Length × 2 and breadth × 3. New area = ?"),
    steps={
        0: rect(6, 4, "6 cm", "4 cm", inside="24 sq cm", note="Try 6 cm by 4 cm"),
        1: R(length="6 × 2 cm", breadth="4 × 3 cm", prop=1, note="Length 2 times as long, breadth 3 times as long",
             hl=["length", "breadth"]),
        2: R(length="12 cm", breadth="12 cm", prop=1, inside="144 sq cm", hl=["fill"]),
    })

_k = 12.0 / 13
GROW_L = [(0, 0), (10 * _k, 0), (12, 0), (12, 7 * _k), (10 * _k, 7 * _k), (0, 7 * _k)]
_j = 12.0 / 10
GROW_B = [(0, 0), (12, 0), (12, 7 * _j), (12, 9 * _j), (0, 9 * _j), (0, 7 * _j)]
add("G4A_QUADS_018",
    figure=P(GROW_L, edges=[None, "3 cm", None, None, None, None], dashed=[(1, 4)], note="3 cm longer: the extra strip is 21 sq cm"),
    steps={
        0: P(GROW_L, edges=[None, "3 cm", "21 ÷ 3 cm", None, None, None], dashed=[(1, 4)],
             note="Strip of 21 sq cm, 3 cm wide: breadth = 21 ÷ 3", hl=["e2"]),
        1: P(GROW_B, edges=["20 ÷ 2 cm", None, "2 cm", None, None, None], dashed=[(2, 5)],
             note="Strip of 20 sq cm, 2 cm wide: length = 20 ÷ 2", hl=["e0"]),
        2: rect(10, 7, "10 cm", "7 cm", note="The rectangle is 10 cm long and 7 cm wide"),
        3: rect(10, 7, "10 cm", "7 cm", note="Perimeter = 2 × (10 + 7) = 34 cm", hl=["border"]),
    })

add("G4A_QUADS_019",
    figure=GRID(4, 9, note="One way to use all 36 tiles: 4 by 9"),
    steps={
        0: GRID(4, 9, note="The two sides multiply to give 36: 4 × 9 = 36"),
        2: GRID(6, 6, note="6 by 6 is a square. After this the pairs repeat"),
        3: TABLE(["Side", "Side"], [["1", "36"], ["2", "18"], ["3", "12"], ["4", "9"], ["6", "6"]], note="Each pair multiplies to 36"),
    })

add("G4A_QUADS_020",
    figure=GRID(3, 3),
    steps={
        0: GRID(3, 3, note="Small squares: 3 rows of 3, which is 9"),
        1: GRID(3, 3, shaded=[(0, 0), (0, 1), (1, 0), (1, 1)], note="A 2 by 2 block: 2 places across and 2 places down"),
        2: GRID(3, 3, shaded=[(r, c) for r in range(3) for c in range(3)], note="1 square is the whole 3 by 3 board"),
    })

add("G4A_QUADS_021",
    figure=row_of_squares(5),
    steps={
        0: row_of_squares(5, note="1 small square on its own is a square: not counted", hl=["e0"]),
        1: row_of_squares(5, note="2 squares long: 4 of them. 3 squares long: 3 of them", hl=["e0", "e1"]),
        2: row_of_squares(5, note="4 squares long: 2 of them. The whole strip: 1", hl=["e0", "e1", "e2", "e3"]),
        3: row_of_squares(5, note="4 + 3 + 2 + 1 = 10"),
    })

STRIPS = [(0, 0), (3, 0), (6, 0), (9, 0), (12, 0), (12, 12), (9, 12), (6, 12), (3, 12), (0, 12)]
STRIPS_DASH = [(1, 8), (2, 7), (3, 6)]
add("G4A_QUADS_024",
    figure=P(STRIPS, dashed=STRIPS_DASH, note="4 equal strips. Each strip has a perimeter of 40 cm"),
    steps={
        0: P(STRIPS, dashed=STRIPS_DASH, note="One strip: long side + short side = 40 ÷ 2", hl=["e0", "e9"]),
        1: BM([{"segs": [(1, "short", "a")] * 4 + [(1, "short", "b")], "brace": "20 cm"}],
              note="Long side = 4 short sides, so 20 cm is 5 equal parts"),
        2: P(STRIPS, edges=["4 cm", None, None, None, None, None, None, None, None, "4 × 4 cm"], dashed=STRIPS_DASH,
             note="The long side of a strip is the side of the square", hl=["e9"]),
        3: R(square=True, inside="256 sq cm", note="Area = side × side", hl=["fill"]),
    })

add("G4A_QUADS_025",
    figure=R(grid=(3, 1), length="length", breadth="breadth", note="The length is 3 times the breadth"),
    steps={
        0: R(grid=(3, 1), length="3 × breadth", breadth="breadth", note="Area = 3 equal squares, each breadth × breadth"),
        1: R(grid=(3, 1), length="3 × breadth", breadth="breadth", note="Divide each area by 3 to get one square"),
        2: R(grid=(3, 1), length="3 × breadth", breadth="breadth", note="Only 25 is a number multiplied by itself", hl=["breadth"]),
        3: R(grid=(3, 1), length="15 cm", breadth="5 cm", note="Breadth 5 cm, length 15 cm"),
        4: R(grid=(3, 1), length="15 cm", breadth="5 cm", note="Area = 75 sq cm", hl=["fill"]),
    })

NOTCH = [(0, 0), (6, 0), (6, 4), (10, 4), (10, 10), (0, 10)]
add("G4A_QUADS_026",
    figure=P(NOTCH, edges=[None, "4 cm", "4 cm", None, "10 cm", "10 cm"], note="A 4 cm square is cut from one corner. Perimeter = ?"),
    steps={
        0: P(NOTCH, edges=[None, "4 cm", "4 cm", None, "10 cm", "10 cm"], note="Two edges are still 10 cm long", hl=["e4", "e5"]),
        1: P(NOTCH, edges=["10 − 4 cm", "4 cm", "4 cm", "10 − 4 cm", "10 cm", "10 cm"], note="Two edges are now shorter", hl=["e0", "e3"]),
        2: P(NOTCH, edges=["10 − 4 cm", "4 cm", "4 cm", "10 − 4 cm", "10 cm", "10 cm"], note="The notch adds two new edges of 4 cm", hl=["e1", "e2"]),
        3: P(NOTCH, edges=["10 − 4 cm", "4 cm", "4 cm", "10 − 4 cm", "10 cm", "10 cm"], note="Add all six edges: 40 cm",
             hl=["e0", "e1", "e2", "e3", "e4", "e5"]),
    })

add("Q_CH14_022",
    figure=rect(13, 8, "13 cm", "?", note="Perimeter = 42 cm"),
    steps={
        0: rect(13, 8, "13 cm", "?", note="length + breadth = 42 ÷ 2", hl=["length", "breadth"]),
        1: rect(13, 8, "13 cm", "?", note="breadth = half the perimeter − 13", hl=["breadth"]),
        2: rect(13, 8, "13 cm", "8 cm", note="Check: 13 + 8 = 21, and twice 21 is 42", hl=["border"]),
    })

add("Q_CH20_003",
    figure=R(square=True, length="11 cm", note="Perimeter = ?", hl=["border"]),
    steps={
        0: square4("11 cm", note="4 equal sides: perimeter = 4 × 11"),
        1: square4("11 cm", note="11 + 11 + 11 + 11 = 4 × 11"),
        2: square4("11 cm", note="Perimeter = 44 cm"),
    })

add("Q_CH20_004",
    figure=R(square=True, length="9 m", inside="Area = ?"),
    steps={
        0: R(square=True, grid=(9, 9), length="9 m", breadth="9 m", note="9 rows of 9 unit squares"),
        1: R(square=True, grid=(9, 9), length="9 m", breadth="9 m", note="Each small square is 1 sq. m, so area is in sq. m"),
        2: R(square=True, length="9 m", breadth="9 m", inside="81 sq. m", hl=["fill"]),
    })

add("Q_CH20_005",
    figure=rect(12, 7, "12 cm", "7 cm", note="Perimeter = ?", hl=["border"]),
    steps={
        0: rect(12, 7, "12 cm", "7 cm", note="12 + 7 = 19 cm", hl=["length", "breadth"]),
        1: rect(12, 7, "12 cm", "7 cm", note="Two lengths and two breadths: double 19", hl=["border"]),
        2: rect(12, 7, "12 cm", "7 cm", note="Perimeter = 38 cm", hl=["border"]),
    })

add("Q_CH20_006",
    figure=rect(15, 8, "15 cm", "8 cm", inside="Area = ?"),
    steps={
        0: rect(15, 8, "15 cm", "8 cm", note="Area = 15 × 8", hl=["length", "breadth"]),
        1: split_rect(15, 8, "length", 10, 5, lb="8 cm", la="10 cm", lpb="5 cm", note="10 × 8 = 80 and 5 × 8 = 40, and 80 + 40 = 120"),
        2: rect(15, 8, "15 cm", "8 cm", inside="120 cm²", hl=["fill"]),
    })

add("Q_CH20_007",
    steps={
        1: R(square=True, grid=(8, 8), length="8", note="Perimeter 4 × 8 = 32, area 8 × 8 = 64: not equal"),
        2: R(square=True, grid=(6, 6), length="6", note="Perimeter 4 × 6 = 24, area 6 × 6 = 36: not equal"),
        3: R(square=True, grid=(4, 4), length="4", note="Perimeter 16 and area 16: equal"),
    })

add("Q_CH20_008",
    figure=rect(10.5, 5.5, "length", "breadth", note="Perimeter = 32 m"),
    steps={
        0: rect(10.5, 5.5, "length", "breadth", note="length + breadth = 32 ÷ 2", hl=["length", "breadth"]),
        1: TABLE(["Pair", "Sum"], [["18 + 14", "32"]], note="That is the whole perimeter, not half: too big", hl=["r0"]),
        2: TABLE(["Pair", "Sum"], [["18 + 14", "32"], ["8 + 7", "15"]], note="15 is 1 short of 16", hl=["r1"]),
        3: TABLE(["Pair", "Sum"], [["18 + 14", "32"], ["8 + 7", "15"], ["10.5 + 5.5", "16"]], note="This pair adds to 16: it fits", hl=["r2"]),
    })

add("Q_CH20_009",
    figure=R(length="2m + 5n", breadth="m − 3n", note="Perimeter = ?", hl=["border"]),
    steps={
        0: R(length="2m + 5n", breadth="m − 3n", note="(2m + 5n) + (m − 3n) = 3m + 2n", hl=["length", "breadth"]),
        1: R(length="2m + 5n", breadth="m − 3n", note="2 × (3m + 2n) = 6m + 4n", hl=["border"]),
    })

add("Q_CH20_010",
    figure=R(length="(3a − 5) cm", breadth="(a + 5) cm", prop=1, note="Perimeter = 40 cm"),
    steps={
        0: R(length="(3a − 5) cm", breadth="(a + 5) cm", prop=1, note="(3a − 5) + (a + 5) = 4a", hl=["length", "breadth"]),
        1: R(length="(3a − 5) cm", breadth="(a + 5) cm", prop=1, note="2 × 4a = 8a = 40", hl=["border"]),
        2: R(length="10 cm", breadth="10 cm", prop=1, note="a = 5 makes both sides 10 cm"),
    })

add("Q_CH20_011",
    figure=rect(350, 120, "350 m", "120 m", note="Ten rounds of the field = ?", hl=["border"]),
    steps={
        0: rect(350, 120, "350 m", "120 m", note="350 + 120", hl=["length", "breadth"]),
        1: rect(350, 120, "350 m", "120 m", note="One full round = 940 m", hl=["border"]),
        2: rect(350, 120, "350 m", "120 m", note="Ten rounds: 10 × 940 m", hl=["border"]),
    })

add("Q_CH20_012",
    figure=BM([{"label": "Length", "segs": [(5, None, "a"), (2, "2 cm", "b")]}, {"label": "Breadth", "segs": [(5, None, "a")]}],
              note="Length + breadth = 12 cm. They differ by 2 cm"),
    steps={
        0: BM([{"label": "Length", "segs": [(5, None, "a"), (2, "2 cm", "b")]}, {"label": "Breadth", "segs": [(5, None, "a")]}],
              note="Take away the 2 cm: 12 − 2 = 10 cm is two breadths", hl=["b0s0", "b1s0"]),
        1: BM([{"label": "Length", "segs": [(5, "10 ÷ 2", "a"), (2, "2 cm", "b")]}, {"label": "Breadth", "segs": [(5, "10 ÷ 2", "a")]}],
              note="Halve 10 cm to get the breadth", hl=["b1s0"]),
        2: BM([{"label": "Length", "segs": [(5, "breadth", "a"), (2, "2 cm", "b")]}, {"label": "Breadth", "segs": [(5, "breadth", "a")]}],
              note="The length is 2 cm more than the breadth", hl=["b0"]),
        3: rect(7, 5, "7 cm", "5 cm", note="7 + 5 = 12. Area = 7 × 5", hl=["length", "breadth"]),
        4: rect(7, 5, "7 cm", "5 cm", inside="35 cm²", hl=["fill"]),
    })

add("Q_CH20_013",
    steps={
        0: square4("5.5 cm", note="Square: 4 sides of 5.5 cm, so 22 cm"),
        1: T("equilateral", sides={"ab": "6 cm", "bc": "6 cm", "ca": "6 cm"}, note="Triangle: 3 sides of 6 cm, so 18 cm", hl=["ab", "bc", "ca"]),
        2: rect(5, 3, "5 cm", "3 cm", note="Rectangle: two of 5 cm and two of 3 cm, so 16 cm", hl=["border"]),
        3: P(RHOMBUS_PTS, edges=["5 cm"] * 4, note="Rhombus: 4 sides of 5 cm, so 20 cm", hl=["e0", "e1", "e2", "e3"]),
        4: CHART([("Square", 22), ("Triangle", 18), ("Rectangle", 16), ("Rhombus", 20)], unit="cm", note="The smallest is 16 cm", hl=["b2"]),
    })

add("Q_CH20_014",
    figure=R(square=True, length="6 cm", note="An equilateral triangle has the same perimeter. Its side = ?"),
    steps={
        0: square4("6 cm", note="Square: 4 × 6 = 24 cm"),
        1: T("equilateral", sides={"ab": "s", "bc": "s", "ca": "s"}, note="Triangle: 3 × s = 24", hl=["ab", "bc", "ca"]),
        2: T("equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"}, note="s = 24 ÷ 3 = 8 cm"),
    })

add("Q_CH20_015",
    figure=rect(16, 4, "16 cm", "4 cm", note="A square has the same area. Perimeter of the square = ?"),
    steps={
        0: rect(16, 4, "16 cm", "4 cm", note="Area = 16 × 4 = 64 square cm", hl=["fill"]),
        1: R(square=True, grid=(8, 8), length="8 cm", breadth="8 cm", note="8 × 8 = 64, so the side is 8 cm"),
        2: square4("8 cm", note="Perimeter = 4 × 8 = 32 cm"),
    })

add("Q_CH20_016",
    figure=rect(16, 4, "16 cm", "4 cm", note="A square has the same perimeter. Area of the square = ?"),
    steps={
        0: rect(16, 4, "16 cm", "4 cm", note="Perimeter = 2 × (16 + 4)", hl=["border"]),
        1: square4("?", note="40 cm shared among 4 equal sides: 10 cm each"),
        2: R(square=True, length="10 cm", breadth="10 cm", note="Area = 10 × 10", hl=["length", "breadth"]),
        3: R(square=True, length="10 cm", breadth="10 cm", inside="100 sq. cm", hl=["fill"]),
    })

add("Q_CH20_023",
    figure=R(square=True, length="?", inside="144 cm²"),
    steps={
        0: R(square=True, length="?", breadth="?", inside="144 cm²", note="side × side = 144", hl=["length", "breadth"]),
        2: R(square=True, grid=(12, 12), length="12 cm", breadth="12 cm", note="12 rows of 12 unit squares: 12 × 12 = 144"),
        3: R(square=True, length="12 cm", breadth="12 cm", inside="144 cm²", hl=["length"]),
    })

add("Q_CH20_024",
    figure=rect(12, 8, "12 cm", "?", inside="96 cm²"),
    steps={
        0: rect(12, 8, "12 cm", "?", inside="96 cm²", note="12 × breadth = 96", hl=["length", "breadth"]),
        1: rect(12, 8, "12 cm", "?", inside="96 cm²", note="breadth = 96 ÷ 12", hl=["breadth"]),
        2: R(grid=(12, 8), length="12 cm", breadth="8 cm", note="Check: 12 × 8 = 96"),
    })


if __name__ == "__main__":
    part.build()
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        part.show(set(sys.argv[2:]))
    part.report()
    print("wrote %s" % part.path)
