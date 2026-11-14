"""Batch 1: questions whose printed figure was lost (essential), then geometry and clocks."""
from c_lib import *

E = {}

# Lost figure. Key: unshaded = 3/8; steps: 8 parts, 5 shaded.
_f = lambda note, hl=None: fb([(8, 5)], note, hl)
E["EXT_G5_WS_B7_001"] = entry(
    figure=_f("What fraction of the figure is NOT shaded?"),
    steps=[
        _f("8 equal parts, 5 of them shaded"),
        _f("8 − 5 = 3 parts are not shaded"),
        _f("Not shaded: 3 out of 8 = 3/8"),
    ],
    essential=True,
)

# Lost figure: where point A sits. Key 4/5 and the steps put A on the 2nd mark.
_parts = lambda note, hl=None: bm([bar([seg("2/5") for _ in range(5)], brace="from 0 to 2")], note, hl)
E["EXT_G5_WS_B7_008"] = entry(
    figure=nl(0, 2, 0.4, points=[(0, "0"), (0.8, "A"), (2, "2")],
              note="0 to 2 is cut into 5 equal parts. A is on the 2nd mark."),
    steps=[
        _parts("Each part is 2 ÷ 5 = 2/5"),
        _parts("A is 2 parts along: 2 × 2/5 = 4/5", ["b0s0", "b0s1"]),
    ],
    essential=True,
)

# Numbering every mark would print 0.8 under A, which is the answer as a decimal.
E["EXT_G5_WS_B7_008"]["figure"]["tickLabels"] = "ends"

# Square with two sides given as expressions.
E["EXT_G5_WS_B6_021"] = entry(
    figure=rect("(2a + 5) cm", "(3a − 1) cm", "Perimeter = ?", square=True,
                note="All four sides of a square are equal"),
    steps=[
        balance("2a + 5", "3a − 1", "Equal sides, so the two expressions balance"),
        balance("5", "a − 1", "Take 2a from both sides, then add 1: a = 6"),
        rect("17 cm", "17 cm", square=True, note="Side = 2 × 6 + 5 = 17 cm", hl=["length"]),
        rect("17 cm", "17 cm", "4 × 17 = 68 cm", square=True, hl=["border"]),
    ],
)

# Triangle with three angles in y. Drawn as a general triangle (sizes unknown before solving).
_t = {"a": "(7y + 24)°", "b": "y°", "c": "(y − 15)°"}
E["EXT_G5_WS_B6_022"] = entry(
    figure=tri("scalene", angles=_t, note="The three angles of a triangle add up to 180°"),
    steps=[
        tri("scalene", angles=_t, note="y + (y − 15) + (7y + 24) = 180", hl=["a", "b", "c"]),
        balance("9y + 9", "180", "9y = 171, so y = 19"),
        tri("scalene", angles={"a": "157°", "b": "19°", "c": "4°"}, note="Put y = 19 into each angle"),
        tri("scalene", angles={"a": "157°", "b": "19°", "c": "4°"}, note="Smallest angle = 4°", hl=["c"]),
    ],
)

# Hour hand two-fifths of the way from 9 to 10 (the fraction is in words, so no before-figure).
E["EXT_G5_WS_B7_027"] = entry(
    steps=[
        fb([(5, 2, "from 9 to 10")], "2/5 of the hour has passed: 2/5 × 60 = 24 minutes"),
        clock(9, 24, "The time is 9:24", ["minute"]),
        None,
    ],
)

# 3/5 of the exercise takes 24 minutes, starting at 11 am.
def _ex(l3, l2, brace=None, note=None, hl=None):
    segs = [seg(l3, tone="a") for _ in range(3)] + [seg(l2, tone="unknown") for _ in range(2)]
    return bm([bar(segs, label="Exercise", brace=brace)], note, hl)

E["EXT_G5_WS_B7_029"] = entry(
    figure=_ex(None, "?", note="3 of the 5 equal parts take 24 minutes"),
    steps=[
        _ex("8 min", "?", note="One part: 24 ÷ 3 = 8 minutes", hl=["b0s0", "b0s1", "b0s2"]),
        _ex("8 min", "8 min", brace="40 min", note="All 5 parts: 5 × 8 = 40 minutes"),
        clock(11, 40, "11:00 + 40 minutes = 11:40 am", ["minute"]),
    ],
)

# Squares: "as many in each as there are groups".
E["EXT_G5_WS_B5_024"] = entry(
    figure=rect("n boxes", "n pencils each", "Total = n × n", square=True,
                note="Boxes and pencils per box are the same number"),
    steps=[
        rect("n boxes", "n pencils each", "Total = n × n", square=True, note="The total must be a square number"),
        rect("27 boxes", "27 pencils each", "27 × 27 = 729", square=True, hl=["fill"]),
        None,
    ],
)
E["EXT_G5_WS_B5_025"] = entry(
    figure=rect("n groups", "n in each group", "n × n, at most 245", square=True,
                note="Groups and students per group are the same number"),
    steps=[
        rect("15 groups", "15 in each group", "15 × 15 = 225", square=True, note="The biggest square that fits in 245"),
        rect("15 groups", "15 in each group", "225", square=True, note="245 − 225 = 20 students left out"),
        None,
    ],
)
E["EXT_G5_WS_B5_026"] = entry(
    figure=rect("b boys", "Rs. b each", "b × b rupees", square=True,
                note="Boys' money + Rs. 75 from the teacher = Rs. 1300"),
    steps=[
        balance("b × b + 75", "1300", "Boys' money plus the teacher's 75"),
        balance("b × b", "1225", "Take 75 from both sides"),
        rect("35 boys", "Rs. 35 each", "35 × 35 = 1225", square=True, hl=["fill"]),
    ],
)
E["EXT_G5_WS_B5_016"] = entry(
    figure=rect("36", "35", "35 × 36", note="How much more turns this into a square?"),
    steps=[
        rect("36", "35", "1260", note="35 × 36 = 1260"),
        rect("36", "35", "1260", note="35 rows of 36: one row short of 36 × 36", hl=["breadth"]),
        rect("36", "36", "1260 + 36 = 1296", square=True, note="Add one more row of 36", hl=["fill"]),
    ],
)
