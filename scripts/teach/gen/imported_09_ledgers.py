"""Integers: lists of gains and losses (shop ledgers, game scores)."""
from imported_09_lib import ANS, B, G, GIVEN, M, N, W, choose, lesson, listed

LESSONS = {}


def piles(g, pos, neg, lead="Instead of going day by day, let's collect each kind."):
    """Two beats: gather the profits, gather the losses."""
    sp_, sn = sum(pos), sum(neg)
    return [
        B("%s The profits first: %s. Together they make %d." % (lead, listed(pos), sp_),
          G(g, ["+%d" % p for p in pos], "profits"), W("p", "%s = %d" % (" + ".join(str(p) for p in pos), sp_))),
        B("Now the losses: %s. Together they make %d." % (listed(neg), sn),
          G(g, ["−%d" % n for n in neg], "losses"), W("n", "%s = %d" % (" + ".join(str(n) for n in neg), sn))),
    ]


# ── Kite shop: the mystery Day 5 ─────────────────────────────────────────────
LESSONS["1be8f27d"] = lesson(
    B("A kite shop's six days: plus 120, minus 85, minus 40, plus 95, then a mystery Day 5, and minus 30. After 6 days the total is exactly 20 more than it was after 4 days.",
      GIVEN("g", "+120, −85, −40, +95, Day 5 = ?, −30"), GIVEN("g2", "6-day total = 4-day total + 20")),
    B("Here is the key. Between the 4-day total and the 6-day total, which days were added on?",
      ask=choose(["Day 5 and Day 6", "only Day 5", "all six days"], 0,
                 "The 4-day total already holds Days 1 to 4. To get to the 6-day total we add just two more days: Day 5 and Day 6.")),
    B("And adding those two days made the total go up by 20. So Day 5 and Day 6 together are worth plus 20.",
      M("g2", "+ 20", "box"), W("k1", "Day 5 + Day 6 = 20", label=True)),
    B("Day 6 was a loss of 30. So Day 5, with 30 taken off, leaves 20.",
      M("g", "−30"), W("k2", "Day 5 − 30 = 20", label=True)),
    B("Which number, with 30 taken off, leaves 20?",
      ask=choose(["50", "−10", "20"], 0,
                 "To undo taking off 30, we put the 30 back. 20 plus 30 gets us to the number we started with.")),
    B("20 plus 30 is 50. So Day 5 was a profit of 50 rupees.",
      ANS("a", "20 + 30 = 50"), M("a", "50", "circle"), N("g", "?", "+50")),
    B("Let's check with the real totals. After 4 days: the profits 120 and 95 make 215, and the losses 85 and 40 make 125. 215 minus 125 is 90.",
      W("c1", "120 + 95 = 215"), W("c2", "85 + 40 = 125"), W("c3", "215 − 125 = 90")),
    B("Now add Day 5 and Day 6. 90 plus 50 minus 30 is 110. And 110 is exactly 20 more than 90. It works.",
      W("c4", "90 + 50 − 30 = 110"), W("c5", "110 − 90 = 20")),
    B("The trap is forgetting Day 6. If Day 5 alone were plus 20, the loss of 30 on Day 6 would drag the total below the 4-day total."),
    B("When a question compares two totals, look at what was added between them. Often you hardly need the totals at all."),
)

# ── Tea seller: penalty of 3 times a negative total ──────────────────────────
LESSONS["39019d6e"] = lesson(
    B("Vikram's tea stall, Monday to Friday: profit 45, loss 60, profit 30, loss 55, profit 25. If the week's total is negative, he pays a penalty of 3 times that amount, taken as a plain positive number.",
      GIVEN("g", "+45, −60, +30, −55, +25"), GIVEN("g2", "Penalty = 3 × (size of a negative total)")),
    piles("g", [45, 30, 25], [60, 55], "Profits are positive numbers and losses are negative. Let's collect each kind."),
    B("Profits of 100, losses of 115. What is the total for the week?",
      ask=choose(["−15", "15", "215"], 0,
                 "The losses are bigger than the profits, by 15. So overall the week is a loss, and the total is negative.")),
    B("100 minus 115 is minus 15. The losses win by 15, so the week's total is minus 15.",
      W("t", "100 − 115 = −15"), M("t", "−15")),
    B("The total is negative, so there is a penalty. The size of minus 15, without its sign, is 15. That size is called the absolute value.",
      N("t", "−15", "size 15")),
    B("The penalty is 3 times that. Which sum do we write?",
      ask=choose(["3 × 15", "3 × (−15)", "15 − 3"], 0,
                 "A penalty is an amount of money to pay, so it is a plain positive number. We use the size, 15, and multiply it by 3.")),
    B("3 times 15 is 45. Vikram pays a penalty of 45 rupees.",
      ANS("a", "3 × 15 = 45"), M("a", "45", "circle")),
    B("Check the week as one long sum, working left to right. It comes to minus 15 again, so the penalty of 45 stands.",
      W("c", "45 − 60 + 30 − 55 + 25 = −15")),
    B("Notice 45 is also Monday's profit. That is only a coincidence. And do not stop at 15: the penalty is 3 times it."),
    B("Collect the plus numbers, collect the minus numbers, and compare. Then read on, because the question may want more than the total."),
)

# ── Chai stall: the total, and how much more to reach 100 ────────────────────
LESSONS["4c39ca55"] = lesson(
    B("Vikram's chai stall, Monday to Friday: profit 45, loss 60, profit 30, loss 25, profit 55. We want his total, and how much more he needs on Saturday to make the week exactly 100.",
      GIVEN("g", "+45, −60, +30, −25, +55"), GIVEN("g2", "Target for the week: 100")),
    piles("g", [45, 30, 55], [60, 25], "Profits are positive and losses are negative. Let's collect each kind."),
    B("Profits of 130, losses of 85. What is the five-day total?",
      ask=choose(["a profit of 45", "a loss of 45", "a profit of 215"], 0,
                 "The profits are bigger than the losses this time, so the week is in profit. The total is the profits take away the losses.")),
    B("130 minus 85 is 45. So far the week shows a profit of 45 rupees.",
      W("t", "130 − 85 = 45"), M("t", "45", "underline", 1)),
    B("He wants the week to total exactly 100. How do we find what Saturday must bring?",
      M("g2", "100"),
      ask=choose(["100 − 45", "100 + 45", "100 − 130"], 0,
                 "He already has 45 and wants to reach 100. The gap from 45 up to 100 is what Saturday must add.")),
    B("100 minus 45 is 55. So the total is 45, and he needs 55 more.",
      ANS("a", "100 − 45 = 55"), M("a", "55", "circle")),
    B("Check: 45 plus 55 is 100. Exactly the target.",
      W("c", "45 + 55 = 100")),
    B("Two things were asked for here: the total, and the amount still needed. Make sure both parts of your choice are right, not only the first."),
    B("Collect the profits, collect the losses, subtract. Then the gap to a target is the target take away what you have."),
)

# ── Samosa stall, seven days, and a bonus rule ───────────────────────────────
LESSONS["7a67b583"] = lesson(
    B("Seven days at the samosa stall. Then a bonus rule: a total above 50 earns a bonus of 30, a total from 0 to 50 earns 10, and a loss earns nothing. We want the total with the bonus added.",
      GIVEN("g", "+120, −85, −40, +95, −110, +150, −60"), GIVEN("g2", "Bonus: over 50 → 30;  0 to 50 → 10;  loss → 0")),
    piles("g", [120, 95, 150], [85, 40, 110, 60], "Seven numbers is a lot to do one by one, so let's collect each kind."),
    B("365 minus 295 is 70. The week made a profit of 70 rupees.",
      W("t", "365 − 295 = 70"), M("t", "70")),
    B("Now the bonus rule. The total is 70. Which bonus does Rahul get?",
      ask=choose(["30", "10", "no bonus"], 0,
                 "Compare 70 with 50. 70 is more than 50, so it lands in the top band of the rule.")),
    B("70 is more than 50, so the bonus is 30.",
      W("r", "70 > 50"), M("g2", "over 50 → 30", "box")),
    B("Add the bonus to the total. 70 plus 30 is 100. Rahul records 100 rupees.",
      ANS("a", "70 + 30 = 100"), M("a", "100", "circle")),
    B("Check the total another way, pairing a profit with a loss. 120 minus 85 is 35. 95 minus 40 is 55. 150 minus 110 is 40. Then 35 plus 55 plus 40, minus 60, is 70.",
      W("c1", "120 − 85 = 35"), W("c2", "95 − 40 = 55"), W("c3", "150 − 110 = 40"), W("c4", "35 + 55 + 40 − 60 = 70")),
    B("Two slips to dodge: stopping at 70 and forgetting the bonus, or grabbing the bonus of 10 without comparing with 50 first."),
    B("Collect the profits, collect the losses, subtract. Then test your total against the rule before you use it."),
)

# ── Tea plantation: six days, then a fee of 50 ───────────────────────────────
LESSONS["7ce5f74f"] = lesson(
    B("Six days at Vikram's shop: plus 120, minus 85, minus 45, plus 60, minus 110, plus 90. Then he pays a fee of 50. If he ends below 0, Suresh covers the loss. If above, Vikram donates it.",
      GIVEN("g", "+120, −85, −45, +60, −110, +90"), GIVEN("g2", "Then pay a fee of 50")),
    piles("g", [120, 60, 90], [85, 45, 110], "Let's collect each kind."),
    B("270 minus 240 is 30. So before the fee, Vikram is 30 rupees up.",
      W("t", "270 − 240 = 30"), M("t", "30")),
    B("Now he pays the fee of 50, but he only has 30. What is his balance after paying?",
      M("g2", "fee of 50"),
      ask=choose(["−20", "20", "80"], 0,
                 "Paying a fee takes money away, so we subtract 50. He has only 30, so the fee uses all of it and he is still 20 short.")),
    B("30 minus 50 is minus 20. 30 of the fee uses up his profit, and the other 20 puts him below 0.",
      W("f", "30 − 50 = −20"), M("f", "−20")),
    B("A negative balance means a loss, so Suresh steps in. He covers a loss of 20 rupees.",
      ANS("a", "Suresh covers a loss of ₹20", True), M("a", "₹20", "circle")),
    B("Check it as one long sum, with the fee on the end. It comes to minus 20 again.",
      W("c", "120 − 85 − 45 + 60 − 110 + 90 − 50 = −20")),
    B("The trap is stopping at plus 30 and saying Vikram donates 30. The fee comes off first, and it changes the sign."),
    B("Collect the profits, collect the losses, subtract. Then take off anything else the story takes off, and only then look at the sign."),
)

# ── Ravi's samosa stall and the target of 50 ─────────────────────────────────
LESSONS["81de1bf3"] = lesson(
    B("Ravi's stall, Monday to Friday: plus 45, minus 30, minus 15, plus 60, minus 25. He needs a total profit of at least 50 to win a certificate. Did he beat the target or miss it, and by how much?",
      GIVEN("g", "+45, −30, −15, +60, −25"), GIVEN("g2", "Target: at least 50")),
    piles("g", [45, 60], [30, 15, 25], "Let's collect each kind."),
    B("105 minus 70 is 35. Ravi's total profit is 35 rupees.",
      W("t", "105 − 70 = 35"), M("t", "35")),
    B("The target is 50 and Ravi made 35. Did he beat the target or miss it?",
      M("g2", "50"),
      ask=choose(["he missed it", "he beat it"], 0,
                 "Compare the two numbers. 35 is smaller than 50, so Ravi has not reached the target.")),
    B("35 is less than 50, so he fell short. By how much? It is the gap from 35 up to 50.",
      W("r", "35 < 50")),
    B("50 minus 35 is 15. He fell short by 15 rupees.",
      ANS("a", "50 − 35 = 15"), M("a", "15", "circle")),
    B("Check: 35 plus 15 is 50. So 15 more rupees would have won the certificate.",
      W("c", "35 + 15 = 50")),
    B("Watch for two slips. Adding only the profits, 105, makes it look as if he sailed past the target. And 35 is his total, not the gap."),
    B("Collect the profits, collect the losses, subtract. Then compare with the target to see which way the gap goes."),
)

# ── Mango orchard: swap the worst month for the best ─────────────────────────
LESSONS["cd575693"] = lesson(
    B("Six months of results, in thousands of rupees. Priya's father imagines swapping the worst month's result for the best month's result, and asks how much the total would go up.",
      GIVEN("g", "−12, −8, +5, +15, +22, −3")),
    B("Which is the worst month, the smallest number of all?",
      ask=choose(["−12", "−3", "+5"], 0,
                 "The worst month is the biggest loss. Among the negative numbers, the one furthest below 0 is the smallest: that is minus 12.")),
    B("The worst is minus 12, in January. And the best is the largest number, plus 22, in May.",
      M("g", "−12", "circle"), M("g", "+22", "circle")),
    B("Now think about the swap. Every other month stays the same. Only January changes, from minus 12 to plus 22.",
      W("s", "January: −12 becomes +22", label=True)),
    B("So the total goes up by the distance from minus 12 to plus 22. How far is that?",
      ask=choose(["34", "10", "22"], 0,
                 "Minus 12 and plus 22 are on opposite sides of 0. First it takes 12 steps to get up to 0, and then 22 more.")),
    B("12 steps to get up to 0, then 22 more. 12 plus 22 is 34. The total goes up by 34 thousand rupees.",
      W("d", "12 + 22 = 34"), ANS("a", "22 − (−12) = 34"), M("a", "34", "circle")),
    B("Let's check with the totals. The old total is 19. With plus 22 in January's place, the new total is 53. And 53 minus 19 is 34.",
      W("c1", "−12 − 8 + 5 + 15 + 22 − 3 = 19"), W("c2", "22 − 8 + 5 + 15 + 22 − 3 = 53"), W("c3", "53 − 19 = 34")),
    B("The tempting answer is 22, just the best month. But we also got rid of a loss of 12, and losing a loss is a gain."),
    B("When one number in a list is swapped, the total changes by exactly the difference between the new number and the old one."),
)

# ── Card game: Meera and Sahil, 4 rounds each ────────────────────────────────
LESSONS["5336bb01"] = lesson(
    B("Meera and Sahil each play 4 rounds. Meera scores plus 6, minus 9, plus 4, minus 3. Sahil scores minus 5, plus 8, minus 2, plus 1. How many more points does Sahil have?",
      GIVEN("gm", "Meera: +6, −9, +4, −3"), GIVEN("gs", "Sahil: −5, +8, −2, +1")),
    B("Meera first. Her gains are 6 and 4, which make 10. Her losses are 9 and 3, which make 12.",
      G("gm", ["+6", "+4"], "gains"), W("m1", "6 + 4 = 10"), G("gm", ["−9", "−3"], "losses"), W("m2", "9 + 3 = 12")),
    B("Gains of 10, losses of 12. What is Meera's total?",
      ask=choose(["−2", "2", "22"], 0,
                 "Her losses are bigger than her gains, by 2. So her total is below 0.")),
    B("10 minus 12 is minus 2. Meera is 2 points below 0.",
      W("m3", "10 − 12 = −2"), M("m3", "−2")),
    B("Now Sahil. His gains are 8 and 1, which make 9. His losses are 5 and 2, which make 7. And 9 minus 7 is 2.",
      W("s1", "8 + 1 = 9"), W("s2", "5 + 2 = 7"), W("s3", "9 − 7 = 2"), M("s3", "2", "underline", 1)),
    B("Sahil has 2 and Meera has minus 2. How many more points does Sahil have?",
      ask=choose(["4", "0", "2"], 0,
                 "They are on opposite sides of 0. From minus 2 up to 0 is 2 points, and from 0 up to Sahil's score is another 2.")),
    B("From minus 2 up to 0 is 2 points, and then 2 more to reach Sahil. That is 4 points. As a sum, 2 minus minus 2 is the same as 2 plus 2.",
      ANS("a", "2 − (−2) = 4"), M("a", "4", "circle"), N("a", "− (−2)", "same as + 2")),
    B("Careful: 2 take away 2 gives 0, as if they were level. They are not: one is above 0 and the other is below."),
    B("Total each player on their own. Then the gap between a positive score and a negative score is their two distances from 0, added."),
)

# ── Kite Festival: Sanya, Arjun and a transfer of half ───────────────────────
LESSONS["73f036cf"] = lesson(
    B("Sanya and Arjun play 4 rounds each. Then comes a rule: if Sanya's total is positive, she gives half of it to Arjun. If it is negative, Arjun gives half of his to her. We want Arjun's final score.",
      GIVEN("gs", "Sanya: +12, −5, −8, +3"), GIVEN("ga", "Arjun: −4, +9, +6, −7")),
    B("Sanya first. Her gains are 12 and 3, which make 15. Her losses are 5 and 8, which make 13. And 15 minus 13 is 2.",
      G("gs", ["+12", "+3"], "gains"), G("gs", ["−5", "−8"], "losses"),
      W("s1", "12 + 3 = 15"), W("s2", "5 + 8 = 13"), W("s3", "15 − 13 = 2")),
    B("Now Arjun. His gains are 9 and 6, which make 15. His losses are 4 and 7, which make 11. And 15 minus 11 is 4.",
      W("a1", "9 + 6 = 15"), W("a2", "4 + 7 = 11"), W("a3", "15 − 11 = 4")),
    B("Sanya has 2 and Arjun has 4. Now the rule. Who gives points to whom?",
      ask=choose(["Sanya gives to Arjun", "Arjun gives to Sanya", "nobody gives"], 0,
                 "The rule looks only at Sanya's total. Her total is 2, which is positive, so she is the one who gives.")),
    B("Sanya's total is positive, so she gives half of her points. Half of 2 is 1.",
      M("s3", "2", "circle"), W("h", "2 ÷ 2 = 1")),
    B("Arjun gets that 1 point. 4 plus 1 is 5. Arjun's final score is 5.",
      ANS("a", "4 + 1 = 5"), M("a", "5", "circle")),
    B("And Sanya? She keeps 2 minus 1, which is 1. Together they still have 6 points, the same as before, so no points went missing.",
      W("c1", "2 + 4 = 6"), W("c2", "1 + 5 = 6")),
    B("Two things to watch. It is half of Sanya's points that moves, not half of Arjun's. And it is the sign of Sanya's total that decides who gives, not who is ahead."),
    B("Total each player, then read the rule slowly and test it with your own numbers."),
)

# ── Chai Shop game: Deepa's total minus Farhan's ─────────────────────────────
LESSONS["d4e7a09e"] = lesson(
    B("Deepa and Farhan play 4 rounds each. Deepa: plus 12, minus 5, minus 9, plus 6. Farhan: minus 3, plus 8, plus 4, minus 7. We want Deepa's total minus Farhan's total.",
      GIVEN("gd", "Deepa: +12, −5, −9, +6"), GIVEN("gf", "Farhan: −3, +8, +4, −7")),
    B("Deepa first. Her gains are 12 and 6, which make 18. Her losses are 5 and 9, which make 14.",
      G("gd", ["+12", "+6"], "gains"), W("d1", "12 + 6 = 18"), G("gd", ["−5", "−9"], "losses"), W("d2", "5 + 9 = 14")),
    B("18 minus 14 is 4. Deepa finishes with 4 rupees.",
      W("d3", "18 − 14 = 4"), M("d3", "4", "underline", 2)),
    B("Now Farhan: minus 3, plus 8, plus 4, minus 7. What is his total?",
      ask=choose(["2", "−2", "22"], 0,
                 "Collect his gains, 8 and 4, and his losses, 3 and 7. Then see which pile is bigger, and by how much.")),
    B("His gains are 8 and 4, which make 12. His losses are 3 and 7, which make 10. And 12 minus 10 is 2.",
      W("f1", "8 + 4 = 12"), W("f2", "3 + 7 = 10"), W("f3", "12 − 10 = 2")),
    B("The question wants Deepa's total minus Farhan's total. Which sum is that?",
      ask=choose(["4 − 2", "2 − 4", "4 + 2"], 0,
                 "Deepa's total comes first, because the question says Deepa's minus Farhan's. Deepa has 4 and Farhan has 2.")),
    B("4 minus 2 is 2. The answer is positive, so Deepa has 2 rupees more than Farhan.",
      ANS("a", "4 − 2 = 2"), M("a", "2", "circle", 2)),
    B("Check Deepa round by round: 12, then 7, then minus 2, then 4. Yes, 4.",
      W("c", "12 − 5 − 9 + 6 = 4")),
    B("The order matters in a subtraction. 2 minus 4 would give minus 2, and that would say Deepa has less. Put first whoever the question names first."),
    B("Total each player on their own, then subtract in the order the question asks for."),
)

# ── Card game: Meera's 5 rounds against Deepa's −2 ───────────────────────────
LESSONS["fc8a2b52"] = lesson(
    B("Meera plays 5 rounds: plus 6, minus 9, plus 4, minus 3, plus 5. Her friend Deepa finished on minus 2. How many more points does Meera have than Deepa?",
      GIVEN("g", "Meera: +6, −9, +4, −3, +5"), GIVEN("g2", "Deepa: total −2")),
    B("Collect Meera's gains: 6, 4 and 5 make 15. And her losses: 9 and 3 make 12.",
      G("g", ["+6", "+4", "+5"], "gains"), W("m1", "6 + 4 + 5 = 15"), G("g", ["−9", "−3"], "losses"), W("m2", "9 + 3 = 12")),
    B("Gains of 15, losses of 12. What is Meera's total?",
      ask=choose(["3", "−3", "27"], 0,
                 "This time the gains are bigger than the losses, by 3. So Meera's total is above 0.")),
    B("15 minus 12 is 3. Meera finishes on 3 points.",
      W("m3", "15 − 12 = 3"), M("m3", "3")),
    B("Meera has 3 and Deepa has minus 2. How many more points does Meera have?",
      M("g2", "−2"),
      ask=choose(["5", "1", "3"], 0,
                 "Deepa is below 0 and Meera is above it. From minus 2 up to 0 is 2 points, and then from 0 up to 3 is 3 more.")),
    B("2 points to climb up to 0, then 3 more to reach Meera. 2 plus 3 is 5. Meera has 5 more points.",
      W("d", "2 + 3 = 5"), ANS("a", "3 − (−2) = 5"), M("a", "5", "circle")),
    B("As a subtraction it is 3 minus minus 2. Taking away a negative is the same as adding, so it becomes 3 plus 2.",
      N("a", "− (−2)", "same as + 2")),
    B("The slip to avoid is 3 take away 2, which gives 1. That would be right if Deepa had plus 2, but she is below 0."),
    B("Find the total first. Then, for scores on opposite sides of 0, add their distances from 0."),
)
