"""2018 final paper, second batch: models for work, fractions of a group, percent, interest."""
from a_helpers import F, V, bar, bars, seg

VISUALS = {}

# Nine men take 32 days; 72 men take?
VISUALS["EXT_G5_FP_2018_010"] = V(
    F("table", headers=["Men", "Days"], rows=[["nine", "32"], ["72", "?"]],
      note="More men finish the same work in fewer days"),
    [
        F("table", headers=["Men", "Days", "Work"], rows=[["9", "32", "288 man-days"], ["72", "?", "288 man-days"]],
          hl=["r0"], note="The job is 9 × 32 = 288 man-days whoever does it"),
        F("table", headers=["Men", "Days", "Work"], rows=[["9", "32", "288 man-days"], ["72", "4", "288 man-days"]],
          hl=["r1"], note="72 men need 288 ÷ 72 = 4 days"),
        F("table", headers=["Men", "Days"], rows=[["9", "32"], ["72", "4"]],
          note="8 times as many men, so 8 times quicker: 32 ÷ 8 = 4"),
    ])

# Museum: 4/5 adults, 120 children, 3/8 of the adults male.
_ad = [seg("adults", 1, "a") for _ in range(4)]
VISUALS["EXT_G5_FP_2018_013"] = V(
    bars(bar(_ad + [seg("120 children", 1, "b")], brace="all visitors"),
         bar([seg("male", 1, "c") for _ in range(3)] + [seg(None, 1, "a") for _ in range(5)], brace="the adults"),
         note="4/5 are adults; 3/8 of the adults are male. Male adults = ?"),
    [
        bars(bar(_ad + [seg("120 children", 1, "b")], brace="all visitors"),
             hl=["b0s4"], note="Children are the other 1/5 of the visitors = 120"),
        bars(bar([seg("120", 1, "a") for _ in range(4)] + [seg("120", 1, "b")], brace="600 visitors"),
             hl=["b0s0", "b0s1", "b0s2", "b0s3"], note="Visitors = 120 × 5 = 600; adults = 600 − 120 = 480"),
        bars(bar([seg("male", 1, "c") for _ in range(3)] + [seg(None, 1, "a") for _ in range(5)], brace="480 adults"),
             hl=["b0s0", "b0s1", "b0s2"], note="3/8 of 480 = 480 ÷ 8 × 3 = 180 male adults"),
    ])

# Interest on Rs.8000 at 6% for 2 years.
VISUALS["EXT_G5_FP_2018_015"] = V(
    bars(bar([seg("Rs.8000", 10, "a")], label="deposit"),
         bar([seg("6%", 0.6, "b"), seg("6%", 0.6, "b")], label="interest", brace="2 years = Rs.?"),
         note="Each year adds 6% of Rs.8000"),
    [
        bars(bar([seg("Rs.8000", 10, "a")], label="deposit"),
             bar([seg("Rs.480", 0.6, "c"), seg("6%", 0.6, "b")], label="interest", brace="2 years = Rs.?"),
             hl=["b1s0"], note="1% of 8000 = 80, so 6% = Rs.480 for one year"),
        bars(bar([seg("Rs.8000", 10, "a")], label="deposit"),
             bar([seg("Rs.480", 0.6, "c"), seg("Rs.480", 0.6, "c")], label="interest", brace="2 years = Rs.960"),
             hl=["b1"], note="Two years: 480 × 2 = Rs.960"),
    ])

# Books: money from sales = cost + profit.
VISUALS["EXT_G5_FP_2018_019"] = V(
    bars(bar([seg("cost of 6 dozen ?", 4, "unknown"), seg("profit Rs.180", 1, "b")], brace="3 × Rs.150 + 3 × Rs.200"),
         note="The money from selling covers the cost and the profit"),
    [
        bars(bar([seg("cost of 6 dozen ?", 4, "unknown"), seg("profit Rs.180", 1, "b")], brace="sold for Rs.1050"),
             note="Sales = 3 × 150 + 3 × 200 = 450 + 600 = Rs.1050"),
        bars(bar([seg("cost Rs.870", 4, "a"), seg("profit Rs.180", 1, "b")], brace="sold for Rs.1050"),
             hl=["b0s0"], note="Cost = 1050 − 180 = Rs.870 for 6 dozen"),
        bars(bar([seg("Rs.145", 1, "a")] + [seg(None, 1, "a") for _ in range(5)], brace="Rs.870 for 6 dozen"),
             hl=["b0s0"], note="One dozen cost 870 ÷ 6 = Rs.145"),
    ])

# 15 dozens gain Rs.45; how many dozens gain Rs.84?
VISUALS["EXT_G5_FP_2018_025"] = V(
    bars(bar([seg("gain Rs.45", 5, "a")], label="15 dozens"), bar([seg("gain Rs.84", 9, "b")], label="? dozens"),
         note="Every dozen brings the same gain"),
    [
        bars(bar([seg("gain Rs.45", 5, "a")], label="15 dozens"), bar([seg("gain Rs.84", 9, "b")], label="? dozens"),
             hl=["b0"], note="One dozen gains 45 ÷ 15 = Rs.3"),
        bars(bar([seg("gain Rs.45", 5, "a")], label="15 dozens"), bar([seg("gain Rs.84", 9, "b")], label="28 dozens"),
             hl=["b1"], note="84 ÷ 3 = 28 dozens"),
    ])

# Rs.800 article at 20% discount.
VISUALS["EXT_G5_FP_2018_030"] = V(
    bars(bar([seg("sale price ?", 8, "unknown"), seg("20% off", 2, "b")], brace="Rs.800")),
    [
        bars(bar([seg("sale price ?", 8, "unknown"), seg("Rs.160 off", 2, "b")], brace="Rs.800"),
             hl=["b0s1"], note="20% of 800 = Rs.160"),
        bars(bar([seg("Rs.640", 8, "a"), seg("Rs.160 off", 2, "b")], brace="Rs.800"),
             hl=["b0s0"], note="Sale price = 800 − 160 = Rs.640"),
    ])

# Rs.4000 doubles at 12.5% simple interest.
VISUALS["EXT_G5_FP_2018_031"] = V(
    bars(bar([seg("Rs.4000", 8, "a")], label="sum"),
         bar([seg("interest so far", 8, "unknown")], label="to double"),
         note="Each year adds 12.5% of Rs.4000. How many years to double?"),
    [
        bars(bar([seg("Rs.4000", 8, "a")], label="sum"),
             bar([seg("Rs.4000", 8, "b")], label="interest"),
             hl=["b1"], note="To double, the interest must equal the sum: Rs.4000"),
        bars(bar([seg("Rs.4000", 8, "a")], label="sum"),
             bar([seg("Rs.500", 1, "c"), seg(None, 7, "b")], label="interest", brace="Rs.4000"),
             hl=["b1s0"], note="One year adds 12.5% of 4000 = Rs.500"),
        bars(bar([seg("Rs.4000", 8, "a")], label="sum"),
             bar([seg("500", 1, "c") for _ in range(8)], label="interest", brace="Rs.4000 in 8 years"),
             hl=["b1"], note="4000 ÷ 500 = 8 years"),
    ])

# Five tests of 80 marks: 30% on the first four, 35% wanted overall.
_four = [seg("30%", 1, "a") for _ in range(4)]
VISUALS["EXT_G5_FP_2018_035"] = V(
    bars(bar(_four + [seg("?", 1, "unknown")], brace="5 tests of 80 marks"),
         note="He wants 35% of all the marks. Marks needed in the 5th test?"),
    [
        bars(bar(_four + [seg("?", 1, "unknown")], brace="400 marks: need 140"),
             hl=["b0"], note="All 5 tests: 5 × 80 = 400 marks; 35% of 400 = 140"),
        bars(bar(_four + [seg("?", 1, "unknown")], brace="400 marks: need 140"),
             hl=["b0s0", "b0s1", "b0s2", "b0s3"], note="First 4 tests: 30% of 320 = 96 marks so far"),
        bars(bar([seg("96 marks so far", 4, "a"), seg("44", 1, "b")], brace="400 marks: need 140"),
             hl=["b0s1"], note="5th test: 140 − 96 = 44 marks"),
    ])
