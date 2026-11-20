"""Lessons written one by one: the hand-crafted equations Q_CH14_001 to Q_CH14_016.

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, W, answer, balance, bars, both, choose, divide, given, group, lesson, mark,
                                  note, strike)

LESSONS = {}

# a + 5 = 12
LESSONS["Q_CH14_001"] = lesson([
    B("Here is our equation. a, plus 5, equals 12. The letter a is a hidden number, and we are going to find it.",
      given("l1", "a + 5 = 12")),
    B("Both sides are worth the same, like a level balance. Some number, with 5 added to it, makes 12.",
      balance("f1", "a + 5", "12")),
    B("5 was added to a. So, how do we undo adding 5?",
      ask=choose(["take away 5", "add 5 again", "multiply by 5"], 0,
                 "Adding and taking away are partners. To undo plus 5, we take 5 away. "
                 "Adding again would only make the number bigger.")),
    B("So we take 5 away. And to keep the balance level, we take it from both sides.",
      strike("l1", "+ 5", "− 5"), both("l1", "− 5")),
    B("On the left, only a is left. On the right, 12 minus 5 is 7.", W("l2", "a = 12 − 5")),
    B("So a equals 7. There is our hidden number!", answer("l3", "a = 7"), mark("l3", "a = 7", "circle")),
    B("Let's check. 7 plus 5 is 12. It works!", W("l4", "7 + 5 = 12")),
    B("So when a number has been added, we undo it by taking that number away from both sides."),
], "a", 7)

# b − 5 = 12
LESSONS["Q_CH14_002"] = lesson([
    B("Here is our equation. b, minus 5, equals 12. The letter b stands for a hidden number.",
      given("l1", "b − 5 = 12")),
    B("Think of it as a story. I had b sweets. I gave 5 away, and 12 are left. "
      "Did I start with more than 12, or fewer?",
      ask=choose(["more than 12", "fewer than 12"], 0,
                 "Some sweets were given away, and 12 are still left. "
                 "So before giving any away, there must have been more than 12.")),
    B("So b is bigger than 12. To undo taking away 5, we put the 5 back. We add 5 to both sides.",
      strike("l1", "− 5", "+ 5"), both("l1", "+ 5")),
    B("On the left, only b is left. On the right, 12 plus 5 is 17.", W("l2", "b = 12 + 5")),
    B("So b equals 17.", answer("l3", "b = 17"), mark("l3", "b = 17", "circle")),
    B("Careful with this one. 12 minus 5 is 7, but that takes the 5 away a second time. We needed to put it back."),
    B("Let's check. 17 minus 5 is 12. It works!", W("l4", "17 − 5 = 12")),
    B("So to undo taking away, we add. And we always do the same to both sides."),
], "b", 17)

# 3c = 12
LESSONS["Q_CH14_003"] = lesson([
    B("Here is our equation. 3 c equals 12. We want to find the hidden number c.", given("l1", "3c = 12")),
    B("When a number is written right next to a letter, it means times. So 3 c is 3 times c.",
      note("l1", "3c", "3 × c", "below")),
    B("3 times some number makes 12. What undoes times 3?",
      ask=choose(["divide by 3", "take away 3", "multiply by 3"], 0,
                 "Times and divide are partners. To undo times 3, we divide by 3. "
                 "Taking away would undo adding, and nothing was added here.")),
    B("So we divide both sides by 3.", divide("l1", 3)),
    B("12 divided by 3 is 4, because 3 times 4 is 12. So c equals 4.",
      W("l2", "12 ÷ 3 = 4"), answer("l3", "c = 4"), mark("l3", "c = 4", "circle")),
    B("Let's check. 3 times 4 is 12. Both sides match.", W("l4", "3 × 4 = 12")),
    B("So a number next to a letter means times, and we undo times by dividing."),
], "c", 4)

# d/3 = 12
LESSONS["Q_CH14_004"] = lesson([
    B("Here is our equation. d over 3 equals 12. Let's find the hidden number d.", given("l1", "d/3 = 12")),
    B("A letter over a number means divide. So d was divided by 3, and the answer was 12.",
      note("l1", "d/3", "d ÷ 3", "below")),
    B("Picture d as a bar cut into 3 equal parts. Each part is 12.",
      bars("f1", ("d", [(1, "12", "a"), (1, "12", "a"), (1, "12", "a")]))),
    B("So how do we get back to the whole of d?",
      ask=choose(["multiply 12 by 3", "divide 12 by 3", "add 3 to 12"], 0,
                 "d was cut into 3 equal parts of 12. To build d again we need all 3 parts, "
                 "so we multiply 12 by 3.")),
    B("To undo divide by 3, we multiply by 3. And we do it to both sides.", both("l1", "× 3")),
    B("3 times 10 is 30, and 3 times 2 is 6. So 3 times 12 is 36. That means d equals 36.",
      W("l2", "12 × 3 = 30 + 6"), answer("l3", "d = 36"), mark("l3", "d = 36", "circle")),
    B("Let's check. 36 divided by 3 is 12. It works!", W("l4", "36 ÷ 3 = 12")),
    B("So we undo dividing by multiplying. Dividing again would make d smaller, and d has to be bigger than 12."),
], "d", 36)

# 5 + e = 12
LESSONS["Q_CH14_005"] = lesson([
    B("Here is our equation. 5, plus e, equals 12. The letter e is a hidden number.", given("l1", "5 + e = 12")),
    B("Look at the bar. The whole bar is 12. One part is 5, and the other part is e.",
      bars("f1", (None, [(5, "5", "a"), (7, "e", "unknown")], "12"))),
    B("We know the whole and one part. How do we find the other part?",
      ask=choose(["take 5 away from 12", "add 5 to 12", "multiply 5 by 12"], 0,
                 "The whole bar is 12, so e must be smaller than 12. "
                 "We take the part we know, 5, away from the whole.")),
    B("On the equation, that means taking 5 from both sides.", strike("l1", "5", "− 5"), both("l1", "− 5")),
    B("12 minus 5 is 7. So e equals 7.",
      W("l2", "e = 12 − 5"), answer("l3", "e = 7"), mark("l3", "e = 7", "circle")),
    B("Let's check. 5 plus 7 is 12. It works!", W("l4", "5 + 7 = 12")),
    B("So when two parts make a total, the hidden part is the total take away the part we know."),
], "e", 7)

# 15 − f = 6
LESSONS["Q_CH14_006"] = lesson([
    B("Here is our equation. 15, minus f, equals 6. This time the hidden number is the one being taken away.",
      given("l1", "15 − f = 6")),
    B("Think of 15 sweets. We eat f of them, and 6 are left.",
      bars("f1", (None, [(9, "f", "unknown"), (6, "6", "a")], "15"))),
    B("So how many did we eat? How do we find f?",
      ask=choose(["15 take away 6", "15 plus 6", "f is just 6"], 0,
                 "The 15 sweets are in two parts: the f we ate, and the 6 that are left. "
                 "So f is 15 take away 6.")),
    B("15 minus 6 is 9. So f equals 9.",
      W("l2", "f = 15 − 6"), answer("l3", "f = 9"), mark("l3", "f = 9", "circle")),
    B("Notice that f has to be smaller than 15. We cannot eat more sweets than we have."),
    B("Let's check. 15 minus 9 is 6. It works!", W("l4", "15 − 9 = 6")),
    B("So when the hidden number is the one taken away, find the gap between the start and what is left."),
], "f", 9)

# 32/g = 4
LESSONS["Q_CH14_007"] = lesson([
    B("Here is our equation. 32 over g equals 4. That means 32 divided by g is 4.",
      given("l1", "32/g = 4"), note("l1", "32/g", "32 ÷ g", "below")),
    B("Think of 32 sweets shared into g groups, with 4 in each group. So g groups of 4 make 32.",
      W("l2", "g × 4 = 32")),
    B("Which number times 4 makes 32? Use your 4 times table.",
      ask=choose(["8", "28", "36"], 0,
                 "Adding 4 or taking away 4 does not help, because this is about sharing. "
                 "In the 4 times table, 8 times 4 is 32.")),
    B("8 times 4 is 32. So 32 divided by 4 gives us g.", W("l3", "32 ÷ 4 = 8")),
    B("So g equals 8.", answer("l4", "g = 8"), mark("l4", "g = 8", "circle")),
    B("Let's check. 32 divided by 8 is 4. It works!", W("l5", "32 ÷ 8 = 4")),
    B("So when the letter is the number we divide by, turn it into a times fact and use the table."),
], "g", 8)

# 7 + h + 2 = 15
LESSONS["Q_CH14_008"] = lesson([
    B("Here is our equation. 7, plus h, plus 2, equals 15.", given("l1", "7 + h + 2 = 15")),
    B("There are two plain numbers on the left, 7 and 2. Let's put them together first.",
      group("l1", ["7", "2"], "7 + 2 = 9")),
    B("7 plus 2 is 9. So the equation becomes 9, plus h, equals 15.", W("l2", "9 + h = 15")),
    B("Now, how do we find h?",
      ask=choose(["take 9 away from 15", "take only 7 away from 15", "add 9 to 15"], 0,
                 "Both the 7 and the 2 sit with h, and together they make 9. "
                 "So we take the whole 9 away from 15.")),
    B("So we take 9 from both sides.", strike("l2", "9", "− 9"), both("l2", "− 9")),
    B("15 minus 9 is 6. So h equals 6.",
      W("l3", "h = 15 − 9"), answer("l4", "h = 6"), mark("l4", "h = 6", "circle")),
    B("Let's check. 7, plus 6, plus 2, makes 15. It works!", W("l5", "7 + 6 + 2 = 15")),
    B("So first join the plain numbers together. Then undo the adding."),
], "h", 6)

# 2x + 3 = 11
LESSONS["Q_CH14_009"] = lesson([
    B("Here is our equation. 2 x, plus 3, equals 11. Two things were done to x, so we have two things to undo.",
      given("l1", "2x + 3 = 11")),
    B("First x was doubled. Then 3 was added. We undo them backwards, like taking off shoes before socks.",
      note("l1", "2x", "2 × x", "below")),
    B("So which do we undo first?",
      ask=choose(["the plus 3", "the times 2"], 0,
                 "The plus 3 was done last, so it comes off first. "
                 "If we halved 11 straight away, we would get a messy number.")),
    B("To undo plus 3, we take 3 from both sides.", strike("l1", "+ 3", "− 3"), both("l1", "− 3")),
    B("11 minus 3 is 8. So 2 x equals 8.", W("l2", "2x = 11 − 3"), W("l3", "2x = 8")),
    B("2 x means 2 times x. If 2 times x is 8, what is x?",
      ask=choose(["4", "8", "16"], 0,
                 "8 is 2 times x, so x is half of 8. We divide by 2, and that gives 4.")),
    B("We divide both sides by 2. 8 divided by 2 is 4. So x equals 4.",
      divide("l3", 2), answer("l4", "x = 4"), mark("l4", "x = 4", "circle")),
    B("Let's check. 2 times 4 is 8, and 8 plus 3 is 11. It works!", W("l5", "2 × 4 + 3 = 11")),
    B("So with two steps, undo the adding first, then the times. Last on, first off."),
], "x", 4)

# 5m − 7 = 18
LESSONS["Q_CH14_010"] = lesson([
    B("Here is our equation. 5 m, minus 7, equals 18. Let's find the hidden number m.",
      given("l1", "5m − 7 = 18")),
    B("5 m means 5 times m. So m was multiplied by 5, and then 7 was taken away.",
      note("l1", "5m", "5 × m", "below")),
    B("The minus 7 was done last, so we undo it first. How?",
      ask=choose(["add 7 to both sides", "take 7 from both sides", "divide both sides by 7"], 0,
                 "The 7 was already taken away. To undo that we put it back, so we add 7. "
                 "Taking it away again would move us further from the start.")),
    B("So we add 7 to both sides.", strike("l1", "− 7", "+ 7"), both("l1", "+ 7")),
    B("18 plus 7 is 25. So 5 m equals 25.", W("l2", "5m = 18 + 7"), W("l3", "5m = 25")),
    B("Careful: 25 is 5 m, not m. We have one more step. What undoes times 5?",
      ask=choose(["divide by 5", "take away 5", "multiply by 5"], 0,
                 "Times and divide are partners. To undo times 5, we divide by 5.")),
    B("25 divided by 5 is 5. So m equals 5.",
      divide("l3", 5), answer("l4", "m = 5"), mark("l4", "m = 5", "circle")),
    B("Let's check. 5 times 5 is 25, and 25 minus 7 is 18. It works!", W("l5", "5 × 5 − 7 = 18")),
    B("So undo the taking away by adding. Then undo the times by dividing."),
], "m", 5)

# x/3 + 5 = 10
LESSONS["Q_CH14_011"] = lesson([
    B("Here is our equation. x over 3, plus 5, equals 10.", given("l1", "x/3 + 5 = 10")),
    B("x over 3 means x divided by 3. So x was divided by 3, and then 5 was added.",
      note("l1", "x/3", "x ÷ 3", "below")),
    B("Which do we undo first?",
      ask=choose(["the plus 5", "the divide by 3"], 0,
                 "We undo the last thing first, and the plus 5 came last. "
                 "If we multiplied 10 by 3 straight away, the 5 would get counted 3 times.")),
    B("So we take 5 from both sides.", strike("l1", "+ 5", "− 5"), both("l1", "− 5")),
    B("10 minus 5 is 5. So x over 3 equals 5.", W("l2", "x/3 = 10 − 5"), W("l3", "x/3 = 5")),
    B("x divided by 3 is 5. Careful, 5 is not x yet. What undoes divide by 3?",
      ask=choose(["multiply by 3", "divide by 3", "take away 3"], 0,
                 "Divide and times are partners. x was cut into 3 equal parts of 5. "
                 "To build x again, we multiply 5 by 3.")),
    B("So we multiply both sides by 3. 5 times 3 is 15. So x equals 15.",
      both("l3", "× 3"), answer("l4", "x = 15"), mark("l4", "x = 15", "circle")),
    B("Let's check. 15 divided by 3 is 5, and 5 plus 5 is 10. It works!", W("l5", "15 ÷ 3 + 5 = 10")),
    B("So undo the adding first. Then undo the dividing by multiplying."),
], "x", 15)

# y/4 − 8 = 0
LESSONS["Q_CH14_012"] = lesson([
    B("Here is our equation. y over 4, minus 8, equals 0.", given("l1", "y/4 − 8 = 0")),
    B("Look at the right side. It is 0. So after we take away 8, nothing is left.", mark("l1", "0", "circle")),
    B("If taking away 8 leaves nothing, what must y over 4 be?",
      ask=choose(["8", "0", "4"], 0,
                 "Think of having some sweets, giving away 8, and having none left. "
                 "Then you must have started with exactly 8.")),
    B("So y over 4 equals 8. On the board, that is adding 8 to both sides.",
      strike("l1", "− 8", "+ 8"), both("l1", "+ 8"), W("l2", "y/4 = 8")),
    B("y over 4 means y divided by 4. So 8 is only one of 4 equal parts of y. It is not y itself.",
      note("l2", "y/4", "y ÷ 4", "below")),
    B("What undoes divide by 4?",
      ask=choose(["multiply by 4", "divide by 4", "add 4"], 0,
                 "Divide and times are partners. y was cut into 4 equal parts of 8, "
                 "so we multiply 8 by 4 to build y again.")),
    B("8 times 4 is 32. So y equals 32.",
      both("l2", "× 4"), W("l3", "8 × 4 = 32"), answer("l4", "y = 32"), mark("l4", "y = 32", "circle")),
    B("Let's check. 32 divided by 4 is 8, and 8 minus 8 is 0. It works!", W("l5", "32 ÷ 4 − 8 = 0")),
    B("So undo the taking away first. Then undo the dividing by multiplying."),
], "y", 32)

# z = 12 − 2z
LESSONS["Q_CH14_013"] = lesson([
    B("Here is our equation. z equals 12, minus 2 z. Look closely: the letter z is on both sides.",
      given("l1", "z = 12 − 2z")),
    B("We want all the z together on one side. On the right, 2 z is being taken away.",
      mark("l1", "2z", "underline")),
    B("How do we clear away the minus 2 z on the right?",
      ask=choose(["add 2z to both sides", "take 2z from both sides", "divide both sides by 2"], 0,
                 "The 2 z is being taken away. To undo taking away, we add. So we add 2 z to both sides.")),
    B("So we add 2 z to both sides. On the right, minus 2 z and plus 2 z cancel, and just 12 is left.",
      strike("l1", "− 2z", "+ 2z"), both("l1", "+ 2z"), W("l2", "z + 2z = 12")),
    B("On the left we now have z, plus 2 z. How many z is that altogether?",
      ask=choose(["3z", "2z", "4z"], 0,
                 "The z standing on its own counts as 1 z. So 1 z and 2 z make 3 z.")),
    B("So 3 z equals 12.", group("l2", ["z", "2z"], "3z"), W("l3", "3z = 12")),
    B("3 z means 3 times z, so we divide both sides by 3. 12 divided by 3 is 4. So z equals 4.",
      divide("l3", 3), answer("l4", "z = 4"), mark("l4", "z = 4", "circle")),
    B("Let's check. The left side is 4. The right side is 12, minus 2 times 4. That is 12 minus 8, which is 4. "
      "Both sides match.", W("l5", "12 − 2 × 4 = 4")),
    B("So when the letter is on both sides, first bring all the letters to one side. Then solve as usual."),
], "z", 4)

# 6a − 32 = 2a
LESSONS["Q_CH14_014"] = lesson([
    B("Here is our equation. 6 a, minus 32, equals 2 a. The letter a is on both sides.",
      given("l1", "6a − 32 = 2a")),
    B("Think of a as a bag of sweets. 6 bags, with 32 sweets taken out, weigh the same as 2 bags.",
      balance("f1", "6a − 32", "2a")),
    B("Let's get the bags together. If we take 2 a from both sides, how many a are left on the left?",
      ask=choose(["4a", "8a", "6a"], 0,
                 "6 a take away 2 a leaves 4 a. We are taking away here, not adding, so it is not 8 a.")),
    B("We take 2 a from both sides. The right side becomes 0, and the left becomes 4 a, minus 32.",
      both("l1", "− 2a"), W("l2", "4a − 32 = 0")),
    B("If 4 a, minus 32, leaves nothing, then 4 a must be exactly 32.",
      strike("l2", "− 32", "+ 32"), W("l3", "4a = 32")),
    B("4 times a is 32. What do we do now?",
      ask=choose(["divide 32 by 4", "divide 32 by 8", "take 4 from 32"], 0,
                 "4 a means 4 times a. To undo times 4, we divide by 4.")),
    B("32 divided by 4 is 8, because 4 times 8 is 32. So a equals 8.",
      divide("l3", 4), answer("l4", "a = 8"), mark("l4", "a = 8", "circle")),
    B("Let's check. 6 times 8 is 48, and 48 minus 32 is 16. And 2 times 8 is also 16. Both sides match.",
      W("l5", "6 × 8 = 48"), W("l6", "48 − 32 = 16"), W("l7", "2 × 8 = 16")),
    B("Notice that 16 is what each side is worth. The question asks for a, and a is 8."),
    B("So when the letter is on both sides, gather the letters first. Then divide."),
], "a", 8)

# 4b + 5 = 2b + 19
LESSONS["Q_CH14_015"] = lesson([
    B("Here is our equation. 4 b, plus 5, equals 2 b, plus 19. There are letters and plain numbers on both sides.",
      given("l1", "4b + 5 = 2b + 19")),
    B("Our plan is to get the letters on one side and the plain numbers on the other.",
      balance("f1", "4b + 5", "2b + 19")),
    B("Let's start with the letters. What do we take from both sides, so that the right side has no b?",
      ask=choose(["2b", "4b", "5"], 0,
                 "The right side has 2 b. If we take 2 b from both sides, the right side has no b left.")),
    B("We take 2 b from both sides. 4 b take away 2 b leaves 2 b.",
      strike("l1", "2b", "− 2b"), both("l1", "− 2b"), W("l2", "2b + 5 = 19")),
    B("Now it is a two-step equation. What comes off next?",
      ask=choose(["take 5 from both sides", "add 5 to both sides", "divide both sides by 5"], 0,
                 "The 5 is added on the left. To undo adding, we take away. So 5 comes off both sides.")),
    B("19 minus 5 is 14. So 2 b equals 14.",
      strike("l2", "+ 5", "− 5"), both("l2", "− 5"), W("l3", "2b = 14")),
    B("2 b means 2 times b, so we halve. Half of 14 is 7. So b equals 7.",
      divide("l3", 2), answer("l4", "b = 7"), mark("l4", "b = 7", "circle")),
    B("Let's check. Left: 4 times 7, plus 5, makes 33. Right: 2 times 7, plus 19, also makes 33. Both sides match.",
      W("l5", "4 × 7 + 5 = 33"), W("l6", "2 × 7 + 19 = 33")),
    B("So gather the letters on one side and the numbers on the other. Always do the same to both sides."),
], "b", 7)

# 7 + 5c = 3c + 25
LESSONS["Q_CH14_016"] = lesson([
    B("Here is our equation. 7, plus 5 c, equals 3 c, plus 25.", given("l1", "7 + 5c = 3c + 25")),
    B("Think of c as a box of marbles. The left pan has 7 marbles and 5 boxes. "
      "The right pan has 3 boxes and 25 marbles.", balance("f1", "7 + 5c", "3c + 25")),
    B("If we lift 3 boxes off each pan, the balance stays level. How many boxes stay on the left?",
      ask=choose(["2 boxes", "8 boxes", "5 boxes"], 0,
                 "There were 5 boxes on the left, and we lift 3 off. 5 take away 3 leaves 2 boxes.")),
    B("So we take 3 c from both sides. Now 7, plus 2 c, equals 25.",
      strike("l1", "3c", "− 3c"), both("l1", "− 3c"), W("l2", "7 + 2c = 25")),
    B("Next, the 7 loose marbles on the left. What do we do with them?",
      ask=choose(["take 7 from both sides", "add 7 to both sides", "take 7 from the left only"], 0,
                 "To undo the plus 7, we take 7 away. And it must come off both pans, or the balance would tip.")),
    B("25 minus 7 is 18. So 2 c equals 18.",
      strike("l2", "7", "− 7"), both("l2", "− 7"), W("l3", "2c = 18")),
    B("2 boxes hold 18 marbles, so one box holds half of 18, which is 9. So c equals 9.",
      divide("l3", 2), answer("l4", "c = 9"), mark("l4", "c = 9", "circle")),
    B("Let's check. Left: 7, plus 5 times 9, makes 52. Right: 3 times 9, plus 25, also makes 52. Level!",
      W("l5", "7 + 5 × 9 = 52"), W("l6", "3 × 9 + 25 = 52")),
    B("So take the same boxes off both pans, then the same loose marbles. What is left tells you one box."),
], "c", 9)
