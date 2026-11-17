"""Imported batch 07, part e: the textbook questions (consecutive numbers, ages, words into equations, plain equations, formulas)."""
from imported_07_lib import ANS, B, BOTH, DIV, E, G, GIVEN, M, N, S, W, choose, lesson, pick, placed, tail

P = "IPMTB_grade5_"
LESSONS = {}

# ── 6 consecutive even numbers add up to 78 ──────────────────────────────────
qid = P + "ch01_q043"
LESSONS[qid] = lesson(
    B("6 even numbers in a row add up to 78. We want the smallest of them.",
      GIVEN("q", "6 consecutive even numbers, sum 78. Smallest = ?", True)),
    B("Think of even numbers in a row, like 2, 4, 6. How far is it from one to the next?",
      ask=choose(["1", "2", "10"], 1,
                 "Even numbers skip the odd ones in between. From 2 to 4, from 4 to 6: each jump is 2.")),
    B("So if the smallest is n, the next is n plus 2, then n plus 4, and so on up to n plus 10. Careful: with jumps of 1, odd numbers would sneak into the list.",
      W("e", "n + (n + 2) + (n + 4) + (n + 6) + (n + 8) + (n + 10) = 78")),
    B("Count the letters: there are 6 lots of n, so 6 n. Then the extras: 2, 4, 6, 8 and 10 add up to 30.",
      W("s", "2 + 4 + 6 + 8 + 10 = 30"), W("e2", "6n + 30 = 78")),
    tail(qid, "n", 6, 30, 78, "e2", found="The smallest number is 8."),
    B("Check. The 6 numbers are 8, 10, 12, 14, 16 and 18. Add them up and we get 78.",
      W("c", "8 + 10 + 12 + 14 + 16 + 18 = 78")),
    B("So: call the smallest one n, write the others by adding 2 each time, add them all up, and solve."),
    check=("n", 8))

# ── 3 consecutive natural numbers add up to 60 ───────────────────────────────
qid = P + "ch01_q044"
LESSONS[qid] = lesson(
    B("3 natural numbers in a row add up to 60. We want the middle one.",
      GIVEN("q", "3 consecutive natural numbers, sum 60. Middle = ?", True)),
    B("Here is a neat trick: give the letter to the middle number. Call it n. Then the one before is n minus 1, and the one after is n plus 1.",
      W("e", "(n − 1) + n + (n + 1) = 60"), N("e", ("n", 2), "middle", "below")),
    B("Look at the minus 1 and the plus 1. What happens to them when we add everything up?",
      ask=choose(["they make 2", "they cancel out", "they make minus 2"], 1,
                 "One number is 1 below n and the other is 1 above. Take 1 off, put 1 on, and you are back where you started. They cancel.")),
    B("So the minus 1 and the plus 1 vanish, and we are left with 3 lots of n. 3 n equals 60.",
      S("e", "− 1"), S("e", "+ 1"), W("e2", "3n = 60")),
    B("3 n means 3 times n. How do we find n?",
      ask=choose(["subtract 3", "divide by 3", "multiply by 3"], 1,
                 "Times and divide are partners. To undo times 3, we divide both sides by 3.")),
    B("60 divided by 3 is 20. The middle number is 20.",
      DIV("e2", 3), ANS("a", "n = 20"), M("a", "n = 20", "circle")),
    B("Check. The numbers are 19, 20 and 21. And 19 plus 20 plus 21 is 60.",
      W("c", "19 + 20 + 21 = 60")),
    B("For 3 numbers in a row, the middle one is the total divided by 3. Giving the letter to the middle number made everything else cancel."),
    check=("n", 20))

# ── Ages after 10 years: (x + 10) + (x + 15) = 55 ────────────────────────────
qid = P + "ch05_q034"
LESSONS[qid] = lesson(
    B("Sunita is 5 years older than Kavita. In 10 years, their ages will add up to 55. We want their ages now.",
      GIVEN("q", "Sunita = Kavita + 5.   In 10 years, ages add to 55.", True)),
    B("Call Kavita's age now x. Sunita is 5 years older, so she is x plus 5.",
      W("k", "Kavita now: x", label=True), W("s", "Sunita now: x + 5", label=True)),
    B("Now jump 10 years ahead. Kavita will be x plus 10. How old will Sunita be?",
      ask=choose(["x + 5", "x + 10", "x + 15"], 2,
                 "Sunita is x plus 5 now. In 10 years she is 10 older as well: x plus 5 plus 10, which is x plus 15.")),
    B("Careful: both of them grow 10 years older, not just one. So they will be x plus 10 and x plus 15, and together that is 55.",
      W("e", "(x + 10) + (x + 15) = 55")),
    B("Gather like terms. x and x make 2 x. And 10 and 15 make 25.",
      G("e", ["x", ("x", 2)], "2x"), G("e", ["10", "15"], "25"), W("e2", "2x + 25 = 55")),
    tail(qid, "x", 2, 25, 55, "e2", final=False, found="Kavita is 15 now."),
    B("And Sunita is 5 years older. 15 plus 5 is 20. So Kavita is 15 years old and Sunita is 20.",
      W("s2", "15 + 5 = 20"), ANS("a", "Kavita 15 years, Sunita 20 years", True),
      M("a", "Kavita 15 years, Sunita 20 years", "circle")),
    B("Check. In 10 years they will be 25 and 30. And 25 plus 30 is 55. It works.",
      W("c1", "15 + 10 = 25"), W("c2", "20 + 10 = 30"), W("c3", "25 + 30 = 55")),
    B("For an age puzzle: write the ages now with one letter, move everyone forward together, then add and solve."),
    check=("x", 15))

# ── Words into an equation: a number divided by 7 gives 25 ───────────────────
qid = P + "ch08_q002"
LESSONS[qid] = lesson(
    B("This one asks us to turn a sentence into an equation. A number, when divided by 7, gives 25.",
      GIVEN("q", "A number divided by 7 gives 25", True)),
    B("We don't know the number, so we call it x. Now we translate the sentence, one piece at a time.",
      N("q", "A number", "x")),
    B("The number divided by 7. How do we write that?",
      ask=choose(["7 ÷ x", "7x", "x ÷ 7"], 2,
                 "The number is the thing being divided, so it comes first: x divided by 7. And 7 x would mean 7 times the number.")),
    B("x divided by 7. In the choices the divide is written as a sloping line, like a fraction with x on top and 7 underneath. It means the same thing.",
      E("p", "x ÷ 7", "x", 175), N("q", "divided by 7", "÷ 7")),
    B("And gives 25 means the result equals 25. So the equation is x divided by 7 equals 25.",
      N("q", "gives 25", "= 25"), E("a", "x ÷ 7 = 25", "x", 175, tone="answer"), M("a", "x ÷ 7 = 25", "circle")),
    B("Careful with the order. Swap the 7 and the 25, or turn the divide into a times, and the equation describes a different number. Each piece must stay where the sentence put it."),
    B("Let's test it. If x divided by 7 is 25, then x is 25 times 7, which is 175. And 175 divided by 7 is 25, just as the sentence says.",
      W("c1", "25 × 7 = 175"), W("c2", "175 ÷ 7 = 25")),
    B("So: name the unknown, then translate each phrase in order. Divided by 7 becomes the divide sign and a 7. Gives 25 becomes equals 25."),
)

# ── A one step equation: x − 5 = 1 ───────────────────────────────────────────
qid = P + "ch08_q007"
LESSONS[qid] = lesson(
    B("A short equation. x minus 5 equals 1. Some number, with 5 taken away, leaves 1.",
      GIVEN("q", "x − 5 = 1")),
    B("We want x by itself. What undoes minus 5?",
      ask=choose(["subtract 5", "add 5", "divide by 5"], 1,
                 "Minus 5 took 5 away. To get it back, we add 5. Adding undoes subtracting.")),
    B("And to keep the balance level, we add 5 to both sides.",
      S("q", "− 5", "+ 5"), BOTH("q", "+ 5"), W("l2", "x − 5 + 5 = 1 + 5")),
    B("On the left, minus 5 and plus 5 cancel, leaving just x. On the right, 1 plus 5 is 6. So x equals 6.",
      ANS("a", "x = 6"), M("a", "x = 6", "circle")),
    B("Careful: a common slip is to take 5 away again, or to work out 5 minus 1 and say 4. We are undoing a minus, so we add."),
    B("Check. Put 6 in place of x. 6 minus 5 is 1. It works.",
      W("c", "6 − 5 = 1")),
    B("For a one step equation, do the opposite of what was done to x, and do it to both sides."),
    check=("x", 6))


# ── x on both sides, no story: a1·x + b1 = a2·x + b2 ─────────────────────────
def plain_both(qid, a1, b1, a2, b2, asks):
    a, c = a1 - a2, b2
    x = (b2 - b1) // a
    side = a1 * x + b1
    assert side == a2 * x + b2
    eq = "%dx + %d = %dx + %d" % (a1, b1, a2, b2)
    right = "take %dx from both sides" % a2
    choices, idx = placed(qid, "m", right, ["take %dx from the right only" % a2, "add %dx to both sides" % a2])
    return lesson(
        B(pick(qid, "i", [
            "Here is our equation. %d x plus %d equals %d x plus %d. This time x is on both sides." % (a1, b1, a2, b2),
            "%d x plus %d equals %d x plus %d. Notice that x appears on both sides of the equals sign." % (a1, b1, a2, b2)]),
          GIVEN("q", eq)),
        B("We want all the x terms on one side. Which move does that?",
          ask=choose(choices, idx,
                     "Whatever we do, we do to both sides. Taking %d x from both sides clears the x from the right, and still leaves some on the left." % a2)),
        B("Take %d x from both sides. On the left, %d x minus %d x is %d x. On the right, the %d x is gone." % (a2, a1, a2, a, a2),
          S("q", "%dx" % a2, "− %dx" % a2), BOTH("q", "− %dx" % a2), W("e2", "%dx + %d = %d" % (a, b1, c))),
        tail(qid, "x", a, b1, c, "e2", asks=asks),
        B("Check both sides with x as %d. Left: %d times %d, plus %d, is %d. Right: %d times %d, plus %d, is %d. Both sides agree." % (x, a1, x, b1, side, a2, x, b2, side),
          W("c1", "%d × %d + %d = %d" % (a1, x, b1, side)), W("c2", "%d × %d + %d = %d" % (a2, x, b2, side))),
        B(pick(qid, "s", [
            "Careful not to stop at %d x equals %d and say %d. That is %d lots of x. Collect the x terms, clear the loose number, then divide." % (a, c - b1, c - b1, a),
            "One trap: %d x equals %d is not the end, because that is %d lots of x. So the plan is to collect the x terms, clear the loose number, then divide." % (a, c - b1, a)])),
        check=("x", x))


LESSONS[P + "ch08_q013"] = plain_both(P + "ch08_q013", 5, 7, 3, 17, ("clear",))

# ── Two ages that add up: x + (x + 5) = 25 ───────────────────────────────────
qid = P + "ch08_q014"
LESSONS[qid] = lesson(
    B("Rekha is 5 years older than Madhavi, and their ages add up to 25 years. We want both ages.",
      GIVEN("q", "Rekha = Madhavi + 5.   Sum of ages = 25.", True)),
    B("Let's give the letter x to the younger girl. Who is that?",
      ask=choose(["Rekha", "Madhavi"], 1,
                 "Rekha is 5 years older, so Rekha has the bigger age. The younger one is Madhavi.")),
    B("So Madhavi is x. And Rekha, 5 years older, is x plus 5.",
      W("m", "Madhavi: x", label=True), W("r", "Rekha: x + 5", label=True)),
    B("Their ages add up to 25. x and x make 2 x, so 2 x plus 5 equals 25.",
      W("e", "x + (x + 5) = 25"), G("e", ["x", ("x", 2)], "2x"), W("e2", "2x + 5 = 25")),
    tail(qid, "x", 2, 5, 25, "e2", final=False, found="Madhavi is 10 years old."),
    B("Rekha is 5 years older. 10 plus 5 is 15. So Rekha is 15 and Madhavi is 10.",
      W("r2", "10 + 5 = 15"), ANS("a", "Rekha = 15 years, Madhavi = 10 years", True),
      M("a", "Rekha = 15 years, Madhavi = 10 years", "circle")),
    B("Check. 15 plus 10 is 25, and 15 is 5 more than 10. Careful when you pick the choice: one has the right numbers with the names swapped. Rekha must be the older one.",
      W("c", "15 + 10 = 25")),
    B("For two ages: give the letter to the younger, write the older from it, add, and solve."),
    check=("x", 10))

# ── Words into an equation: a number multiplied by 4 gives 20 ────────────────
qid = P + "ch08_q016"
LESSONS[qid] = lesson(
    B("Here we turn words into an equation. A number, when multiplied by 4, gives 20.",
      GIVEN("q", "A number multiplied by 4 gives 20", True)),
    B("The number is unknown, so let's call it x.",
      N("q", "A number", "x")),
    B("Multiplied by 4. Which piece of maths says that about x?",
      ask=choose(["x + 4", "x × 4", "x ÷ 4"], 1, "Multiplied means times. So it is x times 4.")),
    B("x times 4. Now the word gives. It tells us what the result is, so it turns into the equals sign.",
      E("p", "x × 4", "x", 5), N("q", "multiplied by 4", "× 4"), N("q", "gives", "=")),
    B("So what goes on the other side of the equals sign?",
      ask=choose(["4", "20", "1/20"], 1,
                 "The sentence says the result is 20. Nothing has been turned upside down, so it is plain 20.")),
    B("x times 4 equals 20. In the choices, the times sign is written as a little star.",
      E("a", "x × 4 = 20", "x", 5, tone="answer"), M("a", "x × 4 = 20", "circle")),
    B("Test it with a number. 5 times 4 is 20. So x would be 5, and the equation says exactly what the sentence says.",
      W("c", "5 × 4 = 20")),
    B("Careful: the 4 and the 20 must stay where the sentence put them. Swap them and you describe a different number. So translate each phrase in order."),
)

# ── Words into an equation: a number subtracted from 15 gives 4 ──────────────
qid = P + "ch08_q018"
LESSONS[qid] = lesson(
    B("Words into an equation again. A number is subtracted from 15, and we get 4.",
      GIVEN("q", "A number is subtracted from 15, we get 4", True)),
    B("Call the number x. Now the tricky part: subtracted from 15. Try it with a real number. If 3 is subtracted from 15, what do we write?",
      N("q", "A number", "x"),
      ask=choose(["3 − 15", "15 − 3"], 1,
                 "Subtracted from 15 means we start with 15 and take the number away. So the 15 comes first: 15 minus 3.")),
    B("So we start with 15 and take away. With 3 it is 15 minus 3. With our unknown number, it is 15 minus x.",
      W("t", "15 − 3", label=True), E("p", "15 − x", "x", 11)),
    B("Careful, this is the classic trap. The words name the number first, but the maths puts the 15 first. x minus 15 would mean taking 15 away from the number.",
      M("p", "15")),
    B("We get 4 means the result equals 4. So the equation is 15 minus x equals 4.",
      N("q", "we get 4", "= 4"), E("a", "15 − x = 4", "x", 11, tone="answer"), M("a", "15 − x = 4", "circle")),
    B("Let's test our equation. Which number, taken away from 15, leaves 4?",
      ask=choose(["19", "11", "4"], 1, "Count up from 4 to 15, or work out 15 minus 4. Both give 11.")),
    B("15 minus 11 is 4. So the equation works, with x as 11.",
      W("c", "15 − 11 = 4")),
    B("So when you read subtracted from, start with the number that comes after the word from. Then take the other one away."),
)

LESSONS[P + "ch08_q026"] = plain_both(P + "ch08_q026", 6, 8, 4, 18, ("div",))

# ── Tidy one side first: y × 6 = 36 ÷ 6 ──────────────────────────────────────
qid = P + "ch08_q030"
LESSONS[qid] = lesson(
    B("Here is our equation. y times 6 equals 36 divided by 6. Notice there is a sum waiting on the right hand side.",
      GIVEN("q", "y × 6 = 36 ÷ 6")),
    B("What should we do first?",
      ask=choose(["say y is 36", "work out 36 ÷ 6", "multiply 36 by 6"], 1,
                 "The right hand side is not finished yet. 36 divided by 6 is a sum we can simply work out. Do that first, and the equation gets much shorter.")),
    B("36 divided by 6 is 6. So the equation is really y times 6 equals 6.",
      M("q", "36 ÷ 6"), W("r", "36 ÷ 6 = 6"), W("e2", "y × 6 = 6")),
    B("y times 6 gives 6. What undoes times 6?",
      ask=choose(["divide by 6", "subtract 6", "multiply by 6"], 0,
                 "Times and divide are partners. To undo times 6, we divide both sides by 6.")),
    B("Divide both sides by 6. 6 divided by 6 is 1. So y equals 1.",
      DIV("e2", 6), ANS("a", "y = 1"), M("a", "y = 1", "circle")),
    B("Does 1 feel like an odd answer? It is fine. 1 times any number leaves it unchanged, so 1 times 6 is 6, and both sides match.",
      W("c", "1 × 6 = 36 ÷ 6")),
    B("Careful: the slip here is to see 36 and pick it, or to stop at 6. But 6 is the value of the right hand side, not the value of y."),
    B("So: tidy each side first, then undo what is being done to the letter."),
    check=("y", 1))

# ── Put in a value: 16x − 7y = 77 with x = 7 ─────────────────────────────────
qid = P + "ch09_q002"
LESSONS[qid] = lesson(
    B("Two letters this time. 16 x minus 7 y equals 77. But we are told that x is 7, so only y is unknown.",
      GIVEN("q", "16x − 7y = 77,   x = 7", True)),
    B("x is 7. So what does 16 x become?",
      ask=choose(["167", "16 × 7", "16 + 7"], 1,
                 "16 x means 16 times x. A number written next to a letter is multiplying it. So with x as 7, it is 16 times 7.")),
    B("Put 7 in place of x. Careful: only the x becomes 7. The 7 in front of the y stays just as it is.",
      M("q", "16x"), W("e1", "16 × 7 − 7y = 77")),
    B("16 times 7 is 112. So 112 minus 7 y equals 77.",
      W("m", "16 × 7 = 112"), W("e2", "112 − 7y = 77")),
    B("112, take away something, leaves 77. How big is that something?",
      ask=choose(["112 + 77", "112 − 77", "77 − 7"], 1,
                 "If taking 7 y away from 112 leaves 77, then 7 y is the gap between 112 and 77. That is 112 minus 77.")),
    B("So 7 y equals 112 minus 77, which is 35.",
      W("e3", "7y = 112 − 77"), W("e4", "7y = 35")),
    B("7 y means 7 times y, so we divide both sides by 7. 35 divided by 7 is 5. So y equals 5.",
      DIV("e4", 7), ANS("a", "y = 5"), M("a", "y = 5", "circle")),
    B("Check. 16 times 7 is 112, and 7 times 5 is 35. 112 minus 35 is 77. It works.",
      W("c", "16 × 7 − 7 × 5 = 77")),
    B("When you are given the value of one letter, put it in straight away. Then you have an ordinary equation in the other letter."),
    check=("y", 5))

# ── A rule with three letters: a = b × c, then a + c ─────────────────────────
qid = P + "ch09_q013"
LESSONS[qid] = lesson(
    B("We have a rule: a equals b times c. We are told a is 15 and b is 5, and we want a plus c.",
      GIVEN("q", "a = b × c,   a = 15,   b = 5", True)),
    B("Put in the numbers we know. a becomes 15, and b becomes 5.",
      E("e", "15 = 5 × c", "c", 3), N("e", "15", "a"), N("e", ("5", 2), "b")),
    B("15 equals 5 times c. How do we find c?",
      ask=choose(["15 − 5", "15 ÷ 5", "15 × 5"], 1,
                 "5 times c makes 15. To undo times 5, we divide by 5. So c is 15 divided by 5.")),
    B("15 divided by 5 is 3. So c is 3.",
      DIV("e", 5), E("c", "c = 3", "c", 3), M("c", "c = 3", "box")),
    B("Are we finished?",
      ask=choose(["Yes, the answer is 3", "No, we still need a + c"], 1,
                 "Look back at the question. It asks for a plus c, not just c.")),
    B("Careful: finding c is only half the job. The question wants a plus c. a is 15 and c is 3, so 15 plus 3 is 18.",
      ANS("a", "15 + 3 = 18"), M("a", "18", "circle")),
    B("Check the rule with our numbers. b times c is 5 times 3, which is 15, and that is a. So c is right, and a plus c is 18.",
      W("k", "5 × 3 = 15")),
    B("So: put the known values into the rule, find the missing letter, and then answer the question that was asked."),
)

# ── A formula: D = S × T ─────────────────────────────────────────────────────
qid = P + "ch09_q014"
LESSONS[qid] = lesson(
    B("Here is a formula: D equals S times T. We know D is 70 and T is 10, and we want S.",
      GIVEN("q", "D = S × T,   D = 70,   T = 10", True)),
    B("Put the numbers we know into the formula. D becomes 70, and T becomes 10.",
      E("e", "70 = S × 10", "S", 7), N("e", "70", "D"), N("e", "10", "T")),
    B("70 equals S times 10. Which move finds S?",
      ask=choose(["70 × 10", "70 ÷ 10", "70 − 10"], 1,
                 "S is being multiplied by 10. To undo times 10, we divide by 10. Multiplying again would only make the number bigger.")),
    B("Divide both sides by 10. 70 divided by 10 is 7. So S is 7.",
      DIV("e", 10), E("a", "S = 7", "S", 7, tone="answer"), M("a", "S = 7", "circle")),
    B("Careful: the formula has a times sign in it, so it is tempting to multiply 70 by 10. But 70 is already the result of the multiplying. We are working backwards."),
    B("Check. Put 7 back in. 7 times 10 is 70, and that is D. It works.",
      W("c", "7 × 10 = 70")),
    B("With a formula, put in what you know. If the missing letter is being multiplied, divide to find it."),
)
