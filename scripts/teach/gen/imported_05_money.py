"""Batch 05: money stories with decimals (spending, sharing a bill, profit).

Where several questions tell the same story with different numbers, one builder
writes the lesson and computes every line; the rest are written one by one.
"""
from imported_05_lib import ANS, B, D, FIG, GIVEN, M, N, RING, W, ask, bar, lesson, mon, num, rs, table

LESSONS = {}

P = "AIGEN_grade5_"


# ── Start with some money, buy things, perhaps find some more ────────────────

def spend(who, she, intro, given, start, prices, found=None, found_clue=None, closing=None):
    start = D(start)
    prices = [D(p) for p in prices]
    spent = sum(prices)
    left = start - spent
    beats = [
        B(intro, GIVEN("q", given, True)),
        B("What should we work out first?",
          ask=ask("the total %s spent" % she, ["the price of just one thing", "the money %s has at the end" % she],
                  "Several prices went out of the purse. Add them into one total first, and then there is only one subtraction to do.")),
    ]
    if len(prices) == 3:
        s12 = prices[0] + prices[1]
        beats.append(B("Line up the decimal points and add. %s plus %s is %s." % (mon(prices[0]), mon(prices[1]), mon(s12)),
                       W("a1", "%s + %s = %s" % (rs(prices[0]), rs(prices[1]), rs(s12)))))
        beats.append(B("Then %s plus %s is %s. That is everything %s spent." % (mon(s12), mon(prices[2]), mon(spent), who),
                       W("a2", "%s + %s = %s" % (rs(s12), rs(prices[2]), rs(spent))), M("a2", rs(spent))))
    else:
        beats.append(B("Line up the decimal points and add. %s plus %s is %s. That is everything %s spent." % (
            mon(prices[0]), mon(prices[1]), mon(spent), who),
            W("a2", "%s + %s = %s" % (rs(prices[0]), rs(prices[1]), rs(spent))), M("a2", rs(spent))))
    sub = "₹%d.00 − %s = %s" % (int(start), rs(spent), rs(left))
    zeros = "Write %s with a point and two zeros, so the paise have something to be taken from." % mon(start)
    if found is not None:
        found = D(found)
        final = left + found
        beats += [
            B("Now take that away from the %s rupees. %s %s minus %s leaves %s." % (
                mon(start), zeros, mon(start), mon(spent), mon(left)), W("s", sub)),
            B("Is %s rupees the answer?" % mon(left),
              ask=ask("No: add the %s rupees %s found" % (mon(found), she),
                      ["Yes: %s rupees is the answer" % mon(left), "No: take away %s rupees more" % mon(found)],
                      "Read the end of the story again. %s That is money coming in, so it is added on." % found_clue)),
            B("%s plus %s is %s. %s now has %s rupees." % (mon(left), mon(found), mon(final), who, mon(final)),
              ANS("a", "%s + %s = %s" % (rs(left), rs(found), rs(final))), RING("a", rs(final))),
            B("Check by going backwards. %s minus the %s found is %s, and %s plus the %s spent is %s, the money at the start." % (
                mon(final), mon(found), mon(left), mon(left), mon(spent), mon(start)),
              W("c", "%s + %s = %s" % (rs(left), rs(spent), rs(start)))),
            B(closing or "So in a money story: add up what went out, subtract it once, then add what came in. And keep the decimal points in line."),
        ]
    else:
        beats += [
            B("Now take that away from the %s rupee note. %s %s minus %s leaves %s rupees of change." % (
                mon(start), zeros, mon(start), mon(spent), mon(left)),
              ANS("a", sub), RING("a", rs(left))),
            B("Careful: %s is what %s spent, not the change. It is one of the choices, waiting to catch you." % (mon(spent), she),
              M("a2", rs(spent), "box")),
            B("Check: the money spent and the change should make the note again. %s plus %s is %s." % (
                mon(spent), mon(left), mon(start)),
              W("c", "%s + %s = %s" % (rs(spent), rs(left), rs(start)))),
            B(closing or "So for change: add up the whole bill first, then take it from the note. And keep the decimal points in line."),
        ]
    return lesson(*beats)


LESSONS[P + "11634c19-aabc-416b-a7e2-60f66802660a"] = spend(
    "Riya", "she",
    "Riya starts with 100 rupees. She buys tea leaves, sugar and milk, and then she finds a 2 rupee coin. How much does she have now?",
    "₹100. Spent ₹32.45, ₹18.70, ₹25.50. Found ₹2.", 100, ["32.45", "18.70", "25.50"],
    found=2, found_clue="Riya picked up a 2 rupee coin on her way back.")

LESSONS[P + "223c949d-adbe-438c-bf25-ff76ccf7fb0a"] = spend(
    "Priya", "she",
    "Priya goes to the mela with 50 rupees. She buys sparklers and diyas, and then finds a 5 rupee coin. How much does she have now?",
    "₹50. Spent ₹18.75 and ₹14.50. Found ₹5.", 50, ["18.75", "14.50"],
    found=5, found_clue="Priya found a 5 rupee coin on the ground.",
    closing="Money going out is subtracted, and money coming in is added. Read to the very end of the story before you stop.")

LESSONS[P + "321e53f5-a334-48dc-9de2-eec181959281"] = spend(
    "Aarav", "he",
    "Aarav has 100 rupees of gift money. He buys a toy flute and a box of sweets, and then finds 5.25 rupees in his jacket pocket. How much does he have now?",
    "₹100. Spent ₹23.45 and ₹31.80. Found ₹5.25.", 100, ["23.45", "31.80"],
    found="5.25", found_clue="Aarav found 5.25 rupees in his pocket and added it to his money.",
    closing="Spend, so subtract. Find, so add. And a neat round answer like this one is a good sign that the decimals were lined up properly.")

LESSONS[P + "7027d81e-f554-4a17-87c7-20ab0e973ca0"] = spend(
    "Aarav", "he",
    "Aarav buys a geometry box, a pack of pencils and an eraser, and pays with a 100 rupee note. How much change does he get?",
    "Bought: ₹45.60, ₹12.85, ₹3.75. Paid ₹100.", 100, ["45.60", "12.85", "3.75"])


# ── Spent some, has some left: how much at the start? ────────────────────────

def grandma(qid, spends, left, less, ask_first, closing):
    spends = [D(s) for s in spends]
    left, less = D(left), D(less)
    s12 = spends[0] + spends[1]
    spent = s12 + spends[2]
    gift = spent + left
    priya = gift - less
    LESSONS[qid] = lesson(
        B("Ravi spent his Diwali money on 3 things and still has %s rupees left. His sister Priya was given %s rupees less than Ravi. How much was Priya given?" % (
            mon(left), mon(less)),
          GIVEN("q", "Spent %s, %s, %s. Left: %s" % (rs(spends[0]), rs(spends[1]), rs(spends[2]), rs(left)), True),
          W("q2", "Priya = Ravi's gift − %s" % rs(less), True)),
        B(ask_first,
          ask=ask("how much Ravi was given", ["how much Ravi spent", "how much Ravi has left"],
                  "Priya's amount is measured from what Ravi was given, right at the start. So that starting amount is the first thing to find.")),
        B("Ravi's gift went two ways: some was spent, and some is still with him. Put the two back together, and we have the whole gift.",
          FIG("f", bar([(3, "spent", "a"), (1.5, "left %s" % rs(left), "b")], "Ravi's gift = ?"))),
        B("Add the spending, with the decimal points in line. %s plus %s is %s." % (mon(spends[0]), mon(spends[1]), mon(s12)),
          W("a1", "%s + %s = %s" % (rs(spends[0]), rs(spends[1]), rs(s12)))),
        B("Add the third, %s, and he spent %s in all." % (mon(spends[2]), mon(spent)),
          W("a2", "%s + %s = %s" % (rs(s12), rs(spends[2]), rs(spent)))),
        B("Now add what he has left. %s plus %s is %s. So Ravi was given %s rupees." % (mon(spent), mon(left), mon(gift), mon(gift)),
          W("g", "%s + %s = %s" % (rs(spent), rs(left), rs(gift))), N("g", rs(gift), "Ravi's gift")),
        B("Careful: %s is Ravi's money, and it is one of the choices. But the question asks about Priya." % mon(gift)),
        B("Priya was given %s less. %s minus %s is %s rupees." % (mon(less), mon(gift), mon(less), mon(priya)),
          ANS("a", "%s − %s = %s" % (rs(gift), rs(less), rs(priya))), RING("a", rs(priya))),
        B("Check: %s plus %s is %s, Ravi's gift. And %s minus the %s he spent leaves %s. It all fits." % (
            mon(priya), mon(less), mon(gift), mon(gift), mon(spent), mon(left)),
          W("c1", "%s + %s = %s" % (rs(priya), rs(less), rs(gift))), W("c2", "%s − %s = %s" % (rs(gift), rs(spent), rs(left)))),
        B(closing),
    )


grandma(P + "16bd94d4-afa8-45d7-a397-aab52d11f241", ["247.50", "183.75", "118.25"], "200.50", 150,
        "Before we can find Priya's money, what must we know?",
        "When a story tells you what was spent and what is left, add them to get back to the start. Then answer the question that was asked.")
grandma(P + "2caefe13-065e-41c8-a41b-b2b4a264e9e4", ["247.50", "183.75", "94.25"], "124.50", 350,
        "The story never says how much Ravi was given. Which amount do we need first?",
        "Money spent plus money left takes you back to the start. And always check whose money the question wants.")


# ── Sharing what is left of a bill ───────────────────────────────────────────

LESSONS[P + "098739b2-ab2d-4e62-8506-dfbb34789255"] = lesson(
    B("The bill is 156.50 rupees. Rohan, Aarav and Meera pay part of it, and Kiran and Priya share the rest equally. How much does each of those two pay?",
      GIVEN("q", "Bill ₹156.50. Paid: ₹45.75, ₹38.60, ₹29.85", True), W("q2", "The rest is shared equally by 2", True),
      FIG("f", bar([(2, "paid by 3", "a"), (1, "Kiran ?", "unknown"), (1, "Priya ?", "unknown")], "₹156.50"))),
    B("What do we find first?",
      ask=ask("what the 3 friends paid altogether", ["156.50 ÷ 2", "156.50 ÷ 5"],
              "Kiran and Priya share only what is left of the bill. To know what is left, we first need the total the other 3 have paid.")),
    B("45.75 plus 38.60 is 84.35.",
      W("a1", "₹45.75 + ₹38.60 = ₹84.35")),
    B("Add Meera's 29.85, and the three of them have paid 114.20.",
      W("a2", "₹84.35 + ₹29.85 = ₹114.20")),
    B("Take that from the bill. 156.50 minus 114.20 leaves 42.30.",
      W("s", "₹156.50 − ₹114.20 = ₹42.30")),
    B("Careful: 42.30 is for Kiran and Priya together. It is one of the choices, but the question asks what each of them pays.",
      N("s", "₹42.30", "for 2 people")),
    B("Half of 42 is 21, and half of 0.30 is 0.15. So each of them pays 21.15 rupees.",
      W("h1", "42 ÷ 2 = 21"), W("h2", "0.30 ÷ 2 = 0.15"), ANS("a", "₹42.30 ÷ 2 = ₹21.15"), RING("a", "₹21.15")),
    B("Check by adding up all 5 payments. 114.20, plus 21.15, plus 21.15, makes 156.50, the whole bill.",
      W("c", "₹114.20 + ₹21.15 + ₹21.15 = ₹156.50")),
    B("So: add what has been paid, subtract to find what is left, and then share it. Three small steps, in that order."),
)

LESSONS[P + "383296a4-7767-4dcf-97c2-90b402055bcd"] = lesson(
    B("The bat costs 875.50 rupees. Priya and Arjun have saved some of it, and their grandmother gives the rest, split equally between them. How much does each receive from her?",
      GIVEN("q", "Bat ₹875.50. Saved: ₹312.75 and ₹248.60", True), W("q2", "Grandmother's gift is split equally", True),
      FIG("f", bar([(3, "₹312.75", "a"), (2.5, "₹248.60", "b"), (3, "gift ?", "unknown")], "₹875.50"))),
    B("First, what the two of them have saved. 312.75 plus 248.60 is 561.35.",
      W("a", "₹312.75 + ₹248.60 = ₹561.35")),
    B("The bat costs 875.50. How do we find grandmother's gift?",
      ask=ask("875.50 − 561.35", ["875.50 + 561.35", "875.50 ÷ 2"],
              "They now have exactly enough. So the gift fills the gap between what they saved and what the bat costs. A gap is found by subtracting.")),
    B("875.50 minus 561.35 is 314.15. That is the whole gift.",
      W("s", "₹875.50 − ₹561.35 = ₹314.15")),
    B("Careful: 314.15 is one of the choices, but it is the gift for both children together. Each one gets half.",
      N("s", "₹314.15", "for both")),
    B("Half of 314 is 157, and half of 0.15 is 0.075. So each receives 157.075 rupees.",
      W("h1", "314 ÷ 2 = 157"), W("h2", "0.15 ÷ 2 = 0.075"), ANS("ans", "₹314.15 ÷ 2 = ₹157.075"), RING("ans", "₹157.075")),
    B("Notice the 3 places after the point. The gift has an odd number of paise, and half of an odd number is never whole. So the exact half needs one more place."),
    B("Check: 2 shares of 157.075 make 314.15. And 561.35 plus 314.15 is 875.50, the price of the bat.",
      W("c1", "2 × 157.075 = 314.15"), W("c2", "₹561.35 + ₹314.15 = ₹875.50")),
    B("So: add what they have, subtract to find the gap, then halve it. And keep every decimal place when you halve."),
)

LESSONS[P + "0bec48ff-17bd-4645-8f31-587a37db5c47"] = lesson(
    B("Ravi and Priya sell laddoos for 2 days, put all their money together, and split it equally. How much does each get?",
      GIVEN("q", "All earnings shared equally: each = ?", True),
      FIG("f", table(["Seller", "Price", "Day 1", "Day 2"], [["Ravi", "₹12.75", "24", "16"], ["Priya", "₹9.50", "36", "28"]]))),
    B("Each seller keeps the same price on both days. So first add up how many each one sold. Ravi: 24 and 16 make 40. Priya: 36 and 28 make 64.",
      W("r1", "24 + 16 = 40"), W("p1", "36 + 28 = 64")),
    B("Ravi's money is 40 times 12.75. Now 4 times 12.75 is 51, so 40 times is 10 times as much: 510 rupees.",
      W("r2", "4 × 12.75 = 51"), W("r3", "40 × ₹12.75 = ₹510")),
    B("Priya's money is 64 times 9.50. 64 nines are 576, and 64 halves are 32. Together, 608 rupees.",
      W("p2", "64 × 9 = 576"), W("p3", "576 + 32 = 608"), W("p4", "64 × ₹9.50 = ₹608")),
    B("They put the money together and split it equally. So what do we do with 510 and 608?",
      ask=ask("add them, then halve", ["subtract them", "add them, and stop there"],
              "Putting money together means adding. And splitting it equally between 2 people means halving the total.")),
    B("510 plus 608 is 1118.",
      W("t", "₹510 + ₹608 = ₹1118")),
    B("Half of 1118 is 559. Each person gets 559 rupees.",
      ANS("a", "₹1118 ÷ 2 = ₹559"), RING("a", "₹559")),
    B("Check: 2 shares of 559 make 1118, all the money.",
      W("c", "2 × 559 = 1118")),
    B("Careful: Ravi earned 510 himself, and that is one of the choices. But the money was pooled first. Find each total, add, then share."),
)

LESSONS[P + "8cf87eb3-9782-44eb-aa20-7405c54a620c"] = lesson(
    B("The friends spent 847.50 rupees on ingredients and took in 1338.75. They give 0.4 of the profit to charity and share the rest among 3. How much does each friend get?",
      GIVEN("q", "Cost ₹847.50. Earnings ₹1338.75.", True), W("q2", "0.4 of profit to charity, rest shared by 3", True)),
    B("Profit is what they took in, minus what they paid out. 1338.75 minus 847.50 is 491.25.",
      W("p", "₹1338.75 − ₹847.50 = ₹491.25"), N("p", "₹491.25", "profit")),
    B("The price of one samosa, 12.75, is just passing by. We already know the total earnings, so we do not need it."),
    B("They give 0.4 of the profit to charity. What part of the profit do they keep?",
      ask=ask("0.6", ["0.4", "1.4"],
              "The whole profit is 1 whole. Give away 0.4 of it, and 1 minus 0.4 is left. That is 0.6.")),
    B("So they keep 0.6 of 491.25. One tenth of 491.25 is 49.125, and 6 tenths is 6 times that: 294.75.",
      W("k1", "491.25 ÷ 10 = 49.125"), W("k2", "0.6 × 491.25 = 294.75")),
    B("Now share 294.75 among 3 friends. 294 divided by 3 is 98, and 0.75 divided by 3 is 0.25.",
      W("d1", "294 ÷ 3 = 98"), W("d2", "0.75 ÷ 3 = 0.25")),
    B("Each friend gets 98.25 rupees.",
      ANS("a", "₹294.75 ÷ 3 = ₹98.25"), RING("a", "₹98.25")),
    B("Check: the charity gets 196.50. Add the 294.75 the friends keep, and we are back at the profit, 491.25.",
      W("c1", "0.4 × 491.25 = 196.50"), W("c2", "₹196.50 + ₹294.75 = ₹491.25")),
    B("Careful: sharing the whole profit by 3 forgets the charity. Find the profit, take out the gift, and only then share."),
)


# ── Profit at the chai stall ─────────────────────────────────────────────────

def parts(name, cups, price, tag):
    """One beat: cups times price, done as the whole rupees and then the part after the point."""
    whole = int(price)
    frac = price - whole
    total = cups * price
    final = W(tag + "3", "%s × %s = %s" % (mon(cups), rs(price), rs(total)))
    if frac == 0:
        return B("%s cups: %s times %d is %s rupees." % (name.capitalize(), mon(cups), whole, mon(total)), final)
    a, b = cups * whole, cups * frac
    return B("%s cups: %s times %d is %s, and %s times %s is %s. Together, %s rupees." % (
        name.capitalize(), mon(cups), whole, mon(a), mon(cups), num(frac), num(b), mon(total)),
        W(tag + "1", "%s × %d = %s" % (mon(cups), whole, mon(a))),
        W(tag + "2", "%s × %s = %s" % (mon(cups), num(frac), num(b))), final)


def profit(qid, intro, sizes, costs, extra, closing):
    """sizes: three (name, cups, price); costs: three (name, amount)."""
    (n1, c1, p1), (n2, c2, p2), (n3, c3, p3) = [(n, D(c), D(p)) for (n, c, p) in sizes]
    whole = int(p1)
    a = c1 * whole
    b = c1 * (p1 - whole)
    e1, e2, e3 = c1 * p1, c2 * p2, c3 * p3
    assert a + b == e1 and (p1 - whole) == D("0.5")
    earned = e1 + e2 + e3
    cs = [D(c) for (_, c) in costs]
    spent = sum(cs)
    gain = earned - spent
    LESSONS[qid] = lesson(
        B(intro,
          GIVEN("q", "Profit from the chai stall = ?", True),
          FIG("f", table(["Size", "Price", "Cups sold"], [[n.capitalize(), rs(p), mon(c)] for (n, c, p) in sizes]))),
        B(extra),
        B("What is profit?",
          ask=ask("money earned minus money spent", ["money earned plus money spent", "all the money earned"],
                  "Profit is what you really gain. Count the money that came in, then take away what had to be paid out.")),
        B("Start with the money earned. %s cups: %s at %s each. %s times %d is %s, and %s halves are %s more. That is %s rupees." % (
            n1.capitalize(), mon(c1), mon(p1), mon(c1), whole, mon(a), mon(c1), mon(b), mon(e1)),
          W("e0", "%s × %d = %s" % (mon(c1), whole, mon(a))), W("e1", "%s × %s = %s" % (mon(c1), rs(p1), rs(e1)))),
        parts(n2, c2, p2, "m"),
        parts(n3, c3, p3, "l"),
        B("Add the three: %s plus %s plus %s is %s rupees earned." % (mon(e1), mon(e2), mon(e3), mon(earned)),
          W("e4", "%s + %s + %s = %s" % (rs(e1), rs(e2), rs(e3), rs(earned))), N("e4", rs(earned), "earned")),
        B("Now the spending: %s on %s, %s on %s and %s on %s. Together that is %s." % (
            mon(cs[0]), costs[0][0], mon(cs[1]), costs[1][0], mon(cs[2]), costs[2][0], mon(spent)),
          W("s1", "%s + %s + %s = %s" % (rs(cs[0]), rs(cs[1]), rs(cs[2]), rs(spent))), N("s1", rs(spent), "spent")),
        B("Profit is earned minus spent. %s minus %s is %s rupees." % (mon(earned), mon(spent), mon(gain)),
          ANS("a", "%s − %s = %s" % (rs(earned), rs(spent), rs(gain))), RING("a", rs(gain))),
        B("Check: profit plus spending should give back the earnings. %s plus %s is %s." % (mon(gain), mon(spent), mon(earned)),
          W("c", "%s + %s = %s" % (rs(gain), rs(spent), rs(earned)))),
        B(closing),
    )


profit(P + "14e0935f-4c1b-4524-a02b-70a5121073a8",
       "Ravi's father sells chai in 3 sizes, and pays for milk, tea leaves and sugar. We want his profit from the match.",
       [("small", 24, "12.50"), ("medium", 36, "18.75"), ("large", 20, "28.25")],
       [("milk", "485.60"), ("tea leaves", "132.40"), ("sugar", "97.50")],
       "Careful, some numbers here are just passing by. 150, 250 and 400 millilitres tell us how big the cups are. They do nothing to the money.",
       "So for profit: add up everything earned, add up everything spent, and subtract. And leave out the numbers that are not about money.")
profit(P + "e8cf72a7-2c5f-42bc-ae88-a9b4faefd474",
       "Ravi sells 3 sizes of chai on match day, and he has to buy milk, tea leaves and sugar. What is his profit for the day?",
       [("small", 24, "12.50"), ("medium", 36, "18.75"), ("large", 15, "28.00")],
       [("milk", "485.60"), ("tea leaves", "124.40"), ("sugar", "90.00")],
       "Before we start, sort the numbers. 150, 250 and 400 millilitres are cup sizes. They are not money, so we set them aside.",
       "Careful: the money earned is one of the choices, but that is not profit yet. Earned, minus spent: that is profit.")
