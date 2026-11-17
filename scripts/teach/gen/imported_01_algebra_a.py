"""Algebra: three story questions and the 'find the value' questions from the textbook."""
from imported_01_lib import AI, ANS, ARC, B, G, GIVEN, M, N, S, TB, W, choose, lesson

LESSONS = {}

# ── Game stall: 4x + 3x + 10 + 5x − 15 at x = 6 ──────────────────────────────
LESSONS[AI + "4199a5e1-ca44-4626-98e4-7c3bdcc064ae"] = lesson(
    B("Ananya and Bhavesh charge x rupees a game. Day 1: 4 games and 3 games, plus a bonus of 10 rupees. Day 2: 5 more games, but 15 rupees spent on prizes. With x as 6, what do they earn in all?",
      GIVEN("l1", "Day 1: 4 games + 3 games + ₹10 bonus"), GIVEN("l2", "Day 2: 5 games − ₹15 for prizes.   x = 6")),
    B("Each game brings in x rupees. So Day 1 is 4 x, plus 3 x, plus 10. And Day 2 is 5 x, minus 15.",
      W("d1", "Day 1: 4x + 3x + 10", label=True), W("d2", "Day 2: 5x − 15", label=True)),
    B("Gather all the games first. 4 x, 3 x and 5 x: how many x is that altogether?",
      ask=choose(["7x", "12x", "12"], 1,
                 "Add the numbers of games: 4 plus 3 is 7, and 5 more is 12. They are all x's, so that is 12 x.")),
    B("So the games bring in 12 x.", W("g", "Games: 4x + 3x + 5x = 12x", label=True)),
    B("Now the plain rupees: a bonus of 10 coming in, and 15 going out on prizes. What do those two do to the total?",
      ask=choose(["Add 25", "Add 5", "Take away 5"], 2,
                 "The 10 comes in, but the 15 goes out. 15 is 5 more than 10, so overall they lose 5 rupees.")),
    B("Careful: that is the trap. The 15 was spent, so it is taken away, not added. Plus 10 and minus 15 together make minus 5.",
      W("r", "10 − 15 = −5")),
    B("So the total for both days is 12 x, minus 5.", W("t", "Total = 12x − 5", label=True), M("t", "12x − 5", "box")),
    B("Now put in x as 6. 12 times 6 is 72.", W("s1", "12 × 6 = 72")),
    B("And 72 minus 5 is 67. They earn 67 rupees.", ANS("ans", "12 × 6 − 5 = 67"), M("ans", "67", "circle")),
    B("Check it day by day. Day 1 comes to 52 rupees, and Day 2 comes to 15. And 52 plus 15 is 67.",
      W("c1", "7 × 6 + 10 = 52"), W("c2", "5 × 6 − 15 = 15"), W("c3", "52 + 15 = 67")),
    B("Write each day with x, gather the x's, gather the plain numbers, and only then put in the value of x."),
)

# ── Sweet boxes: 4x + 3(2x + 3) at x = 6 ─────────────────────────────────────
LESSONS[AI + "cbe76d81-0925-48a8-abe4-9872096cf41c"] = lesson(
    B("Kavitha's small box holds x sweets. A large box holds 2 x plus 3. She makes 4 small boxes and 3 large ones, and x is 6. How many sweets in all?",
      GIVEN("l1", "Small box: x.   Large box: 2x + 3.   x = 6"), GIVEN("l2", "4 small boxes + 3 large boxes = ?")),
    B("The 4 small boxes hold 4 x. The 3 large boxes hold 3 times the whole bracket, 2 x plus 3.",
      W("eq", "Total = 4x + 3(2x + 3)", label=True)),
    B("3 times that bracket. What does it open out to?",
      ask=choose(["6x + 3", "6x + 9", "5x + 6"], 1,
                 "The 3 outside multiplies both things inside. 3 times 2 x is 6 x, and 3 times 3 is 9.")),
    B("The 3 multiplies the 2 x, and it multiplies the 3 as well. Each large box has 3 extra sweets and there are 3 boxes, so 9 extras.",
      ARC("eq", "3", ["2x", ("3", 2)]), W("e2", "Total = 4x + 6x + 9", label=True)),
    B("That is the classic slip in this question: multiplying the 2 x but leaving the 3 alone. Every large box has those 3 extras."),
    B("Now gather the x's. 4 x and 6 x make 10 x.", G("e2", ["4x", "6x"], "10x"), W("e3", "Total = 10x + 9", label=True)),
    B("Put in x as 6. 10 times 6 is 60, and 60 plus 9 is 69. Kavitha has 69 sweets.",
      W("s1", "10 × 6 = 60"), ANS("ans", "10 × 6 + 9 = 69"), M("ans", "69", "circle")),
    B("Check by counting boxes. A small box holds 6 sweets. A large box holds 2 times 6, plus 3, which is 15.",
      W("c1", "2 × 6 + 3 = 15")),
    B("4 small boxes hold 24, and 3 large boxes hold 45. 24 plus 45 is 69. It matches.",
      W("c2", "4 × 6 = 24"), W("c3", "3 × 15 = 45"), W("c4", "24 + 45 = 69")),
    B("A number outside a bracket multiplies everything inside. Open the bracket, gather the like terms, then put in the value."),
)

# ── Samosa stall: x(3x + 4 + 2x − 1) at x = 6 ────────────────────────────────
LESSONS[AI + "dccc9f5e-9046-49e2-9204-2ce43d2e1aab"] = lesson(
    B("Ananya sells samosas at x rupees each. On Day 1 she sells 3 x plus 4 samosas. On Day 2 she sells 2 x minus 1. With x as 6, how much does she earn?",
      GIVEN("l1", "Price: ₹x each.   x = 6"), GIVEN("l2", "Day 1: 3x + 4 samosas.   Day 2: 2x − 1 samosas")),
    B("Careful: those expressions count samosas, not rupees. So how do we get her earnings?",
      ask=choose(["Total samosas + price", "Just add the two days", "Total samosas × price"], 2,
                 "Every samosa brings in the price. So her earnings are the number of samosas, times the price of one.")),
    B("First the samosas. Add the two days: 3 x plus 4, and 2 x minus 1.", W("s", "(3x + 4) + (2x − 1)", label=True)),
    B("3 x and 2 x make 5 x. And plus 4 with minus 1 leaves plus 3. So she sells 5 x plus 3 samosas.",
      G("s", ["3x", "2x"], "5x"), W("s2", "Samosas = 5x + 3", label=True)),
    B("Now x is 6. 5 times 6 is 30, and 3 more is 33 samosas.", W("n1", "5 × 6 = 30"), W("n2", "30 + 3 = 33")),
    B("We are not finished. 33 is a number of samosas. Each one sells for x rupees, and x is 6, so we multiply 33 by 6.",
      N("n2", "33", "samosas, not rupees")),
    B("33 times 6. 30 times 6 is 180, and 3 times 6 is 18. Together, 198.",
      W("m1", "30 × 6 = 180"), W("m2", "3 × 6 = 18"), W("m3", "180 + 18 = 198")),
    B("She earns 198 rupees.", ANS("ans", "33 × 6 = 198"), M("ans", "198", "circle")),
    B("Check the samosas day by day. Day 1: 3 times 6, plus 4, is 22. Day 2: 2 times 6, minus 1, is 11. And 22 plus 11 is 33.",
      W("c1", "3 × 6 + 4 = 22"), W("c2", "2 × 6 − 1 = 11"), W("c3", "22 + 11 = 33")),
    B("Notice that x did two jobs here: it set how many were sold, and the price of each. Find the count first, then multiply by the price."),
)

# ── The 4th even number after 5x + 5 ─────────────────────────────────────────
LESSONS[TB + "ch01_q033"] = lesson(
    B("5 x plus 5 is some even number. We don't know which one. We want the 4th even number that comes after it.",
      GIVEN("l1", "5x + 5 is even. 4th even number after it = ?")),
    B("Think about even numbers in a row: 2, 4, 6, 8. How far is it from one even number to the next?",
      ask=choose(["1", "2", "4"], 1,
                 "Look at 2, 4, 6, 8. Between two even numbers there is always one odd number. So each step is 2.")),
    B("So to reach the next even number we add 2, whatever number we start from. Even when the start is written with a letter.",
      W("s1", "5x + 5 + 2 = 5x + 7"), N("s1", "5x + 7", "1st")),
    B("That is the 1st one after it. Add 2 again for the 2nd: 5 x plus 9.", W("s2", "5x + 7 + 2 = 5x + 9"), N("s2", "5x + 9", "2nd")),
    B("And again for the 3rd: 5 x plus 11.", W("s3", "5x + 9 + 2 = 5x + 11"), N("s3", "5x + 11", "3rd")),
    B("And once more for the 4th: 5 x plus 13.",
      W("s4", "5x + 11 + 2 = 5x + 13"), N("s4", "5x + 13", "4th"),
      ANS("ans", "4th even number after = 5x + 13", True), M("ans", "5x + 13", "circle")),
    B("Careful where you start counting. 5 x plus 5 itself is not the 1st one after. Count it by mistake and you stop one short, at 5 x plus 11."),
    B("Here is a quicker way. We took 4 steps of 2. How much did we add altogether?",
      ask=choose(["6", "8", "4"], 1, "4 steps, and each step is 2. 4 times 2 is 8.")),
    B("So we can add 8 in one go. 5 x plus 5, plus 8, is 5 x plus 13. The same answer.",
      W("q1", "4 × 2 = 8"), W("q2", "5x + 5 + 8 = 5x + 13")),
    B("Let's test it with a real number. If x is 1, then 5 x plus 5 is 10. The even numbers after 10 are 12, 14, 16 and 18. And 5 plus 13 is 18.",
      W("t1", "5 × 1 + 5 = 10"), W("t2", "After 10: 12, 14, 16, 18", label=True), W("t3", "5 × 1 + 13 = 18")),
    B("Even numbers go up in 2s. So the 4th one after is 4 steps of 2, which is 8 more."),
    check=("x", 5),
)

# ── 17x − 10 at x = 2 ────────────────────────────────────────────────────────
LESSONS[TB + "ch01_q034"] = lesson(
    B("Here is an expression: 17 x, minus 10. We are told that x is 2, and we want the number it makes.",
      GIVEN("l1", "17x − 10,   x = 2")),
    B("First, what does 17 x mean when x is 2?",
      ask=choose(["172", "17 + 2", "17 × 2"], 2,
                 "A number written right next to a letter means multiply. So 17 x is 17 times x, and with x as 2 that is 17 times 2.")),
    B("Careful: this is the classic trap. Sliding the 2 in beside the 17 to make 172 is not what the letter means. It is 17 times 2.",
      W("l2", "17 × 2 − 10"), N("l2", "2", "x")),
    B("Times comes before minus. 17 times 2 is double 17, which is 34.", W("l3", "17 × 2 = 34")),
    B("Then take away the 10. 34 minus 10 is 24.", ANS("ans", "17 × 2 − 10 = 24"), M("ans", "24", "circle")),
    B("The question gives us a way to check. It says the answer is an even number. 24 ends in 4, so it is even. That fits."),
    B("Two other slips to dodge: stopping at 34 before taking away the 10, and forgetting the x altogether, which leaves 17 minus 10."),
    B("To find the value of an expression, swap the letter for its number, remember that side by side means times, and then do the sum."),
)

# ── 7a + 3b − c ──────────────────────────────────────────────────────────────
LESSONS[TB + "ch09_q001"] = lesson(
    B("Here is an expression with three letters: 7 a, plus 3 b, minus c. We know that a is 1, b is 2 and c is 3.",
      GIVEN("l1", "7a + 3b − c"), GIVEN("l2", "a = 1, b = 2, c = 3")),
    B("What does 3 b mean, when b is 2?",
      ask=choose(["3 × 2", "32", "3 + 2"], 0,
                 "A number written right beside a letter means times. So 3 b is 3 times b, and b is 2.")),
    B("So swap each letter for its number. 7 times 1, plus 3 times 2, minus 3.",
      W("s", "7 × 1 + 3 × 2 − 3"), N("s", "1", "a"), N("s", "2", "b"), N("s", "3", "c", nth=2)),
    B("Which parts do we work out first?",
      ask=choose(["The addition", "The multiplications", "The subtraction"], 1,
                 "Times comes before plus and minus. So first work out 7 times 1 and 3 times 2, and only then add and subtract.")),
    B("7 times 1 is 7, and 3 times 2 is 6. So now we have 7, plus 6, minus 3.", W("s2", "7 + 6 − 3")),
    B("7 plus 6 is 13, and 13 minus 3 is 10.", W("s3", "7 + 6 = 13"), W("s4", "13 − 3 = 10")),
    B("So the value is 10.", ANS("ans", "7 × 1 + 3 × 2 − 3 = 10"), M("ans", "10", "circle")),
    B("Careful with the lonely c at the end. It has no number in front, so it is just 1 c. We take away 3, once."),
    B("Check by going in a different order. 7 minus 3 is 4, and 4 plus 6 is 10 again.", W("chk", "7 − 3 + 6 = 10")),
    B("Swap the letters for their numbers, do the times first, then add and subtract from left to right."),
)

# ── 3x − 5y + 7 ──────────────────────────────────────────────────────────────
LESSONS[TB + "ch09_q004"] = lesson(
    B("x is 3 and y is 2. We want the value of 3 x, minus 5 y, plus 7.", GIVEN("l1", "3x − 5y + 7,   x = 3, y = 2")),
    B("Start with the 5 y. What does it mean when y is 2?",
      ask=choose(["52", "5 × 2", "5 + 2"], 1,
                 "A number written right beside a letter means times. So 5 y is 5 times y, which is 5 times 2.")),
    B("So swap the letters for their numbers. 3 x becomes 3 times 3, and 5 y becomes 5 times 2.",
      W("s", "3 × 3 − 5 × 2 + 7")),
    B("Times first. 3 times 3 is 9, and 5 times 2 is 10. So we have 9, minus 10, plus 7.", W("s2", "9 − 10 + 7")),
    B("Now a puzzle. 9 minus 10: we cannot take 10 from 9 without dipping below zero. What can we do?",
      ask=choose(["Swap it round: 10 − 9", "Add the 7 first, then take away 10", "Stop: there is no answer"], 1,
                 "We may not swap a take-away round: 10 minus 9 is a different sum. But the plus 7 is waiting, and adding first is allowed.")),
    B("9 plus 7 is 16. Then 16 minus 10 is 6.", W("s3", "9 + 7 = 16"), W("s4", "16 − 10 = 6")),
    B("It is like money. You have 9 rupees, you owe 10, and then you are given 7 more. You end up with 6.",
      ANS("ans", "3 × 3 − 5 × 2 + 7 = 6"), M("ans", "6", "circle")),
    B("If you know numbers below zero, the straight way works too. 9 minus 10 is minus 1, and minus 1 plus 7 is 6.",
      W("alt", "−1 + 7 = 6")),
    B("The slip to avoid is adding the 10 and the 7 first and taking all of that away. The minus belongs only to the 10."),
    B("Swap letters for numbers and do the times first. Then, if a take-away looks stuck, add the plus parts before you subtract."),
)

# ── 3a + 2b − (a + b)c with c = 0 ────────────────────────────────────────────
LESSONS[TB + "ch09_q019"] = lesson(
    B("a is 3, b is 1 and c is 0. We want the value of 3 a, plus 2 b, minus the bracket a plus b, times c.",
      GIVEN("l1", "3a + 2b − (a + b)c"), GIVEN("l2", "a = 3, b = 1, c = 0")),
    B("Swap in the numbers. 3 times 3, plus 2 times 1, minus the bracket 3 plus 1, times 0.",
      W("s", "3 × 3 + 2 × 1 − (3 + 1) × 0")),
    B("Brackets first. 3 plus 1 is 4. So the last part is 4 times 0.", W("s2", "3 × 3 + 2 × 1 − 4 × 0")),
    B("What is 4 times 0?",
      ask=choose(["4", "0", "40"], 1, "Times 0 means no lots at all. 4 lots of nothing is nothing. Anything times 0 is 0.")),
    B("So the whole last part disappears: we are taking away 0. Careful, though. Only that part is 0, not the whole expression.",
      S("s2", "− 4 × 0", "− 0")),
    B("Now the other two parts. 3 times 3 is 9, and 2 times 1 is 2.", W("s3", "9 + 2 − 0")),
    B("9 plus 2 is 11, and taking away 0 changes nothing. The value is 11.",
      ANS("ans", "9 + 2 − 0 = 11"), M("ans", "11", "circle")),
    B("Check the whole line in one go, and it agrees.", W("chk", "3 × 3 + 2 × 1 − (3 + 1) × 0 = 11")),
    B("Swap letters for numbers. Brackets first, then times, then plus and minus. And when you spot a times 0, that whole piece is 0."),
)

# ── −3p + 2q + 3r with p = −3 ────────────────────────────────────────────────
LESSONS[TB + "ch09_q020"] = lesson(
    B("Here the letter p stands for a number below zero: minus 3. We want the value of minus 3 p, plus 2 q, plus 3 r.",
      GIVEN("l1", "−3p + 2q + 3r"), GIVEN("l2", "p = −3, q = 2, r = 4")),
    B("Swap in the numbers. Put the minus 3 in a bracket, so that its sign does not get lost.",
      W("s", "−3 × (−3) + 2 × 2 + 3 × 4"), M("s", "(−3)", "box")),
    B("Take the easy parts first. 2 times 2 is 4, and 3 times 4 is 12.", W("e1", "2 × 2 = 4"), W("e2", "3 × 4 = 12")),
    B("Now the first part: minus 3, times minus 3. What is it?",
      ask=choose(["−9", "9", "−6"], 1,
                 "3 times 3 is 9. Each minus sign flips the answer to the other side of zero. Two flips bring it back, so it is plus 9.")),
    B("Here is a way to see it. p is a debt of 3. Minus 3 p means taking that debt away 3 times. Lose three debts of 3 and you are 9 better off.",
      W("e3", "−3 × (−3) = 9"), M("e3", "9", "box")),
    B("Careful: this is the trap. With only one flip you get minus 9, and the total comes out far too small."),
    B("Now add the three parts. 9 plus 4 is 13, and 13 plus 12 is 25.", W("a1", "9 + 4 = 13"), W("a2", "13 + 12 = 25")),
    B("So the value is 25.", ANS("ans", "−3 × (−3) + 2 × 2 + 3 × 4 = 25"), M("ans", "25", "circle")),
    B("Check by adding in another order: 12 plus 4 plus 9 is 25 again.", W("chk", "12 + 4 + 9 = 25")),
    B("Bracket any number below zero when you swap it in. Minus times minus gives plus. Then add up the parts."),
)

# ── A chain: a → z → y → x ───────────────────────────────────────────────────
LESSONS[TB + "ch09_q036"] = lesson(
    B("Four letters, each one built from the next, and then an expression that uses them. It looks like a tangle, so we look for the loose end.",
      GIVEN("l1", "x = y − 2,  y = z + 1,  z = a + 6,  a = 6"), GIVEN("l2", "Find x + a(y × a − 3)")),
    B("We know that a is 6. Which letter can we work out next?",
      ask=choose(["x", "y", "z"], 2,
                 "To find x we need y, and to find y we need z. But z only needs a, and we know a. So z comes first.")),
    B("z is a plus 6. That is 6 plus 6, which is 12.", W("z", "6 + 6 = 12"), N("z", "12", "z")),
    B("y is z plus 1: 12 plus 1 is 13. And x is y minus 2: 13 minus 2 is 11.",
      W("y", "12 + 1 = 13"), N("y", "13", "y"), W("x", "13 − 2 = 11"), N("x", "11", "x")),
    B("Now put them into the expression. x is 11, a is 6, and inside the bracket y times a is 13 times 6.",
      W("e", "11 + 6 × (13 × 6 − 3)")),
    B("What do we work out first?",
      ask=choose(["11 + 6", "The bracket", "6 × 13"], 1,
                 "Brackets always come first. And inside the bracket, the times comes before the minus.")),
    B("Inside the bracket: 13 times 6. 10 sixes are 60 and 3 sixes are 18, so 78. Then 78 minus 3 is 75.",
      W("b1", "10 × 6 = 60"), W("b2", "3 × 6 = 18"), W("b3", "60 + 18 = 78"), W("b4", "78 − 3 = 75")),
    B("Now we have 11, plus 6 times 75. Careful: times before plus. Adding the 11 and the 6 first is the trap.",
      W("e2", "11 + 6 × 75"), M("e2", "6 × 75")),
    B("6 times 75. 6 times 70 is 420, and 6 times 5 is 30. That makes 450.",
      W("m1", "6 × 70 = 420"), W("m2", "6 × 5 = 30"), W("m3", "6 × 75 = 450")),
    B("Last of all, add the 11. 450 plus 11 is 461.", ANS("ans", "11 + 6 × (13 × 6 − 3) = 461"), M("ans", "461", "circle")),
    B("A quick check on size. 6 times 75 is 450, so the answer has to be a little more than 450. And 461 is."),
    B("Start from the letter you know and work along the chain. Then brackets first, times next, and plus last."),
)
