"""Simple interest: one part unknown (the other bank's rate or deposit, an unknown split, equal interest)."""
from imported_09_lib import ANS, B, FIG, FORMULA, GIVEN, M, W, choose, hundreds, lesson

LESSONS = {}

FORMULA_SAY = "principal times rate times time, divided by 100"


def known_bank(name, p, r, t):
    """One beat: the bank whose deposit and rate we know."""
    h = hundreds(p)
    y = h * r
    return B("%s we can do straight away. %d is %d hundreds, each earning %d rupees a year. %d times %d is %d a year, and %d years gives %d."
             % (name, p, h, r, h, r, y, t, y * t),
             W("a1", "%d × %d = %d" % (h, r, y)), W("a2", "%d × %d = %d" % (y, t, y * t))), y * t


def other_interest(an, bn, total, ai):
    """Two beats: the other bank's interest is the total take away the known bank's."""
    return [
        B("The two banks together paid %d. %s paid %d of it. So how much did %s pay?" % (total, an, ai, bn),
          ask=choose(["%d − %d" % (total, ai), "%d + %d" % (total, ai), "%d ÷ 2" % total], 0,
                     "The total is %s's interest and %s's interest put together. Take %s's share out, and %s's share is left." % (an, bn, an, bn))),
        B("%d minus %d is %d. That is %s's interest." % (total, ai, total - ai, bn),
          W("o", "%d − %d = %d" % (total, ai, total - ai)), M("o", str(total - ai), "underline", ("%d − %d = %d" % (total, ai, total - ai)).count(str(total - ai)))),
    ]


# ── The rest in the second bank: find that deposit ───────────────────────────

def rest_principal(intro, givens, an, bn, ap, ar, br, t, total, trap):
    a_beat, ai = known_bank(an, ap, ar, t)
    bi = total - ai
    per = br * t
    assert bi % per == 0
    bh = bi // per
    return lesson(
        B(intro, *[GIVEN(i, text) for i, text in givens]),
        a_beat,
        other_interest(an, bn, total, ai),
        B("Now think about just one hundred rupees in %s. At %d percent it earns %d rupees a year, so over %d years it earns %d." % (bn, br, br, t, per),
          W("h", "%d × %d = %d" % (br, t, per))),
        B("Each hundred in %s earned %d rupees, and %s paid %d in all. How many hundreds were in there?" % (bn, per, bn, bi),
          ask=choose(["%d ÷ %d" % (bi, per), "%d × %d" % (bi, per), "%d − %d" % (bi, per)], 0,
                     "Every hundred brings in %d rupees. So count how many lots of %d there are in %d." % (per, per, bi))),
        B("%d divided by %d is %d, because %d times %d is %d. So %s held %d hundreds, which is %d rupees." % (bi, per, bh, bh, per, bi, bn, bh, bh * 100),
          W("d", "%d ÷ %d = %d" % (bi, per, bh)), ANS("a", "%d × 100 = %d" % (bh, bh * 100)), M("a", str(bh * 100), "circle")),
        B("Check %s with the formula: %s. %d times %d times %d, divided by 100, is %d. And %d plus %d is %d."
          % (bn, FORMULA_SAY, bh * 100, br, t, bi, ai, bi, total),
          W("f", FORMULA, label=True), W("c1", "%d × %d × %d ÷ 100 = %d" % (bh * 100, br, t, bi)), W("c2", "%d + %d = %d" % (ai, bi, total))),
        B(trap),
        B("Work out the bank you know, subtract to get the other bank's interest, then work backwards to its deposit."),
    )


LESSONS["7f6507a5"] = rest_principal(
    "Meera's father puts 8000 rupees in Bank A at 5 percent a year, and the rest of his money in Bank B at 8 percent a year. After 4 years the two banks together have paid 4480 in interest. How much is in Bank B?",
    [("g", "Bank A: ₹8000 at 5%. Bank B: ? at 8%"), ("g2", "After 4 years: total interest ₹4480")],
    "Bank A", "Bank B", 8000, 5, 8, 4, 4480,
    "The slip to avoid is sharing the 4480 equally between the banks. They hold different amounts at different rates, so they pay different interest.")

LESSONS["838c8ba1"] = rest_principal(
    "Arjun's father puts 15000 rupees in Bank Desh at 6 percent a year, and the rest in Bank Bharat at 10 percent a year. After 4 years the two banks together have paid 8400 in interest. How much is in Bank Bharat?",
    [("g", "Bank Desh: ₹15000 at 6%. Bank Bharat: ? at 10%"), ("g2", "After 4 years: total interest ₹8400")],
    "Bank Desh", "Bank Bharat", 15000, 6, 10, 4, 8400,
    "Do not assume Bank Bharat holds the same 15000 as Bank Desh. The question says the rest, and the rest turns out to be a different amount.")

# ── Second bank's deposit known: find its rate ───────────────────────────────
_a, _ai = known_bank("Bank A", 8000, 5, 4)
LESSONS["8007f356"] = lesson(
    B("Ankit's father puts 8000 rupees in Bank A at 5 percent a year, and 6000 in Bank B at a rate we are not told. After 4 years the two banks together have paid 3520 in interest. What is Bank B's rate?",
      GIVEN("g", "Bank A: ₹8000 at 5%. Bank B: ₹6000 at R%"), GIVEN("g2", "After 4 years: total interest ₹3520")),
    _a,
    other_interest("Bank A", "Bank B", 3520, _ai),
    B("That 1920 built up over 4 years, the same each year. 1920 divided by 4 is 480 rupees a year.",
      W("y", "1920 ÷ 4 = 480")),
    B("Bank B holds 6000, which is 60 hundreds. Together they earn 480 a year. So what does each hundred earn?",
      W("h", "6000 ÷ 100 = 60"),
      ask=choose(["480 ÷ 60", "480 × 60", "480 ÷ 100"], 0,
                 "The 480 rupees is shared equally among the 60 hundreds. Sharing equally is dividing: 480 divided by 60.")),
    B("480 divided by 60 is 8. Each hundred earns 8 rupees a year, so Bank B's rate is 8 percent.",
      W("r", "480 ÷ 60 = 8"), ANS("a", "R = 8% a year", True), M("a", "8%", "circle")),
    B("Check Bank B with the formula: " + FORMULA_SAY + ". 6000 times 8 times 4, divided by 100, is 1920. And 1600 plus 1920 is 3520.",
      W("f", FORMULA, label=True), W("c1", "6000 × 8 × 4 ÷ 100 = 1920"), W("c2", "1600 + 1920 = 3520")),
    B("Two cuts are needed to reach a rate: down to 1 year, and down to 1 hundred. Miss either one and the number comes out far too big."),
    B("Work out the bank you know, subtract to get the other bank's interest, then cut it down to 1 year and 1 hundred."),
)

# ── Equal interest from both banks: Bank B's rate (2.5%) ─────────────────────
LESSONS["3164e238"] = lesson(
    B("Anita has 6000 rupees. She puts 2000 in Bank A at 5 percent a year and the rest in Bank B. After 4 years both banks have paid her the same interest. What is Bank B's rate?",
      GIVEN("g", "Bank A: ₹2000 at 5%. Bank B: the rest of ₹6000 at R%"), GIVEN("g2", "After 4 years: same interest from both")),
    B("First, how much is in Bank B? 6000 minus 2000 is 4000.",
      M("g", "the rest of ₹6000"), W("s", "6000 − 2000 = 4000")),
    B("Bank A next. 2000 is 20 hundreds, each earning 5 rupees a year. 20 times 5 is 100 rupees a year.",
      W("a0", "2000 ÷ 100 = 20"), W("a1", "20 × 5 = 100")),
    B("Both banks paid the same interest over the same 4 years. So how much does Bank B pay each year?",
      M("g2", "same interest"),
      ask=choose(["₹100, the same as Bank A", "₹200, because it holds twice as much", "₹50"], 0,
                 "The same total interest, over the same number of years, means the same interest every year. So Bank B also pays 100 rupees a year.")),
    B("So Bank B's 4000 rupees earns only 100 a year. 4000 is 40 hundreds, so each hundred earns 100 divided by 40.",
      W("b0", "4000 ÷ 100 = 40")),
    B("100 divided by 40. What is it?",
      ask=choose(["2.5", "4", "0.4"], 0,
                 "40 goes into 100 two times, with some left over. What is left over is exactly half of another 40. So the answer is 2 and a half.")),
    B("100 divided by 40 is 2.5. Each hundred earns 2 and a half rupees a year, so Bank B's rate is 2.5 percent.",
      W("b1", "100 ÷ 40 = 2.5"), ANS("a", "R = 2.5% a year", True), M("a", "2.5%", "circle")),
    B("Check over the 4 years. Bank B: 4000 times 2.5 times 4, divided by 100, is 400. Bank A: 100 a year for 4 years is 400 too.",
      W("c1", "4000 × 2.5 × 4 ÷ 100 = 400"), W("c2", "100 × 4 = 400")),
    B("This makes sense. Bank B holds twice as much money as Bank A, so it needs only half the rate to pay the same. Half of 5 percent is 2.5 percent."),
    B("For equal interest: find what one bank pays in a year, then ask what rate makes the other bank match it."),
)

# ── Equal interest from both schemes: Scheme B's rate (40/7 %) ───────────────
LESSONS["3a906d76"] = lesson(
    B("Ravi has 12000 rupees. He puts 5000 in Scheme A at 8 percent a year and the rest in Scheme B. After 3 years both schemes have earned the same interest. What is Scheme B's rate?",
      GIVEN("g", "Scheme A: ₹5000 at 8%. Scheme B: the rest of ₹12000"), GIVEN("g2", "After 3 years: same interest from both. R = ?")),
    B("First, how much is in Scheme B? 12000 minus 5000 is 7000.",
      M("g", "the rest of ₹12000"), W("s", "12000 − 5000 = 7000")),
    B("Scheme A next. 5000 is 50 hundreds, each earning 8 rupees a year. 50 times 8 is 400 rupees a year.",
      W("a0", "5000 ÷ 100 = 50"), W("a1", "50 × 8 = 400")),
    B("Both schemes earned the same interest over the same 3 years. So how much does Scheme B earn each year?",
      M("g2", "same interest"),
      ask=choose(["₹400, the same as Scheme A", "more, because it holds more", "₹1200"], 0,
                 "The same total, over the same 3 years, means the same amount every year. So Scheme B also earns 400 rupees a year.")),
    B("Scheme B holds 7000, which is 70 hundreds. Together they earn 400 a year, so each hundred earns 400 divided by 70.",
      W("b0", "7000 ÷ 100 = 70")),
    B("400 divided by 70 does not come out as a whole number, so we leave it as a fraction. Cancel a zero from the top and the bottom: 40 over 7.",
      W("b1", "400 ÷ 70 = 40/7"), M("b1", "40/7")),
    B("Roughly how big is 40 over 7? Here are two facts to help.",
      W("e1", "7 × 5 = 35"), W("e2", "7 × 6 = 42"),
      ask=choose(["between 5 and 6", "exactly 5", "more than 8"], 0,
                 "7 times 5 is 35, and 7 times 6 is 42. 40 sits between those two, so 40 over 7 is between 5 and 6.")),
    B("So Scheme B's rate is 40 over 7 percent, a little under 6 percent.",
      ANS("a", "R = 40/7 %", True), M("a", "40/7 %", "circle")),
    B("Check over the 3 years: both schemes come to 1200. And the rate is lower than Scheme A's 8 percent, as it must be, because Scheme B holds more money.",
      W("c1", "5000 × 8 × 3 ÷ 100 = 1200"), W("c2", "7000 × 40/7 × 3 ÷ 100 = 1200")),
    B("Do not be put off when an answer is a fraction. If the working is sound, a fraction is a perfectly good answer."),
)

# ── Equal interest from an unknown split (₹4615.38) ──────────────────────────
LESSONS["920aaa2e"] = lesson(
    B("Ravi splits 12000 rupees between two accounts. One pays 5 percent a year and the other pays 8 percent. After 3 years both accounts have earned the same interest. How much is in the 8 percent account?",
      GIVEN("g", "₹12000 in two parts: one at 5%, one at 8%"), GIVEN("g2", "After 3 years: same interest from both. 8% part = ?")),
    B("Both parts earn the same interest. Which part must be the smaller one?",
      ask=choose(["the 8% part", "the 5% part", "they are equal"], 0,
                 "A higher rate earns more on every hundred rupees. To end up with the same interest, the 8 percent account needs fewer hundreds in it.")),
    B("Think in hundreds. Each hundred at 5 percent earns 5 rupees a year. Each hundred at 8 percent earns 8. For the interest to match, those have to balance.",
      W("k", "(hundreds at 5%) × 5 = (hundreds at 8%) × 8", label=True)),
    B("Here is a pair that balances. 8 hundreds at 5 percent earn 40, and 5 hundreds at 8 percent earn 40 as well.",
      W("k1", "8 × 5 = 40"), W("k2", "5 × 8 = 40")),
    B("So the money splits in the ratio 8 to 5: 8 shares in the 5 percent account for every 5 shares in the 8 percent account. That is 13 shares in all.",
      W("k3", "8 + 5 = 13"),
      FIG("f", {"kind": "barModel", "bars": [{"segments": [
          {"units": 8, "label": "8 shares at 5%", "tone": "a"}, {"units": 5, "label": "5 shares at 8%", "tone": "b"}],
          "brace": "₹12000"}]})),
    B("The 8 percent account gets 5 of the 13 shares of 12000. Which sum is that?",
      ask=choose(["12000 × 5 ÷ 13", "12000 × 8 ÷ 13", "12000 ÷ 5"], 0,
                 "Split 12000 into 13 equal shares, then take 5 of them, because the 8 percent account is the smaller part, with 5 shares.")),
    B("12000 times 5 is 60000. Dividing by 13 does not come out exactly. To the nearest paisa it is 4615 rupees and 38 paise.",
      W("m", "12000 × 5 = 60000"), ANS("a", "60000 ÷ 13 ≈ 4615.38"), M("a", "4615.38", "circle"),
      W("aw", "₹4615.38 = 4615 rupees 38 paise", label=True)),
    B("The other part is the rest, 7384.62. Notice it is the bigger part, and it sits in the 5 percent account.",
      W("o", "12000 − 4615.38 = 7384.62")),
    B("Check 1 year. 4615.38 times 8, divided by 100, is about 369.23. And 7384.62 times 5, divided by 100, is about 369.23 too. They match.",
      W("c1", "4615.38 × 8 ÷ 100 ≈ 369.23"), W("c2", "7384.62 × 5 ÷ 100 ≈ 369.23")),
    B("The 3 years never mattered, because both parts stayed the same length of time. And mind which part the question asks for: the 8 percent part is the smaller one."),
    B("For equal interest, the bigger rate gets the smaller share. Swap the two rates to get the ratio of the shares."),
)

# ── Unknown split, total interest known: how much in Account B ───────────────
LESSONS["13ec64a9"] = lesson(
    B("Ravi splits 12000 rupees between two accounts. Account A pays 5 percent a year and Account B pays 8 percent. After 3 years the two together have paid 2340 in interest. How much is in Account B?",
      GIVEN("g", "₹12000 split: Account A at 5%, Account B at 8%"), GIVEN("g2", "After 3 years: total interest ₹2340. B = ?")),
    B("We do not know the split, so let's begin with a pretend. Suppose every rupee went into Account A, at 5 percent."),
    B("12000 is 120 hundreds, each earning 5 rupees a year. 120 times 5 is 600 a year, and over 3 years that is 1800.",
      W("p0", "12000 ÷ 100 = 120"), W("p1", "120 × 5 = 600"), W("p2", "600 × 3 = 1800")),
    B("But the real interest was 2340, which is more than 1800. Where did the extra come from?",
      ask=choose(["money in B earns at a higher rate", "the money stayed longer", "the bank added a gift"], 0,
                 "Our pretend put everything at 5 percent. In real life some of the money sits in Account B, where every hundred earns more.")),
    B("The extra is 2340 minus 1800, which is 540 rupees.",
      W("e", "2340 − 1800 = 540"), M("e", "540", "box")),
    B("Each hundred in B earns 8 instead of 5: that is 3 rupees extra a year. Over 3 years, 9 rupees extra per hundred.",
      W("x1", "8 − 5 = 3"), W("x2", "3 × 3 = 9")),
    B("Each hundred in B brings 9 extra rupees, and the extra is 540 altogether. How many hundreds are in B?",
      ask=choose(["540 ÷ 9", "540 × 9", "540 − 9"], 0,
                 "Every hundred sitting in Account B accounts for 9 of the extra rupees. So count how many lots of 9 make 540.")),
    B("540 divided by 9 is 60. So Account B holds 60 hundreds, which is 6000 rupees.",
      W("d", "540 ÷ 9 = 60"), ANS("a", "60 × 100 = 6000"), M("a", "6000", "circle")),
    B("Check. That leaves 6000 in A as well. A at 5 percent for 3 years earns 900. B at 8 percent for 3 years earns 1440. And 900 plus 1440 is 2340.",
      W("c1", "6000 × 5 × 3 ÷ 100 = 900"), W("c2", "6000 × 8 × 3 ÷ 100 = 1440"), W("c3", "900 + 1440 = 2340")),
    B("Careful with the extra per hundred. It comes from the difference of the rates, 3, not from the 8 on its own."),
    B("When a total is split in a way you are not told, pretend it is all one kind. The gap between the pretend and the truth tells you the split."),
)

# ── Unknown split, total interest known: how much in Bank A ──────────────────
LESSONS["3c453b93"] = lesson(
    B("Grandfather splits 12000 rupees between two banks. Bank A pays 5 percent a year and Bank B pays 8 percent. After 4 years the two banks together have paid 2880 in interest. How much went into Bank A?",
      GIVEN("g", "₹12000 split: Bank A at 5%, Bank B at 8%"), GIVEN("g2", "After 4 years: total interest ₹2880. A = ?")),
    B("We do not know the split, so let's begin with a pretend. Suppose every rupee went into Bank B, at 8 percent."),
    B("12000 is 120 hundreds, each earning 8 rupees a year. 120 times 8 is 960 a year, and over 4 years that is 3840.",
      W("p0", "12000 ÷ 100 = 120"), W("p1", "120 × 8 = 960"), W("p2", "960 × 4 = 3840")),
    B("But the real interest was only 2880, less than 3840. Why is the real figure smaller?",
      ask=choose(["some money is in A, at a lower rate", "the money stayed a shorter time", "Bank B paid less than it promised"], 0,
                 "Our pretend put everything at 8 percent. In real life some of the money sits in Bank A, where every hundred earns less.")),
    B("The shortfall is 3840 minus 2880, which is 960 rupees.",
      W("e", "3840 − 2880 = 960"), M("e", "960", "box")),
    B("Each hundred in Bank A earns 5 instead of 8: that is 3 rupees less a year. Over 4 years, 12 rupees less per hundred.",
      W("x1", "8 − 5 = 3"), W("x2", "3 × 4 = 12")),
    B("Each hundred in A loses 12 rupees of interest, and 960 is lost altogether. How many hundreds are in A?",
      ask=choose(["960 ÷ 12", "960 × 12", "960 − 12"], 0,
                 "Every hundred sitting in Bank A accounts for 12 of the missing rupees. So count how many lots of 12 make 960.")),
    B("960 divided by 12 is 80. So Bank A holds 80 hundreds, which is 8000 rupees.",
      W("d", "960 ÷ 12 = 80"), ANS("a", "80 × 100 = 8000"), M("a", "8000", "circle")),
    B("Check. A has 8000 at 5 percent for 4 years, which earns 1600. B has the other 4000 at 8 percent, which earns 1280. And 1600 plus 1280 is 2880.",
      W("c1", "8000 × 5 × 4 ÷ 100 = 1600"), W("c2", "4000 × 8 × 4 ÷ 100 = 1280"), W("c3", "1600 + 1280 = 2880")),
    B("It is only a coincidence that 960 turned up twice in this working. And mind which bank is asked for: A is the 5 percent one, and it holds the bigger part."),
    B("When a total is split in a way you are not told, pretend it is all one kind. The gap between the pretend and the truth tells you the split."),
)

# ── Meera at 8%, Ravi at 12% for one year less: same amount ──────────────────
LESSONS["3e15386d"] = lesson(
    B("Meera and Ravi each deposit 5000 rupees. Meera gets 8 percent a year and Ravi gets 12 percent, but Ravi takes his money out 1 year earlier. They end with exactly the same amount. How many years did Meera stay?",
      GIVEN("g", "Meera: ₹5000 at 8%. Ravi: ₹5000 at 12%"), GIVEN("g2", "Ravi stays 1 year less. Same amount at the end")),
    B("They started with the same 5000 and ended with the same amount. So the interest each one earned must be the same too.",
      W("k", "Meera's interest = Ravi's interest", label=True)),
    B("Take 1 year for each. 5000 is 50 hundreds. Meera earns 8 rupees on each, which is 400 a year. Ravi earns 12 on each, which is 600 a year.",
      W("h", "5000 ÷ 100 = 50"), W("m", "50 × 8 = 400"), W("r", "50 × 12 = 600")),
    B("Ravi earns more each year but stays 1 year less. Let's test. If Meera stays 2 years, Ravi stays 1. Are their interests equal?",
      ask=choose(["No: 800 and 600", "Yes, they are equal", "No: 400 and 600"], 0,
                 "Meera's 2 years give 2 times 400, which is 800. Ravi's 1 year gives 600. Not equal yet, so we try a longer stay.")),
    B("2 years and 1 year gives 800 and 600: not equal. Try Meera 3 years, Ravi 2. Meera: 3 times 400 is 1200. Ravi: 2 times 600 is 1200. Equal!",
      W("t1", "2 × 400 = 800"), W("t2", "3 × 400 = 1200"), W("t3", "2 × 600 = 1200"), M("t2", "1200"), M("t3", "1200")),
    B("So Meera kept her money in the bank for 3 years, and Ravi for 2.",
      ANS("a", "Meera: 3 years", True), M("a", "3 years", "circle")),
    B("Why does it settle at 3? In each year they share, Ravi gains 200 on Meera. Meera's extra year is worth 400 to her. So 2 years of Ravi's gains cancel it exactly.",
      W("w1", "600 − 400 = 200"), W("w2", "400 ÷ 200 = 2")),
    B("Would 4 years work? Meera would earn 1600, and Ravi, in 3 years, 1800. No longer equal. So 3 years is the only answer.",
      W("c1", "4 × 400 = 1600"), W("c2", "3 × 600 = 1800")),
    B("And both of them walk away with 5000 plus 1200, which is 6200 rupees.",
      W("c3", "5000 + 1200 = 6200")),
    B("Remember whose time was asked for: Meera's, the longer one. And when you cannot see an answer straight away, test small numbers in an orderly way."),
)
