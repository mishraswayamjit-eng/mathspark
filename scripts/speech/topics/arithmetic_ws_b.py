"""Hand-written narration lines for worksheet questions EXT_G5_WS_B3 to _B6 (arithmetic topic).

Only the lines the rules in arithmetic_engine.py do not read well. See arithmetic.py for the shape.
"""

_SMALLER = "Try with smaller numbers: 23 times 4 equals 92. Units: 3 times 4 equals 12, ends in 2, that works."
_NOT = "That does not work."

OVERRIDES = {
    "EXT_G5_WS_B3_002": {
        "q": "Multiply the two numbers by inserting proper digits in place of the asterisks and find the product. 5, blank, 7, times 4, blank. The first row is blank, 5, 8, blank. Plus the second row, blank, blank, 0, blank, 0. The total is 2, 2, blank, 6, 1.",
        "hints": {
            0: "The product ends in 1. 7 times blank must end in 1. Which single digit, times 7, ends in 1?",
            1: "3 times 7 equals 21, which ends in 1. So the units digit of the multiplier is 3. Multiplier equals 43.",
            2: "Try: if it is 5 blank 7, times 43, the units row equals 5 blank 7, times 3, which is blank, 5, 8, blank. 507 times 3 equals 1521. 517 times 3 equals 1551. 527 times 3 equals 1581. 537 times 3 equals 1611. 547 times 3 equals 1641. 557 times 3 equals 1671. 567 times 3 equals 1701. We need the blank 58 blank pattern. 527 times 3 equals 1581, that works. 527 times 43 equals 22661.",
        },
        "steps": {
            0: "Units digit of product is 1. 7 times what, gives something ending in 1? Only 7 times 3 equals 21 works. Multiplier units digit equals 3.",
            1: "Multiplier equals 43. From partial product row 1, blank 58 blank: 5 blank 7, times 3, equals blank 58 blank. Try 527 times 3 equals 1581. That works.",
        },
    },
    "EXT_G5_WS_B3_004": {
        "hints": {
            1: "Number of doublings equals 120 divided by 20, which is 6. Starting from 1, after 6 doublings: 1 times 2 to the power six.",
            2: "Try: after 20 minutes there are 2, after 40 minutes 4, after 60 minutes 8, and so on.",
        },
        "steps": {1: "After 6 doublings: 1 times 2 to the power six, equals 64."},
    },
    "EXT_G5_WS_B3_006": {
        "hints": {0: "Build the chain: cups, then bottles, then jugs, then buckets."},
        "steps": {0: "1 bottle equals 4 cups. 1 jug equals 3 bottles, which is 12 cups."},
    },
    "EXT_G5_WS_B3_007": {
        "steps": {1: "New product equals 2 a times 3 b, which is 6 a b. That is 6 times 108, which is 648."},
    },
    "EXT_G5_WS_B3_008": {
        "q": "Which of the following could be the product of blank, blank, 6, and blank 9, if the asterisk denotes digits, not necessarily the same?",
        "hints": {
            0: "A 3-digit number times a 2-digit number gives at most a 5-digit number. Check which option is possible.",
            1: "Units: 6 times 9 equals 54, so the product ends in 4. Check the options: 5417 ends in 7, no. 5104 ends in 4, yes. 86996 ends in 6, no. 357604 ends in 4, yes.",
            2: _SMALLER,
        },
        "steps": {
            0: "Units digit of product: 6 times 9 equals 54, so the product ends in 4.",
            1: "Check options: A ends in 7, no. B ends in 4, yes. C ends in 6, no. D ends in 4, yes.",
            2: "B: 5104 divided by 19 equals 268.6 and so on. Try 5104 divided by 29, which equals 176. 176 fits the blank 76 pattern, with blank equal to 1, so 176 times 29 equals 5104. 176 matches blank, blank, 6. That works.",
            3: "But wait, C, 86996, ends in 6, not 4. Let me recheck. Hmm, but maybe I need to recheck the image for option text. From the image: option 1 is 5417, option 2 is 5104, option 3 is 86996, option 4 is 357604. Let me verify B: 176 times 29 equals 5104. 176 matches the blank, blank, 6 pattern, and 29 matches blank 9. So B works.",
            4: "Actually, also check D: 357604. The most that blank, blank, 6, times blank 9 can be, is 996 times 99, which is 98604. 357604 is greater than 98604, so it is impossible.",
        },
    },
    "EXT_G5_WS_B3_009": {
        "q": "What can be the possible product of blank, blank, 7, times blank 4, from the given alternatives, when blank denotes digits, not necessarily the same?",
        "hints": {
            0: "Units: 7 times 4 equals 28, so the product ends in 8. Check the options.",
            1: "A: 104978 ends in 8, yes. B: 35271 ends in 1, no. C: 16448 ends in 8, yes. D: 1398 ends in 8, yes.",
            2: _SMALLER,
        },
        "steps": {
            0: "Units: 7 times 4 equals 28, so the product ends in 8.",
            1: "Check A: 104978 is too large for a 3-digit number times a 2-digit number. The maximum is 93718.",
        },
    },
    "EXT_G5_WS_B3_011": {
        "hints": {
            1: "540 divided by 26 equals 20, remainder 20. So 20 full rows, plus 20 girls in the 21st row. We need 26 minus 20, which is 6 more.",
            2: "Try: 12 items, 5 per row: 12 divided by 5 equals 2, remainder 2. We need 5 minus 2, which is 3 more for the 3rd row.",
        },
    },
    "EXT_G5_WS_B3_012": {
        "hints": {
            0: "Convert to centimetres: 10 metres equals 1000 centimetres. Divide by 7 and find the remainder.",
            1: "1000 divided by 7 equals 142, remainder 6. But we want the minimum leftover. If each piece is 143 centimetres: 143 times 7 equals 1001, which is greater than 1000. So each piece equals 142 centimetres, and the leftover equals 1000 minus 994, which is 6 centimetres. Hmm.",
        },
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
    "EXT_G5_WS_B3_034": {
        "hints": {
            0: "Total steps equals 11 plus 17 minus 1, which is 27. Subtract 1 because Manav's step is counted twice.",
            1: "Middle step equals, open bracket, 27 plus 1, close bracket, divided by 2, which is the 14th step from the bottom.",
        },
    },
    "EXT_G5_WS_B3_035": {
        "steps": {
            2: "Between Nisha, 19th, and Disha, 15th: 19 minus 15 minus 1, which is 3. Hmm, or is it 19 minus 15, which equals 4?",
            3: "Positions between 15 and 19: 16, 17, 18. That is 3 people. The answer is A.",
        },
    },
    "EXT_G5_WS_B3_038": {
        "hints": {
            1: "Overtime rate equals 8 times 2, which is 16 rupees per hour. Overtime hours equals 96 divided by 16, which is 6.",
            2: "Try: 5 rupees per hour, 10 hours regular equals 50, total equals 74, overtime pay equals 24, overtime rate equals 10, overtime hours equals 2.4.",
        },
    },
    "EXT_G5_WS_B3_039": {
        "hints": {
            0: "P equals 6 a plus 2, and Q equals 6 b plus 5, for some integers a and b.",
            2: "Try: P equals 8, which divided by 6 leaves remainder 2. Q equals 11, which divided by 6 leaves remainder 5. P plus Q equals 19. 19 divided by 6 equals 3, remainder 1.",
        },
        "steps": {0: "P equals 6 a plus 2, and Q equals 6 b plus 5."},
    },
    "EXT_G5_WS_B4_015": {
        "hints": {
            1: "Statement 1: is 4 a multiple of 8? No. Statement 2: is 12 a multiple of 6? Yes, and any multiple of 12 is a multiple of 6, since 12 equals 6 times 2.",
            2: "Similar: 'Every multiple of 6 is a multiple of 3' is true, because 6 equals 3 times 2.",
        },
        "steps": {
            0: "Statement 1: 4 is a multiple of 4 but not of 8, so it is false.",
            1: "Statement 2: if n is divisible by 12, then n equals 12 k, which is 6 times 2 k, so n is divisible by 6. So it is true.",
            2: "Statement 3: 7 minus 3 equals 4, which is not prime, so it is false.",
            3: "Statement 4: 3 times 1 equals 3, and 3 is not divisible by 9, so it is false.",
            4: "Only statement 2 is always true.",
        },
    },
    "EXT_G5_WS_B4_023": {
        "q": "Which of the following sets of symbols should be placed in the blanks: 10, blank, 10, blank, 10, blank, 10, blank, 0?",
        "hints": {
            1: "Option C: 10 times 10 divided by 10, minus 10. By BODMAS: 10 times 10 equals 100, 100 divided by 10 equals 10, and 10 minus 10 equals 0. That works!",
            2: "Similar: fill in: 5, blank, 5, blank, 5, blank, 5, equals 0. Try times, divided by, minus: 5 times 5 divided by 5, minus 5, equals 5 minus 5, which is 0. That works.",
        },
        "steps": {
            1: "Step 1, BODMAS, multiplication first: 10 times 10 equals 100.",
            2: "Step 2, division next: 100 divided by 10 equals 10.",
            3: "Step 3, subtraction last: 10 minus 10 equals 0. That works.",
        },
    },
    "EXT_G5_WS_B4_024": {
        "q": "4, blank, 8, blank, 15, blank, 5, equals 35. Which sequence of operations?",
        "hints": {
            2: "Similar: 2, blank, 3, blank, 6, blank, 1, equals 7. Try times, plus, divided by: 2 times 3, plus 6 divided by 1, equals 6 plus 6, which is 12. " + _NOT + " Try plus, times, minus: 2 plus 3 times 6 minus 1, equals 2 plus 18 minus 1, which is 19. " + _NOT,
        },
    },
    "EXT_G5_WS_B4_025": {
        "hints": {
            0: "Without brackets: 45 divided by 7, plus 2 times 4, equals 6.43 plus 8, which is about 14.43, and that is not equal to 20. Try inserting brackets to change the order.",
            1: "If we put brackets around 7 plus 2: 45 divided by, open bracket, 7 plus 2, close bracket, times 4, equals 45 divided by 9 times 4, that is 5 times 4, which is 20. That works!",
            2: "Similar: make 24 divided by 2, plus 4 times 3, equals 12, true. Try brackets around 2 plus 4: 24 divided by, open bracket, 2 plus 4, close bracket, times 3, equals 4 times 3, which is 12. That works.",
        },
    },
    "EXT_G5_WS_B4_027": {
        "hints": {
            1: "Option 3: 6 times 6, minus 6 divided by 6, equals 36 minus 1, which is 35. Does that match? Yes!",
            2: "Similar: is 4 times 4, minus 4 divided by 4, equal to 15? 16 minus 1 equals 15. That works.",
        },
        "steps": {
            0: "Option 1: 15 minus 15 times 15 equals 15 minus 225, which is minus 210, not 0. " + _NOT,
            1: "Option 2: 18 times, open bracket, 18 plus 0, close bracket, equals 18 times 18, which is 324, not 36. " + _NOT,
            2: "Option 3: 6 times 6, minus 6 divided by 6, equals 36 minus 1, which is 35. That works.",
            3: "Option 4: 17 minus 5 times 0 equals 17 minus 0, which is 17, not 0. " + _NOT,
        },
    },
    "EXT_G5_WS_B4_028": {
        "hints": {
            1: "A: 15 times 2 equals 30. B: 15 minus 35 equals minus 20. C: 15 minus 7 minus 5 equals 3. D: 8 times 5 equals 40. Smallest is minus 20, the most negative.",
            2: "Similar: which is least? 3 times, open bracket, 2 minus 5, close bracket. 3 minus 2 times 5. 3 minus 2 minus 5. Answers: minus 9, minus 7, minus 4. Least equals minus 9.",
        },
        "steps": {1: "B: 15 minus 7 times 5 equals 15 minus 35, which is minus 20. BODMAS: multiply first!"},
    },
    "EXT_G5_WS_B4_029": {
        "hints": {
            0: "Work from the innermost bracket outward: 5 plus 7 first, then curly braces, then square brackets.",
            1: "Innermost: 5 plus 7 equals 12. Then, open curly bracket, 2 times 12 minus 28, close curly bracket, equals 24 minus 28, which is minus 4. Then, open square bracket, 2 plus 3 times 7 minus, open bracket, minus 4, close bracket, close square bracket. BODMAS inside gives 2 plus 21 plus 4, which is 27.",
        },
    },
    "EXT_G5_WS_B4_030": {
        "hints": {0: "BODMAS: first evaluate the curly braces, then multiplication and division, then addition and subtraction."},
    },
    "EXT_G5_WS_B4_031": {
        "hints": {0: "Work innermost brackets first, then curly braces, then divide."},
        "steps": {0: "Inner brackets: 48 divided by 3 equals 16, and 2 plus 3 equals 5."},
    },
    "EXT_G5_WS_B4_032": {
        "hints": {0: "The bar, called a vinculum, over 6 plus 3 times 2, groups that expression. Under BODMAS within the bar: 3 times 2 equals 6 first, then 6 plus 6 equals 12."},
        "steps": {0: "Vinculum: 6 plus 3 times 2 equals 6 plus 6, which is 12, using BODMAS within."},
    },
    "EXT_G5_WS_B5_023": {
        "q": "If you add all the odd natural numbers less than 30, the sum will be what?",
        "hints": {
            0: "Odd numbers less than 30: 1, 3, 5, and so on up to 29. How many are there?",
            2: "Similar: 1 plus 3 plus 5 plus 7 is 4 odd numbers, which gives 4 squared, which is 16. That works.",
        },
        "steps": {0: "Odd numbers less than 30: 1, 3, 5, and so on up to 29."},
    },
    "EXT_G5_WS_B6_018": {
        "steps": {
            0: "Start: a plus b c equals 5.",
            1: "Subtract a: b c equals 5 minus a.",
        },
    },
}
