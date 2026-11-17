"""Imported batch 07, part a: coins, packets, three sisters, chai, boxes on both sides, savings, profit share."""
from imported_07_lib import ANS, ARC, B, BOTH, DIV, E, G, GIVEN, M, N, S, W, choose, lesson, pick, placed, tail

P = "AIGEN_grade5_"
LESSONS = {}

# ── Coins in a jar: 0.50n + 0.25(84 − n) = 31.50 ─────────────────────────────
qid = P + "87ffdf7c-3de2-4754-ae5f-b231ece8a52e"
LESSONS[qid] = lesson(
    B("Ravi's jar holds 84 coins. Some are 50 paise coins and the rest are 25 paise coins. Here is his equation, where n is the number of 50 paise coins.",
      GIVEN("q", "0.50 × n + 0.25 × (84 − n) = 31.50")),
    B("First, let's make sure we can read it. If n of the coins are 50 paise coins, how many are 25 paise coins?",
      ask=choose(["84 + n", "84 − n", "n − 84"], 1,
                 "There are 84 coins in all. Take away the n that are 50 paise coins, and the rest, 84 minus n, are the 25 paise coins.")),
    B("84 minus n: there it is, in the bracket. Now, decimals are fiddly, so let's count in paise instead. 1 rupee is 100 paise, so 31.50 rupees is 3150 paise.",
      M("q", "(84 − n)"), W("p", "31.50 × 100 = 3150")),
    B("In paise, the coins are worth 50 and 25. So the equation becomes 50 n, plus 25 times the bracket, equals 3150. Every number is whole now.",
      W("e", "50n + 25(84 − n) = 3150")),
    B("The 25 multiplies everything inside the bracket. 25 times 84 is 2100. And what about the n inside: what does the whole bracket become?",
      ARC("e", "25", ["84", ("n", 2)]), W("m", "25 × 84 = 2100"),
      ask=choose(["2100 − 25n", "2100 + 25n", "2100 − n"], 0,
                 "The 25 multiplies the 84 and the n as well. And inside the bracket the n is being taken away, so it stays taken away: 2100 minus 25 n.")),
    B("So the equation is now 50 n, plus 2100, minus 25 n, equals 3150. Careful with that minus: forget it and the answer goes astray.",
      W("e2", "50n + 2100 − 25n = 3150"), M("e2", "− 25n")),
    B("Now gather the n terms. 50 n take away 25 n leaves 25 n.",
      G("e2", ["50n", "− 25n"], "25n"), W("e3", "25n + 2100 = 3150")),
    tail(qid, "n", 25, 2100, 3150, "e3", asks=(), found="Ravi has 42 coins of 50 paise."),
    B("Let's check in paise. 42 coins of 50 paise make 2100. The other 42 coins, at 25 paise, make 1050. Together that is 3150 paise. It works.",
      W("c1", "84 − 42 = 42"), W("c2", "42 × 50 + 42 × 25 = 3150")),
    B("So for a coin puzzle: turn the money into paise, open the bracket with care, gather the letters, then undo one thing at a time."),
    check=("n", 42))

# ── Diyas in packets: 9p + 7 = 88 ────────────────────────────────────────────
qid = P + "8ba6bcc3-b2e0-4df5-bab6-3edc611d90bd"
LESSONS[qid] = lesson(
    B("Priya buys packets with 9 diyas in each, and picks up 7 loose diyas as well. At home she counts 88. We want the number of packets.",
      GIVEN("q", "9 diyas in a packet, 7 loose, 88 in all", True)),
    B("We don't know how many packets, so let's give that a letter, p. Then the packets hold 9 times p diyas. Which equation tells the whole story?",
      ask=choose(["9p − 7 = 88", "9 + 7p = 88", "9p + 7 = 88"], 2,
                 "The packets give 9 times p diyas. The 7 loose ones are extra, so they are added on. And all of that together is 88.")),
    B("9 p for the packets, plus 7 loose ones, equals 88. Careful: the 7 loose diyas were never in a packet, so they must come off before we share into 9s.",
      W("e", "9p + 7 = 88"), N("e", "9p", "in packets"), N("e", "7", "loose")),
    tail(qid, "p", 9, 7, 88, "e", found="Priya bought 9 packets."),
    B("Let's check. 9 packets of 9 is 81, and 7 loose ones make 88. It works.",
      W("c", "9 × 9 + 7 = 88")),
    B("So: give the unknown a letter, write the story as an equation, clear the extras, then divide."),
    check=("p", 9))


# ── Three people, each described from the first: x + (2x + 3) + (kx − 5) = total ──
def three(qid, first, second, third, verb, less, k, total, things, intro, given):
    coef = 3 + k
    x = (total + 2) // coef
    assert coef * x - 2 == total
    v2, v3 = 2 * x + 3, k * x - 5
    vv = ("x", x)
    eq = "x + (2x + 3) + (%dx − 5) = %d" % (k, total)
    choices, idx = placed(qid, "a1", "2x + 3", ["3x + 2", "2(x + 3)"])
    c2, i2 = placed(qid, "a2", "− 2", ["+ 8", "+ 2"])
    return lesson(
        B(intro, GIVEN("q", given, True)),
        B("Everything is described from %s's number, so let's call that x. %s %s 3 more than twice that. How do we write it?" % (first, second, verb),
          W("p", "%s = x" % first, label=True),
          ask=choose(choices, idx, "Twice %s's number is 2 x. Then 3 more means we add 3 after doubling. So %s has 2 x plus 3." % (first, second))),
        B("So %s is 2 x plus 3. %s %s 5 %s than %d times %s's number. That is %d x minus 5." % (second, third, verb, less, k, first, k),
          W("m", "%s = 2x + 3" % second, label=True), W("k", "%s = %dx − 5" % (third, k), label=True)),
        B(pick(qid, "add", ["Add the three together and we must get %d." % total,
                            "All three together make %d. So we add the three expressions." % total]),
          E("e", eq, *vv)),
        B("Gather the x terms first. x, 2 x and %d x make %d x. Now the loose numbers: plus 3 and minus 5. What do they make together?" % (k, coef),
          G("e", ["x", "2x", "%dx" % k], "%dx" % coef),
          ask=choose(c2, i2, "Start at 3 and go down 5. You pass zero and land 2 below it. So together they make minus 2.")),
        B("So the equation tidies up to %d x minus 2 equals %d." % (coef, total),
          E("e2", "%dx − 2 = %d" % (coef, total), *vv)),
        tail(qid, "x", coef, 2, total, "e2", form="ax-b", vv=vv, asks=(), final=False,
             found="%s's number is %d." % (first, x)),
        B(pick(qid, "trap", [
            "Careful, we are not finished! %d is %s's number. The question asks about %s, who has %d x minus 5." % (x, first, third, k),
            "Stop before you tick %d. That is %s's number, and the question wants %s's: %d x minus 5." % (x, first, third, k)]),
          M("k", "%dx − 5" % k)),
        B("%d times %d is %d, and %d minus 5 is %d. That is %s's number: %d %s." % (k, x, k * x, k * x, v3, third, v3, things),
          W("a0", "%d × %d = %d" % (k, x, k * x)), ANS("a", "%d − 5 = %d" % (k * x, v3)), M("a", str(v3), "circle")),
        B("Check all three. %s has %d. %s has 2 times %d, plus 3, which is %d. %s has %d. And together they make %d." % (first, x, second, x, v2, third, v3, total),
          W("c1", "2 × %d + 3 = %d" % (x, v2)), W("c2", "%d + %d + %d = %d" % (x, v2, v3, total))),
        B(pick(qid, "sum", [
            "So: one letter for the person everything is built on, an expression for each of the others, add, solve, and then answer what was really asked.",
            "The plan: call the first person's number x, write the others from it, add them up, solve, and then go back to the person the question asks about."])),
    )


LESSONS[P + "8d25c86e-b382-4c5a-a2d9-8ba2e4377d52"] = three(
    P + "8d25c86e-b382-4c5a-a2d9-8ba2e4377d52", "Priya", "Meera", "Kavya", "buys", "less", 3, 46, "packets",
    "Three sisters buy packets of rangoli powder: Priya, Meera and Kavya. Together they buy 46 packets, and we want to know how many are Kavya's.",
    "Priya + Meera + Kavya = 46 packets")

# ── Chai stall: 3x + 5x + 10 = 58 ────────────────────────────────────────────
qid = P + "8df8f0b7-eafd-41d8-942a-a32d3aa348dc"
LESSONS[qid] = lesson(
    B("Rohan sells chai at x rupees a cup: 3 cups in the morning and 5 in the evening. With a bonus of 10 rupees, he earns 58 rupees.",
      GIVEN("q", "3 cups + 5 cups at ₹x each, bonus ₹10, total ₹58", True)),
    B("The morning cups bring in 3 x, the evening cups 5 x, and the bonus is 10. Altogether that makes 58.",
      W("e", "3x + 5x + 10 = 58"), N("e", "3x", "morning"), N("e", "5x", "evening"), N("e", "10", "bonus")),
    B("3 x and 5 x are like terms: both are counting cups of chai. What do they make together?",
      ask=choose(["15x", "8x", "8"], 1,
                 "3 cups and 5 cups make 8 cups, and each cup costs x. So we add the 3 and the 5 and keep the x: 8 x.")),
    B("So 8 x plus 10 equals 58. Careful: the bonus is not chai money, so it stays as a loose 10.",
      G("e", ["3x", "5x"], "8x"), W("e2", "8x + 10 = 58")),
    tail(qid, "x", 8, 10, 58, "e2", found="One cup of chai costs 6 rupees."),
    B("Check it. 8 cups at 6 rupees is 48 rupees, and the bonus of 10 makes 58. It works.",
      W("c", "8 × 6 + 10 = 58")),
    B("So: gather the like terms first, then clear the loose number, then divide."),
    check=("x", 6))

# ── Samosas in packets with some left over: 9p + 5 = 122 ─────────────────────
qid = P + "952e2075-dc30-4bda-8004-9c9b3b8bfc97"
LESSONS[qid] = lesson(
    B("Sameer has 122 samosas. He packs them 9 to a packet, and 5 are left over. How many full packets did he make?",
      GIVEN("q", "122 samosas, 9 in a packet, 5 left over", True)),
    B("Let p be the number of full packets, so the packets hold 9 times p samosas. Where do the 5 leftover ones go in the equation?",
      ask=choose(["9p + 5 = 122", "9p − 5 = 122", "9p = 122 + 5"], 0,
                 "The 122 is everything: the samosas in packets and the 5 left over. So packets plus leftovers gives 122. That is 9 p plus 5.")),
    B("Samosas in packets, plus the 5 left over, make all 122.",
      W("e", "9p + 5 = 122"), N("e", "9p", "in packets"), N("e", "5", "left over")),
    tail(qid, "p", 9, 5, 122, "e", found="Sameer made 13 full packets."),
    B("Check: 13 packets of 9 is 117, and 5 more makes 122. Just right.",
      W("c", "13 × 9 + 5 = 122")),
    B("Notice we did not divide 122 by 9 straight away. The leftovers come off first, and then we share into packets."),
    check=("p", 13))

# ── Bangles and wrapping: 6x + 11 = 47 ───────────────────────────────────────
qid = P + "97b306a6-061a-4bfa-9733-53bfd0774c0b"
LESSONS[qid] = lesson(
    B("Ananya buys sets of bangles at 6 rupees a set, pays 11 rupees for gift wrapping, and spends 47 rupees in all. How many sets did she buy?",
      GIVEN("q", "₹6 a set, ₹11 wrapping, ₹47 in all", True)),
    B("Call the number of sets x. Then the bangles cost 6 times x rupees. Add the wrapping, and we have the whole bill.",
      W("e", "6x + 11 = 47"), N("e", "6x", "bangles"), N("e", "11", "wrapping")),
    tail(qid, "x", 6, 11, 47, "e", asks=("clear", "div"), found="Ananya bought 6 sets."),
    B("Check. 6 sets at 6 rupees is 36 rupees. Add 11 for the wrapping and we get 47. It works.",
      W("c", "6 × 6 + 11 = 47")),
    B("The wrapping is paid only once, so it comes off first. What is left is shared into sets."),
    check=("x", 6))


# ── The same boxes on both sides: 3x + 7 = 5x − 9 ────────────────────────────
def boxes(qid, a, b, item, lost, intro, given, close):
    return lesson(
        B(intro, GIVEN("q", given, True)),
        B("Let x be the number of %s in one box. %s has 3 boxes and 7 extra, so that is 3 x plus 7." % (item, a),
          W("r", "%s: 3x + 7" % a, label=True)),
        B("%s has 5 boxes but %s 9, so that is 5 x minus 9. Careful: those 9 are taken off, not added." % (b, lost),
          W("s", "%s: 5x − 9" % b, label=True), M("s", "− 9")),
        B("They end up with the same number, so the two expressions are equal.",
          W("e", "3x + 7 = 5x − 9")),
        B("Now there are x terms on both sides. Let's collect them on one side. Which is the tidy move?",
          ask=choose(["add 3x to both sides", "take 3x from both sides", "take 5x from the right only"], 1,
                     "The left has 3 x and the right has 5 x. Take the smaller lot, 3 x, from both sides. Then the left has no x at all, and the balance stays level.")),
        B("Take 3 x from both sides. The left is just 7. On the right, 5 x minus 3 x is 2 x.",
          S("e", "3x", "− 3x"), BOTH("e", "− 3x"), W("e2", "7 = 2x − 9")),
        B("Now the 2 x has 9 taken off it. What should we do about that?",
          ask=choose(["take 9 from both sides", "divide both sides by 2", "add 9 to both sides"], 2,
                     "Taking off 9 is undone by adding 9. And we add it to both sides to keep the balance level.")),
        B("Add 9 to both sides. 7 plus 9 is 16, so 16 equals 2 x.",
          S("e2", "− 9", "+ 9"), BOTH("e2", "+ 9"), W("e3", "16 = 2x")),
        B("2 x means 2 times x, so we divide both sides by 2. 16 divided by 2 is 8. Each box holds 8 %s." % item,
          DIV("e3", 2), ANS("a", "x = 8"), M("a", "x = 8", "circle")),
        B("Check both. %s: 3 times 8, plus 7, is 31. %s: 5 times 8, minus 9, is 31. The same! It works." % (a, b),
          W("c1", "3 × 8 + 7 = 31"), W("c2", "5 × 8 − 9 = 31")),
        B(close),
        check=("x", 8))


LESSONS[P + "a7380945-b88f-4d78-84dc-17a983f72493"] = boxes(
    P + "a7380945-b88f-4d78-84dc-17a983f72493", "Riya", "Ankit", "diyas", "gives away",
    "Riya buys 3 boxes of diyas and 7 loose ones. Ankit buys 5 of the same boxes but gives 9 diyas away. They end up with the same number. How many diyas are in a box?",
    "Riya: 3 boxes + 7.  Ankit: 5 boxes − 9.  Equal.",
    "When the letter is on both sides, collect it on one side first. After that it is an ordinary two step equation.")

# ── Savings each week: 18 + 7w = 67 ──────────────────────────────────────────
qid = P + "ab0824ba-a1ed-4820-85a5-c398094e7069"
LESSONS[qid] = lesson(
    B("Arjun starts with 18 rupees and earns 7 rupees every week. After some weeks he has exactly 67 rupees. How many weeks did he work?",
      GIVEN("q", "₹18 saved, ₹7 each week, ₹67 in all", True)),
    B("Let w be the number of weeks. Which equation tells Arjun's story?",
      ask=choose(["18w + 7 = 67", "18 + 7w = 67", "7w = 67 + 18"], 1,
                 "The 18 rupees is there once, from the start. The 7 rupees comes every week, so it is the 7 that is multiplied by w. Together they make 67.")),
    B("18 to start with, plus 7 for each of the w weeks, equals 67.",
      W("e", "18 + 7w = 67"), N("e", "18", "at the start"), N("e", "7w", "earned")),
    tail(qid, "w", 7, 18, 67, "e", form="b+ax", found="Arjun worked for 7 weeks."),
    B("Check. 7 weeks at 7 rupees is 49 rupees. Add the 18 he began with, and we get 67. It works.",
      W("c", "18 + 7 × 7 = 67")),
    B("Spot what happens once and what happens every week. The every week number is the one that goes with the letter."),
    check=("w", 7))

LESSONS[P + "ab3125dd-3274-4b25-8b51-26bc5a2be982"] = boxes(
    P + "ab3125dd-3274-4b25-8b51-26bc5a2be982", "Arjun", "Meera", "laddoos", "eats",
    "Arjun makes 3 boxes of laddoos and adds 7 extra. Meera makes 5 boxes but eats 9 laddoos. They end up with exactly the same number. We want x, the laddoos in a box.",
    "Arjun: 3 boxes + 7.  Meera: 5 boxes − 9.  Equal.",
    "So: write one expression for each person, set them equal, bring the x terms to one side, and then undo one thing at a time.")

# ── Piggy bank: 23 + 3x = 62 ─────────────────────────────────────────────────
qid = P + "ab461bd6-3427-4f4e-a0f2-c521b420d4cb"
LESSONS[qid] = lesson(
    B("Arjun has 23 rupees in his piggy bank. He earns x rupees a week, and after 3 weeks his savings are 62 rupees. We want x.",
      GIVEN("q", "₹23 saved, ₹x a week for 3 weeks, ₹62 in all", True)),
    B("3 weeks at x rupees a week is 3 x. Add the 23 he already had, and we get 62.",
      W("e", "23 + 3x = 62"), N("e", "23", "piggy bank"), N("e", "3x", "3 weeks")),
    tail(qid, "x", 3, 23, 62, "e", form="b+ax", asks=("clear", "div"), found="Arjun earns 13 rupees each week."),
    B("Check. 3 weeks at 13 rupees is 39 rupees. Add the 23 from the piggy bank, and we get 62. It works.",
      W("c", "23 + 3 × 13 = 62")),
    B("Notice the trap: 62 divided by 3 would share out the piggy bank money too. Take off what he already had, then share by the weeks."),
    check=("x", 13))

# ── Sharing a profit: half to charity, the rest among 3 ──────────────────────
qid = P + "ada26a73-e0f5-45f5-ae2e-3eb92022a6ad"
LESSONS[qid] = lesson(
    B("This story about Riya's diya stall is full of numbers: 12, 35, 179 and 24. Before we calculate anything, let's find out what is really being asked.",
      GIVEN("q", "Profit ₹24: half to charity, the rest shared", True)),
    B("The question is about sharing out the profit. So which number do we start from?",
      ask=choose(["179, what she earned", "24, the profit", "35, the wrapping"], 1,
                 "Read the last sentences again. She donates half her profit, and shares the rest of the profit. And the profit is given to us: 24 rupees.")),
    B("So we start from 24 rupees. Half goes to charity. Half of 24 is 12, so 12 rupees is donated and 12 rupees is left.",
      M("q", "₹24"), W("h", "24 ÷ 2 = 12"), W("r", "24 − 12 = 12")),
    B("The 12 rupees that is left is split equally among Riya herself and 2 friends. How many people share it?",
      ask=choose(["2", "3", "4"], 1, "Count Riya too. Herself and 2 friends makes 3 people.")),
    B("Careful here: it is easy to forget Riya. She and her 2 friends make 3 equal shares.",
      W("n", "1 + 2 = 3"), N("n", "1", "Riya"), N("n", "2", "friends")),
    B("12 shared among 3 is 4. Each friend gets 4 rupees.",
      ANS("a", "12 ÷ 3 = 4"), M("a", "4", "circle")),
    B("Check by building it back up. 3 shares of 4 rupees is 12, and the 12 that was donated makes 24, the whole profit.",
      W("c", "3 × 4 + 12 = 24")),
    B("And the other numbers? They fit too. 179 minus 24 leaves a cost of 155 rupees: 10 boxes at 12 rupees, plus 35 for wrapping. But we never needed them.",
      W("x1", "179 − 24 = 155"), W("x2", "10 × 12 + 35 = 155")),
    B("So read to the end before you calculate, and pick out only the numbers the question needs. Each friend gets 4 rupees."),
)

# ── Gift boxes: n + 2n + 5 = 47 ──────────────────────────────────────────────
qid = P + "b0a099f5-1f5a-4bcc-b0f9-a80714b4267a"
LESSONS[qid] = lesson(
    B("Arjun makes n gift boxes and Priya makes twice as many. There are 5 extra boxes as well, and the total is 47. We need the equation, and then n.",
      GIVEN("q", "Arjun n, Priya twice as many, 5 extra, total 47", True)),
    B("Arjun's boxes are n. How do we write Priya's, twice as many as Arjun's?",
      ask=choose(["n + 2", "2n", "2"], 1, "Twice as many means 2 times as many. And 2 times n is written 2 n.")),
    B("So the total is Arjun's n, plus Priya's 2 n, plus the 5 extra. Careful: Arjun's own boxes count too, so it is not just 2 n plus 5.",
      W("e", "n + 2n + 5 = 47"), N("e", "n", "Arjun"), N("e", "2n", "Priya"), N("e", "5", "extra")),
    B("n and 2 n are like terms. 1 lot of n and 2 lots of n make 3 lots of n.",
      G("e", ["n", "2n"], "3n"), W("e2", "3n + 5 = 47")),
    tail(qid, "n", 3, 5, 47, "e2", found="Arjun made 14 boxes."),
    B("Check. Arjun 14, Priya twice that, which is 28, and 5 extra. 14 plus 28 plus 5 is 47.",
      W("c1", "2 × 14 = 28"), W("c2", "14 + 28 + 5 = 47")),
    B("So the choice we want says n plus 2 n plus 5 equals 47, with n equal to 14. Another choice has the same equation but a different n, so always solve it yourself."),
    check=("n", 14))
