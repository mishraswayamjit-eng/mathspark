"""Batch 2: place value, forming and counting numbers, column sums with missing digits."""
from c_lib import *

E = {}
PV = ["Ten Th", "Th", "H", "T", "U"]

# "Six hundred hundreds" is in words, so the picture only starts with the solution.
E["EXT_G5_WS_01_001"] = entry(steps=[
    pc("60000", "Six hundred hundreds = 600 × 100 = 60,000"),
    pc("60000", "60,000 ÷ 10 = 6000 tens", ["d0", "d1", "d2", "d3"]),
])

E["EXT_G5_WS_01_004"] = entry(
    figure=pc("69512", "Which digits sit in the greatest and the least places?"),
    steps=[
        pc("69512", "Greatest place is ten-thousands: digit 6", ["d0"]),
        pc("69512", "Least place is units: digit 2", ["d4"]),
        pc("69512", "6 − 2 = 4", ["d0", "d4"]),
    ],
)

E["EXT_G5_WS_01_005"] = entry(
    figure=pc("76025", "Compare the place value of 6 with that of 2", ["d1", "d3"]),
    steps=[
        pc("76025", "6 is in the thousands place", ["d1"]),
        pc("76025", "2 is in the tens place", ["d3"]),
        pc("76025", "6 thousands ÷ 2 tens = 300 times", ["d1", "d3"]),
    ],
)

E["EXT_G5_WS_01_006"] = entry(steps=[
    pc("68815", "8000 and 800: only 10 times", ["d1", "d2"]),
    pc("65818", "800 and 8: 100 times", ["d2", "d4"]),
    pc("81586", "80000 and 80: 1000 times", ["d0", "d3"]),
    pc("81586", "81586 is the one we want", ["d0", "d3"]),
])

E["EXT_G5_WS_01_007"] = entry(steps=[
    None,
    pc("134639", "30000 and 30: 1000 times, so not a match", ["d1", "d4"]),
    pc("307638", "300000 and 30: 10000 times, so not a match", ["d0", "d4"]),
    pc("863135", "3000 and 30: 3000 ÷ 30 = 100 times", ["d2", "d4"]),
])

_r = lambda cells, note: table([cells], note, headers=PV)
_r8 = lambda cells, note: table([cells], note, headers=["Ten Th", "Th", "H", "T and U"])
E["EXT_G5_WS_01_008"] = entry(
    figure=_r8(["7", "✻", "✻", "19"], "The two ✻ place values differ by 5400"),
    steps=[
        _r8(["7", "✻", "✻", "19"], "The ✻s are in the thousands and hundreds places"),
        _r8(["7", "d", "d", "19"], "d × 1000 − d × 100 = 900 × d"),
        balance("900 × d", "5400"),
        _r8(["7", "6", "6", "19"], "d = 5400 ÷ 900 = 6"),
    ],
)
E["EXT_G5_WS_01_009"] = entry(
    figure=_r(["3", "✻", "8", "✻", "2"], "The two ✻ place values differ by 6930"),
    steps=[
        _r(["3", "✻", "8", "✻", "2"], "The ✻s are in the thousands and tens places"),
        _r(["3", "d", "8", "d", "2"], "d × 1000 − d × 10 = 990 × d"),
        balance("990 × d", "6930"),
        _r(["3", "7", "8", "7", "2"], "d = 6930 ÷ 990 = 7"),
    ],
)
E["EXT_G5_WS_01_010"] = entry(
    figure=_r(["6", "✻", "8", "✻", "4"], "Both ✻ are the same digit"),
    steps=[
        _r(["6", "✻", "8", "✻", "4"], "The ✻s are in the thousands and tens places"),
        _r(["6", "d", "8", "d", "4"], "The difference is always the digit times 990"),
        _r(["6", "9", "8", "9", "4"], "990 × 9 = 8910, so the digit 9 gives 8910"),
        None,
    ],
)

E["EXT_G5_WS_01_012"] = entry(steps=[
    None,
    pc("87405", "Ending in 5, the rest from biggest to smallest", ["d4"]),
    pc("85407", "Ending in 7, the rest from biggest to smallest", ["d4"]),
    None,
    pc("87405", "The middle (3rd) digit is 4", ["d2"]),
])
E["EXT_G5_WS_01_013"] = entry(steps=[
    None,
    pc("36792", "Ending in 2, the rest from smallest to biggest", ["d4"]),
    pc("23796", "Ending in 6, the rest from smallest to biggest", ["d4"]),
    None,
    pc("23796", "7 is in the hundreds place: 700", ["d2"]),
])

_tu = lambda a, b, note: table([[a, b]], note, headers=["Tens", "Units"])
E["EXT_G5_WS_01_014"] = entry(
    figure=_tu("an odd digit", "an even digit", "How many choices are there for each place?"),
    steps=[
        _tu("1 3 5 7 9", "?", "5 choices for the tens place"),
        _tu("1 3 5 7 9", "0 2 4 6 8", "5 choices for the units place"),
        _tu("5 choices", "5 choices", "5 × 5 = 25 numbers"),
    ],
)

TH = ["Th", "H", "T", "U"]
E["EXT_G5_WS_01_015"] = entry(
    figure=table([["not 0", "?", "?", "?"]], "Digits 7, 0, 3, 9, each used once", headers=TH),
    steps=[
        table([["3 choices", "?", "?", "?"]], "7, 3 or 9 can go first", headers=TH),
        table([["3 choices", "3 choices", "2 choices", "1 choice"]], "Other three places: 3 × 2 × 1 = 6 ways", headers=TH),
        table([["3 choices", "3 choices", "2 choices", "1 choice"]], "3 × 6 = 18 numbers", headers=TH),
    ],
)
E["EXT_G5_WS_01_016"] = entry(
    figure=table([["?", "?", "?", "?"]], "Digits 2, 5, 0, 8 once each; number below 5000", headers=TH),
    steps=[
        table([["2", "?", "?", "?"]], "Only 2 can go in the thousands place", headers=TH),
        table([["2", "3 choices", "2 choices", "1 choice"]], "Other three places: 3 × 2 × 1 = 6 ways", headers=TH),
        table([["2", "0", "5", "8"], ["2", "0", "8", "5"], ["2", "5", "0", "8"], ["2", "5", "8", "0"],
               ["2", "8", "0", "5"], ["2", "8", "5", "0"]], "All 6 numbers below 5000", headers=TH),
    ],
)

E["EXT_G5_WS_B2_011"] = entry(
    figure=pc("469571", "Swap the 5 and the 6. Which places do they move between?", ["d1", "d3"]),
    steps=[
        pc("469571", "6 is in the ten-thousands place, 5 in the hundreds place", ["d1", "d3"]),
        pc("459671", "After the swap the number is 459671", ["d1", "d3"]),
        pc("459671", "Ten-thousands digit fell from 6 to 5, so it is smaller", ["d1"]),
        pc("459671", "469571 − 459671 = 9900 less", ["d1", "d3"]),
    ],
)

# The 23rd even number before 105.
E["EXT_G5_WS_01_018"] = entry(
    figure=nl(96, 106, 1, points=[(105, "105")], note="Count the even numbers going back from 105"),
    steps=[
        nl(96, 106, 1, points=[(105, "105"), (104, "1st")], note="105 is odd, so the 1st even number before it is 104"),
        nl(60, 106, 2, points=[(104, "1st")], hops=[(104, 60, "22 steps of 2")], note="From the 1st to the 23rd: 22 × 2 = 44 back"),
        nl(60, 106, 2, points=[(104, "1st"), (60, "23rd")], note="104 − 44 = 60", hl=["p1"]),
    ],
)

# Column sums with letters.
E["EXT_G5_WS_B2_001"] = entry(
    figure=table([["·", "A", "4", "8"], ["·", "3", "2", "B"], ["·", "5", "C", "1"], ["1", "4", "7", "8"]], "The first three rows add up to the last row",
                 headers=TH),
    steps=[
        table([["·", "A", "4", "8"], ["·", "3", "2", "9"], ["·", "5", "C", "1"], ["1", "4", "7", "8"]], "Units: 8 + 9 + 1 = 18. Write 8, carry 1. B = 9",
              headers=TH),
        table([["·", "A", "4", "8"], ["·", "3", "2", "9"], ["·", "5", "0", "1"], ["1", "4", "7", "8"]], "Tens: 4 + 2 + 0 + 1 = 7. C = 0",
              headers=TH),
        table([["·", "6", "4", "8"], ["·", "3", "2", "9"], ["·", "5", "0", "1"], ["1", "4", "7", "8"]], "Hundreds: 6 + 3 + 5 = 14. A = 6",
              headers=TH),
        table([["·", "6", "4", "8"], ["·", "3", "2", "9"], ["·", "5", "0", "1"], ["1", "4", "7", "8"]], "A = 6, B = 9, C = 0",
              headers=TH),
    ],
)

E["EXT_G5_WS_B2_002"] = entry(
    figure=table([["9", "8", "P", "3"], ["4", "5", "6", "2"], ["5", "Q", "8", "1"]],
                 "Top row − middle row = bottom row. Find P + Q.", headers=TH),
    steps=[
        table([["9", "8", "P", "3"], ["4", "5", "6", "2"], ["5", "Q", "8", "1"]], "Units: 3 − 2 = 1", headers=TH),
        table([["9", "8", "4", "3"], ["4", "5", "6", "2"], ["5", "Q", "8", "1"]], "Tens: borrow, 14 − 6 = 8. P = 4", headers=TH),
        table([["9", "8", "4", "3"], ["4", "5", "6", "2"], ["5", "2", "8", "1"]], "Hundreds: 7 − 5 = 2. Q = 2", headers=TH),
        table([["9", "8", "4", "3"], ["4", "5", "6", "2"], ["5", "2", "8", "1"]], "P + Q = 4 + 2 = 6", headers=TH),
    ],
)

# Long multiplication with missing digits.
# A table cell cannot be empty, so blank cells hold a middle dot.
C5 = lambda rows, note: table(rows, note)
E["EXT_G5_WS_B3_002"] = entry(
    figure=C5([["·", "·", "5", "✻", "7"], ["·", "·", "×", "4", "✻"], ["·", "✻", "5", "8", "✻"],
               ["✻", "✻", "0", "✻", "0"], ["2", "2", "✻", "6", "1"]],
              "The two middle rows add up to the product in the last row"),
    steps=[
        C5([["·", "·", "5", "✻", "7"], ["·", "·", "×", "4", "3"], ["·", "✻", "5", "8", "✻"],
            ["✻", "✻", "0", "✻", "0"], ["2", "2", "✻", "6", "1"]], "7 × 3 = 21 ends in 1, so the missing digit is 3"),
        C5([["·", "·", "5", "2", "7"], ["·", "·", "×", "4", "3"], ["·", "1", "5", "8", "1"],
            ["✻", "✻", "0", "✻", "0"], ["2", "2", "✻", "6", "1"]], "527 × 3 = 1581 fits the first row"),
        C5([["·", "·", "5", "2", "7"], ["·", "·", "×", "4", "3"], ["·", "1", "5", "8", "1"],
            ["2", "1", "0", "8", "0"], ["2", "2", "6", "6", "1"]], "527 × 43 = 22661"),
    ],
)
