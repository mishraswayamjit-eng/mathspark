"""2017 final paper, second batch: models for proportion, percent, interest, place value."""
from a_helpers import F, V, bar, bars, fb, seg

VISUALS = {}

# 72 men take 40 hours; 9 men take?
VISUALS["EXT_G5_FP_2017_008"] = V(
    F("table", headers=["Men", "Hours"], rows=[["72", "40"], ["9", "?"]],
      note="Fewer men need more hours for the same work"),
    [
        F("table", headers=["Men", "Hours", "Work"], rows=[["72", "40", "2880 man-hours"], ["9", "?", "2880 man-hours"]],
          hl=["r0"], note="The job is 72 × 40 = 2880 man-hours whoever does it"),
        F("table", headers=["Men", "Hours", "Work"], rows=[["72", "40", "2880 man-hours"], ["9", "320", "2880 man-hours"]],
          hl=["r1"], note="9 men need 2880 ÷ 9 = 320 hours"),
        F("table", headers=["Men", "Hours"], rows=[["72", "40"], ["9", "320"]],
          note="8 times fewer men, so 8 times as long: 40 × 8 = 320"),
    ])

# Simple interest on Rs.3000 at 12% for 5 years.
_yrs = [seg("12%", 1.2, "b") for _ in range(5)]
VISUALS["EXT_G5_FP_2017_009"] = V(
    bars(bar([seg("Rs.3000", 10, "a")], label="sum"),
         bar(_yrs, label="interest", brace="5 years = Rs.?"),
         note="Every year adds 12% of Rs.3000"),
    [
        bars(bar([seg("Rs.3000", 10, "a")], label="sum"),
             bar(_yrs, label="interest", brace="5 years = Rs.?"),
             hl=["b0"], note="1% of 3000 = 30"),
        bars(bar([seg("Rs.3000", 10, "a")], label="sum"),
             bar([seg("Rs.360", 1.2, "c")] + _yrs[1:], label="interest", brace="5 years = Rs.?"),
             hl=["b1s0"], note="One year at 12% = 12 × 30 = Rs.360"),
        bars(bar([seg("Rs.3000", 10, "a")], label="sum"),
             bar([seg("Rs.360", 1.2, "c") for _ in range(5)], label="interest", brace="5 years = Rs.1800"),
             hl=["b1"], note="Five years = 5 × 360 = Rs.1800"),
    ])

# Price cut from Rs.10800 to Rs.8640.
VISUALS["EXT_G5_FP_2017_012"] = V(
    bars(bar([seg("now Rs.8640", 3, "a"), seg("cut ?", 1, "unknown")], brace="was Rs.10800"),
         note="What percent of the old price was taken off?"),
    [
        bars(bar([seg("now Rs.8640", 4, "a"), seg("Rs.2160", 1, "b")], brace="was Rs.10800"),
             hl=["b0s1"], note="Cut = 10800 − 8640 = Rs.2160"),
        bars(bar([seg("now Rs.8640", 4, "a"), seg("20%", 1, "b")], brace="Rs.10800 = 100%"),
             hl=["b0s1"], note="2160 ÷ 10800 × 100 = 20%"),
    ])

# Two-digit numbers divisible by 2, 3 and 4.
VISUALS["EXT_G5_FP_2017_013"] = V(None, [
    None,
    F("numberLine", min=0, max=96, step=12,
      hops=[{"from": a, "to": a + 12} for a in range(0, 96, 12)],
      note="Jump in 12s: 12, 24, 36, 48, 60, 72, 84, 96 are the two-digit ones"),
    None,
])

# 21 oranges in dozens.
VISUALS["EXT_G5_FP_2017_014"] = V(
    F("set", total=21, item="oranges", note="How many dozens (groups of 12) is this?"),
    [
        fb((12, 12, "1 dozen"), (12, 9, "9 oranges left"), note="21 oranges = 1 full dozen and 9 left over"),
        fb((12, 12, "1 dozen"), (12, 9, "9/12 = 0.75"), hl=["b1"], note="9 out of 12 is 3/4 of a dozen = 0.75"),
        fb((12, 12, "1 dozen"), (12, 9, "0.75 dozen"), note="1 dozen + 0.75 dozen = 1.75 dozen"),
    ])

# Rs.2000 grows to Rs.3500 at 5% a year.
VISUALS["EXT_G5_FP_2017_017"] = V(
    bars(bar([seg("Rs.2000 put in", 2, "a"), seg("interest ?", 1, "unknown")], brace="Rs.3500 at the end"),
         note="Each year adds 5% of Rs.2000. How many years?"),
    [
        bars(bar([seg("Rs.2000 put in", 2, "a"), seg("Rs.1500", 1.5, "b")], brace="Rs.3500 at the end"),
             hl=["b0s1"], note="Interest needed = 3500 − 2000 = Rs.1500"),
        bars(bar([seg("Rs.2000 put in", 2, "a"), seg("Rs.1500", 1.5, "b")], brace="Rs.3500 at the end"),
             hl=["b0s0"], note="One year adds 5% of 2000 = Rs.100"),
        bars(bar([seg("Rs.2000 put in", 2, "a"), seg("15 × Rs.100", 1.5, "b")], brace="Rs.3500 at the end"),
             hl=["b0s1"], note="1500 ÷ 100 = 15 years"),
    ])

# 2x + 1 = 8, find 4x + 1.
VISUALS["EXT_G5_FP_2017_020"] = V(
    F("balance", left="2x + 1", right="8", note="Both pans weigh the same. What would 4x + 1 weigh?"),
    [
        F("balance", left="2x", right="7", note="Take 1 off both pans: 2x = 7"),
        F("balance", left="4x", right="14", note="Double both pans: 4x = 14"),
        F("balance", left="4x + 1", right="15", note="Put 1 back on both pans: 4x + 1 = 15"),
    ])

# 250000 lions, down by 90%.
_gone = [seg(None, 1, "b") for _ in range(9)]
VISUALS["EXT_G5_FP_2017_021"] = V(
    bars(bar(_gone + [seg("?", 1, "unknown")], brace="250000 lions in 1976"),
         note="90% of them are gone. How many are left?"),
    [
        bars(bar(_gone + [seg("10%", 1, "a")], brace="250000 lions = 100%"),
             hl=["b0s9"], note="Left = 100% − 90% = 10%"),
        bars(bar(_gone + [seg("25000", 1, "a")], brace="250000 lions = 100%"),
             hl=["b0s9"], note="10% is one of ten equal parts: 25000"),
        None,
    ])

# Rs.504 for 7 days; how many days for Rs.792?
VISUALS["EXT_G5_FP_2017_022"] = V(
    bars(bar([seg() for _ in range(7)], label="7 days", brace="Rs.504"),
         bar([seg("? days", 11, "unknown")], brace="Rs.792"),
         note="He earns the same amount every day"),
    [
        bars(bar([seg("Rs.72", tone="a")] + [seg() for _ in range(6)], label="7 days", brace="Rs.504"),
             bar([seg("? days", 11, "unknown")], brace="Rs.792"),
             hl=["b0s0"], note="One day pays 504 ÷ 7 = Rs.72"),
        bars(bar([seg("Rs.72", tone="a")] + [seg() for _ in range(6)], label="7 days", brace="Rs.504"),
             bar([seg("11 days", 11, "b")], brace="Rs.792"),
             hl=["b1"], note="792 ÷ 72 = 11 days"),
    ])

# A dozen pencils cost Rs.18; cost of 18 pencils.
VISUALS["EXT_G5_FP_2017_031"] = V(
    bars(bar([seg("Rs.18", 4, "a")], label="12 pencils"), bar([seg("Rs.?", 6, "unknown")], label="18 pencils"),
         note="A dozen is 12"),
    [
        bars(bar([seg("Rs.18", 4, "a")], label="12 pencils"), bar([seg("Rs.?", 6, "unknown")], label="18 pencils"),
             hl=["b0"], note="1 pencil costs 18 ÷ 12 = Rs.1.50"),
        bars(bar([seg("Rs.18", 4, "a")], label="12 pencils"), bar([seg("Rs.27", 6, "b")], label="18 pencils"),
             hl=["b1"], note="18 pencils cost 18 × 1.50 = Rs.27"),
    ])

# Greatest odd number from 7, 5, 2, 0, 4.
VISUALS["EXT_G5_FP_2017_033"] = V(
    F("table", rows=[["7", "5", "2", "0", "4"]], note="An odd number must end in an odd digit: 7 or 5"),
    [
        F("placeChart", number="74205", hl=["d4"], note="Ending in 5: biggest digits first gives 74205"),
        F("placeChart", number="54207", hl=["d4"], note="Ending in 7: the best start left is 5, giving 54207"),
        F("placeChart", number="74205", hl=["d0"], note="74205 starts with 7, so it is the greater one"),
        F("placeChart", number="75420", hl=["d4"], note="75420 ends in 0, so it is even"),
    ])

# Least number to subtract from 370 to reach a square.
VISUALS["EXT_G5_FP_2017_034"] = V(None, [
    F("numberLine", min=360, max=400, step=5,
      points=[{"at": 361, "label": "19² = 361"}, {"at": 370, "label": "370"}, {"at": 400, "label": "20² = 400"}],
      note="370 lies between the squares 361 and 400"),
    F("numberLine", min=360, max=400, step=5,
      points=[{"at": 361, "label": "361"}, {"at": 370, "label": "370"}],
      hops=[{"from": 370, "to": 361, "label": "− 9"}], hl=["h0"],
      note="Step back from 370 to 361: take away 9"),
])

# Tens digit is four times the thousands digit: check each choice.
VISUALS["EXT_G5_FP_2017_039"] = V(None, [
    F("placeChart", number="8621", hl=["d0", "d2"], note="Thousands 8, tens 2: the tens digit is the smaller one"),
    F("placeChart", number="2386", hl=["d0", "d2"], note="Thousands 2, tens 8: 8 = 4 × 2"),
    F("placeChart", number="8326", hl=["d0", "d2"], note="Thousands 8, tens 2 again, so this one does not fit"),
    F("placeChart", number="2386", hl=["d0", "d2"], note="2386 is the one that fits"),
], usesOptions=True)
