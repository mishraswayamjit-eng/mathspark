# -*- coding: utf-8 -*-
"""Expected computations for the 'algebraic-expressions' lesson quiz.

See expected_addition_subtraction.py for the format. Each expression is the
question worked out with the letters already replaced by their numbers.
"""

EXPECT = {
    # Level 1: variables, terms, coefficients, constants
    "ae-l1-q1": "9",
    "ae-l1-q2": ("1 + 1 + 1", "1"),            # terms 3x, 4y, 7
    "ae-l1-q3": "11",
    "ae-l1-q4": ("1", "1"),                    # y = 1y
    "ae-l1-q5": "4",
    "ae-l1-q6": "6 * 3",
    "ae-l1-q7": ("1 + 1 + 1 + 1 + 1", "1"),    # terms 5x, 2y, 3x, 8, y
    "ae-l1-q8": "2 + 9 + 4",
    # Level 2: substitution
    "ae-l2-q1": "4 * 5 + 3",
    "ae-l2-q2": "20 - 3 * 4",
    "ae-l2-q3": "3 * 4 + 2 * 5",
    "ae-l2-q4": "7 * 3 + 6",
    "ae-l2-q5": "5 * 30 + 2 * 10",
    "ae-l2-q6": "2 * 12 + 2 * 7",
    # x = 7, y = 7 - 2, p = y + 5; then (p + x) * y
    "ae-l2-q7": "((7 - 2 + 5) + 7) * (7 - 2)",
    "ae-l2-q8": ("6 ** 2 + 3 * 6 - 4", "2"),   # the 2 is the square
    # Level 3: like terms
    "ae-l3-q1": "3 + 6",
    "ae-l3-q2": "10 - 4",
    "ae-l3-q3": ("5 + 1 + 2", "1"),            # x = 1x
    "ae-l3-q4": "7 + 3",
    "ae-l3-q5": "(4 + 5) * 6",
    "ae-l3-q6": ("4 + 1", "1"),                # y = 1y
    "ae-l3-q7": "5 - 3 + 4",
    "ae-l3-q8": "1 - 1 + 1",                   # constants: -1, +1, +1
    # Level 4: words to expressions
    "ae-l4-q1": "12 + 8",
    "ae-l4-q2": "2 * 10 - 3",
    "ae-l4-q3": ("3 * 4 + 5", "3"),            # "three times"
    "ae-l4-q4": ("2 * (4 + 5)", "2"),          # "twice"
    "ae-l4-q5": "5 * 6 + 4 * 10",
    "ae-l4-q6": "3 * 25 + 12 * 5",
    "ae-l4-q7": "(16 - 2) / 2",
    "ae-l4-q8": ("(48 - 1 - 2) / 3", "3"),     # "three numbers"
    # Level 5: multiply, divide, test
    "ae-l5-q1": "5 * 3",
    "ae-l5-q2": "3 * 4",
    "ae-l5-q3": "20 / 5",
    "ae-l5-q4": "10 / 5",
    "ae-l5-q5": "4 * 9 - 2",
    "ae-l5-q6": "(6 * 20 + 9) / 3",
    "ae-l5-q7": "12 * 6 - 14",
    "ae-l5-q8": "4 * (2 * 7 - 9) - 2 * 7",
}

# Sentences that state an equation to be solved, or a claim the equality
# reader cannot see. Each carries its own proof with the numbers put in.
ALLOW = {
    # n = 7 solves it: 7 and 9 are odd numbers in a row and add up to 16
    "The sum of two odd numbers in a row is 16. If the smaller one is n, then n + (n + 2) = 16. What is n?":
        ["7 + (7 + 2) == 16", "7 % 2 == 1"],
    # the question says the two expressions agree when x is 6
    "When x is 6, the value of 12x − 14 is the same as the value of 7x + 16. What is that value?":
        ["12 * 6 - 14 == 7 * 6 + 16"],
    # n = 15 solves the three-in-a-row question (no '=' in it, so proved here)
    "Three numbers in a row add up to 48. If the smallest is n, the sum is n + (n + 1) + (n + 2). What is n?":
        ["15 + (15 + 1) + (15 + 2) == 48"],
    # the like-term questions: the whole simplification, tested at x = 2, y = 3
    "Add 4x + 5y − 3, 2x − 3y + 2 and 4y − 3x + 4. What is the coefficient of y in the sum?":
        ["(4*2 + 5*3 - 3) + (2*2 - 3*3 + 2) + (4*3 - 3*2 + 4) == 3*2 + 6*3 + 3"],
    "Add x + y − 1, y − x + 1 and 1 − 2y. All the letters cancel. What number is left?":
        ["(2 + 3 - 1) + (3 - 2 + 1) + (1 - 2*3) == 1", "(5 + 7 - 1) + (7 - 5 + 1) + (1 - 2*7) == 1"],
}
