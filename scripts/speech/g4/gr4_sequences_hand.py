"""Lines written by hand for gr4_sequences, where the rules do not give a line worth hearing.

HAND is keyed by question id: {"q": "...", "options": {index: "..."}, "hints": {...}, "steps": {...}}.
TEXT is keyed by the exact printed text, for a line that repeats across questions.
A hand line is used only while its numbers still match the source (see gr4_sequences.py).

Powers above 3 and subscripts are said with the small number as a word ("3 to the power six",
"T ten"): the checker does not count a raised or lowered digit as a number, so a digit there
would read as an extra value.
"""

HAND = {
    # ── Past papers, printed in a clipped style: said as full sentences ──────────────
    "EXT_G4_FP_2020_003": {
        "q": "The series is 64, 81, 100, 121, and so on. Which number is not in the series?",
    },
    "EXT_G4_FP_2021_013": {
        "q": "What is the 10th term of 24, 39, 53, 66, 78, and so on?",
    },
    "EXT_G4_FP_2021_027": {
        "q": "What is the sum of the series 1, 3, 5, 7, and so on, up to 27?",
    },
    "EXT_G4_FP_2021_030": {
        "q": "What is the 59th odd number prior to 726?",
    },
    "EXT_G4_FP_2022_014": {
        "q": "What is the sum of the 7th and 11th even numbers after the greatest 2-digit prime?",
    },
    "EXT_G4_FP_2022_017": {
        "q": "The series is 122, 117, 107, 92, 72, A. Find A.",
    },
    "EXT_G4_FP_2022_030": {
        "q": "What is the 12th term of the series 13, 15, 18, 23, 30, 41, and so on?",
        "steps": {
            2: "Add these 11 primes. 2 plus 3 plus 5 plus 7, plus 11 plus 13 plus 17, plus 19 plus 23, plus 29 plus 31, equals 160.",
        },
    },
    "EXT_G4_FP_2023_003": {
        "q": "W plus 9 is odd. What is the 48th even number after it?",
    },
    "EXT_G4_FP_2023_015": {
        "q": "Find the 28th term of the series: 24, 41, 58, 75, 92, and so on.",
    },
    "EXT_G4_FP_2024_002": {
        "q": "x plus 9 is a 2-digit prime. Find the 12th even number after it.",
    },
    "EXT_G4_FP_2024_007": {
        "q": "What is the 11th number in the series 7, 10, 13, 16, 19, and so on?",
    },
    "EXT_G4_FP_2024_039": {
        "q": "What is the 9th number in the series 12, 23, 33, 42, 50, and so on?",
    },
    "EXT_G4_FP_2025_004": {
        "q": "Which of these equals the sum of the first 12 odd natural numbers?",
        "hints": {
            2: "Similar example: the first 5 odd numbers are 1, 3, 5, 7, 9. Their sum is 1 plus 3 plus 5 plus 7 plus 9, equals 25, "
               "which is 5 times 5. So the sum of the first 5 odd numbers is 5 times 5.",
        },
    },
    "EXT_G4_FP_2025_017": {
        "q": "Which number goes in place of the question mark in the series: 90, 85, 75, 60, 40, question mark?",
    },
    "EXT_G4_FP_2025_037": {
        "q": "What is the 38th term of the series 12, 19, 26, 33, 40, and so on?",
    },

    # ── A worksheet question whose choices are printed shapes ─────────────────────────
    "EXT_G4_WS2_CH16_018": {
        "q": "A sequence is formed by repeating 5 symbols: a star, a filled square, a circle, a triangle, "
             "and a circle with a plus inside. Which symbol will be in the 37th place?",
        "options": {0: "the star", 1: "the filled square", 2: "the circle", 3: "the circle with a plus inside"},
        "steps": {
            3: "The 2nd symbol in the group is the filled square. So the 37th symbol is the filled square.",
        },
    },

    # ── Newly written questions ───────────────────────────────────────────────────────
    "G4A_SEQUENCES_004": {
        "q": "What is the value of 20 minus 19, plus 18 minus 17, plus 16 minus 15, and so on, down to plus 2 minus 1? "
             "The numbers go down one at a time from 20 to 1, and the signs take turns.",
        "hints": {
            2: "Similar problem: 8 minus 7, plus 6 minus 5, plus 4 minus 3, plus 2 minus 1. "
               "Each of the pairs 8 minus 7, 6 minus 5, 4 minus 3 and 2 minus 1 is worth 1, and there are 4 pairs, so the value is 4.",
        },
    },

    # ── Past paper with a misprint ("How many kilometer") ─────────────────────────────
    "PYQ_2017_Q05": {
        "q": "A man walked a total of 66 kilometres in 6 days. Every day he walked 4 kilometres less than the previous day. "
             "How many kilometres did he walk on the 6th day?",
    },

    # ── Generated families with a formula in the hint ─────────────────────────────────
    "PH3_EXT_G4_FP_2024_033_02_b": {
        "hints": {1: "For natural numbers: n times, open bracket, n plus 1, close bracket, all over 2. That equals 6 times 7, over 2."},
        "steps": {0: "The formula for the sum of the first 6 natural numbers: n times, open bracket, n plus 1, close bracket, all over 2. "
                     "That equals 6 times 7, over 2."},
    },
    "PH3_EXT_G4_WS2_CH16_016_01_b": {
        "hints": {1: "For even numbers: n times, open bracket, n plus 1, close bracket. That equals 19 times 20."},
        "steps": {0: "The formula for the sum of the first 19 even numbers: n times, open bracket, n plus 1, close bracket. "
                     "That equals 19 times 20."},
    },

    # ── Hand-written chapter questions with notes-style hints and steps ───────────────
    "Q_CH16_001": {
        "hints": {2: "Missing: the digit is 5, and the count is 5. So the number is 55555."},
        "steps": {
            0: "Digit pattern: 9, 7, blank, 3, 1, decreasing by 2. The missing digit is 5.",
            1: "Repetition pattern: 7, 6, blank, 4, 3, decreasing by 1. The missing count is 5.",
            2: "Answer: the digit 5, repeated 5 times, which is 55555.",
        },
    },
    "Q_CH16_003": {
        "q": "Find the number in place of the question mark: 2, 6, 12, 20, question mark, 42, 56.",
        "hints": {
            1: "Differences: 4, 6, 8, blank, blank, blank, increasing by 2 each time.",
            2: "The next difference is 10. So the question mark is 20 plus 10, which is 30. "
               "Check: 42 minus 30 equals 12, and 56 minus 42 equals 14. The pattern holds!",
        },
        "steps": {
            1: "The next difference is 10. So the question mark is 20 plus 10, which is 30.",
            2: "Verify: 42 minus 30 equals 12, and 56 minus 42 equals 14. Differences: 10, 12, 14. Correct.",
            3: "Bonus: these are n times, open bracket, n plus 1, close bracket. 1 times 2 equals 2, 2 times 3 equals 6, "
               "3 times 4 equals 12, 4 times 5 equals 20, 5 times 6 equals 30.",
        },
    },
    "Q_CH16_004": {
        "hints": {2: "The next one is 6 cubed, which is 6 times 6 times 6, which is 216."},
        "steps": {1: "The next one is 6 cubed, which is 6 times 6 times 6. 6 times 6 equals 36, and 36 times 6 equals 216."},
    },
    "Q_CH16_005": {
        "hints": {1: "Differences: 3, 6, 9, 12. These are multiples of 3! Next differences: 15, 18."},
    },
    "Q_CH16_006": {
        "hints": {
            2: "So: 525 minus 87 equals 438, correct. 438 minus 87 equals 351. 351 minus 87 equals 264, correct. The missing number is 351.",
        },
        "steps": {
            1: "Verify: 177 minus 90 equals 87, and 525 minus 438 equals 87. The common difference is 87.",
        },
    },
    "Q_CH16_007": {
        "q": "Which number should replace the asterisk? 37, 39, 42, 47, 54, asterisk, 78.",
        "hints": {
            1: "2, 3, 5, 7. They're prime numbers! The next primes are 11, 13.",
            2: "The asterisk is 54 plus 11, which is 65. Check: 65 plus 13 equals 78!",
        },
        "steps": {
            0: "Differences: 2, 3, 5, 7. These are consecutive primes!",
            2: "The asterisk is 54 plus 11, which is 65. Verify: 65 plus 13 equals 78.",
        },
    },
    "Q_CH16_008": {
        "steps": {
            2: "Sum of differences equals 7 plus 8, and so on, up to 15, which is 99. So T ten equals 53 plus 99, which is 152.",
        },
    },
    "Q_CH16_009": {
        "hints": {
            1: "4 plus 7 equals 11, 7 plus 11 equals 18, 11 plus 18 equals 29. Each term is the sum of the previous two! Like Fibonacci!",
        },
        "steps": {
            0: "Pattern: each term is the sum of the previous two. 4 plus 7 equals 11, 7 plus 11 equals 18, 11 plus 18 equals 29.",
        },
    },
    "Q_CH16_011": {
        "q": "Find the number in place of the asterisk: 0.25, 0.50, 1, 1.75, asterisk, 4.",
        "hints": {
            2: "Next differences: 1.00, 1.25. So the asterisk is 1.75 plus 1.00, which is 2.75. Check: 2.75 plus 1.25 equals 4.",
        },
        "steps": {
            2: "The asterisk is 1.75 plus 1.00, which is 2.75. Verify: 2.75 plus 1.25 equals 4.",
        },
    },
    "Q_CH16_014": {
        "steps": {0: "Pattern: each term is the previous one, times 2."},
    },
    "Q_CH16_015": {
        "hints": {2: "The next one is 6 squared, which is 36."},
        "steps": {1: "The next one is 6 squared, which is 36."},
    },
    "Q_CH16_017": {
        "hints": {
            1: "Or think of it as: each term, times 3, minus 1, equals the next term. "
               "2 times 3, minus 1, equals 5. 5 times 3, minus 1, equals 14. 14 times 3, minus 1, equals 41.",
        },
        "steps": {
            0: "Pattern: next equals previous, times 3, minus 1. 2 times 3, minus 1, equals 5.",
        },
    },
    "Q_CH16_018": {
        "hints": {
            1: "You multiply by 2, then 3, then 4, then 5. These are factorials! "
               "1 factorial, 2 factorial, 3 factorial, 4 factorial, 5 factorial.",
        },
        "steps": {
            2: "These are factorials: 1 factorial equals 1, 2 factorial equals 2, 3 factorial equals 6, "
               "4 factorial equals 24, 5 factorial equals 120, 6 factorial equals 720.",
        },
    },
    "Q_CH16_020": {
        "hints": {
            1: "2 plus 3 equals 5, 3 plus 5 equals 8, 5 plus 8 equals 13, 8 plus 13 equals 21. "
               "Each number is the sum of the previous two! Fibonacci!",
        },
        "steps": {
            0: "Pattern: each term is the sum of the previous two terms. "
               "2 plus 3 equals 5, 3 plus 5 equals 8, 5 plus 8 equals 13, 8 plus 13 equals 21.",
        },
    },
    "Q_CH16_021": {
        "steps": {0: "Differences: 3, 5, 7, 11, 9. The pattern breaks!"},
    },
    "Q_CH16_022": {
        "steps": {0: "Pattern: each term, times 3, equals the next term."},
    },
    "Q_CH16_023": {
        "hints": {
            0: "The pattern is T n equals n times, open bracket, n plus 1, close bracket. "
               "Verify: T one equals 1 times 2, which is 2. T two equals 2 times 3, which is 6. T three equals 3 times 4, which is 12.",
            1: "For the 10th term: T ten equals 10 times, open bracket, 10 plus 1, close bracket.",
        },
        "steps": {
            0: "Formula: T n equals n times, open bracket, n plus 1, close bracket.",
            1: "T ten equals 10 times 11, which is 110.",
        },
    },
    "Q_CH16_024": {
        "hints": {
            0: "Find the ratio: 243 divided by 729 equals one third. 81 divided by 243 equals one third. Each term is divided by 3!",
            1: "These are powers of 3: 3 to the power six equals 729, 3 to the power five equals 243, "
               "3 to the power four equals 81, 3 cubed equals 27, 3 squared equals 9.",
            2: "Next: 3 to the power one equals 3.",
        },
        "steps": {
            0: "Pattern: each term, divided by 3, equals the next term. 729 divided by 3 equals 243, 243 divided by 3 equals 81, and so on.",
            1: "Or: 3 to the power six, 3 to the power five, 3 to the power four, 3 cubed, 3 squared, 3 to the power one.",
            2: "The next one is 3 to the power one, which is 3.",
        },
    },
    "Q_CH16_025": {
        "hints": {
            1: "Odd positions: 1, 2, 3, 4, 5, the counting numbers! Even positions: 1, 4, 9, 16, blank. These are squares!",
            2: "Next even position: 5 squared, which is 25.",
        },
        "steps": {2: "The next one is 5 squared, which is 25."},
    },
}

TEXT = {
    "nth term of an AP = a + (n−1)d.":
        "The nth term of an A P equals A plus, open bracket, n minus 1, close bracket, times d.",
    "Sum of AP = n/2 × (first term + last term).":
        "The sum of an A P equals n over 2, times, open bracket, first term plus last term, close bracket.",
}
