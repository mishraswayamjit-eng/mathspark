"""Hand-written narration lines for past-paper questions (EXT_G5_FP_...) in the arithmetic topic.

Only the lines the rules in arithmetic_engine.py do not read well. See arithmetic.py for the shape.
"""

_NOT = "That does not work."

OVERRIDES = {
    "EXT_G5_FP_2016_002": {
        "hints": {
            0: "If you know the first plus second bags together, then the total, minus first plus second, tells you the third bag alone.",
            1: "Total, minus two bags, equals the bag that was left out.",
        },
    },
    "EXT_G5_FP_2016_010": {
        "hints": {1: "15 minutes equals 15 over 60 of an hour, which is one quarter of an hour, or 0.25 hours."},
        "steps": {0: "15 minutes equals 15 over 60 of an hour, which is one quarter of an hour, or 0.25 hours."},
    },
    "EXT_G5_FP_2016_031": {
        "hints": {1: "BODMAS: Brackets, then Multiplication, then Addition and Subtraction."},
        "steps": {4: "The least value is 0. That is 9 minus 3 times 3."},
    },
    "EXT_G5_FP_2017_010": {
        "q": "Which set of signs of operations should be replaced in the boxes so that the equation is true: 10, blank, 6, blank, 4, blank, 6, equals 28?",
        "steps": {1: "Option B: 10 plus 6, minus 4 divided by 6, is not 28. " + _NOT},
    },
    "EXT_G5_FP_2017_015": {
        "hints": {1: "Bracket order: round brackets, then curly brackets, then square brackets. Then BODMAS."},
    },
    "EXT_G5_FP_2017_025": {
        "q": "A two-digit number, blank 9, is multiplied by a three-digit number, blank, blank, 3. The digits in the blank places are not necessarily the same. Which of the following can be the product of the given two numbers?",
        "steps": {
            0: "Last digit: 9 times 3 equals 27, so it ends in 7. All options end in 7, so size must decide.",
            1: "1907 and 957 are smaller than the smallest possible product, 1957. So they do not work.",
            2: "756927 is bigger than the largest possible product, about 98,300. So it does not work.",
            3: "Only 46847 is left, and it works. It equals 79 times 593.",
        },
    },
    "EXT_G5_FP_2017_032": {
        "q": "What is the value of: open bracket, 66 plus 77 plus 88 plus 99, close bracket, divided by, open bracket, 11 plus 22 plus 33 plus 44, close bracket?",
    },
    "EXT_G5_FP_2018_003": {
        "steps": {0: "1.5 times 0.05 equals 0.075. That is 15 times 5 equals 75, with 3 decimal places."},
    },
    "EXT_G5_FP_2018_028": {
        "hints": {
            0: "Articles must be a whole number. Multiply each decimal by 12. Which one gives a number with a decimal part?",
            1: "Number of articles equals dozens times 12, and it must be whole.",
        },
        "steps": {
            0: "3.75 times 12 equals 45, that works. 3.25 times 12 equals 39, that works. 3.5 times 12 equals 42, that works too.",
            1: "3.15 times 12 equals 37.8. That does not work, because you can't have 0.8 of an article.",
        },
    },
    "EXT_G5_FP_2018_032": {
        "q": "A three-digit number, blank, blank, 7, is multiplied by a two-digit number, blank 8. The digits in the blank places are not necessarily the same. Which of the following can be the product of the given two numbers?",
        "steps": {
            0: "Last digit: 7 times 8 equals 56, so it ends in 6. That removes 29405, which ends in 5.",
            1: "1906 is smaller than the smallest possible product, 1926. So it does not work.",
            2: "977706 is bigger than the largest possible product, 97,706. So it does not work.",
            3: "Only 52606 is left, and it works. It equals 58 times 907.",
        },
    },
    "EXT_G5_FP_2019_003": {
        "steps": {2: "The 1st is 0.56 and the 4th is 0.034."},
    },
    "EXT_G5_FP_2019_026": {
        "hints": {1: "Order: round brackets, then curly brackets. And inside brackets, multiplication before addition."},
    },
    "EXT_G5_FP_2020_006": {
        "hints": {1: "BODMAS: B, then multiplication before addition and subtraction."},
        "steps": {4: "The greatest is, open bracket, 10 plus 3, close bracket, times 3."},
    },
    "EXT_G5_FP_2021_030": {
        "steps": {
            0: "87 times 156 equals 13572. That is 87 times 150 equals 13050, and 87 times 6 equals 522.",
            2: "So 13601 divided by 87 equals 156, remainder 29. Subtract 29.",
        },
    },
    "EXT_G5_FP_2022_017": {
        "q": "Solve: 5 over 6 of 72, minus 2 times, open square bracket, 2 over 5 of 40, plus 1 over 9 of 27, close square bracket.",
        "steps": {1: "2 over 5 of 40 equals 16, and 1 over 9 of 27 equals 3. So the bracket equals 16 plus 3, which is 19."},
    },
    "EXT_G5_FP_2022_021": {
        "hints": {0: "Without brackets the answer is a big negative number. A bracket around a subtraction can make the divisor smaller. Try brackets around 21 minus 9."},
    },
    "EXT_G5_FP_2022_023": {
        "q": "A two-digit number, blank 8, is multiplied by a three-digit number, blank, blank, 6. Which of the following can be their product, if blank represents a digit, not necessarily the same?",
        "steps": {
            0: "Last digit: 8 times 6 equals 48, so it ends in 8. That removes 79764, which ends in 4.",
            1: "1808 is smaller than the smallest possible product, 1908. So it does not work.",
            2: "970608 is bigger than the largest possible product, 97,608. So it does not work.",
            3: "Only 50808 is left, and it works. It equals 58 times 876.",
        },
    },
    "EXT_G5_FP_2022_024": {
        "hints": {
            0: "How did each number change? 6.7 to 0.67 is divided by 10, and 58 to 5.8 is divided by 10. So how does the answer change?",
            1: "Dividing two factors by 10 each divides the product by 10 times 10, which is 100.",
        },
    },
    "EXT_G5_FP_2023_001": {
        "hints": {
            0: "Add column by column. Notice every column has the same four digits, 1, 2, 3, 4. What does each column add up to?",
            1: "Each column: 4 plus 1 plus 2 plus 3 equals 10, in some order.",
        },
        "steps": {0: "Every column adds to 1 plus 2 plus 3 plus 4, which is 10."},
    },
    "EXT_G5_FP_2023_005": {
        "q": "What is the value of: open bracket, 1 times 2 times 3, times 4 times 5 times 6, times 7, close bracket, divided by, open bracket, 1 plus 2 plus 3, plus 4 plus 5 plus 6, plus 7 plus 8, close bracket?",
        "hints": {0: "Work out the top, multiply, and the bottom, add, separately. The bottom is 1 plus 2 plus, and so on, up to 8. Use pairs to add quickly."},
        "steps": {1: "Bottom: 1 plus 2 plus, and so on, up to 8, equals 8 times 9 divided by 2, which is 36."},
    },
    "EXT_G5_FP_2023_015": {
        "q": "Simplify using BODMAS rule: open bracket, 9, plus 3 over 5 of 25, minus 7 over 13 of 39, close bracket, divided by 4 over 3.",
        "hints": {0: "'Of' means multiply. Do both 'of' parts first inside the bracket, then add and subtract, then divide by 4 over 3, which means multiply by 3 over 4."},
        "steps": {
            0: "3 over 5 of 25 equals 15, and 7 over 13 of 39 equals 21.",
            2: "3 divided by 4 over 3, equals 3 times 3 over 4, that is 9 over 4, which is 2.25.",
        },
    },
    "EXT_G5_FP_2023_018": {
        "q": "What fraction of a day is 216 minutes, as a decimal?",
        "hints": {0: "A day has 24 times 60, which is 1440 minutes. Divide 216 by 1440."},
        "steps": {1: "216 over 1440 equals 3 over 20, dividing by 72."},
    },
    "EXT_G5_FP_2023_020": {
        "hints": {0: "Add 3042 and 869 first. Then: that sum, minus the number, equals 2165. So the number equals the sum minus 2165."},
        "steps": {1: "3911 minus what number equals 2165? So the number equals 3911 minus 2165."},
    },
    "EXT_G5_FP_2023_030": {
        "q": "Given that 168 times 54 equals 9072, then find the value of 0.9072 divided by 16.8.",
    },
    "EXT_G5_FP_2023_037": {
        "hints": {0: "Without brackets: 42 divided by 7 times 2, plus 16, equals 12 plus 16, which is 28. To reach 19 the division must give a smaller answer. Try bracketing 7 times 2."},
        "steps": {2: "The others don't work: brackets around 2 plus 16 gives 42 divided by 7 times 18, which is 108. " + _NOT},
    },
    "EXT_G5_FP_2024_003": {
        "hints": {0: "No brackets or powers here. Do all the divisions and multiplications first, going left to right. Then do addition and subtraction, left to right."},
    },
    "EXT_G5_FP_2024_027": {
        "hints": {1: "867 divided by 68 equals 12.75, from the given fact. Dividing the top by 100 and the bottom by 10 changes the answer by dividing by 10."},
    },
    "EXT_G5_FP_2024_036": {
        "q": "Which set of signs of operation should be replaced in the boxes so that the equation is true: 12, blank, 6, blank, 3, blank, 14, equals 16?",
    },
    "EXT_G5_FP_2025_004": {
        "hints": {1: "Remainder equals Dividend minus, open bracket, Divisor times whole-number quotient, close bracket."},
    },
    "EXT_G5_FP_2025_019": {
        "hints": {0: "Group the numbers with a plus together, and the numbers with a minus together. Then subtract one total from the other."},
    },
    "EXT_G5_FP_2025_023": {
        "hints": {1: "B first, then D and M left to right, then A and S left to right."},
    },
    "EXT_G5_FP_2025_030": {
        "hints": {1: "Decimal places in the answer equals total decimal places in the numbers multiplied. 1 plus 1 equals 2."},
        "steps": {0: "72 times 39 equals 2808. With 2 decimal places, that is 28.08."},
    },
    "EXT_G5_FP_2025_033": {
        "q": "A three-digit number, blank, blank, 7, is multiplied by a three-digit number, blank, blank, 6. Which of the following can be their product, if blank represents a digit, not necessarily the same?",
        "steps": {
            0: "Ones digit: 7 times 6 equals 42, so the product ends in 2. That removes 457647, which ends in 7.",
            1: "Smallest possible equals 107 times 106, which is 11342, so 11332 is too small.",
            2: "Largest possible equals 997 times 996, which is 993012, so 994312 is too big.",
            3: "Only 353362 is left, and it works. It equals 547 times 646.",
        },
    },
    "EXT_G5_FP_2025_035": {
        "steps": {0: "Option B: 192 divided by 36, minus 4 plus 13, equals 5.33 and so on, minus 4 plus 13. " + _NOT},
    },
}
