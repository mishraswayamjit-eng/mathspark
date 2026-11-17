"""Simple-interest lessons, second half."""
from imported_10_lib import ANS, ASK, B, GIVEN, L, M, N, RING, W, add, f, hundreds, pick


# ── Two banks, everything withdrawn: deposits and interests all come back ────

def two_banks(key, who, pa, ra, pb, rb, years, purpose):
    ha, hb = pa // 100, pb // 100
    ya, yb = ha * ra, hb * rb
    ia, ib = ya * years, yb * years
    dep, intr = pa + pb, ia + ib
    add(key,
        B("%s puts %d rupees in Bank A at %d per cent and %d rupees in Bank B at %d per cent, %s. After %d years all the money is taken out. How much is that?"
          % (who, pa, ra, pb, rb, purpose, years),
          GIVEN("q", "Bank A: ₹%s at %d%%.  Bank B: ₹%s at %d%%.  %d years." % (f(pa), ra, f(pb), rb, years))),
        B("Take Bank A first. %d is %d hundreds, and each hundred earns %d rupees a year. %d times %d is %d a year."
          % (pa, ha, ra, ha, ra, ya),
          W("a1", "%s ÷ 100 = %s" % (f(pa), f(ha))), W("a2", "%s × %s = %s" % (f(ha), f(ra), f(ya))),
          N("a2", "= " + f(ya), "Bank A, 1 year")),
        B("The money stays for %d years, so Bank A pays %d times %d, which is %d." % (years, ya, years, ia),
          W("a3", "%s × %s = %s" % (f(ya), years, f(ia))), N("a3", "= " + f(ia), "Bank A interest")),
        B("Bank B the same way. %d is %d hundreds, each earning %d rupees. %d times %d is %d a year, so %d in %d years."
          % (pb, hb, rb, hb, rb, yb, ib, years),
          W("b1", "%s ÷ 100 = %s" % (f(pb), f(hb))), W("b2", "%s × %s = %s" % (f(hb), f(rb), f(yb))),
          W("b3", "%s × %s = %s" % (f(yb), years, f(ib))), N("b3", "= " + f(ib), "Bank B interest")),
        ASK(key, "a1", "Now all the money is withdrawn from both banks. What comes back?",
            "both deposits and both interests", ["only the two interests", "only the two deposits"],
            "A bank hands back what was put in, with the interest on top. So there are 4 things to add: 2 deposits and 2 lots of interest."),
        B("The deposits: %d plus %d is %d. The interest: %d plus %d is %d." % (pa, pb, dep, ia, ib, intr),
          W("d", "%s + %s = %s" % (f(pa), f(pb), f(dep))), N("d", "= " + f(dep), "deposits"),
          W("i", "%s + %s = %s" % (f(ia), f(ib), f(intr))), N("i", "= " + f(intr), "interest")),
        B("Altogether, %d plus %d is %d rupees." % (dep, intr, dep + intr),
          ANS("ans", "%s + %s = %s" % (f(dep), f(intr), f(dep + intr))), RING("ans", f(dep + intr))),
        B("Check it bank by bank. Bank A gives back %d, Bank B gives back %d, and together that is %d again."
          % (pa + ia, pb + ib, dep + intr),
          W("c1", "%s + %s = %s" % (f(pa), f(ia), f(pa + ia))), W("c2", "%s + %s = %s" % (f(pb), f(ib), f(pb + ib))),
          W("c3", "%s + %s = %s" % (f(pa + ia), f(pb + ib), f(dep + intr)))),
        B(pick(key, "end", [
            "So treat each bank on its own: 1 year's interest, times the years. Then remember that the deposits come back too.",
            "So work each bank out separately, a year at a time. And when everything is withdrawn, the deposits are part of the total.",
        ])),
        )


two_banks("c8e400d8", "Ankit's mother", 2000, 10, 3000, 6, 2, "saving for his school trip")
two_banks("ef719755", "Ankit's father", 5000, 8, 7000, 5, 2, "for the school fees")

# ── Ravi and Meena: same bank, same rate ─────────────────────────────────────

Q = "d2fb6b24"
add(Q,
    B("Ravi's 4500 rupees becomes 5310 in 3 years. Meena puts 6000 in the same bank, at the same rate, for 4 years. We want Meena's interest.",
      GIVEN("q", "Ravi: ₹4,500 becomes ₹5,310 in 3 years."), L("q2", "Meena: ₹6,000 for 4 years, same rate. Interest = ?")),
    B("We do not know the rate yet, but Ravi's money can tell us. His interest is 5310 minus 4500, which is 810.",
      W("i", "5,310 − 4,500 = 810"), N("i", "= 810", "Ravi, 3 years")),
    B("That is for 3 years. So in 1 year Ravi earns 810 divided by 3, which is 270.",
      W("y", "810 ÷ 3 = 270"), N("y", "= 270", "Ravi, 1 year")),
    ASK(Q, "a1", "Ravi's 4500 is 45 hundreds, and together they earn 270 a year. What does each hundred earn?",
        "270 ÷ 45", ["270 × 45", "270 ÷ 100"],
        "The 270 rupees is shared equally among the 45 hundreds. So divide 270 by 45.",
        W("h", "4,500 ÷ 100 = 45")),
    B("270 divided by 45 is 6. Every hundred earns 6 rupees a year, so the rate is 6 per cent.",
      W("r", "270 ÷ 45 = 6"), N("r", "= 6", "rate: 6% a year")),
    B("Now Meena. Her 6000 is 60 hundreds, and each one earns 6 rupees. 60 times 6 is 360 a year.",
      W("m1", "6,000 ÷ 100 = 60"), W("m2", "60 × 6 = 360"), N("m2", "= 360", "Meena, 1 year")),
    B("Careful with the years: Meena's money stays for 4 years. The 3 years belonged to Ravi. 360 times 4 is 1440 rupees.",
      ANS("ans", "360 × 4 = 1,440"), RING("ans", "1,440")),
    B("Check the rate on Ravi. 45 hundreds, 6 rupees each, for 3 years: 45 times 6 times 3 is 810. That is his interest, so the rate is right.",
      W("c", "45 × 6 × 3 = 810")),
    B("So when two people share a rate, use the one you know to find what each hundred earns in a year. Then give that rate to the other."),
    )

# ── Ravi's two deposits: different numbers of years ──────────────────────────

Q = "e15d0d87"
add(Q,
    B("12000 rupees is deposited when Ravi turns 10. By his 13th birthday it has earned 2880. Then he adds 8000 more at the same rate. We want all the interest by the time he turns 16.",
      GIVEN("q", "₹12,000 earns ₹2,880 in 3 years."), L("q2", "Then ₹8,000 more, same rate, for 3 years"),
      L("q3", "Total interest by age 16 = ?")),
    B("Start with what the first deposit earns in 1 year. 2880 came in 3 years, and 2880 divided by 3 is 960.",
      W("y", "2,880 ÷ 3 = 960"), N("y", "= 960", "₹12,000, 1 year")),
    ASK(Q, "a1", "The 12000 went in on his 10th birthday. By the time he turns 16, for how many years has it been earning?",
        "6 years", ["3 years", "9 years"],
        "Count from his 10th birthday to his 16th. That is 6 years, and the first deposit earns interest in every one of them."),
    B("6 years at 960 a year: 960 times 6 is 5760. Careful: this already includes the 2880 from the first 3 years, so we must not add that again.",
      W("i1", "960 × 6 = 5,760"), N("i1", "= 5,760", "first deposit")),
    B("For the second deposit we need the rate. 12000 is 120 hundreds, earning 960 a year. 960 divided by 120 is 8, so the rate is 8 per cent.",
      W("h", "12,000 ÷ 100 = 120"), W("r", "960 ÷ 120 = 8"), N("r", "= 8", "rate: 8% a year")),
    B("The 8000 is 80 hundreds, each earning 8 rupees. 80 times 8 is 640 a year.",
      W("h2", "8,000 ÷ 100 = 80"), W("y2", "80 × 8 = 640"), N("y2", "= 640", "₹8,000, 1 year")),
    B("The second deposit is in the bank for only 3 years. 640 times 3 is 1920.",
      W("i2", "640 × 3 = 1,920"), N("i2", "= 1,920", "second deposit")),
    B("Now put the two together. 5760 plus 1920 is 7680 rupees.",
      ANS("ans", "5,760 + 1,920 = 7,680"), RING("ans", "7,680")),
    B("Check it by time instead. The first 3 years gave 2880. In the next 3 years both deposits earn: 960 plus 640 is 1600 a year, so 4800. And 2880 plus 4800 is 7680.",
      W("c1", "960 + 640 = 1,600"), W("c2", "1,600 × 3 = 4,800"), W("c3", "2,880 + 4,800 = 7,680")),
    B("So give every deposit its own number of years. Find 1 year's interest for each, multiply by its own years, and then add."),
    )

# ── Priya's father: how many years? ──────────────────────────────────────────

Q = "ea9dae78"
h1, h2 = hundreds(6000, 6, "a")
add(Q,
    B("6000 rupees is in a post office scheme at 6 per cent simple interest a year. So far it has earned 1800 rupees. For how many years has it been there?",
      GIVEN("q", "₹6,000 at 6% a year earns ₹1,800. Years = ?")),
    h1, h2,
    ASK(Q, "a1", "Every year adds 360 rupees, and the interest has reached 1800. How do we find the number of years?",
        "1800 ÷ 360", ["1800 − 360", "1800 ÷ 6"],
        "We are counting how many lots of 360 fit into 1800. That is a division: 1800 divided by 360."),
    B("To make the division friendlier, drop a zero from both numbers: 180 divided by 36. And 36 times 5 is 180. So the answer is 5 years.",
      W("d", "180 ÷ 36 = 5"), ANS("ans", "1,800 ÷ 360 = 5"), RING("ans", "5")),
    B("Careful with the 6 in the question. It is the rate, not the time. The number of years always has to be worked out."),
    B("Check by building it up. 5 years of 360 is 1800. That is exactly the interest in the question.",
      W("c", "360 × 5 = 1,800")),
    B("So for a how-many-years question: find what 1 year earns, then see how many of those make the whole interest."),
    )

# ── Raju: interest from two banks, then a bat ────────────────────────────────

Q = "f5b795fe"
add(Q,
    B("Raju's 15000 rupees is split: 9000 in Bank A at 6 per cent, and the rest in Bank B at 10 per cent, for 2 years. He buys a bat for 2000 from the interest. How much interest is left?",
      GIVEN("q", "₹15,000: ₹9,000 at 6% (Bank A), the rest at 10% (Bank B)"), L("q2", "2 years. Then a ₹2,000 bat, paid from the interest.")),
    B("First, the rest. 15000 minus 9000 is 6000, so Bank B holds 6000 rupees.",
      W("r", "15,000 − 9,000 = 6,000"), N("r", "= 6,000", "in Bank B")),
    B("Bank A: 9000 is 90 hundreds, each earning 6 rupees a year. 90 times 6 is 540. Careful, the money stays 2 years, so double it: 1080.",
      W("a1", "9,000 ÷ 100 = 90"), W("a2", "90 × 6 = 540"), W("a3", "540 × 2 = 1,080"), N("a3", "= 1,080", "Bank A interest")),
    B("Bank B: 6000 is 60 hundreds, each earning 10 rupees a year. 60 times 10 is 600, and for 2 years that is 1200.",
      W("b1", "6,000 ÷ 100 = 60"), W("b2", "60 × 10 = 600"), W("b3", "600 × 2 = 1,200"), N("b3", "= 1,200", "Bank B interest")),
    ASK(Q, "a1", "Raju pays for the bat. Which money does he pay from?",
        "the interest from both banks", ["the whole 15000", "Bank B's interest only"],
        "The story says he uses the total interest earned from both banks. The 15000 itself is not touched."),
    B("So add the two lots of interest. 1080 plus 1200 is 2280.",
      W("t", "1,080 + 1,200 = 2,280"), N("t", "= 2,280", "all the interest")),
    B("Now buy the bat. 2280 minus 2000 leaves 280 rupees.",
      ANS("ans", "2,280 − 2,000 = 280"), RING("ans", "280")),
    B("Check by adding back. The 280 left, plus the 2000 for the bat, is 2280, all the interest he earned.",
      W("c", "280 + 2,000 = 2,280")),
    B("So split the money first, work out each bank's interest for all the years, add them, and only then spend."),
    )

# ── Ravi's cricket balls ─────────────────────────────────────────────────────

Q = "ff2b2ef6"
h1, h2 = hundreds(5000, 6, "a")
add(Q,
    B("Ravi puts 5000 rupees in a bank at 6 per cent simple interest a year, for 3 years. With just the interest he buys cricket balls at 150 rupees each. How many can he buy?",
      GIVEN("q", "₹5,000 at 6% a year for 3 years. A ball costs ₹150.")),
    h1, h2,
    B("The money stays for 3 years. 300 times 3 is 900. So the interest is 900 rupees.",
      W("i", "300 × 3 = 900"), N("i", "= 900", "interest for 3 years")),
    ASK(Q, "a1", "He spends only the interest on balls that cost 150 each. Which sum tells us how many balls?",
        "900 ÷ 150", ["5000 ÷ 150", "900 − 150"],
        "Only the interest is being spent, and that is 900 rupees. Each ball uses up 150 of it, so we count how many 150s fit into 900."),
    B("2 balls cost 300. And 900 is 3 lots of 300, so that is 3 lots of 2 balls: 6 balls.",
      W("m", "150 × 2 = 300"), ANS("ans", "900 ÷ 150 = 6"), RING("ans", "6")),
    B("Check by multiplying. 6 balls at 150 each is 900, which uses up the interest exactly.",
      W("c", "150 × 6 = 900")),
    B("Notice his 5000 is still safe in the bank. The question only let him spend the interest, so only the interest gets divided."),
    B("So: 1 year's interest, times the years, and then share that interest out by the price of 1 ball."),
    )
