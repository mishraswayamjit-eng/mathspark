"""Hand-written narration for gr4_operations, where the rules do not give a line worth hearing.

HAND: question id -> {"q": ..., "options": [...], "hints": [...], "steps": [...]}; None keeps the rule's line.
LINES: a printed line (exactly as in the bank) -> its spoken form, wherever it appears.
"""

LINES = {
    "Selling price = Cost price + Profit.": "Selling price equals cost price plus profit.",
    "Selling price = Cost price − Loss.": "Selling price equals cost price minus loss.",
    "The signs + × − make the sum equal 20.": "The signs plus, times and minus make the sum equal 20.",
}

HAND = {
    # The hidden digits are printed as stars inside brackets.
    "PYQ_2016_Q32": {
        "q": "Which of the following can be the product of star, star, 7 and star, star, 8, where star denotes digits, not necessarily the same?",
    },
    "PYQ_2017_Q09": {
        "q": "Where should the bracket be put to make the following equation true: 5 times 7 plus 3 minus 10 equals 40?",
        # Rewritten help (Nov 2026): "to make 4 × 6 + 2 − 5 = 27 true?" reads badly word for word.
        "hints": [None, None,
                  "Here is a similar one: where should the bracket go to make it true that 4 times 6 plus 2 minus 5 equals 27? "
                  "Without a bracket the left side is 24 plus 2 minus 5, which is 21. "
                  "With a bracket around 6 plus 2 it becomes 4 times 8 minus 5, and 32 minus 5 equals 27. "
                  "So the bracket goes around 6 plus 2."],
    },
    "PYQ_2018_Q07": {
        "q": "Which of the following can be the product of star, star, 8 and star, star, 7, where star denotes digits, not necessarily the same?",
    },
    "PYQ_2019_Q32": {
        "q": "Which of the following can be the product of star, star, 7 and star, star, 6, where star denotes digits, not necessarily the same?",
        "hints": [None, None,
                  "Here is a similar one. The product of star, 3 and star, 4 must end in 2, because 3 times 4 equals 12. "
                  "Two 2-digit numbers give a product from 10 times 10, which is 100, up to 99 times 99, which is 9801. "
                  "So 1472 could be the product, but 1475 could not."],
    },
    "PYQ_2018_Q23": {
        "hints": [None, None,
                  "Here is a similar one. A hall has rows A to J, which is 10 rows, with 12 seats each. "
                  "That is 10 times 12, which is 120 seats. If 2 seats are empty in each of rows A to E, "
                  "that is 5 times 2, which is 10 empty seats. So 120 minus 10, which is 110 people, are seated."],
    },
    "G4A_OPERATIONS_015": {
        "steps": [None, None,
                  "The other two choices give 12 divided by 6 plus 2, which is 4, and 12 minus 6 plus 2, which is 8.",
                  None],
    },
    "G4A_OPERATIONS_021": {
        "q": "Which sign must go in the box to make this true? 6 plus 12, box, 3 times 2, equals 12. "
             "The usual order of operations is followed.",
        "steps": [None, None,
                  "The other two signs give 6 plus 12 plus 6, which is 24, and 6 plus 72, which is 78.",
                  "The sign in the box must be minus, the subtract sign."],
    },
    "Q_CH09_009": {
        "q": "35 times 12 equals 35 times 10, plus 35 times what?",
        "hints": [None, None,
                  "Here is a similar one: 24 times 15 equals 24 times 10, plus 24 times what? "
                  "15 is 10 and 5 more, so the missing number is 5."],
        "steps": [None, None,
                  "So 12 lots of 35 is 10 lots of 35 plus 2 lots of 35. 35 times 12 equals 35 times 10, plus 35 times 2.",
                  None],
    },
    "Q_CH09_013": {
        "q": "Open bracket, 12 times 5, close bracket, times 4, equals 12 times open bracket, 5 times what, close bracket?",
    },
    "EXT_G4_FP_2022_032": {
        "hints": [None, None,
                  "Here is a similar one. Is it true that 5 times 5 plus 6 equals 4 times 4 plus 5 times 3? "
                  "The left side is 25 plus 6, which is 31. The right side is 16 plus 15, which is 31. "
                  "Both sides are 31, so it is true."],
    },
    "Q_CH09_010": {
        "hints": [None, None,
                  "Here is a similar one: 143 times 27 equals 27 times what? "
                  "Swapping the order does not change the product, so the missing number is 143."],
    },
    "Q_CH09_014": {
        "options": [None, None, "Open bracket, 8 plus 4 times 3, close bracket", None],
    },
    "Q_CH09_025": {
        "q": "If 7 times a missing number equals 91, then what is the missing number?",
        "hints": [None, None,
                  "Here is a similar one: 8 times a missing number equals 120. Divide 120 by 8. "
                  "80 divided by 8 equals 10 and 40 divided by 8 equals 5, so the missing number is 10 plus 5, which is 15."],
    },
}
