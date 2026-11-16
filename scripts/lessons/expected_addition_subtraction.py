# -*- coding: utf-8 -*-
"""Expected computations for the 'addition-subtraction' lesson quiz.

Written separately from the lesson text. check_new_lessons.py evaluates each
one exactly and compares it with the keyed answer in data/lessons.

    id: "expression"                      every number must be in the question
    id: ("expression", "constants")       numbers the question gives in words
"""

EXPECT = {
    # Level 1: adding big numbers
    "as-l1-q1": "2415 + 3272",
    "as-l1-q2": "476 + 358",
    "as-l1-q3": "6789 + 2345",
    "as-l1-q4": "125 + 240 + 310 + 95",
    "as-l1-q5": "12450 + 3875",
    "as-l1-q6": "18640 + 21785",
    "as-l1-q7": "234500 + 165750",
    "as-l1-q8": "58967 + 36485",
    # Level 2: subtracting big numbers
    "as-l2-q1": "8694 - 5273",
    "as-l2-q2": "742 - 368",
    "as-l2-q3": "6003 - 2748",
    "as-l2-q4": "10000 - 3456",
    "as-l2-q5": "8500 - 5725",
    "as-l2-q6": "1240 - 385",
    "as-l2-q7": "50000 - 27643",
    "as-l2-q8": "302105 - 198476",
    # Level 3: estimating and shortcuts
    "as-l3-q1": ("rnd(6812, 1000) + rnd(2190, 1000)", "1000"),
    "as-l3-q2": "3456 + 999",
    "as-l3-q3": "7300 - 998",
    "as-l3-q4": "46 + 75 + 54 + 25",
    "as-l3-q5": ("rnd(1899, 1000) + rnd(2999, 1000)", "1000"),
    "as-l3-q6": "198 + 199 + 203",
    "as-l3-q7": "2345 + 3452 + 4523 + 5234",
    "as-l3-q8": "9999 + 999 + 99 + 9",
    # Level 4: missing numbers
    "as-l4-q1": "4000 - 2350",
    "as-l4-q2": "7000 - 4625",
    "as-l4-q3": "3000 - 1275",
    "as-l4-q4": "1154 + 846",
    "as-l4-q5": "1500 - 875",
    "as-l4-q6": "12000 - 7360",
    "as-l4-q7": "(3042 + 869) - 2165",
    # the tens digit of the hidden number 643 - 275
    "as-l4-q8": ("(643 - 275) // 10 % 10", "10"),
    # Level 5: word problems
    "as-l5-q1": "480 + 135",
    "as-l5-q2": "912 - 478",
    "as-l5-q3": "640 + 85",
    "as-l5-q4": "3000 - (1245 + 980)",
    # second basket = 11 + 18 - 24; first and third = all - second
    "as-l5-q5": "24 - (11 + 18 - 24)",
    # girls + boys - everyone in commerce
    "as-l5-q6": "735 + (735 + 145) - (435 + 375)",
    "as-l5-q7": "(22 + 44 + 66 + 88) / (11 + 22 + 33 + 44)",
    "as-l5-q8": "4000 - (5000 - 2875)",
}

# Sentences with a blank digit: the checker cannot read "4_7", so each one
# carries its own proof with the digit filled in.
ALLOW = {
    "Look at 4_7 + 285 = 732. In the ones column 7 + 5 = 12, so write 2 and carry 1.":
        ["447 + 285 == 732"],
    "In the sum 3_8 + 275 = 643, which digit goes in the blank?":
        ["368 + 275 == 643"],
}
