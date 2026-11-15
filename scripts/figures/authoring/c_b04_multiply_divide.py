"""Batch 4: worksheet B3: multiplication and division word problems, sums with a difference, positions, rates."""
from c_lib import *

E = {}

# Amoeba doubling every 20 minutes ("two hours" and "one amoeba" are in words).
E["EXT_G5_WS_B3_004"] = entry(
    figure=nl(0, 120, 20, points=[(0, "start")], hops=[(0, 20, "× 2")],
              note="The number doubles every 20 minutes"),
    steps=[
        bm([bar([seg("× 2") for _ in range(6)], label="2 hours", brace="120 min = 6 doublings")],
           "120 ÷ 20 = 6 doublings"),
        bm([bar([seg(n) for n in ["2", "4", "8", "16", "32", "64"]], label="2 hours", brace="6 doublings")],
           "Start with 1 and double 6 times"),
        bm([bar([seg(n) for n in ["2", "4", "8", "16", "32", "64"]], label="2 hours", brace="6 doublings")],
           "After two hours there are 64 amoebas", ["b0s5"]),
    ],
)

# 10 m of wire cut into 7 equal whole-centimetre pieces, with a little left over.
def _wire(piece, left, brace, note, hl=None):
    return bm([bar([seg(piece, 1, "a") for _ in range(7)] + [seg(left, 0.6, "unknown")], label="Wire", brace=brace)], note, hl)

E["EXT_G5_WS_B3_012"] = entry(
    figure=_wire(None, "?", "10 m", "7 equal pieces, each a whole number of centimetres"),
    steps=[
        _wire(None, "?", "1000 cm", "10 m = 1000 cm"),
        _wire("142", "?", "1000 cm", "Longest pieces that fit: 7 × 142 = 994 cm", ["b0s0"]),
        _wire("142", "6 cm", "1000 cm", "Left over: 1000 − 994 = 6 cm", ["b0s7"]),
    ],
)

# 56 apples leave 4 at a time; 3 oranges go in each time.
def _swap(turns, oranges, note, hl=None):
    return table([["each turn", "4 apples out", "3 oranges in"], [turns, "56 apples out", oranges]], note, hl)

E["EXT_G5_WS_B3_025"] = entry(
    figure=_swap("all the turns", "? oranges in", "How many turns does it take to empty the apples?"),
    steps=[
        _swap("14 turns", "? oranges in", "56 ÷ 4 = 14 turns", ["r1"]),
        _swap("14 turns", "42 oranges in", "14 × 3 = 42 oranges", ["r1"]),
        None,
    ],
)

def _cups(jug, bucket, two, note, hl=None):
    return table([["1 bottle", "4 cups"], ["1 jug", jug], ["1 bucket", bucket], ["2 buckets", two]], note, hl)

E["EXT_G5_WS_B3_006"] = entry(
    figure=_cups("3 bottles", "7 jugs", "? cups", "Turn everything into cups, one row at a time"),
    steps=[
        _cups("12 cups", "7 jugs", "? cups", "1 jug = 3 bottles = 12 cups", ["r1"]),
        _cups("12 cups", "84 cups", "? cups", "1 bucket = 7 jugs = 84 cups", ["r2"]),
        _cups("12 cups", "84 cups", "168 cups", "2 buckets = 168 cups", ["r3"]),
    ],
)

E["EXT_G5_WS_B3_021"] = entry(
    figure=bm([bar([seg("1 min"), seg("1 min"), seg("1 min")], brace="126 words")],
              "126 words in 3 minutes. How many in half a minute?"),
    steps=[
        bm([bar([seg("42"), seg("42"), seg("42")], brace="126 words")], "One minute: 126 ÷ 3 = 42 words"),
        bm([bar([seg("21", 0.5, "b"), seg("21", 0.5), seg("42"), seg("42")], brace="126 words")],
           "Half a minute: 42 ÷ 2 = 21 words", ["b0s0"]),
    ],
)

# Two unknowns with a known sum and a known difference.
def _pair(l0, l1, small, extra, note, hl=None, brace1=None):
    return bm([bar([seg(small, 3, "a")], label=l0),
               bar([seg(small, 3, "a"), seg(extra, 1, "b")], label=l1, brace=brace1)], note, hl)

E["EXT_G5_WS_B3_026"] = entry(
    figure=_pair("Smaller", "Larger", "?", "2", "Odd numbers next to each other. Together they make 124."),
    steps=[
        nl(58, 66, 1, points=[(62, "half of 124")], note="124 ÷ 2 = 62. The two numbers sit either side of 62."),
        nl(58, 66, 1, points=[(61, "61"), (62, "half"), (63, "63")], note="Odd numbers either side of 62: 61 + 63 = 124",
           hl=["p0", "p2"]),
        _pair("Smaller", "Larger", "61", "2", "The smaller number is 61", ["b0"]),
    ],
)
E["EXT_G5_WS_B3_027"] = entry(
    figure=_pair("Smaller", "Larger", "?", "9", "Multiples of 9 next to each other. Together 153."),
    steps=[
        _pair("Smaller", "Larger", "?", "9", "Take the extra 9 away: 153 − 9 = 144", ["b1s1"]),
        _pair("Smaller", "Larger", "72", "9", "Two equal parts: 144 ÷ 2 = 72", ["b0s0", "b1s0"]),
        _pair("Smaller", "Larger", "72", "9", "Larger = 72 + 9 = 81", ["b1"], brace1="81"),
    ],
)
E["EXT_G5_WS_B3_028"] = entry(
    figure=_pair("Diya", "Siya", "?", "3", "Siya is always 3 years older. Together 35 years now."),
    steps=[
        _pair("Diya", "Siya", "?", "3", "The age gap never changes: Siya is 3 years older now too"),
        _pair("Diya", "Siya", "16", "3", "35 − 3 = 32 is twice Diya's age: 32 ÷ 2 = 16", ["b0s0", "b1s0"]),
        _pair("Diya", "Siya", "16", "3", "Siya = 16 + 3 = 19", ["b1"], brace1="19 years"),
    ],
)
E["EXT_G5_WS_B3_029"] = entry(
    figure=_pair("Pencil", "Pen", "?", "Rs. 10", "Together they cost Rs. 18. Find the cost of 3 pencils."),
    steps=[
        _pair("Pencil", "Pen", "P", "Rs. 10", "P + (P + 10) = 18"),
        _pair("Pencil", "Pen", "Rs. 4", "Rs. 10", "2P = 8, so one pencil is Rs. 4", ["b0"]),
        bm([bar([seg("Rs. 4"), seg("Rs. 4"), seg("Rs. 4")], label="3 pencils", brace="Rs. 12")], "3 × 4 = Rs. 12"),
    ],
)
E["EXT_G5_WS_B3_030"] = entry(
    figure=_pair("Boys", "Girls", "?", "6", "Together: every medal from the 14 events"),
    steps=[
        _pair("Boys", "Girls", "?", "6", "14 events × 3 medals = 42 medals in all"),
        _pair("Boys", "Girls", "B", "6", "B + (B + 6) = 42"),
        _pair("Boys", "Girls", "18", "6", "2B = 36, so the boys won 18", ["b0"]),
    ],
)

def _fruit(apple, brace2, note, hl=None):
    return bm([bar([seg(apple, 1, "a"), seg(apple, 1, "a"), seg("15", 1, "b"), seg("15", 1, "b"), seg("15", 1, "b")],
                   label="2 apples 3 oranges", brace="Rs. 85"),
               bar([seg(apple, 1, "a"), seg(apple, 1, "a"), seg(apple, 1, "a"), seg("15", 1, "b"), seg("15", 1, "b")],
                   label="3 apples 2 oranges", brace=brace2)], note, hl)

E["EXT_G5_WS_B3_031"] = entry(
    figure=_fruit("?", "?", "Each orange costs Rs. 15. Find the apple price first."),
    steps=[
        _fruit("?", "?", "3 oranges: 3 × 15 = 45. So 2 apples: 85 − 45 = 40", ["b0s0", "b0s1"]),
        _fruit("20", "?", "One apple: 40 ÷ 2 = 20", ["b0s0", "b0s1"]),
        _fruit("20", "?", "3 apples: 3 × 20 = 60. 2 oranges: 2 × 15 = 30", ["b1"]),
        _fruit("20", "Rs. 90", "60 + 30 = 90", ["b1"]),
    ],
)

E["EXT_G5_WS_B3_032"] = entry(
    figure=bm([bar([seg("Rs. 5", 1, "a"), seg("Rs. 10", 1, "b"), seg("Rs. 20", 1, "c")], label="One set of notes", brace="?")],
              "Rs. 910 is made of equal sets like this one"),
    steps=[
        bm([bar([seg("Rs. 5", 1, "a"), seg("Rs. 10", 1, "b"), seg("Rs. 20", 1, "c")], label="One set of notes", brace="Rs. 35")],
           "One set: 5 + 10 + 20 = 35"),
        bm([bar([seg("Rs. 5", 1, "a"), seg("Rs. 10", 1, "b"), seg("Rs. 20", 1, "c")], label="One set of notes", brace="Rs. 35")],
           "910 ÷ 35 = 26 sets, so 26 notes of each kind"),
    ],
)
_st = lambda brace, note: bm([bar([seg("5 p", 1, "a"), seg("20 p", 1, "b"), seg("25 p", 1, "c")],
                                  label="One set of stamps", brace=brace)], note)
E["EXT_G5_WS_B3_033"] = entry(
    figure=_st("?", "Rs. 9 buys equal sets like this one"),
    steps=[
        _st("50 paise", "One set: 5 + 20 + 25 = 50 paise"),
        _st("50 paise", "Rs. 9 = 900 paise. 900 ÷ 50 = 18 sets"),
        _st("50 paise", "18 sets × 3 stamps = 54 stamps"),
    ],
)

# Positions counted from both ends.
def _stairs(brace, note, hl=None):
    return bm([bar([seg("below Manav", 2.5, "a"), seg("Manav", 1, "b"), seg("above Manav", 4, "c")],
                   label="Staircase", brace=brace)], note, hl)

E["EXT_G5_WS_B3_034"] = entry(
    figure=_stairs("? steps", "Manav's step is 11th from the bottom and 17th from the top"),
    steps=[
        _stairs("27 steps", "11 + 17 counts Manav's step twice: 11 + 17 − 1 = 27", ["b0s1"]),
        bm([bar([seg("13 steps", 3, "a"), seg("middle", 1, "b"), seg("13 steps", 3, "a")], label="Staircase", brace="27 steps")],
           "27 − 1 = 26, and 26 ÷ 2 = 13 steps on each side"),
        bm([bar([seg("13 steps", 3, "a"), seg("middle", 1, "b"), seg("13 steps", 3, "a")], label="Staircase", brace="27 steps")],
           "The middle step is the 14th from the bottom", ["b0s1"]),
    ],
)

def _queue(brace, note, hl=None):
    return bm([bar([seg("in front", 4, "a"), seg("Nisha", 1, "b"), seg("behind", 2.5, "c")],
                   label="Queue", brace=brace)], note, hl)

E["EXT_G5_WS_B3_035"] = entry(
    figure=_queue("? people", "Nisha is 19th from the front and 11th from the back"),
    steps=[
        _queue("29 people", "19 + 11 counts Nisha twice: 19 + 11 − 1 = 29", ["b0s1"]),
        bm([bar([seg("14 people", 3, "a"), seg("Disha", 1, "b"), seg("14 people", 3, "a")], label="Queue", brace="29 people")],
           "14 + 1 + 14 = 29, so Disha is 15th from the front", ["b0s1"]),
        nl(14, 20, 1, points=[(15, "Disha"), (16,), (17,), (18,), (19, "Nisha")],
           note="16th, 17th and 18th: 3 people between them", hl=["p1", "p2", "p3"]),
    ],
)

def _rice(note, last="?", hl=None):
    return table([["six people", "1 day", "1 kg"], ["24 people", "1 week", last]], note, hl, headers=["People", "Time", "Rice"])

E["EXT_G5_WS_B3_037"] = entry(
    figure=_rice("More people and more days both mean more rice"),
    steps=[
        setf(24, 4, "people", "24 people = 4 groups of 6, so 4 kg a day"),
        _rice("7 days × 4 kg a day = 28 kg", "28 kg", ["r1"]),
    ],
)

def _wage(a, b, note, hl=None):
    return bm([bar([seg(a, 2, "a"), seg(b, 2, "unknown")], label="Pay", brace="Rs. 336")], note, hl)

E["EXT_G5_WS_B3_038"] = entry(
    figure=_wage("30 h at Rs. 8", "overtime: ? h", "Overtime hours are paid at twice Rs. 8"),
    steps=[
        _wage("Rs. 240", "overtime: ? h", "Usual hours: 30 × 8 = 240", ["b0s0"]),
        _wage("Rs. 240", "Rs. 96", "Overtime pay: 336 − 240 = 96", ["b0s1"]),
        _wage("Rs. 240", "6 hours", "Overtime is Rs. 16 an hour: 96 ÷ 16 = 6 hours", ["b0s1"]),
    ],
)

def _school(girls, note, hl=None):
    return bm([bar([seg(tone="a") for _ in range(4)], label="Girls", brace=girls),
               bar([seg(tone="b") for _ in range(7)], label="Boys", brace="455")], note, hl)

E["EXT_G5_WS_B3_040"] = entry(
    figure=_school("?", "4 girls for every 7 boys. One teacher for every 55 students."),
    steps=[
        _school("260", "Girls = 455 × 4/7 = 260", ["b0"]),
        _school("260", "Students = 455 + 260 = 715"),
        _school("260", "Teachers = 715 ÷ 55 = 13"),
    ],
)
