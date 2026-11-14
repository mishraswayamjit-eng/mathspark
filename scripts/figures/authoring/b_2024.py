"""Grade 5 final paper 2024: figures written question by question."""
from b_kit import *

P = "EXT_G5_FP_2024_"
ENTRIES = {}

# ── geometry, angles, clocks, directions ────────────────────────────────────

# 005 angle between the hands at 7:20
ENTRIES[P + "005"] = entry(
    clock(7, 20, angle=True, note="Angle between the hands = ?"),
    [
        clock(7, 20, hl=["hour"], note="Hour hand: 220° from the 12"),
        clock(7, 20, hl=["minute"], note="Minute hand: 120° from the 12"),
        clock(7, 20, angle=True, hl=["angle"], note="220 − 120 = 100°"),
    ])

# 034 Shraddha faces East, turns 135° clockwise then 315° anticlockwise
ENTRIES[P + "034"] = entry(
    compass("E", [(135, "cw"), (315, "acw")], note="Follow the two turns. Facing now = ?"),
    [
        compass("E", [(135, "cw")], end=True, hl=["t0"], note="135° clockwise from East ends at South-West"),
        compass("SW", [(315, "acw")], end=True, hl=["t0"], note="315° anticlockwise ends where 45° clockwise does"),
        compass("W", hl=["start"], note="Now facing West"),
    ])

# 001 square of side 56 cm and a rectangle of breadth 49 cm with equal areas
ENTRIES[P + "001"] = entry(
    rect(length="?", breadth="49 cm", inside="same area as square", note="The square has side 56 cm. Perimeter of the rectangle = ?"),
    [
        rect(square=True, length="56 cm", breadth="56 cm", inside="56 × 56 = 3136", hl=["fill"]),
        rect(length="64 cm", breadth="49 cm", inside="Area 3136", hl=["length"], note="3136 ÷ 49 = 64 cm"),
        rect(length="64 cm", breadth="49 cm", inside="Perimeter 226 cm", hl=["border"], note="2 × (64 + 49) = 226 cm"),
        None,
    ])

# 019 equilateral triangle of side 12 cm and a rectangle with the same perimeter
ENTRIES[P + "019"] = entry(
    tri("equilateral", ab="12 cm", bc="12 cm", ca="12 cm", note="A rectangle has the same perimeter. Which sides fit?"),
    [
        tri("equilateral", ab="12 cm", bc="12 cm", ca="12 cm", hl=["ab", "bc", "ca"], note="3 × 12 = 36 cm"),
        rect(length="L", breadth="B", inside="Perimeter 36 cm", hl=["length", "breadth"], note="One length and one breadth make 18 cm"),
        rect(length="13 cm", breadth="5 cm", inside="13 + 5 = 18", proportion=2.6),
    ])

# 033 square of side 30 cm stretched one way and squeezed the other
ENTRIES[P + "033"] = entry(
    rect(square=True, length="30 cm", breadth="30 cm", note="One side becomes 5/4 of 30 cm, the other 3/5 of 30 cm"),
    [
        rect(length="37.5 cm", breadth="18 cm", proportion=2.1, hl=["length", "breadth"], note="The new shape is a rectangle"),
        rect(length="37.5 cm", breadth="18 cm", proportion=2.1, inside="Area 675", hl=["fill"]),
        rect(square=True, length="30 cm", breadth="30 cm", inside="Area 900", hl=["fill"]),
        rect(square=True, length="30 cm", breadth="30 cm", inside="Area 900", note="900 − 675 = 225 sq.cm"),
    ])

# ── journeys ────────────────────────────────────────────────────────────────

# 008 A to B, 680 km in 8 hours; return 17 km/h slower
ENTRIES[P + "008"] = entry(
    journey(["A", "B"], [("680 km", "8 hours")], note="The return trip is 17 km/h slower. Time back = ?"),
    [
        journey(["A", "B"], [("680 km", "85 km/h")], hl=["l0"], note="680 ÷ 8 = 85 km/h"),
        journey(["B", "A"], [("680 km", "68 km/h")], hl=["l0"], note="85 − 17 = 68 km/h on the way back"),
        journey(["B", "A"], [("680 km", "10 hours")], note="680 ÷ 68 = 10 hours"),
        journey(["B", "A"], [("680 km", "600 minutes")]),
    ])

# 023 train London to Paris
ENTRIES[P + "023"] = entry(
    journey(["London", "Paris"], [("32.5 m/s", "6:45 to 9:15 pm")], note="Distance = ?"),
    [
        journey(["London", "Paris"], [("32.5 m/s", "2 h 30 min")], hl=["l0"], note="2 hours 30 minutes = 9000 seconds"),
        journey(["London", "Paris"], [("32.5 m/s", "9000 s")], note="32.5 × 9000 = 292500 m"),
        journey(["London", "Paris"], [("292.5 km", "2 h 30 min")], hl=["l0"]),
    ])

# ── tables ──────────────────────────────────────────────────────────────────

# 018 three dozen mangoes
ENTRIES[P + "018"] = entry(
    tbl([["Three dozen", "Rs.1800"], ["26", "?"]], headers=["Mangoes", "Cost"]),
    [
        tbl([["36", "Rs.1800"], ["26", "?"]], headers=["Mangoes", "Cost"], hl=["r0"], note="3 × 12 = 36 mangoes"),
        tbl([["36", "Rs.1800"], ["1", "Rs.50"], ["26", "?"]], headers=["Mangoes", "Cost"], hl=["r1"]),
        tbl([["36", "Rs.1800"], ["1", "Rs.50"], ["26", "Rs.1300"]], headers=["Mangoes", "Cost"], hl=["r2"]),
    ])

# 015 28% of a number is 196
ENTRIES[P + "015"] = entry(
    tbl([["28%", "196"], ["43%", "?"]], headers=["Part", "Value"]),
    [
        tbl([["28%", "196"], ["1%", "7"], ["43%", "?"]], headers=["Part", "Value"], hl=["r1"]),
        tbl([["28%", "196"], ["1%", "7"], ["43%", "301"]], headers=["Part", "Value"], hl=["r2"]),
    ])

# 026 Mishti's marks
_marks = [["Science", "44", "50"], ["Mathematics", "50", "50"], ["English", "42", "50"], ["Social Science", "84", "100"]]
_mh = ["Subject", "Scored", "Out of"]
ENTRIES[P + "026"] = entry(
    tbl(_marks, headers=_mh, note="Overall percentage = ?"),
    [
        tbl(_marks + [["Total", "220", "?"]], headers=_mh, hl=["r4"]),
        tbl(_marks + [["Total", "220", "250"]], headers=_mh, hl=["r4"]),
        tbl(_marks + [["Total", "220", "250"]], headers=_mh, hl=["r4"], note="220 out of 250 is 88 out of 100"),
    ])

# 024 cricket bats
_bh = ["Deal", "Bats", "Price each"]
_bh2 = ["Deal", "Bats", "Price each", "Total"]
_cost = bar([seg(5, "Rs.32,500", "a")], "Cost")
_sold = bar([seg(5, "Rs.32,500", "a"), seg(1, "profit Rs.2,600", "c")], "Sold for", "Rs.35,100")
ENTRIES[P + "024"] = entry(
    tbl([["Bought", "26", "Rs.1250"], ["Sold", "14", "Rs.1800"], ["Sold", "the rest", "Rs.825"]], headers=_bh, note="Profit % or loss % overall = ?"),
    [
        tbl([["Bought", "26", "Rs.1250", "Rs.32,500"], ["Sold", "14", "Rs.1800", "?"], ["Sold", "the rest", "Rs.825", "?"]], headers=_bh2, hl=["r0"]),
        tbl([["Bought", "26", "Rs.1250", "Rs.32,500"], ["Sold", "14", "Rs.1800", "Rs.25,200"], ["Sold", "12", "Rs.825", "Rs.9,900"]], headers=_bh2, hl=["r1", "r2"], note="25,200 + 9,900 = Rs.35,100"),
        bars([_cost, _sold], hl=["b1s1"]),
        bars([_cost, _sold], note="2600 out of 32500 is 8 out of 100"),
    ])

# ── bar models ──────────────────────────────────────────────────────────────

# 002 sold at 440 with 10% profit; price for 17% profit
ENTRIES[P + "002"] = entry(
    bars([bar([seg(10, "cost = 100%", "a"), seg(1, "10%", "b")], "Sold for", "Rs.440")], note="Price for a 17% profit = ?"),
    [
        bars([bar([seg(10, "Rs.400", "a"), seg(1, "10%", "b")], "Sold for", "Rs.440")], hl=["b0s0"], note="110% is 440, so 1% is 4 and the cost is 400"),
        bars([bar([seg(10, "Rs.400", "a"), seg(1.7, "17%", "c")], "New price", "Rs.468")], hl=["b0s1"], note="117 × 4 = 468"),
    ])

# 017 Medha borrows 3500, repays 4340 after 3 years
ENTRIES[P + "017"] = entry(
    bars([bar([seg(3, "Rs.3500", "a")] + [seg(1, "?", "unknown") for _ in range(3)], "Paid back", "Rs.4340 after 3 years")], note="Each ? is one year of interest. Rate = ?"),
    [
        bars([bar([seg(3, "Rs.3500", "a"), seg(3, "interest Rs.840", "b")], "Paid back", "Rs.4340 after 3 years")], hl=["b0s1"]),
        bars([bar([seg(3, "Rs.3500", "a")] + [seg(1, "8%", "b") for _ in range(3)], "Paid back", "Rs.4340 after 3 years")], note="Rs.840 over 3 years on Rs.3500 is 8% a year"),
    ])

# 038 interest on 4250 for 5 years at 8%
ENTRIES[P + "038"] = entry(
    bars([bar([seg(1, "8% of 4250", "b") for _ in range(5)], "Interest", "5 years: ?")], note="One piece for each year"),
    [
        bars([bar([seg(1, "8% of 4250", "b") for _ in range(5)], "Interest", "5 years: ?")], note="1% of 4250 = 42.5"),
        bars([bar([seg(1, "Rs.340", "b") for _ in range(5)], "Interest", "5 years: ?")], hl=["b0s0"], note="8 × 42.5 = 340 for one year"),
        bars([bar([seg(1, "Rs.340", "b") for _ in range(5)], "Interest", "Rs.1700")], hl=["b0"]),
    ])

# 021 which fraction is greatest (bars only after answering: they would give it away)
ENTRIES[P + "021"] = entry(None, [
    fbars([(19, 9, "9/19"), (21, 10, "10/21")], note="Both are less than half shaded"),
    fbars([(17, 15, "15/17"), (13, 11, "11/13")], note="Each is 2 parts short of a whole"),
    fbars([(17, 15, "15/17"), (13, 11, "11/13")], hl=["b0"], note="Parts of 17 are smaller, so 15/17 is closer to 1"),
    None,
])

# ── equations, sequences, place value ───────────────────────────────────────

# 014 6x − 9 = (4x + 30)/2
ENTRIES[P + "014"] = entry(
    bal("6x − 9", "(4x + 30) ÷ 2", note="Both pans weigh the same. x = ?"),
    [
        bal("6x − 9", "2x + 15", hl=["right"], note="Halve everything on the right pan"),
        None,
        bal("4x", "24", note="Take 2x off both pans and add 9 to both"),
        bal("x", "6", note="Share both pans into 4 equal parts"),
    ])

# 035 (4x − 5)/5 = (2x + 3)/3
ENTRIES[P + "035"] = entry(
    bal("(4x − 5) ÷ 5", "(2x + 3) ÷ 3", note="Both pans weigh the same. x = ?"),
    [
        bal("3 × (4x − 5)", "5 × (2x + 3)", note="Make both pans 15 times as heavy"),
        bal("12x − 15", "10x + 15", note="Open the brackets"),
        bal("2x", "30", note="Take 10x off both pans and add 15 to both"),
        bal("x", "15", note="Halve both pans"),
    ])

# 016 11th and 18th terms of 3, 7, 11, 15, 19
_p16 = [3, 7, 11, 15, 19]
_h16 = lambda lab: [(3, 7, lab), (7, 11, lab), (11, 15, lab), (15, 19, lab)]
ENTRIES[P + "016"] = entry(
    nl(3, 19, 4, points=_p16, hops=_h16("?"), note="Find the 11th and the 18th terms, then add them"),
    [
        nl(3, 19, 4, points=_p16, hops=_h16("+4")),
        nl(3, 19, 4, points=_p16, hops=_h16("+4"), note="11th term: 10 jumps of 4 from 3 is 43"),
        nl(3, 19, 4, points=_p16, hops=_h16("+4"), note="18th term: 17 jumps of 4 from 3 is 71"),
        None,
    ])

# 029 9th term of 405, 363, 321, 279, 237
_p29 = [405, 363, 321, 279, 237]
_h29 = lambda lab: [(405, 363, lab), (363, 321, lab), (321, 279, lab), (279, 237, lab)]
ENTRIES[P + "029"] = entry(
    nl(237, 405, 42, points=_p29, hops=_h29("?"), note="How big is each jump back? 9th term = ?"),
    [
        nl(237, 405, 42, points=_p29, hops=_h29("−42")),
        nl(237, 405, 42, points=_p29, hops=_h29("−42"), note="8 jumps of 42 back from 405: 405 − 336 = 69"),
    ])

# 007 7th odd number after 54 and 12th even number before 65
ENTRIES[P + "007"] = entry(None, [
    nl(54, 68, 1, points=[54, (67, "7th odd")], hops=[(55, 57), (57, 59), (59, 61), (61, 63), (63, 65), (65, 67)], note="55 is the 1st odd number after 54"),
    nl(40, 66, 2, points=[(64, "1st even"), (42, "12th even")], note="11 jumps of 2 back from 64 lands on 42"),
    None,
])

# 011 digit 4 in 97 squared
ENTRIES[P + "011"] = entry(None, [
    None,
    place("9409", note="97 × 97 = 9409"),
    place("9409", hl=["d1"], note="4 in the hundreds place is 400"),
])
