"""Hand-written narration for gr4_ratio, where the rules do not give a line worth hearing.

HAND is keyed by question id; a None in a list means "leave this line to the rules".
"""

HAND = {
    "G4A_RATIO_035": {
        "q": "A piggy bank holds only 1 rupee, 2 rupee and 5 rupee coins. The numbers of 1 rupee, 2 rupee and 5 rupee coins "
             "are in the ratio 3 is to 2 is to 1. The coins are worth 96 rupees altogether. How many 5 rupee coins are there?",
        "hints": [None, None,
                  "A similar one: 1 rupee and 5 rupee coins in the ratio 2 is to 1 are worth 35 rupees. "
                  "One group of 2 one-rupee coins and 1 five-rupee coin is worth 7 rupees, "
                  "so there are 35 divided by 7, which is 5 groups, and 5 five-rupee coins."],
        "steps": ["Take one group: 3 coins of 1 rupee, 2 coins of 2 rupees and 1 coin of 5 rupees. Find its value. "
                  "3 times 1, plus 2 times 2, plus 1 times 5, equals 12."],
    },
    "G4A_RATIO_044": {
        "steps": ["The total is a multiple of 3 plus 4, which is 7. Between 40 and 50, the multiples of 7 are 42 and 49."],
    },
}

LINES = {}
