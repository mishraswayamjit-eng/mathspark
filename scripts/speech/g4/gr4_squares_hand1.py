"""Hand-written narration for gr4_squares. None means: use the rules for that line.

HAND is keyed by question id; LINES is keyed by the printed line (for lines shared by several questions).
"""

N = None

HAND = {
    "EXT_G4_FP_2021_023": {
        "q": "Compare: 29 squared, blank, 31 squared minus 10 squared?",
    },
    "EXT_G4_FP_2023_032": {
        "q": "Sum of which two numbers gives a square? 159 and 165, 198 and 145, 189 and 330, or none.",
    },
    "EXT_G4_FP_2025_009": {
        "hints": [N, N, "Similar example: find the remainder when the greatest 3-digit square is divided by the smallest 3-digit square. They are 31 times 31, which is 961, and 10 times 10, which is 100. Nine 100s make 900, and 961 minus 900 equals 61. The remainder is 61."],
    },
    "G4A_SQUARES_006": {
        "steps": ["Saplings equals rows, times saplings in each row. 11 times 11."],
    },
    "G4A_SQUARES_017": {
        "hints": [N, N, "Example: with 90 children, the biggest square is 9 times 9, which is 81, so 90 minus 81, which is 9 children, are left out."],
    },
    "G4A_SQUARES_039": {
        "hints": [N, N, "A similar one: 25 children in a square stand 5 to a side. Four sides of 5 make 20, but the 4 corner children were counted twice, so 20 minus 4, which is 16 children, are on the edge."],
    },
    "G4A_SQUARES_045": {
        "hints": [N, N, "A similar one with a gap of 5: 1 plus 5 equals 6, which is not a square, but 4 plus 5 equals 9, which is. So the age would be 4."],
    },
    "EXT_G4_FP_2022_009": {
        "steps": [N, N, N, "The other two pairs give 64 plus 2025, which is 2089, and 81 plus 625, which is 706. Neither is a square number."],
    },
    "G4A_SQUARES_044": {
        "hints": [N, N, "A similar one: 1111 times 1111 equals 1234321. Its digits add up to 1 plus 2 plus 3 plus 4 plus 3 plus 2 plus 1, which makes 16, and that is 4 times 4."],
    },
    "G4A_SQUARES_046": {
        "hints": [N, N, "A similar one: the smallest multiplier of 8 that gives a square greater than 50. Multiplying 8 by 2 gives the square of 4, which is too small. Multiply that by 4 and you have 8 times 8, which is 64, and that is greater than 50. So the multiplier is 8."],
    },
}

# Lines shared by more than one question, keyed by the printed line.
LINES = {
    "The other two pairs give 59 + 52 = 111 and 76 + 78 = 154. Neither is a square number.":
        "The other two pairs give 59 plus 52, which is 111, and 76 plus 78, which is 154. Neither is a square number.",
    "The other pairs give 198 + 145 = 343 and 189 + 330 = 519. Neither is a square number.":
        "The other pairs give 198 plus 145, which is 343, and 189 plus 330, which is 519. Neither is a square number.",
}
