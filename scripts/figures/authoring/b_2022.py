"""Grade 5 final paper 2022: figures written question by question."""
from b_kit import *

P = "EXT_G5_FP_2022_"
ENTRIES = {}

# ── geometry, directions ─────────────────────────────────────────────────────

# 020 Mishti faces south-west, turns 180° clockwise then 225° anticlockwise
ENTRIES[P + "020"] = entry(
    # Start direction only: drawing the turns would point at the answer.
    compass("SW", note="She starts facing south-west. Facing now = ?"),
    [
        compass("SW", [(180, "cw")], end=True, hl=["t0"], note="A half turn from South-West ends at North-East"),
        compass("NE", [(225, "acw")], end=True, hl=["t0"], note="225° is 5 steps of 45°: N, NW, W, SW, S"),
        compass("S", hl=["start"], note="Now facing South"),
    ])

# 016 rectangle, perimeter 96 cm, breadth 6 cm less than length
ENTRIES[P + "016"] = entry(
    rect(length="L", breadth="L − 6", inside="Perimeter 96 cm", note="Area = ?"),
    [
        rect(length="27 cm", breadth="L − 6", inside="L + B = 48", hl=["length"], note="2L − 6 = 48, so L = 27 cm"),
        rect(length="27 cm", breadth="21 cm", hl=["breadth"], note="27 − 6 = 21 cm"),
        rect(length="27 cm", breadth="21 cm", inside="27 × 21 = 567", hl=["fill"]),
    ])

# 028 triangle with sides in terms of a
_t = lambda ab, bc, ca, **kw: fig("triangle", shape="scalene", sides={"ab": ab, "bc": bc, "ca": ca}, **kw)
ENTRIES[P + "028"] = entry(
    _t("3a + 5", "7a + 10", "4a + 15", note="a = 5. Perimeter = ?"),
    [
        _t("20", "7a + 10", "4a + 15", highlight=["ab"]),
        _t("20", "45", "4a + 15", highlight=["bc"]),
        _t("20", "45", "35", highlight=["ca"]),
        _t("20", "45", "35", highlight=["ab", "bc", "ca"], note="20 + 45 + 35 = 100 units"),
    ])

# 029 rectangle, perimeter 84 cm, breadth half of length
ENTRIES[P + "029"] = entry(
    rect(length="L", breadth="half of L", proportion=2, inside="Perimeter 84 cm", note="L = ?"),
    [
        rect(length="L", breadth="half of L", proportion=2, hl=["length", "breadth"], note="One length and one breadth make 84 ÷ 2 = 42"),
        rect(length="L", breadth="half of L", proportion=2, hl=["length", "breadth"], note="L and half of L together make 42"),
        rect(length="28 cm", breadth="14 cm", proportion=2, hl=["length"], note="28 + 14 = 42"),
    ])

# ── journeys ────────────────────────────────────────────────────────────────

# 012 train 120 m long passes a pole
ENTRIES[P + "012"] = entry(
    journey(["Front at pole", "End at pole"], [("120 m", "36 km/h")], note="The train must move its own length past the pole. Time = ?"),
    [
        journey(["Front at pole", "End at pole"], [("120 m", "10 m/s")], hl=["l0"], note="36 km/h is 10 metres every second"),
        journey(["Front at pole", "End at pole"], [("120 m", "12 seconds")], note="120 ÷ 10 = 12 seconds"),
    ])

# 030 car 600 m in 25 s
ENTRIES[P + "030"] = entry(
    journey(["Start", "25 s later"], [("600 m", "25 s")], note="At the same speed, how far in 1 hour?"),
    [
        journey(["Start", "25 s later"], [("600 m", "24 m/s")], hl=["l0"], note="600 ÷ 25 = 24 metres every second"),
        journey(["Start", "1 hour later"], [("86.4 km", "3600 s")], note="24 × 3600 = 86400 m"),
        None,
    ])

# ── tables for the unitary method ───────────────────────────────────────────

# 001 one gross of notebooks
ENTRIES[P + "001"] = entry(
    tbl([["1 gross", "Rs.936"], ["48", "?"]], headers=["Books", "Cost"], note="A gross is twelve dozen"),
    [
        tbl([["144", "Rs.936"], ["1", "Rs.6.50"], ["48", "?"]], headers=["Books", "Cost"], hl=["r1"]),
        tbl([["144", "Rs.936"], ["1", "Rs.6.50"], ["48", "Rs.312"]], headers=["Books", "Cost"], hl=["r2"]),
    ])

# 038 jugs and a decalitre
ENTRIES[P + "038"] = entry(
    tbl([["16", "1 decalitre"], ["?", "15625 ml"]], headers=["Jugs", "Juice"]),
    [
        tbl([["16", "10000 ml"], ["1", "625 ml"], ["?", "15625 ml"]], headers=["Jugs", "Juice"], hl=["r1"]),
        tbl([["16", "10000 ml"], ["1", "625 ml"], ["25", "15625 ml"]], headers=["Jugs", "Juice"], hl=["r2"]),
    ])

# ── bar models ──────────────────────────────────────────────────────────────

# 011 bought 400, sold 324
ENTRIES[P + "011"] = entry(
    bars([bar([seg(5, "Rs.400", "a")], "Worth"), bar([seg(4, "Rs.324", "a"), seg(1, "loss ?", "unknown")], "Sold for")], note="Loss as a percent of Rs.400 = ?"),
    [
        bars([bar([seg(5, "Rs.400", "a")], "Worth"), bar([seg(4, "Rs.324", "a"), seg(1, "loss Rs.76", "b")], "Sold for")], hl=["b1s1"]),
        bars([bar([seg(5, "Rs.400", "a")], "Worth"), bar([seg(4, "Rs.324", "a"), seg(1, "loss Rs.76", "b")], "Sold for")], note="76 out of 400 is 19 out of 100"),
    ])

# 015 scores 94, short by 74, pass mark is 40%
ENTRIES[P + "015"] = entry(
    bars([bar([seg(2.2, "94 scored", "a"), seg(1.8, "74 short", "b")], "Pass mark", "40% of maximum"), bar([seg(10, "?", "unknown")], "Maximum")]),
    [
        bars([bar([seg(2.2, "94 scored", "a"), seg(1.8, "74 short", "b")], "Pass mark", "168 = 40% of maximum"), bar([seg(10, "?", "unknown")], "Maximum")], hl=["b0"]),
        bars([bar([seg(2.2, "94 scored", "a"), seg(1.8, "74 short", "b")], "Pass mark", "168 = 40% of maximum"), bar([seg(10, "?", "unknown")], "Maximum")], note="40% is 168, so 1% is 4.2"),
        bars([bar([seg(2.2, "94 scored", "a"), seg(1.8, "74 short", "b")], "Pass mark", "168 = 40% of maximum"), bar([seg(10, "420", "c")], "Maximum")], hl=["b1"]),
    ])

# 031 phone bought for 18000, 18% profit wanted
ENTRIES[P + "031"] = entry(
    bars([bar([seg(5, "Rs.18000", "a")], "Cost"), bar([seg(5, "Rs.18000", "a"), seg(1, "18% profit", "b")], "Selling price", "?")]),
    [
        bars([bar([seg(5, "Rs.18000", "a")], "Cost"), bar([seg(5, "Rs.18000", "a"), seg(1, "Rs.3240", "b")], "Selling price", "?")], hl=["b1s1"], note="1% is 180, so 18% is 3240"),
        bars([bar([seg(5, "Rs.18000", "a")], "Cost"), bar([seg(5, "Rs.18000", "a"), seg(1, "Rs.3240", "b")], "Selling price", "Rs.21240")], hl=["b1"]),
    ])

# 005 interest 160 in 5 years at 8%
ENTRIES[P + "005"] = entry(
    bars([bar([seg(1, "8%", "b") for _ in range(5)], "Interest", "Rs.160 in 5 years")], note="Each piece is 8% of the principal. Principal = ?"),
    [
        bars([bar([seg(1, "8%", "b") for _ in range(5)], "Interest", "Rs.160 in 5 years")], hl=["b0"], note="8 × 5 = 40, so Rs.160 is 40% of the principal"),
        bars([bar([seg(1, "8%", "b") for _ in range(5)], "Interest", "Rs.160 in 5 years")], note="40% is Rs.160, so the whole principal is Rs.400"),
        bars([bar([seg(1, "Rs.32", "b") for _ in range(5)], "Interest", "Rs.160 in 5 years")], note="Check: 8% of 400 is 32 a year"),
    ])

# 022 deposit 26500 at 8% for 4 years
ENTRIES[P + "022"] = entry(
    bars([bar([seg(4, "Rs.26500", "a")] + [seg(1, "8%", "b") for _ in range(4)], "After 4 years", "Amount = ?")], note="Each small piece is one year of interest"),
    [
        bars([bar([seg(4, "Rs.26500", "a")] + [seg(1, "Rs.2120", "b") for _ in range(4)], "After 4 years", "Amount = ?")], hl=["b0s1"], note="8% of 26500 is 2120"),
        bars([bar([seg(4, "Rs.26500", "a"), seg(4, "Rs.8480", "b")], "After 4 years", "Amount = ?")], hl=["b0s1"], note="2120 × 4 = 8480"),
        bars([bar([seg(4, "Rs.26500", "a"), seg(4, "Rs.8480", "b")], "After 4 years", "Rs.34980")], hl=["b0"]),
    ])

# 035 two consecutive odd numbers
ENTRIES[P + "035"] = entry(
    bars([bar([seg(4, "W", "a")], "First odd"), bar([seg(4, "W", "a"), seg(1, "2", "b")], "Next odd")], note="Together the two bars make 192"),
    [
        bars([bar([seg(4, "W", "a")], "First odd"), bar([seg(4, "W", "a"), seg(1, "2", "b")], "Next odd", "W + 2")], hl=["b1"]),
        bars([bar([seg(4, "W", "a")], "First odd"), bar([seg(4, "W", "a"), seg(1, "2", "b")], "Next odd", "W + 2")], hl=["b0", "b1"], note="W + (W + 2) = 192"),
        bars([bar([seg(4, "95", "a")], "First odd"), bar([seg(4, "95", "a"), seg(1, "2", "b")], "Next odd", "97")], note="95 + 97 = 192"),
    ])

# ── equations, sequences, place value, factors ──────────────────────────────

# 006 4(2x − 1) = 5(x + 2) + 4
ENTRIES[P + "006"] = entry(
    bal("4(2x − 1)", "5(x + 2) + 4", note="Both pans weigh the same. x = ?"),
    [
        bal("8x − 4", "5x + 14", note="Open the brackets on each pan"),
        bal("3x", "18", note="Take 5x off both pans and add 4 to both"),
        bal("x", "6", note="Share both pans into 3 equal parts"),
    ])

# 002 gaps double each time
ENTRIES[P + "002"] = entry(
    nl(9, 37, 4, points=[9, 13, 21, 37], hops=[(9, 13, "?"), (13, 21, "?"), (21, 37, "?")], note="Look at the size of each jump. After 37 come K and 133"),
    [
        nl(9, 37, 4, points=[9, 13, 21, 37], hops=[(9, 13, "+4"), (13, 21, "+8"), (21, 37, "+16")], note="Each jump is double the one before"),
        nl(37, 69, 4, points=[37, (69, "K")], hops=[(37, 69, "+32")]),
        nl(69, 133, 8, points=[(69, "K"), 133], hops=[(69, 133, "+64")], note="The next jump lands on 133, so the pattern fits"),
        None,
    ])

# 033 11th term of 19, 31, 43, 55
ENTRIES[P + "033"] = entry(
    nl(19, 55, 12, points=[19, 31, 43, 55], hops=[(19, 31, "?"), (31, 43, "?"), (43, 55, "?")], note="How big is each jump? 11th term = ?"),
    [
        nl(19, 55, 12, points=[19, 31, 43, 55], hops=[(19, 31, "+12"), (31, 43, "+12"), (43, 55, "+12")]),
        nl(19, 55, 12, points=[19, 31, 43, 55], hops=[(19, 31, "+12"), (31, 43, "+12"), (43, 55, "+12")], note="10 jumps of 12 from 19: 19 + 120 = 139"),
    ])

# 025 number given in words; the picture starts once it is written in digits
ENTRIES[P + "025"] = entry(None, [
    place("6794521", note="The number has 7 digits"),
    place("6794521", hl=["d3"], note="The 4th digit is the middle one"),
    place("6794521", hl=["d3"], note="4 in the thousands place is 4000"),
])

# 039 HCF and LCM of 12 and 90
ENTRIES[P + "039"] = entry(None, [
    fig("venn", leftTitle="12", rightTitle="90", left="rest of 12", both="2 × 3", right="rest of 90", highlight=["both"], note="Shared prime factors: 2 × 3 = 6"),
    fig("venn", leftTitle="12", rightTitle="90", left="2", both="2 × 3", right="3 × 5", highlight=["left", "both", "right"], note="Every factor once: 2 × 2 × 3 × 3 × 5 = 180"),
    None,
])
