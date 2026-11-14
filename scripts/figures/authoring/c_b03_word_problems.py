"""Batch 3: worksheet B2 word problems: queues, sequences, ages, sums and differences, Venn."""
from c_lib import *

E = {}

# Queue: Anay 10th from the front, 5 people, then Vinay 8th from the end.
def _q(brace, note, hl=None):
    return bm([bar([seg("Anay is 10th", 3, "a"), seg("5 between", 2, "b"), seg("Vinay 8th from end", 3, "c")],
                   label="Queue", brace=brace)], note, hl)

E["EXT_G5_WS_01_017"] = entry(
    figure=_q("? people", "Front of the queue is on the left"),
    steps=[
        _q("? people", "Up to and including Anay: 10 people", ["b0s0"]),
        _q("? people", "Then the 5 people between them", ["b0s1"]),
        _q("? people", "From Vinay to the end: 8 people", ["b0s2"]),
        _q("23 people", "10 + 5 + 8 = 23"),
    ],
)

# The other number is 17638 more than 4905 (it cannot be less: 4905 is too small).
def _d(brace, note, hl=None):
    return bm([bar([seg("4905", 1, "a")], label="One number"),
               bar([seg("4905", 1, "a"), seg("17638", 3, "b")], label="Other number", brace=brace)], note, hl)

E["EXT_G5_WS_B2_009"] = entry(
    figure=_d("?", "The two numbers differ by 17638"),
    steps=[_d("?", "Other number = 4905 + 17638", ["b1"]), _d("22543", "4905 + 17638 = 22543", ["b1"])],
)

# Consecutive numbers around an average.
_row = lambda cells, note, hl=None: table([cells], note, hl)
E["EXT_G5_WS_B2_012"] = entry(
    figure=_row(["?", "□", "□", "□", "□"], "5 numbers in a row. Their average is 24."),
    steps=[
        _row(["?", "□", "24", "□", "□"], "The average of 5 numbers in a row is the middle one"),
        _row(["22", "23", "24", "25", "26"], "Count back and forward from 24"),
        _row(["22", "23", "24", "25", "26"], "Smallest = 22", ["r0"]),
    ],
)
E["EXT_G5_WS_B2_013"] = entry(steps=[
    nl(25, 37, 2, points=[(31, "middle")], note="The middle of the 7 numbers is the average, 31"),
    nl(25, 37, 2, points=[(25,), (27,), (29,), (31, "middle"), (33,), (35,)], hops=[(35, 37, "+ 2")],
       note="Odd numbers go up in 2s on both sides of 31"),
    nl(25, 37, 2, points=[(31, "middle"), (37, "largest")], note="Largest = 37", hl=["p1"]),
])
E["EXT_G5_WS_B2_014"] = entry(
    figure=_row(["□", "□", "□", "?", "□"], "Even numbers in a row that add up to 80"),
    steps=[
        _row(["□", "□", "16", "?", "□"], "80 ÷ 5 = 16 is the middle number"),
        _row(["12", "14", "16", "18", "20"], "Even numbers go up in 2s"),
        _row(["12", "14", "16", "18", "20"], "The 4th number is 18", ["r0"]),
        None,
    ],
)

# Ages.
E["EXT_G5_WS_B2_015"] = entry(
    figure=nl(0, 20, 1, points=[(17, "in 6 years")], note="Go back 6 years to now, then 8 more years"),
    steps=[
        nl(0, 20, 1, points=[(17, "in 6 years"), (11, "now")], hops=[(17, 11, "− 6")], note="Now: 17 − 6 = 11 years"),
        nl(0, 20, 1, points=[(11, "now"), (3, "8 years ago")], hops=[(11, 3, "− 8")], note="8 years ago: 11 − 8 = 3 years"),
    ],
)

def _two(brace, note, hl=None):
    return bm([bar([seg("Disha", 3, "a"), seg("Nisha", 3, "b")], label="Now", brace="25 years"),
               bar([seg("Disha − 4", 2.5, "a"), seg("Nisha − 4", 2.5, "b")], label="4 years ago", brace=brace)], note, hl)

E["EXT_G5_WS_B2_016"] = entry(
    figure=_two("?", "Both girls were younger 4 years ago"),
    steps=[_two("?", "Each one was 4 years younger", ["b1"]), _two("17 years", "25 − 4 − 4 = 17", ["b1"])],
)

def _fam(add, brace, note, hl=None):
    return bm([bar([seg("Mr. Joshi", 3, "a"), seg("wife", 3, "b"), seg("son", 2, "c")], label="2020", brace="100 years"),
               bar([seg(add, 3, "a"), seg(add, 3, "b"), seg(add, 2, "c")], label="2028", brace=brace)], note, hl)

E["EXT_G5_WS_B2_017"] = entry(
    figure=_fam("older", "?", "Everyone grows older between 2020 and 2028"),
    steps=[
        _fam("+ 8", "?", "2028 − 2020 = 8 years later"),
        _fam("+ 8", "?", "3 people × 8 years = 24 years more", ["b1"]),
        _fam("+ 8", "124 years", "100 + 24 = 124"),
    ],
)

def _vv(now, ago, note, hl=None):
    return bm([bar([seg("Vijay", 2, "a"), seg("Vinay", 2, "b")], label="5 years ago", brace=ago),
               bar([seg("Vijay", 2.5, "a"), seg("Vinay", 2.5, "b")], label="Now", brace=now),
               bar([seg("Vijay", 3, "a"), seg("Vinay", 3, "b")], label="In 4 years", brace="67 years")], note, hl)

E["EXT_G5_WS_B2_018"] = entry(
    figure=_vv("?", "?", "Work back from the sum in 4 years"),
    steps=[
        _vv("59 years", "?", "Both are 4 years younger now: 67 − 2 × 4 = 59", ["b1"]),
        _vv("59 years", "49 years", "Both were 5 years younger: 59 − 2 × 5 = 49", ["b0"]),
        None,
    ],
)

def _as(a15, s15, born, note, hl=None):
    rows = [["2005", "37", "?"], ["2015", a15, s15]]
    if born:
        rows.insert(0, [born, "·", "0"])
    return table(rows, note, hl, headers=["Year", "Aman", "Suman"])

E["EXT_G5_WS_B2_019"] = entry(
    figure=_as("?", "?", None, "In 2015 the two ages add up to 87"),
    steps=[
        _as("47", "?", None, "10 years on from 2005: 37 + 10 = 47", ["r1"]),
        _as("47", "40", None, "87 − 47 = 40", ["r1"]),
        _as("47", "40", "1975", "Born 40 years before 2015: 2015 − 40 = 1975", ["r0"]),
    ],
)

# Three bags, two overlapping pairs.
def _bags(second, note, hl=None):
    return bm([bar([seg("first", 2, "a"), seg(second, 2, "b"), seg("third", 2, "c")], label="All three", brace="27 oranges"),
               bar([seg("first", 2, "a"), seg(second, 2, "b")], label="first + second", brace="13 oranges"),
               bar([seg(second, 2, "b"), seg("third", 2, "c")], label="second + third", brace="19 oranges")], note, hl)

E["EXT_G5_WS_B2_021"] = entry(
    figure=_bags("second", "The second bag is in both pairs. First + third = ?"),
    steps=[
        _bags("5", "The second bag is counted twice: 13 + 19 − 27 = 5", ["b0s1"]),
        _bags("5", "First + third = 27 − 5 = 22", ["b0s0", "b0s2"]),
        None,
    ],
)

def _cls(boys, note, hl=None):
    return bm([bar([seg("42", 4, "a")], label="Girls"),
               bar([seg(boys, 2.5, "b"), seg("11 fewer", 1.5, "unknown")], label="Boys")], note, hl)

E["EXT_G5_WS_B2_022"] = entry(
    figure=_cls("?", "Whole class = girls + boys = ?"),
    steps=[_cls("31", "Boys = 42 − 11 = 31", ["b1s0"]), _cls("31", "Class = 42 + 31 = 73")],
)

def _votes(brace, note, hl=None):
    return bm([bar([seg("275", 4, "a")], label="A"),
               bar([seg("275", 4, "a"), seg("35", 1, "b")], label="B", brace=brace)], note, hl)

E["EXT_G5_WS_B2_023"] = entry(
    figure=_votes(None, "B got 35 more votes than A. Total votes = ?"),
    steps=[_votes("310", "B = 275 + 35 = 310", ["b1"]), _votes("310", "Total = 275 + 310 = 585"), None],
)

# Account slip: the 600 went the opposite way, so the balance is out by two lots of 600.
E["EXT_G5_WS_B2_024"] = entry(steps=[
    nl(13800, 15000, 600, points=[(15000, "shown")], hops=[(15000, 14400, "undo the + 600")],
       note="600 was added but should have been taken away"),
    nl(13800, 15000, 600, points=[(15000, "shown"), (13800, "correct")],
       hops=[(15000, 14400, "undo the + 600"), (14400, 13800, "now − 600")], note="15000 − 1200 = 13800"),
    None,
])
E["EXT_G5_WS_B2_025"] = entry(steps=[
    nl(15000, 16200, 600, points=[(15000, "shown")], hops=[(15000, 15600, "undo the − 600")],
       note="600 was taken away but should have been added"),
    nl(15000, 16200, 600, points=[(15000, "shown"), (16200, "correct")],
       hops=[(15000, 15600, "undo the − 600"), (15600, 16200, "now + 600")], note="15000 + 1200 = 16200"),
    None,
])

E["EXT_G5_WS_B2_026"] = entry(
    figure=venn("Delhi", "Kashmir", "?", "6", "?", "40 students. 18 went to Delhi, 15 to Kashmir, 6 to both."),
    steps=[
        venn("Delhi", "Kashmir", "18 − 6", "6", "15 − 6", "At least one place: 18 + 15 − 6 = 27"),
        venn("Delhi", "Kashmir", "18 − 6", "6", "15 − 6", "Outside both circles: 40 − 27 = 13"),
        None,
    ],
)
E["EXT_G5_WS_B2_027"] = entry(
    figure=venn("Hindi", "Marathi", "?", "5", "?", "30 students. The Hindi circle holds 21 in all."),
    steps=[
        venn("Hindi", "Marathi", "16", "5", "?", "Hindi only = 21 − 5 = 16", ["left"]),
        venn("Hindi", "Marathi", "16", "5", "9", "Marathi only = 30 − 16 − 5 = 9", ["right"]),
        None,
    ],
)

# Four players: every line joining two of them is one game.
_sq = lambda note: {"kind": "polygon", "points": [[2, 2], [10, 2], [10, 10], [2, 10]],
                    "corners": ["A", "B", "C", "D"], "dashed": [{"from": 0, "to": 2}, {"from": 1, "to": 3}], "note": note}
E["EXT_G5_WS_B2_029"] = entry(steps=[
    _sq("Each line joins 2 of the 4 players: that is one game"),
    _sq("4 × 3 ÷ 2 = 6 lines, so 6 games"),
    None,
])
