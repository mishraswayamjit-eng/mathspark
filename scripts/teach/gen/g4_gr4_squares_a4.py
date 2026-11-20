"""gr4_squares, written per question: G4A_SQUARES_025 to 036."""
from g4_gr4_numbers_lib import A, C, FIG, G, Q, W, X, b, dots

L = {}

L["G4A_SQUARES_025"] = [
    b("Tara has a square made of 64 tiles. She wants to grow it into the next bigger square. How many more tiles?",
      G("64 tiles in a square. Tiles for the next bigger square?"), FIG(dots(8, 8, note="64 tiles: 8 rows of 8"))),
    b("64 tiles make a square. How many tiles are along each side?",
      Q(["8", "16", "32"], "We need a number that, times itself, makes 64. 8 times 8 is 64, so each side has 8 tiles.")),
    b("8 times 8 is 64. So her square is 8 by 8.", W("8 × 8 = 64")),
    b("The next bigger square is 9 by 9. And 9 times 9 is 81.",
      W("9 × 9 = 81"), FIG(dots(9, 9, note="The next square: 9 rows of 9"))),
    b("She has 64 and needs 81. 81 minus 64 is 17.", W("81 − 64 = 17"), A("17")),
    b("See where the 17 tiles go: one new row of 8, one new column of 8, and 1 tile in the corner.", W("8 + 8 + 1 = 17")),
    b("That corner tile is the trap. Forget it, and you get 16.", W("8 + 8 = 16:  the corner is missing")),
]

L["G4A_SQUARES_026"] = [
    b("A number, squared, makes 225. We take the number that is 1 more, and square that instead.",
      G("A number squared is 225. (The number + 1) squared = ?")),
    b("Which number, times itself, makes 225? A clue: 10 times 10 is 100 and 20 times 20 is 400.",
      W("10 × 10 = 100"), W("20 × 20 = 400"),
      Q(["15", "25", "112"],
        "225 is between 100 and 400, so the number is between 10 and 20. And 225 ends in 5, so the number ends in 5. That is 15.")),
    b("15 times 15 is 225. So the number is 15.", W("15 × 15 = 225")),
    b("One more than 15 is 16.", W("15 + 1 = 16")),
    b("16 times 16: 16 times 10 is 160, and 16 times 6 is 96. Together, 256.",
      W("16 × 10 = 160"), W("16 × 6 = 96"), W("16 × 16 = 256"), A("256")),
    b("Careful: add 1 to the number, not to its square. 225 plus 1 is 226, and that is not a square at all.",
      W("225 + 1 = 226:  not a square")),
    b("So: go back to the number, change it, and then square again."),
]

L["G4A_SQUARES_027"] = [
    b("We count every perfect square from 1 to 100, with both ends included.", G("How many perfect squares from 1 to 100?")),
    b("The first one is 1 times 1, which is 1. Yes, 1 is a perfect square!", W("1 × 1 = 1")),
    b("And the last one? Which number, times itself, makes exactly 100?",
      Q(["10", "50", "9"], "10 times 10 is 100. So 100 is itself a perfect square, the square of 10.")),
    b("10 times 10 is 100. So the squares run from the square of 1 up to the square of 10.", W("10 × 10 = 100")),
    b("Here they all are.", W("1, 4, 9, 16, 25, 36, 49, 64, 81, 100")),
    b("Each number from 1 to 10 gives one square. So there are 10 of them.", A("10")),
    b("Careful: both ends count here, 1 and 100. Miss one and you get 9. And 11 times 11 is 121, which is too big.",
      W("11 × 11 = 121:  too big")),
]

L["G4A_SQUARES_028"] = [
    b("51 squared, take away 49 squared. Big numbers, but there is a neat way in.", G("51² − 49² = ?")),
    b("Start with 51 times 50, which is 2550.", W("51 × 50 = 2550")),
    b("51 times 51 is one more 51 than that. 2550 plus 51 is 2601.", W("51² = 2550 + 51 = 2601")),
    b("Now 49 times 49. 49 times 50 is 2450. Is 49 times 49 more or less than that?",
      W("49 × 50 = 2450"),
      Q(["less, by one 49", "more, by one 49"], "49 times 49 has one 49 fewer than 49 times 50. So we take 49 away.")),
    b("2450 minus 49 is 2401.", W("49² = 2450 − 49 = 2401")),
    b("Now subtract the squares. 2601 minus 2401 is 200.", W("2601 − 2401 = 200"), A("200")),
    b("The trap: 51 minus 49 is 2, and 2 squared is 4. But we must square first, and only then subtract.",
      W("(51 − 49)² = 4")),
    b("A shortcut to enjoy: add the two numbers to get 100, and multiply by their difference, 2. That gives 200 as well.",
      W("51 + 49 = 100"), W("100 × 2 = 200")),
]

L["G4A_SQUARES_029"] = [
    b("We divide 48 by something, and the result must be a perfect square. We want the smallest number that works.",
      G("48 ÷ ? = a perfect square  (smallest ?)")),
    b("Smallest means we test small numbers in order. Dividing by 1 leaves 48, which is not a square.", W("48 ÷ 1 = 48")),
    b("Divide by 2 and we get 24. Is 24 a square? 4 times 4 is 16 and 5 times 5 is 25. So no.",
      W("48 ÷ 2 = 24"), W("4 × 4 = 16"), W("5 × 5 = 25")),
    b("Now divide by 3. What is 48 divided by 3?",
      Q(["16", "18", "12"], "3 times 16 is 48. So 48 divided by 3 is 16.")),
    b("48 divided by 3 is 16. And 16 is 4 times 4. A perfect square!", W("48 ÷ 3 = 16")),
    b("So the smallest number to divide by is 3.", A("3")),
    b("Careful: dividing by 12 gives 4, which is a square too. But 12 is not the smallest. That is why we test in order.",
      W("48 ÷ 12 = 4")),
]

L["G4A_SQUARES_030"] = [
    b("We subtract as little as we can from 1000, and we must land on a perfect square.",
      G("1000 − ? = a perfect square  (smallest ?)")),
    b("We need the biggest perfect square below 1000. 30 times 30 is 900. So try the numbers just above 30.",
      W("30 × 30 = 900")),
    b("31 times 31: 31 times 30 is 930, and one more 31 makes 961.", W("31 × 30 = 930"), W("31 × 31 = 961")),
    b("32 times 32 is 1024. Can we use that one?",
      W("32 × 32 = 1024"),
      Q(["No, it is more than 1000", "Yes, it is closer to 1000"],
        "We are subtracting from 1000, so the square must be less than 1000. 1024 is above it.")),
    b("1024 is above 1000. This is the trap: it is nearer, but we cannot reach it by taking away. So our square is 961."),
    b("1000 minus 961 is 39.", W("1000 − 961 = 39"), A("39")),
    b("Check: 1000 minus 39 is 961, which is 31 times 31.", W("1000 − 39 = 961")),
    b("Careful: 31 is the number we squared, not the number to subtract."),
]

L["G4A_SQUARES_031"] = [
    b("We count the whole numbers that lie between 15 squared and 16 squared.",
      G("How many whole numbers between 15² and 16²?")),
    b("First work out the two squares. 15 times 15 is 225, and 16 times 16 is 256.", W("15² = 225"), W("16² = 256")),
    b("The numbers between them start at 226 and end at 255.", W("226, 227, ... , 254, 255")),
    b("256 minus 225 is 31. Is that the number of whole numbers in between?",
      W("256 − 225 = 31"),
      Q(["No, it is one fewer", "Yes, 31"],
        "The gap of 31 counts every step from 225 up to 256, and the last step lands on 256 itself. So there is one fewer in between.")),
    b("This is the trap. There are 31 steps, but the last step lands on 256, which is an end. So 30 numbers are in between.",
      W("31 − 1 = 30"), A("30")),
    b("Check another way: from 226 to 255 is 255 minus 226, plus 1.", W("255 − 226 + 1 = 30")),
    b("A pattern: between 15 squared and 16 squared there are 2 times 15 numbers. It works for any two neighbours.",
      W("2 × 15 = 30")),
]

L["G4A_SQUARES_032"] = [
    b("The farmer has enough trees for one square, with 5 left over. For the next bigger square he is 20 short. How many trees has he?",
      G("A square with 5 left over; 20 more for the next square")),
    b("Picture his trees on a number line. He is 5 past one perfect square, and 20 short of the next one."),
    b("So how far apart are those two squares?",
      Q(["25", "15", "20"],
        "From the smaller square up to his trees is 5. From his trees up to the bigger square is 20. Together that is 5 plus 20.")),
    b("5 plus 20 is 25. We need two neighbouring squares that are 25 apart.", W("5 + 20 = 25")),
    b("A tip: neighbouring squares differ by the sum of the two numbers. 12 plus 13 is 25, so try 12 and 13.",
      W("12 + 13 = 25")),
    b("12 times 12 is 144, and 13 times 13 is 169. And yes, 169 minus 144 is 25!",
      W("12 × 12 = 144"), W("13 × 13 = 169"), W("169 − 144 = 25")),
    b("So his square holds 144 trees, with 5 left over. 144 plus 5 is 149.", W("144 + 5 = 149"), A("149")),
    b("Check: 149 plus 20 is 169, the next square. And careful: 144 forgets the 5 left over.", W("149 + 20 = 169")),
]

L["G4A_SQUARES_033"] = [
    b("Asha has two square sheets of stamps: 9 rows of 9, and 12 rows of 12. She makes one big square from all of them.",
      G("9 rows of 9 and 12 rows of 12, made into one square")),
    b("Count the stamps on each sheet. 9 times 9 is 81. And 12 times 12 is 144.", W("9 × 9 = 81"), W("12 × 12 = 144")),
    b("Altogether, 81 plus 144 is 225 stamps.", W("81 + 144 = 225")),
    b("The big square has 225 stamps. How do we find the number in each row?",
      Q(["find what times itself is 225", "add 9 and 12", "multiply 9 by 12"],
        "In a square, the rows and columns are equal. So we need the number that, times itself, makes 225.")),
    b("Try 15. 15 times 10 is 150, and 15 times 5 is 75. Together, 225.",
      W("15 × 10 = 150"), W("15 × 5 = 75"), W("15 × 15 = 225")),
    b("So the big square has 15 stamps in each row.", A("15")),
    b("The trap: 9 plus 12 is 21, but sides cannot simply be added. 21 times 21 is 441, far more stamps than she has.",
      W("9 + 12 = 21"), W("21 × 21 = 441")),
]

L["G4A_SQUARES_034"] = [
    b("A riddle with two clues. I am a two-digit perfect square, and my digits add up to 13.",
      G("A two-digit perfect square. Its digits add up to 13.")),
    b("Start with the stronger clue: a two-digit perfect square. There are only 6 of those.",
      W("16, 25, 36, 49, 64, 81", name="sq")),
    b("Now test the second clue on each. 1 plus 6 is 7. 2 plus 5 is 7. 3 plus 6 is 9. None of those is 13.",
      W("1 + 6 = 7"), W("2 + 5 = 7"), W("3 + 6 = 9")),
    b("What do the digits of 49 add up to?",
      Q(["13", "11", "36"], "The digits of 49 are 4 and 9. And 4 plus 9 is 13.")),
    b("4 plus 9 is 13. That fits!", W("4 + 9 = 13"), C("49", on="sq")),
    b("The last two: 6 plus 4 is 10, and 8 plus 1 is 9. So only 49 works.", W("6 + 4 = 10"), W("8 + 1 = 9"), A("49")),
    b("Careful: 67 and 94 also have digits that add up to 13. But they are not perfect squares. Both clues must fit.",
      W("67 and 94: not squares")),
]

L["G4A_SQUARES_035"] = [
    b("We want the smallest perfect square that can be divided exactly by 6, and also by 8.",
      G("Smallest perfect square that 6 and 8 both divide")),
    b("It can be divided by 8, so it must be even. So we only test the even squares, in order.",
      W("4, 16, 36, 64, 100, 144", name="sq")),
    b("4 and 16 cannot be divided by 6. 36 can, but 36 cannot be divided exactly by 8.",
      X("4", on="sq"), X("16", on="sq"), X("36", on="sq")),
    b("64 is 8 times 8, so 8 divides it. Does 6 divide 64 exactly?",
      Q(["No, 6 × 10 = 60 and 6 × 11 = 66", "Yes, exactly"],
        "6 times 10 is 60 and 6 times 11 is 66. 64 falls between them, so 6 does not divide it exactly.")),
    b("64 is out. And 100 is out too, because 6 times 16 is 96 and 6 times 17 is 102.",
      X("64", on="sq"), X("100", on="sq"), W("6 × 16 = 96"), W("6 × 17 = 102")),
    b("Now 144. 144 divided by 6 is 24, and 144 divided by 8 is 18. Both are exact!",
      W("144 ÷ 6 = 24"), W("144 ÷ 8 = 18"), C("144", on="sq")),
    b("So the smallest such perfect square is 144.", A("144")),
    b("The trap is 24 or 48. Both 6 and 8 divide them, but they are not perfect squares. Every word of the question counts.",
      W("24 and 48: not perfect squares")),
]

L["G4A_SQUARES_036"] = [
    b("Most numbers have an even number of factors. We count the numbers from 1 to 50 that have an odd number of factors.",
      G("1 to 50: how many numbers have an odd number of factors?")),
    b("Factors come in pairs. For 12: 1 and 12, 2 and 6, 3 and 4. That is 3 pairs, so 6 factors. An even count.",
      W("12:   1 × 12,   2 × 6,   3 × 4", lab=True)),
    b("Now look at 16: 1 and 16, 2 and 8, and then 4 and 4.", W("16:   1 × 16,   2 × 8,   4 × 4", lab=True)),
    b("4 and 4 is a pair made of the same number. How many times do we count the factor 4?",
      Q(["once", "twice"], "4 is just one factor of 16. We do not list it twice. So this pair adds only 1 to the count.")),
    b("So 16 has 5 factors: 1, 2, 4, 8 and 16. An odd count! That happens when a factor pairs with itself.",
      W("factors of 16:   1, 2, 4, 8, 16")),
    b("This is the key idea. A number has an odd number of factors only when it is a perfect square."),
    b("So we just count the perfect squares up to 50.", W("1, 4, 9, 16, 25, 36, 49")),
    b("There are 7. The next square, 64, is past 50.", W("8 × 8 = 64:  past 50"), A("7")),
    b("Careful: this is not about odd numbers, and not about prime numbers. It is about squares."),
]
