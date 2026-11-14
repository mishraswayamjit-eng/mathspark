"""2016 final paper, second batch."""
from a_helpers import F, V, bar, bars, fb, seg

VISUALS = {}

# Smallest five-digit odd number from the digits 1, 8, 4, 0, 7; place value of 4.
VISUALS["EXT_G5_FP_2016_019"] = V(
    F("table", rows=[["1", "8", "4", "0", "7"]], note="Make the smallest odd number using every digit once"),
    [
        F("placeChart", number="10487", hl=["d4"], note="Ending in 7, the smallest is 10487"),
        F("placeChart", number="40781", hl=["d4"], note="Ending in 1, the smallest is 40781 (it cannot start with 0)"),
        F("placeChart", number="10487", note="10487 is the smaller of the two"),
        F("placeChart", number="10487", hl=["d2"], note="The 4 sits in the hundreds place: 4 × 100 = 400"),
    ])

# Digits of 2138574 that keep their place when sorted.
VISUALS["EXT_G5_FP_2016_024"] = V(
    F("placeChart", number="2138574", note="Sort the digits smallest first. Which digits do not move?"),
    [
        F("placeChart", number="2138574", note="The number as given: 2 1 3 8 5 7 4"),
        None,
        F("placeChart", number="2138574", hl=["d2", "d4", "d5"], note="Sorted is 1 2 3 4 5 7 8: only 3, 5 and 7 stay put"),
        None,
    ])

# 1/2 − 1/4 − 1/3 + 1/6 in twelfths.
VISUALS["EXT_G5_FP_2016_029"] = V(None, [
    fb((12, 6, "1/2 = 6/12"), (12, 3, "1/4 = 3/12"), (12, 4, "1/3 = 4/12"), (12, 2, "1/6 = 2/12"),
       note="Cut every strip into 12 equal parts"),
    fb((12, 1, "1/12"), note="6 − 3 − 4 + 2 = 1 twelfth is left"),
    None,
])

# Shirt marked Rs.700 sold for Rs.651.
VISUALS["EXT_G5_FP_2016_032"] = V(
    bars(bar([seg("sold for Rs.651", 4, "a"), seg("discount ?", 1, "unknown")], brace="Rs.700 marked"),
         note="What percent of Rs.700 is the discount?"),
    [
        bars(bar([seg("sold for Rs.651", 4, "a"), seg("Rs.49", 1, "b")], brace="Rs.700 marked"),
             hl=["b0s1"], note="Discount = 700 − 651 = Rs.49"),
        bars(bar([seg("sold for Rs.651", 4, "a"), seg("Rs.49 = 7%", 1, "b")], brace="Rs.700 = 100%"),
             hl=["b0s1"], note="49 out of 700 is 7 out of every 100, so 7%"),
    ])

# 27 eggs in dozens.
VISUALS["EXT_G5_FP_2016_033"] = V(
    F("set", total=27, item="eggs", note="How many dozens (groups of 12) is this?"),
    [
        fb((12, 12, "1 dozen"), (12, 12, "1 dozen"), (12, 3, "3 eggs left"),
           note="27 eggs = 2 full dozens and 3 eggs left over"),
        fb((12, 12, "1 dozen"), (12, 12, "1 dozen"), (12, 3, "3/12 = 0.25"), hl=["b2"],
           note="3 out of 12 is a quarter of a dozen = 0.25"),
        fb((12, 12, "1 dozen"), (12, 12, "1 dozen"), (12, 3, "0.25 dozen"),
           note="2 dozens + 0.25 dozen = 2.25 dozen"),
    ])

# 12 buckets hold 108 litres; how many for 162 litres?
VISUALS["EXT_G5_FP_2016_034"] = V(
    bars(bar([seg() for _ in range(12)], label="12 buckets", brace="108 litres"),
         bar([seg("? buckets", 12, "unknown")], brace="162 litres"),
         note="Every bucket holds the same amount"),
    [
        bars(bar([seg("9 L", tone="a")] + [seg() for _ in range(11)], label="12 buckets", brace="108 litres"),
             bar([seg("? buckets", 12, "unknown")], brace="162 litres"),
             hl=["b0s0"], note="One bucket holds 108 ÷ 12 = 9 litres"),
        bars(bar([seg("9 L", tone="a")] + [seg() for _ in range(11)], label="12 buckets", brace="108 litres"),
             bar([seg("18 buckets", 12, "b")], brace="162 litres"),
             hl=["b1"], note="162 ÷ 9 = 18 buckets"),
    ])

# Five gifts, Rs.21 in all, with overlapping pair totals.
VISUALS["EXT_G5_FP_2016_035"] = V(
    bars(bar([seg("A"), seg("B"), seg("C"), seg("D"), seg("E")], brace="Rs.21 in all"),
         note="A+B = 6, B+C = 10, C+D = 7, D+E = 9. A + E = ?"),
    [
        bars(bar([seg("A", tone="a"), seg("B", tone="a"), seg("C", tone="b"), seg("D", tone="b"), seg("E")], brace="Rs.21 in all"),
             hl=["b0s0", "b0s1", "b0s2", "b0s3"], note="A + B and C + D do not overlap: 6 + 7 = 13"),
        bars(bar([seg("A", tone="a"), seg("B", tone="a"), seg("C", tone="b"), seg("D", tone="b"), seg("E = 8", tone="c")], brace="Rs.21 in all"),
             hl=["b0s4"], note="What is left is E: 21 − 13 = 8"),
        bars(bar([seg("A = 2"), seg("B = 4"), seg("C = 6"), seg("D = 1"), seg("E = 8")], brace="Rs.21 in all"),
             note="Work back along the pairs: D = 1, C = 6, B = 4, A = 2"),
        bars(bar([seg("A = 2", tone="a"), seg("B = 4"), seg("C = 6"), seg("D = 1"), seg("E = 8", tone="a")], brace="Rs.21 in all"),
             hl=["b0s0", "b0s4"], note="A + E = 2 + 8 = 10"),
    ])

# Three times an angle equals its supplement.
VISUALS["EXT_G5_FP_2016_037"] = V(
    bars(bar([seg("x", tone="a")], label="angle"),
         bar([seg("x", tone="b"), seg("x", tone="b"), seg("x", tone="b")], label="supplement"),
         note="An angle and its supplement together make 180°"),
    [
        F("angles", layout="onLine", parts=[{"label": "x"}, {"label": "180° − x"}],
          note="The angle and its supplement sit together on a straight line"),
        bars(bar([seg("x", tone="a"), seg("x", tone="b"), seg("x", tone="b"), seg("x", tone="b")], brace="180°"),
             note="The supplement is 3 lots of x, so 4 lots of x make 180°"),
        F("angles", layout="onLine", parts=[{"label": "45°", "size": 45}, {"label": "135°"}], hl=["p0"],
          note="x = 180° ÷ 4 = 45°, and its supplement is 135°"),
    ])

# Triangle with sides in terms of a, a = 3.
VISUALS["EXT_G5_FP_2016_038"] = V(
    F("triangle", shape="scalene", sides={"ab": "(2a + 6) cm", "bc": "(3a + 5) cm", "ca": "(a + 7) cm"},
      note="a = 3. Perimeter = ?"),
    [
        F("triangle", shape="scalene", sides={"ab": "12 cm", "bc": "(3a + 5) cm", "ca": "(a + 7) cm"}, hl=["ab"],
          note="2 × 3 + 6 = 12 cm"),
        F("triangle", shape="scalene", sides={"ab": "12 cm", "bc": "14 cm", "ca": "(a + 7) cm"}, hl=["bc"],
          note="3 × 3 + 5 = 14 cm"),
        F("triangle", shape="scalene", sides={"ab": "12 cm", "bc": "14 cm", "ca": "10 cm"}, hl=["ca"],
          note="3 + 7 = 10 cm"),
        F("triangle", shape="scalene", sides={"ab": "12 cm", "bc": "14 cm", "ca": "10 cm"}, hl=["ab", "bc", "ca"],
          note="Perimeter = 12 + 14 + 10 = 36 cm"),
    ])

# Sum that grows to Rs.4500 in 5 years at 10% a year.
_si = [seg("10%", 0.5, "b") for _ in range(5)]
VISUALS["EXT_G5_FP_2016_039"] = V(
    bars(bar([seg("the sum = 100%", 5, "unknown")] + _si, brace="Rs.4500 after 5 years"),
         note="Each year adds 10% of the sum as interest"),
    [
        bars(bar([seg("the sum = 100%", 5, "unknown")] + _si, brace="Rs.4500 after 5 years"),
             hl=["b0s1", "b0s2", "b0s3", "b0s4", "b0s5"], note="Interest for 5 years = 5 × 10% = 50% of the sum"),
        bars(bar([seg("the sum = 100%", 5, "unknown"), seg("interest = 50%", 2.5, "b")], brace="150% = Rs.4500"),
             note="Sum + interest = 100% + 50% = 150% of the sum"),
        bars(bar([seg("Rs.3000", 5, "a"), seg("interest = 50%", 2.5, "b")], brace="150% = Rs.4500"),
             hl=["b0s0"], note="1% = 4500 ÷ 150 = 30, so the sum = Rs.3000"),
    ])
