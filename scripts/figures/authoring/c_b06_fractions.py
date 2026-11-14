"""Batch 6: worksheet B7: fractions and fraction word problems."""
from c_lib import *

E = {}

# Which fraction lies between 1/3 and 5/8?
E["EXT_G5_WS_B7_014"] = entry(
    figure=fb([(3, 1, "1/3"), (8, 5, "5/8")], "Which fraction is bigger than the top bar, smaller than the bottom?"),
    steps=[
        fb([(3, 1, "1/3"), (8, 5, "5/8")], "The answer must lie between these two"),
        fb([(3, 1, "1/3"), (24, 13, "13/24"), (8, 5, "5/8")], "13/24 sits between them", ["b1"]),
        None,
    ],
)

E["EXT_G5_WS_B7_018"] = entry(steps=[
    None,
    fb([(9, 7, "7/9"), (9, 2, "2/9")], "7 ninths and 2 ninths make 9 ninths: one whole"),
])

E["EXT_G5_WS_B7_024"] = entry(
    figure=fb([(12, 11, "x = 11/12"), (3, 2, "y = 2/3"), (4, 1, "z = 1/4")], "Find x − y + z"),
    steps=[
        fb([(12, 11, "x = 11/12"), (12, 8, "y = 8/12"), (12, 3, "z = 3/12")], "Cut every bar into 12 equal parts"),
        fb([(12, 6, "6/12 = 1/2")], "11 − 8 + 3 = 6 twelfths, which is one half"),
        None,
    ],
)

# Four-ninths of a number is 24 (the fraction is in words, so the bar carries no numbers).
def _ninths(brace, note, hl=None):
    segs = [seg(tone="a") for _ in range(4)] + [seg(tone="b") for _ in range(5)]
    return bm([bar(segs, label="The number", brace=brace)], note, hl)

E["EXT_G5_WS_B7_028"] = entry(
    figure=_ninths("?", "The darker parts together are 24. Half of the whole bar = ?"),
    steps=[
        _ninths("54", "4 of the 9 parts are 24, so the number is 24 × 9/4 = 54"),
        _ninths("54", "Half of 54 = 27"),
    ],
)

def _tank(brace, note, hl=None):
    segs = [seg("full", tone="a") for _ in range(4)] + [seg("empty", tone="unknown") for _ in range(3)]
    return bm([bar(segs, label="Tank", brace=brace)], note, hl)

E["EXT_G5_WS_B7_030"] = entry(
    figure=_tank("? litres", "The tank is 4/7 full. The empty parts need 120 litres."),
    steps=[
        _tank("? litres", "3/7 of the tank = 120 litres", ["b0s4", "b0s5", "b0s6"]),
        _tank("280 litres", "Whole tank = 120 × 7/3 = 280 litres"),
        None,
    ],
)

def _bank(brace, left, note, hl=None):
    segs = [seg("taken out", tone="a") for _ in range(3)] + [seg(left, tone="unknown") for _ in range(2)]
    return bm([bar(segs, label="Account", brace=brace)], note, hl)

E["EXT_G5_WS_B7_031"] = entry(
    figure=_bank("?", "left", "The parts taken out come to Rs. 2700. How much is left?"),
    steps=[
        _bank("Rs. 4500", "left", "Whole amount = 2700 × 5/3 = 4500"),
        _bank("Rs. 4500", "left", "Left = 4500 − 2700 = 1800", ["b0s3", "b0s4"]),
        None,
    ],
)

def _class(brace, note, hl=None):
    segs = ([seg("library", tone="a") for _ in range(3)] + [seg("lab", tone="b") for _ in range(2)]
            + [seg("play", tone="c") for _ in range(2)])
    return bm([bar(segs, label="Class", brace=brace)], note, hl)

E["EXT_G5_WS_B7_032"] = entry(
    figure=_class("? students", "3/7 library, two-sevenths lab. The rest, 14 students, play."),
    steps=[
        _class("? students", "Playground: 2/7 of the class = 14", ["b0s5", "b0s6"]),
        _class("49 students", "Whole class = 49"),
        _class("49 students", "Library = 3/7 × 49 = 21", ["b0s0", "b0s1", "b0s2"]),
    ],
)

def _garden(brace, note, hl=None):
    segs = ([seg("rose", tone="a") for _ in range(2)] + [seg("sun", tone="b")]
            + [seg("mari", tone="c") for _ in range(4)] + [seg("hib", tone="unknown") for _ in range(2)])
    return bm([bar(segs, label="Garden", brace=brace)], note, hl)

E["EXT_G5_WS_B7_033"] = entry(
    figure=_garden("? plants", "9 equal parts. The hibiscus parts are 30 plants."),
    steps=[
        _garden("135 plants", "Hibiscus: 2/9 of the garden = 30, so 135 plants in all", ["b0s7", "b0s8"]),
        _garden("135 plants", "Sunflower + marigold = 5/9 × 135 = 75", ["b0s2", "b0s3", "b0s4", "b0s5", "b0s6"]),
        None,
    ],
)

E["EXT_G5_WS_B7_034"] = entry(
    figure=fb([(8, 5, "120 litres"), (3, 2, "? litres")], "Same tank: 5/8 full, then 2/3 full"),
    steps=[
        fb([(8, 5, "120 litres"), (3, 2, "? litres")], "Whole tank = 120 × 8/5 = 192 litres", ["b0"]),
        fb([(8, 5, "120 litres"), (3, 2, "128 litres")], "2/3 × 192 = 128 litres", ["b1"]),
        None,
    ],
)

def _zoo(brace, note, hl=None):
    segs = [seg("adults", tone="a") for _ in range(3)] + [seg("children", tone="b") for _ in range(2)]
    return bm([bar(segs, label="Visitors", brace=brace)], note, hl)

E["EXT_G5_WS_B7_035"] = entry(
    figure=_zoo("? visitors", "3/5 are adults. The children parts are 120."),
    steps=[
        _zoo("300 visitors", "Children: 2/5 of all = 120, so 300 visitors", ["b0s3", "b0s4"]),
        _zoo("300 visitors", "Adults = 180", ["b0s0", "b0s1", "b0s2"]),
        fb([(9, 5, "female adults")], "5/9 of the 180 adults = 100"),
    ],
)

E["EXT_G5_WS_B7_036"] = entry(
    figure=bm([bar([seg("308 kg", 3, "a"), seg("52 kg", 1, "b")], label="Stock", brace="total = ?")],
              "First 2/5 of the total is sold, then a quarter of the rest"),
    steps=[
        bm([bar([seg("308 kg", 3, "a"), seg("52 kg", 1, "b")], label="Stock", brace="360 kg")], "Total = 360 kg"),
        bm([bar([seg("Joshi", tone="a"), seg("Joshi", tone="a"), seg("rest", tone="b"), seg("rest", tone="b"),
                 seg("rest", tone="b")], label="Stock", brace="360 kg")], "Joshi: 2/5 × 360 = 144. Rest = 216"),
        bm([bar([seg("Shinde", tone="a"), seg("left", tone="b"), seg("left", tone="b"), seg("left", tone="b")],
                label="The rest", brace="216 kg")], "Shinde: 1/4 × 216 = 54. Left = 162 kg"),
    ],
)
