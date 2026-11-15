"""Lessons written by hand: longer equations, and an age problem turned into an equation."""
from algebra_lib import B, W, answer, arc, both, choose, divide, given, group, lesson, mark, note, strike

LESSONS = {}

# 4(2x − 1) = 5(x + 2) + 4
LESSONS["EXT_G5_FP_2022_006"] = lesson([
    B("This equation has a bracket on each side. We open the brackets first, and then we solve.",
      given("l1", "4(2x − 1) = 5(x + 2) + 4")),
    B("Left side first. The 4 multiplies both things inside. 4 times 2 x is 8 x. "
      "And careful: 4 times minus 1 is minus 4.",
      arc("l1", "4", "2x", "1"), W("l2", "8x − 4 = 5(x + 2) + 4")),
    B("Now the right side. What does 5 times the bracket, x plus 2, open into?",
      ask=choose(["5x + 2", "5x + 10", "x + 10"], 1,
                 "The 5 multiplies the x and the 2. 5 times x is 5 x, and 5 times 2 is 10. So we get 5 x plus 10.")),
    B("So the bracket becomes 5 x plus 10, and the plus 4 is still waiting at the end.",
      arc("l2", "5", ("x", 2), "2"), W("l3", "8x − 4 = 5x + 10 + 4")),
    B("10 and 4 are both plain numbers. Together they make 14.",
      group("l3", ["+ 10", "+ 4"], "14"), W("l4", "8x − 4 = 5x + 14")),
    B("x is on both sides now. What is a good next move?",
      ask=choose(["divide both sides by 8", "take 5x from both sides", "add 5x to both sides"], 1,
                 "We want the x terms together. The 5 x on the right is a plus 5 x, "
                 "so we take 5 x away, from both sides.")),
    B("Take 5 x from both sides. On the right it is gone. On the left, 8 x take away 5 x leaves 3 x.",
      strike("l4", "5x", "− 5x"), both("l4", "− 5x"), W("l5", "3x − 4 = 14")),
    B("Undo the minus 4 by adding 4 to both sides. 14 plus 4 is 18, so 3 x equals 18.",
      strike("l5", "− 4", "+ 4"), both("l5", "+ 4"), W("l6", "3x = 18")),
    B("Divide both sides by 3. 18 divided by 3 is 6. So x equals 6.",
      divide("l6", "3"), answer("l7", "x = 6"), mark("l7", "x = 6")),
    B("Check. Left: the bracket is 2 times 6, minus 1, which is 11. And 4 times 11 is 44. "
      "Right: the bracket is 8, and 5 times 8, plus 4, is also 44.",
      W("l8", "2 × 6 − 1 = 11"), W("l9", "4 × 11 = 44"), W("l10", "5 × 8 + 4 = 44")),
    B("The plan: open every bracket, tidy each side, bring the letters together, "
      "clear the plain number, and divide last."),
], "x", 6)

# (p + 3) × (p + 2) if 2p + 5 = 9p − 30
LESSONS["EXT_G5_FP_2023_013"] = lesson([
    B("Two jobs in this one. First we solve the equation to find p. "
      "Then we use p to work out p plus 3, times p plus 2.",
      given("l1", "2p + 5 = 9p − 30"), given("l0", "(p + 3) × (p + 2) = ?")),
    B("p is on both sides. Which lot of p shall we take away from both sides?",
      ask=choose(["the 9p, the bigger lot", "the 2p, the smaller lot", "neither: divide by 2 first"], 1,
                 "Taking away the smaller lot, 2 p, keeps everything positive, and that is much easier to work with.")),
    B("Take 2 p from both sides. On the left only 5 is left. On the right, 9 p take away 2 p is 7 p.",
      strike("l1", "2p", "− 2p"), both("l1", "− 2p"), W("l2", "5 = 7p − 30")),
    B("Now undo the minus 30, by adding 30 to both sides. 5 plus 30 is 35.",
      strike("l2", "− 30", "+ 30"), both("l2", "+ 30"), W("l3", "35 = 7p")),
    B("7 p means 7 times p. Divide both sides by 7, and 35 divided by 7 is 5. So p equals 5.",
      divide("l3", "7"), W("l4", "p = 5"), mark("l4", "p = 5", "underline")),
    B("Are we finished?",
      ask=choose(["Yes, p = 5 is the answer", "No, we still need (p + 3) × (p + 2)"], 1,
                 "Look back at the question. It does not ask for p. "
                 "It asks for the value of p plus 3, times p plus 2.")),
    B("Put 5 in for p. 5 plus 3 is 8, and 5 plus 2 is 7. 8 times 7 is 56.",
      W("l5", "(5 + 3) × (5 + 2) = 8 × 7"), answer("l6", "(p + 3) × (p + 2) = 56"), mark("l6", "56")),
    B("Now look at the choices: 84, 14 and 36. Our 56 is not there. So the answer is none of these.",
      W("l7", "choices: 84, 14, 36, none of these", label=True), mark("l7", "none of these")),
    B("When your answer is not listed, check before you trust it. With p as 5, the left side is 2 times 5, plus 5, "
      "which is 15. The right is 9 times 5, minus 30, also 15.",
      W("l8", "2 × 5 + 5 = 15"), W("l9", "9 × 5 − 30 = 15")),
    B("So: solve for the letter, then answer what was really asked. "
      "And if your checked answer is not among the choices, none of these is the one to pick."),
], "p", 5)

# 6x − 9 = (4x + 30)/2
LESSONS["EXT_G5_FP_2024_014"] = lesson([
    B("Here is our equation. 6 x minus 9, equals 4 x plus 30, all over 2. Let's tidy the right side first.",
      given("l1", "6x − 9 = (4x + 30)/2")),
    B("All over 2 means the whole bracket is halved. What is half of 4 x plus 30?",
      ask=choose(["2x + 30", "2x + 15", "4x + 15"], 1,
                 "The 2 divides both parts. Half of 4 x is 2 x, and half of 30 is 15. "
                 "Halving only one of them is the slip to avoid.")),
    B("So half of 4 x is 2 x, and half of 30 is 15.",
      arc("l1", "2", "4x", "30"), W("l2", "6x − 9 = 2x + 15")),
    B("x is on both sides. Take the smaller lot, 2 x, from both sides. 6 x take away 2 x leaves 4 x.",
      strike("l2", "2x", "− 2x"), both("l2", "− 2x"), W("l3", "4x − 9 = 15")),
    B("What is in the way of the 4 x now?",
      ask=choose(["the 15", "the 4", "the − 9"], 2,
                 "Look at the left side. The 4 x has a minus 9 hanging on to it. That is what we clear next.")),
    B("To undo minus 9 we add 9 to both sides. 15 plus 9 is 24. So 4 x equals 24.",
      strike("l3", "− 9", "+ 9"), both("l3", "+ 9"), W("l4", "4x = 24")),
    B("Divide both sides by 4. 24 divided by 4 is 6. So x equals 6.",
      divide("l4", "4"), answer("l5", "x = 6"), mark("l5", "x = 6")),
    B("Check. Left: 6 times 6 is 36, and 36 minus 9 is 27. Right: 4 times 6, plus 30, is 54, "
      "and half of 54 is 27. Both sides are 27.",
      W("l6", "6 × 6 = 36"), W("l7", "36 − 9 = 27"), W("l8", "4 × 6 + 30 = 54"), W("l9", "54 ÷ 2 = 27")),
    B("So: tidy any fraction first, bring the x terms together, clear the plain number, then divide."),
], "x", 6)

# (4x − 5)/5 = (2x + 3)/3
LESSONS["EXT_G5_FP_2024_035"] = lesson([
    B("A fraction on each side this time. 4 x minus 5, over 5, equals 2 x plus 3, over 3. "
      "First we clear the bottoms.",
      given("l1", "(4x − 5)/5 = (2x + 3)/3")),
    B("Multiply both sides by 5 and by 3. On the left the 5 cancels and the 3 stays. "
      "On the right the 3 cancels and the 5 stays. That is cross multiplying.",
      arc("l1", ("3", 2), "(4x − 5)"), arc("l1", ("5", 2), "(2x + 3)"), W("l2", "3(4x − 5) = 5(2x + 3)")),
    B("Open the left bracket. The 3 multiplies the 4 x, and it multiplies the minus 5. What is 3 times minus 5?",
      ask=choose(["+ 15", "− 15", "− 5"], 1,
                 "3 times 5 is 15, and the minus sign stays with it. So we get minus 15.")),
    B("So the left side is 12 x minus 15. On the right, 5 times 2 x is 10 x, and 5 times 3 is 15.",
      arc("l2", "3", "4x", "5"), arc("l2", ("5", 2), "2x", ("3", 2)), W("l3", "12x − 15 = 10x + 15")),
    B("Take the smaller lot of x, 10 x, from both sides. 12 x take away 10 x leaves 2 x.",
      strike("l3", "10x", "− 10x"), both("l3", "− 10x"), W("l4", "2x − 15 = 15")),
    B("What clears the minus 15?",
      ask=choose(["take 15 from both sides", "add 15 to both sides", "divide both sides by 15"], 1,
                 "Adding undoes taking away. So we add 15, and we add it to both sides.")),
    B("Add 15 to both sides. 15 plus 15 is 30, so 2 x equals 30.",
      strike("l4", "− 15", "+ 15"), both("l4", "+ 15"), W("l5", "2x = 30")),
    B("Divide both sides by 2. Half of 30 is 15. So x equals 15.",
      divide("l5", "2"), answer("l6", "x = 15"), mark("l6", "x = 15")),
    B("Check with 15. Left: 4 times 15, minus 5, is 55, and 55 over 5 is 11. "
      "Right: 2 times 15, plus 3, is 33, and 33 over 3 is 11. Both sides are 11.",
      W("l7", "4 × 15 − 5 = 55"), W("l8", "55/5 = 11"), W("l9", "2 × 15 + 3 = 33"), W("l10", "33/3 = 11")),
    B("With a fraction on each side: cross multiply, open the brackets, then solve it like any other equation."),
], "x", 15)

# Four children, ages add to 20. Find Anil.
LESSONS["EXT_G5_FP_2017_006"] = lesson([
    B("Four children, and their ages add up to 20. We want Anil's age, so let's call Anil's age a.",
      given("l1", "Anil + Bunty + Chetan + David = 20", label=True), W("l2", "Anil = a", label=True)),
    B("Anil is 3 years younger than Chetan. So how do we write Chetan's age?",
      ask=choose(["a − 3", "a + 3", "3a"], 1,
                 "If Anil is 3 years younger, then Chetan is 3 years older than Anil. Older means we add: a plus 3.")),
    B("So Chetan is a plus 3. David is 5 years older than Chetan, so David is a plus 3 plus 5, which is a plus 8.",
      W("l3", "Chetan = a + 3", label=True), W("l4", "David = a + 3 + 5 = a + 8", label=True)),
    B("David is 3 years older than Bunty, so Bunty is 3 years younger than David. "
      "That makes Bunty a plus 8 minus 3, which is a plus 5.",
      W("l5", "Bunty = a + 8 − 3 = a + 5", label=True)),
    B("Now add all four ages, and that must be 20.",
      W("l6", "a + (a + 5) + (a + 3) + (a + 8) = 20")),
    B("Gather the like terms. There are 4 lots of a. And the plain numbers, 5 and 3 and 8, make 16.",
      group("l6", [("a", 1), ("a", 2), ("a", 3), ("a", 4)], "4a"), group("l6", ["+ 5", "+ 3", "+ 8"], "16"),
      W("l7", "4a + 16 = 20")),
    B("Now it is an equation we know. What do we do first?",
      ask=choose(["divide both sides by 4", "take 16 from both sides", "add 16 to both sides"], 1,
                 "The 4 a has a plus 16 hanging on to it. We clear that first, by taking 16 from both sides.")),
    B("Take 16 from both sides. 20 minus 16 is 4, so 4 a equals 4.",
      strike("l7", "+ 16", "− 16"), both("l7", "− 16"), W("l8", "4a = 4")),
    B("Divide both sides by 4. 4 divided by 4 is 1. So Anil is just 1 year old.",
      divide("l8", "4"), answer("l9", "a = 1"), mark("l9", "a = 1")),
    B("Check the story. Anil is 1, so Chetan is 4, David is 9 and Bunty is 6. 1 plus 6 plus 4 plus 9 is 20. It fits.",
      W("l10", "1 + 6 + 4 + 9 = 20")),
    B("So in a word problem: give a letter to the thing you want, write everyone else using that letter, "
      "and build one equation."),
], "a", 1)

# A number increased by 17 equals 60 times its reciprocal.
LESSONS["EXT_G5_FP_2021_031"] = lesson([
    B("This question is a sentence we have to turn into maths. A number, increased by 17, "
      "equals 60 times the reciprocal of the number.",
      given("l1", "number + 17 = 60 × reciprocal", label=True)),
    B("First, that long word. What is the reciprocal of 5?",
      ask=choose(["−5", "1/5", "5/1"], 1,
                 "The reciprocal of a number is 1 divided by that number. It is the number turned upside down. "
                 "So the reciprocal of 5 is 1 over 5.")),
    B("So 60 times the reciprocal of a number is 60 times 1 over the number. That is just 60 divided by the number. "
      "If we call the number n, we get this.",
      W("l2", "n + 17 = 60/n")),
    B("We could solve it, but with four choices it is quicker to test them. Start with 5. "
      "5 plus 17 is 22. But 60 divided by 5 is 12. Not a match.",
      W("l3", "5 + 17 = 22"), W("l4", "60 ÷ 5 = 12"), W("l5", "22 ≠ 12")),
    B("Now try 3. 3 plus 17 is 20. What is 60 divided by 3?",
      W("l6", "3 + 17 = 20"),
      ask=choose(["18", "20", "30"], 1,
                 "6 divided by 3 is 2, so 60 divided by 3 is 20.")),
    B("60 divided by 3 is 20 as well. The two sides match!",
      W("l7", "60 ÷ 3 = 20"), answer("l8", "n = 3"), mark("l8", "n = 3")),
    B("And the bigger choices, 17 and 12? Adding 17 makes them bigger still, "
      "but 60 divided by a big number is small. So they cannot match.",
      W("l9", "12 + 17 = 29"), W("l10", "60 ÷ 12 = 5")),
    B("So the number is 3. When a question gives choices, testing each one in the sentence is a fine way to solve it."),
], "n", 3)
