"""Grade 5 final paper 2025: figures written question by question."""
from b_kit import *

P = "EXT_G5_FP_2025_"
ENTRIES = {}

# ── geometry, angles, clocks ────────────────────────────────────────────────

# 011 angle between the hands at 9:33
ENTRIES[P + "011"] = entry(
    clock(9, 33, angle=True, note="Angle between the hands = ?"),
    [
        clock(9, 33, hl=["hour"], note="Hour hand: 286.5° from the 12"),
        clock(9, 33, hl=["minute"], note="Minute hand: 198° from the 12"),
        clock(9, 33, angle=True, hl=["angle"], note="286.5 − 198 = 88.5°"),
    ])

# 029 complement and supplement of 58°
ENTRIES[P + "029"] = entry(
    angles("single", [("58°", 58)], note="Add its complement and its supplement"),
    [
        angles("inRightAngle", [("58°", 58), "32°"], hl=["p1"], note="Up to a right angle: 90 − 58 = 32"),
        angles("onLine", [("58°", 58), "122°"], hl=["p1"], note="Up to a straight line: 180 − 58 = 122"),
        None,
    ])

# 002 circle of area 616 sq.cm; a square with the same distance around
ENTRIES[P + "002"] = entry(
    fig("circle", radius="?", note="Area 616 sq.cm. A square has the same distance around"),
    [
        fig("circle", radius="14 cm", highlight=["radius"], note="22/7 × r × r = 616 gives r × r = 196"),
        fig("circle", radius="14 cm", highlight=["edge"], note="Circumference = 2 × 22/7 × 14 = 88 cm"),
        rect(square=True, length="22 cm", inside="Perimeter 88 cm", hl=["border"], note="88 ÷ 4 = 22 cm for each side"),
        rect(square=True, length="22 cm", breadth="22 cm", inside="22 × 22 = 484", hl=["fill"]),
    ])

# 012 rectangle of area 468 with breadth 18 cm
ENTRIES[P + "012"] = entry(
    rect(length="?", breadth="18 cm", inside="Area 468", note="Perimeter = ?"),
    [
        rect(length="26 cm", breadth="18 cm", inside="Area 468", hl=["length"], note="468 ÷ 18 = 26 cm"),
        rect(length="26 cm", breadth="18 cm", inside="Perimeter 88 cm", hl=["border"], note="2 × (26 + 18) = 88 cm"),
    ])

# 034 square PQRS of area 196; rectangle ABCD four times as big
ENTRIES[P + "034"] = entry(
    rect(square=True, inside="PQRS: 196 sq.cm", note="Rectangle ABCD has four times this area"),
    [
        rect(proportion=3, grid={"cols": 4, "rows": 1}, inside="4 × 196 = 784", hl=["fill"], note="ABCD holds as much as 4 of the squares"),
        None,
        rect(proportion=3, length="56", breadth="14", inside="56 × 14 = 784", hl=["length", "breadth"]),
    ])

# ── journeys ────────────────────────────────────────────────────────────────

# 008 train crosses a pole in 28 s at 108 km/h
ENTRIES[P + "008"] = entry(
    journey(["Front at pole", "End at pole"], [("length ?", "108 km/h for 28 s")], note="The train moves its own length past the pole"),
    [
        journey(["Front at pole", "End at pole"], [("length ?", "30 m/s for 28 s")], hl=["l0"], note="108 km/h is 30 metres every second"),
        journey(["Front at pole", "End at pole"], [("840 m", "30 m/s for 28 s")], note="30 × 28 = 840 m"),
    ])

# 027 432 km at 24 m/s
ENTRIES[P + "027"] = entry(
    journey(["Start", "End"], [("432 km", "24 m/s")], note="Time = ?"),
    [
        journey(["Start", "End"], [("432 km", "86.4 km/h")], hl=["l0"], note="Change the speed into km/h to match the distance"),
        journey(["Start", "End"], [("432 km", "5 hours")], note="432 ÷ 86.4 = 5 hours"),
        None,
    ])

# ── tables ──────────────────────────────────────────────────────────────────

# 003 one gross of cricket balls
ENTRIES[P + "003"] = entry(
    tbl([["1 gross", "Rs.32,400"], ["85", "?"]], headers=["Balls", "Cost"], note="A gross is twelve dozen"),
    [
        tbl([["144", "Rs.32,400"], ["1", "Rs.225"], ["85", "?"]], headers=["Balls", "Cost"], hl=["r1"]),
        tbl([["144", "Rs.32,400"], ["1", "Rs.225"], ["85", "Rs.19,125"]], headers=["Balls", "Cost"], hl=["r2"]),
    ])

# 025 15 men, 28 days; how many more for 20 days
ENTRIES[P + "025"] = entry(
    tbl([["15", "28"], ["?", "20"]], headers=["Men", "Days"], note="Find the men needed, then how many MORE than 15"),
    [
        tbl([["15", "28"], ["?", "20"]], headers=["Men", "Days"], hl=["r0"], note="15 × 28 = 420 days of work for one man"),
        tbl([["15", "28"], ["21", "20"]], headers=["Men", "Days"], hl=["r1"], note="420 ÷ 20 = 21 men"),
        tbl([["15", "28"], ["21", "20"]], headers=["Men", "Days"], note="21 − 15 = 6 more men"),
    ])

# ── bar models ──────────────────────────────────────────────────────────────

# 005 what % of 80 added to 80 gives 12 squared
ENTRIES[P + "005"] = entry(
    bars([bar([seg(2, "80", "a"), seg(2, "?% of 80", "unknown")], "Sum", "square of 12")]),
    [
        bars([bar([seg(2, "80", "a"), seg(2, "?% of 80", "unknown")], "Sum", "144")], hl=["b0"]),
        bars([bar([seg(2, "80", "a"), seg(2, "64", "b")], "Sum", "144")], hl=["b0s1"], note="144 − 80 = 64"),
        bars([bar([seg(2, "80", "a"), seg(2, "64", "b")], "Sum", "144")], note="64 out of 80 is 80 out of 100"),
    ])

# 006 loss of Rs.80; at Rs.375 the profit would be twice the loss
_c6 = lambda sold, brace=None: bar([seg(2, sold, "unknown" if "?" in sold else "c"), seg(0.8, "loss Rs.80", "b")], "Cost price", brace)
_s6 = lambda profit: bar([seg(2.8, "cost price", "a"), seg(1.6, profit, "b")], "Sold at Rs.375")
ENTRIES[P + "006"] = entry(
    bars([_c6("sold for ?"), _s6("profit = 2 × loss")]),
    [
        bars([_c6("sold for ?"), _s6("profit Rs.160")], hl=["b1s1"], note="2 × 80 = 160"),
        bars([_c6("sold for ?", "Rs.215"), _s6("profit Rs.160")], hl=["b0"], note="375 − 160 = 215"),
        bars([_c6("Rs.135", "Rs.215"), _s6("profit Rs.160")], hl=["b0s0"], note="215 − 80 = 135"),
    ])

# 007 28500 becomes 38760 in three years
ENTRIES[P + "007"] = entry(
    bars([bar([seg(3, "Rs.28500", "a")] + [seg(1, "?", "unknown") for _ in range(3)], "Amount", "Rs.38760, three years")], note="Each ? is one year of interest. Rate = ?"),
    [
        bars([bar([seg(3, "Rs.28500", "a"), seg(3, "interest Rs.10,260", "b")], "Amount", "Rs.38760, three years")], hl=["b0s1"]),
        bars([bar([seg(3, "Rs.28500", "a")] + [seg(1, "12%", "b") for _ in range(3)], "Amount", "Rs.38760, three years")], note="Rs.10,260 over 3 years on Rs.28,500 is 12% a year"),
    ])

# 010 sum 92, difference 14
ENTRIES[P + "010"] = entry(
    bars([bar([seg(3, "same as smaller", "a"), seg(1, "14", "b")], "Greater"), bar([seg(3, "?", "unknown")], "Smaller")], note="Together the two bars make 92. Square of the greater = ?"),
    [
        bars([bar([seg(3, "same as smaller", "a"), seg(1, "14", "b")], "Greater", "53"), bar([seg(3, "?", "unknown")], "Smaller")], hl=["b0"], note="92 + 14 = 106 is two of the greater, so it is 53"),
        bars([bar([seg(3, "39", "a"), seg(1, "14", "b")], "Greater", "53"), bar([seg(3, "39", "a")], "Smaller")], hl=["b1"], note="53 + 39 = 92"),
        None,
    ])

# 024 sold at Rs.78 with a 35% loss; price for a 15% profit
ENTRIES[P + "024"] = entry(
    bars([bar([seg(6.5, "sold for Rs.78", "a"), seg(3.5, "35% loss", "b")], "Cost price")], note="Price for a 15% profit = ?"),
    [
        bars([bar([seg(6.5, "sold for Rs.78", "a"), seg(3.5, "35% loss", "b")], "Cost price", "Rs.120")], hl=["b0s0"], note="65% is 78, so 1% is 1.2 and the cost is 120"),
        bars([bar([seg(10, "Rs.120", "a"), seg(1.5, "15%", "c")], "New price", "Rs.138")], hl=["b0s1"], note="115 × 1.2 = 138"),
    ])

# 026 Rs.280 interest every month at 15% a year
_m26 = [seg(1, "Rs.280", "b")] + [seg(1, None, "b") for _ in range(11)]
ENTRIES[P + "026"] = entry(
    bars([bar(_m26, "12 months")], note="Rs.280 every month. A year of it is 15% of the money"),
    [
        bars([bar(_m26, "12 months", "Rs.3360 in a year")], hl=["b0"], note="280 × 12 = 3360"),
        bars([bar(_m26, "12 months", "Rs.3360 = 15%")], note="15% is 3360, so the money invested is Rs.22,400"),
    ])

# 040 Rs.16000 for 18 months at 8%
ENTRIES[P + "040"] = entry(
    bars([bar([seg(2, "1 year at 8%", "b"), seg(1, "half a year", "b")], "Interest", "18 months: ?")], note="Rs.16000 is invested"),
    [
        bars([bar([seg(2, "1 year at 8%", "b"), seg(1, "half a year", "b")], "Interest", "18 months: ?")], note="18 months = 1.5 years"),
        bars([bar([seg(2, "Rs.1280", "b"), seg(1, "half a year", "b")], "Interest", "18 months: ?")], hl=["b0s0"], note="8% of 16000 is 1280"),
        bars([bar([seg(2, "Rs.1280", "b"), seg(1, "half of 1280", "b")], "Interest", "Rs.1920")], hl=["b0"], note="1280 × 1.5 = 1920"),
    ])

# 014 3/4, 5/6, 4/5: greatest minus smallest
_f14 = lambda a, b, c: [(4, 3, a), (6, 5, b), (5, 4, c)]
ENTRIES[P + "014"] = entry(
    fbars(_f14("3/4", "5/6", "4/5"), note="Greatest − smallest = ?"),
    [
        None,
        fbars(_f14("3/4 = 45/60", "5/6 = 50/60", "4/5 = 48/60"), note="Cut every bar into 60 equal parts to compare"),
        fbars(_f14("3/4 = 45/60", "5/6 = 50/60", "4/5 = 48/60"), hl=["b0", "b1"], note="Greatest is 50/60, smallest is 45/60"),
        fbars(_f14("3/4 = 45/60", "5/6 = 50/60", "4/5 = 48/60"), hl=["b0", "b1"], note="50/60 − 45/60 = 5/60 = 1/12"),
    ])

# ── equations, sequences, place value ───────────────────────────────────────

# 028 4x + 3 = 22, find 12x + 3
ENTRIES[P + "028"] = entry(
    bal("4x + 3", "22", note="Both pans weigh the same. 12x + 3 = ?"),
    [
        bal("4x", "19", note="Take 3 off both pans"),
        bal("12x", "57", note="Make both pans 3 times as heavy"),
        bal("12x + 3", "60", note="Put 3 back on both pans"),
    ])

# 022 sum of the first 8 terms of 7, 11, 15, 19
_all22 = [(7, 11), (11, 15), (15, 19), (19, 23), (23, 27), (27, 31), (31, 35)]
ENTRIES[P + "022"] = entry(
    nl(7, 19, 4, points=[7, 11, 15, 19], hops=[(7, 11, "?"), (11, 15, "?"), (15, 19, "?")], note="Carry the pattern on to 8 terms, then add them"),
    [
        nl(7, 35, 4, points=[7, 35], hops=_all22, note="8 terms, from 7 up to 35"),
        tbl([["7", "11", "15", "19"], ["35", "31", "27", "23"]], note="Pair first with last: every pair makes 42"),
        tbl([["7", "11", "15", "19"], ["35", "31", "27", "23"]], note="4 pairs of 42 = 168"),
    ])

# 032 8th term of 197, 193, 185, 173, 157
_p32 = [197, 193, 185, 173, 157]
_h32 = lambda labs: [(197, 193, labs[0]), (193, 185, labs[1]), (185, 173, labs[2]), (173, 157, labs[3])]
ENTRIES[P + "032"] = entry(
    nl(157, 197, 1, points=_p32, hops=_h32(["?"] * 4), note="Look at the size of each jump back. 8th term = ?"),
    [
        nl(157, 197, 1, points=_p32, hops=_h32(["−4", "−8", "−12", "−16"])),
        nl(157, 197, 1, points=_p32, hops=_h32(["−4", "−8", "−12", "−16"]), note="Each jump is 4 bigger than the one before"),
        tbl([["Jump", "−20", "−24", "−28"], ["Value", "137", "113", "85"]], headers=["Term", "6th", "7th", "8th"], hl=["r1"]),
    ])

# 001 hundreds digit of 25 × 97
ENTRIES[P + "001"] = entry(None, [
    None,
    None,
    place("2425", note="25 × 97 = 2425"),
    place("2425", hl=["d1"], note="4 in the hundreds place is 400"),
])
