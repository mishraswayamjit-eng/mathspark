"""gr4_squares, written per question: G4A_SQUARES_013 to 024."""
from g4_gr4_numbers_lib import A, C, FIG, G, Q, U, W, X, b, dots

L = {}

L["G4A_SQUARES_013"] = [
    b("We count the perfect squares that lie between 50 and 150.", G("How many perfect squares between 50 and 150?")),
    b("Find where to start. 7 times 7 is 49, just below 50. So the first square inside is 8 times 8, which is 64.",
      W("7 × 7 = 49:  too small"), W("8 × 8 = 64")),
    b("Carry on. 9 times 9 is 81, 10 times 10 is 100, 11 times 11 is 121 and 12 times 12 is 144.", 
      W("9 × 9 = 81"), W("10 × 10 = 100"), W("11 × 11 = 121"), W("12 × 12 = 144")),
    b("13 times 13 is 169. Does that one count?",
      W("13 × 13 = 169"),
      Q(["No, it is more than 150", "Yes, it counts"], "169 is bigger than 150, so it is outside our range. We stop at 144.")),
    b("So the squares are 64, 81, 100, 121 and 144.", W("64, 81, 100, 121, 144")),
    b("Count them. There are 5 perfect squares.", A("5")),
    b("Careful at both ends. 49 is just outside, and so is 169. Always check the edges."),
]

L["G4A_SQUARES_014"] = [
    b("One of these digits can never be the last digit of a perfect square. Let us find out which.",
      G("Which digit is never the last digit of a perfect square?"), W("4     7     5     6", name="o")),
    b("The last digit of a square depends only on the last digit of the number. So we just square the digits 0 to 9."),
    b("The squares are 0, 1, 4, 9, 16, 25, 36, 49, 64 and 81.", W("0, 1, 4, 9, 16, 25, 36, 49, 64, 81")),
    b("Their last digits are 0, 1, 4, 9, 6, 5, 6, 9, 4 and 1.", W("last digits:   0, 1, 4, 9, 6, 5, 6, 9, 4, 1")),
    b("Which of our 4 digits is missing from that list?",
      Q(["7", "4", "6"],
        "4 is there, from 2 times 2. 5 is there, from 5 times 5. 6 is there, from 4 times 4. But 7 never appears.")),
    b("7 never shows up. So no perfect square ends in 7.", C("7", on="o"), A("7")),
    b("In fact squares only ever end in 0, 1, 4, 5, 6 or 9. Never in 2, 3, 7 or 8. A handy fact for spotting squares!"),
]

L["G4A_SQUARES_015"] = [
    b("10 squared, take away 6 squared. We square each number first.", G("10² − 6² = ?", name="g")),
    b("10 squared is 10 times 10, which is 100.", U("10²", on="g"), W("10² = 100")),
    b("And what is 6 squared?",
      Q(["36", "12", "26"], "6 squared is 6 times 6, which is 36. 6 times 2 would be only 12.")),
    b("6 squared is 36.", U("6²", on="g"), W("6² = 36")),
    b("Now subtract. 100 minus 36 is 64.", W("100 − 36 = 64"), A("64")),
    b("Careful: do not subtract first. 10 minus 6 is 4, and 4 squared is only 16.", W("(10 − 6)² = 16")),
    b("So: squares first, then the take away."),
]

L["G4A_SQUARES_016"] = [
    b("We add up these 6 odd numbers, and then ask which number the total is the square of.",
      G("1 + 3 + 5 + 7 + 9 + 11 is the square of ?")),
    b("A neat way to add: pair the ends. 1 and 11 make 12. 3 and 9 make 12. 5 and 7 make 12.",
      W("1 + 11 = 12"), W("3 + 9 = 12"), W("5 + 7 = 12")),
    b("3 lots of 12 make 36.", W("3 × 12 = 36")),
    b("The total is 36. Which number, times itself, makes 36?",
      Q(["6", "36", "11"], "6 times 6 is 36. The question asks for the number that is squared, not for the total.")),
    b("6 times 6 is 36. So the sum is the square of 6.", W("6 × 6 = 36"), A("6")),
    b("Here is the pretty part. We added 6 odd numbers, and got 6 times 6. That always works!",
      FIG(dots(6, 6, note="6 odd numbers build a 6 by 6 square"))),
    b("Try it: 1 plus 3 is 4, which is 2 times 2. And 1 plus 3 plus 5 is 9, which is 3 times 3.",
      W("1 + 3 = 4"), W("1 + 3 + 5 = 9")),
]

L["G4A_SQUARES_017"] = [
    b("The teacher makes the biggest square she can from 150 children. Some will not fit. How many?",
      G("150 children, biggest possible square. Left out = ?")),
    b("A square has the same number in every row and column. So the number she uses is a perfect square, as big as possible, but not more than 150."),
    b("12 times 12 is 144. And 13 times 13 is 169.", W("12 × 12 = 144"), W("13 × 13 = 169")),
    b("Which square can the teacher make with 150 children?",
      Q(["12 by 12", "13 by 13"],
        "13 by 13 needs 169 children, but there are only 150. So the biggest square she can make is 12 by 12.")),
    b("169 is too many. So the biggest square uses 144 children.", FIG(dots(12, 12, note="12 rows of 12 = 144"))),
    b("The rest are left out. 150 minus 144 is 6.", W("150 − 144 = 6"), A("6")),
    b("Careful: 12 is the number in each row, not the number left out. And 19 is how many more she would need for the next square.",
      W("169 − 150 = 19")),
]

L["G4A_SQUARES_018"] = [
    b("The gardener wants to plant all 200 roses in a square. He may need to buy a few more. How many, at least?",
      G("200 plants, all in a square. Extra plants needed = ?")),
    b("He wants to use every plant, so the square must hold at least 200. We need the first perfect square that is 200 or more."),
    b("14 times 14 is 196. Can a 14 by 14 square hold all 200 plants?",
      W("14 × 14 = 196"),
      Q(["No, 196 is less than 200", "Yes, it is close enough"],
        "196 is 4 short of 200. So 4 plants would be left over, and he wants to plant them all.")),
    b("196 is too small. This is the trap: we must go up to the next square, not down."),
    b("15 times 15 is 225. That holds them all.", W("15 × 15 = 225")),
    b("He has 200 and needs 225. 225 minus 200 is 25. So he buys 25 more.", W("225 − 200 = 25"), A("25")),
    b("Careful: 4 is how many would be left over from the smaller square. And 15 is the number in each row, not the number to buy.",
      W("200 − 196 = 4")),
]

L["G4A_SQUARES_019"] = [
    b("The square root of 400, added to the square root of 49. We find each root first, and then add.",
      G("√400 + √49 = ?")),
    b("The square root of 400 is the number that, times itself, makes 400. Which is it?",
      Q(["20", "200", "40"],
        "20 times 20 is 400, because 2 times 2 is 4, with 2 zeros. 200 is only half of 400, and a square root is not a half.")),
    b("20 times 20 is 400. So the square root of 400 is 20.", W("20 × 20 = 400"), W("√400 = 20")),
    b("7 times 7 is 49. So the square root of 49 is 7.", W("7 × 7 = 49"), W("√49 = 7")),
    b("Now add. 20 plus 7 is 27.", W("20 + 7 = 27"), A("27")),
    b("Careful: do not add first. 400 plus 49 is 449, and that is not what the question asks.", W("400 + 49 = 449")),
    b("So: find each square root on its own, then add."),
]

L["G4A_SQUARES_020"] = [
    b("441 soldiers stand in a square, and every soldier in the front row holds a flag. How many flags?",
      G("441 soldiers in a square. Flags in the front row = ?")),
    b("We need the number of soldiers in one row. That number, times itself, is 441.", W("? × ? = 441")),
    b("Try 20. 20 times 20 is 400. A bit too small.", W("20 × 20 = 400")),
    b("400 is too small. Here is a clue: 441 ends in 1. Which number should we try next?",
      Q(["21", "25", "30"],
        "We need just a little more than 20. And 21 ends in 1, so its square ends in 1 too, like 441.")),
    b("21 times 21: 21 times 20 is 420, and one more 21 makes 441.", W("21 × 20 = 420"), W("420 + 21 = 441")),
    b("So each row has 21 soldiers, and the front row holds 21 flags.", W("21 × 21 = 441"), A("21")),
    b("Careful: only the front row holds flags. Not all four sides, and not all 441 soldiers."),
]

L["G4A_SQUARES_021"] = [
    b("Three of these are perfect squares, and one is not. We want the one that is not.",
      G("Which is NOT a perfect square?"), W("164     121     144     196", name="o")),
    b("List the squares just above 10 times 10. 11 times 11 is 121. 12 times 12 is 144.",
      W("11 × 11 = 121"), W("12 × 12 = 144")),
    b("13 times 13 is 169. 14 times 14 is 196.", W("13 × 13 = 169"), W("14 × 14 = 196")),
    b("Which of our numbers is missing from the list 121, 144, 169, 196?",
      Q(["164", "144", "196"], "121, 144 and 196 are all in the list of squares. 164 is not there.")),
    b("164 is not in the list. It sits between 144 and 169, so it is not a perfect square.",
      W("144 < 164 < 169"), C("164", on="o"), A("164")),
    b("Careful: 164 looks a lot like 169 and 144. Looking like a square is not enough. Check against the tables."),
]

L["G4A_SQUARES_022"] = [
    b("Two numbers come one after the other. Their squares are 144 and 169. We want the sum of the two numbers.",
      G("Squares are 144 and 169. Sum of the two numbers = ?")),
    b("144 is the square of which number?",
      Q(["12", "72", "14"], "12 times 12 is 144. 72 is half of 144, and a square root is not a half.")),
    b("12 times 12 is 144. So the first number is 12.", W("12 × 12 = 144")),
    b("The numbers come one after the other, so the second should be 13. Check: 13 times 13 is 169. Yes!",
      W("13 × 13 = 169")),
    b("Now add the two numbers. 12 plus 13 is 25.", W("12 + 13 = 25"), A("25")),
    b("Careful: the question asks for the sum of the numbers, not of their squares. 144 plus 169 is 313, a very different answer.",
      W("144 + 169 = 313")),
]

L["G4A_SQUARES_023"] = [
    b("Only one of these 4 numbers is a perfect square. We can find it without any long multiplying, just from the last digits.",
      G("Only one is a perfect square. Use the last digits."), W("1232     1443     1521     1687", name="o")),
    b("Remember how squares end. Square the digits 0 to 9, and the last digits are only ever 0, 1, 4, 5, 6 or 9.",
      W("squares end in:   0, 1, 4, 5, 6 or 9")),
    b("So which endings are impossible for a perfect square?",
      Q(["2, 3, 7 and 8", "1, 4 and 9", "5 and 6"],
        "Squares can end in 0, 1, 4, 5, 6 or 9. The digits left over are 2, 3, 7 and 8, and no square ends in those.")),
    b("1232 ends in 2. 1443 ends in 3. 1687 ends in 7. All three are ruled out.",
      X("1232", on="o"), X("1443", on="o"), X("1687", on="o")),
    b("Only 1521 is left. It ends in 1, which is fine.", C("1521", on="o")),
    b("And indeed, 39 times 39 is 1521.", W("39 × 39 = 1521"), A("1521")),
    b("Careful: a good ending does not prove a number is a square. But a bad ending proves it is not. That was enough here."),
]

L["G4A_SQUARES_024"] = [
    b("4 squares to add. We square each number first, and then add them up.", G("1² + 2² + 3² + 4² = ?")),
    b("1 times 1 is 1. And 2 times 2 is 4.", W("1² = 1"), W("2² = 4")),
    b("What is 3 squared?",
      Q(["9", "6", "33"], "3 squared is 3 times 3, which is 9. 3 times 2 would be 6, but squaring is times itself.")),
    b("3 times 3 is 9. And 4 times 4 is 16.", W("3² = 9"), W("4² = 16")),
    b("Now add the squares. 1 plus 4 plus 9 plus 16 is 30.", W("1 + 4 + 9 + 16 = 30"), A("30")),
    b("Careful: adding first gives 1 plus 2 plus 3 plus 4, which is 10, and 10 squared is 100. Not the same thing at all.",
      W("(1 + 2 + 3 + 4)² = 100")),
]
