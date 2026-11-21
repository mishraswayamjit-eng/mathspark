"""Hand-written narration for gr4_numbers. None means: use the rules for that line.

HAND is keyed by question id; LINES is keyed by the printed line (for lines shared by several questions).

The hints and steps of the questions listed in data/bank-import/g4/renarrate.json were rewritten in
the bank; their new hand lines are in gr4_numbers_hand3.py, and only question and option lines for
those ids are kept here.
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
    },
    "Q_CH01_003": {
        "q": "Which is the largest: 45,032, 45,302, 45,320, or 45,203?",
    },
    "Q_CH01_009": {
        "options": ["5,342, then 5,234, then 5,423, then 5,432",
                    "5,234, then 5,342, then 5,432, then 5,423",
                    "5,234, then 5,342, then 5,423, then 5,432",
                    "5,432, then 5,423, then 5,342, then 5,234"],
    },
    "Q_CH01_025": {
        "q": "Fill in the blank: 65,432, blank, 65,342.",
        "options": ["is less than", N, "is equal to", "is greater than"],
        "steps": [N, N, "So 65,432 is greater than 65,342. The sign is the greater than sign."],
    },
}

LINES = {}
