"""Algebra: which of these expressions has the value...? (eight textbook questions)."""
from imported_01_expr import option_line
from imported_01_lib import ANS, B, GIVEN, M, S, TB, W, choose, lesson

LESSONS = {}

# ── x = 0, y = 2: which has the value 10? ────────────────────────────────────
V = {"x": 0, "y": 2}
LESSONS[TB + "ch09_q007"] = lesson(
    B("x is 0 and y is 2. One of these four expressions comes to exactly 10, and we have to find which.",
      GIVEN("l1", "x = 0, y = 2. Which has the value 10?"),
      GIVEN("l2", "A: 3x + 2y   B: 5y + x   C: 3y − x   D: x + y")),
    B("Choice A starts with 3 x, and x is 0. What is 3 times 0?",
      ask=choose(["3", "0", "30"], 1, "3 times 0 means 3 lots of nothing. That is still nothing: 0.")),
    B("So in A, the 3 x part is 0. Then 2 y is 2 times 2, which is 4. And 0 plus 4 is 4. Not 10.",
      option_line("a", "A", [(3, "x"), (2, "y")], V, True)),
    B("B starts with 5 y. What does 5 y mean when y is 2?",
      ask=choose(["52", "5 + 2", "5 × 2"], 2,
                 "A number written right beside a letter means times. So 5 y is 5 times y, and with y as 2 that is 5 times 2.")),
    B("5 times 2 is 10. Then we add x, which adds 0. So B is exactly 10. This one works.",
      option_line("b", "B", [(5, "y"), (1, "x")], V, True), M("b", "10", "circle", 2)),
    B("Let's make sure of the other two. C: 3 times 2 is 6, and taking away 0 leaves 6.",
      option_line("c", "C", [(3, "y"), (-1, "x")], V, True)),
    B("And D is 0 plus 2, which is just 2.", option_line("d", "D", [(1, "x"), (1, "y")], V)),
    B("Only B reaches 10.", ANS("ans", "B: 5y + x = 10", True), M("ans", "5y + x", "circle")),
    B("Careful with a 0. Multiplying by 0 wipes that part out completely. But adding or taking away 0 changes nothing at all."),
    B("When the choices are expressions, put the numbers into each one and work it out. Then pick the one that hits the target."),
)

# ── a = 2, b = 4, c = 1: which is zero? ──────────────────────────────────────
V = {"a": 2, "b": 4, "c": 1}
LESSONS[TB + "ch09_q011"] = lesson(
    B("a is 2, b is 4 and c is 1. We want the expression that comes to zero.",
      GIVEN("l1", "a = 2, b = 4, c = 1. Which has the value zero?"),
      GIVEN("l2", "A: a + b + c   B: a − b + 2c   C: 2c + 2a − 2b")),
    B("A is all adding: 2 plus 4 plus 1 is 7. Adding these numbers can never bring us down to zero.",
      option_line("a", "A", [(1, "a"), (1, "b"), (1, "c")], V)),
    B("B is a, minus b, plus 2 c. With the numbers in, which sum is that?",
      ask=choose(["2 − 4 + 2 × 1", "2 − 4 + 21", "2 − (4 + 2 × 1)"], 0,
                 "Swap each letter for its number, and keep the signs where they are. 2 c means 2 times c, which is 2 times 1.")),
    B("2 times 1 is 2. So B is 2, minus 4, plus 2.", option_line("b", "B", [(1, "a"), (-1, "b"), (2, "c")], V, True)),
    B("2 minus 4 looks stuck, so think of it as in and out. In goes 2, and another 2, which is 4. Out goes 4. Nothing is left: zero.",
      W("b2", "2 + 2 − 4 = 0")),
    B("B gives zero. But look at C before deciding. 2 times 1 is 2, 2 times 2 is 4, and 2 times 4 is 8.",
      option_line("c", "C", [(2, "c"), (2, "a"), (-2, "b")], V, True)),
    B("In goes 2 plus 4, which is 6. Out goes 8. We take out 2 more than we put in, so C lands 2 below zero. Close, but not zero.",
      W("c2", "2 + 4 = 6")),
    B("So the answer is B.", ANS("ans", "B: a − b + 2c = 0", True), M("ans", "a − b + 2c", "circle")),
    B("Careful with None of these. It is only right when every other choice has been tried and has missed. Here B hits zero."),
    B("Put the numbers in, then compare what goes in with what comes out. Equal amounts in and out means zero."),
)

# ── a = 2, b = 3, c = 1: which is zero? ──────────────────────────────────────
V = {"a": 2, "b": 3, "c": 1}
LESSONS[TB + "ch09_q029"] = lesson(
    B("a is 2, b is 3 and c is 1. One of these may come to zero. Let's test them.",
      GIVEN("l1", "a = 2, b = 3, c = 1. Which has the value zero?"),
      GIVEN("l2", "A: a + b + c   B: a − b + 2c   C: 2c + 2a − 2b")),
    B("A: 2 plus 3 plus 1 is 6. It is all adding, so it had no chance of being zero.",
      option_line("a", "A", [(1, "a"), (1, "b"), (1, "c")], V)),
    B("B: a, minus b, plus 2 c. That is 2, minus 3, plus 2 times 1.",
      option_line("b", "B", [(1, "a"), (-1, "b"), (2, "c")], V, True)),
    B("In goes 2 and another 2, which is 4. Out goes 3. So 1 is left over. Close, but not zero."),
    B("Two misses. Is it time to choose None of these?",
      ask=choose(["Yes, two have missed", "No, test C first"], 1,
                 "None of these is only safe when every other choice has been tried. C is still waiting, so we test it.")),
    B("C: 2 c, plus 2 a, minus 2 b. 2 times 1 is 2, 2 times 2 is 4, and 2 times 3 is 6.",
      option_line("c", "C", [(2, "c"), (2, "a"), (-2, "b")], V, True)),
    B("In goes 2 plus 4, which is 6. Out goes 6. Nothing is left: zero.",
      ANS("ans", "C: 2c + 2a − 2b = 0", True), M("ans", "2c + 2a − 2b", "circle")),
    B("There is a neat reason too. Everything in C is doubled. Inside, c plus a is 3 and b is 3, so they cancel. And double nothing is still nothing.",
      W("why", "2 × (1 + 2 − 3) = 0")),
    B("Test every choice before you trust None of these. And to spot a zero, look for what goes in being equal to what comes out."),
)

# ── p = 5, q = 6: which equals 3p + q? ───────────────────────────────────────
V = {"p": 5, "q": 6}
LESSONS[TB + "ch09_q015"] = lesson(
    B("p is 5 and q is 6. We want the expression that has the same value as 3 p plus q.",
      GIVEN("l1", "p = 5, q = 6. Which has the same value as 3p + q?"),
      GIVEN("l2", "A: 2p + 3q   B: 2p + 2q − p   C: 5p + q − 10")),
    B("What do we need to do first?",
      ask=choose(["Test choice A", "Find the value of 3p + q", "Pick the one that looks like 3p + q"], 1,
                 "We are hunting for a match. Before we can match anything, we need the target: the value of 3 p plus q.")),
    B("3 times 5 is 15, and 15 plus 6 is 21. So 21 is our target.",
      W("t", "3 × 5 + 6 = 15 + 6 = 21"), M("t", "21", "box")),
    B("A: 2 times 5 is 10, and 3 times 6 is 18. 10 plus 18 is 28. Too big.",
      option_line("a", "A", [(2, "p"), (3, "q")], V, True)),
    B("B: 2 times 5 is 10, 2 times 6 is 12, and then we take away p, which is 5. 10 plus 12, minus 5, is 17. Too small.",
      option_line("b", "B", [(2, "p"), (2, "q"), (-1, "p")], V, True)),
    B("C: 5 times 5 is 25. Add q, which is 6, then take away 10. 25 plus 6, minus 10, is 21. A match!",
      option_line("c", "C", [(5, "p"), (1, "q"), (-10, "")], V, True)),
    B("So C has the same value as 3 p plus q.", ANS("ans", "C: 5p + q − 10 = 21", True), M("ans", "5p + q − 10", "circle")),
    B("Careful: C looks nothing like 3 p plus q, and A looks much more like it. Looks do not matter here. Only the value does."),
    B("Here is why C works. It has 2 more p than the target, and 2 times 5 is 10. Then it takes that 10 straight back off.",
      W("why", "2 × 5 − 10 = 0")),
    B("Find the target value first. Then work out each choice and look for the same number."),
)

# ── g = 2, h = 3: which is greater than 10? ──────────────────────────────────
V = {"g": 2, "h": 3}
LESSONS[TB + "ch09_q016"] = lesson(
    B("g is 2 and h is 3. We want the expression whose value is greater than 10.",
      GIVEN("l1", "g = 2, h = 3. Which has a value greater than 10?"),
      GIVEN("l2", "A: 2g + 2h   B: g + h − 3   C: gh − 6   D: 2g + 3h")),
    B("A: 2 times 2 is 4, and 2 times 3 is 6. 4 plus 6 is 10.", option_line("a", "A", [(2, "g"), (2, "h")], V, True)),
    B("A comes to exactly 10. Is that greater than 10?",
      ask=choose(["Yes, 10 counts", "No, it must be more than 10"], 1,
                 "Greater than 10 means past 10, not on it. 10 is equal to 10, so A just misses.")),
    B("That is the trap in this question. A lands right on 10, and it is the first one you try. So we keep going."),
    B("B: 2 plus 3 is 5, and 5 minus 3 is 2. Far too small.", option_line("b", "B", [(1, "g"), (1, "h"), (-3, "")], V)),
    B("C has g h: two letters side by side. What does g h mean?",
      ask=choose(["g + h", "the number 23", "g × h"], 2,
                 "Letters written side by side are multiplied, just like a number beside a letter. So g h is g times h, which is 2 times 3.")),
    B("So C is 2 times 3, which is 6, minus 6. That is 0.", option_line("c", "C", [(1, "gh"), (-6, "")], V, True)),
    B("D: 2 times 2 is 4, and 3 times 3 is 9. 4 plus 9 is 13, and 13 is greater than 10.",
      option_line("d", "D", [(2, "g"), (3, "h")], V, True)),
    B("So the answer is D.", ANS("ans", "D: 2g + 3h = 13, and 13 > 10", True), M("ans", "2g + 3h", "circle")),
    B("Work out every choice, then read the question's words with care. Greater than means strictly more."),
)

# ── l = 2, m = −3, n = −1: which is −14? ─────────────────────────────────────
V = {"l": 2, "m": -3, "n": -1}
LESSONS[TB + "ch09_q021"] = lesson(
    B("Three letters, and two of them stand for numbers below zero. We want the expression that comes to minus 14.",
      GIVEN("l1", "l = 2, m = −3, n = −1. Which has the value −14?"),
      GIVEN("l2", "A: 2l + 3m − n   B: −2l + 4m − 2n"), GIVEN("l3", "C: 5l − 4m − n   D: −l − 2m + n")),
    B("Two sign rules will carry us through. A plus number times a minus number gives a minus. And taking away a minus number is the same as adding.",
      W("r1", "plus × minus = minus", label=True), W("r2", "taking away a minus = adding", label=True)),
    B("A: 2 times 2 is 4. 3 times minus 3 is minus 9. And taking away minus 1 adds 1. So 4, minus 9, plus 1: that is minus 4, not minus 14.",
      option_line("a", "A", [(2, "l"), (3, "m"), (-1, "n")], V, True)),
    B("Now B, one part at a time. Minus 2 times 2 is minus 4. And 4 times minus 3 is minus 12.",
      W("b1", "−2 × 2 = −4"), W("b2", "4 × (−3) = −12")),
    B("The last part of B takes away 2 n. 2 times minus 1 is minus 2. So what does taking away minus 2 do?",
      ask=choose(["Takes away 2", "Adds 2", "Changes nothing"], 1,
                 "Taking away a debt leaves you better off. So taking away minus 2 is the same as adding 2.")),
    B("So B is minus 4, minus 12, plus 2. Down 4 and down 12 is down 16. Then up 2 leaves us at minus 14.",
      W("b3", "−4 − 12 = −16"), option_line("b", "B", [(-2, "l"), (4, "m"), (-2, "n")], V, True)),
    B("B hits minus 14. A quick look at the others: C is 10, plus 12, plus 1, which is 23. D is minus 2, plus 6, minus 1, which is 3. Both are above zero.",
      option_line("c", "C", [(5, "l"), (-4, "m"), (-1, "n")], V, True),
      option_line("d", "D", [(-1, "l"), (-2, "m"), (1, "n")], V, True)),
    B("So the answer is B.", ANS("ans", "B: −2l + 4m − 2n = −14", True), M("ans", "−2l + 4m − 2n", "circle")),
    B("The trap is the last part of B. Forget that taking away a minus adds, and you go down 2 instead of up 2, and miss the target."),
    B("With numbers below zero, slow down at every sign. Bracket them when you swap them in, and remember that taking away a minus adds."),
)

# ── x = 9, y = 2: which is NOT 14? ───────────────────────────────────────────
V = {"x": 9, "y": 2}
LESSONS[TB + "ch09_q026"] = lesson(
    B("x is 9 and y is 2. Three of these expressions come to 14. We want the odd one out: the one that does not.",
      GIVEN("l1", "x = 9, y = 2. Which is NOT equal to 14?"),
      GIVEN("l2", "A: x + y + 3   B: x + 2y + 1"), GIVEN("l3", "C: 2x − 2y   D: 2x + 2y − 7")),
    B("A: 9 plus 2 plus 3 is 14.", option_line("a", "A", [(1, "x"), (1, "y"), (3, "")], V)),
    B("A comes to 14. So is A our answer?",
      ask=choose(["Yes, it gives 14", "No, we want the one that misses 14"], 1,
                 "Read the question again: it asks for the one that is not equal to 14. A hits 14, so A is safe, and we move on.")),
    B("That is the trap in a NOT question. The first choice that hits 14 feels like the answer. Here, hitting 14 means we cross it out.",
      S("l2", "A: x + y + 3")),
    B("B: 2 times 2 is 4. Then 9 plus 4 plus 1 is 14 again. Cross it out.",
      option_line("b", "B", [(1, "x"), (2, "y"), (1, "")], V, True), S("l2", "B: x + 2y + 1")),
    B("C: 2 times 9 is 18, and 2 times 2 is 4. 18 minus 4 is 14. Cross it out too.",
      option_line("c", "C", [(2, "x"), (-2, "y")], V, True), S("l3", "C: 2x − 2y")),
    B("Only D is left. But we never guess, so work it out: 18 plus 4, minus 7, is 15. Not 14.",
      option_line("d", "D", [(2, "x"), (2, "y"), (-7, "")], V, True)),
    B("So D is the one that is not equal to 14.",
      ANS("ans", "D: 2x + 2y − 7 = 15, not 14", True), M("ans", "2x + 2y − 7", "circle")),
    B("In a NOT question, work out every choice, cross out the ones that hit the target, and keep the one that misses."),
)

# ── x = 5, y = 3, z = −2: which is 12? ───────────────────────────────────────
V = {"x": 5, "y": 3, "z": -2}
LESSONS[TB + "ch09_q027"] = lesson(
    B("x is 5, y is 3, and z is a number below zero: minus 2. We want the expression equal to 12.",
      GIVEN("l1", "x = 5, y = 3, z = −2. Which is equal to 12?"),
      GIVEN("l2", "A: 2x + 3y − 2z   B: 5x − 3y + 2z"), GIVEN("l3", "C: 4x − 3y + z   D: x + y + z")),
    B("Start with the simplest one, D. 5 plus 3 is 8, and adding minus 2 takes 2 off. That is 6, not 12.",
      option_line("d", "D", [(1, "x"), (1, "y"), (1, "z")], V, True)),
    B("A ends by taking away 2 z. 2 times minus 2 is minus 4. So what does taking away minus 4 do?",
      ask=choose(["Takes away 4", "Adds 4"], 1,
                 "Taking away a debt of 4 leaves you 4 better off. So taking away minus 4 is the same as adding 4.")),
    B("So A is 10, plus 9, plus 4. That is 23, far past 12.",
      option_line("a", "A", [(2, "x"), (3, "y"), (-2, "z")], V, True)),
    B("B: 5 times 5 is 25, and 3 times 3 is 9. Then 2 times minus 2 is minus 4, and adding minus 4 takes 4 off.",
      W("b0", "5 × 5 − 3 × 3 + 2 × (−2) = 25 − 9 − 4")),
    B("25 minus 9 is 16, and 16 minus 4 is 12. That is our target.",
      W("b1", "25 − 9 = 16"), W("b2", "16 − 4 = 12"), M("b2", "12", "circle")),
    B("And C, to be sure: 20, minus 9, minus 2, is 9. Not 12.", option_line("c", "C", [(4, "x"), (-3, "y"), (1, "z")], V, True)),
    B("So the answer is B.", ANS("ans", "B: 5x − 3y + 2z = 12", True), M("ans", "5x − 3y + 2z", "circle")),
    B("Careful with z. Treat it as plus 2 and B comes out too big. The minus sign travels with the number wherever z goes."),
    B("Swap in the numbers, brackets round the one below zero. Adding a minus pulls the total down, and taking away a minus pushes it up."),
)
