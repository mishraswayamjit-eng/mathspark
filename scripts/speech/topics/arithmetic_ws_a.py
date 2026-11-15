"""Hand-written narration lines for worksheet questions EXT_G5_WS_01 and _B2 (arithmetic topic).

Only the lines the rules in arithmetic_engine.py do not read well. See arithmetic.py for the shape.
Missing-digit sums are read one digit at a time, with "blank" for a gap.
"""

OVERRIDES = {
    "EXT_G5_WS_01_017": {
        "hints": {1: "People equals Anay's position, plus people between them, plus Vinay's position from the end, minus overlaps if any. Total equals 10 plus 5 plus 8, which is 23."},
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
        "hints": {
            0: "Look at each column separately, starting from the units column, the rightmost one.",
            2: "Try a similar one: 2 blank 3, plus blank 41, plus 1 blank 5, equals 829. Units: 3 plus 1 plus 5 equals 9, that works. Tens: blank plus 4 plus blank must give 2, with a carry. Work column by column!",
        },
        "steps": {
            0: "Units column: 8 plus B plus 1 equals something ending in 8. So 9 plus B ends in 8. B equals 9. The sum is 18, carry 1.",
            1: "Tens column: 4 plus 2 plus C, plus 1 carried over, equals something ending in 7. So 7 plus C ends in 7. C equals 0. The sum is 7, carry 0.",
        },
    },
    "EXT_G5_WS_B2_002": {
        "q": "Find the value of P plus Q. 9, 8, P, 3. Minus 4, 5, 6, 2. Equals 5, Q, 8, 1.",
        "hints": {
            1: "Units: 3 minus 2 equals 1, that works. Tens: P minus 6 equals 8. What value of P works? Remember borrowing.",
            2: "Try: 7 blank 43, minus 2 blank 61, equals 4 blank 82. Units: 3 minus 1 equals 2, that works. Tens: 4 minus 6 needs borrowing. 14 minus 6 equals 8, that works.",
        },
    },
    "EXT_G5_WS_B2_003": {
        "q": "The sum of the first 10 natural numbers exceeds the sum of the first 10 whole numbers by what?",
        "hints": {
            1: "Natural numbers start from 1. Whole numbers start from 0. The first 10 of each are?",
            2: "Natural: 1, 2, and so on up to 10, sum equals 55. Whole: 0, 1, and so on up to 9, sum equals 45. Difference equals 55 minus 45, which is 10. Wait, or are the 'first 10 whole numbers' 0 to 9?",
        },
        "steps": {
            0: "First 10 natural numbers: 1, 2, 3, and so on up to 10. Sum equals 10 times 11, divided by 2, which is 55.",
            1: "First 10 whole numbers: 0, 1, 2, and so on up to 9. Sum equals 9 times 10, divided by 2, which is 45.",
        },
    },
    "EXT_G5_WS_B2_008": {
        "hints": {1: "Maximum: five numbers, each equal to 99. Sum of units equals 5 times 9, which is 45, carry 4. Sum of tens equals 5 times 9 plus 4, which is 49, carry 4."},
    },
    "EXT_G5_WS_B2_014": {
        "hints": {
            0: "The average of 5 consecutive even numbers equals the middle number, the 3rd. Average equals 80 divided by 5.",
            1: "Average equals 16, which is the middle number. So the numbers are 12, 14, 16, 18, 20.",
            2: "Try: 3 consecutive evens summing to 18: 4, 6, 8. The middle is 6, and the 4th would be the next one, 8.",
        },
        "steps": {
            0: "Average equals 80 divided by 5, which is 16. This is the 3rd, the middle number.",
            2: "The 4th number equals 18. Wait, that doesn't match any option. Let me recheck: 12 plus 14 plus 16, plus 18 plus 20, equals 80, that works. The 4th equals 18.",
            3: "Hmm, option 2 is 18. So the answer is B.",
        },
    },
    "EXT_G5_WS_B2_028": {
        "steps": {
            0: "February 2022 has 28 days. Is 2022 divisible by 4? Actually 2022 divided by 4 equals 505.5, so it is not a leap year. 28 days.",
            1: "Sum equals 1 plus 2 plus, and so on, up to 28. That equals 28 times 29 divided by 2, which is 406.",
        },
    },
}
