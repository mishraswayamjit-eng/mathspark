"""Lessons written one by one: the past-paper questions EXT_G4_FP_...

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, E, L, T, W, answer, arc, balance, bars, both, choose, divide, fig, given, group,
                                  lesson, mark, note, strike)

LESSONS = {}

# Find x: 3x − 7 = 8 − 2x
LESSONS["EXT_G4_FP_2020_005"] = lesson([
    B("Here is our equation. 3 x, minus 7, equals 8, minus 2 x. Look: the x is on both sides.",
      given("l1", "3x − 7 = 8 − 2x")),
    B("We want all the x on one side. On the right, 2 x is being taken away.", mark("l1", "2x", "underline")),
    B("How do we clear the minus 2 x from the right?",
      ask=choose(["add 2x to both sides", "take 2x from both sides", "add 7 to both sides"], 0,
                 "The 2 x is being taken away. To undo taking away, we add. So we add 2 x to both sides.")),
    B("We add 2 x to both sides. On the left, 3 x and 2 x make 5 x. On the right, only 8 is left.",
      strike("l1", "− 2x", "+ 2x"), both("l1", "+ 2x"), W("l2", "5x − 7 = 8")),
    B("Now it is a two-step equation. What next?",
      ask=choose(["add 7 to both sides", "take 7 from both sides", "divide by 5 first"], 0,
                 "The 7 is being taken away on the left. To undo it, we add 7 to both sides.")),
    B("8 plus 7 is 15. So 5 x equals 15.",
      strike("l2", "− 7", "+ 7"), both("l2", "+ 7"), W("l3", "5x = 15")),
    B("Careful: 15 is 5 x, not x. We divide both sides by 5. 15 divided by 5 is 3. So x equals 3.",
      divide("l3", 5), answer("l4", "x = 3"), mark("l4", "x = 3", "circle")),
    B("Let's check. Left: 3 times 3 is 9, and 9 minus 7 is 2. Right: 2 times 3 is 6, and 8 minus 6 is 2. "
      "Both sides are 2!", W("l5", "3 × 3 − 7 = 2"), W("l6", "8 − 2 × 3 = 2")),
    B("So when x is on both sides, first bring the x together. Then solve the two-step equation."),
], "x", 3)

# Sum of 2 natural numbers = 16, difference = 8. Product?
LESSONS["EXT_G4_FP_2021_028"] = lesson([
    B("Two numbers add up to 16, and their difference is 8. We must find their product. "
      "So first we need the two numbers.", given("g1", "Sum = 16, difference = 8", label=True)),
    B("Look at the bars. The bigger number is the smaller number, and 8 more.",
      bars("f1", ("Bigger", [(4, "?", "unknown"), (8, "8", "c")]), ("Smaller", [(4, "?", "unknown")]))),
    B("If we take that extra 8 away from the total of 16, what is left?",
      ask=choose(["two lots of the smaller number", "the bigger number", "the product"], 0,
                 "Without the extra 8, the two bars are the same length. "
                 "So what is left is two lots of the smaller number.")),
    B("16 minus 8 is 8. Two lots of the smaller number make 8, so the smaller number is 4.",
      W("l1", "16 − 8 = 8"), W("l2", "8 ÷ 2 = 4")),
    B("The bigger number is 8 more than 4. That is 12.", W("l3", "4 + 8 = 12")),
    B("Quick check. 12 plus 4 is 16, and 12 minus 4 is 8. Both clues fit.",
      W("l4", "12 + 4 = 16"), W("l5", "12 − 4 = 8")),
    B("Now, what does the question ask for?",
      ask=choose(["12 times 4", "12 plus 4", "8 times 8"], 0,
                 "Product means the answer when we multiply. So we multiply our two numbers, 12 and 4.")),
    B("12 times 4. 10 times 4 is 40, and 2 times 4 is 8. Together that is 48.",
      W("l6", "12 × 4 = 40 + 8"), answer("l7", "12 × 4 = 48"), mark("l7", "48", "circle")),
    B("Careful with 8 times 8. Two 8s do add up to 16, but they are not 8 apart. "
      "Find the two numbers first, then multiply."),
])

# 1/3 + 1/2 + 1/x = 4
LESSONS["EXT_G4_FP_2021_036"] = lesson([
    B("Here is our equation. One third, plus one half, plus 1 over x, equals 4. We need to find x.",
      given("l1", "1/3 + 1/2 + 1/x = 4")),
    B("Let's first add the two fractions we know. Thirds and halves are different sizes, "
      "so we change both into sixths.", W("l2", "1/3 = 2/6"), W("l3", "1/2 = 3/6")),
    B("2 sixths plus 3 sixths is 5 sixths.", group("l1", ["1/3", "1/2"], "5/6"), W("l4", "1/3 + 1/2 = 5/6")),
    B("So 5 sixths, plus 1 over x, equals 4.", W("l5", "5/6 + 1/x = 4")),
    B("How do we find 1 over x?",
      ask=choose(["take 5/6 away from 4", "add 5/6 to 4", "turn 5/6 upside down"], 0,
                 "5 sixths and 1 over x together make 4. "
                 "So 1 over x is what is left when we take 5 sixths away from 4.")),
    B("To subtract, we write 4 in sixths. One whole is 6 sixths, so 4 wholes are 24 sixths.", W("l6", "4 = 24/6")),
    B("24 sixths minus 5 sixths is 19 sixths. So 1 over x equals 19 over 6.",
      W("l7", "24/6 − 5/6 = 19/6"), W("l8", "1/x = 19/6")),
    B("Careful, here is the trap. 19 over 6 is 1 over x. It is not x. How do we get x?",
      ask=choose(["turn it upside down: 6/19", "keep it as 19/6", "take it away from 1"], 0,
                 "If 1 over x is 19 over 6, then x is the same fraction flipped over. So x is 6 over 19.")),
    B("We flip the fraction. So x equals 6 over 19.", answer("l9", "x = 6/19"), mark("l9", "6/19", "circle")),
    B("Let's check. 1 over x is 19 sixths. And 5 sixths plus 19 sixths is 24 sixths, which is 4. It works!",
      W("l10", "5/6 + 19/6 = 24/6")),
    B("So add the fractions you know, take them from the total, and then flip to find x."),
], "x", "6/19")

# 6a + 8 = 4a + 18 (the value, 5, is not listed)
LESSONS["EXT_G4_FP_2022_002"] = lesson([
    B("Here is our equation. 6 a, plus 8, equals 4 a, plus 18. The letter a is on both sides.",
      given("l1", "6a + 8 = 4a + 18")),
    B("Think of a balance, with bags called a. Let's gather the bags on the left. The right side has 4 a.",
      balance("f1", "6a + 8", "4a + 18")),
    B("If we take 4 a from both sides, what is left on the left?",
      ask=choose(["2a + 8", "10a + 8", "2a"], 0,
                 "6 a take away 4 a leaves 2 a. The plus 8 has not been touched, so it stays. "
                 "That gives 2 a, plus 8.")),
    B("We take 4 a from both sides. Now 2 a, plus 8, equals 18.",
      strike("l1", "4a", "− 4a"), both("l1", "− 4a"), W("l2", "2a + 8 = 18")),
    B("Next, take 8 from both sides. 18 minus 8 is 10. So 2 a equals 10.",
      strike("l2", "+ 8", "− 8"), both("l2", "− 8"), W("l3", "2a = 10")),
    B("10 is one of the choices. Is 10 our answer?",
      ask=choose(["No. 10 is 2a, so halve it.", "Yes, a is 10."], 0,
                 "10 is what 2 a is worth. We want just one a, so we still have to divide by 2.")),
    B("We divide both sides by 2. 10 divided by 2 is 5. So a equals 5.", divide("l3", 2), W("l4", "a = 5")),
    B("Let's check. Left: 6 times 5, plus 8, makes 38. Right: 4 times 5, plus 18, also makes 38. "
      "So a really is 5.", W("l5", "6 × 5 + 8 = 38"), W("l6", "4 × 5 + 18 = 38")),
    B("Now look at the choices. Our 5 is not among them! When that happens, trust your checked working."),
    B("So the answer is: none of these.",
      answer("l7", "a = 5, so: None of these", label=True), mark("l7", "None of these", "circle")),
    B("Solve it fully, check it, and only then look at the choices. Sometimes the right number is not listed."),
], "a", 5)

# 8P + 7 = 39, Q = P + 3. Find 2P + 3Q.
_PQ = {"P": 4, "Q": 7}
LESSONS["EXT_G4_FP_2022_023"] = lesson([
    B("We have two facts. 8 P, plus 7, equals 39. And Q equals P plus 3. We must find 2 P, plus 3 Q.",
      E("g1", "8P + 7 = 39", _PQ, "given"), E("g2", "Q = P + 3", _PQ, "given"), W("g3", "2P + 3Q = ?")),
    B("That is three small jobs. Find P. Then find Q. Then work out the last sum. "
      "Which fact lets us find P straight away?",
      ask=choose(["8P + 7 = 39", "Q = P + 3"], 0,
                 "Q equals P plus 3 has two letters we do not know yet. "
                 "But the other fact has only P in it, so we start there.")),
    B("Take 7 from both sides. 39 minus 7 is 32. So 8 P equals 32.",
      strike("g1", "+ 7", "− 7"), both("g1", "− 7"), E("l1", "8P = 32", _PQ)),
    B("Divide both sides by 8. 8 times 4 is 32, so P equals 4.", divide("l1", 8), E("l2", "P = 4", _PQ)),
    B("Now Q. Q is 3 more than P, so Q is 4 plus 3, which is 7.", E("l3", "Q = 4 + 3 = 7", _PQ)),
    B("Now the last job: 2 P, plus 3 Q. Which sum is that?",
      ask=choose(["2 × 4 + 3 × 7", "3 × 4 + 2 × 7", "2 + 4 + 3 + 7"], 0,
                 "The 2 goes with P, and P is 4. The 3 goes with Q, and Q is 7. "
                 "So it is 2 times 4, plus 3 times 7.")),
    B("2 times 4 is 8. And 3 times 7 is 21.", W("l4", "2 × 4 = 8"), W("l5", "3 × 7 = 21")),
    B("8 plus 21 is 29. So 2 P, plus 3 Q, equals 29.",
      E("l6", "2P + 3Q = 8 + 21 = 29", _PQ, "answer"), mark("l6", "29", "circle")),
    B("Careful not to swap the 2 and the 3, and not to stop at 21. Do each job in order, and the last sum is easy."),
])

# Mishti 97 pens, Manav 11. She gives some so that she has twice his.
LESSONS["EXT_G4_FP_2023_006"] = lesson([
    B("Mishti has 97 pens and Manav has 11. Mishti gives some pens to Manav. "
      "After that, she has twice as many as he has.", given("g1", "Mishti 97 pens, Manav 11 pens", label=True)),
    B("When Mishti gives pens to Manav, what happens to the total number of pens?",
      ask=choose(["it stays the same", "it gets smaller", "it gets bigger"], 0,
                 "No pens are lost, and no new pens appear. They only move from one child to the other. "
                 "So the total stays the same.")),
    B("So let's find the total. 97 plus 11 is 108.", W("l1", "97 + 11 = 108")),
    B("At the end Mishti has twice as many as Manav. So Manav has 1 share and Mishti has 2 shares. "
      "That is 3 equal shares.",
      bars("f1", ("Mishti", [(3, "1 share", "a"), (3, "1 share", "a")]), ("Manav", [(3, "1 share", "b")]))),
    B("3 equal shares make 108 pens. How do we find one share?",
      ask=choose(["108 ÷ 3", "108 ÷ 2", "108 − 3"], 0,
                 "Mishti's 2 shares and Manav's 1 share make 3 shares in all. So we divide 108 by 3, not by 2.")),
    B("108 divided by 3. 3 times 30 is 90, and 3 times 6 is 18. So one share is 36.",
      W("l2", "3 × 30 = 90"), W("l3", "3 × 6 = 18"), W("l4", "108 ÷ 3 = 36")),
    B("So Manav ends with 36 pens. He started with 11. The pens he gained are the pens Mishti gave.",
      L("l5", "Manav: 11 → 36")),
    B("36 minus 11 is 25. So Mishti gave 25 pens.", answer("l6", "36 − 11 = 25"), mark("l6", "25", "circle")),
    B("Let's check. Mishti is left with 97 minus 25, which is 72. And 72 is twice 36. It works!",
      W("l7", "97 − 25 = 72"), W("l8", "2 × 36 = 72")),
    B("So when things only move from one person to another, the total stays the same. "
      "Use the total to find the shares."),
])

# If 3x + 7 = 38, then 6x + 7 = ?  (69, which is not listed)
LESSONS["EXT_G4_FP_2023_011"] = lesson([
    B("We know that 3 x, plus 7, equals 38. We must find 6 x, plus 7.",
      given("l1", "3x + 7 = 38"), W("l2", "6x + 7 = ?")),
    B("Here is a secret: we do not need x itself. Look at 6 x and 3 x. How are they related?",
      ask=choose(["6x is double 3x", "6x is 3 more than 3x", "they are the same"], 0,
                 "6 is 2 times 3. So 6 x is 2 lots of 3 x. It is double.")),
    B("So first let's find 3 x. Take 7 from both sides. 38 minus 7 is 31. So 3 x equals 31.",
      strike("l1", "+ 7", "− 7"), both("l1", "− 7"), W("l3", "3x = 31")),
    B("Now double it. 6 x is 2 times 31, which is 62.", W("l4", "6x = 2 × 31"), W("l5", "6x = 62")),
    B("We want 6 x, plus 7. What do we add to 62?",
      ask=choose(["7, just once", "14, because we doubled", "nothing"], 0,
                 "Only the 3 x part was doubled. The plus 7 in 6 x plus 7 is a plain 7, so we add 7 just once.")),
    B("62 plus 7 is 69. So 6 x, plus 7, equals 69.", W("l6", "6x + 7 = 62 + 7"), W("l7", "6x + 7 = 69")),
    B("Here is the trap. Doubling the whole of 38 gives 76. But that doubles the 7 as well, "
      "and we only want one 7.", W("l8", "2 × 38 = 76"), note("l8", "76", "7 doubled too")),
    B("Now look at the choices. 69 is not there! So the answer is: none of these.",
      answer("l9", "69 is not listed: none of these", label=True), mark("l9", "none of these", "circle")),
    B("So look for a shortcut before solving. And if your checked answer is not listed, choose none of these."),
], "x", "31/3")

# For N = 8, which equation is true?
_N = {"N": 8}
LESSONS["EXT_G4_FP_2023_020"] = lesson([
    B("We are told that N is 8. We must find which equation is true. So we test each one, "
      "by putting 8 in place of N.", given("g1", "N = 8", label=True)),
    B("An equation is true when the left side and the right side come to the same number."),
    B("First: 3 N minus 14, and N plus 3. Left: 3 times 8 is 24, and 24 minus 14 is 10. Right: 8 plus 3 is 11.",
      W("a1", "3N − 14 = N + 3 ?"), W("a2", "3 × 8 = 24"), W("a3", "24 − 14 = 10"), W("a4", "8 + 3 = 11")),
    B("10 and 11 are close, but they are not equal. So the first equation is not true.",
      note("a3", "10", "left"), note("a4", "11", "right")),
    B("Second: 44 minus 4 N, and 3 N minus 12. Start with the left side. What is 44, minus 4 times 8?",
      W("b1", "44 − 4N = 3N − 12 ?"),
      ask=choose(["12", "320", "32"], 0,
                 "Multiply first: 4 times 8 is 32. Then take 32 away from 44. That leaves 12.")),
    B("So the left side is 12. Now the right: 3 times 8 is 24, and 24 minus 12 is 12. Both sides are 12!",
      W("b2", "4 × 8 = 32"), W("b3", "44 − 32 = 12"), W("b4", "24 − 12 = 12")),
    B("This one is true. But a careful mathematician tests the third one too: 62 plus 3 N, and 11 N plus 2.",
      W("c1", "62 + 3N = 11N + 2 ?")),
    B("Left: 62 plus 24 is 86. Right: 11 times 8 is 88, and 2 more is 90. Not equal.",
      W("c2", "62 + 24 = 86"), W("c3", "11 × 8 = 88"), W("c4", "88 + 2 = 90")),
    B("So the true equation is 44 minus 4 N, equals 3 N minus 12.",
      E("ans", "44 − 4N = 3N − 12", _N, "answer"), mark("ans", "44 − 4N = 3N − 12", "circle")),
    B("To test an equation, put the number in for the letter. Do the times first, then the adding or taking away."),
])

# 7(3P − 4) = 4(5 + 3P) + 6
_P = {"P": 6}
LESSONS["EXT_G4_FP_2023_021"] = lesson([
    B("Here is our equation. 7 times a bracket, equals 4 times a bracket, plus 6. "
      "It looks big, so we take it one step at a time.", E("g1", "7(3P − 4) = 4(5 + 3P) + 6", _P, "given")),
    B("First we open the brackets. The 7 multiplies everything inside its bracket: the 3 P, and the 4 as well.",
      arc("g1", "7", "3P", "4")),
    B("7 times 3 P is 21 P. And what is 7 times the minus 4?",
      E("l1", "7 × 3P = 21P", _P),
      ask=choose(["− 28", "− 4", "− 11"], 0,
                 "The 7 multiplies the 4 as well, not only the 3 P. 7 times 4 is 28, so we get minus 28.")),
    B("So the left side becomes 21 P, minus 28.", E("l2", "7(3P − 4) = 21P − 28", _P)),
    B("Now the right side. The 4 multiplies the 5 and the 3 P. 4 times 5 is 20, and 4 times 3 P is 12 P. "
      "The plus 6 just waits.",
      arc("g1", T("4", 2), "5", T("3P", 2)), E("l3", "4(5 + 3P) + 6 = 20 + 12P + 6", _P)),
    B("20 and 6 make 26. So our equation is now 21 P minus 28, equals 12 P plus 26. No more brackets!",
      E("l4", "21P − 28 = 12P + 26", _P)),
    B("The letter P is on both sides. What shall we take from both sides?",
      ask=choose(["12P", "21P", "26"], 0,
                 "We take away the smaller lot of P, which is 12 P. Then the right side has no P left.")),
    B("21 P take away 12 P is 9 P. So 9 P, minus 28, equals 26.",
      strike("l4", "12P", "− 12P"), both("l4", "− 12P"), E("l5", "9P − 28 = 26", _P)),
    B("Add 28 to both sides. 26 plus 28 is 54. So 9 P equals 54.",
      strike("l5", "− 28", "+ 28"), both("l5", "+ 28"), E("l6", "9P = 54", _P)),
    B("Divide both sides by 9. 9 times 6 is 54. So P equals 6.",
      divide("l6", 9), E("l7", "P = 6", _P, "answer"), mark("l7", "P = 6", "circle")),
    B("Let's check. Left: the bracket is 14, and 7 times 14 is 98. Right: the bracket is 23, "
      "and 4 times 23, plus 6, is also 98.", W("l8", "7 × 14 = 98"), W("l9", "4 × 23 + 6 = 98")),
    B("So open the brackets first, multiplying everything inside. Then gather the letters, and solve."),
])

# m + n = 18, n + p = 24, m + p = 36. Find p.  (21, which is not listed)
_MNP = {"m": 15, "n": 3, "p": 21}
LESSONS["EXT_G4_FP_2023_028"] = lesson([
    B("Three sums, and three hidden numbers: m, n and p. Each sum uses two of the letters. We must find p.",
      E("g1", "m + n = 18", _MNP, "given"), E("g2", "n + p = 24", _MNP, "given"),
      E("g3", "m + p = 36", _MNP, "given")),
    B("Here is a clever trick. We add all three sums together. 18 plus 24 is 42, and 42 plus 36 is 78.",
      W("l1", "18 + 24 = 42"), W("l2", "42 + 36 = 78")),
    B("In those three sums, how many times does each letter appear?",
      ask=choose(["twice", "once", "three times"], 0,
                 "Look at m. It is in the first sum and in the third sum. That is twice. "
                 "It is the same for n and for p.")),
    B("So 78 is two lots of m plus n plus p.", E("l3", "2 × (m + n + p) = 78", _MNP)),
    B("Half of 78 is 39. So m plus n plus p equals 39.", E("l4", "m + n + p = 39", _MNP)),
    B("All three together make 39. And the first sum says m plus n is 18. So how do we find p?",
      ask=choose(["39 − 18", "39 + 18", "39 − 24"], 0,
                 "Take away the m and the n together, and only p is left. "
                 "m plus n is 18, so p is 39 minus 18.")),
    B("39 minus 18 is 21. So p equals 21.", E("l5", "p = 39 − 18", _MNP), E("l6", "p = 21", _MNP)),
    B("Let's check. n is 24 minus 21, which is 3. m is 36 minus 21, which is 15. And 15 plus 3 is 18. "
      "All three sums work!", W("l7", "24 − 21 = 3"), W("l8", "36 − 21 = 15"), W("l9", "15 + 3 = 18")),
    B("Now look at the choices. 21 is not there. 18 is only m plus n, and 15 is m. "
      "So the answer is: none of these.",
      answer("l10", "p = 21: none of these", label=True), mark("l10", "none of these", "circle")),
    B("So when each letter appears twice, add all the sums and halve. Then take away the pair you do not want."),
])

# 16y − 36 = 4y + (8 × 9)
LESSONS["EXT_G4_FP_2024_012"] = lesson([
    B("Here is our equation. 16 y, minus 36, equals 4 y, plus a bracket.",
      given("l1", "16y − 36 = 4y + (8 × 9)")),
    B("Start with the bracket. It has only plain numbers in it. 8 times 9 is 72.",
      mark("l1", "(8 × 9)", "box"), note("l1", "(8 × 9)", "72"), W("l2", "16y − 36 = 4y + 72")),
    B("Now y is on both sides. What do we take from both sides?",
      ask=choose(["4y", "16y", "36"], 0,
                 "We take away the smaller lot of y, which is 4 y. Then the right side has no y left.")),
    B("16 y take away 4 y is 12 y. So 12 y, minus 36, equals 72.",
      strike("l2", "4y", "− 4y"), both("l2", "− 4y"), W("l3", "12y − 36 = 72")),
    B("What next?",
      ask=choose(["add 36 to both sides", "take 36 from both sides", "divide by 12 first"], 0,
                 "The 36 is being taken away on the left. To undo that, we add 36 to both sides.")),
    B("72 plus 36 is 108. So 12 y equals 108.",
      strike("l3", "− 36", "+ 36"), both("l3", "+ 36"), W("l4", "12y = 108")),
    B("Now divide both sides by 12. Try 9: 10 times 9 is 90, and 2 times 9 is 18. Together that is 108.",
      divide("l4", 12), W("l5", "12 × 9 = 90 + 18")),
    B("So 12 times 9 is 108, and y equals 9.", answer("l6", "y = 9"), mark("l6", "y = 9", "circle")),
    B("Let's check. Left: 16 times 9, minus 36, is 108. Right: 4 times 9, plus 72, is also 108. Both sides match.",
      W("l7", "16 × 9 − 36 = 108"), W("l8", "4 × 9 + 72 = 108")),
    B("So work out any plain bracket first. Then gather the letters, undo the taking away, and divide."),
], "y", 9)

# Two consecutive odd numbers add up to 16. Sum of their squares?
LESSONS["EXT_G4_FP_2024_028"] = lesson([
    B("Two consecutive odd numbers add up to 16. We must find the sum of their squares. "
      "First, let's find the two numbers.", given("g1", "Two consecutive odd numbers add up to 16", label=True)),
    B("Consecutive odd numbers are odd numbers next to each other, like 3 and 5. They are always 2 apart."),
    B("Half of 16 is 8. So the two numbers sit on either side of 8: one just below, and one just above.",
      W("l1", "16 ÷ 2 = 8"),
      fig("f1", {"kind": "numberLine", "min": 5, "max": 11, "step": 1, "points": [{"at": 8, "label": "middle"}]})),
    B("Which two odd numbers sit on either side of 8?",
      ask=choose(["7 and 9", "8 and 8", "6 and 10"], 0,
                 "8 is even, so it cannot be one of them. The odd numbers next to 8 are 7 and 9. "
                 "And 7 plus 9 is 16.")),
    B("The numbers are 7 and 9. Now we square each one. To square a number, we multiply it by itself.",
      W("l2", "7 + 9 = 16")),
    B("7 times 7 is 49. And 9 times 9 is 81.", W("l3", "7 × 7 = 49"), W("l4", "9 × 9 = 81")),
    B("What do we do with 49 and 81?",
      ask=choose(["add them", "multiply them", "subtract them"], 0,
                 "The question asks for the sum of the squares. Sum means add.")),
    B("49 plus 81. Take 1 from the 81 and give it to the 49. That makes 50 plus 80, which is 130.",
      W("l5", "50 + 80 = 130"), answer("l6", "49 + 81 = 130"), mark("l6", "130", "circle")),
    B("So find the two numbers first, square each one, then add. Three small steps."),
])

# 12x − 19 = 53. Find 5x + 29.
_X6 = {"x": 6}
LESSONS["EXT_G4_FP_2024_037"] = lesson([
    B("We know that 12 x, minus 19, equals 53. We must find the value of 5 x, plus 29. So there are two jobs.",
      E("g1", "12x − 19 = 53", _X6, "given"), W("g2", "5x + 29 = ?")),
    B("Which job comes first?",
      ask=choose(["find x from the equation", "work out 5x + 29 straight away", "add 53 and 29"], 0,
                 "We cannot work out 5 x plus 29 until we know x. So first we solve the equation to find x.")),
    B("To undo minus 19, we add 19 to both sides. 53 plus 19 is 72. So 12 x equals 72.",
      strike("g1", "− 19", "+ 19"), both("g1", "+ 19"), E("l1", "12x = 72", _X6)),
    B("Divide both sides by 12. 12 times 6 is 72, so x equals 6.", divide("l1", 12), E("l2", "x = 6", _X6)),
    B("That is job one done. But careful: 6 is not the answer. The question asks for 5 x, plus 29.",
      mark("g2", "5x + 29", "underline")),
    B("x is 6. So what is 5 x?",
      ask=choose(["30", "56", "11"], 0, "5 x means 5 times x. And 5 times 6 is 30.")),
    B("5 times 6 is 30. Then 30 plus 29 is 59. So 5 x, plus 29, equals 59.",
      W("l3", "5 × 6 = 30"), answer("l4", "30 + 29 = 59"), mark("l4", "59", "circle")),
    B("Let's check our x. 12 times 6 is 72, and 72 minus 19 is 53. Yes, x is right.",
      W("l5", "12 × 6 − 19 = 53")),
    B("Two jobs: solve for the letter, then put it into the second expression. "
      "Always read what the question really asks."),
])

# 4m/3 + 17 = 2m + 3
LESSONS["EXT_G4_FP_2025_020"] = lesson([
    B("Here is our equation. 4 m over 3, plus 17, equals 2 m, plus 3. There is a fraction in it.",
      given("l1", "4m/3 + 17 = 2m + 3")),
    B("Fractions make equations awkward, so we clear it away. The bottom number is 3, "
      "so we multiply by 3.", mark("l1", "4m/3", "box")),
    B("When we multiply by 3, which parts must be multiplied?",
      ask=choose(["every part on both sides", "only the fraction", "only the left side"], 0,
                 "The two sides must stay equal. So every single part gets multiplied by 3: "
                 "the fraction, the 17, the 2 m and the 3.")),
    B("4 m over 3, times 3, is just 4 m. And 17 times 3 is 51.", both("l1", "× 3"), W("l2", "17 × 3 = 51")),
    B("On the right, 2 m times 3 is 6 m, and 3 times 3 is 9. So now 4 m, plus 51, equals 6 m, plus 9.",
      W("l3", "4m + 51 = 6m + 9")),
    B("The letter m is on both sides. Which shall we take from both sides?",
      ask=choose(["4m", "6m", "51"], 0,
                 "Take away the smaller lot, 4 m. Then the left side has no m, and the right side has 2 m.")),
    B("6 m take away 4 m is 2 m. So 51 equals 2 m, plus 9.",
      strike("l3", "4m", "− 4m"), both("l3", "− 4m"), W("l4", "51 = 2m + 9")),
    B("Take 9 from both sides. 51 minus 9 is 42. So 2 m equals 42.",
      strike("l4", "+ 9", "− 9"), both("l4", "− 9"), W("l5", "2m = 42")),
    B("Half of 42 is 21. So m equals 21.", divide("l5", 2), answer("l6", "m = 21"), mark("l6", "m = 21", "circle")),
    B("Let's check. Left: 4 times 21 is 84, and 84 divided by 3 is 28. Then 28 plus 17 is 45. "
      "Right: 42 plus 3 is 45. Both sides match.",
      W("l7", "4 × 21 = 84"), W("l8", "84 ÷ 3 = 28"), W("l9", "28 + 17 = 45"), W("l10", "42 + 3 = 45")),
    B("So when there is a fraction, multiply every part by the bottom number first. Then solve as usual."),
], "m", 21)

# If 3m + 7 = 28, find 2m + 25.
_M7 = {"m": 7}
LESSONS["EXT_G4_FP_2025_035"] = lesson([
    B("We know that 3 m, plus 7, equals 28. We must find 2 m, plus 25.",
      E("g1", "3m + 7 = 28", _M7, "given"), W("g2", "2m + 25 = ?")),
    B("First we need m. Take 7 from both sides. 28 minus 7 is 21. So 3 m equals 21.",
      strike("g1", "+ 7", "− 7"), both("g1", "− 7"), E("l1", "3m = 21", _M7)),
    B("3 times m is 21. So what is m?",
      ask=choose(["7", "18", "63"], 0, "To undo times 3, we divide by 3. And 21 divided by 3 is 7.")),
    B("21 divided by 3 is 7. So m equals 7.", divide("l1", 3), E("l2", "m = 7", _M7)),
    B("Careful: we are not finished. The question asks for 2 m, plus 25.", mark("g2", "2m + 25", "underline")),
    B("m is 7. So which sum gives 2 m, plus 25?",
      ask=choose(["2 × 7 + 25", "27 + 25", "2 + 7 + 25"], 0,
                 "2 m means 2 times m. So it is 2 times 7, and then 25 more.")),
    B("2 times 7 is 14. And 14 plus 25 is 39.",
      W("l3", "2 × 7 = 14"), answer("l4", "14 + 25 = 39"), mark("l4", "39", "circle")),
    B("Let's check our m. 3 times 7 is 21, and 21 plus 7 is 28. Yes, m is right.", W("l5", "3 × 7 + 7 = 28")),
    B("Find the letter first. Then use it in the second expression. Two jobs, in order."),
])
