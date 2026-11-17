"""Simple interest: two banks side by side, and finding a shared rate from one story to use in another."""
from imported_09_lib import ANS, B, FORMULA, GIVEN, M, W, choose, hundreds, lesson, rate_beats

LESSONS = {}

FORMULA_SAY = "principal times rate times time, divided by 100"


# ── Two banks, both fully known ──────────────────────────────────────────────

def two_banks(intro, givens, pre, a, b, t, mode, trap, summary, extra_check=None):
    (an, ap, ar), (bn, bp, br) = a, b
    ah, bh = hundreds(ap), hundreds(bp)
    ay, by = ah * ar, bh * br
    ai, bi = ay * t, by * t
    beats = [B(intro, *[GIVEN(i, text) for i, text in givens])] + list(pre)
    beats.append(B("%s first. %d is %d hundreds, each earning %d rupees a year. %d times %d is %d a year, and for %d years that is %d."
                   % (an, ap, ah, ar, ah, ar, ay, t, ai),
                   W("a1", "%d × %d = %d" % (ah, ar, ay)), W("a2", "%d × %d = %d" % (ay, t, ai))))
    beats.append(B("Now %s, with %d rupees at %d percent. How much interest does it pay in 1 year?" % (bn, bp, br),
                   W("b0", "%d ÷ 100 = %d" % (bp, bh)),
                   ask=choose(["₹%d" % by, "₹%d" % (bh * ar), "₹%d" % (bp * br)], 0,
                              "%d is %d hundreds, and in %s each hundred earns %d rupees a year. So we want %d times %d." % (bp, bh, bn, br, bh, br))))
    beats.append(B("%d times %d is %d a year, and for %d years that is %d." % (bh, br, by, t, bi),
                   W("b1", "%d × %d = %d" % (bh, br, by)), W("b2", "%d × %d = %d" % (by, t, bi))))
    if mode == "sum":
        beats.append(B("Now add the two banks. %d plus %d is %d rupees of interest altogether." % (ai, bi, ai + bi),
                       ANS("a", "%d + %d = %d" % (ai, bi, ai + bi)), M("a", str(ai + bi), "circle")))
    else:
        beats.append(B("%s pays more. %d minus %d is %d rupees more." % (an, ai, bi, ai - bi),
                       ANS("a", "%d − %d = %d" % (ai, bi, ai - bi)), M("a", str(ai - bi), "circle")))
    beats.append(extra_check or B(
        "Check with the formula: %s. %s gives %d and %s gives %d, the same as before." % (FORMULA_SAY, an, ai, bn, bi),
        W("f", FORMULA, label=True), W("c1", "%d × %d × %d ÷ 100 = %d" % (ap, ar, t, ai)), W("c2", "%d × %d × %d ÷ 100 = %d" % (bp, br, t, bi))))
    beats += [B(trap), B(summary)]
    return lesson(beats)


def age_time(name, start, end):
    t = end - start
    return [
        B("The money goes in when %s is %d, and we look again when she turns %d. For how long does it earn interest?" % (name, start, end),
          ask=choose(["%d years" % t, "%d years" % end, "%d years" % start], 0,
                     "The ages are not the time. Count the years in between: from %d to %d is %d take away %d." % (start, end, end, start))),
        B("%d minus %d is %d. The money earns interest for %d years." % (end, start, t, t),
          W("t", "%d − %d = %d" % (end, start, t))),
    ]


LESSONS["05ab6300"] = two_banks(
    "Ravi has 3000 rupees. He puts 1800 in Bank A at 5 percent a year, and the remaining amount in Bank B at 10 percent a year. After 2 years, how much interest has he earned altogether?",
    [("g", "Bank A: ₹1800 at 5%. Bank B: the rest of ₹3000 at 10%"), ("g2", "T = 2 years. Total interest = ?")],
    [B("First, how much went into Bank B? 3000 minus 1800 is 1200. So Bank B holds 1200 rupees.",
       M("g", "the rest of ₹3000"), W("s", "3000 − 1800 = 1200"))],
    ("Bank A", 1800, 5), ("Bank B", 1200, 10), 2, "sum",
    "Do not use the whole 3000 for Bank B. Only what remained after Bank A went there.",
    "Two banks means two separate pieces of working: 1 year's interest, times the years, for each. Then add.")

LESSONS["1ffea6d1"] = two_banks(
    "Rahul has 5000 rupees. He puts 3000 in Bank A at 4 percent a year and 2000 in Bank B at 7 percent a year. After 2 years, what is the total interest from both banks?",
    [("g", "Bank A: ₹3000 at 4%. Bank B: ₹2000 at 7%"), ("g2", "T = 2 years. Total interest = ?")],
    [],
    ("Bank A", 3000, 4), ("Bank B", 2000, 7), 2, "sum",
    "Each bank has its own rate, so we cannot add the deposits or the rates first. Work each bank on its own, then add the interest.",
    "For each bank: 1 year's interest, times the years. Then add the two.")

LESSONS["4bded903"] = two_banks(
    "Meena has 12000 rupees. She puts half in Bank A at 8 percent a year and the other half in Bank B at 5 percent a year. After 4 years, how much interest has she earned from both banks together?",
    [("g", "₹12000: half in Bank A at 8%, half in Bank B at 5%"), ("g2", "T = 4 years. Total interest = ?")],
    [B("Half of 12000 is 6000. So each bank holds 6000 rupees.",
       M("g", "half"), W("s", "12000 ÷ 2 = 6000"))],
    ("Bank A", 6000, 8), ("Bank B", 6000, 5), 4, "sum",
    "Halve the money first. Using the full 12000 in both banks would count every rupee twice.",
    "Split the money, work out each bank on its own, then add the interest.")

LESSONS["51bc47d4"] = two_banks(
    "Meena gets 12000 rupees on her 10th birthday. Half goes into Bank A at 8 percent a year and half into Bank B at 5 percent a year. When she turns 14, how much more interest has Bank A paid than Bank B?",
    [("g", "₹12000: half in Bank A at 8%, half in Bank B at 5%"), ("g2", "Age 10 to age 14. Bank A − Bank B = ?")],
    [B("Half of 12000 is 6000. So each bank holds 6000 rupees.",
       M("g", "half"), W("s", "12000 ÷ 2 = 6000"))] + age_time("Meena", 10, 14),
    ("Bank A", 6000, 8), ("Bank B", 6000, 5), 4, "diff",
    "Two traps here. The ages 10 and 14 are not the time: the time is the 4 years between them. And the question wants the difference, not the total.",
    "Same money in both banks, so only the rates differ. Work out each, then subtract.",
    extra_check=B("A neat check: the rates differ by 3 percent. 60 hundreds times 3 is 180 rupees a year, and 4 years of that is 720.",
                  W("c1", "8 − 5 = 3"), W("c2", "60 × 3 = 180"), W("c3", "180 × 4 = 720")))

LESSONS["88a2f579"] = two_banks(
    "Priya gets 12000 rupees on her 10th birthday. Half goes into Bank A at 6 percent a year and half into Bank B at 8 percent a year. When she turns 15, how much interest is there altogether for her bicycle?",
    [("g", "₹12000: half in Bank A at 6%, half in Bank B at 8%"), ("g2", "Age 10 to age 15. Total interest = ?")],
    [B("Half of 12000 is 6000. So each bank holds 6000 rupees.",
       M("g", "half"), W("s", "12000 ÷ 2 = 6000"))] + age_time("Priya", 10, 15),
    ("Bank A", 6000, 6), ("Bank B", 6000, 8), 5, "sum",
    "Watch the ages. 10 and 15 are birthdays, not years in the bank. The time is the 5 years between them.",
    "Find the time, split the money, work out each bank on its own, then add.")


# ── Find the rate from Ravi, use it for Meena ────────────────────────────────

_r, _rate = rate_beats(4500, 3, 5850)
LESSONS["347217a1"] = lesson(
    B("Two people, one bank, one rate. Ravi put in 4500 rupees and got back 5850 after 3 years. Meena puts in 6000 at the same rate for 4 years. We want Meena's interest.",
      GIVEN("g", "Ravi: ₹4500 becomes ₹5850 in 3 years"), GIVEN("g2", "Meena: ₹6000 for 4 years, same rate")),
    B("We are not told the rate. Whose numbers can we use to find it?",
      ask=choose(["Ravi's", "Meena's", "nobody's"], 0,
                 "For Ravi we know the deposit, the time and the total he got back. That is enough to work out the rate. For Meena, the interest is the very thing we are looking for.")),
    _r,
    B("Now Meena, at 10 percent. Her 6000 rupees is 60 hundreds. How much interest does she earn in 1 year?",
      M("g2", "₹6000"),
      ask=choose(["₹600", "₹60", "₹6000"], 0,
                 "Each hundred earns 10 rupees a year, and she has 60 hundreds. So it is 60 lots of 10.")),
    B("60 times 10 is 600 rupees a year. Over 4 years, 600 times 4 is 2400. Meena earns 2400 rupees of interest.",
      W("m1", "60 × 10 = 600"), ANS("a", "600 × 4 = 2400"), M("a", "2400", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 6000 times 10 times 4, divided by 100, is 2400.",
      W("f", FORMULA, label=True), W("c", "6000 × 10 × 4 ÷ 100 = 2400")),
    B("The trap is to use Ravi's 3 years for Meena, or to stop at 1 year's interest. Each person has their own deposit and their own time. Only the rate is shared."),
    B("Find the shared rate from the person you know everything about. Then use it for the other person."),
)

_r, _rate = rate_beats(4500, 3, 5850)
LESSONS["96af4dc8"] = lesson(
    B("Ravi put 4500 rupees in a bank and received 5850 in total after 3 years. Meena puts 6000 in the same bank, at the same rate, for 2 years. How much interest will Meena earn?",
      GIVEN("g", "Ravi: ₹4500 becomes ₹5850 in 3 years"), GIVEN("g2", "Meena: ₹6000 for 2 years, same rate")),
    B("The rate is hidden. What must we work out first?",
      ask=choose(["Ravi's interest, to get the rate", "Meena's total amount", "Ravi's interest for 2 years"], 0,
                 "The only link between Ravi and Meena is the bank's rate. Ravi's numbers are complete, so we use them to uncover it.")),
    _r,
    B("Now Meena. Her 6000 rupees is 60 hundreds, and each hundred earns 10 rupees a year. 60 times 10 is 600 rupees a year.",
      M("g2", "₹6000"), W("m0", "6000 ÷ 100 = 60"), W("m1", "60 × 10 = 600")),
    B("Meena leaves her money for 2 years. Which sum gives her interest?",
      M("g2", "2 years"),
      ask=choose(["600 × 2", "600 × 3", "600 + 2"], 0,
                 "Meena's own time is 2 years. The 3 years belonged to Ravi. So she earns 2 lots of 600.")),
    B("600 times 2 is 1200. Meena earns 1200 rupees of interest.",
      ANS("a", "600 × 2 = 1200"), M("a", "1200", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 6000 times 10 times 2, divided by 100, is 1200.",
      W("f", FORMULA, label=True), W("c", "6000 × 10 × 2 ÷ 100 = 1200")),
    B("Look out for 1350 among the choices. That is Ravi's interest, not Meena's."),
    B("When two people share a rate, find it from the one whose story is complete, then carry it across."),
)

# ── Father's loan gives the rate; mother's deposit needs the time ────────────
_r, _rate = rate_beats(24000, 3, 31200, first="The extra he paid back is the interest.")
LESSONS["0f4c01ab"] = lesson(
    B("Meera's father borrowed 24000 rupees and paid back 31200 after 3 years. Her mother deposits 15000 at the same rate. After how many years will she have earned 4500 in interest?",
      GIVEN("g", "Father: ₹24000 loan, pays back ₹31200 after 3 years"), GIVEN("g2", "Mother: ₹15000, same rate, interest ₹4500, T = ?")),
    B("What must we find first, before we can help the mother?",
      ask=choose(["the rate, from the father's loan", "the mother's total amount", "the father's time"], 0,
                 "The mother's bank uses the same rate as the father's loan, but nobody tells us that rate. The father's numbers let us work it out.")),
    _r,
    B("Now the mother. 15000 is 150 hundreds, each earning 10 rupees a year. 150 times 10 is 1500 rupees a year.",
      M("g2", "₹15000"), W("m0", "15000 ÷ 100 = 150"), W("m1", "150 × 10 = 1500")),
    B("She wants 4500 in interest, and each year brings 1500. How do we find the number of years?",
      M("g2", "interest ₹4500"),
      ask=choose(["4500 ÷ 1500", "4500 − 1500", "4500 × 1500"], 0,
                 "Every year adds the same 1500 rupees. So we ask how many lots of 1500 fit into 4500. That is a division.")),
    B("4500 divided by 1500 is 3, because 3 times 1500 is 4500. She needs 3 years.",
      W("m2", "4500 ÷ 1500 = 3"), ANS("a", "T = 3 years", True), M("a", "3 years", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 15000 times 10 times 3, divided by 100, is 4500.",
      W("f", FORMULA, label=True), W("c", "15000 × 10 × 3 ÷ 100 = 4500")),
    B("It is only chance that both stories take 3 years. The link between them is the rate, 10 percent, and nothing else."),
    B("A loan and a deposit work the same way. Get the rate from the story that is complete, then find 1 year's interest and count the years."),
)

# ── Ravi's birthdays give the rate; Priya's deposit needs the time ───────────
_r, _rate = rate_beats(12000, 2, 13440)
LESSONS["300ad9ba"] = lesson(
    B("Ravi's grandfather put 12000 rupees in a bank on Ravi's 8th birthday. By his 10th birthday it had grown to 13440. Priya gets the same rate: she deposits 8500 and earns 5100 in interest. For how many years?",
      GIVEN("g", "Ravi: ₹12000 at age 8, ₹13440 at age 10"), GIVEN("g2", "Priya: ₹8500, same rate, interest ₹5100, T = ?")),
    B("How long was Ravi's money in the bank?",
      ask=choose(["2 years", "8 years", "10 years"], 0,
                 "The money went in on his 8th birthday and was counted on his 10th. The time is the gap between those two birthdays.")),
    B("From his 8th birthday to his 10th is 2 years.",
      W("t", "10 − 8 = 2"), M("g", "age 8"), M("g", "age 10")),
    _r,
    B("Now Priya. 8500 is 85 hundreds, each earning 6 rupees a year. 85 times 6 is 510 rupees a year.",
      M("g2", "₹8500"), W("p0", "8500 ÷ 100 = 85"), W("p1", "85 × 6 = 510")),
    B("She earned 5100 altogether, at 510 a year. How many years is that?",
      M("g2", "interest ₹5100"),
      ask=choose(["10 years", "5 years", "100 years"], 0,
                 "How many lots of 510 make 5100? Look at the two numbers: 5100 is 510 with one more zero on the end.")),
    B("5100 divided by 510 is 10. Priya kept her money in the bank for 10 years.",
      W("p2", "5100 ÷ 510 = 10"), ANS("a", "T = 10 years", True), M("a", "10 years", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 8500 times 6 times 10, divided by 100, is 5100.",
      W("f", FORMULA, label=True), W("c", "8500 × 6 × 10 ÷ 100 = 5100")),
    B("The ages are a trap for the careless. 8 and 10 are birthdays, not years in the bank."),
    B("Find the time, then the rate, from the story that is complete. Then use the rate in the other story."),
)

# ── Father's loan gives the rate; mother's interest gives her deposit ────────
_r, _rate = rate_beats(24000, 3, 31200, first="The extra he paid back is the interest.")
LESSONS["9457685e"] = lesson(
    B("Priya's father borrowed 24000 rupees and paid back 31200 after 3 years. Her mother deposits some money at the same rate, and after 5 years her interest is 6000. How much did the mother deposit?",
      GIVEN("g", "Father: ₹24000 loan, pays back ₹31200 after 3 years"), GIVEN("g2", "Mother: same rate, 5 years, interest ₹6000, P = ?")),
    B("The mother's deposit depends on the rate. Where can we get the rate from?",
      ask=choose(["the father's loan", "the mother's interest", "it cannot be found"], 0,
                 "For the father we know the loan, the time and what he paid back. That is a complete story, so it can give us the rate.")),
    _r,
    B("Now the mother. Her 6000 of interest built up over 5 years. 6000 divided by 5 is 1200 rupees a year.",
      M("g2", "5 years"), W("m1", "6000 ÷ 5 = 1200")),
    B("At 10 percent, every 100 rupees she deposited earns 10 rupees a year. She earns 1200 a year. How many hundreds did she deposit?",
      ask=choose(["1200 ÷ 10", "1200 × 10", "1200 − 10"], 0,
                 "Each hundred brings in 10 rupees. So count how many lots of 10 there are in 1200: that is how many hundreds she has.")),
    B("1200 divided by 10 is 120. So she deposited 120 hundreds, which is 12000 rupees.",
      W("m2", "1200 ÷ 10 = 120"), ANS("a", "120 × 100 = 12000"), M("a", "12000", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 12000 times 10 times 5, divided by 100, is 6000.",
      W("f", FORMULA, label=True), W("c", "12000 × 10 × 5 ÷ 100 = 6000")),
    B("Notice the deposit is much bigger than the interest it earns in a year. At 10 percent, it is 10 times as big. That is a quick way to sense-check your answer."),
    B("Rate first, from the complete story. Then 1 year's interest, and from that, work back to the deposit."),
)

# ── Priya at 6%, Rohan at 9%: when is the gap ₹1500? ─────────────────────────
LESSONS["5a0113bc"] = lesson(
    B("Priya and Rohan each deposit 10000 rupees. Priya's bank pays 6 percent a year and Rohan's pays 9 percent. After some years, Rohan's interest is 1500 rupees more than Priya's. How many years?",
      GIVEN("g", "Priya: ₹10000 at 6%. Rohan: ₹10000 at 9%"), GIVEN("g2", "Difference in interest = ₹1500, T = ?")),
    B("Start with 1 year. 10000 is 100 hundreds. Priya earns 6 rupees on each, which is 600 a year. Rohan earns 9 on each, which is 900 a year.",
      W("h", "10000 ÷ 100 = 100"), W("p", "100 × 6 = 600"), W("r", "100 × 9 = 900")),
    B("After 1 year, how far ahead is Rohan?",
      ask=choose(["₹300", "₹1500", "₹900"], 0,
                 "Compare one year for each. Rohan gets 900 and Priya gets 600, so the gap is 900 take away 600.")),
    B("900 minus 600 is 300. And every year, the gap grows by another 300.",
      W("d", "900 − 600 = 300"), M("d", "300", "box")),
    B("The gap has reached 1500. How do we find how many years that took?",
      M("g2", "₹1500"),
      ask=choose(["1500 ÷ 300", "1500 − 300", "1500 ÷ 900"], 0,
                 "The gap grows 300 at a time, once a year. So count how many lots of 300 make 1500.")),
    B("1500 divided by 300 is 5, because 5 times 300 is 1500. They kept their money in the banks for 5 years.",
      W("t", "1500 ÷ 300 = 5"), ANS("a", "T = 5 years", True), M("a", "5 years", "circle")),
    B("Check. After 5 years Rohan has earned 5 times 900, which is 4500. Priya has 5 times 600, which is 3000. The difference is 1500.",
      W("c1", "5 × 900 = 4500"), W("c2", "5 × 600 = 3000"), W("c3", "4500 − 3000 = 1500")),
    B("A neat shortcut: the rates differ by 3 percent, and 3 percent of 10000 is that same 300 a year.",
      W("s1", "9 − 6 = 3"), W("s2", "100 × 3 = 300")),
    B("When two things grow steadily, look at how much the gap between them grows each year."),
)
