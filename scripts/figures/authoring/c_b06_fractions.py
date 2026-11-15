"""Batch 6: worksheet B7: fractions and fraction word problems."""
from c_lib import *

E = {}

# Which fraction lies between 1/3 and 5/8?
E["EXT_G5_WS_B7_014"] = entry(
    figure=fb([(3, 1, "1/3"), (8, 5, "5/8")], "Which fraction is bigger than the top bar, smaller than the bottom?"),
    steps=[
        fb([(24, 8, "1/3 = 8/24"), (24, 15, "5/8 = 15/24")], "In twenty-fourths the top must be between 8 and 15"),
        fb([(24, 4, "1/6 = 4/24"), (24, 8, "1/3 = 8/24"), (24, 15, "5/8 = 15/24"), (24, 22, "11/12 = 22/24")],
           "1/6 is too small and 11/12 is too big", ["b0", "b3"]),
        fb([(24, 8, "1/3 = 8/24"), (24, 15, "5/8 = 15/24"), (24, 17, "17/24")], "17 is more than 15, so 17/24 is too big", ["b2"]),
        fb([(24, 8, "1/3 = 8/24"), (24, 13, "13/24"), (24, 15, "5/8 = 15/24")], "13 lies between 8 and 15", ["b1"]),
    ],
)

# Mixed numbers as wholes plus a part.
E["EXT_G5_WS_B7_016"] = entry(steps=[
    None,
    fb([(8, 8, "1 whole = 8/8"), (8, 3, "3/8")], "8 eighths + 3 eighths = 11 eighths"),
    None,
])
E["EXT_G5_WS_B7_017"] = entry(steps=[
    None,
    fb([(5, 5, "1 whole"), (5, 5, "1 whole"), (5, 5, "1 whole"), (5, 1, "1/5")], "15 fifths + 1 fifth = 16 fifths"),
    None,
])

E["EXT_G5_WS_B7_018"] = entry(steps=[
    None,
    None,
    fb([(9, 7, "7/9"), (9, 2, "2/9")], "7 ninths and 2 ninths make 9 ninths: one whole"),
])

E["EXT_G5_WS_B7_024"] = entry(
    figure=fb([(12, 11, "x = 11/12"), (3, 2, "y = 2/3"), (4, 1, "z = 1/4")], "Find x − y + z"),
    steps=[
        fb([(12, 11, "x = 11/12"), (3, 2, "y = 2/3"), (4, 1, "z = 1/4")], "x − y + z is 11/12 − 2/3 + 1/4"),
        fb([(12, 11, "x = 11/12"), (12, 8, "y = 8/12"), (12, 3, "z = 3/12")], "Cut every bar into 12 equal parts"),
        fb([(12, 6, "6/12")], "11 − 8 + 3 = 6 twelfths"),
        fb([(12, 6, "6/12"), (2, 1, "1/2")], "6/12 is the same as 1/2"),
    ],
)

# Four-ninths of a number is 24 (the fraction is in words, so the before-figure carries no numbers).
def _ninths(dark, light, brace, note, hl=None):
    segs = [seg(dark, tone="a") for _ in range(4)] + [seg(light, tone="b") for _ in range(5)]
    return bm([bar(segs, label="The number", brace=brace)], note, hl)

E["EXT_G5_WS_B7_028"] = entry(
    figure=_ninths(None, None, "?", "The darker parts together are 24. Half of the whole bar = ?"),
    steps=[
        _ninths(None, None, "?", "4 of the 9 equal parts make 24", ["b0s0", "b0s1", "b0s2", "b0s3"]),
        _ninths("6", None, "?", "One part = 24 ÷ 4 = 6"),
        _ninths("6", "6", "54", "All 9 parts: 9 × 6 = 54"),
        _ninths("6", "6", "54", "Half of 54 = 54 ÷ 2 = 27"),
    ],
)

EMPTY = ["b0s4", "b0s5", "b0s6"]
def _tank(full, empty, brace, note, hl=None):
    segs = [seg(full, tone="a") for _ in range(4)] + [seg(empty, tone="unknown") for _ in range(3)]
    return bm([bar(segs, label="Tank", brace=brace)], note, hl)

E["EXT_G5_WS_B7_030"] = entry(
    figure=_tank("full", "empty", "? litres", "The tank is 4/7 full. The empty parts need 120 litres."),
    steps=[
        _tank("full", "empty", "? litres", "Empty part: 7/7 − 4/7 = 3/7 of the tank", EMPTY),
        _tank("full", "40", "? litres", "3/7 holds 120 litres, so one part is 120 ÷ 3 = 40", EMPTY),
        _tank("40", "40", "280 litres", "All 7 parts: 7 × 40 = 280"),
        None,
    ],
)

def _bank(out, left, note, hl=None):
    segs = [seg(out, tone="a") for _ in range(3)] + [seg(left, tone="unknown") for _ in range(2)]
    return bm([bar(segs, label="Account")], note, hl)

E["EXT_G5_WS_B7_031"] = entry(
    figure=_bank("taken out", "left", "The parts taken out come to Rs. 2700. How much is left?"),
    steps=[
        _bank("taken out", "left", "3 of the 5 equal parts make Rs. 2700", ["b0s0", "b0s1", "b0s2"]),
        _bank("900", "left", "One part = 2700 ÷ 3 = 900"),
        _bank("900", "left", "5 − 3 = 2 parts are left in the account", ["b0s3", "b0s4"]),
        _bank("900", "900", "2 × 900 = 1800 left", ["b0s3", "b0s4"]),
    ],
)

def _class(a, b, c, brace, note, hl=None):
    segs = ([seg(a, tone="a") for _ in range(3)] + [seg(b, tone="b") for _ in range(2)]
            + [seg(c, tone="c") for _ in range(2)])
    return bm([bar(segs, label="Class", brace=brace)], note, hl)

E["EXT_G5_WS_B7_032"] = entry(
    figure=_class("library", "lab", "play", "? students", "3/7 library, two-sevenths lab. The rest, 14 students, play."),
    steps=[
        _class("library", "lab", "play", None, "Library and lab together: 3/7 + 2/7 = 5/7",
               ["b0s0", "b0s1", "b0s2", "b0s3", "b0s4"]),
        _class("library", "lab", "play", None, "Playground: 7/7 − 5/7 = 2/7, and that is 14 students", ["b0s5", "b0s6"]),
        _class("library", "lab", "7", None, "One part: 14 ÷ 2 = 7 students", ["b0s5", "b0s6"]),
        _class("7", "lab", "7", None, "Library = 3 parts: 3 × 7 = 21", ["b0s0", "b0s1", "b0s2"]),
    ],
)

def _garden(sm, hib, note, hl=None):
    sun, mari = ("sun", "mari") if sm is None else (sm, sm)
    segs = ([seg("rose", tone="a") for _ in range(2)] + [seg(sun, tone="b")]
            + [seg(mari, tone="c") for _ in range(4)] + [seg(hib, tone="unknown") for _ in range(2)])
    return bm([bar(segs, label="Garden")], note, hl)

E["EXT_G5_WS_B7_033"] = entry(
    figure=bm([bar([seg("rose", tone="a") for _ in range(2)] + [seg("sun", tone="b")]
                   + [seg("mari", tone="c") for _ in range(4)] + [seg("hib", tone="unknown") for _ in range(2)],
                   label="Garden", brace="? plants")], "9 equal parts. The hibiscus parts are 30 plants."),
    steps=[
        _garden(None, "hib", "Roses, sunflowers, marigolds: 2/9 + 1/9 + 4/9 = 7/9",
                ["b0s0", "b0s1", "b0s2", "b0s3", "b0s4", "b0s5", "b0s6"]),
        _garden(None, "hib", "Hibiscus: 9/9 − 7/9 = 2/9, and that is 30 plants", ["b0s7", "b0s8"]),
        _garden(None, "15", "One part: 30 ÷ 2 = 15 plants", ["b0s7", "b0s8"]),
        _garden("15", "15", "Sunflower + marigold: 5 parts, 5 × 15 = 75", ["b0s2", "b0s3", "b0s4", "b0s5", "b0s6"]),
        None,
    ],
)

E["EXT_G5_WS_B7_034"] = entry(
    figure=fb([(8, 5, "120 litres"), (3, 2, "? litres")], "Same tank: 5/8 full, then 2/3 full"),
    steps=[
        fb([(8, 5, "120 litres"), (3, 2, "? litres")], "5 parts hold 120, so one part is 120 ÷ 5 = 24 litres", ["b0"]),
        fb([(8, 8, "192 litres"), (3, 2, "? litres")], "Full tank = 8 parts: 8 × 24 = 192 litres", ["b0"]),
        fb([(8, 8, "192 litres"), (3, 2, "128 litres")], "192 ÷ 3 = 64, and 2 × 64 = 128 litres", ["b1"]),
        None,
    ],
)

def _zoo(a, c, brace, note, hl=None):
    segs = [seg(a, tone="a") for _ in range(3)] + [seg(c, tone="b") for _ in range(2)]
    return bm([bar(segs, label="Visitors", brace=brace)], note, hl)

E["EXT_G5_WS_B7_035"] = entry(
    figure=_zoo("adults", "children", "? visitors", "3/5 are adults. The children parts are 120."),
    steps=[
        _zoo("adults", "children", None, "Children: 5/5 − 3/5 = 2/5, and that is 120", ["b0s3", "b0s4"]),
        _zoo("60", "60", None, "One part: 120 ÷ 2 = 60. Adults: 3 × 60 = 180", ["b0s0", "b0s1", "b0s2"]),
        bm([bar([seg("20", tone="a") for _ in range(5)] + [seg("20", tone="b") for _ in range(4)],
                label="Adults", brace="180 adults")], "One ninth of 180 is 180 ÷ 9 = 20"),
        bm([bar([seg("20", tone="a") for _ in range(5)] + [seg("20", tone="b") for _ in range(4)],
                label="Adults", brace="180 adults")], "Female adults: 5 × 20 = 100",
           ["b0s0", "b0s1", "b0s2", "b0s3", "b0s4"]),
    ],
)

def _fifths(note, hl=None):
    return bm([bar([seg("72", tone="a"), seg("72", tone="a"), seg("72", tone="b"), seg("72", tone="b"), seg("72", tone="b")],
                   label="Stock", brace="360 kg")], note, hl)

def _quarters(note, hl=None):
    return bm([bar([seg("54", tone="a"), seg("54", tone="b"), seg("54", tone="b"), seg("54", tone="b")],
                   label="Remaining", brace="216 kg")], note, hl)

E["EXT_G5_WS_B7_036"] = entry(
    figure=bm([bar([seg("308 kg", 3, "a"), seg("52 kg", 1, "b")], label="Stock", brace="total = ?")],
              "First 2/5 of the total is sold, then a quarter of the rest"),
    steps=[
        bm([bar([seg("308 kg", 3, "a"), seg("52 kg", 1, "b")], label="Stock", brace="360 kg")], "Total: 308 + 52 = 360 kg"),
        _fifths("One fifth: 360 ÷ 5 = 72. Joshi buys 2 × 72 = 144 kg", ["b0s0", "b0s1"]),
        _fifths("Remaining: 360 − 144 = 216 kg", ["b0s2", "b0s3", "b0s4"]),
        _quarters("Shinde buys a quarter: 216 ÷ 4 = 54 kg", ["b0s0"]),
        _quarters("Left: 216 − 54 = 162 kg", ["b0s1", "b0s2", "b0s3"]),
    ],
)
