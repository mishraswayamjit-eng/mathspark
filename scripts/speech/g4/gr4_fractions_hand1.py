"""Hand-written narration for gr4_fractions, where the rules do not give a line worth hearing.

HAND is keyed by question id; a None in a list means "leave this line to the rules".
LINES is keyed by the printed line, for terse lines that repeat across questions.
"""

HAND = {
    "EXT_G4_FP_2020_002": {
        "q": "1 over 9, plus 1 over 18, equals 1 over box. Find the number in the box.",
    },
    "EXT_G4_FP_2021_002": {
        "q": "Find the star. 2 over 7, plus 2 over 7, plus 2 over 7, equals star over 21.",
    },
    "EXT_G4_FP_2022_004": {
        "q": "Work out 12 over 19, plus 1 and 11 over 19, minus 16 over 19.",
    },
    "EXT_G4_FP_2022_006": {
        "q": "If W, X, Y and Z are all equal, find the smallest fraction: W over 23, Y over 29, X over 17, or Z over 13.",
    },
    "EXT_G4_FP_2024_005": {
        "q": "If M, N, Q and P are all equal, find the greatest fraction: M over 12, P over 10, Q over 7, or N over 8.",
    },
    "EXT_G4_FP_2023_014": {
        "q": "Which same number, M, can go in each place? M over 14, plus M over 14, plus M over 14, equals 162 over 126.",
    },
    "EXT_G4_FP_2025_039": {
        "q": "Three fractions have the same denominator. Their numerators are 5, 8 and 11. Their sum is 2. What is the denominator?",
    },
    "G4A_FRACTIONS_011": {
        "q": "Twelve beads are threaded on a string in this order: R, R, B, G, R, B, B, R, G, R, B, R. Here R is a red bead, B is a blue bead and G is a green bead. What fraction of the beads are blue, in lowest terms?",
    },
    "G4A_FRACTIONS_006": {
        "steps": [None, None,
                  "From longest to shortest: 3 over 4 for Bala, 3 over 5 for Asha, 3 over 7 for Dev, and 3 over 10 for Chitra."],
    },
    "Q_CH07_001": {
        "hints": [None, "Option A: all have denominator 5.", "Options B, C and D all have different denominators."],
        "steps": ["Option A: all have denominator 5."],
    },
    "Q_CH07_004": {
        "hints": ["Multiply the whole number by the denominator, then add the numerator.",
                  "3 times 5, plus 2, equals 17. Keep the denominator.",
                  "That gives 17 over 5."],
        "steps": ["3 times 5, plus 2, equals 17. Keep the denominator."],
    },
    "Q_CH07_005": {
        "hints": ["23 divided by 4 equals 5, remainder 3.",
                  "That gives 5 and three quarters.",
                  "Check: 5 times 4, plus 3, equals 23."],
        "steps": ["That gives 5 and three quarters."],
    },
    "Q_CH07_006": {
        "hints": ["The denominators are the same, so add the numerators. 3 plus 5 equals 8.", None,
                  "The answer is 1, which is also 8 over 8."],
    },
    "Q_CH07_007": {
        "hints": ["Find the L C M of 3 and 4, which is 12.",
                  "1 over 3 equals 4 over 12. 1 over 4 equals 3 over 12. The sum is 7 over 12.", None],
        "steps": ["1 over 3 equals 4 over 12. 1 over 4 equals 3 over 12. The sum is 7 over 12."],
    },
    "Q_CH07_008": {
        "hints": ["The L C M of 6 and 3 is 6. 1 over 3 equals 2 over 6.", None, None],
    },
    "Q_CH07_014": {
        "hints": ["The L C M of 3, 4, 6 and 2 is 12. Convert: 8 over 12, 9 over 12, 10 over 12 and 6 over 12.",
                  "In ascending order: 6 over 12, then 8 over 12, then 9 over 12, then 10 over 12.",
                  "That is 1 over 2, 2 over 3, 3 over 4 and 5 over 6."],
        "steps": ["In ascending order: 6 over 12, then 8 over 12, then 9 over 12, then 10 over 12.",
                  "The answer is A."],
    },
}

LINES = {
    "Same denominator → compare numerators.": "The denominators are the same, so compare the numerators.",
    "Largest numerator = 6.": "The largest numerator is 6.",
    "Same numerator → LARGER denominator = SMALLER fraction.": "The numerators are the same, so the larger denominator gives the smaller fraction.",
    "Largest denominator = 8.": "The largest denominator is 8.",
}
