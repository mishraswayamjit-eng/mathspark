"""Imported batch 06, part c: equations that need a step before the usual two (like terms, a bracket,
a cost to work out first, x on both sides), and the three whose answer is an equation with its value."""
from imported_06_lib import ANS, ARC, B, BOTH, C, DIV, FIG, G, GIVEN, M, N, QID, S, W, ask, choose, lesson, solve

LESSONS = {}


def bars(*rows):
    """A bar model: each row is (label, [(units, text, tone), ...])."""
    return {"kind": "barModel", "bars": [
        {"label": label, "segments": [{"units": u, "label": t, "tone": tone} for u, t, tone in segs]}
        for label, segs in rows]}


# 12x + 33 − 9 = 120
q = QID("0234cf63")
LESSONS[q] = lesson(
    B("Neha buys x notebooks at 12 rupees each and a 33 rupee pack of stickers. Her mother's discount takes 9 rupees off, "
      "and she pays 120. How many notebooks?",
      GIVEN("g", "x notebooks at ₹12 + ₹33 stickers − ₹9 off = ₹120", True)),
    B("A discount of 9 rupees. Does that go on to the bill, or come off it?",
      ask=choose(["it goes on: + 9", "it comes off: − 9"], 1,
                 "A discount makes the bill smaller. So the 9 rupees is taken away from what she would have paid.")),
    B("So: 12 x for the notebooks, plus 33 for stickers, minus the 9 discount, equals 120.",
      W("e0", "12x + 33 − 9 = 120")),
    B("Tidy the plain numbers first. 33 minus 9 is 24.",
      G("e0", ["33", "9"], "24"), W("e1", "12x + 24 = 120")),
    solve(q, "x", 12, "+", 24, 120, asks="undo", tail=" Neha bought 8 notebooks."),
    B("Check: 8 notebooks at 12 rupees is 96. Add 33 for stickers to get 129, take off the 9 discount, and she pays 120.",
      W("c1", "8 × 12 = 96"), W("c2", "96 + 33 = 129"), W("c3", "129 − 9 = 120")),
    B("When a bill has several plain numbers, tidy them into one first. Then undo the plus, and undo the times."),
    check=("x", 8))

# 3n + 7 = 34 (the equation is given)
q = QID("1144268b")
LESSONS[q] = lesson(
    B("Meera's petals give us an equation: 3 n, plus 7, equals 34. The n is the number she started with.",
      GIVEN("e1", "3n + 7 = 34")),
    B("Think how the 34 was made: start with n, multiply by 3, then add 7. To get back to n, we undo those steps "
      "in reverse order, last one first.",
      N("e1", "3n", "first: times 3"), N("e1", "+ 7", "then: plus 7")),
    solve(q, "n", 3, "+", 7, 34, asks="both", tail=" So n is 9."),
    B("Check: 3 times 9 is 27, and 27 plus 7 is 34. It matches.",
      W("c1", "3 × 9 + 7 = 34")),
    B("Always undo in reverse order: first the plus 7, then the times 3. Dividing 34 by 3 at the start would not work."),
    check=("n", 9))

# (3x + 15) + (5x − 25) = 110
q = QID("172ba01e")
LESSONS[q] = lesson(
    B("Riya sells stickers at x rupees each. Saturday: 3 stickers, plus 15 rupees in tips. Sunday: 5 stickers, "
      "but she spends 25 on supplies. After both days she has 110 rupees.",
      GIVEN("g", "Sat: 3 stickers + ₹15. Sun: 5 stickers − ₹25. Total ₹110", True)),
    B("Saturday is 3 x plus 15. Sunday is 5 x minus 25. Put the two days together and they make 110.",
      W("e0", "3x + 15 + 5x − 25 = 110")),
    B("Let's gather like terms. 3 x and 5 x make 8 x. What do plus 15 and minus 25 make together?",
      G("e0", ["3x", "5x"], "8x"),
      ask=choose(["+ 10", "− 10", "+ 40"], 1,
                 "She gained 15 and then spent 25. Spending more than you gained leaves you 10 down. "
                 "So together they make minus 10.")),
    B("So the equation is 8 x, minus 10, equals 110.",
      G("e0", ["15", "25"], "− 10"), W("e1", "8x − 10 = 110")),
    solve(q, "x", 8, "−", 10, 110, asks="div", tail=" One sticker costs 15 rupees."),
    B("Check: Saturday is 3 times 15, plus 15, which is 60. Sunday is 5 times 15, minus 25, which is 50. And 60 plus 50 is 110.",
      W("c1", "3 × 15 + 15 = 60"), W("c2", "5 × 15 − 25 = 50"), W("c3", "60 + 50 = 110")),
    B("Write each day using x, gather the like terms, then solve. Watch the signs as you gather: money spent is a minus."),
    check=("x", 15))

# 3n + 35 = 98, so n = 21
q = QID("1cf27d7b")
LESSONS[q] = lesson(
    B("Riya has 35 rupees in her piggy bank. She earns n rupees a week, and after 3 weeks she has 98 rupees. "
      "We need the equation, and the value of n.",
      GIVEN("g", "₹35 saved + ₹n a week for 3 weeks = ₹98", True)),
    B("Which equation fits the story?",
      ask=ask(q, "eq", "3n + 35 = 98", ["3n − 35 = 98", "n + 35 = 98"],
              "She earns n rupees in each of 3 weeks, which is 3 n. That is added to the 35 she already has, to make 98.")),
    B("3 n earned, plus the 35 she started with, equals 98.",
      W("e1", "3n + 35 = 98"), N("e1", "3n", "3 weeks' pay"), N("e1", "35", "piggy bank")),
    solve(q, "n", 3, "+", 35, 98, asks="undo", final=False, tail=" Riya earns 21 rupees a week."),
    B("So the answer has two parts: the equation 3 n plus 35 equals 98, and n equals 21.",
      ANS("ans", "3n + 35 = 98, so n = 21", True), C("ans", "n = 21")),
    B("One of the choices has the right equation but says n is 31. Test it: 3 times 31 is 93, and adding 35 goes well past 98.",
      W("t", "3 × 31 = 93")),
    B("Ours passes the test: 3 times 21 is 63, and 63 plus 35 is 98.",
      W("c1", "3 × 21 + 35 = 98")),
    B("When the choices give an equation and a value, check both. The equation must fit the story, "
      "and the value must make it true."),
    check=("n", 21))

# 12x + 35 + 20 = 175 − 24
q = QID("20c89c9f")
LESSONS[q] = lesson(
    B("Riya buys x packets of tea at 12 rupees each, and spends 35 on sugar and 20 on milk. She earns 175 rupees "
      "and makes 24 rupees profit. How many packets did she buy?",
      GIVEN("g", "x packets at ₹12 + ₹35 + ₹20. Earned ₹175, profit ₹24", True)),
    B("Profit is what she earned, minus what she spent. So how much did Riya spend in all?",
      ask=choose(["175 + 24", "175 − 24", "175"], 1,
                 "She earned 175 and kept 24 of it as profit. The rest went on costs. So her spending is 175 minus 24.")),
    B("175 minus 24 is 151. So everything she bought cost 151 rupees.",
      W("p1", "175 − 24 = 151")),
    B("Now the shopping list: 12 x for tea, 35 for sugar and 20 for milk. Together they come to 151.",
      W("e0", "12x + 35 + 20 = 151")),
    B("Sugar and milk together: 35 plus 20 is 55.",
      G("e0", ["35", "20"], "55"), W("e1", "12x + 55 = 151")),
    solve(q, "x", 12, "+", 55, 151, asks="div", tail=" She bought 8 packets of tea leaves."),
    B("Check: 8 packets at 12 rupees is 96. Add 35 and 20 to get 151. And 175 minus 151 leaves the 24 profit.",
      W("c1", "8 × 12 + 35 + 20 = 151"), W("c2", "175 − 151 = 24")),
    B("Find the total cost first, from the earnings and the profit. Then the equation is an ordinary two-step one."),
    check=("x", 8))

# 32 + 7x − 15 = 150
q = QID("22072f4d")
LESSONS[q] = lesson(
    B("Vikram has 32 rupees. He earns the same amount each week for 7 weeks, then spends 15 on a ball, and has 150 left. "
      "How much does he earn in a week? Call it x.",
      GIVEN("g", "₹32 saved + 7 weeks' pay − ₹15 ball = ₹150", True)),
    B("Which equation follows his money through the story?",
      ask=ask(q, "eq", "32 + 7x − 15 = 150", ["32 + 7x + 15 = 150", "32 + x − 15 = 150"],
              "Earning x rupees for 7 weeks adds 7 x. Buying the ball takes money away, so the 15 is subtracted.")),
    B("He starts with 32, earns 7 x, spends 15, and ends with 150.",
      W("e0", "32 + 7x − 15 = 150")),
    B("Tidy the plain numbers first: 32 minus 15 is 17.",
      G("e0", ["32", "15"], "17"), W("e1", "17 + 7x = 150")),
    solve(q, "x", 7, "+", 17, 150, const_first=True, asks="undo", tail=" Vikram earns 19 rupees a week."),
    B("Check: 7 weeks at 19 rupees is 133. With his 32 that makes 165, and after the 15 rupee ball, 150 is left.",
      W("c1", "32 + 133 = 165"), W("c2", "165 − 15 = 150")),
    B("Follow the money in order to write the equation. Then tidy the plain numbers, undo the plus, and undo the times."),
    check=("x", 19))

# x + 2x + 7 = 43
q = QID("2e8eddbc")
LESSONS[q] = lesson(
    B("Meera squeezes some glasses of orange juice, and twice as many of lemonade. Kiran brings 7 more glasses of lemonade. "
      "There are 43 glasses in all. How many are orange juice?",
      GIVEN("g", "orange + lemonade (twice as many, + 7) = 43 glasses", True)),
    B("Let the orange juice be x glasses. Meera's lemonade is twice that, 2 x, and Kiran adds 7. Altogether, 43.",
      FIG("f1", bars(("orange", [(2, "x", "a")]), ("lemonade", [(2, "x", "b"), (2, "x", "b"), (1, "7", "c")]))),
      W("e0", "x + 2x + 7 = 43")),
    B("x and 2 x are like terms. What do they make together?",
      ask=choose(["2x", "3x", "3"], 1,
                 "x on its own means 1 x. And 1 x plus 2 x is 3 x. Look at the bars: there are 3 boxes marked x.")),
    B("So 3 x, plus 7, equals 43.",
      G("e0", ["x", "2x"], "3x"), W("e1", "3x + 7 = 43")),
    solve(q, "x", 3, "+", 7, 43, asks=None, tail=" Meera squeezed 12 glasses of orange juice."),
    B("Check: 12 glasses of orange. Lemonade is 2 times 12, plus 7, which is 31. And 12 plus 31 is 43.",
      W("c1", "2 × 12 + 7 = 31"), W("c2", "12 + 31 = 43")),
    B("One choice is 18. That comes from sharing the 36 between only 2, forgetting that the orange juice is one of the 3 shares.",
      W("t", "36 ÷ 2 = 18")),
    B("Call the smallest amount x, write everything else using x, gather the like terms, and solve."),
    check=("x", 12))

# (5x − 12) + (3x − 8) = 60
q = QID("41d6f1df")
LESSONS[q] = lesson(
    B("Meena sells samosas at x rupees each. Her profit on day 1 was 5 x minus 12, and on day 2 it was 3 x minus 8. "
      "Together the profit was 60 rupees. Let's find x.",
      GIVEN("e0", "(5x − 12) + (3x − 8) = 60")),
    B("Gather the like terms. First the x terms: 5 x and 3 x make 8 x.",
      G("e0", ["5x", "3x"], "8x")),
    B("Now the plain numbers: minus 12 and minus 8. What do they make together?",
      ask=choose(["− 4", "− 20", "+ 20"], 1,
                 "She spent 12 on day 1 and 8 more on day 2. Both are money going out, so together she spent 20. "
                 "That is minus 20.")),
    B("So the equation is 8 x, minus 20, equals 60.",
      G("e0", ["12", "8"], "− 20"), W("e1", "8x − 20 = 60")),
    solve(q, "x", 8, "−", 20, 60, asks="div", tail=" One samosa costs 10 rupees."),
    B("Check: day 1 is 5 times 10, minus 12, which is 38. Day 2 is 3 times 10, minus 8, which is 22. And 38 plus 22 is 60.",
      W("c1", "5 × 10 − 12 = 38"), W("c2", "3 × 10 − 8 = 22"), W("c3", "38 + 22 = 60")),
    B("Gather the x terms, gather the plain numbers with their signs, then solve the short equation that is left."),
    check=("x", 10))

# x + 3x = 52 (with a distracting 47)
q = QID("4db3b22f")
LESSONS[q] = lesson(
    B("This story has a number that is only there to distract us: mother's 47 coins are separate. What matters is that "
      "Rohan has 3 times as many coins as Kavya, and together they have 52.",
      GIVEN("g", "Rohan = 3 × Kavya. Together: 52 coins", True)),
    B("Let Kavya have x coins. Then Rohan has 3 x. Picture it as bars: one box for Kavya, and 3 for Rohan.",
      FIG("f1", bars(("Kavya", [(2, "x", "a")]), ("Rohan", [(2, "x", "b"), (2, "x", "b"), (2, "x", "b")]))),
      W("d", "Kavya = x,  Rohan = 3x", label=True)),
    B("Together they have 52 coins. So what equals 52?",
      ask=choose(["3x", "4x", "x + 3"], 1,
                 "Count Kavya's coins too. Her x, and Rohan's 3 x, make 4 x altogether.")),
    B("x plus 3 x is 4 x. So 4 x equals 52.",
      W("e0", "x + 3x = 52"), W("e1", "4x = 52")),
    B("4 x means 4 times x, so we divide both sides by 4. 52 divided by 4 is 13. Kavya has 13 coins.",
      DIV("e1", 4), ANS("ans", "x = 13"), C("ans", "x = 13")),
    B("Careful: 39 is among the choices. That is Rohan's share, 3 times 13. The question asks for Kavya's.",
      W("t", "3 × 13 = 39")),
    B("Check: 13 plus 39 is 52. And 52 is 5 more than mother's 47, just as the story says.",
      W("c1", "13 + 39 = 52"), W("c2", "47 + 5 = 52")),
    B("Pick out the facts you need, call the smaller share x, and count how many x make the total."),
    check=("x", 13))

# 12s − 120 = 168; s = 24
q = QID("51111ef2")
LESSONS[q] = lesson(
    B("Arjun sells s samosas at 12 rupees each. He spent 75 rupees on ingredients and 45 on plates, and his profit was "
      "168 rupees. We need the equation, and s.",
      GIVEN("g", "s samosas at ₹12. Costs ₹75 + ₹45. Profit ₹168", True)),
    B("First, his costs. 75 for ingredients and 45 for plates is 120 rupees in all.",
      W("p1", "75 + 45 = 120")),
    B("Profit is the money taken in, minus the costs. Which equation fits?",
      ask=ask(q, "eq", "12s − 120 = 168", ["12s + 120 = 168", "12s − 75 = 168"],
              "Selling s samosas brings in 12 s. Both costs, 120 together, come out of that. What is left is the profit, 168.")),
    B("12 s comes in, 120 goes out, and 168 is the profit.",
      W("e1", "12s − 120 = 168"), N("e1", "12s", "money in"), N("e1", "120", "costs")),
    solve(q, "s", 12, "−", 120, 168, asks=None, final=False, tail=" Arjun sold 24 samosas."),
    B("So the answer is the equation 12 s minus 120 equals 168, with s equal to 24.",
      ANS("ans", "12s − 120 = 168, so s = 24", True), C("ans", "s = 24")),
    B("One choice has s as 14. That is 168 divided by 12, which forgets to add the costs back on.",
      W("t", "168 ÷ 12 = 14")),
    B("Check: 24 samosas at 12 rupees is 288. Take away the 120 he spent, and the profit is 168.",
      W("c1", "24 × 12 − 120 = 168")),
    B("For profit questions: money in, minus all the costs, equals profit. Add up every cost before you write the equation."),
    check=("s", 24))

# 45x + 120 + 55 = 500 − 10
q = QID("62357bfd")
LESSONS[q] = lesson(
    B("Riya buys x boxes of diyas at 45 rupees each, and pays 120 for decorations and 55 for candles. "
      "She hands over 500 rupees and gets 10 back. How many boxes?",
      GIVEN("g", "x boxes at ₹45 + ₹120 + ₹55. Paid ₹500, got ₹10 back", True)),
    B("She hands over 500 and gets 10 back. So how much did she really spend?",
      ask=choose(["500 + 10", "500", "500 − 10"], 2,
                 "The change is money that comes back to her. So she spent less than 500: it is 500 minus 10.")),
    B("500 minus 10 is 490. That is the real bill.",
      W("p1", "500 − 10 = 490")),
    B("The bill is 45 x for the diyas, 120 for decorations and 55 for candles.",
      W("e0", "45x + 120 + 55 = 490")),
    B("Tidy the plain numbers: 120 plus 55 is 175.",
      G("e0", ["120", "55"], "175"), W("e1", "45x + 175 = 490")),
    solve(q, "x", 45, "+", 175, 490, asks="div", tail=" Riya bought 7 boxes."),
    B("Check: 7 boxes at 45 rupees is 315. Add 120 and 55 to get 490. With the 10 rupees change, that is the 500 she handed over.",
      W("c1", "7 × 45 + 120 + 55 = 490"), W("c2", "490 + 10 = 500")),
    B("Work out what was really spent, tidy the plain numbers into one, then solve."),
    check=("x", 7))

# 5x + 3 × 15 + 40 = 255
q = QID("68512e96")
LESSONS[q] = lesson(
    B("Coach Sharma buys 5 cricket balls at x rupees each, 3 stumps at 15 rupees each, and grip tape for 40 rupees. "
      "The bill is 255 rupees. What does one ball cost?",
      GIVEN("g", "5 balls at ₹x + 3 stumps at ₹15 + ₹40 tape = ₹255", True)),
    B("Start with what we can work out. 3 stumps at 15 rupees each is 45 rupees.",
      W("p1", "3 × 15 = 45")),
    B("Which equation fits the whole bill?",
      ask=ask(q, "eq", "5x + 45 + 40 = 255", ["5x + 15 + 40 = 255", "5x + 45 = 255"],
              "Three things are on the bill: 5 balls at x rupees, all 3 stumps for 45, and the tape for 40. "
              "Every one of them has to be in the equation.")),
    B("5 x for the balls, 45 for the stumps and 40 for the tape make 255.",
      W("e0", "5x + 45 + 40 = 255")),
    B("45 plus 40 is 85.",
      G("e0", ["45", "40"], "85"), W("e1", "5x + 85 = 255")),
    solve(q, "x", 5, "+", 85, 255, asks=None, tail=" One cricket ball costs 34 rupees."),
    B("Check: 5 balls at 34 rupees is 170. Add 45 for the stumps and 40 for the tape, and we get 255.",
      W("c1", "5 × 34 + 45 + 40 = 255")),
    B("Work out the costs you know, add them into one number, take that off the bill, and divide what is left."),
    check=("x", 34))

# 4x + 18 = 7x − 12
q = QID("69e582a5")
LESSONS[q] = lesson(
    B("Priya buys 4 packets of powder and pays 18 more for glue. Ankit buys 7 packets and gets 12 rupees off. "
      "Both pay the same. What does one packet cost? Call it x.",
      GIVEN("g", "Priya: 4 packets + ₹18. Ankit: 7 packets − ₹12. Same bill", True)),
    B("Priya pays 4 x plus 18. Ankit pays 7 x minus 12. They pay the same, so we put an equals sign between them.",
      W("e1", "4x + 18 = 7x − 12"), N("e1", "4x + 18", "Priya"), N("e1", "7x − 12", "Ankit")),
    B("Now x is on both sides. A good first move is to take the smaller lot of x from both sides. Which move is that?",
      ask=choose(["take 7x from both sides", "take 4x from both sides", "add 4x to both sides"], 1,
                 "4 x is smaller than 7 x. Taking 4 x from both sides clears the x from the left, "
                 "and still leaves some x on the right.")),
    B("Take 4 x from both sides. The left keeps just 18. On the right, 7 x minus 4 x is 3 x.",
      S("e1", "4x", "− 4x"), BOTH("e1", "− 4x"), W("e2", "18 = 3x − 12")),
    B("Now undo the minus 12 by adding 12 to both sides. 18 plus 12 is 30.",
      S("e2", "− 12", "+ 12"), BOTH("e2", "+ 12"), W("e3", "30 = 3x")),
    B("3 x is 30, so divide both sides by 3. x equals 10. A packet costs 10 rupees.",
      DIV("e3", 3), ANS("ans", "x = 10"), C("ans", "x = 10")),
    B("Check both bills. Priya: 4 times 10, plus 18, is 58. Ankit: 7 times 10, minus 12, is 58 as well. The same!",
      W("c1", "4 × 10 + 18 = 58"), W("c2", "7 × 10 − 12 = 58")),
    B("Here is why it works. Ankit has 3 more packets than Priya, and those 3 packets cover the gap of 18 plus 12, "
      "which is 30 rupees."),
    B("When x is on both sides, collect the x on one side and the plain numbers on the other. Then divide."),
    check=("x", 10))

# 4x + 2x + 15 = 51
q = QID("6efdf367")
LESSONS[q] = lesson(
    B("Vikram sells notebooks at x rupees each: 4 on day 1 and 2 on day 2. He also earns 15 rupees from bookmarks, "
      "and makes 51 rupees in all. Let's find x.",
      GIVEN("g", "Day 1: 4 notebooks. Day 2: 2 notebooks + ₹15. Total ₹51", True)),
    B("Day 1 brings in 4 x. Day 2 brings in 2 x, plus 15 from bookmarks. All together that is 51.",
      W("e0", "4x + 2x + 15 = 51")),
    B("4 x and 2 x are like terms: both count notebooks. What do they make together?",
      ask=choose(["8x", "6x", "6"], 1,
                 "4 notebooks and 2 notebooks make 6 notebooks. So 4 x plus 2 x is 6 x. We add the numbers, and the x stays.")),
    B("So the equation becomes 6 x, plus 15, equals 51.",
      G("e0", ["4x", "2x"], "6x"), W("e1", "6x + 15 = 51")),
    solve(q, "x", 6, "+", 15, 51, asks="undo", tail=" One notebook costs 6 rupees."),
    B("One choice is 9. That is the 36 shared among only the 4 notebooks from day 1, leaving out day 2.",
      W("t", "36 ÷ 4 = 9")),
    B("Check: day 1 is 4 times 6, which is 24. Day 2 is 2 times 6, plus 15, which is 27. And 24 plus 27 is 51.",
      W("c1", "4 × 6 = 24"), W("c2", "2 × 6 + 15 = 27"), W("c3", "24 + 27 = 51")),
    B("Gather the like terms first. Then it is the usual two steps: undo the plus, undo the times."),
    check=("x", 6))

# (80 + 35w) + (120 + 25w) = 500
q = QID("7023e2d6")
LESSONS[q] = lesson(
    B("Priya has 80 rupees and saves 35 a week. Karan has 120 rupees and saves 25 a week. They want a bat that costs "
      "500 rupees. After how many weeks will they have exactly enough?",
      GIVEN("g", "Priya ₹80 + ₹35 a week. Karan ₹120 + ₹25 a week. Bat ₹500", True)),
    B("Call the number of weeks w. After w weeks Priya has 80 plus 35 w, and Karan has 120 plus 25 w. Together they need 500.",
      W("e0", "80 + 35w + 120 + 25w = 500")),
    B("Let's gather like terms. Each week, how much do the two of them save together?",
      ask=choose(["10", "35", "60"], 2,
                 "Each week Priya adds 35 and Karan adds 25. Both are saving, so we add: 35 plus 25 is 60.")),
    B("So the w terms make 60 w. And the money they already have, 80 plus 120, is 200.",
      G("e0", ["35w", "25w"], "60w"), G("e0", ["80", "120"], "200"), W("e1", "200 + 60w = 500")),
    solve(q, "w", 60, "+", 200, 500, const_first=True, asks=None, tail=" In 5 weeks they will have enough."),
    B("Check: after 5 weeks Priya has 255 rupees and Karan has 245. Together that is 500.",
      W("c1", "80 + 35 × 5 = 255"), W("c2", "120 + 25 × 5 = 245"), W("c3", "255 + 245 = 500")),
    B("Add what they have now, add what they save each week, and you get one simple equation for the two of them."),
    check=("w", 5))

# 3(x + 4) = 30: divide first
q = QID("71b21fc2")
LESSONS[q] = lesson(
    B("Meera sets out 3 rows of lamps. Each row has the same number of lamps, plus 4 extra at the end for decoration. "
      "There are 30 lamps in all. How many are in a row before the extras? Call it x.",
      GIVEN("g", "3 rows, each with x lamps + 4 extra. Total 30", True)),
    B("One row has x lamps plus 4 extra. Which equation gives all 3 rows?",
      ask=ask(q, "eq", "3(x + 4) = 30", ["3x + 4 = 30", "x + 4 = 30"],
              "Every row gets its own 4 extra lamps. So the whole row, x plus 4, is repeated 3 times. "
              "The bracket keeps the row together.")),
    B("One row is x plus 4, and there are 3 rows like that, making 30.",
      W("e1", "3(x + 4) = 30"), M("e1", "(x + 4)", "box"), N("e1", "(x + 4)", "one row")),
    B("The whole bracket is multiplied by 3. So divide both sides by 3 first, and we find one whole row: "
      "30 divided by 3 is 10.",
      DIV("e1", 3), W("e2", "x + 4 = 10")),
    B("One row, x plus 4, is 10 lamps. How do we get x on its own?",
      ask=ask(q, "undo", "take 4 from both sides", ["add 4 to both sides", "divide both sides by 4"],
              "Adding 4 is undone by taking 4 away. And we take it from both sides to keep them equal.")),
    B("10 minus 4 is 6. So each row has 6 lamps before the extras.",
      S("e2", "+ 4", "− 4"), BOTH("e2", "− 4"), ANS("ans", "x = 6"), C("ans", "x = 6")),
    B("10 is among the choices, but that is a whole row with its 4 extras. The question asks for the lamps before the extras."),
    B("Check: 6 plus 4 is 10 lamps in a row, and 3 rows of 10 make 30.",
      W("c1", "3 × (6 + 4) = 30")),
    B("When a whole bracket is multiplied, you can divide first to find the bracket, then deal with what is inside it."),
    check=("x", 6))

# 4n + 30 = 150; n = 30
q = QID("7c249154")
LESSONS[q] = lesson(
    B("Riya has saved n rupees, and Arjun has saved 3 times as much. Their mother gives each of them 15 rupees. "
      "Now they have 150 rupees together. We need the equation, and Riya's savings.",
      GIVEN("g", "Riya: n. Arjun: 3n. Each gets ₹15. Together ₹150", True)),
    B("After the gift, Riya has n plus 15. Arjun has 3 n plus 15. Together that is 150.",
      W("e0", "(n + 15) + (3n + 15) = 150")),
    B("Gather like terms. n and 3 n make 4 n. And how much gift money is there in all?",
      G("e0", ["n", "3n"], "4n"),
      ask=choose(["15", "30", "45"], 1,
                 "Mother gives 15 rupees to each of them. There are 2 children, so that is 15 plus 15, which is 30.")),
    B("So the equation is 4 n, plus 30, equals 150.",
      G("e0", ["15", ("15", 2)], "30"), W("e1", "4n + 30 = 150")),
    solve(q, "n", 4, "+", 30, 150, asks="div", final=False, tail=" Riya saved 30 rupees."),
    B("So the answer is the equation 4 n plus 30 equals 150, and Riya saved 30 rupees.",
      ANS("ans", "4n + 30 = 150, so n = 30", True), C("ans", "n = 30")),
    B("The trap is adding the gift only once. Each of them got 15 rupees, so it goes into the equation twice."),
    B("Check: Arjun saved 3 times 30, which is 90. After the gifts they have 45 and 105, and 45 plus 105 is 150.",
      W("c1", "3 × 30 = 90"), W("c2", "30 + 15 = 45"), W("c3", "90 + 15 = 105"), W("c4", "45 + 105 = 150")),
    B("Write what each person has, add them up, and gather the like terms. The word each means it counts for both."),
    check=("n", 30))

# 3(n + 2) = 21: open the bracket
q = QID("7ef490f7")
LESSONS[q] = lesson(
    B("Rohan packs samosas in boxes. Each box has n samosas, plus 2 bonus ones on top. He sells 3 boxes "
      "and gives away 21 samosas in all. Let's find n.",
      GIVEN("g", "3 boxes, each with n samosas + 2 bonus. Total 21", True)),
    B("Which equation counts the samosas in all 3 boxes?",
      ask=ask(q, "eq", "3(n + 2) = 21", ["3n + 2 = 21", "n + 2 = 21"],
              "Each box gets its own 2 bonus samosas. So one box holds n plus 2, and there are 3 boxes like that.")),
    B("One box is n plus 2. 3 boxes like that make 21.",
      W("e0", "3(n + 2) = 21")),
    B("Let's open the bracket. The 3 multiplies both things inside: 3 times n, and 3 times 2. "
      "Careful, the 2 is multiplied as well: that is 6 bonus samosas.",
      ARC("e0", "3", ["n", "2"]), W("e1", "3n + 6 = 21")),
    solve(q, "n", 3, "+", 6, 21, asks="undo", tail=" So n is 5."),
    B("Check: one box holds 5 plus 2, which is 7 samosas. And 3 boxes of 7 make 21.",
      W("c1", "3 × (5 + 2) = 21")),
    B("7 is among the choices, but that is a whole box, bonus included. The question asks for n, the 5 underneath."),
    B("A number outside a bracket multiplies everything inside. Open the bracket, then solve as usual."),
    check=("n", 5))
