"""Figures for Grade 4 "Decimal Fractions" (gr4_decimals).

    python -X utf8 scripts/figures/authoring/g4_gr4_decimals.py            # build the part file
    python -X utf8 scripts/figures/authoring/g4_gr4_decimals.py --review   # also print every figure against its question

Writes data/question-figures/parts/g4-gr4_decimals.json.

By rule: "X buys N things at Rs.P each and pays Rs.M. How much change?" (a bar model read from the question).
Everything else is drawn one question at a time:
  - multiplying or dividing by 10, 100, 1000: the number in the place-value chart, before and after;
  - comparing and ordering: a table that gives every number the same count of decimal places, or a number line;
  - word problems: bar models in proportion (a piece too thin to label is widened a little);
  - fractions and decimals: fraction strips, or a 10 by 10 square for hundredths.
A place-value chart is not shown before answering when naming the place is the answer.
"""
import re
import sys

from g4_gr4_numbers_lib import Part, pc, table, line, grid, bm, bar, seg, fb, journey, step_texts

P = Part("gr4_decimals")


def chart(number, idx=None, note=None):
    return pc(str(number), note=note, hl=["d%d" % i for i in idx] if idx else None)


def widths(values):
    """Drawn widths in proportion to the values; a piece under a ninth of the whole is widened so its label fits."""
    floor = sum(values) / 9.0
    grown = [max(v, floor) for v in values]
    scale = 10.0 / max(grown)
    return [round(max(0.2, v * scale), 3) for v in grown]


def strip(labels, values, tones=None, brace=None, label=None):
    """One bar of labelled pieces drawn in proportion to `values`.

    A piece that is still unknown ("?") is drawn as wide as the average known piece, as the contract
    asks, so its width does not give the answer away. Once its value is shown it is drawn to scale.
    """
    tones = tones or ["a"] * len(labels)
    hidden = [t == "unknown" and l == "?" for l, t in zip(labels, tones)]
    known = [v for v, h in zip(values, hidden) if not h]
    if any(hidden) and known:
        mean = sum(known) / float(len(known))
        values = [mean if h else v for v, h in zip(values, hidden)]
    return bar([seg(l, w, t) for l, w, t in zip(labels, widths(values), tones)], label=label, brace=brace)


def compare(big, small, gap, big_label, small_label, gap_label, note=None, hl=None):
    """Two bars, one under the other: the bigger number, and the smaller number with the gap beside it."""
    w = widths([big, small, gap])
    return bm([bar([seg(big_label, w[0], "a")]),
               bar([seg(small_label, w[1], "b"),
                    seg(gap_label, max(0.2, round(w[0] - w[1], 3)), "unknown" if gap_label == "?" else "c")])],
              note=note, hl=hl)


def padded(rows, headers=None, note=None, hl=None):
    return table([list(r) for r in rows], headers=headers, note=note, hl=hl)


# ── Rule: change from a payment ──────────────────────────────────────────────
CHANGE = re.compile(r"^(\w+) buys (\d+) (\w+) at Rs\.(\d+) each and pays Rs\.(\d+)\. How much change does \w+ get back\?$")


def rule_change(q):
    m = CHANGE.match(q["questionText"])
    if not m:
        return False
    name, n, item, price, paid = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    cost = n * price
    change = paid - cost
    texts = step_texts(q)
    assert change > 0 and len(texts) == 2
    brace = "Rs.%d paid" % paid
    w = widths([cost, change])
    # While the change is unknown its piece is drawn as wide as one item, not to scale.
    # Label each item's piece only where the piece is wide enough to hold the price.
    roomy = 292.0 / (n + 1) >= 34
    before = bm([bar([seg("Rs.%d" % price if roomy else None, 1, "a") for i in range(n)]
                     + [seg("?", 1, "unknown")], brace=brace)],
                note="%d %s at Rs.%d each, then the change" % (n, item, price))
    # Step 1 finds the cost ("... so they cost 5 × 5 = 25 rupees"); step 2 takes it from the money paid.
    cost_sum = re.search(r"\d+ × \d+ = \d+", texts[0]).group(0)
    change_sum = re.search(r"\d+ − \d+ = \d+", texts[1]).group(0)
    assert cost_sum.endswith("= %d" % cost) and change_sum.endswith("= %d" % change), q["id"]
    steps = [
        bm([bar([seg("Rs.%d" % cost, n, "a"), seg("?", 1, "unknown")], brace=brace)],
           note="The %d %s cost %s rupees" % (n, item, cost_sum), hl=["b0s0"]),
        bm([bar([seg("Rs.%d" % cost, w[0], "a"), seg("Rs.%d" % change, w[1], "b")], brace=brace)],
           note="Take the cost away: %s rupees of change" % change_sum, hl=["b0s1"]),
    ]
    P.add(q, before, steps, origin="rule")
    return True


for _q in P.qs:
    rule_change(_q)


# ── Individually drawn ───────────────────────────────────────────────────────
A = P.add

# Multiplying and dividing by 10, 100, 1000: the digits move across the chart
A("Q_CH11_001",
  chart("12.5", None, "Divide by 10: where does each digit move?"),
  {0: chart("12.5", None, "Dividing by 10 makes the number ten times smaller"),
   1: chart("1.25", None, "The point moves one place left: between the 1 and the 2"),
   2: chart("1.25", None, "12.5 ÷ 10 = 1.25")})
A("Q_CH11_002",
  chart("12.5", None, "Divide by 100: where does each digit move?"),
  {0: chart("12.5", None, "100 has two zeros: the point moves two places to the left"),
   1: chart("0.125", [0], "The point moves past the 2 and the 1. A 0 goes in front"),
   2: chart("0.125", None, "12.5 ÷ 100 = 0.125")})
A("Q_CH11_003",
  chart("12.5", None, "Divide by 10000: where does each digit move?"),
  {1: chart("0.125", None, "Dividing by 10 twice gives 1.25, then 0.125")})
A("Q_CH11_008",
  chart("7.06", None, "Divide by 10: where does each digit move?"),
  {0: chart("7.06", None, "Every digit moves one place to the right"),
   1: chart("0.706", [1, 2, 3], "7 tenths, 0 hundredths and 6 thousandths"),
   2: chart("0.706", None, "7.06 ÷ 10 = 0.706")})
A("Q_CH11_009",
  chart("652.7", None, "Divide by 100: where does each digit move?"),
  {1: chart("65.27", None, "One place: 652.7 becomes 65.27"),
   2: chart("6.527", None, "One more place: 652.7 ÷ 100 = 6.527")})
A("Q_CH11_010",
  chart("3.8", None, "Divide by 100: where does each digit move?"),
  {1: chart("0.38", None, "One place: 3.8 becomes 0.38"),
   2: chart("0.038", [1], "One more place: a zero fills the gap"),
   3: chart("0.038", None, "3.8 ÷ 100 = 0.038")})
A("Q_CH11_023",
  chart("809", None, "Divide by 10: where does each digit move?"),
  {0: chart("809.0", None, "Write 809 as 809.0"),
   1: chart("80.9", None, "The point moves one place to the left. The 0 stays"),
   2: chart("80.9", None, "809 ÷ 10 = 80.9")})
A("PYQ_2019_Q19", None, {
    1: chart("0.357", None, "One place: 0.0357 becomes 0.357"),
    2: chart("3.57", None, "One more place: 0.0357 × 100 = 3.57")})
A("G4A_DECIMALS_007",
  chart("4.50", None, "Multiply by 10: where does each digit move?"),
  {0: chart("45.00", None, "Each digit moves one place to the left"),
   1: chart("45.00", None, "10 pencils cost Rs. 45.00")})
A("G4A_DECIMALS_016",
  chart("0.045", None, "First multiply by 1000, then divide by 10"),
  {0: chart("45", None, "× 1000: every digit moves three places to the left"),
   1: chart("4.5", None, "÷ 10: every digit moves one place to the right"),
   2: chart("4.5", None, "The answer is 4.5")})
A("G4A_DECIMALS_017",
  chart("3.7", None, "The number in the box, times 100, gives this"),
  {1: chart("0.037", [1], "3.7 ÷ 100: every digit moves two places to the right"),
   2: chart("0.037", None, "0.037 × 100 = 3.7")})
A("G4A_DECIMALS_033",
  chart("62.5", None, "This is the number after it was multiplied by 10"),
  {0: chart("6.25", None, "Undo the multiplying: 62.5 ÷ 10 = 6.25"),
   1: chart("0.625", None, "Now divide by 10, as Rahul was asked to"),
   2: chart("0.625", None, "His answer should have been 0.625")})
A("G4A_DECIMALS_050",
  chart("0.47", None, "This is the number after it was divided by 10"),
  {0: chart("4.7", None, "Undo the division: 0.47 × 10 = 4.7"),
   1: chart("47", None, "Now multiply by 10, as Arun was asked to"),
   2: chart("47", None, "Arun should have got 47")})

# Reading decimal places
A("G4A_DECIMALS_001", None, {
    0: chart("536.429", [3, 4, 5], "4 tenths, 2 hundredths and 9 thousandths"),
    1: chart("536.429", [4], "The digit in the hundredths place is 2")})
A("G4A_DECIMALS_002", None, {
    2: chart("7.09", [1, 2], "0 in the tenths place and 9 in the hundredths place")})
A("G4A_DECIMALS_003", None, {
    2: chart("4.307", [1, 2, 3], "3 tenths, 0 hundredths and 7 thousandths")})
A("G4A_DECIMALS_010", None, {1: chart("8.05", [1, 2], "8 rupees and 5 paise is Rs. 8.05")})
A("G4A_DECIMALS_012",
  chart("5.252", [1, 3], "Compare the values of the two marked 2s"),
  {0: chart("5.252", [1], "The first 2 is in the tenths place: 0.2"),
   1: chart("5.252", [3], "The second 2 is in the thousandths place: 0.002"),
   2: chart("5.252", [1, 3], "Two places apart, and each place is 10 times as large"),
   3: chart("5.252", [1, 3], "0.2 is 100 times as large as 0.002")})
A("G4A_DECIMALS_029", None, {
    0: chart("8.530", None, "Greatest: the digits from biggest to smallest"),
    1: chart("0.358", None, "Smallest: the digits from smallest to biggest")})
A("Q_CH11_020", None, {
    0: chart("45.783", [2, 3, 4], "After the point: tenths, hundredths, thousandths"),
    1: chart("45.783", [2, 3], "7 is in the tenths place. 8 is the second digit after the point"),
    2: chart("45.783", [3], "The digit 8 is in the hundredths place")})
A("PYQ_2018_Q08", None, {
    0: chart("7.256", [1, 2, 3], "The digits after the decimal point are 2, 5 and 6"),
    1: chart("7.256", [2], "The 5 is in the hundredths place"),
    2: chart("7.256", [2], "5 hundredths is 5/100")})

# Number lines
A("G4A_DECIMALS_004",
  line(4.3, 4.4, 0.01, points=[(4.3, "4.3"), (4.4, "4.4")], ticks="none", note="Which number lies between 4.3 and 4.4?"),
  {0: line(4.3, 4.4, 0.01, points=[(4.3, "4.30"), (4.4, "4.40")], ticks="none", note="Write the ends as 4.30 and 4.40"),
   1: line(4.3, 4.4, 0.01, points=[(4.3, "4.30"), (4.35, "4.35"), (4.4, "4.40")], ticks="none", hl=["p1"],
           note="4.35 is more than 4.30 and less than 4.40")})
A("G4A_DECIMALS_023",
  line(2.4, 2.5, 0.01, points=[(2.4, "2.4"), (2.5, "2.5")], ticks="none", note="Which number is exactly halfway?"),
  {0: line(2.4, 2.5, 0.01, points=[(2.4, "2.40"), (2.5, "2.50")], ticks="none", note="Write the ends as 2.40 and 2.50"),
   1: line(2.4, 2.5, 0.01, points=[(2.4, "2.40"), (2.5, "2.50")], hops=[(2.4, 2.5, "0.10")], ticks="none",
           note="The gap is 0.10, and half of the gap is 0.05"),
   2: line(2.4, 2.5, 0.01, points=[(2.4, "2.40"), (2.5, "2.50")], hops=[(2.4, 2.45, "+0.05")], ticks="none"),
   3: line(2.4, 2.5, 0.01, points=[(2.4, "2.40"), (2.45, "2.45"), (2.5, "2.50")], ticks="none", hl=["p1"],
           note="2.45 is exactly halfway")})
A("G4A_DECIMALS_025",
  line(0.4, 1.3, 0.3, points=[(0.4, "0.4"), (0.7, "0.7"), (1.0, "1.0"), (1.3, "1.3")],
       hops=[(0.4, 0.7, "?"), (0.7, 1.0, "?"), (1.0, 1.3, "?")], ticks="none", note="How big is each jump?"),
  {3: line(0.4, 2.5, 0.3, points=[(0.4, "1st"), (2.5, "8th")], ticks="none", note="7 jumps from the 1st number reach 2.5")})
A("G4A_DECIMALS_028",
  line(36, 39, 0.25, points=[(36.8, "36.8 cm")], ticks="none", note="Up 1.5 cm, then down 0.75 cm"),
  {0: line(36, 39, 0.25, points=[(36.8, "36.8"), (38.3, "38.3")], hops=[(36.8, 38.3, "+1.5")], ticks="none"),
   1: line(36, 39, 0.25, points=[(36.8, None), (37.55, "37.55"), (38.3, None)],
           hops=[(36.8, 38.3, "+1.5"), (38.3, 37.55, "−0.75")], ticks="none"),
   2: line(36, 39, 0.25, points=[(36.8, None), (37.55, "37.55"), (38.3, None)],
           hops=[(36.8, 38.3, "+1.5"), (38.3, 37.55, "−0.75")], ticks="none", hl=["p1"],
           note="The water is now 37.55 cm deep")})
A("G4A_DECIMALS_031",
  line(1.5, 4, 2.5, points=[(1.5, "1.5 cm"), (4, "4 cm")], ticks="none", note="It grows 0.25 cm every day"),
  {0: line(1.5, 4, 2.5, points=[(1.5, "1.5 cm"), (4, "4 cm")], hops=[(1.5, 4, "?")], ticks="none",
           note="How much does it still have to grow?"),
   3: line(1.5, 4, 0.25, points=[(1.5, "1.5 cm"), (4, "4 cm")], ticks="none",
           note="10 jumps of 0.25 cm, one each day, reach 4 cm")})
A("G4A_DECIMALS_043", None, {
    0: chart("49.50", None, "The largest number that starts with 49"),
    1: chart("50.49", None, "The smallest number that starts with 50"),
    2: line(49.4, 50.6, 0.1, points=[(49.5, "49.50"), (50, "50"), (50.49, "50.49")], ticks="none",
            note="The gap 0.49 is smaller than the gap 0.50"),
    3: line(49.4, 50.6, 0.1, points=[(49.5, "49.50"), (50, "50"), (50.49, "50.49")], ticks="none", hl=["p2"],
            note="50.49 is closest to 50")})
A("G4A_DECIMALS_046", None, {
    2: line(0.2, 0.55, 0.05, points=[(0.25, "1/4"), (0.5, "1/2")], ticks="none", note="The ends are 0.250 and 0.500"),
    3: line(0.2, 0.55, 0.05, points=[(0.25, "1/4"), (0.255, None), (0.26, None), (0.3, None), (0.45, None), (0.5, "1/2")],
            ticks="none", note="0.255, 0.26, 0.3 and 0.45 lie between them: 4 numbers")})
A("G4A_DECIMALS_047",
  line(0.3, 0.31, 0.001, points=[(0.3, "0.3"), (0.31, "0.31")], ticks="none",
       note="Numbers with three decimal digits between these two"),
  {0: line(0.3, 0.31, 0.001, points=[(0.3, "0.300"), (0.31, "0.310")], ticks="none"),
   1: line(0.3, 0.31, 0.001, points=[(0.3, "0.300"), (0.31, "0.310")], ticks="none",
           note="0.301 up to 0.309 sit on the ticks in between"),
   3: line(0.3, 0.31, 0.001, points=[(0.3, "0.300"), (0.31, "0.310")], ticks="none",
           note="9 numbers lie between the two ends")})
A("G4A_DECIMALS_051",
  line(5.3, 5.8, 0.1, points=[(5.4, "5.4"), (5.68, "5.68")], ticks="none", note="5.□8 must lie between these two numbers"),
  {0: line(5.3, 5.8, 0.1, points=[(5.4, "5.40"), (5.68, "5.68")], ticks="none"),
   2: line(5.3, 5.8, 0.1, points=[(5.4, "5.40"), (5.48, "5.48"), (5.58, "5.58"), (5.68, "5.68")], ticks="none",
           hl=["p1", "p2"], note="5.48 and 5.58 lie between 5.40 and 5.68")})
A("EXT_G4_WS2_CH11_002", None, {
    1: line(0, 1, 0.05, points=[(0.05, "0.05"), (0.5, "0.50")], ticks="ends", note="5 hundredths and 50 hundredths"),
    2: line(0, 1, 0.05, points=[(0.05, "0.05"), (0.5, "0.5")], ticks="ends", hl=["p1"], note="0.5 is the greater number")})
A("EXT_G4_WS2_CH11_003",
  line(4.7, 4.8, 0.01, points=[(4.756, "4.756")], ticks="none", note="Which tenth is 4.756 nearer to?"),
  {0: chart("4.756", [1, 2], "The tenths digit is 7. The digit after it is 5"),
   1: line(4.7, 4.8, 0.01, points=[(4.7, "4.7"), (4.756, "4.756"), (4.8, "4.8")], hops=[(4.756, 4.8)], ticks="none",
           note="The next digit is 5 or more, so round up: 7 becomes 8"),
   2: line(4.7, 4.8, 0.01, points=[(4.756, None), (4.8, "4.8")], hops=[(4.756, 4.8)], ticks="none", hl=["p1"],
           note="4.756 rounds to 4.8")})

# Comparing and ordering: give every number the same count of decimal places
H2 = ["Number", "Same places"]
_g13 = [["0.5", "0.500"], ["0.05", "0.050"], ["0.55", "0.550"], ["0.505", "0.505"]]
A("Q_CH11_013", None, {
    0: padded(_g13, H2, "Write every number with three decimal places"),
    1: padded(_g13, H2, "0.050 has 0 tenths. The other three have 5 tenths", ["r1"]),
    2: padded(_g13, H2, "0.550 has 5 hundredths. 0.500 and 0.505 have 0 hundredths", ["r2"]),
    3: padded(_g13, H2, "The greatest is 0.55", ["r2"])})
_a24 = [["3.3", "3.300"], ["3.03", "3.030"], ["3.303", "3.303"], ["3.33", "3.330"]]
A("Q_CH11_024", None, {
    0: padded(_a24, H2, "Write every number with three decimal places"),
    1: padded(_a24, H2, "3.030 has 0 tenths, so it is the smallest", ["r1"]),
    2: padded(_a24, H2, "3.330 has 3 hundredths, so it is the greatest", ["r3"]),
    3: padded(_a24, H2, "3.300 has 0 thousandths, so it comes before 3.303", ["r0", "r2"]),
    4: padded([["3.03", "3.030"], ["3.3", "3.300"], ["3.303", "3.303"], ["3.33", "3.330"]], H2, "In ascending order, smallest first")})
# Sums of several decimals: only the lining-up and sorting steps have something to show.
A("EXT_G4_FP_2022_021", None, {
    0: padded([["12.1212"], ["17.0050"], ["9.1102"]], None, "Four decimal places each, with the points lined up")})
_signs = [["Added", "1.8", "2.3", "2.7"], ["Taken away", "1.9", "3.2", "-"]]
A("EXT_G4_FP_2024_016", None, {
    0: padded(_signs, None, "Add up the numbers that are being added", ["r0"]),
    1: padded(_signs, None, "Add up the numbers that are being taken away", ["r1"])})
A("PYQ_2018_Q06", None, {
    0: padded([["0.007", "0.007"], ["0.07", "0.070"], ["7.07", "7.070"], ["0.70", "0.700"]], H2),
    2: padded([["0.007", "0.007"], ["0.07", "0.070"], ["7.07", "7.070"], ["0.70", "0.700"]], H2,
              "7 thousandths is the least", ["r0"])})
A("PYQ_2016_Q30", None, {
    0: padded([["0.023", "0.0230"], ["0.23", "0.2300"], ["0.0023", "0.0023"], ["2.3", "2.3000"]], H2),
    1: padded([["0.023", "0.0230"], ["0.23", "0.2300"], ["0.0023", "0.0023"], ["2.3", "2.3000"]], H2,
              "The smallest is 0.0023 and the greatest is 2.3", ["r2", "r3"])})
A("EXT_G4_FP_2021_026", None, {
    0: padded([["4.004", "4.004"], ["4.04", "4.040"], ["4.4", "4.400"], ["4.444", "4.444"]], H2),
    3: padded([["4.004", "4.004"], ["4.04", "4.040"], ["4.4", "4.400"], ["4.444", "4.444"]], H2,
              "Already in order, smallest first")})
A("EXT_G4_FP_2022_024", None, {
    0: padded([["0.0075", "0.0075"], ["0.219", "0.2190"], ["0.082", "0.0820"], ["0.07", "0.0700"], ["0.008", "0.0080"]], H2),
    1: padded([["0.219", "0.2190"], ["0.082", "0.0820"], ["0.07", "0.0700"], ["0.008", "0.0080"], ["0.0075", "0.0075"]], H2,
              "Descending: biggest first"),
    2: padded([["0.219", "0.2190"], ["0.082", "0.0820"], ["0.07", "0.0700"], ["0.008", "0.0080"], ["0.0075", "0.0075"]], H2,
              "The 1st is 0.219 and the 4th is 0.008", ["r0", "r3"])})
A("G4A_DECIMALS_011",
  padded([["Anil", "3.38 m"], ["Bharat", "3.045 m"], ["Chirag", "3.4 m"], ["Dinesh", "3.405 m"]], ["Child", "Jump"]),
  {0: padded([["Anil", "3.38 m", "3.380"], ["Bharat", "3.045 m", "3.045"], ["Chirag", "3.4 m", "3.400"], ["Dinesh", "3.405 m", "3.405"]],
             ["Child", "Jump", "Same places"]),
   1: padded([["Dinesh", "3.405"], ["Chirag", "3.400"], ["Anil", "3.380"], ["Bharat", "3.045"]], ["Child", "Jump"],
             "Longest jump first"),
   2: padded([["Dinesh", "3.405"], ["Chirag", "3.400"], ["Anil", "3.380"], ["Bharat", "3.045"]], ["Child", "Jump"],
             "Chirag came second", ["r1"])})
A("G4A_DECIMALS_018", None, {
    2: padded([["0.58", "0.580"], ["3/5", "0.600"], ["5/8", "0.625"], ["0.65", "0.650"]], ["Number", "As a decimal"]),
    3: padded([["0.58", "0.580"], ["3/5", "0.600"], ["5/8", "0.625"], ["0.65", "0.650"]], ["Number", "As a decimal"],
              "The greatest is 0.65", ["r3"])})
A("G4A_DECIMALS_034", None, {
    2: padded([["0.4", "0.400"], ["3/8", "0.375"], ["0.38", "0.380"], ["7/20", "0.350"]], ["Number", "As a decimal"]),
    3: padded([["7/20", "0.350"], ["3/8", "0.375"], ["0.38", "0.380"], ["0.4", "0.400"]], ["Number", "As a decimal"],
              "In order, smallest first")})
A("G4A_DECIMALS_041",
  padded([["Asha", "12.5"], ["Bina", "12.45"], ["Chetan", "12.058"], ["Dev", "12.6"], ["Esha", "12.509"]], ["Child", "Seconds"]),
  {0: padded([["Asha", "12.500"], ["Bina", "12.450"], ["Chetan", "12.058"], ["Dev", "12.600"], ["Esha", "12.509"]],
             ["Child", "Seconds"], "Every time with three decimal places"),
   1: padded([["Chetan", "12.058"], ["Bina", "12.450"], ["Asha", "12.500"], ["Esha", "12.509"], ["Dev", "12.600"]],
             ["Child", "Seconds"], "Least time first"),
   2: padded([["Chetan", "12.058"], ["Bina", "12.450"], ["Asha", "12.500"], ["Esha", "12.509"], ["Dev", "12.600"]],
             ["Child", "Seconds"], "Chetan came first", ["r0"]),
   3: padded([["Chetan", "12.058"], ["Bina", "12.450"], ["Asha", "12.500"], ["Esha", "12.509"], ["Dev", "12.600"]],
             ["Child", "Seconds"], "Bina came second", ["r1"])})
A("G4A_DECIMALS_048", None, {
    0: padded([["2.5", "2.500"], ["2.45", "2.450"], ["2.405", "2.405"], ["2.08", "2.080"], ["2.6", "2.600"]], H2),
    1: padded([["2.08", "2.080"], ["2.405", "2.405"], ["2.45", "2.450"], ["2.5", "2.500"], ["2.6", "2.600"]], H2,
              "In order, smallest first"),
    2: padded([["2.08", "2.080"], ["2.405", "2.405"], ["2.45", "2.450"], ["2.5", "2.500"], ["2.6", "2.600"]], H2,
              "The smallest is 2.08 and the middle one is 2.45", ["r0", "r2"])})
A("G4A_DECIMALS_053",
  padded([["Anu", "0.6"], ["Bala", "5/8"], ["Charu", "0.58"], ["Dinu", "13/20"]], ["Child", "Drank"]),
  {1: padded([["Anu", "0.6", "0.600"], ["Bala", "5/8", "0.625"], ["Charu", "0.58", "0.580"], ["Dinu", "13/20", "0.650"]],
             ["Child", "Drank", "As a decimal"]),
   2: padded([["Anu", "0.6", "0.600"], ["Bala", "5/8", "0.625"], ["Charu", "0.58", "0.580"], ["Dinu", "13/20", "0.650"]],
             ["Child", "Drank", "As a decimal"], "The smallest amount drunk is 0.580", ["r2"]),
   3: padded([["Anu", "0.6", "0.600"], ["Bala", "5/8", "0.625"], ["Charu", "0.58", "0.580"], ["Dinu", "13/20", "0.650"]],
             ["Child", "Drank", "As a decimal"], "Charu drank the least, so she has the most left", ["r2"])})

# Word problems: bar models and journeys
A("G4A_DECIMALS_005",
  journey(["Home", "School", "Library"], [{"top": "1.6 km"}, {"top": "0.85 km"}], "Total distance = ?"),
  {0: journey(["Home", "School", "Library"], [{"top": "1.60 km"}, {"top": "0.85 km"}], "Write both with two decimal places"),
   2: journey(["Home", "School", "Library"], [{"top": "1.60 km"}, {"top": "0.85 km"}], "Riya walks 2.45 km in all",
              ["l0", "l1"])})
A("G4A_DECIMALS_006",
  bm([strip(["1.35 m", "?"], [1.35, 3.65], ["a", "unknown"], "5 m")], note="A piece is cut off. How much is left?"),
  {0: bm([strip(["1.35 m", "?"], [1.35, 3.65], ["a", "unknown"], "5.00 m")], note="Write 5 m as 5.00 m"),
   2: bm([strip(["1.35 m", "3.65 m"], [1.35, 3.65], ["a", "b"], "5.00 m")], hl=["b0s1"], note="3.65 m of rope is left")})
A("G4A_DECIMALS_009",
  bm([bar([seg("?", 1, "unknown")] + [seg(None, 1, "a")] * 5, brace="7.2 m")], note="6 equal pieces"),
  {0: bm([bar([seg("?", 1, "unknown")] + [seg(None, 1, "a")] * 5, brace="72 tenths")], note="7.2 m is 72 tenths of a metre"),
   2: bm([bar([seg("1.2 m", 1, "b")] * 6, brace="7.2 m")], note="12 tenths is 1.2, so each piece is 1.2 m")})
A("G4A_DECIMALS_013",
  bm([strip(["2.5", "0.375", "14"], [2.5, 0.375, 14], ["a", "b", "c"], "? kg")], note="Three parcels, in kg. Total weight = ?"),
  {0: bm([strip(["2.500", "0.375", "14.000"], [2.5, 0.375, 14], ["a", "b", "c"], "?")],
         note="Give every weight three decimal places"),
   1: bm([strip(["2.500", "0.375", "14.000"], [2.5, 0.375, 14], ["a", "b", "c"], "?")], hl=["b0s0", "b0s1"],
         note="Add the first two"),
   3: bm([strip(["2.5", "0.375", "14"], [2.5, 0.375, 14], ["a", "b", "c"], "16.875 kg")],
         note="The total weight is 16.875 kg")})
A("G4A_DECIMALS_014",
  compare(10, 3.607, 6.393, "10", "3.607", "?", "How much longer is the top bar?"),
  {0: compare(10, 3.607, 6.393, "10.000", "3.607", "?", "Write 10 as 10.000"),
   2: compare(10, 3.607, 6.393, "10.000", "3.607", "6.393", "6.393 + 3.607 = 10", ["b1s1"])})
A("G4A_DECIMALS_020",
  bm([strip(["37.50", "12.75", "4.25", "?"], [37.5, 12.75, 4.25, 45.5], ["a", "b", "c", "unknown"], "Rs. 100")],
     note="Notebook, pen, eraser (in rupees), and the change"),
  {0: bm([strip(["37.50", "12.75", "4.25", "?"], [37.5, 12.75, 4.25, 45.5], ["a", "b", "c", "unknown"], "Rs. 100")],
         hl=["b0s1", "b0s2"], note="Add the pen and the eraser"),
   1: bm([strip(["37.50", "12.75", "4.25", "?"], [37.5, 12.75, 4.25, 45.5], ["a", "b", "c", "unknown"], "Rs. 100")],
         hl=["b0s0", "b0s1", "b0s2"], note="Add the notebook to get the total bill"),
   3: bm([strip(["37.50", "12.75", "4.25", "45.50"], [37.5, 12.75, 4.25, 45.5], ["a", "b", "c", "b"], "Rs. 100")],
         hl=["b0s3"], note="Tara gets Rs. 45.50 as change")})
A("G4A_DECIMALS_022",
  bm([bar([seg("?", 1, "unknown")] + [seg(None, 1, "a")] * 3, brace="Rs. 342")], note="Four equal shares"),
  {2: bm([bar([seg("Rs. 85.50", 1, "b")] * 4, brace="Rs. 342")], note="Each friend pays 85 rupees and 50 paise")})
A("G4A_DECIMALS_024",
  bm([strip(["6 shirts", "?"], [13.5, 6.5], ["a", "unknown"], "20 m")], note="Each shirt uses 2.25 m of cloth"),
  {0: bm([strip(["6 shirts", "?"], [13.5, 6.5], ["a", "unknown"], "20 m")], hl=["b0s0"],
         note="Find the cloth used for 6 shirts: 6 lots of 2.25 m"),
   2: bm([strip(["6 shirts", "6.5 m"], [13.5, 6.5], ["a", "b"], "20 m")], hl=["b0s1"], note="6.5 m of cloth is left")})
A("G4A_DECIMALS_027",
  bm([bar([seg("?", 1, "unknown")] + [seg(None, 1, "a")] * 7, brace="3 litres")], note="8 equal glasses"),
  {2: bm([bar([seg("0.375", 1, "b")] + [seg(None, 1, "a")] * 7, brace="3 litres")], hl=["b0s0"],
         note="Each glass has 0.375 litre of juice")})
A("G4A_DECIMALS_035",
  bm([strip(["3.45", "2.8", "?"], [3.45, 2.8, 3.75], ["a", "b", "unknown"], "10")], note="Three numbers that add up to 10"),
  {0: bm([strip(["3.45", "2.8", "?"], [3.45, 2.8, 3.75], ["a", "b", "unknown"], "10")], hl=["b0s0", "b0s1"],
         note="Add the two numbers you know"),
   2: bm([strip(["3.45", "2.8", "3.75"], [3.45, 2.8, 3.75], ["a", "b", "c"], "10")], hl=["b0s1"],
         note="The smallest of the three is 2.8"),
   3: bm([strip(["3.45", "2.8", "3.75"], [3.45, 2.8, 3.75], ["a", "b", "c"], "10")], hl=["b0s1", "b0s2"],
         note="The third number is 0.95 greater than the smallest")})
_full = [seg("?", 1, "unknown"), seg("half the oil", 2, "a"), seg("half the oil", 2, "a")]
A("G4A_DECIMALS_036",
  bm([bar(_full, label="Full", brace="2.35 kg"), bar(_full[:2], label="Half used", brace="1.3 kg")],
     note="The empty bottle weighs the same both times"),
  {0: bm([bar(_full, label="Full", brace="2.35 kg"), bar(_full[:2], label="Half used", brace="1.3 kg")],
         hl=["b0s2"], note="The weight that went missing is half of the oil"),
   1: bm([bar(_full, label="Full", brace="2.35 kg"), bar(_full[:2], label="Half used", brace="1.3 kg")],
         hl=["b0s1", "b0s2"], note="All the oil weighs twice as much"),
   3: bm([bar([seg("0.25 kg", 1, "c")] + _full[1:], label="Full", brace="2.35 kg"),
          bar([seg("0.25 kg", 1, "c")] + _full[1:2], label="Half used", brace="1.3 kg")],
         hl=["b0s0"], note="The empty bottle weighs 0.25 kg")})
_fair = ["₹12.50", "toy", "₹5", "₹18.75"]
_fair_v = [12.5, 23.75, 5, 18.75]
_fair_t = ["a", "b", "c", "a"]
A("G4A_DECIMALS_045",
  bm([strip(_fair, _fair_v, _fair_t, "?")], note="Snack, toy, ride, and the money he came home with"),
  {0: bm([strip(_fair, _fair_v, _fair_t, "?")], hl=["b0s2", "b0s3"], note="Undo the ride: add back ₹5"),
   1: bm([strip(_fair, _fair_v, _fair_t, "?")], hl=["b0s1"], note="The toy cost half, so it matches the two pieces after it"),
   2: bm([strip(_fair, _fair_v, _fair_t, "?")], hl=["b0s0"], note="Undo the snack: add back ₹12.50"),
   3: bm([strip(_fair, _fair_v, _fair_t, "₹60")], note="Kabir took ₹60 to the fair")})
A("G4A_DECIMALS_049",
  bm([bar([seg("?", 2, "unknown"), seg("₹7.50", 1.5, "b")], label="Notebook"), bar([seg("?", 2, "unknown")], label="Pen")],
     note="2 notebooks and 3 pens cost ₹65 in all"),
  {3: bm([bar([seg("₹10", 2, "a"), seg("₹7.50", 1.5, "b")], label="Notebook"), bar([seg("₹10", 2, "a")], label="Pen")],
         hl=["b0"], note="One notebook costs ₹7.50 more than a pen: ₹17.50")})
A("G4A_DECIMALS_052",
  bm([strip(["tea", "samosas", "?"], [50, 22.5, 27.5], ["a", "b", "unknown"], "₹100")],
     note="Tea at ₹12.50 a cup, samosas at ₹7.50 each, and the change"),
  {0: bm([strip(["tea", "samosas", "?"], [50, 22.5, 27.5], ["a", "b", "unknown"], "₹100")], hl=["b0s0"],
         note="Four cups of tea"),
   1: bm([strip(["tea", "3 samosas", "?"], [50, 22.5, 27.5], ["a", "b", "unknown"], "₹100")], hl=["b0s1"],
         note="All except one eat a samosa: 3 samosas"),
   3: bm([strip(["tea", "3 samosas", "₹27.50"], [50, 22.5, 27.5], ["a", "b", "c"], "₹100")], hl=["b0s2"],
         note="The change is ₹27.50")})
A("PYQ_2017_Q07",
  bm([strip(["Rs. 39.46", "?"], [39.46, 10.54], ["a", "unknown"], "Rs. 50")], note="Groceries, and the change"),
  {1: line(39, 50, 1, points=[(39.46, "39.46"), (40, "40")], hops=[(39.46, 40, "0.54")], ticks="none",
           note="Count up from 39.46 to 40"),
   2: line(39, 50, 1, points=[(39.46, "39.46"), (40, "40"), (50, "50")], hops=[(39.46, 40, "0.54"), (40, 50, "10")],
           ticks="none", note="Then count up from 40 to 50"),
   3: bm([strip(["Rs. 39.46", "Rs. 10.54"], [39.46, 10.54], ["a", "b"], "Rs. 50")], hl=["b0s1"],
         note="Add the two jumps: Rs. 10.54")})
A("EXT_G4_FP_2020_032",
  compare(1.3, 0.13, 1.17, "1.3", "0.13", "?", "How much longer is the top bar?"),
  {1: compare(1.3, 0.13, 1.17, "1.30", "0.13", "?", "Write 1.3 as 1.30 so the places line up"),
   3: compare(1.3, 0.13, 1.17, "1.30", "0.13", "1.17", "1.3 is greater than 0.13 by 1.17", ["b1s1"])})
A("PYQ_2016_Q02",
  compare(9.07, 7.9, 1.17, "9.07", "7.9", "?", "How much longer is the top bar?"),
  {0: compare(9.07, 7.9, 1.17, "9.07", "7.90", "?", "Write 7.9 as 7.90"),
   2: compare(9.07, 7.9, 1.17, "9.07", "7.90", "1.17", "7.90 + 1.17 = 9.07", ["b1s1"])})
A("PYQ_2017_Q17",
  compare(9.7, 0.97, 8.73, "9.7", "0.97", "?", "How far apart are the two numbers?"),
  {1: compare(9.7, 0.97, 8.73, "9.70", "0.97", "?", "Write 9.7 as 9.70 so the points line up"),
   2: compare(9.7, 0.97, 8.73, "9.70", "0.97", "8.73", "0.97 + 8.73 = 9.70", ["b1s1"])})
A("EXT_G4_FP_2020_012",
  bm([bar([seg("45 min", 9, "a"), seg(None, 3, "unknown")], brace="1 hour = 60 min")], note="What part of an hour is 45 min?"),
  {0: bm([bar([seg("45 min", 9, "a"), seg(None, 3, "unknown")], brace="1 hour = 60 min")], hl=["b0s0"],
         note="45 minutes is 45 out of 60 of an hour"),
   1: bm([bar([seg(None, 3, "a")] * 3 + [seg(None, 3, "unknown")], brace="1 hour")],
         note="Three quarters of an hour is 0.75 of an hour")})
A("Q_CH12_002",
  bm([bar([seg("40 rupees", 4, "a")], label="1 dollar"), bar([seg("100 rupees", 10, "b")], label="?")],
     note="How many 40s fit into 100?"),
  {1: bm([bar([seg("40 rupees", 4, "a")], label="1 dollar"),
          bar([seg("40", 4, "a"), seg("40", 4, "a"), seg("20", 2, "unknown")], label="?")],
         note="Two dollars use 80 rupees, and 20 rupees are left"),
   2: bm([bar([seg("40 rupees", 4, "a")], label="1 dollar"),
          bar([seg("40", 4, "a"), seg("40", 4, "a"), seg("20", 2, "unknown")], label="?")],
         hl=["b1s2"], note="20 rupees is half of 40 rupees: half a dollar"),
   3: bm([bar([seg("40 rupees", 4, "a")], label="1 dollar"),
          bar([seg("40", 4, "a"), seg("40", 4, "a"), seg("20", 2, "b")], label="2.5")],
         note="100 rupees give 2.5 dollars")})
A("Q_CH11_022",
  padded([["Apples", "2.5 kg", "₹120 per kg"], ["Oranges", "1.25 kg", "₹80 per kg"]], ["Fruit", "Weight", "Price"]),
  {0: padded([["Apples", "2.5 kg", "₹300"], ["Oranges", "1.25 kg", "?"]], ["Fruit", "Weight", "Cost"],
             "2 kg cost ₹240 and half a kg costs ₹60", ["r0"]),
   1: padded([["Apples", "2.5 kg", "₹300"], ["Oranges", "1.25 kg", "₹100"]], ["Fruit", "Weight", "Cost"],
             "1 kg costs ₹80 and a quarter of a kg costs ₹20", ["r1"]),
   2: padded([["Apples", "2.5 kg", "₹300"], ["Oranges", "1.25 kg", "₹100"]], ["Fruit", "Weight", "Cost"],
             "Riya spent ₹400 in total")})
_days = [["Mon", "Rs. 2.50"], ["Tue", "Rs. 3.00"], ["Wed", "Rs. 3.50"], ["Thu", "Rs. 4.00"], ["Fri", "Rs. 4.50"], ["Sat", "Rs. 5.00"]]
A("G4A_DECIMALS_039", None, {
    0: padded(_days, ["Day", "Saved"]),
    1: padded(_days, ["Day", "Saved"], "First + last, second + fifth, third + fourth: each Rs. 7.50"),
    2: padded(_days, ["Day", "Saved"], "Three pairs of Rs. 7.50 make Rs. 22.50")})

# Fractions and decimals
A("Q_CH11_011",
  fb([(4, 3, "3/4")], note="3/4 as a decimal = ?"),
  {3: fb([(4, 3, "3/4 = 0.75")])})
A("Q_CH11_012", None, {2: fb([(8, 1, "1/8")], note="0.125 is 1/8, and it cannot be made simpler")})
A("G4A_DECIMALS_008",
  fb([(20, 7, "7/20")], note="7/20 as a decimal = ?"),
  {0: fb([(20, 7, "7/20")], note="Each of the 20 parts is 5 hundredths"),
   1: fb([(20, 7, "7/20 = 0.35")], note="35 hundredths is written 0.35")})
A("G4A_DECIMALS_019", None, {2: fb([(4, 4, "1"), (4, 3, "3/4")], note="1.75 is 1 3/4")})
A("G4A_DECIMALS_040", None, {
    0: fb([(8, 1, "1 m")], note="0.125 m is one eighth of a metre: 8 pieces in 1 m"),
    1: fb([(8, 8, "1 m"), (8, 8, "1 m")], note="2 m gives 16 pieces"),
    2: fb([(8, 8, "1 m"), (8, 8, "1 m"), (8, 4, "half a metre")], note="The extra half metre gives 4 more pieces"),
    3: fb([(8, 8, "1 m"), (8, 8, "1 m"), (8, 4, "half a metre")], note="16 + 4 = 20 pieces")})
A("PYQ_2019_Q01",
  fb([(8, 1, "1/8")], note="9 wholes and this 1/8: write it as a decimal"),
  {1: fb([(8, 1, "1/8")], note="8 × 125 = 1000, so 1/8 is 125 thousandths"),
   2: fb([(8, 1, "1/8 = 0.125")]),
   3: fb([(8, 1, "1/8 = 0.125")], note="9 1/8 as a decimal is 9.125")})
_28 = [(r, c) for r in range(10) for c in range(10)][:28]
A("EXT_G4_WS2_CH11_001",
  grid(10, 10, _28, "0.28 of the big square is shaded"),
  {0: grid(10, 10, _28, "0.28 means 28 hundredths: 28 of the 100 small squares"),
   3: grid(10, 10, _28, "0.28 = 7/25")})

P.write()
if "--review" in sys.argv:
    P.review()
if "--redo" in sys.argv:
    # Round 3: the change-from-a-payment family.
    P.review([q["id"] for q in P.qs if CHANGE.match(q["questionText"])])
if "--redo2" in sys.argv:
    P.review(["EXT_G4_FP_2022_021", "EXT_G4_FP_2023_016", "EXT_G4_FP_2024_016", "G4A_DECIMALS_016", "Q_CH11_001",
              "Q_CH11_002", "Q_CH11_013", "Q_CH11_020", "Q_CH11_024"])
