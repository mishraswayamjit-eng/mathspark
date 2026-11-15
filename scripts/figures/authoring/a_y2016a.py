"""2016 final paper, first batch. Each entry was decided by reading that question."""
from a_helpers import F, V, bar, bars, fb, seg

VISUALS = {}

# Three bags, 24 apples; overlapping pair totals.
VISUALS["EXT_G5_FP_2016_002"] = V(
    bars(bar([seg("first", tone="a"), seg("second", tone="b"), seg("third", tone="c")], brace="24 apples"),
         note="first + second = 11, second + third = 18, first + third = ?"),
    [
        bars(bar([seg("first", tone="a"), seg("second", tone="a"), seg("13", tone="c")], brace="24 apples"),
             hl=["b0s2"], note="Take away first + second: 24 − 11 = 13 in the third bag"),
        bars(bar([seg("6", tone="a"), seg("second", tone="b"), seg("third", tone="b")], brace="24 apples"),
             hl=["b0s0"], note="Take away second + third: 24 − 18 = 6 in the first bag"),
        bars(bar([seg("6", tone="a"), seg("second", tone="b"), seg("13", tone="a")], brace="24 apples"),
             hl=["b0s0", "b0s2"], note="first + third = 6 + 13 = 19"),
    ])

# Whole numbers between 4 squared and 4 cubed: the ends do not count.
VISUALS["EXT_G5_FP_2016_003"] = V(None, [
    F("numberLine", min=16, max=64, step=4, points=[{"at": 16, "label": "4²"}, {"at": 64, "label": "4³"}],
      note="4² = 16 and 4³ = 64"),
    F("numberLine", min=16, max=64, step=4, points=[{"at": 16, "label": "16"}, {"at": 64, "label": "64"}],
      hops=[{"from": 16, "to": 64, "label": "17 to 63"}], note="Between means 16 and 64 themselves are left out"),
    None,
])

# Hour hand 4/5 of the way from 12 to 1.
VISUALS["EXT_G5_FP_2016_004"] = V(
    fb((5, 4, "from 12 to 1"), note="The hour hand has gone 4/5 of the way from 12 to 1"),
    [
        fb((5, 0, "12 to 1 = 60 min"), note="The whole stretch from 12 to 1 takes 60 minutes"),
        fb((5, 4, "4/5 of 60 minutes"), note="4 of the 5 equal parts of the hour have passed"),
        fb((5, 4, "4 × 12 = 48 min"), note="Each fifth is 60 ÷ 5 = 12 minutes, so 4 fifths = 48 minutes"),
        F("clock", hour=12, minute=48, hl=["hour"], note="The time is 12:48"),
    ])

# 36 is 12% of which number?
VISUALS["EXT_G5_FP_2016_005"] = V(
    bars(bar([seg("12% = 36", units=2.4, tone="a"), seg("the rest", units=8.8, tone="b")], brace="100% = ?")),
    [
        bars(bar([seg("12% = 36", units=2.4, tone="a"), seg("the rest", units=8.8, tone="b")], brace="100% = ?"),
             hl=["b0s0"], note="12% is 36, so 1% = 36 ÷ 12 = 3"),
        bars(bar([seg("12% = 36", units=2.4, tone="a"), seg("the rest", units=8.8, tone="b")], brace="100% = 300"),
             hl=["b0"], note="100% = 3 × 100 = 300"),
    ])

# Pay = regular pay + overtime pay.
VISUALS["EXT_G5_FP_2016_007"] = V(
    bars(bar([seg("40 h at Rs.3", tone="a"), seg("overtime: ? h", tone="unknown")], brace="Rs.168 paid"),
         note="Overtime is paid at twice Rs.3 per hour"),
    [
        bars(bar([seg("Rs.120", tone="a"), seg("overtime", tone="unknown")], brace="Rs.168 paid"),
             hl=["b0s0"], note="Regular pay = 40 × 3 = Rs.120"),
        bars(bar([seg("Rs.120", tone="a"), seg("Rs.48", tone="b")], brace="Rs.168 paid"),
             hl=["b0s1"], note="Overtime pay = 168 − 120 = Rs.48"),
        None,
        bars(bar([seg("Rs.120", tone="a"), seg("Rs.48 = 8 h", tone="b")], brace="Rs.168 paid"),
             hl=["b0s1"], note="Rs.48 at Rs.6 an hour = 8 hours of overtime"),
    ])

# 1 hr 15 min as a decimal of an hour.
VISUALS["EXT_G5_FP_2016_010"] = V(
    F("clock", hour=12, minute=15, hl=["minute"], note="What part of a full hour is 15 minutes?"),
    [
        fb((4, 1, "15 min = 1/4 hr"), shape="circle", note="15 out of 60 minutes is 1/4 of an hour = 0.25 hr"),
        fb((1, 1, "1 hr"), (4, 1, "0.25 hr"), shape="circle", note="1 hr + 0.25 hr = 1.25 hr"),
    ])

# A fraction between 1/3 and 7/8.
VISUALS["EXT_G5_FP_2016_012"] = V(
    fb((3, 1, "1/3"), (8, 7, "7/8"), note="Which fraction is bigger than 1/3 but smaller than 7/8?"),
    [
        fb((24, 8, "1/3 = 8/24"), (24, 21, "7/8 = 21/24"), note="Cut both into 24 equal parts to compare"),
        fb((24, 6, "1/4 = 6/24"), (24, 23, "23/24"), (24, 22, "11/12 = 22/24"),
           note="6 is below 8; 23 and 22 are above 21"),
        fb((24, 8, "8/24"), (24, 17, "17/24"), (24, 21, "21/24"), hl=["b1"],
           note="17/24 sits between 8/24 and 21/24"),
    ])

# Walk + ride = 37 min, walk + walk = 55 min, ride + ride = ?
VISUALS["EXT_G5_FP_2016_013"] = V(
    bars(bar([seg("walk", 3, "a"), seg("ride", 1, "b")], brace="37 min"),
         bar([seg("walk", 3, "a"), seg("walk", 3, "a")], brace="55 min"),
         bar([seg("ride", 1, "b"), seg("ride", 1, "b")], brace="? min")),
    [
        bars(bar([seg("walk", 3, "a"), seg("ride", 1, "b")], brace="37 min"),
             bar([seg("27.5", 3, "a"), seg("27.5", 3, "a")], brace="55 min"),
             bar([seg("ride", 1, "b"), seg("ride", 1, "b")], brace="? min"),
             hl=["b1"], note="Two walks take 55 min, so one walk = 55 ÷ 2 = 27.5 min"),
        bars(bar([seg("27.5", 3, "a"), seg("9.5", 1, "b")], brace="37 min"),
             bar([seg("27.5", 3, "a"), seg("27.5", 3, "a")], brace="55 min"),
             bar([seg("ride", 1, "b"), seg("ride", 1, "b")], brace="? min"),
             hl=["b0s1"], note="One ride = 37 − 27.5 = 9.5 min"),
        bars(bar([seg("27.5", 3, "a"), seg("9.5", 1, "b")], brace="37 min"),
             bar([seg("27.5", 3, "a"), seg("27.5", 3, "a")], brace="55 min"),
             bar([seg("9.5", 1, "b"), seg("9.5", 1, "b")], brace="19 min"),
             hl=["b2"], note="Two rides = 2 × 9.5 = 19 minutes"),
    ])

# Rectangle: one side 8 cm, perimeter 40 cm, area?
VISUALS["EXT_G5_FP_2016_015"] = V(
    F("rectangle", length="?", breadth="8 cm", inside="Perimeter = 40 cm", note="Find the other side first, then the area"),
    [
        F("rectangle", length="?", breadth="8 cm", hl=["length", "breadth"],
          note="One length + one breadth = half the perimeter = 40 ÷ 2 = 20 cm"),
        F("rectangle", length="12 cm", breadth="8 cm", hl=["length"], note="Other side = 20 − 8 = 12 cm"),
        F("rectangle", length="12 cm", breadth="8 cm", inside="Area = 96 cm²", hl=["fill"], note="Area = 8 × 12 = 96 cm²"),
    ])

# 40 gm costs Rs.12; 70 gm costs?
VISUALS["EXT_G5_FP_2016_017"] = V(
    bars(bar([seg("Rs.12", 4, "a")], label="40 gm"), bar([seg("Rs.?", 7, "unknown")], label="70 gm")),
    [
        bars(bar([seg("Rs.12", 4, "a")], label="40 gm"), bar([seg("Rs.?", 7, "unknown")], label="70 gm"),
             hl=["b0"], note="1 gm costs 12 ÷ 40 = Rs.0.30"),
        bars(bar([seg("Rs.12", 4, "a")], label="40 gm"), bar([seg("Rs.21", 7, "b")], label="70 gm"),
             hl=["b1"], note="70 gm costs 70 × 0.30 = Rs.21"),
    ])

# How many tens in one crore: place-value chart once solving starts.
VISUALS["EXT_G5_FP_2016_018"] = V(None, [
    F("placeChart", number="10000000", note="One crore is 1 followed by seven zeros"),
    F("placeChart", number="1000000", note="Dividing by 10 removes one zero: 1,000,000 tens"),
    F("placeChart", number="1000000", hl=["d0"], note="The 1 is in the ten-lakhs place: ten lakh tens"),
])
