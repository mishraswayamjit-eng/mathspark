"""Lessons written one by one: Q_CH14_017 to Q_CH14_025 and the worksheet questions EXT_G4_WS2_CH14_001 to 008.

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, E, L, W, answer, balance, bars, both, choose, divide, fig, given, lesson, mark,
                                  note, strike)

LESSONS = {}

# If x = 5, which equation is TRUE?
LESSONS["Q_CH14_017"] = lesson([
    B("We are told that x is 5. Four equations are given, and only one of them is true. Let's test each one.",
      given("g1", "x = 5", label=True)),
    B("An equation is true when both sides come to the same number. So we put 5 in place of x, "
      "and work out the left side."),
    B("Start with x, plus 10, equals 16. 5 plus 10 is 15. And 15 is not 16, so this one is not true.",
      W("a1", "x + 10 = 16 ?"), W("a2", "5 + 10 = 15"), note("a2", "15", "not 16")),
    B("Next: 3 x, plus 2, equals 18. Remember, 3 x means 3 times x. 3 times 5 is 15, and 15 plus 2 is 17. Not 18.",
      W("b1", "3x + 2 = 18 ?"), W("b2", "3 × 5 + 2 = 17"), note("b2", "17", "not 18")),
    B("Now 4 x, plus 1, equals 20. What is the left side when x is 5?",
      W("c1", "4x + 1 = 20 ?"),
      ask=choose(["21", "46", "10"], 0,
                 "4 x means 4 times x. It does not mean 4 and 5 written side by side. "
                 "4 times 5 is 20, and 1 more is 21.")),
    B("The left side is 21, but the right side says 20. So close, but not true.",
      W("c2", "4 × 5 + 1 = 21"), note("c2", "21", "not 20")),
    B("Last one: 2 x, minus 3, equals 7. 2 times 5 is 10, and 10 minus 3 is 7. Both sides are 7!",
      W("d1", "2x − 3 = 7 ?"), W("d2", "2 × 5 − 3 = 7")),
    B("So the true equation is 2 x, minus 3, equals 7.",
      E("ans", "2x − 3 = 7", {"x": 5}, "answer"), mark("ans", "2x − 3 = 7", "circle")),
    B("To test an equation, put the number in place of the letter, and see whether both sides match."),
])

# A number added to 8 gives 23.
LESSONS["Q_CH14_018"] = lesson([
    B("A number added to 8 gives 23. Let's write that as a sum, with a question mark for the mystery number.",
      given("l1", "8 + ? = 23")),
    B("Look at the bar. The whole bar is 23. One part is 8. The other part is our mystery number.",
      bars("f1", (None, [(8, "8", "a"), (15, "?", "unknown")], "23"))),
    B("How do we find the mystery part?",
      ask=choose(["23 take away 8", "23 plus 8", "23 times 8"], 0,
                 "The total is already 23. The mystery number is only one part of it, "
                 "so it must be smaller than 23. We take 8 away.")),
    B("23 minus 8. First take away 3 to reach 20. Then take away 5 more. That gives 15.",
      W("l2", "23 − 3 = 20"), W("l3", "20 − 5 = 15")),
    B("So the number is 15.", answer("l4", "The number is 15", label=True), mark("l4", "15", "circle")),
    B("Let's check. 8 plus 15 is 23. It works!", W("l5", "8 + 15 = 23")),
    B("So when we know a total and one part, we take the part away from the total to find the other part."),
])

# Seven times a number is 63.
LESSONS["Q_CH14_019"] = lesson([
    B("Seven times a number is 63. Let's write n for the number. So 7 times n equals 63.",
      given("l1", "7 × n = 63")),
    B("That means 7 equal lots of our number make 63.",
      bars("f1", (None, [(1, "n", "unknown")] * 7, "63"))),
    B("How do we find one lot?",
      ask=choose(["divide 63 by 7", "multiply 63 by 7", "take 7 from 63"], 0,
                 "Multiplying would give a number far bigger than 63. Our number is smaller: "
                 "it is one of 7 equal parts of 63. So we divide.")),
    B("So we divide both sides by 7.", divide("l1", 7)),
    B("Think of the 7 times table. 7 times 9 is 63. So 63 divided by 7 is 9.", W("l2", "63 ÷ 7 = 9")),
    B("So the number is 9.", answer("l3", "n = 9"), mark("l3", "n = 9", "circle")),
    B("Let's check. 7 times 9 is 63. It works!", W("l4", "7 × 9 = 63")),
    B("So when the words say times a number, write a times sum. Then undo it by dividing."),
], "n", 9)

# Three times a number decreased by 5 is 16.
LESSONS["Q_CH14_020"] = lesson([
    B("Three times a number, decreased by 5, is 16. Let's call the number n and write it down.",
      given("l1", "3 × n − 5 = 16")),
    B("Decreased by 5 means 5 was taken away. So the number was multiplied by 3, then 5 was taken away, "
      "and 16 was left.", mark("l1", "− 5", "underline")),
    B("We work backwards. What was there just before the 5 was taken away?",
      ask=choose(["16 plus 5", "16 minus 5", "16 divided by 3"], 0,
                 "The 5 was already taken away to leave 16. To go back, we put the 5 back. So it is 16 plus 5.")),
    B("16 plus 5 is 21. So three times the number is 21.",
      strike("l1", "− 5", "+ 5"), W("l2", "3 × n = 16 + 5"), W("l3", "3 × n = 21")),
    B("Careful: 21 is three times the number, not the number itself. What do we do with 21?",
      ask=choose(["divide it by 3", "multiply it by 3", "take 3 away"], 0,
                 "21 is 3 lots of the number. To find one lot, we share 21 into 3 equal parts.")),
    B("21 divided by 3 is 7, because 3 times 7 is 21. So the number is 7.",
      divide("l3", 3), answer("l4", "n = 7"), mark("l4", "n = 7", "circle")),
    B("Let's check. 3 times 7 is 21, and 21 minus 5 is 16. It works!", W("l5", "3 × 7 − 5 = 16")),
    B("So work backwards from the end. Undo the last step first, then the one before it."),
], "n", 7)

# Riya is 3 more than twice her brother's age; Riya is 17.
LESSONS["Q_CH14_021"] = lesson([
    B("Riya's age is 3 years more than twice her brother's age. And Riya is 17.",
      given("g1", "Riya = twice brother + 3", label=True), given("g2", "Riya = 17", label=True)),
    B("Look at the bar. Riya's 17 years are made of two lots of her brother's age, and 3 more.",
      bars("f1", ("Riya", [(3, "brother", "unknown"), (3, "brother", "unknown"), (1.5, "3", "c")], "17"))),
    B("We want the brother's age. Which piece do we deal with first?",
      ask=choose(["take away the 3", "halve 17 first", "add 3 to 17"], 0,
                 "The extra 3 is not part of the doubling. Take it off first. "
                 "What is left is exactly twice the brother's age.")),
    B("17 minus 3 is 14. So twice the brother's age is 14.", W("l1", "17 − 3 = 14")),
    B("Careful: 14 is twice his age, not his age. So how old is the brother?",
      ask=choose(["7", "14", "28"], 0,
                 "14 is two lots of his age. One lot is half of 14, and that is 7.")),
    B("Half of 14 is 7. So Riya's brother is 7 years old.",
      W("l2", "14 ÷ 2 = 7"), answer("l3", "Brother = 7 years", label=True), mark("l3", "7", "circle")),
    B("Let's check. Twice 7 is 14, and 3 more is 17. That is Riya's age. It works!", W("l4", "2 × 7 + 3 = 17")),
    B("So work backwards: take off the extra years first, then halve."),
])

# Aman spends ₹45 and is left with ₹78.
LESSONS["Q_CH14_023"] = lesson([
    B("Aman had some money. He spent 45 rupees, and 78 rupees are left. How much did he have at first?",
      given("l1", "? − 45 = 78")),
    B("His money at first was in two parts: the 45 rupees he spent, and the 78 rupees he still has.",
      bars("f1", ("At first", [(4.5, "spent 45", "a"), (7.8, "left 78", "b")], "?"))),
    B("Did Aman have more than 78 rupees at first, or less?",
      ask=choose(["more than 78", "less than 78"], 0,
                 "He spent some money and still has 78 rupees. So before spending, he must have had more than 78.")),
    B("So we put the two parts back together. We add 78 and 45.", W("l2", "78 + 45 = ?")),
    B("78 plus 40 is 118. Then 5 more makes 123.", W("l3", "78 + 40 = 118"), W("l4", "118 + 5 = 123")),
    B("So Aman had 123 rupees at first.", answer("l5", "₹123"), mark("l5", "₹123", "circle")),
    B("Let's check. 123 minus 45 is 78. That matches what he has left.", W("l6", "123 − 45 = 78")),
    B("So when something was spent or given away, add it back to what is left. That gives the start."),
])

# Three consecutive numbers add up to 36; the smallest?
LESSONS["Q_CH14_025"] = lesson([
    B("Three consecutive numbers add up to 36. Consecutive means they follow one after another, like 4, 5 and 6.",
      given("g1", "Three consecutive numbers add up to 36", label=True)),
    B("Think about the middle number. The smallest is 1 less than the middle. The largest is 1 more.",
      L("l1", "(middle − 1) + middle + (middle + 1) = 36")),
    B("Look: the minus 1 and the plus 1 cancel each other. So the total is just 3 times the middle number.",
      strike("l1", "− 1"), strike("l1", "+ 1"), L("l2", "3 × middle = 36")),
    B("So what is the middle number?",
      ask=choose(["12", "18", "33"], 0,
                 "3 times the middle number is 36. So the middle number is 36 divided by 3, which is 12.")),
    B("36 divided by 3 is 12. So the middle number is 12.", W("l3", "36 ÷ 3 = 12")),
    B("Careful: 12 is the middle number. The question asks for the smallest. Which is it?",
      ask=choose(["11", "12", "13"], 0,
                 "The smallest number comes just before the middle one. Just before 12 is 11.")),
    B("The three numbers are 11, 12 and 13. The smallest is 11.",
      answer("l4", "Smallest number = 11", label=True), mark("l4", "11", "circle")),
    B("Let's check. 11 plus 12 plus 13 is 36. It works!", W("l5", "11 + 12 + 13 = 36")),
    B("So for three numbers in a row, divide the total by 3 to get the middle one. Then step back by 1."),
])

# Solve: x + 5 = 12
LESSONS["EXT_G4_WS2_CH14_001"] = lesson([
    B("Here is our equation. x, plus 5, equals 12. Which number is hiding behind the x?",
      given("l1", "x + 5 = 12")),
    B("The equation says: some number, and 5 more, makes 12. To get back to the number, we undo the 5 more."),
    B("How do we undo plus 5?",
      ask=choose(["subtract 5", "add 5", "multiply by 5"], 0,
                 "Plus and minus are opposites. To undo plus 5, we subtract 5.")),
    B("We subtract 5 from both sides, so that the two sides stay equal.",
      strike("l1", "+ 5", "− 5"), both("l1", "− 5")),
    B("Start at 12 on the number line and hop back 5. We land on 7.",
      fig("f1", {"kind": "numberLine", "min": 0, "max": 12, "step": 1,
                 "hops": [{"from": 12, "to": 7, "label": "− 5"}]}),
      W("l2", "x = 12 − 5")),
    B("So x equals 7.", answer("l3", "x = 7"), mark("l3", "x = 7", "circle")),
    B("Let's check. 7 plus 5 is 12. It works!", W("l4", "7 + 5 = 12")),
    B("So to undo adding, subtract the same number from both sides. Adding it again would only take us further away."),
], "x", 7)

# Solve: 3x = 24
LESSONS["EXT_G4_WS2_CH14_002"] = lesson([
    B("Here is our equation. 3 x equals 24.", given("l1", "3x = 24")),
    B("3 x means 3 times x. Picture 3 equal boxes, with x in each one, holding 24 altogether.",
      bars("f1", (None, [(1, "x", "unknown")] * 3, "24"))),
    B("How do we find what is in one box?",
      ask=choose(["divide 24 by 3", "take 3 from 24", "multiply 24 by 3"], 0,
                 "The 24 is shared equally among 3 boxes. Sharing equally means dividing, so we divide 24 by 3.")),
    B("So we divide both sides by 3.", divide("l1", 3)),
    B("Use the 3 times table. 3 times 8 is 24. So 24 divided by 3 is 8.", W("l2", "24 ÷ 3 = 8")),
    B("So x equals 8.", answer("l3", "x = 8"), mark("l3", "x = 8", "circle")),
    B("Let's check. 3 times 8 is 24. And look: 3 times 7 is only 21, and 3 times 9 is 27. Only 8 fits.",
      W("l4", "3 × 8 = 24"), W("l5", "3 × 7 = 21"), W("l6", "3 × 9 = 27")),
    B("So a number next to x means times. To undo times, divide both sides."),
], "x", 8)

# Solve: x − 7 = 15
LESSONS["EXT_G4_WS2_CH14_003"] = lesson([
    B("Here is our equation. x, minus 7, equals 15.", given("l1", "x − 7 = 15")),
    B("A number had 7 taken away, and 15 was left. So the number we started with was bigger than 15."),
    B("How do we get back to the start?",
      ask=choose(["add 7 to 15", "take 7 from 15", "multiply 15 by 7"], 0,
                 "The 7 has already been taken away. Taking it away again gives a smaller number. "
                 "To go back, we add the 7 on again.")),
    B("So we add 7 to both sides.", strike("l1", "− 7", "+ 7"), both("l1", "+ 7"), W("l2", "x = 15 + 7")),
    B("15 plus 5 is 20, and 2 more is 22.", W("l3", "15 + 5 = 20"), W("l4", "20 + 2 = 22")),
    B("So x equals 22.", answer("l5", "x = 22"), mark("l5", "x = 22", "circle")),
    B("Let's check. 22 minus 7 is 15. It works!", W("l6", "22 − 7 = 15")),
    B("So to undo subtracting, add the same number to both sides."),
], "x", 22)

# Solve: x/4 = 5
LESSONS["EXT_G4_WS2_CH14_004"] = lesson([
    B("Here is our equation. x over 4 equals 5.", given("l1", "x/4 = 5")),
    B("x over 4 means x divided by 4. So x was shared into 4 equal parts, and each part is 5.",
      note("l1", "x/4", "x ÷ 4", "below"), bars("f1", ("x", [(1, "5", "a")] * 4))),
    B("How do we put x back together?",
      ask=choose(["multiply 5 by 4", "add 4 to 5", "take 4 from 5"], 0,
                 "There are 4 equal parts, and each part is 5. To get the whole, we need 4 lots of 5. "
                 "That is multiplying.")),
    B("To undo divide by 4, we multiply both sides by 4.", both("l1", "× 4")),
    B("5 times 4 is 20. So x equals 20.",
      W("l2", "5 × 4 = 20"), answer("l3", "x = 20"), mark("l3", "x = 20", "circle")),
    B("Let's check. 20 divided by 4 is 5. It works!", W("l4", "20 ÷ 4 = 5")),
    B("So we undo dividing by multiplying. The number that was divided is always the bigger one."),
], "x", 20)

# Solve: 2x + 3 = 11
LESSONS["EXT_G4_WS2_CH14_005"] = lesson([
    B("Here is our equation. 2 x, plus 3, equals 11.", given("l1", "2x + 3 = 11")),
    B("Picture a balance. On the left pan are 2 bags, each holding x marbles, and 3 loose marbles. "
      "On the right pan are 11 marbles.", balance("f1", "2x + 3", "11")),
    B("First we take the 3 loose marbles off the left. To keep it level, what must we do on the right?",
      ask=choose(["take off 3 marbles too", "add 3 marbles", "nothing"], 0,
                 "If we take marbles off one pan only, the balance tips. "
                 "So 3 marbles must come off the right pan as well.")),
    B("So 3 comes off both sides. 11 minus 3 is 8.",
      strike("l1", "+ 3", "− 3"), both("l1", "− 3"), W("l2", "2x = 8")),
    B("Now 2 bags balance 8 marbles. How many marbles are in one bag?",
      ask=choose(["4", "8", "6"], 0,
                 "The 2 bags are equal, and together they hold 8. So each bag holds half of 8, which is 4.")),
    B("We divide both sides by 2. Half of 8 is 4. So x equals 4.",
      divide("l2", 2), answer("l3", "x = 4"), mark("l3", "x = 4", "circle")),
    B("Let's check. 2 times 4 is 8, and 8 plus 3 is 11. It works!", W("l4", "2 × 4 + 3 = 11")),
    B("So first take the loose number away from both sides. Then share what is left equally."),
], "x", 4)

# Solve: 5x − 2 = 18
LESSONS["EXT_G4_WS2_CH14_006"] = lesson([
    B("Here is our equation. 5 x, minus 2, equals 18.", given("l1", "5x − 2 = 18")),
    B("So x was multiplied by 5, then 2 was taken away, and 18 was left. Let's walk backwards from 18.",
      note("l1", "5x", "5 × x", "below")),
    B("Just before the 2 was taken away, what was the number?",
      ask=choose(["20", "16", "18"], 0,
                 "Taking away 2 left 18. So just before that, the number was 2 bigger than 18. That is 20.")),
    B("So we add 2 to both sides. 18 plus 2 is 20. That means 5 x equals 20.",
      strike("l1", "− 2", "+ 2"), both("l1", "+ 2"), W("l2", "5x = 20")),
    B("5 times x is 20. What undoes times 5?",
      ask=choose(["divide by 5", "subtract 5", "multiply by 5"], 0,
                 "Times and divide are partners. To undo times 5, we divide by 5.")),
    B("20 divided by 5 is 4, because 5 times 4 is 20. So x equals 4.",
      divide("l2", 5), answer("l3", "x = 4"), mark("l3", "x = 4", "circle")),
    B("Let's check. 5 times 4 is 20, and 20 minus 2 is 18. It works!", W("l4", "5 × 4 − 2 = 18")),
    B("So undo the subtracting by adding. Then undo the times by dividing."),
], "x", 4)

# 3 times a number plus 7 equals 28
LESSONS["EXT_G4_WS2_CH14_007"] = lesson([
    B("3 times a number, plus 7, equals 28. Let's call the number n and write it as an equation.",
      given("l1", "3 × n + 7 = 28")),
    B("Think of a machine. A number goes in. It is multiplied by 3. Then 7 is added. Out comes 28.",
      L("l2", "n → × 3 → + 7 → 28")),
    B("To find what went in, we run the machine backwards. What do we do to 28 first?",
      ask=choose(["take away 7", "divide by 3", "add 7"], 0,
                 "Going backwards, we undo the last step first. The last step was adding 7, "
                 "so first we take away 7.")),
    B("28 minus 7 is 21. So 3 times the number is 21.", W("l3", "28 − 7 = 21"), W("l4", "3 × n = 21")),
    B("And then? How do we undo times 3?",
      ask=choose(["divide by 3", "take away 3", "multiply by 3"], 0,
                 "Times and divide are partners. To undo times 3, we divide by 3.")),
    B("21 divided by 3 is 7. So the number is 7.",
      W("l5", "21 ÷ 3 = 7"), answer("l6", "n = 7"), mark("l6", "n = 7", "circle")),
    B("Let's check. 3 times 7 is 21, and 21 plus 7 is 28. It works!", W("l7", "3 × 7 + 7 = 28")),
    B("So run the machine backwards. Undo the last step first, then the one before."),
], "n", 7)

# Two consecutive numbers add up to 25; the smaller?
LESSONS["EXT_G4_WS2_CH14_008"] = lesson([
    B("Two consecutive numbers add up to 25. Consecutive numbers come one after the other, like 8 and 9.",
      given("g1", "Two consecutive numbers add up to 25", label=True)),
    B("So the bigger number is the smaller number, and 1 more.",
      bars("f1", ("Smaller", [(4, "?", "unknown")]), ("Bigger", [(4, "?", "unknown"), (1, "1", "c")]))),
    B("If we take that extra 1 away from 25, what is left?",
      ask=choose(["two equal numbers", "the smaller number", "the bigger number"], 0,
                 "Without the extra 1, the bigger number is the same as the smaller one. "
                 "So what is left is two equal numbers.")),
    B("25 minus 1 is 24. So two lots of the smaller number make 24.", W("l1", "25 − 1 = 24")),
    B("Half of 24 is 12. So the smaller number is 12.", W("l2", "24 ÷ 2 = 12")),
    B("If the smaller number is 12, what is the bigger one?",
      ask=choose(["13", "11", "24"], 0,
                 "Consecutive numbers go up by 1. The number just after 12 is 13.")),
    B("So the numbers are 12 and 13. The question asks for the smaller one, which is 12.",
      answer("l3", "Smaller number = 12", label=True), mark("l3", "12", "circle")),
    B("Let's check. 12 plus 13 is 25. It works!", W("l4", "12 + 13 = 25")),
    B("So for two numbers in a row, take 1 off the total, then halve. That gives the smaller one."),
])
