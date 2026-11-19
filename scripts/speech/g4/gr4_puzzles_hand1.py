"""Hand-written narration for gr4_puzzles. HAND[question id][part] is text, or {index: text} for lists."""

HAND = {
    "EXT_G4_FP_2020_001": {
        "q": "25 trays. Each has a cup only, or a plate only, or both. 15 have cups, 21 have plates. How many have both?",
    },
    "EXT_G4_FP_2020_010": {
        "q": "Teacher's 3-digit odd number. The hundreds digit is greater than 8. The tens digit is 4 more than the ones. What is the sum of the digits?",
    },
    "EXT_G4_FP_2020_011": {
        "q": "A 5-digit number, 213 a b, leaves a remainder less than 10 when divided by 100. The sum of all its digits equals 13. Find b.",
    },
    "EXT_G4_FP_2021_006": {
        "q": "The product of blank blank 7, and blank blank 8, where the blanks are not the same?",
    },
    "EXT_G4_FP_2021_034": {
        # The checker reads the printed "64,100,A" as the one number 64100, so no pause is allowed after 64.
        "q": "Magic square. Top row: 4, 5, 7. Middle row: 2, 2, 2. Bottom row: 64,100, A. Find A.",
    },
    "EXT_G4_FP_2022_005": {
        "q": "A 2-digit number times a 3-digit number: star 8, times star star 7. Which can be the product?",
    },
    "EXT_G4_FP_2023_007": {
        "q": "Which of the following can be the product of star star 6, and star 9, where star denotes digits, not necessarily the same?",
    },
    "EXT_G4_FP_2024_015": {
        "q": "Magic square. Top row: n, blank, 6. Middle row: 4, x, m. Bottom row: 16, blank, blank. Find m plus n.",
        "steps": {2: "In a 3 by 3 magic square, each line adds up to 3 times the middle number. The diagonal is 22 plus x, so 22 is 2 times x. That makes x equal to 11, and each line adds up to 33."},
    },
    "EXT_G4_FP_2024_018": {
        "q": "The product of star star 8, and star 6, where the stars are not the same?",
    },
    "EXT_G4_FP_2024_035": {
        "q": "A queue of 63 students. You are 13th from the beginning, and your friend is 19th from the end. How many students are between you?",
    },
    "EXT_G4_FP_2025_021": {
        "q": "The product of star star 4, and star star 8, where the stars are not the same?",
    },
    "Q_CH15_003": {
        "hints": {1: "Magic constant equals 3 times centre. So total equals 3 times, 3 times centre, which is 9 times centre."},
    },
    "Q_CH15_011": {
        "hints": {1: "Column 1: 4 plus 3 equals 7, and 7 squared equals 49. Column 2: 6 plus 4 equals 10, and 10 squared equals 100. Check: is the 3rd row equal to row 1 plus row 2, all squared?"},
        "steps": {
            0: "Find the pattern. Row 3 equals Row 1 plus Row 2, all squared.",
            1: "Check column 2: 6 plus 4, all squared, equals 10 squared, which is 100.",
            2: "Column 3: 8 plus what number, all squared, equals 169. The square root of 169 equals 13. So 8 plus the missing number equals 13.",
        },
    },
    "Q_CH15_013": {
        "hints": {
            1: "Row 1: 3, 4, 25. Is 25 equal to 3 squared plus 4 squared? 9 plus 16 equals 25! Row 2: 5 squared plus 7 squared? No. 25 plus 49 equals 74, not 71. Try: 3 times 4 times 2 plus 1 equals 25. 5 times 7 times 2 plus 1 equals 71!",
            2: "Pattern: column 3 equals column 1 times column 2, times 2, plus 1. So the missing number equals 6 times 8 times 2 plus 1, which is 97.",
        },
    },
    "Q_CH15_014": {
        "steps": {
            0: "Pattern: the result is a minus b, joined with a plus b.",
            1: "Check: 9 minus 1, joined with 9 plus 1, gives 8 and 10, which makes 810.",
            2: "Apply: 5 minus 4, joined with 5 plus 4, gives 1 and 9, which makes 19.",
        },
    },
    "Q_CH15_020": {
        "q": "If blue, blue, blue equals red, red, and red equals green, green, green, then blue, blue, blue equals how many greens?",
        "steps": {0: "3 B equals 2 R, and R equals 3 G."},
    },
    "Q_CH15_022": {
        "hints": {2: "Sum of each line equals 25 plus 5, divided by 2, which is 15. Line with 1: 1 plus 5 plus what number equals 15. So the missing number equals 9."},
        "steps": {1: "Each line equals total plus centre, divided by 2. That is 25 plus 5, over 2, which is 15."},
    },
    "Q_CH15_024": {
        "hints": {
            0: "Add all three equations together: A plus B, plus B plus C, plus A plus C, equals 10 plus 15 plus 11.",
            1: "Left side: 2 A plus 2 B plus 2 C equals 36. So 2 times, A plus B plus C, equals 36.",
        },
        "steps": {
            0: "Add all three equations. A plus B, plus B plus C, plus A plus C, equals 10 plus 15 plus 11, which is 36.",
            1: "Left side equals 2 A plus 2 B plus 2 C, which is 2 times, A plus B plus C.",
        },
    },
    "Q_CH15_025": {
        "hints": {2: "The centre of a magic square with consecutive numbers is always the middle number, which is 13."},
    },
}

LINES = {}
