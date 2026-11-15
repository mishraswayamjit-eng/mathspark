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
            "4628 ends in 8, so it cannot be a square. A square ending in 5 always ends in 25, like 225 or 625. And a square ending in 0 ends in an even number of zeros, like 100 or 10000. Use these to test the other choices.",
            "Try a smaller one: which of 138, 196 and 245 is a perfect square? 138 ends in 8, and 245 does not end in 25, so only 196 can be. Check: 14 times 14 equals 196.",
        ],
        "steps": [
            None,
            None,
            "4000 lies between 63 times 63, which is 3969, and 64 times 64, which is 4096. So it is not a perfect square.",
            "That leaves 6241. Check: 79 times 79 equals 6241. So 6241 is the perfect square.",
        ],
    },
    "EXT_G5_WS_B5_004": {
        "hints": [
            None,
            "31 times 31 is 961, which has only three digits. So try 32 times 32 for the smallest four-digit square. The one-digit primes are 2, 3, 5 and 7. Divide your square by the greatest of them, and see what is left over.",
            "Try a smaller one: the smallest two-digit square is 4 times 4, which is 16, and the smallest odd prime is 3. 16 equals 3 times 5, plus 1, so the remainder is 1.",
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
            "100 times 100 is 10000, which has five digits. So try 99 times 99. Then see which place the digit 8 sits in.",
            "A similar one: 86 times 86 equals 7396. Here, the digit 3 is in the hundreds place, so its place value is 3 times 100, which is 300.",
        ],
        "steps": [
            "The greatest 4-digit perfect square is 99 squared, which is 9801.",
            "In 9801: 9 is in the thousands place, 8 in the hundreds, 0 in the tens, and 1 in the units.",
            "The place value of 8 is 8 times 100, which equals 800.",
        ],
    },
    "EXT_G5_WS_B5_008": {
        "hints": [
            "Read the order carefully: first square each one-digit prime, then add the squares.",
            "The one-digit primes are 2, 3, 5 and 7. 1 is not a prime. Work out 2 times 2, 3 times 3, 5 times 5, and 7 times 7. Then add the four results.",
            "Try a smaller one: the sum of the squares of 1, 2 and 3 is 1 plus 4 plus 9, which equals 14.",
        ],
        "steps": [
            "2 squared is 4, 3 squared is 9, 5 squared is 25, and 7 squared is 49.",
            "The sum is 4 plus 9 plus 25 plus 49, which equals 87.",
        ],
    },
    "EXT_G5_WS_B5_009": {
        "hints": [
            "In any division: dividend equals divisor times quotient, plus remainder. Here, the dividend is 1000, and the quotient and remainder are both 25.",
            "Take the remainder away first: 1000 minus 25 is 975. This is the divisor times 25. So divide 975 by 25 to find the divisor, then square it.",
            "Try a smaller one: 50 divided by a number gives quotient 4 and remainder 2. 50 minus 2 is 48, and 48 divided by 4 is 12. So the divisor is 12, and its square is 144.",
        ],
        "steps": [
            "Dividend equals divisor times quotient, plus remainder. So 1000 equals the divisor times 25, plus 25.",
            "Take away the remainder: 1000 minus 25 is 975. So the divisor times 25 is 975.",
            "The divisor is 975 divided by 25, which equals 39.",
            "39 times 39 equals 1521, so the square of the divisor is 1521.",
        ],
    },
    "EXT_G5_WS_B5_010": {
        "hints": [
            None,
            "Start with 10 and 1: 10 times 10, minus 1 times 1, is 100 minus 1, which equals 99. 99 is between 9 times 9, which is 81, and 10 times 10, which is 100. So it is not a square. Now test the other pairs.",
            "Try a smaller one: 5 and 4. 5 times 5, minus 4 times 4, is 25 minus 16, which equals 9. And 3 times 3 is 9, so that difference is a square number.",
        ],
        "steps": [
            "10 and 1: 100 minus 1 is 99, which lies between 9 times 9, or 81, and 10 times 10, or 100. Not a square.",
            "13 and 4: 169 minus 16 is 153, which lies between 12 times 12, or 144, and 13 times 13, or 169. Not a square.",
            "41 and 9: 41 times 41 is 1681, and 9 times 9 is 81. 1681 minus 81 equals 1600.",
            "40 times 40 equals 1600, so 1600 is a square number. The other two pairs do not work, so it cannot be all of these.",
            "So the two numbers are 41 and 9.",
        ],
    },
    "EXT_G5_WS_B5_011": {
        "q": "If m equals 5 and n equals 6, then find the value of m squared plus n squared.",
        "options": [None, None, None, "11 squared"],
        "hints": [
            "m squared means m times m. Put the numbers in place of the letters, square each one, then add.",
            "With m equal to 5, and n equal to 6, you need 5 times 5, and 6 times 6. Square each number first, and only then add the two results.",
            "Try a smaller one: if m is 2 and n is 3, then m squared plus n squared is 4 plus 9, which equals 13. Notice this is not the same as squaring 2 plus 3.",
        ],
        "steps": [
            "m squared is 5 squared, which equals 25.",
            "n squared is 6 squared, which equals 36.",
            "m squared plus n squared is 25 plus 36, which equals 61.",
        ],
    },
    "EXT_G5_WS_B5_013": {
        "hints": [
            None,
            "The sum is 18 divided by 2, which is 9. Which two consecutive numbers, numbers next to each other, like 6 and 7, add up to 9? Square each of them, and add.",
            "Try a smaller one: twice the sum of two consecutive numbers is 10. The sum is 5, so the numbers are 2 and 3. Their squares add up to 4 plus 9, which equals 13.",
        ],
        "steps": [
            "Twice the sum is 18, so the sum is 18 divided by 2, which is 9.",
            "Two consecutive numbers that add up to 9 are 4 and 5, because 4 plus 5 equals 9.",
            "Their squares are 4 times 4, which is 16, and 5 times 5, which is 25.",
            "16 plus 25 equals 41, so the sum of their squares is 41.",
        ],
    },
    "EXT_G5_WS_B5_014": {
        "hints": [
            None,
            "20 times 20 is 400, which is too big. Try 19 times 19. Then take that square away from 386.",
            "Try a smaller one: what least number must be subtracted from 70 to make a perfect square? 8 times 8 is 64, which fits, but 9 times 9 is 81, which is too big. 70 minus 64 is 6, so subtract 6.",
        ],
        "steps": [
            "19 squared is 361, and 20 squared is 400.",
            "386 minus 361 equals 25.",
            "386 minus 25 equals 361, which is 19 squared. Correct.",
        ],
    },
    "EXT_G5_WS_B5_015": {
        "hints": [
            None,
            "37 times 37 is 1369, which is too small. Work out 38 times 38, then subtract 1400 from it.",
            "Try a smaller one: what smallest number must be added to 50 to make a perfect square? 7 times 7 is 49, which is too small. 8 times 8 is 64, the next square, and 64 minus 50 is 14. So add 14.",
        ],
        "steps": [
            "37 times 37 is 1369, which is less than 1400. 38 times 38 is 1444, which is more than 1400.",
            None,
            "1444 minus 1400 equals 44, so the smallest number to add is 44.",
        ],
    },
    "EXT_G5_WS_B5_016": {
        "hints": [
            "First work out 35 times 36. Then find the first square number that is bigger than it.",
            "35 times 36 equals 1260. Compare with squares nearby: 35 times 35 is 1225, which is smaller, so the next square up is 36 times 36. How far is 1260 from it?",
            "Try a smaller one: 4 times 5 is 20. The next square is 5 times 5, which is 25, and 25 minus 20 is 5. So you add 5.",
        ],
        "steps": [
            "35 times 36 equals 1260.",
            "35 times 35 is 1225, which is less than 1260. So the next square number is 36 times 36, which is 1296.",
            "1296 minus 1260 equals 36.",
            None,
        ],
    },
    "EXT_G5_WS_B5_018": {
        "hints": [
            None,
            "Start with 25 times 49: 25 is 5 times 5, and 49 is 7 times 7. Every prime has a partner, so this product is a square: it is 35 times 35. Test the other products the same way, and look for one with a prime left over.",
            "Try a smaller one: 2 times 6 times 3 is the same as 2 times 2, times 3 times 3. The 2s pair up and the 3s pair up, so it is a square: 6 times 6 equals 36. But 2 times 6 times 5 is the same as 2 times 2, times 3, times 5. That has 3 and 5 left alone, so 60 is not a square.",
        ],
        "steps": [
            "25 times 49 is the same as 5 times 5, times 7 times 7, which equals 1225. And 35 times 35 is 1225. A square.",
            "3 times 9 times 12 equals 324, and 18 times 18 is 324. A square.",
            "7 times 14 times 18 equals 1764, and 42 times 42 is 1764. A square.",
            "9 times 12 times 4 equals 432, which lies between 20 times 20, or 400, and 21 times 21, or 441. Not a square.",
            "So the product that is not a square number is 9 times 12 times 4.",
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
            "An even square comes from squaring an even number, and an odd square from an odd number. So count the even numbers whose squares have three digits.",
            "The smallest three-digit square is 10 times 10, which is 100, and the largest is 31 times 31, which is 961. So the even numbers to count go 10, 12, 14, and so on, up to 30. Count them carefully.",
            "Try a smaller one: even two-digit squares. Two-digit squares come from 4 to 9. The even numbers there are 4, 6 and 8, giving 16, 36 and 64. So there are 3.",
        ],
        "steps": [
            None,
            "Three-digit squares run from 10 times 10, which is 100, to 31 times 31, which is 961, because 32 times 32 is 1024, which has four digits.",
            None,
            None,
        ],
    },
    "EXT_G5_WS_B5_022": {
        "q": "How many natural numbers lie between 4 squared and 6 squared?",
        "hints": [
            None,
            "4 times 4 is 16, and 6 times 6 is 36. So count the numbers after 16 and before 36: they start at 17 and stop at 35.",
            "Try a smaller one: between 2 times 2, which is 4, and 3 times 3, which is 9, lie 5, 6, 7 and 8. That is 4 numbers.",
        ],
        "steps": [
            "4 squared is 16, and 6 squared is 36.",
            "Between them, not counting the ends: 17 to 35.",
            "The count is 35 minus 17 plus 1, which equals 19.",
        ],
    },
    "EXT_G5_WS_B5_024": {
        "hints": [
            "If there are 6 boxes, each has 6 pencils: 6 times 6 in all. So the total is always a number times itself, a square number.",
            None,
            "Try a smaller one: could the total be 40, 44 or 49? 40 ends in a single zero. 6 times 6 is 36, and 7 times 7 is 49, so 44 is not a square. Only 49 works: 7 boxes of 7 pencils.",
        ],
        "steps": [
            "If there are n boxes, each box holds n pencils, so the total is n times n. The total must be a perfect square.",
            None,
            "616 lies between 24 times 24, which is 576, and 25 times 25, which is 625. So it is not a square.",
            "27 times 27 equals 729. So the total can be 729 pencils: 27 boxes of 27 pencils.",
        ],
    },
    "EXT_G5_WS_B5_025": {
        "hints": [
            "The number of groups equals the group size, which is n. The total in groups is n squared. Find the largest n squared that is less than or equal to 245.",
            "15 squared is 225, which is less than 245. 16 squared is 256, which is greater than 245. The leftover is 245 minus 225.",
            "A similar one: 30 students, in n groups of n. 5 squared is 25, so the leftover is 5.",
        ],
        "steps": [
            None,
            "Find the biggest square that is not more than 245: 15 times 15 is 225, which fits, but 16 times 16 is 256, which is too many.",
            None,
            "245 minus 225 equals 20, so 20 students will be left out.",
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
