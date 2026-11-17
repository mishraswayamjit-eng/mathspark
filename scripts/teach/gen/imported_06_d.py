"""Imported batch 06, part d: two-part questions, where the equation's answer is a step on the way.

The keyed answer is not the unknown, so these lessons carry no `check`: equation lines are written
as labels (solve(..., lab=True) computes them), and every plain sum on the board is still verified.
"""
from imported_06_lib import ANS, B, BOTH, C, DIV, FIG, G, GIVEN, M, N, QID, W, ask, choose, lesson, solve

LESSONS = {}


def bars(*rows):
    return {"kind": "barModel", "bars": [
        {"label": label, "segments": [{"units": u, "label": t, "tone": tone} for u, t, tone in segs]}
        for label, segs in rows]}


# 7p + 15 = 71, then 8 packets × 3 sparklers ÷ 4 friends
q = QID("14336a8a")
LESSONS[q] = lesson(
    B("Priya buys p packets of sparklers at 7 rupees each and a 15 rupee box of diyas. The bill is 71 rupees. "
      "Each packet holds 3 sparklers, shared equally among 4 friends. How many does each friend get?",
      GIVEN("g", "p packets at ₹7 + ₹15 diyas = ₹71", True), W("g2", "3 sparklers in a packet, 4 friends", label=True)),
    B("There are two parts here. First find how many packets she bought, then share out the sparklers. "
      "For part one, which equation fits the bill?",
      ask=ask(q, "eq", "7p + 15 = 71", ["7p = 71", "7p − 15 = 71"],
              "p packets at 7 rupees each cost 7 p. The diyas cost 15 more, and the two together make the bill of 71.")),
    B("7 p for the sparklers, plus 15 for the diyas, equals 71.",
      W("e1", "7p + 15 = 71", label=True)),
    solve(q, "p", 7, "+", 15, 71, lab=True, asks=None, final=False, tail=" So Priya bought 8 packets."),
    B("But the question is not about packets. Each packet holds 3 sparklers. How do we find the number of sparklers?",
      ask=choose(["8 + 3", "8 × 3", "8 ÷ 4"], 1,
                 "8 packets with 3 sparklers in each is 8 lots of 3. So we multiply.")),
    B("8 times 3 is 24 sparklers.",
      W("s1", "8 × 3 = 24")),
    B("Shared equally among 4 friends, 24 divided by 4 is 6. Each friend gets 6 sparklers.",
      ANS("ans", "24 ÷ 4 = 6"), C("ans", "6")),
    B("Both 8 and 24 are among the choices. They are steps on the way, not the answer. "
      "Always read the last line of the question again."),
    B("Check from the end. 4 friends with 6 each is 24 sparklers, which is 8 packets of 3. "
      "And 8 packets at 7 rupees, plus 15, is 71.",
      W("c1", "7 × 8 + 15 = 71")),
    B("Solve the equation for the packets, then keep going: packets to sparklers, sparklers to friends."),
)

# 5x − 18 = 57, then 3 × 15 − 10
q = QID("3816815d")
LESSONS[q] = lesson(
    B("Riya sells chai at x rupees a cup. On Saturday she sold 5 cups, spent 18 rupees, and made 57 rupees profit. "
      "On Sunday she sold 3 cups and spent 10. What was Sunday's profit?",
      GIVEN("g", "Sat: 5 cups − ₹18 = ₹57 profit", True), W("g2", "Sun: 3 cups − ₹10 = ?", label=True)),
    B("We cannot work out Sunday yet, because we do not know the price of a cup. Saturday can tell us: "
      "5 cups at x rupees, minus 18 for ingredients, left 57.",
      W("e1", "5x − 18 = 57", label=True)),
    solve(q, "x", 5, "−", 18, 57, lab=True, asks="undo", final=False, tail=" A cup of chai costs 15 rupees."),
    B("Now Sunday. She sold 3 cups and spent 10 rupees on ingredients. Which sum gives her profit?",
      ask=choose(["3 × 15", "3 × 15 + 10", "3 × 15 − 10"], 2,
                 "3 cups bring in 3 times 15. But the 10 rupees for ingredients has to come out of that, so we subtract it.")),
    B("3 times 15 is 45. Take away 10, and Sunday's profit is 35 rupees.",
      W("s1", "3 × 15 = 45"), ANS("ans", "45 − 10 = 35"), C("ans", "35")),
    B("45 is among the choices, but that is only the money she took in. Profit is what is left after the costs."),
    B("Check Saturday with our price: 5 times 15 is 75, and 75 minus 18 is 57. It matches.",
      W("c1", "5 × 15 − 18 = 57")),
    B("Use the day you know everything about to find the price. Then use that price on the other day."),
)

# x + (3x − 14) = 146, then 2 × 40 + 18
q = QID("442117ae")
LESSONS[q] = lesson(
    B("Team Rockets scored some runs in their first innings. Their second innings was 3 times that, minus 14, "
      "and the two innings total 146. Team Blazers scored 2 times the Rockets' first innings, plus 18.",
      GIVEN("g", "Rockets: first + (3 × first − 14) = 146", True), W("g2", "Blazers = 2 × first + 18", label=True)),
    B("Let x be the Rockets' first innings. Their second innings is 3 x minus 14. The two together make 146.",
      W("e0", "x + 3x − 14 = 146", label=True)),
    B("x and 3 x are like terms. What do they make together?",
      ask=choose(["3x", "4x", "4"], 1,
                 "x on its own means 1 x. And 1 x plus 3 x is 4 x.")),
    B("So 4 x, minus 14, equals 146.",
      G("e0", ["x", "3x"], "4x"), W("e1", "4x − 14 = 146", label=True)),
    solve(q, "x", 4, "−", 14, 146, lab=True, asks=None, final=False, tail=" The Rockets made 40 in their first innings."),
    B("But read the question again: it asks for the Blazers' score. That is 2 times the Rockets' first innings, plus 18.",
      W("b", "Blazers = 2 × 40 + 18", label=True)),
    B("2 times 40 is 80, and 80 plus 18 is 98 runs.",
      W("s1", "2 × 40 = 80"), ANS("ans", "80 + 18 = 98"), C("ans", "98")),
    B("Check the Rockets. Their second innings is 3 times 40, minus 14, which is 106. And 40 plus 106 is 146.",
      W("c1", "3 × 40 − 14 = 106"), W("c2", "40 + 106 = 146")),
    B("Find x first, but do not stop there. Go back to the question and work out exactly what it asked for."),
)

# Together ₹125, each gets ₹10 more: the total needs no x
q = QID("4b0b023c")
LESSONS[q] = lesson(
    B("Priya has saved x rupees. Arjun has 3 times that, minus 15. Together they have exactly 125 rupees. "
      "Then grandmother gives each of them 10 rupees. How much do they have together now?",
      GIVEN("g", "Together: ₹125. Grandmother gives ₹10 to each", True)),
    B("Read the last question carefully. To find the new total, what do we need to know?",
      ask=choose(["Priya's savings, x", "the old total and the gifts", "Arjun's savings"], 1,
                 "The question asks what they have together. We already know the old total, 125. "
                 "We only need to add the gift money.")),
    B("Here is a surprise: we do not need to solve for x at all. The story already tells us they had 125 rupees together.",
      M("g", "₹125", "box")),
    B("Grandmother gives 10 rupees to each of them. How much gift money is that in all?",
      ask=choose(["10", "20", "30"], 1,
                 "Each means both children get 10. Priya gets 10 and Arjun gets 10, so that is 20 in all.")),
    B("10 for Priya and 10 for Arjun makes 20.",
      W("s1", "10 + 10 = 20")),
    B("125 plus 20 is 145 rupees.",
      ANS("ans", "125 + 20 = 145"), C("ans", "145")),
    B("Shall we check by finding x anyway? Priya's x and Arjun's 3 x minus 15 make 4 x minus 15, and that equals 125.",
      W("e1", "4x − 15 = 125", label=True)),
    B("Add 15 to both sides: 4 x is 140. Divide by 4: x is 35. So Priya has 35, and Arjun has 3 times 35, minus 15, which is 90.",
      BOTH("e1", "+ 15"), W("e2", "4x = 140", label=True), W("e3", "x = 35", label=True), W("c1", "3 × 35 − 15 = 90")),
    B("After the gifts they have 45 and 100. And 45 plus 100 is 145, the same answer.",
      W("c2", "35 + 10 = 45"), W("c3", "90 + 10 = 100"), W("c4", "45 + 100 = 145")),
    B("Before you solve anything, ask what the question really wants. Here it was the total, and only the gifts changed it."),
)

# 25x + 15(2x) = 825, then cups, cost and profit
q = QID("506761a8")
LESSONS[q] = lesson(
    B("Priya sells regular chai at 15 rupees and masala chai at 25 rupees. She sold twice as many regular cups as masala, "
      "and earned 825 rupees. Ingredients cost 3 rupees for every cup. What was her profit?",
      GIVEN("g", "Regular ₹15, masala ₹25. Regular cups = 2 × masala", True),
      W("g2", "Earned ₹825. Ingredients ₹3 a cup", label=True)),
    B("Let x be the number of masala cups. Then she sold 2 x regular cups. Masala brings in 25 x, "
      "and regular brings in 15 times 2 x.",
      W("e0", "25x + 15 × 2x = 825", label=True)),
    B("What is 15 times 2 x?",
      ask=choose(["17x", "30x", "15x"], 1,
                 "15 times 2 is 30. So 15 lots of 2 x make 30 x.")),
    B("25 x plus 30 x is 55 x. So 55 x equals 825.",
      W("e1", "25x + 30x = 825", label=True), W("e2", "55x = 825", label=True)),
    B("Divide both sides by 55. 55 times 10 is 550, and 55 times 5 is 275. Together that is 825, so x is 15.",
      DIV("e2", 55), W("d1", "550 + 275 = 825"), W("d2", "55 × 15 = 825"), W("e3", "x = 15", label=True)),
    B("So she sold 15 masala cups, and twice as many regular cups, 30. That is 45 cups altogether.",
      W("s1", "2 × 15 = 30"), W("s2", "15 + 30 = 45")),
    B("Ingredients cost 3 rupees for every cup. Which number do we multiply by 3?",
      ask=choose(["15, the masala cups", "45, all the cups", "825, the earnings"], 1,
                 "The question says every cup she sold, both types. That is all 45 cups.")),
    B("45 times 3 is 135 rupees spent on ingredients.",
      W("s3", "45 × 3 = 135")),
    B("Profit is earnings minus costs. 825 minus 135 is 690 rupees.",
      ANS("ans", "825 − 135 = 690"), C("ans", "690")),
    B("Check the earnings. 15 masala cups at 25 rupees is 375. 30 regular cups at 15 rupees is 450. And 375 plus 450 is 825.",
      W("c1", "15 × 25 = 375"), W("c2", "30 × 15 = 450"), W("c3", "375 + 450 = 825")),
    B("This one is a chain: an equation for the cups, then the total cups, then the cost, then the profit. "
      "Take one link at a time."),
)

# n + (2n + 3) + (3n − 5) = 58, then row 2
q = QID("5906edac")
LESSONS[q] = lesson(
    B("Riya lays diyas in 3 rows. Row 1 has n. Row 2 has 3 more than double row 1. Row 3 has 5 less than triple row 1. "
      "There are 58 diyas in all. How many are in row 2?",
      GIVEN("g", "3 rows of diyas, 58 in all. Row 2 = ?", True)),
    B("Row 1 is n. Row 2 is 3 more than double that: 2 n plus 3.",
      W("r1", "Row 1 = n", label=True), W("r2", "Row 2 = 2n + 3", label=True)),
    B("Row 3 has 5 less than triple row 1. How do we write that?",
      ask=choose(["5 − 3n", "3n − 5", "3(n − 5)"], 1,
                 "Triple row 1 is 3 n. 5 less than that means we take 5 away from it. So it is 3 n minus 5.")),
    B("So row 3 is 3 n minus 5. Add the 3 rows and we get 58.",
      W("r3", "Row 3 = 3n − 5", label=True), W("e0", "n + 2n + 3 + 3n − 5 = 58", label=True)),
    B("Gather like terms. n, 2 n and 3 n make 6 n. Plus 3 and minus 5 make minus 2.",
      G("e0", ["n", "2n", "3n"], "6n"), G("e0", ["3", "5"], "− 2"), W("e1", "6n − 2 = 58", label=True)),
    solve(q, "n", 6, "−", 2, 58, lab=True, asks="div", final=False, tail=" So row 1 has 10 diyas."),
    B("The question asks for row 2: double 10, plus 3. That is 23 diyas.",
      M("r2", "2n + 3"), ANS("ans", "2 × 10 + 3 = 23"), C("ans", "23")),
    B("Check: row 3 is 3 times 10, minus 5, which is 25. And 10 plus 23 plus 25 is 58.",
      W("c1", "3 × 10 − 5 = 25"), W("c2", "10 + 23 + 25 = 58")),
    B("Notice 25 is among the choices: that is row 3. Find n first, then go back and work out the row you were asked for."),
)

# 3x + 5 = 47, then 5 × 14 + 5
q = QID("5af03536")
LESSONS[q] = lesson(
    B("Ravi charges x rupees for a samosa and 5 rupees for a paper plate. On Monday, 3 samosas on a plate cost 47 rupees. "
      "On Tuesday a customer buys 5 samosas on a plate. What does that cost?",
      GIVEN("g", "Mon: 3 samosas + ₹5 plate = ₹47", True), W("g2", "Tue: 5 samosas + ₹5 plate = ?", label=True)),
    B("Monday tells us the price. 3 samosas at x rupees, plus 5 for the plate, came to 47.",
      W("e1", "3x + 5 = 47", label=True)),
    solve(q, "x", 3, "+", 5, 47, lab=True, asks="undo", final=False, tail=" One samosa costs 14 rupees."),
    B("Now Tuesday: 5 samosas on one plate. Which sum gives the bill?",
      ask=choose(["5 × 14", "5 × 14 + 5", "5 × 14 + 5 × 5"], 1,
                 "5 samosas cost 5 times 14. The plate is charged as well, but there is only one plate, "
                 "so we add 5 just once.")),
    B("5 times 14 is 70, and 70 plus 5 for the plate is 75 rupees.",
      W("s1", "5 × 14 = 70"), ANS("ans", "70 + 5 = 75"), C("ans", "75")),
    B("Here is a neat check. Tuesday has 2 more samosas than Monday. 2 times 14 is 28, and 47 plus 28 is 75.",
      W("c1", "2 × 14 = 28"), W("c2", "47 + 28 = 75")),
    B("Use the bill you know to find the price of one. Then build the new bill, and don't forget the plate."),
)

# 250 coins of ₹0.50 and ₹2.50 worth ₹225; half of the ₹2.50 coins
q = QID("5c85edaa")
LESSONS[q] = lesson(
    B("Ravi's jar has 250 coins. Some are 50 paise coins and the rest are 2 rupees 50 paise coins, worth 225 rupees in all. "
      "Priya has half as many of the bigger coins as Ravi. What are hers worth?",
      GIVEN("g", "250 coins: ₹0.50 and ₹2.50. Total value ₹225", True), W("g2", "₹0.50 = 50 paise", label=True)),
    B("First we need Ravi's bigger coins. Imagine every one of the 250 coins is a small one. "
      "At half a rupee each, the jar would hold 125 rupees.",
      W("s1", "250 × 0.50 = 125")),
    B("But the jar really holds 225 rupees. How much more is that than our imagined jar?",
      ask=choose(["100", "125", "350"], 0,
                 "The real jar holds 225 and the imagined one holds 125. The gap is 225 minus 125, which is 100 rupees.")),
    B("225 minus 125 is 100. That extra 100 rupees must come from the bigger coins.",
      W("s2", "225 − 125 = 100")),
    B("Each time a small coin is swapped for a bigger one, the jar gains 2 rupees. "
      "So if there are n bigger coins, 2 n equals 100.",
      W("s3", "2.50 − 0.50 = 2"), W("e1", "2n = 100", label=True)),
    B("Divide both sides by 2, and n is 50. Ravi has 50 of the bigger coins.",
      DIV("e1", 2), W("e2", "n = 50", label=True)),
    B("Priya has half as many of these coins as Ravi. How many is that?",
      ask=choose(["25", "100", "125"], 0,
                 "Half as many means divide by 2. Ravi has 50, so Priya has 50 divided by 2, which is 25.")),
    B("50 divided by 2 is 25 coins for Priya.",
      W("s4", "50 ÷ 2 = 25")),
    B("Now their value. 25 coins at 2 rupees is 50 rupees. And 25 half rupees make 12 rupees 50 paise.",
      W("s5", "25 × 2 = 50"), W("s6", "25 × 0.50 = 12.50"), N("s6", "12.50", "12 rupees 50 paise")),
    B("50 rupees and 12 rupees 50 paise make 62 rupees 50 paise. That is what Priya's coins are worth.",
      ANS("ans", "50 + 12.50 = 62.50"), N("ans", "62.50", "62 rupees 50 paise"), C("ans", "62.50")),
    B("Careful: 125 rupees is among the choices. That is what Ravi's 50 bigger coins are worth, not Priya's 25.",
      W("t", "50 × 2.50 = 125")),
    B("Check the jar. Ravi's 50 bigger coins are worth 125 rupees. The other 200 coins are worth 100 rupees. "
      "And 125 plus 100 is 225.",
      W("c1", "250 − 50 = 200"), W("c2", "200 × 0.50 = 100"), W("c3", "125 + 100 = 225")),
    B("Pretend all the coins are the small kind, see how much value is missing, and let the bigger coins fill the gap."),
)

# x + 3x = 48, then 36 × 12
q = QID("622c90aa")
LESSONS[q] = lesson(
    B("Ananya sells 3 times as many samosas as Rohan. Together they sell 48, and each samosa costs 12 rupees. "
      "How much money did Ananya earn?",
      GIVEN("g", "Ananya = 3 × Rohan. Together 48 samosas. ₹12 each", True)),
    B("Samosas first, money later. Let Rohan sell x samosas. Then Ananya sells 3 x.",
      FIG("f1", bars(("Rohan", [(2, "x", "a")]), ("Ananya", [(2, "x", "b"), (2, "x", "b"), (2, "x", "b")]))),
      W("d", "Rohan = x,  Ananya = 3x", label=True)),
    B("Together they sold 48. How many x is that?",
      ask=choose(["3x", "4x", "2x"], 1,
                 "Count Rohan's share as well. His x and Ananya's 3 x make 4 x. You can count 4 boxes in the bars.")),
    B("So 4 x equals 48. Divide both sides by 4, and x is 12. Rohan sold 12 samosas.",
      W("e1", "4x = 48", label=True), DIV("e1", 4), W("e2", "x = 12", label=True)),
    B("Ananya sold 3 times as many. 3 times 12 is 36 samosas.",
      W("s1", "3 × 12 = 36")),
    B("Each samosa sells for 12 rupees. Whose samosas do we multiply by 12?",
      ask=choose(["Rohan's 12", "all 48", "Ananya's 36"], 2,
                 "The question asks what Ananya earned. So we use her 36 samosas, not Rohan's and not the total.")),
    B("36 times 12. 36 times 10 is 360, and 36 times 2 is 72. Together that is 432 rupees.",
      W("s2", "36 × 10 = 360"), W("s3", "36 × 2 = 72"), ANS("ans", "36 × 12 = 432"), C("ans", "432")),
    B("Check with the whole stall. 48 samosas at 12 rupees is 576. Rohan earned 12 times 12, which is 144. "
      "And 432 plus 144 is 576.",
      W("c1", "48 × 12 = 576"), W("c2", "12 × 12 = 144"), W("c3", "432 + 144 = 576")),
    B("Mind the two 12s here: one is Rohan's samosas, the other is the price. Find the shares first, "
      "then turn the right share into money."),
)

# 8h + 7 = 71, then 5 × 8
q = QID("639db56c")
LESSONS[q] = lesson(
    B("Arjun packs 3 boxes an hour and Meera packs 5 an hour. 7 boxes were ready before they began. "
      "After h hours of working together there are 71 boxes. How many did Meera pack?",
      GIVEN("g", "Arjun 3 an hour, Meera 5 an hour. 7 ready. Total 71", True)),
    B("Each hour, how many boxes do the two of them pack together?",
      ask=choose(["2", "8", "15"], 1,
                 "Arjun packs 3 and Meera packs 5 in the same hour. Together that is 3 plus 5, which is 8.")),
    B("8 boxes an hour, so 8 h boxes in h hours. Add the 7 that were ready, and we get 71.",
      W("s0", "3 + 5 = 8"), W("e1", "8h + 7 = 71", label=True)),
    solve(q, "h", 8, "+", 7, 71, lab=True, asks=None, final=False, tail=" They worked for 8 hours."),
    B("The question asks how many boxes Meera packed. Which sum is that?",
      ask=choose(["8 × 8", "3 × 8", "5 × 8"], 2,
                 "Meera packs 5 boxes every hour, and she worked for 8 hours. So it is 5 times 8.")),
    B("5 times 8 is 40. Meera packed 40 boxes.",
      ANS("ans", "5 × 8 = 40"), C("ans", "40")),
    B("Check: Arjun packed 3 times 8, which is 24. Then 24 plus 40, plus the 7 ready ones, is 71.",
      W("c1", "3 × 8 = 24"), W("c2", "24 + 40 + 7 = 71")),
    B("Find the hours from the total, then use Meera's own 5 an hour. The answer to the equation is not always "
      "the answer to the question."),
)

# (3x + 10) + (2x − 5) + (x + 20) + (4x − 15) = 310, then 4x − 15
q = QID("6c260ddc")
LESSONS[q] = lesson(
    B("Team India's runs in 4 innings are written using x, and the total is 310. We must find x, "
      "and then the runs in the 4th innings, which is 4 x minus 15.",
      GIVEN("g", "(3x + 10) + (2x − 5) + (x + 20) + (4x − 15) = 310", True)),
    B("Gather the x terms first: 3 x, 2 x, x and 4 x. How many x is that altogether?",
      G("g", ["3x", "2x", ("x", 3), "4x"], "x terms"),
      ask=choose(["9x", "10x", "24x"], 1,
                 "Don't miss the x standing alone: it counts as 1 x. 3 and 2 and 1 and 4 make 10.")),
    B("Now the plain numbers, one step at a time. 10 minus 5 is 5. Add 20 to get 25. Take away 15, and 10 is left.",
      W("s1", "10 − 5 = 5"), W("s2", "5 + 20 = 25"), W("s3", "25 − 15 = 10")),
    B("So the whole equation is 10 x, plus 10, equals 310.",
      W("e1", "10x + 10 = 310", label=True)),
    solve(q, "x", 10, "+", 10, 310, lab=True, asks=None, final=False, tail=" So x is 30."),
    B("We have found x. Are we finished?",
      ask=choose(["Yes, the answer is 30", "No, put x into 4x − 15"], 1,
                 "Here x is only a helper. The question asks for the runs in the 4th innings, and that is 4 x minus 15.")),
    B("4 times 30 is 120, and 120 minus 15 is 105 runs.",
      M("g", "(4x − 15)", "box"), W("s4", "4 × 30 = 120"), ANS("ans", "120 − 15 = 105"), C("ans", "105")),
    B("Check all 4 innings with x as 30: they come to 100, 55, 50 and 105. Add them up and we get 310.",
      W("c1", "3 × 30 + 10 = 100"), W("c2", "2 × 30 − 5 = 55"), W("c3", "30 + 20 = 50"), W("c4", "100 + 55 + 50 + 105 = 310")),
    B("120 is among the choices: that is 4 x with the minus 15 forgotten. Gather, solve, "
      "then put x back into the part you were asked for."),
)
