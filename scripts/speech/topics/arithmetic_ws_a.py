"""Hand-written narration lines for worksheet questions EXT_G5_WS_01 and _B2 (arithmetic topic).

Only the lines the rules in arithmetic_engine.py do not read well. See arithmetic.py for the shape.
Missing-digit sums are read one digit at a time, with "blank" for a gap.
"""

OVERRIDES = {
    "EXT_G5_WS_01_017": {
        "steps": {
            0: "Anay is 10th from front. That means 9 people before Anay, plus Anay.",
            2: "Vinay is 8th from end. That means Vinay, plus 7 people after.",
        },
    },
    "EXT_G5_WS_01_019": {
        "steps": {2: "The difference is, open bracket, Q plus 1, close bracket, minus, open bracket, Q minus 1, close bracket, which is 2."},
    },
    "EXT_G5_WS_B2_001": {
        "q": "In the given sum of addition, find the digits in place of A, B and C. A, 4, 8. Plus 3, 2, B. Plus 5, C, 1. Equals 1, 4, 7, 8.",
        "steps": {
            0: "Units column: 8 plus B plus 1 equals something ending in 8. So 9 plus B ends in 8. B equals 9. The sum is 18, carry 1.",
            1: "Tens column: 4 plus 2 plus C, plus 1 carried over, equals something ending in 7. So 7 plus C ends in 7. C equals 0. The sum is 7, carry 0.",
        },
    },
    "EXT_G5_WS_B2_002": {
        "q": "Find the value of P plus Q. 9, 8, P, 3. Minus 4, 5, 6, 2. Equals 5, Q, 8, 1.",
    },
    "EXT_G5_WS_B2_003": {
        "q": "The sum of the first 10 natural numbers exceeds the sum of the first 10 whole numbers by what?",
        "steps": {
            0: "First 10 natural numbers: 1, 2, 3, and so on up to 10. Sum equals 10 times 11, divided by 2, which is 55.",
            1: "First 10 whole numbers: 0, 1, 2, and so on up to 9. Sum equals 9 times 10, divided by 2, which is 45.",
        },
    },
}
