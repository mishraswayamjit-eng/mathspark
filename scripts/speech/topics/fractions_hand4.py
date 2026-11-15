"""Hand-written narration: worksheet questions 001 to 010, and lines that repeat across the worksheet."""

LINES = {
    "To compare fractions: find common denominator. 2/3 vs 3/4: 8/12 vs 9/12.":
        "To compare fractions, find a common denominator. For 2 over 3 and 3 over 4, that gives 8 over 12 and 9 over 12.",
    "Similar: SI on Rs.500 at 8% for 3yr = 500×8×3/100 = Rs.120.":
        "A similar one: simple interest on 500 rupees, at 8 percent for 3 years, equals 500 times 8 times 3, over 100, which is 120 rupees.",
    "Similar: If 3x+5=20, then 3x=15, x=5. Check: 3(5)+5=20 ✓.":
        "A similar one: if 3 x plus 5 equals 20, then 3 x equals 15, so x equals 5. Check: 3 times 5, plus 5, equals 20. Correct.",
    "Similar: Compare 3/5 and 2/3. LCD=15: 9/15 vs 10/15. So 2/3 is bigger.":
        "A similar one: compare 3 over 5 and 2 over 3. The L C D is 15, giving 9 over 15 and 10 over 15. So 2 over 3 is bigger.",
    "Similar: 1/4 play cricket, 1/4 play football, rest=15 students play nothing. 2/4=15→total=30.":
        "A similar one: 1 over 4 play cricket, 1 over 4 play football, and the rest, 15 students, play nothing. So 2 over 4 is 15 students, and the total is 30.",
    "Try a simpler version with easy fractions (like halves or thirds) to check your method.":
        "Try a simpler version with easy fractions, like halves or thirds, to check your method.",
}

HAND = {
    "EXT_G5_WS_B7_001": {
        "hints": [
            None,
            "The figure shows 8 equal parts, with 5 shaded. Unshaded equals 8 minus 5, which is 3 out of 8.",
            "A similar one: a pizza is cut into 4 slices, and 1 is eaten. What remains is 3 over 4.",
        ],
        "steps": [
            "Total parts, 8. Shaded, 5.",
            "Unshaded equals 8 minus 5, which is 3.",
            "The fraction is 3 over 8.",
        ],
    },
    "EXT_G5_WS_B7_002": {
        "q": "The numerator of a fraction is 21, and the denominator is 16 less than the numerator. Express this fraction as a mixed number.",
        "steps": [
            "The denominator is 21 minus 16, which is 5.",
            "21 over 5 is 4 remainder 1, which is 4 and 1 over 5.",
        ],
    },
    "EXT_G5_WS_B7_003": {
        "q": "Which of the following is the lowest form of 187 over 136?",
        "hints": [
            "Find the G C D of 187 and 136 to simplify.",
            "187 equals 11 times 17. 136 equals 8 times 17. The G C D is 17.",
            "A similar one: 51 over 34. 51 equals 3 times 17, and 34 equals 2 times 17. The G C D is 17. So 51 over 34 equals 3 over 2.",
        ],
        "steps": [
            "187 equals 11 times 17, and 136 equals 8 times 17.",
            "The G C D is 17.",
            "187 over 136 equals 11 over 8.",
        ],
    },
    "EXT_G5_WS_B7_004": {
        "hints": [
            "Count the two-digit numbers: 10 to 99 makes 90. Then count the two-digit perfect squares.",
            "Squares: 4 squared is 16. 5 squared is 25. 6 squared is 36. 7 squared is 49. 8 squared is 64. 9 squared is 81. That's 6.",
        ],
        "steps": [
            "Two-digit numbers: 90.",
            "Two-digit perfect squares: 16, 25, 36, 49, 64 and 81. That makes 6.",
            "The fraction is 6 over 90, which equals 1 over 15.",
        ],
    },
    "EXT_G5_WS_B7_005": {
        "q": "Which numbers should replace the star and the triangle, in that order? Star over 96, equals 3 over 16, equals 12 over triangle.",
        "options": ["18 and 64", "6 and 4", "18 and 80", "18 and 4"],
        "hints": [
            "If star over 96 equals 3 over 16, cross multiply: 16 times star equals 3 times 96, which is 288. So star is 18.",
            "If 3 over 16 equals 12 over triangle, cross multiply: 3 times triangle equals 16 times 12, which is 192. So triangle is 64.",
            "A similar one: star over 12, equals 2 over 3, equals 8 over triangle. Star is 8, and triangle is 12.",
        ],
        "steps": [
            "Star over 96 equals 3 over 16. So star equals 96 times 3, divided by 16, which is 18.",
            "3 over 16 equals 12 over triangle. So triangle equals 16 times 12, divided by 3, which is 64.",
        ],
    },
    "EXT_G5_WS_B7_006": {
        "q": "Find the number in place of the asterisk: 45 over 36 equals what, over 32?",
        "hints": [
            "Cross multiply: 36 times the missing number equals 45 times 32.",
            "36 times the missing number equals 1440. So the missing number is 1440 divided by 36, which is 40.",
            "A similar one: 3 over 5 equals what, over 15? Since 15 equals 5 times 3, multiply the top by 3 too. The missing number is 9.",
        ],
        "steps": [
            "45 over 36 simplifies to 5 over 4.",
            "5 over 4 equals the missing number over 32. So the missing number is 5 times 8, which is 40.",
        ],
    },
    "EXT_G5_WS_B7_007": {
        "q": "Find the value of b, if b minus 8, all over 42, equals 5 over 7.",
        "steps": [
            "7 times, open bracket, b minus 8, close bracket, equals 5 times 42, which is 210.",
            "b minus 8 equals 30.",
            "b equals 38.",
        ],
    },
    "EXT_G5_WS_B7_008": {
        "hints": [
            "The segment from 0 to 2 is split into 5 equal parts. Each part is 2 over 5.",
            "Point A appears to be at the 2nd division mark from 0. Its position is 2 times 2 over 5, which is 4 over 5.",
            "A similar one: 0 to 1, split into 4 parts, has marks at 1 over 4, 2 over 4, 3 over 4, and 1.",
        ],
        "steps": [
            "Each part is 2 divided by 5, which is 2 over 5.",
            "A is at the 2nd mark: 2 times 2 over 5 equals 4 over 5.",
        ],
    },
    "EXT_G5_WS_B7_009": {
        "hints": [
            None,
            "9 over 8 equals 1.125, which is greater than 1. All the others are less than 1.",
        ],
        "steps": [
            "19 over 21 is about 0.905. 11 over 15 is about 0.733. 23 over 32 is about 0.719.",
            "9 over 8 equals 1.125, which is greater than 1!",
            "9 over 8 is the greatest.",
        ],
    },
    "EXT_G5_WS_B7_010": {
        "hints": [
            "Convert each to decimals: 14 over 29 is about 0.483. 11 over 15 is about 0.733. 21 over 32 is about 0.656. 17 over 28 is about 0.607.",
            "The smallest decimal is 14 over 29, which is about 0.483.",
        ],
        "steps": [
            "14 over 29 is about 0.483. 11 over 15 is about 0.733. 21 over 32 is about 0.656. 17 over 28 is about 0.607.",
            "The smallest is 14 over 29.",
            "The answer is A.",
        ],
    },
}
