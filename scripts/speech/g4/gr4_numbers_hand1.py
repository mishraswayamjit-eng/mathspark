"""Hand-written narration for gr4_numbers. None means: use the rules for that line.

HAND is keyed by question id; LINES is keyed by the printed line (for lines shared by several questions).
"""

N = None

HAND = {
    "EXT_G4_FP_2021_031": {
        "q": "Number 6, star, 74, star, 3: difference between the place values of star. Star is the same digit.",
        "hints": [N, N, "Here is a similar one. In 5, star, 3, star, let the star be 4. The stars are in the hundreds and ones places, so the place values are 400 and 4. The difference is 400 minus 4, which is 396."],
        "steps": ["Find the places of the two stars in 6, star, 74, star, 3. From the right, one star is in the tens place and the other is in the ten-thousands place."],
    },
    "G4A_NUMBERS_017": {
        "hints": [N,
                  "Numbers like 4, 9, 40 and 90 use a short subtraction form: I V, I X, X L, and X C. Numbers with 3 and 8 use the most symbols.",
                  "Similar problem: among 19, 28 and 30, write X I X, with 3 symbols, X X V I I I, with 6 symbols, and X X X, with 3 symbols. So 28 needs the most symbols."],
    },
    "PYQ_2017_Q02": {
        "q": "The number T U is a two digit number, with units digit U and tens digit T. The digits M and N are distinct and non zero. What is the largest possible value of M N minus N M?",
    },
    "PYQ_2018_Q03": {
        "q": "Given that m is an even integer and n is an odd integer, which of the following is an odd integer?",
        "options": ["3 m plus 4 n", "m plus 3 n", "5 m plus 6 n", "5 m n"],
        "steps": ["Correct answer: option 2, m plus 3 n."],
    },
    "Q_CH01_001": {
        "hints": ["Find which place 6 is in. Count from the right: 9 ones, 8 tens, 4 hundreds, 2 thousands, 6 ten-thousands."],
    },
    "Q_CH01_002": {
        "hints": ["Successor means the next number. Add 1."],
        "steps": ["Successor equals the number plus 1."],
    },
    "Q_CH01_003": {
        "q": "Which is the largest: 45,032, 45,302, 45,320, or 45,203?",
        "hints": ["All start with 45. Compare the hundreds digit: 0, 3, 3, 2.",
                  "Two have 3 in the hundreds: 45,302 and 45,320. Compare the tens: 0 versus 2."],
        "steps": ["Compare digit by digit, from the left."],
    },
    "Q_CH01_004": {
        "hints": ["Break it down. C D equals 400: D equals 500, and C before D means 500 minus 100. X L equals 40: L equals 50, and X before L means 50 minus 10. I V equals 4."],
    },
    "Q_CH01_005": {
        "hints": [N, "700 equals D C C, which is 500 plus 100 plus 100. 80 equals L X X X, which is 50 plus 10 plus 10 plus 10. 9 equals I X, which is 10 minus 1."],
    },
    "Q_CH01_006": {
        "hints": [N, "6 is greater than or equal to 5, so round up: 4,500 becomes 4,600."],
        "steps": ["The tens digit is 6, which is greater than or equal to 5, so round up."],
    },
    "Q_CH01_007": {
        "hints": [N,
                  "Count digit by digit: 5, 4, 3, 2, 1, 6, 7, 8. Wait, that's only 8. Let me recount: 5,43,21,678 equals 54321678. That's 8 digits.",
                  "Actually: 5, 43, 21, 678 gives 5,43,21,678, which is 5 crore 43 lakh 21 thousand 678. That is 54321678, which has 8 digits. Hmm, but with the comma pattern shown, it could be 9 digits: 5,43,21,678 in the Indian system, with one initial digit. Let me check: 5 crore is 5,00,00,000, which has 8 digits. Is 5,43,21,678 9 digits? No: 5 crore 43 lakh 21 thousand 678 is 5,43,21,678. Count: 5, 4, 3, 2, 1, 6, 7, 8. That is 8 digits."],
        "steps": [N, "Count the digits: 5, 4, 3, 2, 1, 6, 7, 8. That is 8 digits."],
    },
    "Q_CH01_008": {
        "steps": ["3 times 10000, plus 0 times 1000, plus 5 times 100, plus 0 times 10, plus 7 times 1. That is 30000 plus 0 plus 500 plus 0 plus 7."],
    },
    "Q_CH01_009": {
        "options": ["5,342, then 5,234, then 5,423, then 5,432",
                    "5,234, then 5,342, then 5,432, then 5,423",
                    "5,234, then 5,342, then 5,423, then 5,432",
                    "5,432, then 5,423, then 5,342, then 5,234"],
        "hints": ["Ascending means smallest to largest. All start with 5, so compare the hundreds digit.",
                  "Hundreds: 2, 3, 4, 4. Then the tens, for the two with 4: 2 versus 3."],
    },
    "Q_CH01_013": {
        "hints": ["V, which is 5, cannot come before X, which is 10, to subtract. Only I, X and C can be subtracted.",
                  "V, L and D are never subtracted. They can't appear before a larger numeral."],
        "steps": ["Rule: V, L and D cannot be used for subtraction."],
    },
    "Q_CH01_017": {
        "hints": ["Smallest number: put the smallest digit first. But the first digit can't be 0!",
                  "The smallest non-zero digit is 1. Then arrange the rest in ascending order: 0, 3, 7, 9."],
        "steps": ["First digit: the smallest non-zero digit, which is 1."],
    },
    "Q_CH01_019": {
        "steps": ["The smallest 6-digit number is 100000, which is 1 lakh."],
    },
    "Q_CH01_025": {
        "q": "Fill in the blank: 65,432, blank, 65,342.",
        "options": ["is less than", N, "is equal to", "is greater than"],
        "steps": [N, N, "So 65,432 is greater than 65,342. The sign is the greater than sign."],
    },
    "Q_CH01_028": {
        "hints": ["Even number means the last digit must be even. The only even digit available is 8.",
                  "Wait, but if 8 is in the ones place, the remaining digits are 5, 3, 1. The largest is 531, then a blank. 5318.",
                  "Actually: we need the largest number. Start with 8, the largest. But must 8 be in the ones place for even? No, 8 can be the first digit if another even digit is last. The only even digit is 8. So 8 must be the last digit. Remaining: 5, 3, 1. Largest first is 5, 3, 1, which gives 5318. But option C is 8538, which uses 8 twice. Since each digit is used once and only 8 is even, the answer is 5,318. Wait, let me recheck the options. Actually, with digits 5, 3, 8, 1: even means the last digit is 8. The remaining 5, 3, 1 in descending order make 531. The number is 5318. That's option D. Hmm, but option C has 8538, which repeats 8. Let me pick D."],
        "steps": ["Even means the last digit must be 8, the only even digit.",
                  "The remaining digits 5, 3, 1 in descending order: 5, 3, 1."],
    },
    "Q_CH01_029": {
        "hints": [N, "42 in Roman numerals: 40 is X L, and 2 is I I."],
    },
}

LINES = {}
