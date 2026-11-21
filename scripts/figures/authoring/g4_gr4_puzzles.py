"""Figures for Grade 4 "Puzzles & Magic Squares" (topic gr4_puzzles).

    python -X utf8 scripts/figures/authoring/g4_gr4_puzzles.py

Writes data/question-figures/parts/g4-gr4_puzzles.json.

What is drawn:
  - the square of numbers a question gives in words, as a table, read from the question text;
    the unknown boxes are filled in step by step as the steps name them;
  - clue tables for "who am I" and logic puzzles;
  - a balance for a missing-digit sum or a "think of a number" puzzle;
  - bars for picture equations, a Venn diagram for "both", counters for heads and legs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_time_kit import Part, T, BM, NL, V, BAL, SET  # noqa: E402

P = Part("gr4_puzzles")
BOX = "□"


def cell(s):
    s = s.strip()
    return BOX if s in ("", "_", "blank") else s


def rows_by_name(qid, pattern):
    """Rows written as 'Row 1: 9, 2, 7' or 'Top row: 7, 13, 24.'"""
    out = [[cell(c) for c in m.split(",")] for m in re.findall(pattern, P.text(qid))]
    if len(out) != 3 or any(len(r) != 3 for r in out):
        P.problems.append("%s: could not read a 3 by 3 square (%r)" % (qid, out))
    return out


def rows_by_pipes(qid):
    """Rows written as '|  9  | 15 |  6  |'."""
    out = []
    for line in P.text(qid).split("\n"):
        if "|" in line:
            out.append([cell(c) for c in line.strip().strip("|").split("|")])
    if len(out) != 3 or any(len(r) != 3 for r in out):
        P.problems.append("%s: could not read a 3 by 3 square (%r)" % (qid, out))
    return out


def put_in(rows, changes):
    """A copy of the square with some boxes changed. changes: {old cell text: new} or {(row, col): new}."""
    out = [list(r) for r in rows]
    for key, new in changes.items():
        if isinstance(key, tuple):
            out[key[0]][key[1]] = str(new)
        else:
            hit = [(i, j) for i in range(len(out)) for j in range(len(out[i])) if out[i][j] == key]
            if len(hit) != 1:
                P.problems.append("put_in: %r is in %d boxes" % (key, len(hit)))
                continue
            out[hit[0][0]][hit[0][1]] = str(new)
    return out


ROW_N = r"Row \d: ([^\n]+)"
ROW_TMB = r"(?:Top|Middle|Bottom) row: ([^.]+(?:\.\d+)?)\."


# ── Magic squares and number squares ─────────────────────────────────────────

R = rows_by_name("G4A_PUZZLES_001", ROW_N)
P.put("G4A_PUZZLES_001", T(R, note="Every row, column and diagonal has the same total"),
      {0: T(R, hl=["r0"], note="Find the magic total from Row 1: 9 + 2 + 7"),
       1: T(R, hl=["r2"], note="Row 3 must add up to the same total"),
       2: T(put_in(R, {"?": 10}), hl=["r2"], note="The missing number is 10")}, origin="rule")

R = rows_by_name("G4A_PUZZLES_009", ROW_N)
P.put("G4A_PUZZLES_009", T(R, note="Every row, column and diagonal has the same total. P + Q = ?"),
      {0: T(R, hl=["r2"], note="Find the magic total from Row 3: 8 + 18 + 4"),
       1: T(R, hl=["r0"], note="Use Row 1 to find P"),
       2: T(R, hl=["r1"], note="Use Row 2 to find Q"),
       3: T(R, note="Add P and Q"),
       4: T(R, note="P + Q = 22")}, origin="rule")

R = rows_by_name("G4A_PUZZLES_019", ROW_N)
P.put("G4A_PUZZLES_019", T(R, note="Every row, column and diagonal has the same total. Q = ?"),
      {0: T(R, note="The diagonal 9, 11, 13 is complete: it gives the magic total"),
       1: T(R, hl=["r0"], note="Use Row 1 to find P"),
       2: T(R, note="The other diagonal is P, 11, Q. Use it to find Q"),
       3: T(put_in(R, {"Q": 14}), hl=["r2"], note="Q is 14")}, origin="rule")

R = rows_by_name("EXT_G4_FP_2022_028", ROW_TMB)
P.put("EXT_G4_FP_2022_028", T(R, note="Each column follows the same rule. Z = ?"),
      {0: T(R, note="First column: top minus middle, then times itself, gives 16"),
       1: T(R, note="The second column follows the same rule and gives 49"),
       2: T(R, note="13 times 13 is 169, so 24 minus Z must be 13"),
       3: T(put_in(R, {"Z": 11}), note="Z is 11")}, origin="rule")

R = rows_by_name("EXT_G4_FP_2023_029", ROW_TMB)
P.put("EXT_G4_FP_2023_029", T(R, note="Each column follows the same rule. Q = ?"),
      {0: T(R, note="First column: 3 becomes 9, then 9 becomes 81"),
       1: T(R, note="Second column: multiply by 3, then multiply the result by itself"),
       2: T(R, note="Third column: 8 times 3 is 24, so Q is 24 times 24"),
       3: T(put_in(R, {"Q": 576}), note="Q is 576")}, origin="rule")

R = rows_by_name("Q_CH15_009", ROW_TMB)
P.put("Q_CH15_009", T(R, note="Every row, column and diagonal has the same total"),
      {0: T(R, hl=["r0"], note="Add the top row. Write 2 as 6/3 so everything is in thirds"),
       1: T(R, note="Every row, column and diagonal must add up to 5"),
       2: T(R, hl=["r1"], note="Middle row: add 1/3 and 3. Write 3 as 9/3"),
       3: T(put_in(R, {"?": "5/3"}), hl=["r1"], note="5 is 15/3. Take away 10/3: the missing number is 5/3")}, origin="rule")

R = rows_by_pipes("Q_CH15_004")
P.put("Q_CH15_004", T(R, note="A magic square. Find A and B"),
      {0: T(R, hl=["r0"], note="The top row is complete: add it to find the magic total"),
       1: T(put_in(R, {"A": 7}), hl=["r1"], note="Middle row: A is 30 − 23 = 7"),
       2: T(put_in(R, {"A": 7, "B": 11}), hl=["r2"], note="Bottom row: B is 30 − 19 = 11"),
       3: T(put_in(R, {"A": 7, "B": 11}), note="Check the first column: 9 + 7 + 14 = 30")}, origin="rule")

R = rows_by_pipes("Q_CH15_006")
P.put("Q_CH15_006", T(R, note="Complete the magic square. Which number is NOT used?"),
      {0: T(R, hl=["r1"], note="The centre is 5, so every line adds to 3 times 5"),
       1: T(put_in(R, {(0, 1): 3}), hl=["r0"], note="4 + 8 = 12, so the box between them is 15 − 12 = 3"),
       2: T(put_in(R, {(0, 1): 3, (2, 0): 2, (2, 1): 7, (2, 2): 6}), hl=["r2"], note="Opposite boxes add to 10: 6 with 4, 2 with 8, 7 with 3"),
       3: T(put_in(R, {(0, 1): 3, (2, 0): 2, (2, 1): 7, (2, 2): 6, (1, 0): 9, (1, 2): 1}), hl=["r1"], note="First column gives 9. Last column gives 1"),
       4: T(put_in(R, {(0, 1): 3, (2, 0): 2, (2, 1): 7, (2, 2): 6, (1, 0): 9, (1, 2): 1}), note="The square uses 1 to 9. The number not used is 11")},
      origin="rule")

R = rows_by_pipes("Q_CH15_010")
P.put("Q_CH15_010", T(R, note="Rows, columns and diagonals have equal sums. X + Y + Z = ?"),
      {0: T(R, note="The last column is complete: add 4, 15 and 8"),
       1: T(put_in(R, {"Y": 9}), hl=["r1"], note="The centre is one third of the magic sum, so Y is 9"),
       2: T(put_in(R, {"Y": 9, "Z": 10}), hl=["r0"], note="Diagonal Z, Y, 8: Z is 27 − 17 = 10"),
       3: T(put_in(R, {"Y": 9, "Z": 10, "X": 14}), hl=["r2"], note="Diagonal 4, Y, X: X is 27 − 13 = 14"),
       4: T(put_in(R, {"Y": 9, "Z": 10, "X": 14}), note="Now add the three letters"),
       5: T(put_in(R, {"Y": 9, "Z": 10, "X": 14}), note="X + Y + Z = 33")}, origin="rule")

R = rows_by_pipes("Q_CH15_011")
P.put("Q_CH15_011", T(R, note="Each column follows the same rule. Find the missing number"),
      {0: T(R, note="First column: 4 + 3 = 7, and 7 × 7 = 49"),
       1: T(R, note="Second column: 6 + 4 = 10, and 10 × 10 = 100"),
       2: T(R, note="13 × 13 = 169, so the top two numbers must add to 13"),
       3: T(R, note="The top number is 8, so take 8 from 13"),
       4: T(put_in(R, {"?": 5}), note="The missing number is 5")}, origin="rule")

R = rows_by_pipes("Q_CH15_013")
P.put("Q_CH15_013", T(R, note="Each row follows the same rule. Find the missing number"),
      {0: T(R, hl=["r0"], note="3 × 4 = 12. Double it to get 24, add 1 to get 25"),
       1: T(R, hl=["r1"], note="5 × 7 = 35. Double it to get 70, add 1 to get 71"),
       2: T(R, hl=["r0", "r1"], note="A rule must fit every row, so test it on each one"),
       3: T(R, hl=["r2"], note="6 × 8 = 48. Double it to get 96, and add 1"),
       4: T(put_in(R, {"?": 97}), hl=["r2"], note="The missing number is 97")}, origin="rule")

# "n,_,6/4,x,m/16,_,_"
R = [[cell(c) for c in row.split(",")] for row in re.search(r"square: (\S+)\.", P.text("EXT_G4_FP_2024_015")).group(1).split("/")]
P.put("EXT_G4_FP_2024_015", T(R, note="A magic square. Find m + n"),
      {0: T(R, hl=["r1"], note="Middle row and one diagonal share x: 4 + m equals 6 + 16"),
       1: T(R, hl=["r1"], note="Find m"),
       2: T(put_in(R, {"x": 11}), note="Each line is 3 times the middle: x = 11, each line adds to 33"),
       3: T(put_in(R, {"x": 11}), note="The first column is n, 4 and 16. Find n"),
       4: T(put_in(R, {"x": 11}), note="m + n = 31")}, origin="rule")

# "4,5,7/2,2,2/64,100,A": the checker reads this list as 457 / 222 / 64100, so it does not accept
# 4, 5, 7 or 64 as numbers of the question. No figure before answering; the columns appear as the steps name them.
P.put("EXT_G4_FP_2021_034", None,
      {0: T([["4"], ["2"], ["64"]], note="First column: 4 × 2 = 8, and 8 × 8 = 64"),
       1: T([["4", "5"], ["2", "2"], ["64", "100"]], note="Second column: 5 × 2 = 10, and 10 × 10 = 100")})

R = [["4", "3", "8"], ["9", "5", "1"], [BOX, BOX, BOX]]
P.put("EXT_G4_WS2_CH15_002", T(R, note="Complete the magic square. Which number is not used?"),
      {0: T(R, hl=["r0"], note="Find the total of a full row: 4 + 3 + 8"),
       1: T(R, note="Each column must also add up to 15. The first has 4 and 9"),
       2: T(R, note="Do the same for the second and third columns"),
       3: T(put_in(R, {(2, 0): 2, (2, 1): 7, (2, 2): 6}), hl=["r2"], note="The bottom row is 2, 7, 6"),
       4: T(put_in(R, {(2, 0): 2, (2, 1): 7, (2, 2): 6}), note="3, 6 and 9 are all in the square. 11 is not used")})

EMPTY = [[BOX, BOX, BOX], [BOX, "?", BOX], [BOX, BOX, BOX]]

P.put("PYQ_2019_Q31", T(EMPTY, note="Every line of 3 boxes adds up to 54"),
      {0: T(EMPTY, hl=["r1"], note="The central number is always one third of the magic sum"),
       1: T(EMPTY, hl=["r1"], note="The magic sum is 54, so divide 54 by 3"),
       2: T(put_in(EMPTY, {"?": 18}), hl=["r1"], note="The number in the central box is 18")})

R8 = put_in(EMPTY, {"?": 8})
P.put("Q_CH15_008", T(R8, note="Magic constant = ?"),
      {0: T(R8, hl=["r1"], note="The magic constant is 3 times the central number"),
       1: T(R8, hl=["r1"], note="The centre is 8, so multiply 8 by 3"),
       2: T(R8, note="The magic constant is 24")})

P.put("Q_CH15_021", T(EMPTY, note="All nine numbers add up to 72. Centre = ?"),
      {0: T(EMPTY, hl=["r0"], note="Three rows with equal sums: share 72 among the 3 rows"),
       1: T(EMPTY, hl=["r1"], note="Each row adds to 24. The centre is one third of a row"),
       2: T(put_in(EMPTY, {"?": 8}), hl=["r1"], note="Check: 9 boxes with a centre of 8 give 9 × 8 = 72")})

R = [["6", "15", "3"], [BOX, "?", BOX], [BOX, BOX, BOX]]
P.put("Q_CH15_023", T(R, note="Find the magic constant and the centre number"),
      {0: T(R, hl=["r0"], note="The magic constant is the sum of any row: add the first row"),
       1: T(R, hl=["r1"], note="The constant is 3 times the centre, so divide it by 3"),
       2: T(R, hl=["r1"], note="The centre is a new number, one third of 24"),
       3: T(put_in(R, {"?": 8}), hl=["r1"], note="Constant = 24, Centre = 8")})

KNOWN = [["2", "7", "6"], ["9", "5", "1"], ["4", "3", "8"]]
P.put("Q_CH15_002", None,
      {0: T(KNOWN, hl=["r1"], note="A magic square you know. The central box holds 5"),
       1: T(KNOWN, hl=["r0"], note="Add any row to find the magic constant"),
       2: T(KNOWN, hl=["r1"], note="Compare 15 with the central number 5: 15 is 3 times 5"),
       3: T(KNOWN, note="The magic constant is 3 × the central box number")})

CROSS = [["·", "1", "·"], ["?", "5", "?"], ["·", "?", "·"]]
P.put("Q_CH15_022", T(CROSS, note="3, 7 and 9 go at the other ends. Both lines have the same sum"),
      {0: T(CROSS, hl=["r1"], note="Both lines share the 5, so their two ends must add up the same"),
       1: T(CROSS, note="The four end numbers add up to 1 + 3 + 7 + 9 = 20"),
       2: T(CROSS, note="Each pair of ends adds up to 20 ÷ 2 = 10"),
       3: T(put_in(CROSS, {(2, 1): 9}), note="The partner of 1 is 10 − 1 = 9, so 9 is opposite to 1")})

# The sum of all nine numbers (no figure before: the question is about a rule, not one square)
CENTRE = put_in(EMPTY, {"?": "centre"})
FIVE = put_in(EMPTY, {"?": 5})
P.put("Q_CH15_003", None,
      {0: T(CENTRE, hl=["r0", "r1", "r2"], note="Three rows hold all nine numbers: 3 × the magic sum"),
       1: T(FIVE, hl=["r1"], note="With 1 to 9 the centre is 5 and each row adds up to 15"),
       2: T(CENTRE, note="3 × 3 × the central box number, and 3 × 3 = 9"),
       3: T(FIVE, note="Check with 1 to 9: they add up to 45, and 9 × 5 = 45"),
       4: T(CENTRE, hl=["r1"], note="The sum of all nine numbers is 9 × the central box number")})

P.put("G4A_PUZZLES_006", T([["4", "11", "?"]], note="Every row adds up to 21"),
      {0: T([["4", "11", "?"]], note="Add the two numbers you know: 4 + 11"),
       1: T([["4", "11", "?"]], note="Find what is needed to reach 21"),
       2: T([["4", "11", "6"]], note="The missing number is 6")})

# Nine numbers in a row: the middle one goes in the centre
P.put("Q_CH15_007", NL(3, 11, 1, note="The numbers 3 to 11 make a magic square. Which goes in the centre?"),
      {0: NL(3, 11, 1, note="Write the nine numbers in order"),
       1: NL(3, 11, 1, points=[(7, "7")], hl=["p0"], note="The middle number, 7, goes in the centre"),
       2: NL(3, 11, 1, points=[(7, "7")], note="Check: each row adds to 21, and the centre is one third of 21"),
       3: NL(3, 11, 1, points=[(7, "7")], hl=["p0"], note="The number in the central box is 7")})

P.put("Q_CH15_017", NL(11, 19, 1, note="The numbers 11 to 19 fill the square. Magic constant = ?"),
      {0: NL(11, 19, 1, points=[(15, "15")], hl=["p0"], note="The middle number, 15, goes in the centre"),
       1: NL(11, 19, 1, points=[(15, "15")], note="The magic constant is 3 times the centre: 3 × 15"),
       2: NL(11, 19, 1, points=[(15, "15")], note="Check: the nine numbers add to 135, and one third of 135 is 45"),
       3: NL(11, 19, 1, points=[(15, "15")], note="The magic constant is 45")})

P.put("Q_CH15_025", None,
      {0: NL(5, 21, 2, note="The nine odd numbers starting from 5"),
       1: NL(5, 21, 2, points=[(13, "13")], hl=["p0"], note="The middle number is the fifth one: 13"),
       2: NL(5, 21, 2, points=[(5, "5"), (13, "13"), (21, "21")], note="Check: 5 + 13 + 21 = 39, which is 3 times 13"),
       3: NL(5, 21, 2, points=[(13, "13")], hl=["p0"], note="The number in the centre is 13")})


# ── Sets, queues, heads and legs ─────────────────────────────────────────────

v = lambda both, **k: V("Cups: 15", "Plates: 21", "cup only", both, "plate only", **k)
P.put("EXT_G4_FP_2020_001", v("?", note="25 trays in all. How many have both?"),
      {0: v("?", note="Add the trays with cups and the trays with plates"),
       1: v("?", hl=["both"], note="There are only 25 trays: the extra ones were counted twice"),
       2: v("11", hl=["both"], note="11 trays have both a cup and a plate")})


def queue(mid, back=None, **k):
    segs = [(12, None, "a"), (5, "You", "b"), (31, mid, "c" if mid != "?" else "unknown"), (8, "Friend", "b"), (18, back, "a")]
    return BM([(None, segs, "63 students")], **k)


P.put("EXT_G4_FP_2024_035", queue("?", note="You are 13th from the beginning. Your friend is 19th from the end"),
      {0: queue("?", "18 behind", hl=["b0s4"], note="19th from the end means 18 students stand behind your friend"),
       1: queue("?", "18 behind", hl=["b0s2"], note="You are 13th and your friend is 45th: between are places 14 to 44"),
       2: queue("31", "18 behind", hl=["b0s2"], note="31 students are between you")})

P.put("G4A_PUZZLES_023", SET(10, item="animals", note="10 heads and 28 legs. How many are goats?"),
      {0: SET(10, item="animals", note="Suppose all 10 animals were hens with 2 legs each"),
       1: SET(10, item="animals", note="Find the extra legs"),
       2: SET(10, item="animals", note="Each goat has 2 more legs than a hen"),
       3: SET(10, groups=10, shaded=4, item="animals", hl=["shaded"], note="Check with 4 goats (shaded) and 6 hens"),
       4: SET(10, groups=10, shaded=4, item="animals", hl=["shaded"], note="The farmer has 4 goats")})


# ── Digit puzzles ────────────────────────────────────────────────────────────

HTO = ["Hundreds", "Tens", "Ones"]
P.put("EXT_G4_FP_2020_010", T([["more than 8", "4 more than ones", "odd"]], headers=HTO, note="A 3-digit odd number. Sum of its digits = ?"),
      {0: T([["9", "4 more than ones", "odd"]], headers=HTO, note="The only digit more than 8 is 9"),
       1: T([["9", "4 more than ones", "1, 3 or 5"]], headers=HTO, note="The tens digit must still be a single digit"),
       2: T([["9", "5", "1"]], headers=HTO, note="Try ones digit 1: the tens digit is 5 and the number is 951"),
       3: T([["9", "5", "1"]], headers=HTO, hl=["r0"], note="Add the digits of 951"),
       4: T([["951", "15"], ["973", "19"], ["995", "23"]], headers=["Number", "Digit sum"], hl=["r0"], note="973 and 995 give 19 and 23, which are not choices")})

LEAD = ["First digits", "Tens", "Ones"]
P.put("EXT_G4_FP_2020_011", T([["213", "a", "b"]], headers=LEAD, note="Remainder under 10 when divided by 100. Digits add up to 13"),
      {0: T([["213", "a", "b"]], headers=LEAD, note="Dividing by 100, the remainder is the last two digits, ab"),
       1: T([["213", "0", "b"]], headers=LEAD, note="The remainder is less than 10, so the tens digit a must be 0"),
       2: T([["213", "0", "b"]], headers=LEAD, note="Add the digits you know"),
       3: T([["213", "0", "b"]], headers=LEAD, note="All five digits add up to 13, so b is what is left"),
       4: T([["213", "0", "7"]], headers=LEAD, note="b = 7")})

P.put("G4A_PUZZLES_002", T([["4", "?"]], headers=["Tens", "Ones"], note="The two digits add up to 11"),
      {0: T([["4", "?"]], headers=["Tens", "Ones"], hl=["r0"], note="The tens digit is 4"),
       1: T([["4", "?"]], headers=["Tens", "Ones"], note="Find the ones digit: 11 − 4"),
       2: T([["4", "?"]], headers=["Tens", "Ones"], hl=["r0"], note="The number is 47")})

P.put("G4A_PUZZLES_003", BAL("4P + 25", "71", note="4P is a two-digit number. Which digit is P?"),
      {0: BAL("4P", "71 − 25", note="Work backwards to find the two-digit number 4P"),
       1: BAL("46 + 25", "71", hl=["left"], note="So 4P is 46"),
       2: BAL("46 + 25", "71", note="P is 6")})

TO = ["Tens", "Ones"]
P.put("G4A_PUZZLES_010", T([["3", "P"], ["P", "8"], ["8", "2"]], headers=TO, note="3P + P8 = 82: the top two rows add up to the bottom row"),
      {0: T([["3", "P"], ["P", "8"], ["8", "2"]], headers=TO, note="Ones column: P + 8 must end in 2. Since 4 + 8 = 12, try 4"),
       1: T([["3", "4"], ["4", "8"], ["8", "2"]], headers=TO, note="Check the whole sum with P as 4"),
       2: T([["3", "4"], ["4", "8"], ["8", "2"]], headers=TO, note="The sum is true, so P is 4")})

P.put("G4A_PUZZLES_011", T([["P", "Q"], ["Q", "P"]], headers=TO, note="PQ + QP = 77, and P is 1 more than Q"),
      {0: T([["P", "Q"], ["Q", "P"], ["7", "7"]], headers=TO, note="In each column P and Q are added, so P + Q = 7"),
       1: T([["P", "Q"], ["Q", "P"], ["7", "7"]], headers=TO, note="Two digits that add up to 7 and differ by 1 are 4 and 3"),
       2: T([["4", "3"], ["3", "4"], ["7", "7"]], headers=TO, note="P is the bigger digit, so P is 4 and Q is 3"),
       3: T([["4", "3"], ["3", "4"], ["7", "7"]], headers=TO, note="Check the sum: 43 + 34 = 77"),
       4: T([["4", "3"], ["3", "4"], ["7", "7"]], headers=TO, hl=["r0"], note="The number PQ is 43")})

P.put("G4A_PUZZLES_016", BAL("2R5 × 3", "735", note="R stands for one digit"),
      {0: BAL("2R5", "735 ÷ 3", note="Undo the multiplication"),
       1: BAL("2R5", "245", note="So 2R5 is 245, and R is the tens digit"),
       2: BAL("2R5", "245", note="R is 4")})

P.put("G4A_PUZZLES_022", T([["double the ones", "hundreds + ones", "?"]], headers=HTO, note="The three digits add up to 12"),
      {0: T([["2", "3", "1"]], headers=HTO, note="Try ones digit 1: the digits add up to 6, which is too small"),
       1: T([["4", "6", "2"]], headers=HTO, note="Try ones digit 2: hundreds digit 4, tens digit 6"),
       2: T([["4", "6", "2"]], headers=HTO, note="All the clues fit"),
       3: T([["4", "6", "2"]], headers=HTO, hl=["r0"], note="The number is 462")})

mults = [m for m in range(10, 50) if m % 7 == 0]
sums = [sum(int(c) for c in str(m)) for m in mults]
want = "r%d" % sums.index(6)
P.put("G4A_PUZZLES_014", None,
      {0: T([mults[:3], mults[3:]], note="The 2-digit multiples of 7 below 50"),
       1: T([[m, s] for m, s in zip(mults, sums)], headers=["Multiple of 7", "Digit total"], note="Add the digits of each one"),
       2: T([[m, s] for m, s in zip(mults, sums)], headers=["Multiple of 7", "Digit total"], hl=[want], note="Only one has digits adding up to 6. The number is 42")},
      origin="rule")

P.put("PYQ_2018_Q24", T([["4", "4", "4"], ["9", "9", "9"]], note="He uses 5 cards: a 3-digit number and a 2-digit number"),
      {0: T([["4", "4", "4"], ["9", "9", "9"]], note="3-digit: 444 to 499, or 944 to 999. 2-digit: 44 to 99"),
       1: T([["4", "4", "4"], ["9", "9", "9"]], note="Differences run from 345 to 455, or from 845 to 955"),
       2: T([["4", "4", "4"], ["9", "9", "9"]], note="With only 4s and 9s, the difference ends in 0 or 5"),
       3: T([["3-digit number", "499"], ["2-digit number", "49"]], note="499 − 49 uses two 4s and three 9s"),
       4: T([["3-digit number", "499"], ["2-digit number", "49"]], note="So the difference can be 450")})

P.put("PYQ_2018_Q33", None,
      {1: T([["4", "★", "4"]], note="8 + 4 = 12 ends in 2, so the palindrome looks like 4 ★ 4"),
       2: T([["4", "2", "4"]], note="424 + 2018 = 2442, which is a palindrome"),
       3: T([["4", "2", "4"]], note="Its digits add up to 4 + 2 + 4 = 10")})

P.put("Q_CH16_019", T([["?", "1", "?", "?"]], headers=["M", "A", "T", "H"], note="A = 1, B = 2, C = 3 and so on. Add the four letters"),
      {0: T([["13", "1", "20", "8"]], headers=["M", "A", "T", "H"], note="Find each letter's place in the alphabet"),
       1: T([["13", "1", "20", "8"]], headers=["M", "A", "T", "H"], note="Add the four numbers"),
       2: T([["13", "1", "20", "8"]], headers=["M", "A", "T", "H"], note="The sum of the letters in MATH is 42")})

found = re.findall(r"(\d+ \+ \d+) = (\d+|\?)", P.text("Q_CH15_014"))
R = [list(r) for r in found]
P.put("Q_CH15_014", T(R, note="What number should replace the question mark?"),
      {0: T(R, hl=["r0"], note="5 − 3 = 2 and 5 + 3 = 8. Side by side they make 28"),
       1: T(R, hl=["r1", "r2"], note="9 and 1 give 8 and 10. 8 and 6 give 2 and 14"),
       2: T(R, note="The rule: write the difference first, then the sum"),
       3: T(R, hl=["r3"], note="For 5 and 4: the difference is 1 and the sum is 9"),
       4: T(put_in(R, {"?": 19}), hl=["r3"], note="Writing 1 and then 9 gives 19")}, origin="rule")


# ── Picture equations and "think of a number" ────────────────────────────────

def stars(star, moon, sw=1, mw=1, **k):
    return BM([(None, [(sw, star), (sw, star)], "14"), (None, [(sw, star), (mw, moon, "b")], "10")], **k)


P.put("G4A_PUZZLES_004", stars("star", "moon", note="What is the moon worth?"),
      {0: stars("7", "moon", hl=["b0"], note="Two equal stars make 14, so one star is 7"),
       1: stars("7", "moon", hl=["b1s1"], note="A star plus a moon makes 10"),
       2: stars("7", "3", 7, 3, hl=["b1s1"], note="The moon is worth 3")})


def shop(pencil, eraser, pw=1, ew=1, **k):
    return BM([(None, [(pw, pencil), (ew, eraser, "b")], "₹12"), (None, [(pw, pencil), (ew, eraser, "b"), (pw, pencil)], "₹19")], **k)


P.put("G4A_PUZZLES_015", shop("pencil", "eraser", note="How much does the eraser cost?"),
      {0: shop("pencil", "eraser", hl=["b1s2"], note="The second purchase has one extra pencil: find its cost"),
       1: shop("₹7", "eraser", hl=["b0s1"], note="A pencil and an eraser cost ₹12 together"),
       2: shop("₹7", "₹5", 7, 5, hl=["b0s1"], note="The eraser costs ₹5")})

P.put("G4A_PUZZLES_012", BAL("? × 2 + 3", "17", note="Double the number, then add 3. The answer is 17"),
      {0: BAL("? × 2", "14", note="Undo the adding of 3"),
       1: BAL("?", "7", note="Undo the doubling"),
       2: BAL("7 × 2 + 3", "17", note="Check: double 7, then add 3"),
       3: BAL("7 × 2 + 3", "17", note="The number was 7")})

P.put("Q_CH15_024", T([["A + B", "10"], ["B + C", "15"], ["A + C", "11"]], note="A + B + C = ?"),
      {0: T([["A + B", "10"], ["B + C", "15"], ["A + C", "11"]], note="Add the three sums together"),
       1: T([["A + B", "10"], ["B + C", "15"], ["A + C", "11"]], note="36 is two lots of A + B + C: each letter is counted twice"),
       2: T([["A + B", "10"], ["B + C", "15"], ["A + C", "11"]], note="Halve 36 to get one lot"),
       3: T([["A + B", "10"], ["B + C", "15"], ["A + C", "11"]], note="Check: C is 8, A is 3 and B is 7. So A + B + C = 18")})

blue = ("blue", [(2, None, "b")] * 3, None)
red = ("red", [(3, None, "a")] * 2, None)
green = ("green", [(1, None, "c")] * 6, None)
P.put("Q_CH15_020", BM([blue, red], note="Three blue = two red. One red = three green"),
      {0: BM([blue, red], hl=["b0", "b1"], note="Three blue circles are worth two red circles"),
       1: BM([blue, red, green], hl=["b2"], note="Swap each of the two red circles for three green circles"),
       2: BM([blue, red, green], hl=["b2"], note="That gives 2 × 3 = 6 green circles"),
       3: BM([blue, red, green], note="So three blue circles are worth 6 green circles")})


# ── Logic and ordering ───────────────────────────────────────────────────────

P.put("G4A_PUZZLES_005", None,
      {0: T([["Amit", "Bina", "Chetan"]], note="Tallest on the left: Amit, Bina, Chetan"),
       1: T([["Amit", "Bina", "Chetan", "Divya"]], note="Divya is shorter than Chetan, so she comes last"),
       2: T([["Amit", "Bina", "Chetan", "Divya"]], note="The tallest is Amit")})

pets = lambda isha, lata, **k: T([["Isha", isha], ["Jay", "cat"], ["Kiran", "rabbit"], ["Lata", lata]], headers=["Child", "Pet"], **k)
P.put("G4A_PUZZLES_013", pets("not the dog", "?"),
      {0: pets("not the dog", "?", hl=["r1", "r2"], note="The cat and the rabbit are taken: dog and parrot are left"),
       1: pets("parrot", "?", hl=["r0"], note="Isha does not have the dog, so Isha has the parrot"),
       2: pets("parrot", "dog", hl=["r3"], note="The only pet left for Lata is the dog")})

P.put("G4A_PUZZLES_017", None,
      {0: T([["Farah", "Dev", "Esha"]], note="First on the left: Farah, then Dev, then Esha"),
       1: T([["Farah", "Dev", "Hari", "Esha"]], note="Hari is between Dev and Esha"),
       2: T([["Farah", "Dev", "Hari", "Esha", "Gita"]], note="Gita is last"),
       3: T([["Farah", "Dev", "Hari", "Esha", "Gita"]], note="The child who came second is Dev")})

dice = lambda **k: T([["1", "?"], ["2", "?"], ["3", "?"]], headers=["Face she sees", "Opposite face"], **k)
P.put("G4A_PUZZLES_018", dice(note="Opposite faces always add up to 7"),
      {0: dice(note="Find the face opposite each face she can see"),
       1: dice(note="Add the three hidden faces"),
       2: dice(note="The hidden faces total 15")})

LABELS = [["Box 1", "in this box"], ["Box 2", "not in this box"], ["Box 3", "not in Box 1"]]


def boxes(where, marks, **k):
    return T([LABELS[i] + [marks[i]] for i in range(3)], headers=["Label on", "Laddoo is", "If in " + where], **k)


P.put("G4A_PUZZLES_025", T(LABELS, headers=["Label on", "Laddoo is"], note="Only one of the three labels is true"),
      {0: boxes("Box 1", ["true", "true", "untrue"], note="If it is in Box 1, two labels are true. This does not fit"),
       1: boxes("Box 3", ["untrue", "true", "true"], note="If it is in Box 3, two labels are true again"),
       2: boxes("Box 2", ["untrue", "untrue", "true"], hl=["r2"], note="If it is in Box 2, exactly one label is true"),
       3: boxes("Box 2", ["untrue", "untrue", "true"], note="The laddoo is in Box 2")})

P.write()
