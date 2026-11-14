"""2019 final paper, second batch: models for percent, interest, proportion, place value."""
from a_helpers import F, V, bar, bars, seg

VISUALS = {}

# Sold for Rs.407 at 10% profit.
VISUALS["EXT_G5_FP_2019_002"] = V(
    bars(bar([seg("cost price ?", 10, "unknown"), seg("10%", 1, "b")], brace="sold for Rs.407"),
         note="The profit is 10% of the cost price"),
    [
        bars(bar([seg("cost = 100%", 10, "unknown"), seg("10%", 1, "b")], brace="110% = Rs.407"),
             note="Cost + profit = 110% of the cost, so 1% = 407 ÷ 110 = 3.7"),
        bars(bar([seg("Rs.370", 10, "a"), seg("10%", 1, "b")], brace="110% = Rs.407"),
             hl=["b0s0"], note="Cost price = 3.7 × 100 = Rs.370"),
    ])

# Ordering five decimals.
_sorted = [["0.560"], ["0.062"], ["0.050"], ["0.034"], ["0.007"]]
VISUALS["EXT_G5_FP_2019_003"] = V(None, [
    F("table", rows=[["0.062"], ["0.050"], ["0.560"], ["0.034"], ["0.007"]],
      note="Give every number 3 decimal places so they line up"),
    F("table", rows=_sorted, note="Biggest first: 0.560, 0.062, 0.050, 0.034, 0.007"),
    F("table", rows=_sorted, hl=["r0", "r3"], note="1st is 0.56 and 4th is 0.034"),
    None,
])

# Sum that earns Rs.189 in 3 years at 9%.
_y9 = [seg("9%", 0.9, "b") for _ in range(3)]
VISUALS["EXT_G5_FP_2019_004"] = V(
    bars(bar([seg("sum = ?", 10, "unknown")]),
         bar(_y9, label="interest", brace="Rs.189 in 3 years"),
         note="Each year adds 9% of the sum"),
    [
        bars(bar([seg("sum = 100%", 10, "unknown")]),
             bar([seg("27% of the sum", 2.7, "b")], label="interest", brace="Rs.189 in 3 years"),
             hl=["b1"], note="3 years at 9% = 27% of the sum"),
        bars(bar([seg("Rs.700", 10, "a")]),
             bar([seg("27% of the sum", 2.7, "b")], label="interest", brace="Rs.189 in 3 years"),
             hl=["b0"], note="Sum = 189 × 100 ÷ 27 = Rs.700"),
        bars(bar([seg("Rs.700", 10, "a")]),
             bar([seg("Rs.63", 0.9, "c") for _ in range(3)], label="interest", brace="Rs.189 in 3 years"),
             note="Check: 9% of 700 = 63 a year, and 63 × 3 = 189"),
    ])

# 850 soldiers in a square formation.
VISUALS["EXT_G5_FP_2019_008"] = V(None, [
    F("numberLine", min=840, max=900, step=5,
      points=[{"at": 841, "label": "29 × 29"}, {"at": 850, "label": "850"}, {"at": 900, "label": "30 × 30"}],
      note="850 lies between the squares 841 and 900"),
    None,
    F("numberLine", min=840, max=900, step=5,
      points=[{"at": 841, "label": "841 in rows"}, {"at": 850, "label": "850"}],
      hops=[{"from": 841, "to": 850, "label": "9 left out"}], hl=["h0"],
      note="850 − 841 = 9 soldiers are left out"),
])

# Five persons eat 1 kg a day; 20 people in a week.
VISUALS["EXT_G5_FP_2019_009"] = V(
    F("table", headers=["People", "Time", "Rice"], rows=[["five", "1 day", "1 kg"], ["20", "1 week", "?"]],
      note="Change one thing at a time: first the people, then the days"),
    [
        F("table", headers=["People", "Time", "Rice"], rows=[["5", "1 day", "1 kg"], ["20", "1 day", "4 kg"], ["20", "1 week", "?"]],
          hl=["r1"], note="20 people is 4 groups of 5, so 4 kg in a day"),
        F("table", headers=["People", "Time", "Rice"], rows=[["5", "1 day", "1 kg"], ["20", "1 day", "4 kg"], ["20", "7 days", "28 kg"]],
          hl=["r2"], note="A week is 7 days: 4 × 7 = 28 kg"),
    ])

# Five litres cost Rs.370; three litres?
VISUALS["EXT_G5_FP_2019_015"] = V(
    bars(bar([seg() for _ in range(5)], label="five litres", brace="Rs.370"),
         bar([seg(None, 1, "unknown") for _ in range(3)], label="three litres", brace="Rs.?"),
         note="Each litre costs the same"),
    [
        bars(bar([seg("Rs.74", 1, "a")] + [seg() for _ in range(4)], label="5 litres", brace="Rs.370"),
             bar([seg(None, 1, "unknown") for _ in range(3)], label="three litres", brace="Rs.?"),
             hl=["b0s0"], note="1 litre = 370 ÷ 5 = Rs.74"),
        bars(bar([seg("Rs.74", 1, "a")] + [seg() for _ in range(4)], label="5 litres", brace="Rs.370"),
             bar([seg("Rs.74", 1, "b") for _ in range(3)], label="3 litres", brace="Rs.222"),
             hl=["b1"], note="3 litres = 3 × 74 = Rs.222"),
    ])

# 40% passed; 420 did not.
VISUALS["EXT_G5_FP_2019_016"] = V(
    bars(bar([seg("40% passed", 4, "a"), seg("420 did not pass", 6, "b")], brace="all students = ?")),
    [
        bars(bar([seg("40% passed", 4, "a"), seg("60% = 420", 6, "b")], brace="all students = ?"),
             hl=["b0s1"], note="The rest is 100% − 40% = 60%, and that is 420 students"),
        bars(bar([seg("40% passed", 4, "a"), seg("60% = 420", 6, "b")], brace="all students = ?"),
             hl=["b0s1"], note="1% = 420 ÷ 60 = 7 students"),
        bars(bar([seg("40% passed", 4, "a"), seg("60% = 420", 6, "b")], brace="100% = 700 students"),
             hl=["b0"], note="100% = 700 students"),
    ])

# Four-digit numbers from 2, 3, 4, 5 with 5 in the hundreds place.
VISUALS["EXT_G5_FP_2019_020"] = V(
    F("table", headers=["Th", "H", "T", "O"], rows=[["?", "5", "?", "?"]],
      note="2, 3 and 4 fill the empty places, each used once"),
    [
        F("table", headers=["Th", "H", "T", "O"], rows=[["?", "5", "?", "?"]], note="Fix the 5 in the hundreds place"),
        None,
        F("table", headers=["Th", "H", "T", "O"], rows=[["3 choices", "5", "2 choices", "1 choice"]],
          note="3 × 2 × 1 = 6 different numbers"),
        None,
    ])

# 150 toys a minute; how many in 18 seconds?
VISUALS["EXT_G5_FP_2019_029"] = V(
    bars(bar([seg("150 toys", 10, "a")], label="60 seconds"), bar([seg("? toys", 3, "unknown")], label="18 seconds"),
         note="One minute is 60 seconds"),
    [
        bars(bar([seg("150 toys", 10, "a")], label="60 seconds"), bar([seg("? toys", 3, "unknown")], label="18 seconds"),
             hl=["b0"], note="In 1 second: 150 ÷ 60 = 2.5 toys"),
        bars(bar([seg("150 toys", 10, "a")], label="60 seconds"), bar([seg("45 toys", 3, "b")], label="18 seconds"),
             hl=["b1"], note="In 18 seconds: 2.5 × 18 = 45 toys"),
    ])

# Smallest number from the digits of 75003064.
VISUALS["EXT_G5_FP_2019_030"] = V(
    F("placeChart", number="75003064", note="Use the same digits to make the smallest number"),
    [
        F("placeChart", number="75003064", hl=["d2", "d3", "d5"], note="Digits 7, 5, 0, 0, 3, 0, 6, 4: there are three zeros"),
        None,
        F("placeChart", number="30004567", hl=["d0"], note="Start with 3 (not 0), then the zeros, then 4, 5, 6, 7"),
    ])

# Rs.3200 becomes Rs.3680 in 3 years.
VISUALS["EXT_G5_FP_2019_031"] = V(
    bars(bar([seg("Rs.3200 put in", 5, "a"), seg("interest ?", 1, "unknown")], brace="Rs.3680 after 3 years"),
         note="What percent of Rs.3200 is added each year?"),
    [
        bars(bar([seg("Rs.3200 put in", 5, "a"), seg("Rs.480", 1, "b")], brace="Rs.3680 after 3 years"),
             hl=["b0s1"], note="Interest = 3680 − 3200 = Rs.480"),
        bars(bar([seg("Rs.3200 put in", 5, "a"), seg("Rs.480", 1, "b")], brace="Rs.3680 after 3 years"),
             hl=["b0s1"], note="480 × 100 ÷ (3200 × 3) = 5% each year"),
    ])

# Smallest number to add to 1325 to reach a square.
VISUALS["EXT_G5_FP_2019_034"] = V(None, [
    F("numberLine", min=1290, max=1370, step=5,
      points=[{"at": 1296, "label": "36² = 1296"}, {"at": 1325, "label": "1325"}, {"at": 1369, "label": "37² = 1369"}],
      note="1325 lies between the squares 1296 and 1369"),
    F("numberLine", min=1290, max=1370, step=5,
      points=[{"at": 1325, "label": "1325"}, {"at": 1369, "label": "1369"}],
      hops=[{"from": 1325, "to": 1369, "label": "+ 44"}], hl=["h0"],
      note="Step up from 1325 to 1369: add 44"),
])

# Pen bought for Rs.40, sold at 25% profit.
VISUALS["EXT_G5_FP_2019_035"] = V(
    bars(bar([seg("cost Rs.40", 4, "a"), seg("25% profit", 1, "b")], brace="selling price = ?"),
         note="The profit is 25% of Rs.40"),
    [
        bars(bar([seg("cost Rs.40", 4, "a"), seg("Rs.10", 1, "b")], brace="selling price = ?"),
             hl=["b0s1"], note="Profit = 25% of 40 = Rs.10"),
        bars(bar([seg("cost Rs.40", 4, "a"), seg("Rs.10", 1, "b")], brace="selling price = Rs.50"),
             hl=["b0"], note="Selling price = 40 + 10 = Rs.50"),
    ])

# Place values of 7 and 5 in 87459.
VISUALS["EXT_G5_FP_2019_037"] = V(
    F("placeChart", number="87459", hl=["d1", "d3"], note="How many times the value of the 5 is the value of the 7?"),
    [
        F("placeChart", number="87459", hl=["d1", "d3"], note="7 is in the thousands (7000); 5 is in the tens (50)"),
        F("placeChart", number="87459", hl=["d1", "d3"], note="7000 ÷ 50 = 140 times"),
    ])

# Girls 735, which is 145 fewer than boys; commerce and science streams.
VISUALS["EXT_G5_FP_2019_038"] = V(
    bars(bar([seg("735", 5, "a")], label="girls"),
         bar([seg(None, 5, "a"), seg("145 more", 1, "b")], label="boys"),
         note="Commerce has 435 boys and 375 girls. The rest take science"),
    [
        bars(bar([seg("735", 5, "a")], label="girls"),
             bar([seg("735", 5, "a"), seg("145", 1, "b")], label="boys", brace="880 boys"),
             hl=["b1"], note="Boys = 735 + 145 = 880"),
        bars(bar([seg("735", 5, "a")], label="girls"),
             bar([seg("880", 6, "b")], label="boys"),
             note="All students = 880 + 735 = 1615"),
        bars(bar([seg("commerce", 1, "a"), seg("science ?", 1, "unknown")], brace="1615 students"),
             hl=["b0s0"], note="Commerce = 435 + 375 = 810"),
        bars(bar([seg("commerce 810", 1, "a"), seg("science 805", 1, "b")], brace="1615 students"),
             hl=["b0s1"], note="Science = 1615 − 810 = 805"),
    ])
