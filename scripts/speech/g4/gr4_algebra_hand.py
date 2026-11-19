"""Lines written by hand for gr4_algebra, where the rules do not give a line worth hearing.

HAND is keyed by question id: {"q": "...", "options": {index: "..."}, "hints": {...}, "steps": {...}}.
TEXT is keyed by the exact printed text, for a line that repeats across questions.
A hand line is used only while its numbers still match the source (see gr4_algebra.py).
"""

BR = "open bracket, %s, close bracket"

HAND = {
    # ── Past papers, printed in a clipped style: said as full sentences ──────────────
    "EXT_G4_FP_2020_018": {
        "q": "If A equals 2 b, and b equals 3, what is the value of 2 A minus b?",
    },
    "EXT_G4_FP_2020_037": {
        "q": "A rectangle's length equals its breadth plus 2. The breadth equals A plus 2. What is the perimeter?",
    },
    "EXT_G4_FP_2020_039": {
        "q": "A equals 2, and b equals 5. What is the value of, open bracket, A plus b, close bracket, times, open bracket, b minus A, close bracket?",
    },
    "EXT_G4_FP_2021_008": {
        "q": "What is 6 x minus 3 y plus 5 z, when x equals 3, y equals x minus 1, and z equals x plus y?",
    },
    "EXT_G4_FP_2022_038": {
        "hints": {
            2: "Similar example: with A equals 2 and b equals 5, which is least: 3 A plus b, 2 b minus A, or 4 A minus b? "
               "3 A plus b is 6 plus 5, which is 11. 2 b minus A is 10 minus 2, which is 8. 4 A minus b is 8 minus 5, which is 3. "
               "The least value is 3, so 4 A minus b is least.",
        },
    },
    "EXT_G4_FP_2024_001": {
        "hints": {
            2: "Similar example: with m equals 3, n equals 4 and p equals 6, which is least: m times n plus p; "
               "open bracket, p minus m, close bracket, times n; or p plus n minus m? "
               "The first is 12 plus 6, which is 18. The second is 3 times 4, which is 12. The third is 10 minus 3, which is 7. "
               "The least value is 7, so p plus n minus m is least.",
        },
        "steps": {
            4: "The smallest value is 4. So open bracket, p minus n, close bracket, times m, has the least value.",
        },
    },
    "EXT_G4_FP_2024_022": {
        "q": "Insert the sign: 4 A plus 17, blank, 8 A minus 9, where A equals 7.",
        "options": {0: "greater than", 1: "less than", 2: "equal to"},
        "hints": {
            2: "Similar example: compare 5 A plus 6 and 7 A minus 4 when A equals 3. Left side: 5 times 3, plus 6, equals 21. "
               "Right side: 7 times 3, minus 4, equals 17. Since 21 is greater than 17, the sign is the greater than sign.",
        },
        "steps": {
            2: "45 is less than 47, so the sign is the less than sign.",
        },
    },
    "EXT_G4_FP_2025_010": {
        "q": "V plus 38 is a 2-digit prime. Find the 13th even number before it.",
    },
    "EXT_G4_FP_2025_012": {
        "q": "p equals 4, and q equals 2 p plus 1. What is the value of, open bracket, q minus p, close bracket, times, open bracket, q plus p, close bracket?",
    },
    "EXT_G4_FP_2025_038": {
        "q": "p equals 4, A equals 2 p minus 1, and y equals A plus 2. Which expression has the greatest value?",
    },

    # ── Hand-written chapter questions with notes-style hints and steps ───────────────
    "Q_CH13_001": {
        "hints": {0: "Replace A with its value. A equals 3, so A plus 4 becomes what?"},
    },
    "Q_CH13_004": {
        "hints": {0: "The whole expression, A plus 12, is divided by 3. First calculate A plus 12."},
    },
    "Q_CH13_008": {
        "hints": {1: "4 A equals 4 times 3, which is 12. Now add b, which is 5."},
    },
    "Q_CH13_012": {
        "hints": {0: "Break it down: first, the square of t means t squared. Then, half of, means divide by 2."},
    },
    "Q_CH13_018": {
        "hints": {0: "The pencil is x rupees. The pen costs thrice that, so 3 times x, which is 3 x."},
        "steps": {0: "The pencil is x rupees. The pen is 3 times x, which is 3 x rupees."},
    },
    "Q_CH13_019": {
        "options": {3: "x y metres"},
        "hints": {1: "Cutting means subtraction. Remaining equals total, minus cut piece."},
    },
    "Q_CH13_020": {
        "steps": {0: "Convert metres to centimetres: x metres equals 100 x centimetres."},
    },
    "Q_CH13_021": {
        "options": {3: "A 6"},
        "steps": {
            0: "A equals 1 A. The coefficient is 1.",
            1: "Add like terms: 5 A plus 1 A equals 6 A.",
        },
    },
    "Q_CH13_022": {
        "hints": {0: "Add the x terms together, and the y terms together. They are like terms!"},
        "steps": {0: "Group like terms. 3 x plus x, and 4 y plus 2 y."},
    },
    "Q_CH13_023": {
        "hints": {
            0: "Add the A terms: 7 A plus 3 A equals what? Add the b terms: 5 b plus, minus b, equals what?",
            1: "7 A plus 3 A equals 10 A. For b: 5 b plus, minus b, equals 5 b minus b, which is 4 b.",
        },
        "steps": {
            0: "Add the A terms: 7 A plus 3 A equals 10 A.",
            1: "Add the b terms: 5 b plus, minus b, equals 5 b minus 1 b, which is 4 b.",
        },
    },
    "Q_CH13_024": {
        "hints": {
            1: "Check each pair: 5 A and 3 A have the same variable, A. 4 m and 3 n have different variables, m and n!",
        },
        "steps": {
            1: "5 A and 3 A: both A, so like. 4 m and 3 n: m and n, so unlike!",
        },
    },
}

TEXT = {
    "Think step by step.": "Think step by step.",
}
