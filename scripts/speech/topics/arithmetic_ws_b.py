"""Hand-written narration lines for worksheet questions EXT_G5_WS_B3 to _B6 (arithmetic topic).

Only the lines the rules in arithmetic_engine.py do not read well. See arithmetic.py for the shape.
"""

OVERRIDES = {
    "EXT_G5_WS_B3_002": {
        "q": "Multiply the two numbers by inserting proper digits in place of the asterisks and find the product. 5, blank, 7, times 4, blank. The first row is blank, 5, 8, blank. Plus the second row, blank, blank, 0, blank, 0. The total is 2, 2, blank, 6, 1.",
        "steps": {
            0: "Units digit of product is 1. 7 times what, gives something ending in 1? Only 7 times 3 equals 21 works. Multiplier units digit equals 3.",
            1: "Multiplier equals 43. From partial product row 1, blank 58 blank: 5 blank 7, times 3, equals blank 58 blank. Try 527 times 3 equals 1581. That works.",
        },
    },
    "EXT_G5_WS_B3_006": {
        "steps": {0: "1 bottle equals 4 cups. 1 jug equals 3 bottles, which is 12 cups."},
    },
    "EXT_G5_WS_B3_008": {
        "q": "Which of the following could be the product of blank, blank, 6, and blank 9, if the asterisk denotes digits, not necessarily the same?",
    },
    "EXT_G5_WS_B3_009": {
        "q": "What can be the possible product of blank, blank, 7, times blank 4, from the given alternatives, when blank denotes digits, not necessarily the same?",
    },
    "EXT_G5_WS_B3_014": {
        "hints": {
            0: "Divisor equals 11. Quotient equals 11, equal to the divisor. Remainder equals 11 minus 2, which is 9.",
            1: "Number equals Divisor times Quotient plus Remainder, which is 11 times 11, plus 9.",
        },
    },
    "EXT_G5_WS_B3_018": {
        "hints": {2: "Try: wrong divisor 3 gives quotient 10, so the number equals 30. Correct divisor 6: 30 divided by 6 equals 5."},
    },
    "EXT_G5_WS_B4_023": {
        "q": "Which of the following sets of symbols should be placed in the blanks: 10, blank, 10, blank, 10, blank, 10, blank, 0?",
    },
    "EXT_G5_WS_B4_024": {
        "q": "4, blank, 8, blank, 15, blank, 5, equals 35. Which sequence of operations?",
    },
    "EXT_G5_WS_B4_025": {
        "hints": {1: "Try each choice. For example, with brackets around 2 times 4, you get 45 divided by 7 plus 8, which is still not a whole number, so that does not work. Which bracket makes a number that divides 45 exactly?"},
    },
    "EXT_G5_WS_B4_029": {
        "hints": {
            0: "Work from the innermost bracket outward: 5 plus 7 first, then curly braces, then square brackets.",
            1: "Innermost: 5 plus 7 equals 12. Then, open curly bracket, 2 times 12 minus 28, close curly bracket, equals 24 minus 28, which is minus 4. Then, open square bracket, 2 plus 3 times 7 minus, open bracket, minus 4, close bracket, close square bracket. BODMAS inside gives 2 plus 21 plus 4, which is 27.",
        },
    },
    "EXT_G5_WS_B4_031": {
        "steps": {0: "Inner brackets: 48 divided by 3 equals 16, and 2 plus 3 equals 5."},
    },
    "EXT_G5_WS_B5_023": {
        "q": "If you add all the odd natural numbers less than 30, the sum will be what?",
        "steps": {3: "So the sum of these 15 odd numbers is 15 times 15, which is 225, or 15 squared."},
    },
    "EXT_G5_WS_B6_017": {
        "hints": {1: "3 p equals 27, so p equals 27 divided by 3, which is 9. Now put p equals 9 and r equals 5 into p equals q plus r, to find q. Remember the question asks for q squared, not q."},
    },
    "EXT_G5_WS_B6_018": {
        "steps": {
            0: "Start: a plus b c equals 5.",
            1: "Subtract a: b c equals 5 minus a.",
        },
    },
}
