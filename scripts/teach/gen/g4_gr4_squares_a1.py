"""gr4_squares, written per question: past papers and worksheets (EXT_G4_..., PYQ_...)."""
from g4_gr4_numbers_lib import A, BX, C, FIG, G, GRP, Q, U, W, X, b, nline, square, table

L = {}


# ── a² + b² = c² ─────────────────────────────────────────────────────────────

def squares_sum(a, bb, c, name, spoken, trap):
    """Lesson for 'a² + b² = name². Find name.' `name` is the letter as printed; `spoken` how it is said."""
    lab = None if name == "x" else True
    return [
        b("Here is our puzzle. %d squared plus %d squared equals %s squared. We must find %s." % (a, bb, spoken, spoken),
          G("%d² + %d² = %s²" % (a, bb, name), name="g", lab=lab)),
        b("The little 2 means squared: the number times itself. So %d squared is %d times %d, which is %d." % (a, a, a, a * a),
          U("%d²" % a, on="g"), W("%d² = %d × %d = %d" % (a, a, a, a * a))),
        b("Now %d squared. What is %d times %d?" % (bb, bb, bb),
          Q([str(bb * bb), str(2 * bb), str(bb * bb - 100)],
            "Squared means times itself, not times 2. %d lots of %d make %d." % (bb, bb, bb * bb))),
        b("%d times %d is %d." % (bb, bb, bb * bb), U("%d²" % bb, on="g"), W("%d² = %d × %d = %d" % (bb, bb, bb, bb * bb))),
        b("Add the two squares. %d plus %d is %d. So %s squared is %d." % (a * a, bb * bb, c * c, spoken, c * c),
          W("%d + %d = %d" % (a * a, bb * bb, c * c)), W("%s² = %d" % (name, c * c), lab=lab)),
        b("Now, which number times itself makes %d? Try %d. %d times 10 is %d, and %d times %d is %d. Together, %d. Yes!"
          % (c * c, c, c, c * 10, c, c - 10, c * (c - 10), c * c),
          W("%d × 10 = %d" % (c, c * 10)), W("%d × %d = %d" % (c, c - 10, c * (c - 10))), W("%d × %d = %d" % (c, c, c * c))),
        b("So %s is %d." % (spoken, c), A("%s = %d" % (name, c), lab=lab)),
        trap,
        b("So: square each number, add the squares, then find the number whose square that is."),
    ]


L["EXT_G4_FP_2020_034"] = {
    "check": {"variable": "x", "value": "17"},
    "beats": squares_sum(
        8, 15, 17, "x", "x",
        b("Careful: x is not 8 plus 15. That gives 23, and 23 times 23 is far more than 289. Square first, then add.",
          W("8 + 15 = 23"))),
}

L["EXT_G4_FP_2021_003"] = squares_sum(
    5, 12, 13, "M", "M",
    b("Careful: 169 is M squared, not M. The question asks for M itself, the number that times itself makes 169."))


# ── The hall of chairs (asked twice, in the same words) ──────────────────────

def hall():
    return [
        b("The hall has as many rows as there are chairs in each row, and every chair is filled. Which of these could be the number of men?",
          G("Rows = chairs in each row. How many men?"), W("131     325     275     324"),
          FIG(square("?", note="Rows = chairs in each row"))),
        b("Think of a small hall: 5 rows of 5 chairs hold 25 men. So what kind of number is the number of men?",
          W("5 rows of 5:   5 × 5 = 25", lab=True),
          Q(["a number times itself", "an even number", "a number ending in 5"],
            "Men equals rows times chairs in a row, and those two are the same. So it is a number times itself: a square number.")),
        b("So we are looking for a square number. Let us test each choice against squares we know."),
        b("131: 11 times 11 is 121 and 12 times 12 is 144. 131 falls in between, so it is not a square.",
          W("11 × 11 = 121"), W("12 × 12 = 144"), W("121 < 131 < 144")),
        b("275: 16 times 16 is 256 and 17 times 17 is 289. In between again, so not a square.",
          W("16 × 16 = 256"), W("17 × 17 = 289"), W("256 < 275 < 289")),
        b("Now try 18. 18 times 18 is 324. That is one of our choices!",
          W("18 × 18 = 324"), FIG(square(18, inside="324 men", note="18 rows of 18 chairs"))),
        b("Careful with 325. It is only 1 more than 324, but a full hall needs an exact square. One extra man would have no chair."),
        b("So the number of men can be 324.", A("324")),
        b("So: equal rows and columns means a square number. Test each choice by squeezing it between two squares."),
    ]


L["EXT_G4_FP_2021_005"] = hall()
L["PYQ_2016_Q31"] = hall()


# ── Which pair adds up to a square? (asked twice, in the same numbers) ───────

def pair_sum():
    return [
        b("4 pairs of numbers. We add each pair, and look for a total that is a square number.",
          G("Which pair adds up to a square number?"), W("91 & 19     157 & 68     59 & 52     76 & 78")),
        b("First pair: 91 plus 19 is 110.", W("91 + 19 = 110")),
        b("Is 110 a square number? 10 times 10 is 100 and 11 times 11 is 121.",
          W("10 × 10 = 100"), W("11 × 11 = 121"),
          Q(["No, it falls between two squares", "Yes, it is a square"],
            "110 is more than 100 but less than 121. There is no whole number between 10 and 11, so 110 is not a square.")),
        b("110 sits between 100 and 121, so it is not a square. Next pair: 157 plus 68 is 225.", W("157 + 68 = 225")),
        b("225 is 15 times 15. A square number!", W("15 × 15 = 225"), BX("225")),
        b("Let us check the others, to be sure. 59 plus 52 is 111, and 76 plus 78 is 154. Neither is a square.",
          W("59 + 52 = 111"), W("76 + 78 = 154")),
        b("So the pair is 157 and 68.", A("157 & 68")),
        b("A tip: learn the squares of the numbers up to 15 by heart. Then you spot 225 at once."),
    ]


L["EXT_G4_FP_2021_018"] = pair_sum()
L["PYQ_2018_Q36"] = pair_sum()

L["EXT_G4_FP_2023_032"] = [
    b("3 pairs of numbers. We add each pair, and look for a total that is a square number.",
      G("Which two numbers add up to a square?"), W("159 & 165     198 & 145     189 & 330")),
    b("First pair: 159 plus 165 is 324.", W("159 + 165 = 324")),
    b("Is 324 a square? Try 18. 18 times 10 is 180, and 18 times 8 is 144. So what is 18 times 18?",
      W("18 × 10 = 180"), W("18 × 8 = 144"),
      Q(["324", "36", "314"], "18 times 18 is 18 times 10 and 18 times 8 together. 180 plus 144 makes 324.")),
    b("180 plus 144 is 324. So 324 is 18 times 18, a square!", W("18 × 18 = 324"), BX("324")),
    b("Check the others. 198 plus 145 is 343. That is past 324, but short of 19 times 19, which is 361. Not a square.",
      W("198 + 145 = 343"), W("19 × 19 = 361")),
    b("189 plus 330 is 519. 22 times 22 is 484 and 23 times 23 is 529. In between, so not a square.",
      W("189 + 330 = 519"), W("22 × 22 = 484"), W("23 × 23 = 529")),
    b("So the pair is 159 and 165.", A("159 and 165")),
    b("Careful: do not jump to none of these because the sums look hard. Add each pair properly first."),
]

L["EXT_G4_FP_2021_023"] = [
    b("Which sign goes in the box? We work out the left side, then the right side, and compare.",
      G("(29)² □ (31)² − (10)²")),
    b("Left side: 29 times 29. A handy way: 29 times 30 is 870, then take away one 29. That leaves 841.",
      W("29 × 30 = 870"), W("870 − 29 = 841"), W("29² = 841")),
    b("On the right side, what must we do first?",
      Q(["square 31 and square 10", "subtract 10 from 31", "add 31 and 10"],
        "The squares come before the subtraction. So first work out 31 squared and 10 squared, and only then subtract.")),
    b("This is the trap. 31 minus 10 is 21, but we must not subtract first. Each number is squared first.",
      W("31 − 10 = 21:  not yet!")),
    b("31 times 31: 31 times 30 is 930, plus one more 31 is 961.", W("31 × 30 = 930"), W("930 + 31 = 961"), W("31² = 961")),
    b("10 squared is 100. So the right side is 961 minus 100, which is 861.", W("10² = 100"), W("961 − 100 = 861")),
    b("841 is less than 861. So the sign is: less than.", W("841 < 861"), A("(29)² < (31)² − (10)²")),
    b("So: squares first, then the take away, then compare."),
]

L["EXT_G4_FP_2021_032"] = [
    b("We must multiply 28 by the smallest number that turns it into a perfect square. The secret is in its prime factors.",
      G("28 × ? = a perfect square  (smallest ?)"),
      FIG({"kind": "factorTree", "number": 28, "note": "Break 28 into prime factors"})),
    b("Break 28 down. 28 is 2 times 14, and 14 is 2 times 7. So 28 is 2 times 2 times 7.",
      W("28 = 2 × 14"), W("28 = 2 × 2 × 7", name="f")),
    b("In a perfect square, every prime factor has a partner. Look at 36: it is 2 times 2 times 3 times 3. Two pairs.",
      W("36 = 2 × 2 × 3 × 3")),
    b("In 28, the two 2s make a pair. Which factor has no partner?",
      GRP([("2", 2), ("2", 3)], label="a pair", on="f"),
      Q(["7", "2", "14"], "28 is 2 times 2 times 7. The 2s pair up with each other. The 7 stands alone.")),
    b("The 7 is alone. So we give it a partner: multiply by one more 7.", C("7", on="f"), W("28 × 7 = 196")),
    b("Check: 196 is 14 times 14. A perfect square!", W("14 × 14 = 196"), A("7")),
    b("Careful: guessing small numbers does not help here. Any other small number leaves the 7 without a partner."),
    b("So: break into primes, pair them up, and multiply by whatever is left alone."),
]

L["EXT_G4_FP_2022_009"] = [
    b("For each pair, we square both numbers and add. We want a total that is itself a square number.",
      G("Sum of the squares of which two is a square?"), W("10, 15     7, 24     8, 45     9, 25")),
    b("Start with 10 and 15. 10 squared is 100 and 15 squared is 225. Together, 325.", W("10² + 15² = 100 + 225 = 325")),
    b("Is 325 a square? 18 times 18 is 324. So 325 misses by just 1. Not a square.", W("18 × 18 = 324")),
    b("Next, 7 and 24. 7 squared is 49. For 24 squared: 24 times 20 is 480 and 24 times 4 is 96. So what is 24 times 24?",
      W("7² = 49"), W("24 × 20 = 480"), W("24 × 4 = 96"),
      Q(["576", "48", "476"], "Add the two parts. 480 plus 96 makes 576.")),
    b("480 plus 96 is 576. So the total is 49 plus 576, which is 625.", W("7² + 24² = 49 + 576 = 625")),
    b("And 625 is 25 times 25. A square!", W("25 × 25 = 625"), BX("625")),
    b("The other two pairs give 2089 and 706, and neither of those is a square.",
      W("8² + 45² = 2089"), W("9² + 25² = 706")),
    b("So the pair is 7 and 24.", A("7 and 24")),
    b("The trap is the first pair. 325 is so close to 324 that it is easy to believe. Close is not enough for a square."),
]

L["EXT_G4_FP_2022_022"] = [
    b("We must multiply 588 by the least number that makes a perfect square. The secret is in its prime factors.",
      G("588 × ? = a perfect square  (least ?)"),
      FIG({"kind": "factorTree", "number": 588, "note": "Break 588 into prime factors"})),
    b("Break 588 down. 588 is 2 times 294, and 294 is 2 times 147.", W("588 = 2 × 294"), W("294 = 2 × 147")),
    b("147 is 3 times 49, and 49 is 7 times 7. So 588 is 2 times 2 times 3 times 7 times 7.",
      W("147 = 3 × 49"), W("588 = 2 × 2 × 3 × 7 × 7", name="f")),
    b("In a perfect square every factor has a partner. The 2s make a pair and the 7s make a pair. Which factor is alone?",
      Q(["3", "2", "7"], "There are two 2s and two 7s, so they pair up. There is only one 3, so it is alone.")),
    b("The 3 is alone. So we multiply by 3 to give it a partner.", C("3", on="f"), W("588 × 3 = 1764")),
    b("Check: 1764 is 42 times 42. A perfect square.", W("42 × 42 = 1764")),
    b("So the least number is 3. Now look at the choices: 2, 6 and 4. There is no 3!", W("choices: 2, 6, 4, None of these")),
    b("Here is the trap. When your answer is not in the list, do not bend it to fit. The answer is None of these.",
      A("None of these")),
    b("A quick check of the others: multiplying by 2, 4 or 6 still leaves a factor without a partner."),
]

L["EXT_G4_FP_2023_022"] = [
    b("We add something to 1234 to reach a square number. So we need the first square above 1234.",
      G("1234 + ? = a square number"), FIG(nline(1220, 1300, 10, [(1234, "1234")], note="How far is the next square?"))),
    b("Where to start? 30 times 30 is 900, too small. 40 times 40 is 1600, too big. So try in between, at 35.",
      W("30 × 30 = 900"), W("40 × 40 = 1600"), W("try 35")),
    b("35 times 35 is 1225. That is just under 1234.", W("35 × 35 = 1225")),
    b("1225 is below 1234. So which square should we aim for?",
      Q(["36 × 36", "35 × 35", "34 × 34"],
        "We are adding, so we must go up. The next square after 35 times 35 is 36 times 36.")),
    b("36 times 36: 36 times 30 is 1080, and 36 times 6 is 216. Together, 1296.",
      W("36 × 30 = 1080"), W("36 × 6 = 216"), W("36 × 36 = 1296")),
    b("Now find the gap from 1234 up to 1296. It is 62.", W("1296 − 1234 = 62"),
      FIG(nline(1220, 1300, 10, [(1234, "1234"), (1296, "1296")], hops=[(1234, 1296, "+62")]))),
    b("So we must add 62.", A("62")),
    b("Check: 1234 plus 62 is 1296, and that is 36 times 36.", W("1234 + 62 = 1296")),
]

L["EXT_G4_FP_2024_019"] = [
    b("Two special squares to find, and then we divide one by the other.",
      G("Smallest 4-digit square ÷ greatest 2-digit even square")),
    b("The smallest 4-digit number is 1000. 30 times 30 is 900, so we are close. 31 times 31 is 961. Still only 3 digits.",
      W("smallest 4-digit number: 1000"), W("30 × 30 = 900"), W("31 × 31 = 961")),
    b("Try 32. 32 times 32 is 1024. That is the smallest 4-digit square.", W("32 × 32 = 1024")),
    b("Now the 2-digit squares: 16, 25, 36, 49, 64 and 81. Which is the greatest even one?",
      W("16, 25, 36, 49, 64, 81", name="sq"),
      Q(["64", "81", "36"], "81 is the greatest, but it is odd. The greatest even one is 64.")),
    b("81 is bigger, but it is odd. That is the trap. The greatest even one is 64.", X("81", note="odd", on="sq"), C("64", on="sq")),
    b("Now divide 1024 by 64. 64 times 10 is 640. That leaves 384, and 64 times 6 is 384.",
      W("64 × 10 = 640"), W("1024 − 640 = 384"), W("64 × 6 = 384")),
    b("10 lots and 6 lots make 16 lots. So the quotient is 16.", W("1024 ÷ 64 = 16"), A("16")),
    b("So: find each special number carefully, word by word, and only then divide."),
]

L["EXT_G4_FP_2025_009"] = [
    b("We divide the greatest 2-digit square by the smallest 2-digit square, and find what is left over.",
      G("Greatest 2-digit square ÷ smallest one: remainder = ?")),
    b("List the squares. 1, 4 and 9 have one digit. Then come 16, 25, 36, 49, 64 and 81. And 100 has 3 digits.",
      W("16, 25, 36, 49, 64, 81", name="sq"), W("10 × 10 = 100:  3 digits")),
    b("So the greatest 2-digit square is 81 and the smallest is 16.", C("81", on="sq"), C("16", on="sq")),
    b("Now divide 81 by 16. 5 times 16 is 80 and 6 times 16 is 96. So how many lots of 16 fit into 81?",
      W("5 × 16 = 80"), W("6 × 16 = 96"),
      Q(["5", "4", "6"], "5 lots make 80, which fits inside 81. 6 lots make 96, which is too much.")),
    b("5 lots of 16 make 80. 6 lots would be 96, which is too many."),
    b("81 minus 80 leaves 1. That is the remainder.", W("81 − 80 = 1"), A("1")),
    b("Check: 5 times 16, plus 1, is 81.", W("5 × 16 + 1 = 81")),
    b("Careful: 100 is a square, but it has 3 digits. The greatest 2-digit square is 81."),
]

L["EXT_G4_WS2_CH16_013"] = [
    b("6 numbers, and one does not belong. First, what do they all have in common?",
      G("Odd one out: 144, 169, 196, 256, 324, 400", name="g")),
    b("What kind of numbers are these?",
      Q(["square numbers", "prime numbers", "multiples of 12"],
        "144 is 12 times 12. In the same way, every number here is some number times itself, so they are square numbers.")),
    b("They are all squares: of 12, 13, 14, 16, 18 and 20.",
      FIG(table(["Number", "Square of"], [[144, 12], [169, 13], [196, 14], [256, 16], [324, 18], [400, 20]]))),
    b("So being a square does not pick one out. Look again at the numbers being squared: 12, 13, 14, 16, 18 and 20."),
    b("All of them are even, except 13. And an odd number squared stays odd. 169 is the only odd number in the list.",
      C("169", on="g")),
    b("So the odd one out is 169.", A("169")),
    b("When everything looks alike, dig one level deeper. Here, that meant asking what each number is the square of."),
]

L["EXT_G4_WS2_CH16_014"] = [
    b("6 numbers, and one does not belong. They are all square numbers, so let us find what each is the square of.",
      G("Which does not belong? 81, 121, 169, 289, 361, 529", name="g")),
    b("81 is 9 times 9. 121 is 11 times 11. 169 is 13 times 13.",
      FIG(table(["Number", "Square of"], [[81, 9], [121, 11], [169, 13], [289, 17], [361, 19], [529, 23]]))),
    b("289 is 17 times 17. 361 is 19 times 19. And 529 is 23 times 23."),
    b("Look at 9, 11, 13, 17, 19 and 23. What is special about most of them?",
      Q(["they are prime numbers", "they are even numbers", "they are multiples of 3"],
        "11, 13, 17, 19 and 23 can only be divided by 1 and themselves. They are prime numbers.")),
    b("5 of them are prime. But 9 is not prime, because 9 is 3 times 3.", W("9 = 3 × 3")),
    b("So 81 is the square of a number that is not prime. It does not belong.", C("81", on="g"), A("81")),
    b("The trap: all 6 numbers are odd, and all are squares, so those ideas do not help. The difference hides in the number being squared."),
]

L["PYQ_2017_Q34"] = [
    b("For each pair, we square both numbers and add. We want a total that is itself a square number.",
      G("Sum of the squares of which two is a square?"), W("2, 3     5, 6     4, 6     6, 8")),
    b("2 and 3: the squares are 4 and 9, and together they make 13. Not a square.", W("2² + 3² = 4 + 9 = 13")),
    b("5 and 6: 25 plus 36 is 61. And 4 and 6: 16 plus 36 is 52.",
      W("5² + 6² = 25 + 36 = 61"), W("4² + 6² = 16 + 36 = 52")),
    b("7 times 7 is 49 and 8 times 8 is 64. So are 52 and 61 squares?",
      W("7 × 7 = 49"), W("8 × 8 = 64"),
      Q(["No, both lie between 49 and 64", "Yes, both are"],
        "52 and 61 are both more than 49 and less than 64. No whole number lies between 7 and 8, so neither is a square.")),
    b("Now 6 and 8: 36 plus 64 is 100.", W("6² + 8² = 36 + 64 = 100")),
    b("And 100 is 10 times 10. A square! So the pair is 6 and 8.", W("10 × 10 = 100"), A("6 and 8")),
    b("Notice: 6, 8 and 10 are the famous 3, 4 and 5, doubled. 9 plus 16 is 25 as well.", W("3² + 4² = 9 + 16 = 25")),
]

L["PYQ_2017_Q38"] = [
    b("We count the square numbers that have 2 digits and are even.", G("How many even 2-digit square numbers?")),
    b("First list every 2-digit square. Start at 4 times 4, which is 16, and stop before 10 times 10, which is 100.",
      W("16, 25, 36, 49, 64, 81", name="sq"), W("10 × 10 = 100:  3 digits")),
    b("Which numbers give an even square?",
      Q(["even numbers", "odd numbers", "every number"],
        "Even times even is even, and odd times odd is odd. So only even numbers give even squares.")),
    b("Even times even is even. So the even squares come from 4, 6 and 8.",
      W("4 × 4 = 16"), W("6 × 6 = 36"), W("8 × 8 = 64"), C("16", on="sq"), C("36", on="sq"), C("64", on="sq")),
    b("That is 16, 36 and 64. So there are 3 of them.", A("3")),
    b("Careful: 6 is the count of all the 2-digit squares. The question wants only the even ones."),
    b("And 4 and 100 are even squares too, but they do not have 2 digits."),
]

L["PYQ_2019_Q26"] = [
    b("We add something to 710 to reach a square number. So we need the first square above 710.",
      G("710 + ? = a square number"), FIG(nline(700, 730, 5, [(710, "710")], note="How far is the next square?"))),
    b("Where to start? 25 times 25 is 625, too small. 30 times 30 is 900, too big.", W("25 × 25 = 625"), W("30 × 30 = 900")),
    b("Try 26. 26 times 26 is 676. Still below 710.", W("26 × 26 = 676")),
    b("676 is still below 710. What should we try next?",
      Q(["27 × 27", "25 × 25", "26 × 26 again"], "We need a square above 710, so we go up one more, to 27 times 27.")),
    b("27 times 27: 27 times 20 is 540 and 27 times 7 is 189. Together, 729. That is above 710!",
      W("27 × 20 = 540"), W("27 × 7 = 189"), W("27 × 27 = 729")),
    b("The gap from 710 up to 729 is 19.", W("729 − 710 = 19"), A("19")),
    b("Check: 710 plus 19 is 729, which is 27 times 27.", W("710 + 19 = 729")),
    b("Careful: landing near 729 is not enough. A square has to be hit exactly."),
]
