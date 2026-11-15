"""Hand-written narration: past papers 2016 to 2019. A missing key or a None falls back to the rules."""

NTH_AD = "The nth term equals A plus, open bracket, n minus 1, close bracket, times d."

HAND = {
    "EXT_G5_FP_2016_003": {
        "q": "The number of whole numbers that lie between 4 squared and 4 cubed is:",
        "hints": [
            "First work out 4 squared and 4 cubed. 'Between' means you do not count the two end numbers.",
            "The count of whole numbers strictly between A and b is, b minus A, and then minus 1.",
        ],
        "steps": [
            "4 squared is 16, and 4 cubed is 64.",
            "The numbers between 16 and 64 are 17, 18, and so on, up to 63.",
            "The count is 64 minus 16 minus 1, which equals 47.",
        ],
    },
    "EXT_G5_FP_2016_008": {
        "q": "What is the value of the tenth term, T, in the sequence: 2, 7, 14, 23, 34, and so on, up to T?",
        "hints": [
            "Find the gaps between terms: 5, 7, 9, 11, and so on. The gaps themselves go up by 2. Keep extending until you reach the 10th term.",
            "When gaps form a pattern, extend the gaps: 5, 7, 9, 11, 13, 15, 17, 19, 21.",
        ],
        "steps": [
            "The gaps: 7 minus 2 is 5. 14 minus 7 is 7. 23 minus 14 is 9. 34 minus 23 is 11. The next gaps are 13, 15, 17, 19, 21.",
            "The terms are 2, 7, 14, 23, 34, 47, 62, 79, 98, 119.",
            "So the 10th term is 119.",
        ],
    },
    "EXT_G5_FP_2016_030": {
        "q": "What term fits in the blank space in the sequence: one half, 4, 1 over 8, 16, blank, 64?",
        "options": ["1 over 24", "1 over 32", "1 over 40", "1 over 42"],
        "hints": [
            "Two patterns are mixed together. Look at the 1st, 3rd, 5th terms on their own, and the 2nd, 4th, 6th on their own.",
            "This is an alternate term series: split it into two simple series.",
        ],
        "steps": [
            "Terms 2, 4 and 6 are 4, 16 and 64. Each one is the one before, times 4.",
            "Terms 1, 3 and 5 are one half, 1 over 8, and so on. Each one is the one before, divided by 4. One half, divided by 4, is 1 over 8.",
            "Next: 1 over 8, divided by 4, is 1 over 32.",
        ],
    },
    "EXT_G5_FP_2017_016": {
        "hints": [
            None,
            "Start from 100 times 100, which is 10000, and 101 times 101, which is 10201. Is 10025 either of these? Test the other choices in the same way: a number ending in 25 could be the square of a number ending in 5.",
            "For example, 35 times 35 equals 1225, so 1225 is a perfect square. A shortcut for squaring a number ending in 5: for 35, work out 3 times 4, which is 12, and write 25 after it.",
        ],
        "steps": [
            "10025 lies between 100 squared, which is 10000, and 101 squared, which is 10201. So it is not a perfect square.",
            "1025 lies between 32 squared, which is 1024, and 33 squared, which is 1089. So it is not a perfect square.",
            "105 times 105 equals 11025. So this one is a perfect square.",
        ],
    },
    "EXT_G5_FP_2017_034": {
        "q": "The least number that should be subtracted from 370, so that the resulting number is a square number, is:",
        "hints": [
            None,
            "Try squares near 370: 19 times 19 is 361, and 20 times 20 is 400. Which of these is just below 370? Subtract that square from 370.",
            "A similar one: for 150, the square just below is 12 times 12, which is 144. So the least number to subtract is 150 minus 144, which equals 6.",
        ],
        "steps": [
            "19 squared is 361, and 20 squared is 400. The square just below 370 is 361.",
            "370 minus 361 equals 9.",
        ],
    },
    "EXT_G5_FP_2017_036": {
        "q": "In the series 1, 3, 7, 15, 31, 63, and so on, what will be the units digit of the 30th term of the series?",
        "hints": [
            "Compare the terms with powers of 2: 2, 4, 8, 16, 32, 64. How does each term relate? Then look at the pattern of last digits of powers of 2.",
            "The nth term equals 2 to the power n, minus 1. The last digits of 2 to the power n repeat every 4: 2, 4, 8, 6.",
        ],
        "steps": [
            "Each term is 1 less than a power of 2: 2 minus 1, 4 minus 1, 8 minus 1, 16 minus 1, and so on. So the 30th term is 2 to the power thirty, minus 1.",
            "The units digits of the powers of 2 go 2, 4, 8, 6, and then repeat every 4 powers.",
            "30 is 7 lots of 4, with 2 left over, because 7 times 4 is 28. So 2 to the power thirty has the 2nd digit of the cycle: it ends in 4.",
            "Take away 1: the 30th term ends in 4 minus 1, which is 3.",
            "So the units digit is 3.",
        ],
    },
    "EXT_G5_FP_2018_006": {
        "q": "The given series 13, 16, 19, 22, and so on, is increasing by 3 each time. What will be the 75th number of the series?",
        "hints": [
            "The nth term equals the first term plus, open bracket, n minus 1, close bracket, times 3. Remember to use n minus 1, not n.",
            NTH_AD,
        ],
        "steps": [
            "A is 13, d is 3, and n is 75.",
            "The 75th term is 13 plus, 74 times 3. That is 13 plus 222, which equals 235.",
        ],
    },
    "EXT_G5_FP_2018_017": {
        "hints": [
            None,
            "Start with 9 and 16: 9 times 9 is 81, and 16 times 16 is 256, total 337. Is 337 a square? 18 times 18 is 324, and 19 times 19 is 361, so no. Test the other pairs the same way.",
            "A similar one: 6 and 8. 6 times 6 is 36, and 8 times 8 is 64. 36 plus 64 equals 100, which is 10 times 10. So 6 and 8 work.",
        ],
        "steps": [
            "10 and 15: 100 plus 225 equals 325. Not a square, because 18 times 18 is 324, and 19 times 19 is 361.",
            "8 and 15: 64 plus 225 equals 289, and 17 times 17 is 289. This is a square number.",
            "12 and 15: 144 plus 225 equals 369, which lies between 19 times 19, or 361, and 20 times 20, or 400. 9 and 16: 81 plus 256 equals 337, which lies between 18 times 18, or 324, and 19 times 19, or 361. Neither is a square.",
            "So the two numbers are 8 and 15.",
        ],
    },
    "EXT_G5_FP_2018_034": {
        "hints": [
            "A shortcut for numbers ending in 5: multiply the front digits by, front plus 1, and write 25 at the end.",
            "The square of a number written as n, then 5, equals n times, open bracket, n plus 1, close bracket, followed by 25. For 125, n is 12.",
        ],
        "steps": [
            "12 times 13 equals 156.",
            "Write 25 after it: 15625.",
            "Check: 125 times 125 equals 125 times 100, plus 125 times 25. That is 12500 plus 3125, which equals 15625. Correct.",
        ],
    },
    "EXT_G5_FP_2019_008": {
        "hints": [
            "Rows times soldiers in each row, with both numbers equal, means a perfect square. Find the biggest perfect square that is not more than 850.",
            "Find the biggest perfect square that is less than or equal to N. Then N minus that square is the number left over.",
        ],
        "steps": [
            "29 times 29 is 841, and 30 times 30 is 900, which is too many.",
            "Soldiers used: 841.",
            "Left out: 850 minus 841, which equals 9.",
        ],
    },
    "EXT_G5_FP_2019_034": {
        "q": "The smallest number that can be added to 1325, to make the resulting number a square number, is?",
        "hints": [
            "Find the first perfect square above 1325. Try 36 squared and 37 squared.",
            "The next perfect square, minus the number.",
        ],
        "steps": [
            "36 squared is 1296, which is too small. 37 squared is 1369.",
            "1369 minus 1325 equals 44.",
        ],
    },
    "EXT_G5_FP_2019_040": {
        "q": "Which will be the 8th term in the given series of numbers? 10, 12, 15, 20, 27, and so on.",
        "hints": [
            "Look at the gaps: 2, 3, 5, 7, and so on. These are special numbers! What comes next in that list?",
            "The gaps are prime numbers: 2, 3, 5, 7, 11, 13, 17, and so on.",
        ],
        "steps": [
            "The gaps: 12 minus 10 is 2. 15 minus 12 is 3. 20 minus 15 is 5. 27 minus 20 is 7. These are prime numbers.",
            "The next gaps are 11, 13, 17.",
            "The 6th term is 27 plus 11, which is 38. The 7th is 38 plus 13, which is 51. The 8th is 51 plus 17, which is 68.",
        ],
    },
}
