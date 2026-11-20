"""gr4_squares, written per question: G4A_SQUARES_001 to 012."""
from g4_gr4_numbers_lib import A, C, FIG, G, Q, U, W, b, dots, nline

L = {}

L["G4A_SQUARES_001"] = [
    b("The square of 12 means 12 multiplied by itself.", G("The square of 12 = ?"), FIG(dots(12, 12, note="12 rows of 12"))),
    b("Which sum gives the square of 12?",
      Q(["12 × 12", "12 × 2", "12 + 12"], "Squaring means the number times itself. So it is 12 times 12, not 12 times 2.")),
    b("12 times 12 is easier in two parts. Split one 12 into 10 and 2.", W("12 × 12 = 12 × 10 + 12 × 2")),
    b("12 times 10 is 120. And 12 times 2 is 24.", W("12 × 10 = 120"), W("12 × 2 = 24")),
    b("120 plus 24 is 144. So the square of 12 is 144.", W("120 + 24 = 144"), A("144")),
    b("Careful: 10 times 10 plus 2 times 2 is only 104. That leaves out part of the square.", W("10 × 10 + 2 × 2 = 104")),
    b("So remember: the square of a number is the number times itself."),
]

L["G4A_SQUARES_002"] = [
    b("A perfect square is a number times itself, like 3 times 3. One of these 4 numbers is a perfect square.",
      G("Which is a perfect square?"), W("48     64     56     72", name="o")),
    b("List the squares near these numbers. 6 times 6 is 36. 7 times 7 is 49. 8 times 8 is 64. 9 times 9 is 81.",
      W("6 × 6 = 36"), W("7 × 7 = 49"), W("8 × 8 = 64"), W("9 × 9 = 81")),
    b("Which of our numbers is in that list of squares?",
      Q(["64", "48", "56"], "Look down the list of squares: 36, 49, 64, 81. Only 64 is one of our numbers.")),
    b("64 is 8 times 8. So 64 is the perfect square.", C("64", on="o"), A("64")),
    b("Careful: 48, 56 and 72 are in the times tables too. But 48 is 6 times 8, and 56 is 7 times 8. Two different numbers.",
      W("48 = 6 × 8"), W("56 = 7 × 8"), W("72 = 8 × 9")),
    b("A perfect square needs the same number twice."),
]

L["G4A_SQUARES_003"] = [
    b("The board has 81 small squares, with as many rows as columns. How many squares are in each row?",
      G("81 small squares, equal rows and columns. Each row = ?")),
    b("Rows and columns are equal. So the number in a row, times what, makes 81?",
      Q(["times itself", "times 2", "times 3"],
        "There are as many rows as squares in a row. So we multiply the number by itself to get 81.")),
    b("We need a number that, times itself, makes 81.", W("? × ? = 81")),
    b("Try 8. 8 times 8 is 64. Too small.", W("8 × 8 = 64")),
    b("Try 9. 9 times 9 is 81. That fits! So each row has 9 small squares.",
      W("9 × 9 = 81"), FIG(dots(9, 9, note="9 rows of 9")), A("9")),
    b("Careful: do not divide 81 by 3, and do not halve it. The board is square, so both numbers must be the same."),
]

L["G4A_SQUARES_004"] = [
    b("We know only one thing about a number: it ends in 7. Can we still tell how its square ends?",
      G("A number ends in 7. Its square ends in ?")),
    b("Test with the simplest such number, 7 itself. 7 times 7 is 49, which ends in 9.", W("7 × 7 = 49")),
    b("Will a bigger number that ends in 7, like 17, also have a square ending in 9?",
      W("try 17"),
      Q(["Yes, only the last digits matter", "No, it could end in anything"],
        "When we multiply, the last digit of the answer comes only from the last digits of the two numbers. Here that is 7 times 7.")),
    b("17 times 17: 17 times 10 is 170 and 17 times 7 is 119. Together, 289. It ends in 9 again!",
      W("17 × 10 = 170"), W("17 × 7 = 119"), W("17 × 17 = 289")),
    b("The last digit of a product comes only from the last digits. And 7 times 7 always ends in 9.", A("9")),
    b("Careful: the last digit does not just stay 7. And 7 plus 7 is 14, but squaring is multiplying, not adding.",
      W("7 + 7 = 14:  adding, not squaring")),
]

L["G4A_SQUARES_005"] = [
    b("49 is a perfect square, and we want the very next one after it.", G("Next perfect square after 49 = ?")),
    b("49 is which number times itself?",
      Q(["7 × 7", "6 × 6", "9 × 9"], "7 times 7 is 49. So 49 is the square of 7.")),
    b("49 is 7 times 7.", W("7 × 7 = 49")),
    b("The next square comes from the next counting number, which is 8.", W("8 × 8 = 64")),
    b("8 times 8 is 64. So the next perfect square is 64.", A("64")),
    b("Careful: 56 is 7 times 8. For the next square, both numbers must go up to 8.", W("7 × 8 = 56:  not a square")),
    b("The squares go 49, 64, then 81. There is no perfect square in between.", W("9 × 9 = 81")),
]

L["G4A_SQUARES_006"] = [
    b("Ravi plants 11 rows of saplings, with 11 saplings in each row. How many saplings is that?",
      G("11 rows of 11 saplings. How many?"), FIG(dots(11, 11, note="11 rows of 11"))),
    b("Which sum counts all the saplings?",
      Q(["11 × 11", "11 + 11", "11 × 4"],
        "Each row has 11, and there are 11 rows. So we add 11, eleven times over. That is 11 times 11.")),
    b("11 times 11. Start with 11 times 10, which is 110.", W("11 × 10 = 110")),
    b("Then one more 11. 110 plus 11 is 121.", W("110 + 11 = 121")),
    b("So Ravi plants 121 saplings.", W("11 × 11 = 121"), A("121")),
    b("Careful: 22 is only 11 plus 11, which is just 2 rows. And 44 counts along the 4 sides. The saplings fill the whole field.",
      W("11 + 11 = 22"), W("11 × 4 = 44")),
]

L["G4A_SQUARES_007"] = [
    b("5 squared plus 3 squared. The little 2 tells us to square each number.", G("5² + 3² = ?", name="g")),
    b("What does 5 squared mean?",
      Q(["5 × 5", "5 × 2", "5 + 2"],
        "The little 2 means: use the number twice in a multiplication. So 5 squared is 5 times 5.")),
    b("5 squared is 5 times 5, which is 25.", U("5²", on="g"), W("5² = 5 × 5 = 25")),
    b("3 squared is 3 times 3, which is 9.", U("3²", on="g"), W("3² = 3 × 3 = 9")),
    b("Now add the two squares. 25 plus 9 is 34.", W("25 + 9 = 34"), A("34")),
    b("Careful: do not add first. 5 plus 3 is 8, and 8 squared is 64. That is a different sum.", W("(5 + 3)² = 64")),
    b("So: square each number on its own, then add."),
]

L["G4A_SQUARES_008"] = [
    b("The square of 30 is 30 times 30.", G("The square of 30 = ?")),
    b("Here is a trick for numbers that end in zero. First forget the zeros: 3 times 3 is 9.", W("3 × 3 = 9")),
    b("Now put the zeros back. Each 30 has one zero. How many zeros go on the answer?",
      Q(["2 zeros", "1 zero", "3 zeros"], "One zero comes from the first 30 and one from the second 30. That makes 2 zeros.")),
    b("One zero from each 30 makes 2 zeros. So we write 9, and then 2 zeros. That is 900.", W("30 × 30 = 900"), A("900")),
    b("Check: 30 times 10 is 300, and 3 lots of 300 make 900.", W("30 × 10 = 300"), W("3 × 300 = 900")),
    b("Careful: 60 is 30 plus 30. And 90 has only one zero. The square needs both zeros.",
      W("30 + 30 = 60"), W("90: one zero is missing")),
]

L["G4A_SQUARES_009"] = [
    b("We want the biggest perfect square that still has only two digits.", G("Greatest two-digit perfect square = ?")),
    b("The greatest two-digit number is 99. So we want the biggest square that is not more than 99.",
      W("greatest two-digit number: 99")),
    b("10 times 10 is 100. Is that a two-digit number?",
      W("10 × 10 = 100"),
      Q(["No, it has 3 digits", "Yes, it has 2 digits"], "100 has 3 digits: 1, 0 and 0. So it is too big for us.")),
    b("100 is too big. Step back one: 9 times 9 is 81.", W("9 × 9 = 81")),
    b("81 has two digits. So 81 is the greatest two-digit perfect square.", A("81")),
    b("Careful: 99 is the greatest two-digit number, but no whole number times itself makes 99. It lies between 81 and 100.",
      W("81 < 99 < 100")),
]

L["G4A_SQUARES_010"] = [
    b("We take away as little as we can from 30, and we must be left with a perfect square.",
      G("30 − ? = a perfect square  (smallest ?)"), FIG(nline(20, 40, 1, [(30, "30")], note="Find the nearest square below 30"))),
    b("We are taking away, so the square we want is below 30. And for the smallest take away, it should be as near to 30 as possible."),
    b("5 times 5 is 25 and 6 times 6 is 36. Which of these can we reach by taking away from 30?",
      W("5 × 5 = 25"), W("6 × 6 = 36"),
      Q(["25", "36"], "36 is more than 30. We are taking away, so we need the square that is less than 30, which is 25.")),
    b("25 is the nearest square below 30.", FIG(nline(20, 40, 1, [(25, "25"), (30, "30")], hops=[(30, 25, "−5")]))),
    b("30 minus 25 is 5. So we take away 5.", W("30 − 25 = 5"), A("5")),
    b("Careful: 6 is what you would add to reach 36. And taking away 14 or 21 also leaves a square, but they are not the smallest.",
      W("30 − 14 = 16"), W("30 − 21 = 9")),
    b("So: the smallest take away leads to the nearest square below."),
]

L["G4A_SQUARES_011"] = [
    b("All 4 of these are perfect squares. We want the one that is the square of an odd number.",
      G("Which is the square of an odd number?"), W("36     64     49     100", name="o")),
    b("Find what each one is the square of. 36 is 6 times 6. 64 is 8 times 8. 100 is 10 times 10.",
      W("36 = 6 × 6"), W("64 = 8 × 8"), W("100 = 10 × 10")),
    b("6, 8 and 10 are all even. So those three are squares of even numbers."),
    b("49 is 7 times 7. Is 7 odd or even?",
      W("49 = 7 × 7"),
      Q(["odd", "even"], "Even numbers end in 0, 2, 4, 6 or 8. 7 is not one of those, so 7 is odd.")),
    b("7 is odd. So 49 is the square of an odd number.", C("49", on="o"), A("49")),
    b("A shortcut: odd times odd is always odd. So the square of an odd number must be odd, and 49 is the only odd number here."),
]

L["G4A_SQUARES_012"] = [
    b("Two steps here: find the square of 6, and then compare it with 6 itself.", G("(square of 6) − 6 = ?")),
    b("First, the square of 6. What is it?",
      Q(["36", "12", "66"], "The square of 6 is 6 times 6, which is 36. 6 times 2 would only be 12.")),
    b("6 times 6 is 36.", W("6 × 6 = 36"), FIG(dots(6, 6, note="6 rows of 6"))),
    b("Difference means subtract. So take the number 6 away from its square. 36 minus 6 is 30.", W("36 − 6 = 30"), A("30")),
    b("Picture it: from 6 rows of 6, take away one row. 5 rows of 6 are left, and that is 30.", W("5 × 6 = 30")),
    b("Careful: 36 is only the square. The question has one more step. And difference never means add."),
]
