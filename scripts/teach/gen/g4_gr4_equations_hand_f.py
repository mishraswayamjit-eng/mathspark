"""Lessons written one by one: G4A_EQUATIONS_021 to 034.

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, L, W, answer, bars, choose, fig, given, group, lesson, mark, strike)

LESSONS = {}

# Asha adds 8 then doubles; Bina doubles then adds 8
LESSONS["G4A_EQUATIONS_021"] = lesson([
    B("Asha and Bina start with the same number. Asha adds 8, then doubles. Bina doubles, then adds 8. "
      "How much greater is Asha's answer?", given("g1", "Asha: + 8, then × 2.  Bina: × 2, then + 8", label=True)),
    B("We are not told the starting number. So let's try an easy one. Let's start with 1."),
    B("Asha first. 1 plus 8 is 9, and double 9 is 18.", W("l1", "(1 + 8) × 2 = 18")),
    B("Now Bina, starting with 1. She doubles first, then adds 8. What does she get?",
      ask=choose(["10", "18", "9"], 0,
                 "Bina doubles first: double 1 is 2. Then she adds 8. And 2 plus 8 is 10.")),
    B("Double 1 is 2, and 2 plus 8 is 10. So Asha has 18 and Bina has 10. Asha is ahead by 8.",
      W("l2", "1 × 2 + 8 = 10"), W("l3", "18 − 10 = 8")),
    B("Why 8? Asha adds her 8 before doubling, so her 8 gets doubled to 16. Bina's 8 is added after, "
      "so it stays 8.", W("l4", "8 × 2 = 16"), W("l5", "16 − 8 = 8")),
    B("Let's try starting with 5 as well. Look at the two new lines. Is the gap still 8, or has it changed?",
      W("l6", "(5 + 8) × 2 = 26"), W("l7", "5 × 2 + 8 = 18"),
      ask=choose(["it is still 8", "it has changed"], 0,
                 "Look at the board. Starting with 5, Asha gets 26 and Bina gets 18. And 26 minus 18 is still 8.")),
    B("So whatever the starting number, Asha's answer is 8 greater.",
      answer("l8", "Asha is 8 greater", label=True), mark("l8", "8", "circle")),
    B("The order of the steps matters. Adding before doubling means the extra gets doubled too."),
])

# Digits add up to 9; swapped number is 27 more
LESSONS["G4A_EQUATIONS_022"] = lesson([
    B("A two-digit number has digits that add up to 9. When we swap the digits, the new number is 27 more. "
      "What is the number?", given("g1", "Digits add up to 9; swapped number is 27 more", label=True)),
    B("Let's use the first clue to make a list. Two-digit numbers whose digits add up to 9: "
      "18, 27, 36, 45, and so on.", L("l1", "18, 27, 36, 45, 54, 63, 72, 81, 90")),
    B("Swapping must make the number bigger. So which digit must be the smaller one?",
      ask=choose(["the tens digit", "the ones digit"], 0,
                 "If the tens digit is the small one, then after the swap the big digit moves to the tens place, "
                 "and the number grows.")),
    B("So we only need to test 18, 27, 36 and 45.", group("l1", ["18", "27", "36", "45"], "test these")),
    B("18 swapped is 81. The gap is 63. Too big. 27 swapped is 72. The gap is 45. Still too big.",
      W("l2", "81 − 18 = 63"), W("l3", "72 − 27 = 45")),
    B("Now 36. Swapped, it is 63. What is 63 minus 36?",
      ask=choose(["27", "33", "9"], 0,
                 "63 minus 36 is 27. You can check by adding: 36 plus 27 is 63.")),
    B("63 minus 36 is 27. That is exactly the gap we want! So the first number is 36.",
      W("l4", "63 − 36 = 27"), answer("l5", "The number is 36", label=True), mark("l5", "36", "circle")),
    B("Careful: 63 is in the choices too. But the first number must be the smaller one, "
      "because swapping makes it grow."),
    B("So use one clue to make a short list. Then test the list with the other clue."),
])

# Ravi has 4 times Sonu's marbles; after 5 more each, 3 times
_WHO = ["When", "Sonu", "Ravi"]
LESSONS["G4A_EQUATIONS_023"] = lesson([
    B("Ravi has 4 times as many marbles as Sonu. Then each boy wins 5 more. Now Ravi has 3 times as many as Sonu. "
      "How many did Sonu have at first?",
      given("g1", "Ravi = 4 × Sonu. After + 5 each, Ravi = 3 × Sonu", label=True)),
    B("This is tricky to solve straight away. So let's be detectives, and test a number in the story. "
      "Try Sonu with 5 marbles."),
    B("If Sonu had 5, Ravi had 4 times 5, which is 20. After winning 5 each, they have 10 and 25.",
      fig("f1", {"kind": "table", "headers": _WHO, "rows": [["At first", "5", "20"], ["After 5 more", "10", "25"]]})),
    B("Is 25 three times 10?",
      ask=choose(["No, 3 times 10 is 30", "Yes"], 0,
                 "3 times 10 is 30, not 25. So starting with 5 does not fit the second clue.")),
    B("So 5 does not work. Let's try Sonu with 10. Then Ravi had 4 times 10, which is 40.", W("l1", "4 × 10 = 40")),
    B("After winning 5 each, Sonu has 15 and Ravi has 45.", W("l2", "10 + 5 = 15"), W("l3", "40 + 5 = 45")),
    B("Is 45 three times 15?",
      ask=choose(["Yes", "No"], 0,
                 "3 times 10 is 30, and 3 times 5 is 15. Then 30 plus 15 is 45. So yes, it fits!")),
    B("3 times 15 is 45. Both clues fit! So Sonu had 10 marbles at first.",
      W("l4", "3 × 15 = 45"), answer("l5", "Sonu had 10 marbles", label=True), mark("l5", "10", "circle")),
    B("Careful with 15 and 40. 15 is Sonu after winning, and 40 is Ravi at first. "
      "The question asks for Sonu at first."),
    B("So when a puzzle is hard to solve directly, test a number in the story, and check every clue."),
])

# Mangoes: half and 1 more, twice; 3 left
LESSONS["G4A_EQUATIONS_024"] = lesson([
    B("A basket has some mangoes. Asha takes half of them and 1 more. Then Bala takes half of what is left "
      "and 1 more. Now 3 are left.", given("g1", "Asha: half + 1. Bala: half + 1. Left: 3", label=True)),
    B("We know the end, so we go backwards. Start with the 3 mangoes left after Bala."),
    B("Bala took half, and then 1 more. Going backwards, what do we undo first?",
      ask=choose(["put back the 1 extra mango", "double the 3"], 0,
                 "The 1 extra mango was the very last thing Bala took. So it is the first thing we put back.")),
    B("Put back Bala's extra 1. 3 plus 1 is 4. That 4 is the half Bala did not take.", W("l1", "3 + 1 = 4")),
    B("So before Bala, there were double 4. That is 8 mangoes.", W("l2", "4 × 2 = 8")),
    B("Now Asha. After she took her share, 8 were left. What do we do with the 8?",
      ask=choose(["add 1, then double", "double, then add 1", "just double"], 0,
                 "Same as before. Asha's extra 1 was taken last, so we put it back first. Then we double.")),
    B("8 plus 1 is 9. That 9 is half the basket. Double 9 is 18.", W("l3", "8 + 1 = 9"), W("l4", "9 × 2 = 18")),
    B("So there were 18 mangoes at first.",
      answer("l5", "Mangoes at first = 18", label=True), mark("l5", "18", "circle")),
    B("Let's check. Asha takes half of 18, which is 9, and 1 more. That is 10, leaving 8. "
      "Bala takes 4 and 1 more, leaving 3. It works!", W("l6", "18 − 10 = 8"), W("l7", "8 − 5 = 3")),
    B("So going backwards, put back the extra first, then double. Do it once for each person."),
])

# Kavya's game: + 5 for a win, − 2 for a loss
LESSONS["G4A_EQUATIONS_025"] = lesson([
    B("Kavya gets 5 points for each round she wins, and loses 2 points for each round she loses. "
      "After 20 rounds she has 65 points.", given("g1", "Win: + 5. Lose: − 2. 20 rounds, 65 points", label=True)),
    B("Let's pretend she won all 20 rounds. Then she would have 20 times 5 points. That is 100.",
      W("l1", "20 × 5 = 100")),
    B("But she has only 65. She is 35 points short of 100.", W("l2", "100 − 65 = 35")),
    B("Each time a win turns into a loss, how many points does she drop?",
      ask=choose(["7", "5", "2"], 0,
                 "She misses the 5 points she would have won. And she loses 2 more as well. 5 plus 2 is 7.")),
    B("Each lost round costs her 7 points: the 5 she did not win, and 2 more taken away.", W("l3", "5 + 2 = 7")),
    B("She is 35 points short. 35 divided by 7 is 5. So she lost 5 rounds.", W("l4", "35 ÷ 7 = 5")),
    B("Careful! 5 is the rounds she lost. How many did she win?",
      ask=choose(["15", "5", "13"], 0, "She played 20 rounds and lost 5. So she won 20 minus 5, which is 15.")),
    B("20 minus 5 is 15. So Kavya won 15 rounds.", answer("l5", "20 − 5 = 15"), mark("l5", "15", "circle")),
    B("Let's check. 15 wins give 75 points. 5 losses take away 10. And 75 minus 10 is 65. It works!",
      W("l6", "15 × 5 = 75"), W("l7", "5 × 2 = 10"), W("l8", "75 − 10 = 65")),
    B("So pretend every round was a win. Then see how many points are missing, and what each loss costs."),
])

# 2 pens + 3 pencils = ₹36; 2 pens + 5 pencils = ₹48
LESSONS["G4A_EQUATIONS_026"] = lesson([
    B("2 pens and 3 pencils cost 36 rupees. 2 pens and 5 pencils cost 48 rupees. We want the price of one pen.",
      given("g1", "2 pens + 3 pencils = ₹36", label=True), given("g2", "2 pens + 5 pencils = ₹48", label=True)),
    B("Compare the two lines. What is different in the second one?",
      ask=choose(["2 more pencils", "2 more pens", "nothing"], 0,
                 "Both have 2 pens. The first has 3 pencils and the second has 5. "
                 "So the second has 2 more pencils.")),
    B("The second has 2 extra pencils, and it costs more. 48 minus 36 is 12. So 2 pencils cost 12 rupees.",
      mark("g2", "5 pencils", "underline"), W("l1", "48 − 36 = 12")),
    B("Then one pencil costs half of 12, which is 6 rupees.", W("l2", "12 ÷ 2 = 6")),
    B("Careful: 6 rupees is a pencil. The question asks for a pen. So we go back to the first line.",
      mark("g1", "2 pens", "box")),
    B("In the first line, how much do the 3 pencils cost?",
      ask=choose(["₹18", "₹6", "₹9"], 0,
                 "One pencil is 6 rupees. 3 pencils cost 3 times 6, which is 18 rupees.")),
    B("3 times 6 is 18. Take that from 36: 36 minus 18 is 18. So the 2 pens cost 18 rupees.",
      W("l3", "3 × 6 = 18"), W("l4", "36 − 18 = 18")),
    B("One pen is half of 18. So one pen costs 9 rupees.",
      W("l5", "18 ÷ 2 = 9"), answer("l6", "₹9"), mark("l6", "₹9", "circle")),
    B("Let's check the second line. 2 pens cost 18, and 5 pencils cost 30. 18 plus 30 is 48. It works!",
      W("l7", "5 × 6 = 30"), W("l8", "18 + 30 = 48")),
    B("So when two purchases share something, compare them. The extra items explain the extra cost."),
])

# Between 20 and 40: rows of 4 leave 3, rows of 5 leave 2
LESSONS["G4A_EQUATIONS_027"] = lesson([
    B("A class has between 20 and 40 children. In rows of 4, 3 children are left over. "
      "In rows of 5, 2 are left over. How many children?",
      given("g1", "Between 20 and 40. Rows of 4: 3 over. Rows of 5: 2 over", label=True)),
    B("We have two clues. Let's use the first to make a list. Then we test the list with the second."),
    B("Rows of 4 with 3 left over. Start from a multiple of 4, like 20, and add 3. That gives 23. "
      "Then keep adding 4.", L("l1", "23, 27, 31, 35, 39")),
    B("Now the second clue: rows of 5, with 2 left over. Numbers like that end in which digits?",
      ask=choose(["2 or 7", "0 or 5", "3 or 8"], 0,
                 "Multiples of 5 end in 0 or 5. Add the 2 left over, and the number ends in 2 or 7.")),
    B("So we look in our list for a number that ends in 2 or 7.", mark("l1", "27", "circle")),
    B("Only 27 does. 23 ends in 3, 31 ends in 1, 35 ends in 5 and 39 ends in 9."),
    B("So there are 27 children in the class.",
      answer("l2", "Children = 27", label=True), mark("l2", "27", "circle")),
    B("Let's check. 6 rows of 4, and 3 more, make 27. And 5 rows of 5, and 2 more, also make 27. Both clues fit!",
      W("l3", "6 × 4 + 3 = 27"), W("l4", "5 × 5 + 2 = 27")),
    B("So with two clues, list the numbers that fit one clue. Then keep only the one that fits the other."),
])

# Melons, mangoes and guavas
LESSONS["G4A_EQUATIONS_028"] = lesson([
    B("One melon weighs the same as 2 mangoes and 1 guava. One mango weighs the same as 3 guavas. "
      "How many guavas weigh the same as 2 melons?",
      given("g1", "1 melon = 2 mangoes + 1 guava", label=True), given("g2", "1 mango = 3 guavas", label=True)),
    B("Our plan: change everything into guavas. Then we have only one kind of fruit to count."),
    B("1 mango is 3 guavas. So how many guavas are 2 mangoes?",
      ask=choose(["6", "3", "5"], 0,
                 "Each mango is worth 3 guavas. 2 mangoes are 2 times 3, which is 6 guavas.")),
    B("2 times 3 is 6. So in the melon line, we swap the 2 mangoes for 6 guavas.",
      W("l1", "2 × 3 = 6"), strike("g1", "2 mangoes", "6 guavas")),
    B("Now one melon is 6 guavas, and the 1 guava that was already there. 6 plus 1 is 7.",
      W("l2", "6 + 1 = 7"), L("l3", "1 melon = 7 guavas")),
    B("Careful! Read the question again. How many melons does it ask about?",
      ask=choose(["2 melons", "1 melon"], 0,
                 "The question asks about 2 melons. We have found the guavas for 1 melon, "
                 "so there is one more step.")),
    B("2 melons are 2 times 7 guavas. That is 14 guavas.", answer("l4", "2 × 7 = 14"), mark("l4", "14", "circle")),
    B("So swap one fruit at a time until only one kind is left. "
      "And do not forget the guava that was already on the pan."),
])

# As much greater than 36 as less than 86
LESSONS["G4A_EQUATIONS_029"] = lesson([
    B("A number is as much greater than 36 as it is less than 86. What is the number?",
      given("g1", "As much more than 36 as less than 86", label=True)),
    B("That means the number is the same distance from 36 as from 86. So it sits exactly in the middle.",
      fig("f1", {"kind": "numberLine", "min": 36, "max": 86, "step": 25, "tickLabels": "ends",
                 "points": [{"at": 61, "label": "?"}]})),
    B("First, how far apart are 36 and 86?",
      ask=choose(["50", "122", "25"], 0,
                 "To find how far apart two numbers are, we subtract. 86 minus 36 is 50.")),
    B("86 minus 36 is 50. So the whole gap is 50.", W("l1", "86 − 36 = 50")),
    B("Our number is in the middle, so it is half of the gap away from each end. Half of 50 is 25.",
      W("l2", "50 ÷ 2 = 25")),
    B("Careful: 25 is a distance, not the number. How do we get the number?",
      ask=choose(["36 + 25", "86 + 25", "25 + 25"], 0,
                 "Start at 36 and walk 25 steps up. That lands in the middle. So it is 36 plus 25.")),
    B("36 plus 25 is 61. So the number is 61.", answer("l3", "36 + 25 = 61"), mark("l3", "61", "circle")),
    B("Let's check. 61 minus 36 is 25. And 86 minus 61 is 25. The same distance both ways!",
      W("l4", "61 − 36 = 25"), W("l5", "86 − 61 = 25")),
    B("So for a number halfway between two others, find the gap, halve it, and add it to the smaller one."),
])

# Sum 12, product 35: the difference
LESSONS["G4A_EQUATIONS_030"] = lesson([
    B("Two whole numbers add up to 12. When we multiply them, we get 35. "
      "We must find the difference between them.", given("g1", "Sum = 12, product = 35", label=True)),
    B("First we need the two numbers. Let's list the pairs that multiply to make 35.",
      W("l1", "1 × 35 = 35"), W("l2", "5 × 7 = 35")),
    B("Which pair also adds up to 12?",
      ask=choose(["5 and 7", "1 and 35"], 0,
                 "1 plus 35 is far more than 12. But 5 plus 7 is 12. So the numbers are 5 and 7.")),
    B("5 plus 7 is 12. So the two numbers are 5 and 7.", W("l3", "5 + 7 = 12")),
    B("Now read the question again. What does it ask for?",
      ask=choose(["the difference: 7 − 5", "the bigger number: 7", "the smaller number: 5"], 0,
                 "The question does not ask for either number. It asks for the difference, "
                 "which means we subtract.")),
    B("7 minus 5 is 2. So the difference is 2.", answer("l4", "7 − 5 = 2"), mark("l4", "2", "circle")),
    B("So find the pair first, by testing. Then do exactly what the question asks."),
])

# Packs of 4 and 7: exactly 30 pencils
LESSONS["G4A_EQUATIONS_031"] = lesson([
    B("A shop sells pencils in packs of 4 and packs of 7. Meena buys exactly 30 pencils. "
      "How many packs does she buy altogether?", given("g1", "Packs of 4 and packs of 7: 30 pencils", label=True)),
    B("Let's test the packs of 7, one at a time. Whatever is left must be made from packs of 4."),
    B("1 pack of 7 leaves 23. But 23 is not in the 4 times table. So that does not work.", W("l1", "30 − 7 = 23")),
    B("Try 2 packs of 7. That is 14 pencils. How many are left?",
      W("l2", "2 × 7 = 14"),
      ask=choose(["16", "23", "14"], 0, "2 packs of 7 hold 14 pencils. And 30 minus 14 is 16.")),
    B("30 minus 14 is 16. And 16 is in the 4 times table! 4 times 4 is 16.",
      W("l3", "30 − 14 = 16"), W("l4", "4 × 4 = 16")),
    B("So she buys 2 packs of 7 and 4 packs of 4.", L("l5", "2 packs of 7 + 4 packs of 4")),
    B("The question asks for all the packs. How many is that?",
      ask=choose(["6", "4", "2"], 0,
                 "She buys 2 packs of one kind and 4 of the other. 2 plus 4 is 6 packs altogether.")),
    B("2 plus 4 is 6. Meena buys 6 packs altogether.", answer("l6", "2 + 4 = 6"), mark("l6", "6", "circle")),
    B("Let's check. 14 pencils and 16 pencils make 30. And no other way works: "
      "3 packs of 7 leave 9, and 4 packs of 7 leave 2.", W("l7", "14 + 16 = 30")),
    B("So test one kind of pack at a time, and see whether the rest fits the other kind."),
])

# Divided by 8: quotient 9, greatest remainder. Remainder on dividing by 5?
LESSONS["G4A_EQUATIONS_032"] = lesson([
    B("A number is divided by 8. The quotient is 9, and the remainder is the greatest it can be. "
      "What is the remainder when the same number is divided by 5?",
      given("g1", "Number ÷ 8: quotient 9, greatest remainder", label=True)),
    B("When we divide by 8, what is the greatest remainder we can have?",
      ask=choose(["7", "8", "9"], 0,
                 "A remainder is always smaller than the number we divide by. If 8 were left over, "
                 "we could make one more group of 8. So the greatest is 7.")),
    B("The remainder must be smaller than 8. So the greatest remainder is 7.", L("l1", "Remainder = 7")),
    B("Now we build the number. 8 groups of 9, and 7 left over. 8 times 9 is 72, and 72 plus 7 is 79.",
      W("l2", "8 × 9 = 72"), W("l3", "72 + 7 = 79")),
    B("So the number is 79. Now we divide 79 by 5.", W("l4", "79 ÷ 5 = ?")),
    B("Which multiple of 5 is just below 79?",
      ask=choose(["75", "70", "80"], 0,
                 "Multiples of 5 end in 0 or 5. 80 is too big, so the one just below 79 is 75.")),
    B("5 times 15 is 75. And 79 is 4 more than 75. So the remainder is 4.",
      W("l5", "5 × 15 = 75"), answer("l6", "79 − 75 = 4"), mark("l6", "4", "circle")),
    B("Remember: a remainder is always smaller than the divisor. Build the number first, then divide again."),
])

# Sunita 30, Pari 6: when is Sunita 3 times as old?
LESSONS["G4A_EQUATIONS_033"] = lesson([
    B("Sunita is 30 and her daughter Pari is 6. In how many years will Sunita be exactly 3 times as old as Pari?",
      given("g1", "Sunita 30 years, Pari 6 years", label=True)),
    B("Here is the secret. Every year both of them get 1 year older. "
      "So the gap between their ages never changes."),
    B("The gap is 30 minus 6, which is 24 years. Now and always.", W("l1", "30 − 6 = 24")),
    B("When Sunita is 3 times as old, Pari's age is 1 share and Sunita's is 3 shares. The gap is 2 shares.",
      bars("f1", ("Pari", [(3, "1 share", "a")]), ("Sunita", [(3, "1 share", "b")] * 3))),
    B("The gap is 2 shares, and the gap is 24 years. So what is 1 share?",
      ask=choose(["12 years", "8 years", "24 years"], 0,
                 "2 shares make 24 years. So 1 share is half of 24, which is 12.")),
    B("Half of 24 is 12. So Pari will be 12 when it happens.", W("l2", "24 ÷ 2 = 12")),
    B("Careful: 12 is Pari's age then. The question asks in how many years. Pari is 6 now. So?",
      ask=choose(["12 − 6 = 6 years", "12 years", "12 + 6 = 18 years"], 0,
                 "Pari is 6 now and will be 12 then. From 6 to 12 is 6 years.")),
    B("12 minus 6 is 6. So it happens in 6 years.",
      W("l3", "12 − 6 = 6"), answer("l4", "In 6 years", label=True), mark("l4", "6 years", "circle")),
    B("Let's check. In 6 years Sunita is 36 and Pari is 12. And 3 times 12 is 36. It works!",
      W("l5", "30 + 6 = 36"), W("l6", "3 × 12 = 36")),
    B("So in age puzzles, the gap between two people never changes. Use the gap to find the shares."),
])

# The snail in the well
LESSONS["G4A_EQUATIONS_034"] = lesson([
    B("A snail is at the bottom of a well 10 metres deep. Each day it climbs 3 metres. "
      "Each night it slips back 2 metres. On which day does it reach the top?",
      given("g1", "Well 10 m deep. Day: up 3 m. Night: down 2 m", label=True)),
    B("After one full day and one night, how much higher is the snail?",
      ask=choose(["1 metre", "3 metres", "5 metres"], 0,
                 "It climbs 3 metres, then slips back 2. 3 take away 2 is 1. So it gains just 1 metre.")),
    B("So each full day and night, the snail gains 1 metre.", W("l1", "3 − 2 = 1")),
    B("Now the trap. It is tempting to say: 1 metre a day, 10 metres, so 10 days. But think about the last day."),
    B("On its last day the snail climbs 3 metres and is out. It does not slip back, "
      "because it has already reached the top!"),
    B("So from what height can the snail reach the top in one day's climb?",
      ask=choose(["7 metres", "9 metres", "10 metres"], 0,
                 "One day's climb is 3 metres, and the top is at 10 metres. 10 minus 3 is 7. "
                 "So from 7 metres, one climb gets it out.")),
    B("10 minus 3 is 7. The snail needs to start a day at 7 metres.", W("l2", "10 − 3 = 7")),
    B("It gains 1 metre each day and night. So after 7 days and nights, it starts the next morning at 7 metres.",
      fig("f1", {"kind": "numberLine", "min": 0, "max": 10, "step": 1,
                 "hops": [{"from": 7, "to": 10, "label": "day 8"}]})),
    B("The next day is day 8. It climbs from 7 metres to 10 metres, and it is out!",
      W("l3", "7 + 3 = 10"), answer("l4", "The 8th day", label=True), mark("l4", "8th", "circle")),
    B("So in climbing puzzles, treat the last day on its own. On the last day there is no slipping back."),
])
