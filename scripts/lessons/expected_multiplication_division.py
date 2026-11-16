# -*- coding: utf-8 -*-
"""Expected computations for the 'multiplication-division' lesson quiz.

See expected_addition_subtraction.py for the format. `%` is the remainder and
`//` the whole-number quotient.
"""

EXPECT = {
    # Level 1: multiplying big numbers
    "md-l1-q1": "234 * 6",
    "md-l1-q2": "58 * 100",
    "md-l1-q3": "60 * 700",
    "md-l1-q4": "37 * 24",
    "md-l1-q5": "144 * 25",
    "md-l1-q6": "485 * 6",
    "md-l1-q7": "4 * 39 * 25",
    "md-l1-q8": "125 * 48",
    # Level 2: dividing big numbers
    "md-l2-q1": "72 / 8",
    "md-l2-q2": "852 / 4",
    "md-l2-q3": "36000 / 900",
    "md-l2-q4": "47 % 6",
    "md-l2-q5": "1296 / 8",
    "md-l2-q6": "230 % 45",
    "md-l2-q7": "1344 / 32",
    "md-l2-q8": "7035 / 7",
    # Level 3: dividend = divisor x quotient + remainder
    "md-l3-q1": "59 - 7 * 8",
    "md-l3-q2": ("15 - 1", "1"),
    "md-l3-q3": "9 * 12 + 4",
    "md-l3-q4": "25 * 16 + 9",
    "md-l3-q5": "18 * 24 + 7",
    "md-l3-q6": "365 % 12",
    "md-l3-q7": "(2000 - 57) / 29",
    "md-l3-q8": "(1000 - 11) / 23",
    # Level 4: shortcuts and patterns
    "md-l4-q1": "8 * 99",
    "md-l4-q2": "84 * 5",
    "md-l4-q3": "44 * 25",
    "md-l4-q4": "36 * 999",
    "md-l4-q5": "98 * 15",
    "md-l4-q6": "25 * 48",
    # last digit = remainder on dividing by 10
    "md-l4-q7": ("(47 * 68) % 10", "10"),
    "md-l4-q8": ("(123 * 457 * 9) % 10", "10"),
    # Level 5: exam twists
    "md-l5-q1": "50 % 6",
    "md-l5-q2": "6 - 50 % 6",
    "md-l5-q3": "500 % 23",
    "md-l5-q4": "(2 + 4) % 5",
    "md-l5-q5": "104 / 4 * 3",
    # minutes in a week = 60 x 24 x 7
    "md-l5-q6": ("(8 * 7 * 6 * 5 * 4 * 3 * 2 * 1) / (60 * 24 * 7)", "60 24"),
    "md-l5-q7": "13601 % 87",
    "md-l5-q8": "(1 * 3 * 5 * 7 * 9) % 18",
}

ALLOW = {}
