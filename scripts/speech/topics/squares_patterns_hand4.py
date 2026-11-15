"""Hand-written narration: worksheet B5 (squares and square roots).

A missing key or a None falls back to the rules.
"""

SMALL = ("Try with smaller numbers first: 3 squared is 9, 4 squared is 16, 5 squared is 25. "
         "Check if the pattern you found works.")
SQUARES_LIST = "Perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, and so on."
SIM_COUNT = ("A similar one: how many 2-digit squares? The smallest is 4 squared, which is 16. "
             "The largest is 9 squared, which is 81. The count is 9 minus 4 plus 1, which equals 6.")
SIM_BOXES = ("A similar one: n boxes with n items each makes n squared items. "
             "If there are 100 items, n is 10, since 10 squared is 100.")

HAND = {
    "EXT_G5_WS_B5_001": {
        "hints": [
            None,
            "Write out every digit used: 1, 6, 2, 5, 3, 6, 4, 9, 6, 4, 8, 1. Count each digit.",
            "A similar one: in 1-digit squares, 1, 4 and 9, which is the most frequent digit? 1 appears 1 time, 4 appears 1 time, 9 appears 1 time. All tie!",
        ],
        "steps": [
            "The two-digit perfect squares are 16, 25, 36, 49, 64, 81.",
            "How often each digit appears: 1 appears 2 times. 2 appears 1 time. 3 appears 1 time. 4 appears 2 times. 5 appears 1 time. 6 appears 3 times. 8 appears 1 time. 9 appears 1 time.",
            "6 appears 3 times, in 16, 36 and 64, which is the most.",
        ],
    },
    "EXT_G5_WS_B5_002": {
        "hints": [
            None,
            "Try square roots: the square root of 4628 is about 68. 68 squared is 4624, which is not 4628. What is the square root of 6241? Try 79 squared, which is 6241!",
            SMALL,
        ],
        "steps": [
            "Test each: 68 squared is 4624, and 69 squared is 4761. 4628 is between them, so it is not a perfect square.",
            "75 squared is 5625, and 76 squared is 5776. 5665 is between them, so no.",
            "79 squared is 6241. Yes.",
            "63 squared is 3969, and 64 squared is 4096. 4000 is between them, so no.",
        ],
    },
    "EXT_G5_WS_B5_004": {
        "hints": [
            "Find the smallest 4-digit perfect square. Then find the greatest 1-digit prime. Divide, and find the remainder.",
            "The smallest 4-digit square is 32 squared, which is 1024. The greatest 1-digit prime is 7. What is 1024 divided by 7?",
            "A similar one: 100, the smallest 3-digit square, divided by 7, is 14 remainder 2.",
        ],
        "steps": [
            "The smallest 4-digit perfect square is 32 squared, which is 1024.",
            "The greatest 1-digit prime is 7.",
            "1024 divided by 7 is 146, remainder 2.",
            "The remainder is 2.",
        ],
    },
    "EXT_G5_WS_B5_005": {
        "hints": [
            None,
            "99 squared is 9801. The digit 8 is in the hundreds place. Its place value is 8 times 100, which equals 800.",
            "A similar one: in 7396, which is 86 squared, the place value of 3 is 3 times 100, which equals 300.",
        ],
        "steps": [
            "The greatest 4-digit perfect square is 99 squared, which is 9801.",
            "In 9801: 9 is in the thousands place, 8 in the hundreds, 0 in the tens, and 1 in the units.",
            "The place value of 8 is 8 times 100, which equals 800.",
        ],
    },
    "EXT_G5_WS_B5_008": {
        "hints": [None, None, SQUARES_LIST],
        "steps": [
            "2 squared is 4, 3 squared is 9, 5 squared is 25, and 7 squared is 49.",
            "The sum is 4 plus 9 plus 25 plus 49, which equals 87.",
        ],
    },
    "EXT_G5_WS_B5_009": {
        "hints": [
            "Use: dividend equals divisor times quotient, plus remainder. Here, 1000 equals d times 25, plus 25.",
            "1000 equals 25 d plus 25, which is 25 times, open bracket, d plus 1, close bracket. So d plus 1 equals 40, and d equals 39.",
            "A similar one: 50 equals d times 4, plus 4. d equals, open bracket, 50 minus 4, close bracket, divided by 4, which is 46 divided by 4. Hmm, try: 100 equals d times 9, plus 1. d is 11. 11 squared is 121.",
        ],
        "steps": [
            "1000 equals d times 25, plus 25.",
            "25 d equals 975, so d equals 39.",
            "d squared is 39 squared, which equals 1521.",
        ],
    },
    "EXT_G5_WS_B5_010": {
        "hints": [
            "Compute A squared minus b squared for each pair, and check if the result is a perfect square.",
            "10 squared minus 1 squared is 99, not a square. 13 squared minus 4 squared is 153, not a square. 41 squared minus 9 squared is 1600. Is 1600 a perfect square?",
            SMALL,
        ],
        "steps": [
            "10 squared minus 1 squared is 100 minus 1, which equals 99. The square root of 99 is about 9.95, so no.",
            "13 squared minus 4 squared is 169 minus 16, which equals 153. The square root of 153 is about 12.4, so no.",
            "41 squared minus 9 squared is 1681 minus 81, which equals 1600. That is 40 squared. Yes.",
            "Answer: 41 and 9.",
        ],
    },
    "EXT_G5_WS_B5_011": {
        "q": "If m equals 5 and n equals 6, then find the value of m squared plus n squared.",
        "options": [None, None, None, "11 squared"],
        "hints": [None, None, SQUARES_LIST],
        "steps": [
            "m squared is 5 squared, which equals 25.",
            "n squared is 6 squared, which equals 36.",
            "m squared plus n squared is 25 plus 36, which equals 61.",
        ],
    },
    "EXT_G5_WS_B5_013": {
        "hints": [
            "If 2 times, open bracket, n plus n plus 1, close bracket, equals 18, then 2 times, open bracket, 2 n plus 1, close bracket, equals 18. So 2 n plus 1 equals 9, and n equals 4. The numbers are 4 and 5.",
            "The sum of the squares is 4 squared plus 5 squared, which is 16 plus 25.",
            "A similar one: 2 times, open bracket, n plus n plus 1, close bracket, equals 10, which gives n equals 2. Then 2 squared plus 3 squared is 4 plus 9, which equals 13.",
        ],
        "steps": [
            "2 times, open bracket, n plus n plus 1, close bracket, equals 18. So 2 n plus 1 equals 9, which means n equals 4.",
            "The numbers are 4 and 5.",
            "4 squared plus 5 squared is 16 plus 25, which equals 41.",
        ],
    },
    "EXT_G5_WS_B5_014": {
        "hints": [
            "Find the largest perfect square that is less than or equal to 386.",
            "19 squared is 361, and 20 squared is 400. Since 400 is greater than 386, use 361. Subtract: 386 minus 361 equals 25. Hmm, but option A is 25 and B is 19.",
            SMALL,
        ],
        "steps": [
            "19 squared is 361, and 20 squared is 400.",
            "386 minus 361 equals 25.",
            "386 minus 25 equals 361, which is 19 squared. Correct.",
        ],
    },
    "EXT_G5_WS_B5_015": {
        "hints": [
            "Find the smallest perfect square that is greater than or equal to 1400.",
            "37 squared is 1369, which is too small. 38 squared is 1444. Add: 1444 minus 1400 equals 44.",
            "A similar one: what do we add to 50 to make a square? 8 squared is 64, and 64 minus 50 equals 14.",
        ],
        "steps": [
            "37 squared is 1369, which is less than 1400. 38 squared is 1444, which is greater than 1400.",
            "1444 minus 1400 equals 44.",
            "The answer is C.",
        ],
    },
    "EXT_G5_WS_B5_016": {
        "hints": [
            "First compute 35 times 36, then find the nearest perfect square above it.",
            "35 times 36 equals 1260. The next perfect square is 36 squared, which is 1296. The difference is 36. But wait: check if there's something smaller.",
            SMALL,
        ],
        "steps": [
            "35 times 36 equals 1260.",
            "Note: 35 times 36 equals 36 squared minus 36.",
            "Add 36: 1260 plus 36 equals 1296, which is 36 squared.",
        ],
    },
    "EXT_G5_WS_B5_018": {
        "hints": [
            None,
            "25 times 49 is 1225, which is 35 squared. 3 times 9 times 12 is 324, which is 18 squared. 7 times 14 times 18 is 1764, which is 42 squared.",
            SMALL,
        ],
        "steps": [
            "Option A: 25 times 49 equals 1225, which is 35 squared. A square number.",
            "Option B: 3 times 9 times 12 equals 324, which is 18 squared. A square number.",
            "Option C: 7 times 14 times 18 equals 1764, which is 42 squared. A square number.",
            "Option D: 9 times 12 times 4 equals 432. 20 squared is 400, and 21 squared is 441. Not a perfect square.",
        ],
    },
    "EXT_G5_WS_B5_020": {
        "hints": [
            None,
            "The smallest is 10 squared, which is 100. The largest is 31 squared, which is 961. 32 squared is 1024, which has 4 digits.",
            SIM_COUNT,
        ],
        "steps": [
            "The smallest 3-digit square is 10 squared, which is 100.",
            "The largest 3-digit square is 31 squared, which is 961.",
            "The count is 31 minus 10 plus 1, which equals 22.",
        ],
    },
    "EXT_G5_WS_B5_021": {
        "hints": [
            None,
            "The even numbers from 10 to 30 are: 10, 12, 14, 16, 18, 20, 22, 24, 26, 28 and 30.",
            SIM_COUNT,
        ],
        "steps": [
            "The even numbers whose squares have 3 digits are 10, 12, and so on, up to 30.",
            "The count is, open bracket, 30 minus 10, close bracket, divided by 2, plus 1, which equals 11.",
            "The answer is C.",
        ],
    },
    "EXT_G5_WS_B5_022": {
        "q": "How many natural numbers lie between 4 squared and 6 squared?",
        "hints": [
            "4 squared is 16, and 6 squared is 36. Count the natural numbers strictly between 16 and 36.",
            "The numbers are 17, 18, and so on, up to 35. The count is 35 minus 17 plus 1, which equals 19.",
            "A similar one: between 2 squared, which is 4, and 3 squared, which is 9, there are 5, 6, 7 and 8. That is 4 numbers.",
        ],
        "steps": [
            "4 squared is 16, and 6 squared is 36.",
            "Between them, not counting the ends: 17 to 35.",
            "The count is 35 minus 17 plus 1, which equals 19.",
        ],
    },
    "EXT_G5_WS_B5_024": {
        "hints": [
            "If there are n boxes with n pencils each, the total is n times n, which is n squared. So the total must be a perfect square.",
            "Check each: 729 is 27 squared, a perfect square. 1440, 1028, 616: are any of these perfect squares?",
            SIM_BOXES,
        ],
        "steps": [
            "The total is n squared, so it must be a perfect square.",
            "729 is 27 squared. Yes.",
            "The answer is A.",
        ],
    },
    "EXT_G5_WS_B5_025": {
        "hints": [
            "The number of groups equals the group size, which is n. The total in groups is n squared. Find the largest n squared that is less than or equal to 245.",
            "15 squared is 225, which is less than 245. 16 squared is 256, which is greater than 245. The leftover is 245 minus 225.",
            "A similar one: 30 students, in n groups of n. 5 squared is 25, so the leftover is 5.",
        ],
        "steps": [
            "The largest n, with n squared less than or equal to 245, is n equals 15. 15 squared is 225.",
            "Left out: 245 minus 225, which equals 20.",
            "The answer is B.",
        ],
    },
    "EXT_G5_WS_B5_026": {
        "q": "Every boy in the class contributed as many rupees as the total number of boys in the class. The teacher contributed 75 rupees. The total amount collected was 1300 rupees. How much did each boy contribute?",
        "hints": [
            "If there are b boys, each gives b rupees. The total from the boys is b squared. Plus the teacher's 75 rupees, that equals 1300.",
            "b squared equals 1300 minus 75, which is 1225. Find the square root of 1225.",
            SIM_BOXES,
        ],
        "steps": [
            "b squared plus 75 equals 1300.",
            "b squared equals 1225.",
            "b equals 35.",
        ],
    },
}
