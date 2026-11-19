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
    "PYQ_2018_Q33": {
        "hints": {2: "Here is a similar one: a three-digit palindrome is added to 1009 to make a four-digit palindrome. Try a total that begins and ends with 1. Since 9 plus 2 equals 11, which ends in 1, the palindrome looks like 2, star, 2. Trying the middle digit, 212 plus 1009 equals 1221, which reads the same backwards. The digits of 212 add up to 2 plus 1 plus 2, which is 5."},
        "steps": {
            0: "A three-digit number added to 2018 gives a total between 2119 and 3017. The only palindrome there that begins with 3 is 3003, and 3003 minus 2018 equals 985, which is not a palindrome. So the total begins with 2 and ends in 2.",
            1: "Look at the ones digits. 2018 ends in 8, and 8 plus 4 equals 12, which ends in 2, so the three-digit palindrome ends in 4. It starts with the same digit, so it looks like 4, star, 4.",
            2: "Now try the middle digit. 404 plus 2018 equals 2422, and 414 plus 2018 equals 2432. These are not palindromes. But 424 plus 2018 equals 2442, which is.",
            3: "The three-digit palindrome is 424. Its digits add up to 4 plus 2 plus 4, which is 10, so the answer is 10.",
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
}

LINES = {}
