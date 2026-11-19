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
    # Rewritten help (November 2026): only the lines the rules read badly.
    "PYQ_2019_Q09": {
        "steps": [None, None,
                  "From 7 over 15 to 14 over 45, the top was doubled but the bottom was multiplied by 3. "
                  "Doubling both gives 7 over 15 equals 14 over 30, not 14 over 45."],
    },
    "Q_CH07_001": {
        "steps": [None,
                  "In 1 over 2, 1 over 3 and 1 over 4, the tops match, but the bottoms are 2, 3 and 4. "
                  "The groups 2 over 3, 4 over 5, 1 over 6, and 3 over 7, 5 over 9, 2 over 11, have different bottoms as well."],
    },
}

LINES = {}
