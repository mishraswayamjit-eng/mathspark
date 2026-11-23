"""Figures for Grade 4 "Squares & Square Roots" (gr4_squares).

    python -X utf8 scripts/figures/authoring/g4_gr4_squares.py            # build the part file
    python -X utf8 scripts/figures/authoring/g4_gr4_squares.py --review   # also print every figure against its question

Writes data/question-figures/parts/g4-gr4_squares.json.

By rule: "Find the square root of N." and "Find the square of N." (numbers read from the question).
Everything else is drawn one question at a time. A square number is drawn as a real square of unit
squares whenever its side is 12 or less (the largest grid the contract allows); bigger squares are
a plain square with its side labelled.
"""
import re
import sys

from g4_gr4_numbers_lib import Part, table, line, grid, bm, bar, seg, ftree, step_texts, answer

P = Part("gr4_squares")


def box(inside=None, side=None, note=None, hl=None):
    """A square with the same label on both sides."""
    fig = {"kind": "rectangle", "square": True}
    if side:
        fig["length"] = side
        fig["breadth"] = side
    if inside:
        fig["inside"] = inside
    if note:
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def new_layer(n):
    """The L-shaped strip that grows an n by n square into an (n + 1) by (n + 1) square."""
    return [(r, n) for r in range(n + 1)] + [(n, c) for c in range(n)]


def layers(n, which):
    """Cells of the L-shaped layers `which` (layer k holds the 2k + 1 cells with max(row, col) = k)."""
    return [(r, c) for r in range(n) for c in range(n) if max(r, c) in which]


def block(rows, cols):
    return [(r, c) for r in range(rows) for c in range(cols)]


def border(n):
    return [(r, c) for r in range(n) for c in range(n) if r in (0, n - 1) or c in (0, n - 1)]


# ── Rules ────────────────────────────────────────────────────────────────────
ROOT_Q = re.compile(r"^Find the square root of (\d+)\.$")
SQUARE_Q = re.compile(r"^Find the square of (\d+)\.$")


def rule_root(q):
    m = ROOT_Q.match(q["questionText"])
    if not m:
        return False
    n, root = int(m.group(1)), int(answer(q))
    assert root * root == n
    texts = step_texts(q)
    before = box("%d squares" % n, "?", "A square made of %d small squares: how many in each row?" % n)
    last = len(texts) - 1
    if root <= 12:
        final = grid(root, root, note="%d × %d = %d, so the square root is %d" % (root, root, n, root))
    else:
        final = box("%d squares" % n, str(root), "%d × %d = %d, so the square root is %d" % (root, root, n, root))
    steps = {last: final}
    # A step that tries a smaller number ("3 × 3 = 9 is too small") shows that smaller square.
    for i, t in enumerate(texts[:last]):
        trial = re.search(r"(\d+) × (\d+) = (\d+) is too small", t)
        if trial and trial.group(1) == trial.group(2) and int(trial.group(1)) <= 12:
            side = int(trial.group(1))
            steps[i] = grid(side, side, note="%s is too small for %d" % (trial.group(0)[:-len(" is too small")], n))
    P.add(q, before, steps, origin="rule")
    return True


def rule_square(q):
    m = SQUARE_Q.match(q["questionText"])
    if not m:
        return False
    n = int(m.group(1))
    texts = step_texts(q)
    before = box("?", str(n), "%d rows with %d in each row" % (n, n))
    steps = {}
    for i, t in enumerate(texts):
        parts = re.findall(r"(\d+ × \d+) = (\d+)", t)
        if len(parts) == 2:
            steps[i] = table([list(p) for p in parts], note="Split the square into two easier parts")
    steps[len(texts) - 1] = box(answer(q), str(n), "The square of %d is %s" % (n, answer(q)))
    P.add(q, before, steps, origin="rule")
    return True


for _q in P.qs:
    rule_root(_q) or rule_square(_q)


# ── Individually drawn ───────────────────────────────────────────────────────
A = P.add

A("G4A_SQUARES_001",
  grid(12, 12, note="12 rows of 12: how many small squares?"),
  {1: grid(12, 12, [(r, c) for r in range(12) for c in (10, 11)], "12 × 10 = 120 and 12 × 2 = 24"),
   2: grid(12, 12, note="120 + 24 = 144")})
A("G4A_SQUARES_002", None, {2: grid(8, 8, note="64 is 8 × 8, so 64 makes a square")})
A("G4A_SQUARES_003",
  box("81 squares", "?", "The same number in every row and every column"),
  {1: grid(9, 9, note="9 × 9 = 81 fits"),
   2: grid(9, 9, [(0, c) for c in range(9)], "9 small squares in each row")})
A("G4A_SQUARES_005",
  box("49 squares", None, "What is the next bigger square?"),
  {0: grid(7, 7, note="49 is 7 × 7"),
   2: grid(8, 8, new_layer(7), "One more row and column: 8 × 8 = 64")})
A("G4A_SQUARES_006",
  grid(11, 11, note="11 rows with 11 saplings in each row"),
  {1: grid(11, 11, [(r, 10) for r in range(11)], "11 × 10 = 110, and one more 11 makes 121"),
   2: grid(11, 11, note="Ravi plants 121 saplings")})
A("G4A_SQUARES_009", None, {
    0: grid(9, 9, note="9 × 9 = 81 has two digits"),
    1: grid(10, 10, note="10 × 10 = 100 has three digits")})
A("G4A_SQUARES_010", None, {
    0: grid(5, 5, note="5 × 5 = 25 is the square just below 30"),
    2: grid(5, 6, [(r, 5) for r in range(5)], "30 − 25 = 5 must be taken away")})
A("G4A_SQUARES_012",
  grid(6, 6, note="The square of 6"),
  {0: grid(6, 6, note="6 × 6 = 36"),
   1: grid(6, 6, [(0, c) for c in range(6)], "Take 6 away: 36 − 6 = 30")})
_sq13 = [(64, "64"), (81, "81"), (100, "100"), (121, "121"), (144, "144")]
A("G4A_SQUARES_013",
  line(50, 150, 10, ticks="ends", note="Which perfect squares lie between 50 and 150?"),
  {0: line(50, 150, 10, points=_sq13[:1], ticks="ends", note="7 × 7 = 49 is just below 50, so start at 8 × 8 = 64"),
   1: line(50, 150, 10, points=_sq13, ticks="ends"),
   3: line(50, 150, 10, points=_sq13, ticks="ends", note="5 perfect squares lie between 50 and 150")})
A("G4A_SQUARES_015",
  grid(10, 10, block(6, 6), "A 10 by 10 square with a 6 by 6 square shaded inside it"),
  {0: grid(10, 10, note="10 × 10 = 100"),
   1: grid(10, 10, block(6, 6), "The shaded square is 6 × 6 = 36"),
   2: grid(10, 10, block(6, 6), "100 − 36 = 64 squares are not shaded")})
A("G4A_SQUARES_016", None, {
    2: grid(6, 6, layers(6, (0, 2, 4)), "36 is 6 × 6"),
    3: grid(6, 6, layers(6, (0, 2, 4)), "Each L-shape adds the next odd number: 1, 3, 5, 7, 9, 11")})
A("G4A_SQUARES_017", None, {
    0: grid(12, 12, note="12 × 12 = 144"),
    1: grid(12, 12, note="13 × 13 = 169 is too many, so the square uses 144 children"),
    2: grid(12, 12, note="150 − 144 = 6 children are left out")})
A("G4A_SQUARES_018", None, {
    0: line(190, 230, 5, points=[(196, "196"), (200, None)], ticks="none", note="14 × 14 = 196 cannot hold all 200 plants"),
    1: line(190, 230, 5, points=[(200, "200"), (225, "225")], ticks="none", note="15 × 15 = 225 is the first square above 200"),
    2: line(190, 230, 5, points=[(200, "200"), (225, "225")], hops=[(200, 225, "+25")], ticks="none", hl=["h0"])})
A("G4A_SQUARES_020",
  box("441 soldiers", "?", "Every soldier in the front row holds a flag"),
  {2: box("441 soldiers", "21", "21 × 21 = 441"),
   3: box("441 soldiers", "21", "The front row has 21 soldiers, so there are 21 flags", hl=["length"])})
A("G4A_SQUARES_021", None, {
    2: line(140, 170, 5, points=[(144, "144"), (164, "164"), (169, "169")], ticks="none", hl=["p1"],
            note="164 falls between the squares 144 and 169")})
A("G4A_SQUARES_025",
  box("64 tiles", None, "How many more tiles make the next bigger square?"),
  {0: grid(8, 8, note="64 is 8 × 8"),
   1: grid(9, 9, new_layer(8), "The next square is 9 × 9 = 81"),
   2: grid(9, 9, new_layer(8), "81 − 64 = 17 more tiles")})
A("G4A_SQUARES_030", None, {
    0: line(950, 1030, 10, points=[(961, "961"), (1000, "1000"), (1024, "1024")], ticks="none",
            note="31 × 31 = 961 and 32 × 32 = 1024"),
    1: line(950, 1030, 10, points=[(961, "961"), (1000, "1000"), (1024, "1024")], ticks="none", hl=["p0"],
            note="961 is the largest perfect square below 1000"),
    2: line(950, 1030, 10, points=[(961, "961"), (1000, "1000")], hops=[(1000, 961, "−39")], ticks="none", hl=["h0"])})
A("G4A_SQUARES_031", None, {
    0: line(225, 256, 1, points=[(225, "225"), (256, "256")], ticks="none", note="15 × 15 = 225 and 16 × 16 = 256"),
    2: line(225, 256, 1, points=[(225, None), (226, "226"), (255, "255"), (256, None)], ticks="none",
            note="The numbers in between run from 226 to 255")})
A("G4A_SQUARES_032", None, {
    1: line(140, 170, 5, points=[(144, "144"), (169, "169")], hops=[(144, 169, "25")], ticks="none",
            note="12 × 12 = 144 and 13 × 13 = 169 are 25 apart"),
    2: line(140, 170, 5, points=[(144, "144"), (169, "169")], hops=[(144, 149, "+5")], ticks="none",
            note="He has 5 more than the smaller square, 144"),
    3: line(140, 170, 5, points=[(144, "144"), (149, "149"), (169, "169")], hops=[(144, 149, "+5"), (149, 169, "+20")],
            ticks="none", hl=["p1"], note="144 + 5 = 149 trees")})
A("G4A_SQUARES_033", None, {
    2: box("225 stamps", "15", "15 × 15 = 225"),
    3: box("225 stamps", "15", "15 stamps in each row of the big square", hl=["length"])})
_two = [["16", "7"], ["25", "7"], ["36", "9"], ["49", "13"], ["64", "10"], ["81", "9"]]
A("G4A_SQUARES_034", None, {
    0: table([["16", "25", "36"], ["49", "64", "81"]], note="The two-digit perfect squares"),
    1: table(_two, headers=["Square", "Digit sum"]),
    2: table(_two, headers=["Square", "Digit sum"], hl=["r3"], note="4 + 9 = 13")})
A("G4A_SQUARES_037",
  grid(4, 4, layers(4, (1, 3)), "1 + 3 + 5 + 7 = 16 fills a 4 by 4 square"),
  {0: grid(4, 4, layers(4, (1, 3)), "Adding 2, 3 or 4 odd numbers fills a 2, 3 or 4 square")})
A("G4A_SQUARES_039",
  box("144 children", None, "Children on the outside edge hold a flag", hl=["border"]),
  {0: grid(12, 12, note="144 children: 12 on each side"),
   1: grid(12, 12, border(12), "Four sides of 12 would count each corner twice"),
   2: grid(12, 12, border(12), "Take away the 4 corners that were counted twice"),
   3: grid(12, 12, border(12), "44 children hold a flag")})
_floor = [[2, 2], [10, 2], [10, 10], [2, 10]]


def floor(note, label=None):
    d = [{"from": 0, "to": 2}, {"from": 1, "to": 3}]
    if label:
        d[0]["label"] = label
    return {"kind": "polygon", "points": _floor, "rightAngles": [0, 1, 2, 3], "dashed": d, "note": note}


A("G4A_SQUARES_040",
  floor("A square floor of 225 tiles. Both diagonals are red"),
  {1: floor("15 tiles in each row, so each diagonal has 15 tiles", "15 tiles"),
   2: floor("15 is odd, so the diagonals cross on one middle tile", "15 tiles"),
   3: floor("The middle tile is counted once: 29 red tiles", "15 tiles")})
_ages = [["1", "10"], ["4", "13"], ["9", "18"], ["16", "25"], ["25", "34"], ["36", "45"]]
A("G4A_SQUARES_045", None, {
    1: table(_ages, headers=["Age now", "In 9 years"]),
    2: table(_ages, headers=["Age now", "In 9 years"], hl=["r3"], note="16 and 25 are both perfect squares")})
A("G4A_SQUARES_046", None, {0: ftree(12, "12 is 2 × 2 × 3, so it needs one more 3")})

# Past papers
A("EXT_G4_FP_2021_005",
  box(None, "?", "Rows = chairs in each row, so the hall is a square"),
  {3: box("18 × 18", "18", "Try 18 rows of 18 chairs"),
   4: box("324 men", "18", "18 rows of 18 chairs hold 324 men")})
A("PYQ_2016_Q31",
  box(None, "?", "Rows = chairs in each column, so the hall is a square"),
  {1: box("324 men", "18", "18 times 18 is 324"),
   3: box("324 men", "18", "The hall can hold 324 men")})
A("EXT_G4_FP_2021_032", None, {
    0: ftree(28, "Break 28 into prime factors"),
    1: ftree(28, "The two 2s make a pair. The 7 has no partner", hl=["primes"])})
A("EXT_G4_FP_2022_022", None, {
    0: ftree(588, "Break 588 into prime factors"),
    1: ftree(588, "The 2s pair up and the 7s pair up. The 3 has no partner", hl=["primes"])})
A("EXT_G4_FP_2023_022",
  line(1220, 1300, 10, points=[(1234, "1234")], ticks="none", note="How far is the next square number?"),
  {2: line(1220, 1300, 10, points=[(1234, "1234"), (1296, "1296")], hops=[(1234, 1296, "+62")], ticks="none",
           note="36 × 36 = 1296 is the next square")})
A("PYQ_2019_Q26",
  line(670, 730, 10, points=[(710, "710")], ticks="none", note="How far is the next square number?"),
  {0: line(670, 730, 10, points=[(676, "676"), (710, "710"), (729, "729")], ticks="none",
           note="26 × 26 = 676 and 27 × 27 = 729"),
   1: line(670, 730, 10, points=[(710, "710"), (729, "729")], hops=[(710, 729, "?")], ticks="none"),
   3: line(670, 730, 10, points=[(710, "710"), (729, "729")], hops=[(710, 729, "+19")], ticks="none", hl=["h0"])})
A("EXT_G4_FP_2025_009", None, {
    1: {"kind": "barModel", "bars": [bar([seg("16", 16, "a")] * 5 + [seg(None, 1, "unknown")], brace="81")],
        "note": "Five 16s fit into 81, with a little left over"},
    2: {"kind": "barModel", "bars": [bar([seg("16", 16, "a")] * 5 + [seg(None, 1, "b")], brace="81")],
        "highlight": ["b0s5"], "note": "The piece left over is 1"}})
_odd = [["144", "12"], ["169", "13"], ["196", "14"], ["256", "16"], ["324", "18"], ["400", "20"]]
A("EXT_G4_WS2_CH16_013", None, {
    0: table(_odd, headers=["Number", "Square of"]),
    2: table(_odd, headers=["Number", "Square of"], hl=["r1"], note="169 is the square of 13: the only odd number")})
_prime = [["81", "9"], ["121", "11"], ["169", "13"], ["289", "17"], ["361", "19"], ["529", "23"]]
A("EXT_G4_WS2_CH16_014", None, {
    0: table(_prime, headers=["Number", "Square of"]),
    2: table(_prime, headers=["Number", "Square of"], hl=["r0"], note="9 is not prime: it is 3 times 3")})
_two_digit = [["4 × 4", "16"], ["5 × 5", "25"], ["6 × 6", "36"], ["7 × 7", "49"], ["8 × 8", "64"], ["9 × 9", "81"]]
A("PYQ_2017_Q38", None, {
    0: table(_two_digit, note="The square numbers with two digits"),
    1: table(_two_digit, hl=["r0", "r2", "r4"], note="The even ones are 16, 36 and 64")})

P.write()
if "--review" in sys.argv:
    P.review()
if "--redo" in sys.argv:
    P.review(["VAR2_EXT_G4_FP_2020_003_01"])
