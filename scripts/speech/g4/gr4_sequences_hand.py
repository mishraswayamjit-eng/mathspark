"""Lines written by hand for gr4_sequences, where the rules do not give a line worth hearing.

HAND is keyed by question id: {"q": "...", "options": {index: "..."}, "hints": {...}, "steps": {...}}.
TEXT is keyed by the exact printed text, for a line that repeats across questions.
A hand line is used only while its numbers still match the source (see gr4_sequences.py).

Powers above 3 and subscripts are said with the small number as a word ("3 to the power six",
"T ten"): the checker does not count a raised or lowered digit as a number, so a digit there
would read as an extra value.

The questions listed under gr4_sequences in data/bank-import/g4/renarrate.json had their hints
and steps rewritten in the bank. Their old hand lines for hints and steps were removed; only
lines written against the new text are here.
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

    # ── Hand-written chapter questions: the mark named in the question is said by name ─
    "Q_CH16_003": {
        "q": "Find the number in place of the question mark: 2, 6, 12, 20, question mark, 42, 56.",
    },
    "Q_CH16_007": {
        "q": "Which number should replace the asterisk? 37, 39, 42, 47, 54, asterisk, 78.",
    },
    "Q_CH16_011": {
        "q": "Find the number in place of the asterisk: 0.25, 0.50, 1, 1.75, asterisk, 4.",
    },

    # ── Not rewritten in the bank: notes-style hints and steps ────────────────────────
    "Q_CH16_021": {
        "steps": {0: "Differences: 3, 5, 7, 11, 9. The pattern breaks!"},
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
}

TEXT = {
    # The nth-term family (PH3_..., not rewritten in the bank).
    "nth term of an AP = a + (n−1)d.":
        "The nth term of an A P equals A plus, open bracket, n minus 1, close bracket, times d.",
}
