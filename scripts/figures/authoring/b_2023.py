"""Grade 5 final paper 2023: figures written question by question."""
from b_kit import *

P = "EXT_G5_FP_2023_"
ENTRIES = {}

# ── geometry, angles, clocks ────────────────────────────────────────────────

# 010 clock at 12:45, hour hand turns 214°
ENTRIES[P + "010"] = entry(
    clock(12, 45, hl=["hour"], note="The hour hand turns 214° more. New time = ?"),
    [
        clock(12, 45, hl=["hour"], note="The hour hand turns 30° an hour: 7 hours and 4° left"),
        clock(12, 45, hl=["hour"], note="4° more takes the hour hand 8 minutes"),
        clock(7, 53, note="12:45 and 7 h 8 min more is 7:53"),
    ])

# 004 square with the same perimeter as a 22 m by 16 m rectangle
ENTRIES[P + "004"] = entry(
    rect(length="22 m", breadth="16 m", note="A square has the same perimeter. Area of the square = ?"),
    [
        rect(length="22 m", breadth="16 m", inside="Perimeter 76 m", hl=["border"]),
        rect(square=True, length="19 m", inside="Perimeter 76 m", hl=["border"], note="76 ÷ 4 = 19 m for each side"),
        rect(square=True, length="19 m", breadth="19 m", inside="19 × 19 = 361", hl=["fill"]),
        None,
    ])

# 017 right-angled triangle, area = 18 × base
ENTRIES[P + "017"] = entry(
    tri("right", ab="height ?", bc="base", note="Area = 18 × base"),
    [
        tri("right", ab="height", bc="base", enclose=True, hl=["fill"], note="Half of base × height = 18 × base"),
        tri("right", ab="height", bc="base", enclose=True, hl=["ab"], note="So half of the height is 18"),
        tri("right", ab="36 units", bc="base", hl=["ab"], note="18 × 2 = 36"),
    ])

# 039 two sides 16 cm and 7 cm
ENTRIES[P + "039"] = entry(
    tri("scalene", ab="7 cm", bc="16 cm", ca="?", note="The third side must close the triangle"),
    [
        tri("scalene", ab="7 cm", bc="16 cm", ca="?", hl=["ca"], note="Third side: longer than 9 cm, shorter than 23 cm"),
        tri("scalene", ab="7 cm", bc="16 cm", ca="?", hl=["ab", "bc", "ca"], note="Perimeter: more than 32 cm, less than 46 cm"),
        tri("scalene", ab="7 cm", bc="16 cm", ca="11 cm", hl=["ca"], note="16 + 7 + 11 = 34 cm fits"),
    ])

# 040 which pair is supplementary
ENTRIES[P + "040"] = entry(
    angles("onLine", ["?", "?"], note="Supplementary angles fit on a straight line: 180°"),
    [
        angles("onLine", [("127.5°", 127.5), "53.5°"], note="127.5 + 53.5 = 181, a little too much"),
        angles("onLine", [("83.6°", 83.6), "95.4°"], note="83.6 + 95.4 = 179, a little too small"),
        angles("onLine", [("111.8°", 111.8), "68.2°"], hl=["p0", "p1"], note="111.8 + 68.2 = 180, a straight line"),
        angles("onLine", [("115.7°", 115.7), "65.3°"], note="115.7 + 65.3 = 181, a little too much"),
    ])

# ── journeys ────────────────────────────────────────────────────────────────

# 003 five rounds of a 400 m track
ENTRIES[P + "003"] = entry(
    journey(["Start", "100 m mark", "Finish"], [("100 m", "4 m/s"), ("300 m", "5 m/s")], note="This is one round of 400 m. Time for five rounds = ?"),
    [
        journey(["Start", "100 m mark", "Finish"], [("100 m", "25 s"), ("300 m", "60 s")], hl=["l0", "l1"]),
        journey(["Start", "100 m mark", "Finish"], [("100 m", "25 s"), ("300 m", "60 s")], note="One round is 85 s, so five rounds are 425 s"),
        None,
        None,
    ])

# ── tables for the unitary method ───────────────────────────────────────────

# 014 12 men, 54 days
ENTRIES[P + "014"] = entry(
    tbl([["12", "54"], ["?", "24"]], headers=["Men", "Days"], note="The same work in fewer days needs more men"),
    [
        tbl([["12", "54"], ["?", "24"]], headers=["Men", "Days"], hl=["r0"], note="12 × 54 = 648 days of work for one man"),
        tbl([["12", "54"], ["27", "24"]], headers=["Men", "Days"], hl=["r1"], note="648 ÷ 24 = 27 men"),
    ])

# 025 126 km on 12 litres
ENTRIES[P + "025"] = entry(
    tbl([["12", "126 km"], ["22", "?"]], headers=["Litres", "Distance"]),
    [
        tbl([["12", "126 km"], ["1", "10.5 km"], ["22", "?"]], headers=["Litres", "Distance"], hl=["r1"]),
        tbl([["12", "126 km"], ["1", "10.5 km"], ["22", "231 km"]], headers=["Litres", "Distance"], hl=["r2"]),
    ])

# ── bar models ──────────────────────────────────────────────────────────────

# 009 6420 becomes 10,272 in 4 years
ENTRIES[P + "009"] = entry(
    bars([bar([seg(4, "Rs.6420", "a")] + [seg(1, "?", "unknown") for _ in range(4)], "Amount", "Rs.10,272 in 4 years")], note="Each ? is one year of interest. Rate = ?"),
    [
        bars([bar([seg(4, "Rs.6420", "a"), seg(4, "interest Rs.3852", "b")], "Amount", "Rs.10,272 in 4 years")], hl=["b0s1"]),
        bars([bar([seg(4, "Rs.6420", "a")] + [seg(1, "15%", "b") for _ in range(4)], "Amount", "Rs.10,272 in 4 years")], note="Rs.3852 over 4 years on Rs.6420 is 15% a year"),
        None,
    ])

# 020 subtract from 3042 + 869 to leave 2165
ENTRIES[P + "020"] = entry(
    bars([bar([seg(3, "3042", "a"), seg(1, "869", "b")], "Sum"), bar([seg(2, "2165", "c"), seg(2, "?", "unknown")], "Same total")], note="The two bars are the same length"),
    [
        bars([bar([seg(3, "3042", "a"), seg(1, "869", "b")], "Sum", "3911"), bar([seg(2, "2165", "c"), seg(2, "?", "unknown")], "Same total")], hl=["b0"]),
        bars([bar([seg(3, "3042", "a"), seg(1, "869", "b")], "Sum", "3911"), bar([seg(2, "2165", "c"), seg(2, "?", "unknown")], "Same total", "3911")], hl=["b1s1"], note="? = 3911 − 2165"),
        bars([bar([seg(3, "3042", "a"), seg(1, "869", "b")], "Sum", "3911"), bar([seg(2, "2165", "c"), seg(2, "1746", "b")], "Same total", "3911")], hl=["b1s1"]),
    ])

# 023 sold at 336 with loss 84; profit at 542
ENTRIES[P + "023"] = entry(
    bars([bar([seg(3.4, "sold Rs.336", "a"), seg(0.8, "loss Rs.84", "b")], "Cost price"), bar([seg(4.2, "cost price", "a"), seg(0.8, "profit ?", "unknown")], "Sold at Rs.542")]),
    [
        bars([bar([seg(3.4, "sold Rs.336", "a"), seg(0.8, "loss Rs.84", "b")], "Cost price", "Rs.420"), bar([seg(4.2, "cost price", "a"), seg(0.8, "profit ?", "unknown")], "Sold at Rs.542")], hl=["b0"]),
        bars([bar([seg(3.4, "sold Rs.336", "a"), seg(0.8, "loss Rs.84", "b")], "Cost price", "Rs.420"), bar([seg(4.2, "Rs.420", "a"), seg(0.8, "profit Rs.122", "c")], "Sold at Rs.542")], hl=["b1s1"], note="542 − 420 = 122"),
        None,
    ])

# 024 Rs.450 becomes four times itself at 24% a year
ENTRIES[P + "024"] = entry(
    bars([bar([seg(1, "Rs.450", "a")] + [seg(1, "interest", "b") for _ in range(3)], "Four times")], note="24% interest is added each year. Time = ?"),
    [
        bars([bar([seg(1, "Rs.450", "a")] + [seg(1, "Rs.450", "b") for _ in range(3)], "Four times")], hl=["b0s1", "b0s2", "b0s3"], note="Interest needed = 3 × 450 = Rs.1350"),
        bars([bar([seg(1, "Rs.450", "a")] + [seg(1, "Rs.450", "b") for _ in range(3)], "Four times")], note="Each year adds 24% of 450 = Rs.108"),
        bars([bar([seg(1, "Rs.450", "a")] + [seg(1, "Rs.450", "b") for _ in range(3)], "Four times")], note="1350 ÷ 108 = 12.5 years"),
    ])

# 032 sold at 12% loss, loss is Rs.60; profit % at Rs.620
ENTRIES[P + "032"] = entry(
    bars([bar([seg(8.8, "sold for", "a"), seg(1.2, "12% = Rs.60", "b")], "Cost price")], note="If it is sold at Rs.620 instead, profit % = ?"),
    [
        bars([bar([seg(8.8, "sold for", "a"), seg(1.2, "12% = Rs.60", "b")], "Cost price", "Rs.500")], hl=["b0"], note="12% is 60, so 1% is 5"),
        bars([bar([seg(5, "Rs.500", "a"), seg(1.2, "profit Rs.120", "c")], "Sold at", "Rs.620")], hl=["b0s1"]),
        bars([bar([seg(5, "Rs.500", "a"), seg(1.2, "profit Rs.120", "c")], "Sold at", "Rs.620")], note="120 out of 500 is 24 out of 100"),
        None,
    ])

# 033 84 minutes as a percent of 7 hours
ENTRIES[P + "033"] = entry(
    bars([bar([seg(1, "60 min", "a") for _ in range(7)], "7 hours"), bar([seg(1.4, "84 min", "b")], "84 minutes")], note="What percent of the long bar is the short bar?"),
    [
        bars([bar([seg(1, "60 min", "a") for _ in range(7)], "7 hours", "420 minutes"), bar([seg(1.4, "84 min", "b")], "84 minutes")], hl=["b0"]),
        bars([bar([seg(1, "60 min", "a") for _ in range(7)], "7 hours", "420 minutes"), bar([seg(1.4, "84 min", "b")], "84 minutes")], hl=["b1"], note="84 ÷ 420 × 100 = 20%"),
    ])

# 018 216 minutes as a part of a day
ENTRIES[P + "018"] = entry(None, [
    None,
    fbars([(20, 3, "216 of 1440 min")], note="216 minutes is 3 parts out of 20 of a day"),
    fbars([(20, 3, "216 of 1440 min")], note="3/20 = 0.15"),
])

# ── equations, sequences, place value, factors ──────────────────────────────

# 013 2p + 5 = 9p − 30
ENTRIES[P + "013"] = entry(
    bal("2p + 5", "9p − 30", note="Find p first, then (p + 3) × (p + 2)"),
    [
        bal("35", "7p", note="Add 30 to both pans, then take 2p off both. p = 5"),
        None,
        None,
    ])

# 021 4x − 7 = 12, find 12x − 14
ENTRIES[P + "021"] = entry(
    bal("4x − 7", "12", note="Both pans weigh the same. 12x − 14 = ?"),
    [
        bal("4x", "19", note="Add 7 to both pans"),
        bal("12x", "57", note="Make both pans 3 times as heavy"),
        bal("12x − 14", "43", note="Take 14 off both pans"),
    ])

# 016 59th term of 26, 30, 34, 38
ENTRIES[P + "016"] = entry(
    nl(26, 38, 4, points=[26, 30, 34, 38], hops=[(26, 30, "+4"), (30, 34, "+4"), (34, 38, "+4")], note="59th term = ?"),
    [
        nl(26, 38, 4, points=[26, 30, 34, 38], hops=[(26, 30, "+4"), (30, 34, "+4"), (34, 38, "+4")], note="Start at 26 and jump 4 each time, up to the 59th term"),
        nl(26, 38, 4, points=[26, 30, 34, 38], hops=[(26, 30, "+4"), (30, 34, "+4"), (34, 38, "+4")], note="58 jumps of 4 from 26: 26 + 232 = 258"),
    ])

# 026 falling series, gaps are primes
_pts26 = [126, 124, 121, 116, 109, 98]
ENTRIES[P + "026"] = entry(
    nl(98, 126, 1, points=_pts26, hops=[(126, 124, "?"), (124, 121, "?"), (121, 116, "?"), (116, 109, "?"), (109, 98, "?")], note="Look at the size of each jump back. 10th term = ?"),
    [
        nl(98, 126, 1, points=_pts26, hops=[(126, 124, "−2"), (124, 121, "−3"), (121, 116, "−5"), (116, 109, "−7"), (109, 98, "−11")], note="The jumps are the prime numbers"),
        None,
        tbl([["Jump", "−13", "−17", "−19", "−23"], ["Value", "85", "68", "49", "26"]], headers=["Term", "7th", "8th", "9th", "10th"], hl=["r1"]),
    ])

# 027 digit 6 in 97 × 999
ENTRIES[P + "027"] = entry(None, [
    place("96903", note="97 × 999 = 96903"),
    place("96903", hl=["d1"], note="The 6 sits in the thousands place"),
    place("96903", hl=["d1"], note="6 thousands = 6000"),
])

# 034 smallest 5-digit even number from 7, 4, 3, 6, 9
ENTRIES[P + "034"] = entry(None, [
    place("36794", hl=["d4"], note="Ending in 4, the smallest is 36794"),
    place("34796", hl=["d4"], note="Ending in 6, the smallest is 34796"),
    place("34796", note="34796 is the smaller of the two"),
    place("34796", hl=["d2"], note="The hundreds digit is 7"),
])

# 006 HCF and LCM of 48 and 120
ENTRIES[P + "006"] = entry(None, [
    fig("venn", leftTitle="48", rightTitle="120", left="rest of 48", both="2 × 2 × 2 × 3", right="rest of 120", highlight=["both"], note="Shared prime factors: 2 × 2 × 2 × 3 = 24"),
    fig("venn", leftTitle="48", rightTitle="120", left="2", both="2 × 2 × 2 × 3", right="5", highlight=["left", "both", "right"], note="Every factor once: 2 × 24 × 5 = 240"),
    None,
])
