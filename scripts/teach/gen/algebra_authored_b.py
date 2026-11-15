"""Lessons written by hand for the one-off equations: brackets, letters on both sides, fractions."""
from algebra_lib import B, W, answer, arc, both, choose, divide, given, group, lesson, mark, note, strike

LESSONS = {}

# Find a when b = 3: 7a + 2b − 2a = 26.
LESSONS["EXT_G5_WS_B6_013"] = lesson([
    B("This equation has two letters, a and b. But we are told that b is 3, so only a is really hidden.",
      given("l0", "b = 3", label=True), given("l1", "7a + 2b − 2a = 26", label=True)),
    B("First we deal with the b. When b is 3, what does 2 b become?",
      ask=choose(["the number 23", "2 × 3 = 6", "2 + 3 = 5"], 1,
                 "A number written next to a letter means times. So 2 b is 2 times 3, which is 6.")),
    B("So in goes the 3. Now the equation says 7 a, plus 6, minus 2 a, equals 26.",
      note("l1", "2b", "2 × 3 = 6"), W("l2", "7a + 6 − 2a = 26")),
    B("Look for like terms. 7 a and minus 2 a are both a terms. 7 lots of a, take away 2 lots of a, leaves 5 a.",
      group("l2", ["7a", "− 2a"], "5a"), W("l3", "5a + 6 = 26")),
    B("That looks much friendlier. What is in the way of the 5 a?",
      ask=choose(["the 26", "the 5", "the + 6"], 2,
                 "Look at the left side. The 5 a has a plus 6 hanging on to it. That is what we clear first.")),
    B("To undo plus 6 we take 6 from both sides, so the balance stays level. 26 minus 6 is 20, so 5 a equals 20.",
      strike("l3", "+ 6", "− 6"), both("l3", "− 6"), W("l4", "5a = 26 − 6"), W("l5", "5a = 20")),
    B("5 a means 5 times a, so we divide both sides by 5. 20 divided by 5 is 4. So a equals 4.",
      divide("l5", "5"), answer("l6", "a = 4"), mark("l6", "a = 4")),
    B("Check in the equation we started with. 7 times 4 is 28. 2 times 4 is 8. And 28, plus 6, minus 8, is 26. It works.",
      W("l7", "7 × 4 = 28"), W("l8", "28 + 6 − 8 = 26")),
    B("So the plan: put in the number you are given, gather the like terms, then solve as usual."),
], "a", 4)

# For x = 8, which is true?
LESSONS["EXT_G5_WS_B6_014"] = lesson([
    B("We are told x is 8, and we have four equations. Only one of them stays balanced when x is 8. Let's find it.",
      given("l1", "x = 8")),
    B("What is the quickest way to test an equation?",
      ask=choose(["solve each equation for x", "put 8 in for x on both sides", "put 8 in on the left side only"], 1,
                 "Solving all four would take ages. It is quicker to put 8 in place of every x, "
                 "and see whether the left side and the right side come out the same.")),
    B("Start with A. The left side is 8, plus 5 times 8, which comes to 48. "
      "The right side is 3 times 8, plus 18, which is 42. They do not match, so A is out.",
      W("a0", "A:  8 + 5x = 3x + 18", label=True), W("a1", "8 + 5 × 8 = 48"), W("a2", "3 × 8 + 18 = 42"),
      strike("a0", "8 + 5x = 3x + 18")),
    B("Now B. On the left we must take 4 times 8, which is 32, away from 9. That goes below zero. "
      "The right side is 22. No match.",
      W("b0", "B:  9 − 4x = 2x + 6", label=True), W("b1", "4 × 8 = 32"), W("b2", "2 × 8 + 6 = 22"),
      strike("b0", "9 − 4x = 2x + 6")),
    B("Now C. The left side is 5 times 8, plus 7. That is 47. Your turn: what is the right side, 8 x minus 17?",
      W("c0", "C:  5x + 7 = 8x − 17", label=True), W("c1", "5 × 8 + 7 = 47"),
      ask=choose(["64", "47", "81"], 1,
                 "8 x is 8 times 8, which is 64. Then we take away 17, and that leaves 47.")),
    B("8 times 8 is 64, and 64 minus 17 is 47. Both sides are 47. The balance is level!",
      W("c2", "8 × 8 − 17 = 47"), mark("c0", "5x + 7 = 8x − 17", "box")),
    B("Let's make sure about D as well. The left side is 39 and the right side is 37. So close, but close is not equal.",
      W("d0", "D:  4x + 7 = 21 + 2x", label=True), W("d1", "4 × 8 + 7 = 39"), W("d2", "21 + 2 × 8 = 37"),
      strike("d0", "4x + 7 = 21 + 2x")),
    B("So when x is 8, the true one is 5 x plus 7 equals 8 x minus 17.",
      answer("l9", "5x + 7 = 8x − 17"), mark("l9", "5x + 7 = 8x − 17")),
    B("To test an equation, put the number in on both sides and compare. Equal sides mean it is true."),
], "x", 8)

# If 2(3d + 4) = 4(5 − 2d) + 2, find d.
LESSONS["EXT_G5_WS_B6_016"] = lesson([
    B("Here is an equation with a bracket on each side. Before we can find d, the brackets have to be opened.",
      given("l1", "2(3d + 4) = 4(5 − 2d) + 2")),
    B("On the left, the 2 outside multiplies everything inside. 2 times 3 d is 6 d, and 2 times 4 is 8.",
      arc("l1", "2", "3d", "4"), W("l2", "6d + 8 = 4(5 − 2d) + 2")),
    B("Now the right side. The 4 multiplies the 5, and it multiplies the minus 2 d. What is 4 times minus 2 d?",
      ask=choose(["+ 8d", "− 8d", "− 2d"], 1,
                 "The minus sign belongs to the 2 d, so it comes along. 4 times 2 d is 8 d, "
                 "and the minus stays: minus 8 d.")),
    B("So 4 times 5 is 20, and 4 times minus 2 d is minus 8 d. The plus 2 at the end just waits.",
      arc("l2", "4", "5", "2d"), W("l3", "6d + 8 = 20 − 8d + 2")),
    B("Tidy the right side. 20 and 2 are both plain numbers, and together they make 22.",
      group("l3", ["20", "+ 2"], "22"), W("l4", "6d + 8 = 22 − 8d")),
    B("Now there are d terms on both sides, and we want them together. "
      "How do we bring the minus 8 d over to the left?",
      ask=choose(["take 8d from both sides", "add 8d to both sides", "write it on the left as − 8d"], 1,
                 "To undo minus 8 d we add 8 d. And whatever we do to one side, we do to the other. "
                 "A term never just hops across keeping the same sign.")),
    B("So we add 8 d to both sides. On the right it cancels. On the left, 6 d plus 8 d makes 14 d.",
      strike("l4", "− 8d", "+ 8d"), both("l4", "+ 8d"), W("l5", "14d + 8 = 22")),
    B("Now clear the plus 8 by taking 8 from both sides. 22 minus 8 is 14. So 14 d equals 14.",
      strike("l5", "+ 8", "− 8"), both("l5", "− 8"), W("l6", "14d = 14")),
    B("Divide both sides by 14. 14 divided by 14 is 1. So d equals 1.",
      divide("l6", "14"), answer("l7", "d = 1"), mark("l7", "d = 1")),
    B("Check both sides with d as 1. The left is 2 times 7, which is 14. "
      "The right is 4 times 3, plus 2, which is also 14. Balanced.",
      W("l8", "2(3 × 1 + 4) = 14"), W("l9", "4(5 − 2 × 1) + 2 = 14")),
    B("The plan for brackets: open them first, tidy each side, gather the letters on one side "
      "and the numbers on the other, then divide."),
], "d", 1)

# p = m + 3, q = 5 − m. If 2p + 3q = 0, find m.
LESSONS["EXT_G5_WS_B6_019"] = lesson([
    B("Three letters here: p, q and m. But p and q are both built from m. So really there is only one hidden number, m.",
      given("l1", "p = m + 3,  q = 5 − m", label=True), given("l2", "2p + 3q = 0", label=True)),
    B("Wherever we see p, we can write m plus 3 instead. Wherever we see q, we write 5 minus m. "
      "We use brackets, so each one stays together.",
      note("l2", "p", "(m + 3)"), note("l2", "q", "(5 − m)"), W("l3", "2(m + 3) + 3(5 − m) = 0")),
    B("Open the first bracket. 2 times m is 2 m, and 2 times 3 is 6.",
      arc("l3", "2", "m", "3"), W("l4", "2m + 6 + 3(5 − m) = 0")),
    B("Now the second bracket. The 3 multiplies the 5, and it multiplies the minus m. What is 3 times minus m?",
      ask=choose(["+ 3m", "− m", "− 3m"], 2,
                 "The minus sign belongs to the m, so it travels with it. 3 times minus m is minus 3 m.")),
    B("So 3 times 5 is 15, and 3 times minus m is minus 3 m.",
      arc("l4", "3", "5", ("m", 2)), W("l5", "2m + 6 + 15 − 3m = 0")),
    B("Gather the like terms. 6 and 15 make 21. And 2 m take away 3 m leaves us one m short: that is minus m.",
      group("l5", ["+ 6", "+ 15"], "21"), group("l5", ["2m", "− 3m"], "− m"), W("l6", "21 − m = 0")),
    B("21 minus m equals 0. What must m be?",
      ask=choose(["0", "21", "−21"], 1,
                 "21 take away something leaves nothing. So that something must be 21 itself.")),
    B("Let's show it the balance way too. Add m to both sides. On the left the m cancels and 21 is left. "
      "On the right, 0 plus m is m.",
      both("l6", "+ m"), W("l7", "21 = m"), answer("l8", "m = 21"), mark("l8", "m = 21")),
    B("Check. p is 21 plus 3, which is 24. q is 5 minus 21, which is minus 16. "
      "2 times 24 is 48, and 3 times minus 16 is minus 48. Together they make 0.",
      W("l9", "21 + 3 = 24"), W("l10", "5 − 21 = −16"), W("l11", "2 × 24 − 3 × 16 = 0"), W("l12", "48 − 48 = 0")),
    B("When letters are built from another letter, swap them in with brackets, open the brackets, and solve as usual."),
], "m", 21)

# 3x − 4(x + 6) = 0
LESSONS["EXT_G5_FP_2016_009"] = lesson([
    B("Here is our equation. 3 x, minus 4 times the bracket x plus 6, equals 0. "
      "The bracket is the tricky part, so we open it first.",
      given("l1", "3x − 4(x + 6) = 0")),
    B("The minus 4 multiplies both things in the bracket. Minus 4 times x is minus 4 x. "
      "What is minus 4 times plus 6?",
      ask=choose(["+ 24", "− 6", "− 24"], 2,
                 "4 times 6 is 24, and the minus sign in front of the 4 comes along too. So it is minus 24. "
                 "This is the slip to watch for.")),
    B("So the bracket opens into minus 4 x, minus 24.",
      arc("l1", "4", ("x", 2), "6"), W("l2", "3x − 4x − 24 = 0")),
    B("Now gather the x terms. 3 x take away 4 x: we have 3 and we need to take 4, so we are one x short. "
      "That is minus x.",
      group("l2", ["3x", "− 4x"], "− x"), W("l3", "−x − 24 = 0")),
    B("We want a plain x, standing on its own. What could we do to both sides?",
      ask=choose(["add x to both sides", "take x from both sides", "divide both sides by 24"], 0,
                 "The x has a minus in front of it. Adding x to both sides undoes that minus x, "
                 "and puts a plain x on the right.")),
    B("Add x to both sides. On the left, minus x and plus x cancel, leaving minus 24. "
      "On the right, 0 plus x is just x.",
      strike("l3", "−x", "+ x"), both("l3", "+ x"), W("l4", "−24 = x")),
    B("So x equals minus 24. A negative answer is perfectly fine.",
      answer("l5", "x = −24"), mark("l5", "x = −24")),
    B("Check it. 3 times minus 24 is minus 72. Inside the bracket, minus 24 plus 6 is minus 18, "
      "and minus 4 times minus 18 is plus 72. Minus 72 plus 72 is 0.",
      W("l6", "3 × (−24) = −72"), W("l7", "−24 + 6 = −18"), W("l8", "−4 × (−18) = 72"), W("l9", "−72 + 72 = 0")),
    B("The plan: open the bracket, taking the minus sign to every term inside. "
      "Then gather the x terms and keep the balance."),
], "x", "−24")

# 4a − 5 = 2a + 3
LESSONS["EXT_G5_FP_2018_026"] = lesson([
    B("Here is our equation. 4 a, minus 5, equals 2 a, plus 3. This time the letter is on both sides.",
      given("l1", "4a − 5 = 2a + 3")),
    B("We want all the a terms on one side. Which move does that?",
      ask=choose(["move 2a across as + 2a", "take 2a from both sides", "add 2a to both sides"], 1,
                 "The 2 a on the right is a plus 2 a. To undo it we take 2 a away, "
                 "and we take it from both sides so the balance stays level.")),
    B("So we take 2 a from both sides. On the right it is gone. On the left, 4 a take away 2 a leaves 2 a.",
      strike("l1", "2a", "− 2a"), both("l1", "− 2a"), W("l2", "2a − 5 = 3")),
    B("Now it is one we know well. What is in the way of the 2 a?",
      ask=choose(["the 3", "the − 5", "the 2"], 1,
                 "Look at the left side. The 2 a has a minus 5 hanging on to it. That goes next.")),
    B("To undo minus 5 we add 5, to both sides. 3 plus 5 is 8, so 2 a equals 8.",
      strike("l2", "− 5", "+ 5"), both("l2", "+ 5"), W("l3", "2a = 3 + 5"), W("l4", "2a = 8")),
    B("2 a means 2 times a, so we divide both sides by 2. 8 divided by 2 is 4. So a equals 4.",
      divide("l4", "2"), answer("l5", "a = 4"), mark("l5", "a = 4")),
    B("Check both sides with a as 4. Left: 4 times 4, minus 5, is 11. Right: 2 times 4, plus 3, is 11. "
      "Both sides are 11, so it balances.",
      W("l6", "4 × 4 − 5 = 11"), W("l7", "2 × 4 + 3 = 11")),
    B("When the letter is on both sides: gather the letters on one side, then the numbers on the other, then divide."),
], "a", 4)

# (m + 6)/11 = m/9
LESSONS["EXT_G5_FP_2019_021"] = lesson([
    B("Here is an equation with fractions. m plus 6, all over 11, equals m over 9. "
      "Fractions are awkward, so first we get rid of them.",
      given("l1", "(m + 6)/11 = m/9")),
    B("Whatever we do to one side, we do to the other. If we multiply both sides by 11 and by 9, "
      "both bottoms disappear. People call this cross multiplying.",
      arc("l1", "9", "(m + 6)"), arc("l1", "11", ("m", 2)), W("l2", "9(m + 6) = 11m")),
    B("Now open the bracket. What does the 9 multiply?",
      ask=choose(["only the m", "both the m and the 6", "only the 6"], 1,
                 "The 9 is outside the bracket, so it multiplies everything inside: the m, and the 6 as well.")),
    B("9 times m is 9 m, and 9 times 6 is 54.",
      arc("l2", "9", "m", "6"), W("l3", "9m + 54 = 11m")),
    B("m is on both sides. Take the smaller lot, 9 m, away from both sides. "
      "On the right, 11 m take away 9 m leaves 2 m.",
      strike("l3", "9m", "− 9m"), both("l3", "− 9m"), W("l4", "54 = 2m")),
    B("54 equals 2 m. How do we find one m?",
      ask=choose(["take 2 from both sides", "divide both sides by 2", "multiply both sides by 2"], 1,
                 "2 m means 2 times m. Divide undoes times, so we halve both sides.")),
    B("Half of 54 is 27. So m equals 27.",
      divide("l4", "2"), answer("l5", "m = 27"), mark("l5", "m = 27")),
    B("Put 27 back. On the left, 27 plus 6 is 33, and 33 over 11 is 3. On the right, 27 over 9 is 3. "
      "Both sides are 3.",
      W("l6", "27 + 6 = 33"), W("l7", "33/11 = 3"), W("l8", "27/9 = 3")),
    B("With a fraction on each side, cross multiply to clear the bottoms. After that it is an ordinary equation."),
], "m", 27)

# 3x + 7 = 1 − 2x
LESSONS["EXT_G5_FP_2020_014"] = lesson([
    B("Here is our equation. 3 x, plus 7, equals 1, minus 2 x. There is an x on each side, "
      "so let's bring them together.",
      given("l1", "3x + 7 = 1 − 2x")),
    B("On the right there is a minus 2 x. How do we move it over to the left side?",
      ask=choose(["take 2x from both sides", "write − 2x on the left", "add 2x to both sides"], 2,
                 "To undo minus 2 x, we add 2 x. And we add it to both sides, so the balance stays level.")),
    B("Add 2 x to both sides. On the right it cancels, leaving 1. On the left, 3 x plus 2 x makes 5 x.",
      strike("l1", "− 2x", "+ 2x"), both("l1", "+ 2x"), W("l2", "5x + 7 = 1")),
    B("Now undo the plus 7, by taking 7 from both sides.",
      strike("l2", "+ 7", "− 7"), both("l2", "− 7"), W("l3", "5x = 1 − 7")),
    B("1 minus 7. We have 1, and we take away 7. Where do we land?",
      ask=choose(["6", "−6", "8"], 1,
                 "Taking 7 from 1 takes us below zero. From 1 down to 0 is 1 step, "
                 "then 6 more steps down. That lands on minus 6.")),
    B("So 5 x equals minus 6. The last move is the usual one: divide both sides by 5.",
      W("l4", "5x = −6"), divide("l4", "5")),
    B("Minus 6 divided by 5 does not come out as a whole number, so we leave it as a fraction. "
      "x equals minus 6 over 5.",
      answer("l5", "x = −6/5"), mark("l5", "x = −6/5")),
    B("Check with the tidy line, 5 x plus 7 equals 1. 5 times minus 6 over 5 is minus 6. "
      "And minus 6 plus 7 is 1. It works.",
      W("l6", "5 × (−6/5) + 7 = 1")),
    B("The plan: letters to one side, numbers to the other, each time by doing the opposite to both sides. "
      "And an answer can be a negative fraction."),
], "x", "−6/5")
