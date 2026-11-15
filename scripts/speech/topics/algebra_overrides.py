"""Lines written by hand for the algebra topic, where a rule does not give a line worth hearing.

OVERRIDES[question id] = {"q": "...", "options": {index: "..."}, "hints": {index: "..."}, "steps": {index: "..."}}
Anything not listed falls back to the rules in algebra_rules.py.
"""

OB = "open bracket"
CB = "close bracket"

OVERRIDES = {}

# ── Past papers 2016 to 2019 ─────────────────────────────────────────────────

OVERRIDES["EXT_G5_FP_2016_009"] = {
    "steps": {
        2: "x equals minus 24. Check: 3 times minus 24, minus 4 times minus 18, equals minus 72 plus 72, which is 0. That works.",
    },
}

OVERRIDES["EXT_G5_FP_2016_022"] = {
    "q": "What is the sum of: A plus b minus 1, b minus A plus 1, and 1 minus 2 b?",
}

OVERRIDES["EXT_G5_FP_2016_027"] = {
    "hints": {
        1: "Use letters: T for toast, S for sandwich, E for tea. T plus E equals 4. T plus S equals 4.5. S plus 2 E equals 2.",
    },
    "steps": {
        1: "From T plus E equals 4, we get E equals 4 minus T, and S equals 4.5 minus T.",
        2: "S plus 2 E equals, open bracket, 4.5 minus T, close bracket, plus 2 times, open bracket, 4 minus T, close bracket. "
           "That is 12.5 minus 3 T, which equals 2. So T equals 3.5.",
    },
}

OVERRIDES["EXT_G5_FP_2016_035"] = {
    "steps": {
        2: "D equals 9 minus 8, which is 1. C equals 7 minus 1, which is 6. B equals 10 minus 6, which is 4. A equals 6 minus 4, which is 2.",
    },
}

OVERRIDES["EXT_G5_FP_2017_001"] = {
    "hints": {
        1: "Total of all five, minus two pairs that don't overlap, equals the one person left out.",
    },
    "steps": {
        0: "E equals 105, minus, open bracket, A plus B, close bracket, minus, open bracket, C plus D, close bracket. "
           "That is 105 minus 39 minus 38, which is 28.",
        1: "A equals 105, minus, open bracket, B plus C, close bracket, minus, open bracket, D plus E, close bracket. "
           "That is 105 minus 40 minus 44, which is 21.",
        2: "B equals 39 minus 21, which is 18. C equals 40 minus 18, which is 22. D equals 38 minus 22, which is 16.",
        3: "Ages: A is 21, B is 18, C is 22, D is 16, E is 28. So the youngest is 16.",
    },
}

OVERRIDES["EXT_G5_FP_2017_006"] = {
    "hints": {
        1: "Pick one person as the base: Chetan equals c. Express others using c, then solve.",
    },
    "steps": {
        1: "Sum: c, plus c plus 5, plus c plus 2, plus c minus 3, equals 4 c plus 4, which is 20.",
    },
}

OVERRIDES["EXT_G5_FP_2017_037"] = {
    "hints": {
        1: "Open bracket, A plus b, close bracket, divided by c, equals A divided by c, plus b divided by c.",
    },
    "steps": {
        0: "12 x y divided by 4 y equals, open bracket, 12 divided by 4, close bracket, times x, times, open bracket, y divided by y, close bracket. That is 3 x.",
    },
}

OVERRIDES["EXT_G5_FP_2018_004"] = {
    "options": {2: "m plus, open bracket, m plus 2, close bracket, equals 12"},
    "hints": {
        1: "Consecutive odd numbers: m, and m plus 2. Sum means m plus, open bracket, m plus 2, close bracket.",
    },
    "steps": {
        1: "Their sum is 12, so m plus, open bracket, m plus 2, close bracket, equals 12.",
    },
}

OVERRIDES["EXT_G5_FP_2018_027"] = {
    "steps": {
        0: "We need 91 A b c, divided by something, to equal 7 c. So that something equals 91 A b c divided by 7 c.",
    },
}

OVERRIDES["EXT_G5_FP_2019_007"] = {
    "options": {3: "m plus, open bracket, m plus 2, close bracket, equals 16"},
    "steps": {
        1: "Sum equals 16, so m plus, open bracket, m plus 2, close bracket, equals 16.",
        2: "With m equals 7: 7 plus 9 equals 16. That works.",
    },
}

# ── Past papers 2020 to 2025 ─────────────────────────────────────────────────

OVERRIDES["EXT_G5_FP_2020_022"] = {
    "steps": {
        0: "b over A equals one half. It is the flip of A over b equals 2.",
        1: "4 b over A equals 4 times b over A. That is 4 times one half, which is 2.",
    },
}

OVERRIDES["EXT_G5_FP_2021_015"] = {
    "q": "If x equals 3 and y equals minus 2, then x y, over, open bracket, x minus y, close bracket, is what?",
    "hints": {
        0: "Put x equals 3 and y equals minus 2 in the top and bottom separately. Careful: x minus y equals 3 minus, minus 2, which is 3 plus 2.",
    },
    "steps": {
        1: "Bottom: x minus y equals 3 minus, minus 2. That is 3 plus 2, which is 5.",
        2: "Minus 6, over 5, equals minus 6 over 5.",
    },
}

OVERRIDES["EXT_G5_FP_2021_031"] = {
    "steps": {
        0: "Option 5: 5 plus 17 equals 22, and 60 divided by 5 equals 12. That does not work.",
        2: "Check 17: 34 versus 3.5. That does not work. Check 12: 29 versus 5. That does not work.",
    },
}

OVERRIDES["EXT_G5_FP_2022_006"] = {
    "hints": {
        1: "Distribute: 4 times, open bracket, 2 x minus 1, close bracket, equals 8 x minus 4. "
           "And 5 times, open bracket, x plus 2, close bracket, equals 5 x plus 10.",
    },
}

OVERRIDES["EXT_G5_FP_2022_035"] = {
    "options": {2: "W plus, open bracket, W plus 2, close bracket, equals 192"},
    "steps": {
        1: "Their sum is 192, so W plus, open bracket, W plus 2, close bracket, equals 192.",
        2: "Solve it: 2 W plus 2 equals 192, so W equals 95. And 95 plus 97 equals 192. That works.",
    },
}

OVERRIDES["EXT_G5_FP_2023_013"] = {
    "hints": {
        0: "Solve the equation for p first: collect p terms on one side. "
           "Then put p into, open bracket, p plus 3, close bracket, times, open bracket, p plus 2, close bracket.",
    },
    "steps": {
        0: "2 p plus 5 equals 9 p minus 30. So 35 equals 7 p. So p equals 5.",
        2: "56 is not among options A to C, so the answer is none of these.",
    },
}

OVERRIDES["EXT_G5_FP_2023_021"] = {
    "hints": {
        0: "12 x is 3 times 4 x. Find 4 x first: 4 x equals 12 plus 7. You don't need x itself.",
    },
}

OVERRIDES["EXT_G5_FP_2023_022"] = {
    "hints": {1: "Find values in order: A, then m, then p."},
}

OVERRIDES["EXT_G5_FP_2024_012"] = {
    "steps": {
        2: "Option C: 12 times 6, minus 14, equals 72 minus 14, which is 58. And 16, plus 7 times 6, equals 16 plus 42, which is 58. That works.",
    },
}

OVERRIDES["EXT_G5_FP_2024_035"] = {
    "q": "Solve: 4 x minus 5, all over 5, equals 2 x plus 3, all over 3. And find the value of x?",
}

OVERRIDES["EXT_G5_FP_2025_010"] = {
    "steps": {
        0: "Greater equals, open bracket, 92 plus 14, close bracket, divided by 2. That is 106 divided by 2, which is 53.",
        1: "Smaller equals, open bracket, 92 minus 14, close bracket, divided by 2, which is 39. Check: 53 plus 39 equals 92. That works.",
    },
}

OVERRIDES["EXT_G5_FP_2025_017"] = {
    "steps": {
        0: "q equals 2 times 7, minus 9. That is 14 minus 9, which is 5.",
        5: "Greatest is 6, which comes from 4 q minus 2 p.",
    },
}

OVERRIDES["EXT_G5_FP_2025_037"] = {
    "q": "If A equals 17, and b equals, open bracket, A minus 1, close bracket, divided by 2, and c equals b plus 3. "
         "Find the value of A squared, minus c squared, plus b squared.",
    "hints": {
        0: "Find b from A, then c from b. Then work out each square and use plus and minus from left to right.",
        1: "Order of finding: A, then b, then c.",
    },
    "steps": {
        0: "b equals, open bracket, 17 minus 1, close bracket, divided by 2. That is 16 divided by 2, which is 8.",
    },
}

# ── Worksheets: a star stands for a missing digit ────────────────────────────

OVERRIDES["EXT_G5_WS_01_008"] = {
    "q": "7, star, star, 19 is a five-digit number. The stars denote the same digit, and the difference between their place values is 5400. "
         "Find the digit in place of the star.",
    "hints": {0: "The two stars are in the thousands and hundreds places of 7, star, star, 19."},
    "steps": {0: "The two stars are in thousands and hundreds places."},
}

OVERRIDES["EXT_G5_WS_01_009"] = {
    "q": "In the five-digit number 3, star, 8, star, 2, the digits in place of the stars are the same, "
         "and the difference between their place values is 6930. Find the repeated digit.",
    "steps": {0: "The stars are in thousands and tens places."},
}

OVERRIDES["EXT_G5_WS_01_010"] = {
    "q": "In the five-digit number 6, star, 8, star, 4, the star represents the same digit. "
         "Which of the following can be the difference between the place values of the repeated digit?",
    "hints": {
        0: "The stars are in the thousands and tens places of 6, star, 8, star, 4.",
        2: "Check: 3030 divided by 990 equals 3.06, and so on. Hmm. Let me re-examine positions.",
    },
    "steps": {
        0: "The stars are in the thousands and tens places.",
        3: "Wait, rechecking. If the star is in ten-thousands and hundreds: no, 6 is in ten-thousands. "
           "If positions are 4th and 2nd, thousands and tens, then 990 d. "
           "990 times 1 equals 990. 990 times 2 equals 1980. 990 times 3 equals 2970.",
    },
}

# ── Worksheets: the rest ─────────────────────────────────────────────────────

OVERRIDES["EXT_G5_WS_B2_005"] = {
    "hints": {
        1: "2 X is always even, since 2 times anything is even. Even plus 11, which is odd, equals what?",
        2: "Try X equals 1: 2 times 1, plus 11, equals 13, which is odd. X equals 2: 2 times 2, plus 11, equals 15, odd. "
           "X equals 3: 2 times 3, plus 11, equals 17, odd. Always odd!",
    },
}

OVERRIDES["EXT_G5_WS_B2_021"] = {
    "hints": {
        2: "Actually: A plus C equals, open bracket, A plus B plus C, close bracket, minus B. "
           "B equals A plus B, plus B plus C, minus, open bracket, A plus B plus C, close bracket. "
           "That is 13 plus 19 minus 27, which is 5. A plus C equals 27 minus 5, which is 22.",
    },
    "steps": {
        0: "B equals A plus B, plus B plus C, minus, open bracket, A plus B plus C, close bracket. That is 13 plus 19 minus 27, which is 5.",
        2: "Hmm, but let me check the question again: How many oranges in all in the first and the third bags? "
           "That equals A plus C, which is 22. But option C is 22, not A.",
    },
}

OVERRIDES["EXT_G5_WS_B3_029"] = {
    "hints": {
        0: "Let pencil equal P, and pen equal P plus 10. Total: P plus, open bracket, P plus 10, close bracket, equals 18.",
        1: "2 P plus 10 equals 18. 2 P equals 8. P equals 4. Cost of 3 pencils equals 3 times 4, which is 12.",
        2: "Try: pen plus pencil equals 10, and pen is 6 more. P plus, open bracket, P plus 6, close bracket, equals 10. P equals 2. 3 pencils equals 6.",
    },
    "steps": {
        0: "P plus, open bracket, P plus 10, close bracket, equals 18.",
        1: "2 P equals 8, so P equals 4.",
    },
}

OVERRIDES["EXT_G5_WS_B6_013"] = {
    "hints": {
        1: "7 A, plus 2 times 3, minus 2 A, equals 26. So 5 A plus 6 equals 26. So 5 A equals 20.",
        2: "Similar: Find x when y equals 2: 3 x plus 4 y minus x equals 16. So 2 x plus 8 equals 16. So x equals 4.",
    },
    "steps": {
        0: "Substitute b equals 3: 7 A plus 6 minus 2 A equals 26.",
        2: "5 A equals 20, so A equals 4.",
    },
}

OVERRIDES["EXT_G5_WS_B6_014"] = {
    "hints": {
        1: "Try C: Left equals 5 times 8, plus 7, which is 47. Right equals 8 times 8, minus 17, which is 47. Equal!",
        2: "Similar: For x equals 3, is 2 x plus 1 equals x plus 4 true? Left equals 7. Right equals 7. Yes.",
    },
    "steps": {
        0: "Option A: 8, plus 5 times 8, equals 48. Against 3 times 8, plus 18, equals 42. 48 is not equal to 42.",
        1: "Option B: 9, minus 4 times 8, equals minus 23. Against 2 times 8, plus 6, equals 22. Minus 23 is not equal to 22.",
        2: "Option C: 5 times 8, plus 7, equals 47. Against 8 times 8, minus 17, equals 47. 47 equals 47. That works.",
        3: "Option D: 4 times 8, plus 7, equals 39. Against 21, plus 2 times 8, equals 37. 39 is not equal to 37.",
    },
}

OVERRIDES["EXT_G5_WS_B6_015"] = {
    "hints": {
        1: "Shortcut: Notice that 4 m plus 5 equals 2 times 2 m, plus 5. From 2 m plus 1 equals 8, we get 2 m equals 7. "
           "So 4 m equals 14, and 4 m plus 5 equals 19.",
        2: "Similar: If 3 x plus 2 equals 11, find 6 x minus 1. 3 x equals 9. 6 x equals 18. 6 x minus 1 equals 17.",
    },
}

OVERRIDES["EXT_G5_WS_B6_016"] = {
    "hints": {
        1: "Left: 2 times, open bracket, 3 d plus 4, close bracket, equals 6 d plus 8. "
           "Right: 4 times, open bracket, 5 minus 2 d, close bracket, plus 2, equals 20 minus 8 d plus 2, which is 22 minus 8 d.",
        2: "Similar: 3 times, open bracket, 2 x plus 1, close bracket, equals 2 times, open bracket, 4 minus x, close bracket, plus 5. "
           "So 6 x plus 3 equals 13 minus 2 x. So 8 x equals 10. So x equals 1.25.",
    },
    "steps": {
        2: "6 d plus 8 equals 22 minus 8 d. So 14 d equals 14. So d equals 1.",
    },
}

OVERRIDES["EXT_G5_WS_B6_019"] = {
    "hints": {
        0: "Substitute p equals m plus 3, and q equals 5 minus m, into 2 p plus 3 q equals 0.",
        2: "Similar: If A equals x plus 1, and b equals 3 minus x. 2 A plus b equals 0: "
           "2 times, open bracket, x plus 1, close bracket, plus, open bracket, 3 minus x, close bracket, equals 0. "
           "So x plus 5 equals 0. So x equals minus 5.",
    },
}
