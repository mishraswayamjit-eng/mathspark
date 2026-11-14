"""2020 final paper, second batch: models for percent, proportion, interest, number lines."""
from a_helpers import F, V, bar, bars, seg

VISUALS = {}

# 20% of the bill is taken off and Rs.100 is still to pay.
VISUALS["EXT_G5_FP_2020_003"] = V(
    bars(bar([seg("Rs.100 to pay", 8, "a"), seg("20% off", 2, "b")], brace="the full bill = ?")),
    [
        bars(bar([seg("80% = Rs.100", 8, "a"), seg("20% off", 2, "b")], brace="the full bill = 100%"),
             hl=["b0s0"], note="What is left to pay is 100% − 20% = 80% of the bill"),
        bars(bar([seg("80% = Rs.100", 8, "a"), seg("20% off", 2, "b")], brace="the full bill = 100%"),
             hl=["b0s0"], note="1% = 100 ÷ 80 = Rs.1.25"),
        bars(bar([seg("80% = Rs.100", 8, "a"), seg("20% off", 2, "b")], brace="the full bill = Rs.125"),
             hl=["b0"], note="100% = Rs.125"),
    ])

# 8 dozens earn Rs.120; 20 dozens earn?
VISUALS["EXT_G5_FP_2020_009"] = V(
    bars(bar([seg("Rs.120", 4, "a")], label="8 dozens"), bar([seg("Rs.?", 10, "unknown")], label="20 dozens"),
         note="Every dozen earns the same"),
    [
        bars(bar([seg("Rs.120", 4, "a")], label="8 dozens"), bar([seg("Rs.?", 10, "unknown")], label="20 dozens"),
             hl=["b0"], note="One dozen earns 120 ÷ 8 = Rs.15"),
        bars(bar([seg("Rs.120", 4, "a")], label="8 dozens"), bar([seg("Rs.300", 10, "b")], label="20 dozens"),
             hl=["b1"], note="20 dozens earn 20 × 15 = Rs.300"),
    ])

# Rs.25 becomes Rs.37 at 16% a year.
VISUALS["EXT_G5_FP_2020_018"] = V(
    bars(bar([seg("Rs.25 put in", 2, "a"), seg("interest ?", 1, "unknown")], brace="Rs.37 at the end"),
         note="Each year adds 16% of Rs.25. How many years?"),
    [
        bars(bar([seg("Rs.25 put in", 2, "a"), seg("Rs.12", 1, "b")], brace="Rs.37 at the end"),
             hl=["b0s1"], note="Interest needed = 37 − 25 = Rs.12"),
        bars(bar([seg("Rs.25 put in", 2, "a"), seg("Rs.12", 1, "b")], brace="Rs.37 at the end"),
             hl=["b0s0"], note="One year adds 16% of 25 = Rs.4"),
        bars(bar([seg("Rs.25 put in", 6, "a"), seg("Rs.4", 1, "b"), seg("Rs.4", 1, "b"), seg("Rs.4", 1, "b")], brace="Rs.37 at the end"),
             hl=["b0s1", "b0s2", "b0s3"], note="12 ÷ 4 = 3 years"),
    ])

# Two consecutive primes that add to 42.
VISUALS["EXT_G5_FP_2020_023"] = V(None, [
    F("numberLine", min=17, max=25, step=1,
      points=[{"at": 19, "label": "prime"}, {"at": 21, "label": "half of 42"}, {"at": 23, "label": "prime"}],
      note="Look on either side of 21: the nearest primes are 19 and 23"),
    F("numberLine", min=17, max=25, step=1, points=[{"at": 19, "label": "19"}, {"at": 23, "label": "23"}],
      note="19 + 23 = 42, and no number between them is prime"),
    F("numberLine", min=17, max=25, step=1, points=[{"at": 19, "label": "19"}, {"at": 23, "label": "23"}],
      hops=[{"from": 19, "to": 23, "label": "4"}], hl=["h0"], note="Difference = 23 − 19 = 4"),
])

# Rs.27000 for 30 days of work; he works 18 days.
VISUALS["EXT_G5_FP_2020_024"] = V(
    bars(bar([seg("18 days worked", 6, "a"), seg("not worked", 4, "b")], brace="30 days = Rs.27000"),
         note="Pay him only for the days he worked"),
    [
        bars(bar([seg("18 days worked", 6, "a"), seg("not worked", 4, "b")], brace="30 days = Rs.27000"),
             hl=["b0"], note="One day pays 27000 ÷ 30 = Rs.900"),
        bars(bar([seg("Rs.16200", 6, "a"), seg("not worked", 4, "b")], brace="30 days = Rs.27000"),
             hl=["b0s0"], note="18 days pay 18 × 900 = Rs.16200"),
    ])

# Least number to add to 1300 to reach a square.
VISUALS["EXT_G5_FP_2020_025"] = V(None, [
    F("numberLine", min=1290, max=1370, step=5,
      points=[{"at": 1296, "label": "36² = 1296"}, {"at": 1300, "label": "1300"}, {"at": 1369, "label": "37² = 1369"}],
      note="1300 lies between the squares 1296 and 1369"),
    F("numberLine", min=1290, max=1370, step=5,
      points=[{"at": 1300, "label": "1300"}, {"at": 1369, "label": "1369"}],
      hops=[{"from": 1300, "to": 1369, "label": "+ 69"}], hl=["h0"],
      note="Step up from 1300 to 1369: add 69"),
])

# Ajay's sequence 3, 14, 25, 36, ...
_pts = [{"at": n} for n in (3, 14, 25, 36)]
VISUALS["EXT_G5_FP_2020_028"] = V(
    F("numberLine", min=3, max=47, step=11, points=_pts, note="What is the jump from each number to the next?"),
    [
        F("numberLine", min=3, max=47, step=11, points=_pts,
          hops=[{"from": 3, "to": 14, "label": "+ 11"}, {"from": 14, "to": 25, "label": "+ 11"}, {"from": 25, "to": 36, "label": "+ 11"}],
          note="Every term is 3 plus some jumps of 11"),
        None,
        F("numberLine", min=3, max=113, step=11, points=[{"at": 3, "label": "3"}, {"at": 113, "label": "113"}],
          hops=[{"from": 3, "to": 113, "label": "10 jumps of 11"}], hl=["p1"],
          note="113 − 3 = 110 = 11 × 10, so jumps of 11 land exactly on 113"),
        None,
    ])

# Rs.12000 borrowed, Rs.15600 returned after 5 years.
VISUALS["EXT_G5_FP_2020_030"] = V(
    bars(bar([seg("Rs.12000 borrowed", 10, "a"), seg("interest ?", 3, "unknown")], brace="Rs.15600 after 5 years"),
         note="What percent of Rs.12000 is added each year?"),
    [
        bars(bar([seg("Rs.12000 borrowed", 10, "a"), seg("Rs.3600", 3, "b")], brace="Rs.15600 after 5 years"),
             hl=["b0s1"], note="Interest = 15600 − 12000 = Rs.3600"),
        bars(bar([seg("Rs.12000 borrowed", 10, "a"), seg("Rs.3600", 3, "b")], brace="Rs.15600 after 5 years"),
             hl=["b0s1"], note="3600 × 100 ÷ (12000 × 5) = 6% each year"),
    ])

# 2 decagrams in 1-milligram doses.
VISUALS["EXT_G5_FP_2020_031"] = V(None, [
    F("table", headers=["Decagrams", "Grams"], rows=[["1", "10"], ["2", "20"]], hl=["r1"],
      note="A decagram is 10 grams, so 2 decagrams = 20 grams"),
    F("table", headers=["Grams", "Milligrams"], rows=[["1", "1000"], ["20", "20000"]], hl=["r1"],
      note="A gram is 1000 milligrams, so 20 grams = 20000 milligrams"),
    None,
])

# 5% of 5% of Rs.100 on a hundred square.
_five = [[0, c] for c in range(5)]
VISUALS["EXT_G5_FP_2020_032"] = V(
    F("grid", rows=10, cols=10, note="Rs.100 as 100 one-rupee squares. Take 5%, then 5% of that"),
    [
        F("grid", rows=10, cols=10, shaded=_five, note="5% of 100 is 5 squares: Rs.5"),
        F("grid", rows=10, cols=10, shaded=_five, note="Now 5% of those 5 rupees: 5 × 5 ÷ 100 = 0.25"),
        None,
    ])

# Bat sold for Rs.600 at 20% profit.
VISUALS["EXT_G5_FP_2020_034"] = V(
    bars(bar([seg("cost price ?", 10, "unknown"), seg("20%", 2, "b")], brace="sold for Rs.600"),
         note="The profit is 20% of the cost price"),
    [
        bars(bar([seg("cost = 100%", 10, "unknown"), seg("20%", 2, "b")], brace="120% = Rs.600"),
             note="Cost + profit = 120% of the cost, so 1% = 5"),
        bars(bar([seg("Rs.500", 10, "a"), seg("20%", 2, "b")], brace="120% = Rs.600"),
             hl=["b0s0"], note="Cost price = 5 × 100 = Rs.500"),
    ])

# Three consecutive numbers add to 66.
VISUALS["EXT_G5_FP_2020_036"] = V(
    bars(bar([seg("first", 1, "unknown"), seg("next", 1, "unknown"), seg("next", 1, "unknown")], brace="66 in all"),
         note="Three numbers in a row: each is 1 more than the one before"),
    [
        bars(bar([seg("first"), seg("22", 1, "a"), seg("last")], brace="66 in all"),
             hl=["b0s1"], note="The middle number is the average: 66 ÷ 3 = 22"),
        bars(bar([seg("21"), seg("22", 1, "a"), seg("23")], brace="66 in all"),
             note="One below and one above 22: 21, 22 and 23"),
        bars(bar([seg("21"), seg("22"), seg("23", 1, "a")], brace="66 in all"),
             hl=["b0s2"], note="23 is the one in the choices"),
    ])

# 555 digits used to number the pages.
VISUALS["EXT_G5_FP_2020_037"] = V(None, [
    F("table", headers=["Pages", "How many", "Digits"], rows=[["1 to 9", "9", "9"]],
      note="One-digit pages use 9 digits"),
    F("table", headers=["Pages", "How many", "Digits"], rows=[["1 to 9", "9", "9"], ["10 to 99", "90", "180"]], hl=["r1"],
      note="Two-digit pages use 90 × 2 = 180 digits: 189 so far"),
    F("table", headers=["Pages", "How many", "Digits"],
      rows=[["1 to 9", "9", "9"], ["10 to 99", "90", "180"], ["100 onwards", "122", "366"]], hl=["r2"],
      note="555 − 189 = 366 digits left, 3 for each page: 122 pages"),
    F("table", headers=["Pages", "How many", "Digits"],
      rows=[["1 to 9", "9", "9"], ["10 to 99", "90", "180"], ["100 onwards", "122", "366"]],
      note="Last page = 99 + 122 = 221"),
])
