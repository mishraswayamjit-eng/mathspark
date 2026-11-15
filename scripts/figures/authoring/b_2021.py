"""Grade 5 final paper 2021: figures written question by question."""
from b_kit import *

P = "EXT_G5_FP_2021_"
ENTRIES = {}

# 006 complementary angle of (25 − y)°
ENTRIES[P + "006"] = entry(
    angles("inRightAngle", ["(25 − y)°", "?"], note="The two angles together make a right angle"),
    [
        angles("inRightAngle", ["(25 − y)°", "?"], hl=["p1"], note="Other part = 90 − (25 − y)"),
        None,
        angles("inRightAngle", ["(25 − y)°", "(65 + y)°"], hl=["p1"], note="90 − 25 + y = 65 + y"),
    ])

# 033 aeroplane Mumbai to Dubai
ENTRIES[P + "033"] = entry(
    journey(["Mumbai", "Dubai"], [("212.5 m/s", "6:20 to 8:50 pm")], note="Distance = ?"),
    [
        journey(["Mumbai", "Dubai"], [("212.5 m/s", "2 h 30 min")], hl=["l0"], note="2 h 30 min = 9000 seconds"),
        journey(["Mumbai", "Dubai"], [("212.5 m/s", "9000 s")], note="212.5 × 9000 = 1912500 m"),
        journey(["Mumbai", "Dubai"], [("1912.5 km", "2 h 30 min")], hl=["l0"]),
    ])

# 013 2x + 1 = 8, find 4x + 1
ENTRIES[P + "013"] = entry(
    bal("2x + 1", "8", note="Both pans weigh the same. 4x + 1 = ?"),
    [
        bal("2x", "7", note="Take 1 off both pans"),
        bal("4x", "14", note="Double both pans"),
        bal("4x + 1", "15", note="Put 1 back on both pans"),
    ])

# 007 the two 6s: one worth 1000 times the other
ENTRIES[P + "007"] = entry(None, [
    place("66728", hl=["d0", "d1"], note="60000 and 6000: only 10 times"),
    place("68726", hl=["d0", "d4"], note="60000 and 6: that is 10000 times"),
    place("86762", hl=["d1", "d3"], note="6000 and 60: only 100 times"),
    place("68762", hl=["d0", "d3"], note="60000 and 60: 60000 ÷ 60 = 1000"),
])

# 004 divisible by 11: alternate digits
ENTRIES[P + "004"] = entry(None, [
    place("3116365", hl=["d0", "d2", "d4", "d6"], note="Every other digit makes 12, the rest make 13. Gap is 1"),
    place("901351", hl=["d0", "d2", "d4"], note="9 + 1 + 5 = 15, the rest make 4, and 15 − 4 = 11"),
    None,
    None,
])

# 005 12th term of 15, 19, 23, 27
ENTRIES[P + "005"] = entry(
    nl(15, 27, 4, points=[15, 19, 23, 27], hops=[(15, 19, "?"), (19, 23, "?"), (23, 27, "?")], note="How big is each jump? 12th term = ?"),
    [
        nl(15, 27, 4, points=[15, 19, 23, 27], hops=[(15, 19, "+4"), (19, 23, "+4"), (23, 27, "+4")]),
        nl(15, 27, 4, points=[15, 19, 23, 27], hops=[(15, 19, "+4"), (19, 23, "+4"), (23, 27, "+4")], note="11 jumps of 4 from 15: 15 + 44 = 59"),
    ])

# 025 gaps are primes
ENTRIES[P + "025"] = entry(
    nl(10, 27, 1, points=[10, 12, 15, 20, 27], hops=[(10, 12, "?"), (12, 15, "?"), (15, 20, "?"), (20, 27, "?")], note="Look at the size of each jump. 8th term = ?"),
    [
        nl(10, 27, 1, points=[10, 12, 15, 20, 27], hops=[(10, 12, "+2"), (12, 15, "+3"), (15, 20, "+5"), (20, 27, "+7")], note="The jumps are the prime numbers"),
        tbl([["Jump", "+11", "+13", "+17"], ["Value", "38", "51", "68"]], headers=["Term", "6th", "7th", "8th"], hl=["r1"]),
    ])

# 002 candy bars
ENTRIES[P + "002"] = entry(
    tbl([["Buys", "5", "Rs.2"], ["Sells", "2", "Rs.1"]], headers=["Deal", "Candy bars", "Price"], note="He buys and sells 1000 bars. Profit or loss % = ?"),
    [
        tbl([["Buys", "5 for Rs.2", "Rs.400"], ["Sells", "2 for Rs.1", "?"]], headers=["Deal", "Rate", "1000 bars"], hl=["r0"]),
        tbl([["Buys", "5 for Rs.2", "Rs.400"], ["Sells", "2 for Rs.1", "Rs.500"]], headers=["Deal", "Rate", "1000 bars"], hl=["r1"]),
        bars([bar([seg(4, "Rs.400", "a")], "Cost"), bar([seg(4, "Rs.400", "a"), seg(1, "profit Rs.100", "b")], "Sold", "Rs.500")], hl=["b1s1"]),
        bars([bar([seg(4, "Rs.400", "a")], "Cost"), bar([seg(4, "Rs.400", "a"), seg(1, "profit Rs.100", "b")], "Sold", "Rs.500")], note="100 out of 400 is 25 out of 100"),
    ])

# 034 loan cleared after 3 years
ENTRIES[P + "034"] = entry(
    bars([bar([seg(3, "Rs.18000", "a"), seg(1, "?", "unknown"), seg(1, "?", "unknown"), seg(1, "?", "unknown")], "Paid back", "Rs.25,560 after 3 years")], note="Each ? is one year of interest. Rate = ?"),
    [
        bars([bar([seg(3, "Rs.18000", "a"), seg(3, "interest Rs.7560", "b")], "Paid back", "Rs.25,560 after 3 years")], hl=["b0s1"]),
        bars([bar([seg(3, "Rs.18000", "a"), seg(1, "14%", "b"), seg(1, "14%", "b"), seg(1, "14%", "b")], "Paid back", "Rs.25,560 after 3 years")], note="Rs.7560 over 3 years on Rs.18000 is 14% a year"),
    ])

# 032 one third of one fourth of a number is 15
ENTRIES[P + "032"] = entry(None, [
    fbars([(4, 1, "1/4 of the number"), (12, 1, "1/3 of that = 15")], note="1 part out of 12 of the number is 15"),
    fbars([(12, 1, "each part is 15")], note="12 parts of 15 make 180"),
    fbars([(10, 3, "3/10 of 180")], note="One part is 18, so three parts are 54"),
    None,
])

# 038 tailor: 8 pieces from each metre
ENTRIES[P + "038"] = entry(
    bars([bar([seg(1) for _ in range(8)], "1 metre", "8 pieces"), bar([seg(8, "? pieces", "unknown")], "37.5 metres")], note="Every metre gives 8 pieces"),
    [
        bars([bar([seg(1) for _ in range(8)], "1 metre", "8 pieces"), bar([seg(8, "300 pieces", "b")], "37.5 metres")], note="37.5 × 8 = 300 pieces"),
        None,
    ])
