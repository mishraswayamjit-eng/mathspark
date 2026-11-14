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
        bm([bar([seg("× 2") for _ in range(6)], label="2 hours", brace="1 becomes 64")],
           "Double 6 times: 64 amoebas"),
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
        _pair("Smaller", "Larger", "n", "2", "n + (n + 2) = 124"),
        _pair("Smaller", "Larger", "n", "2", "Without the extra 2, two equal parts make 122", ["b0s0", "b1s0"]),
        _pair("Smaller", "Larger", "61", "2", "n = 61, the smaller number", ["b0"]),
    ],
)
E["EXT_G5_WS_B3_027"] = entry(
    figure=_pair("Smaller", "Larger", "?", "9", "Multiples of 9 next to each other. Together 153."),
    steps=[
        _pair("Smaller", "Larger", "9k", "9", "9k + 9(k + 1) = 153"),
        _pair("Smaller", "Larger", "9k", "9", "18k + 9 = 153, so k = 8"),
        _pair("Smaller", "Larger", "72", "9", "Larger = 72 + 9 = 81", ["b1"], brace1="81"),
    ],
)
E["EXT_G5_WS_B3_028"] = entry(
    figure=_pair("Diya", "Siya", "?", "3", "Siya is always 3 years older. Together 35 years now."),
    steps=[
        _pair("Diya", "Siya", "D", "3", "The age gap never changes: S = D + 3"),
        _pair("Diya", "Siya", "16", "3", "D + D + 3 = 35, so D = 16 and Siya = 19", ["b1"], brace1="19 years"),
        None,
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
        _fruit("20", "?", "Apples: 85 − 45 = 40 for two, so Rs. 20 each", ["b0s0", "b0s1"]),
        _fruit("20", "Rs. 90", "3 apples + 2 oranges = 60 + 30 = 90", ["b1"]),
        None,
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
        _stairs("27 steps", "Middle step = (27 + 1) ÷ 2 = 14th"),
        None,
    ],
)

def _queue(brace, note, hl=None):
    return bm([bar([seg("in front", 4, "a"), seg("Nisha", 1, "b"), seg("behind", 2.5, "c")],
                   label="Queue", brace=brace)], note, hl)

E["EXT_G5_WS_B3_035"] = entry(
    figure=_queue("? people", "Nisha is 19th from the front and 11th from the back"),
    steps=[
        _queue("29 people", "19 + 11 counts Nisha twice: 19 + 11 − 1 = 29", ["b0s1"]),
        _queue("29 people", "The middle of 29 people is the 15th: Disha"),
        nl(14, 20, 1, points=[(15, "Disha"), (19, "Nisha")], note="Count the places between the 15th and the 19th"),
        nl(14, 20, 1, points=[(15, "Disha"), (19, "Nisha")], note="Three places lie between them, so 3 people"),
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
