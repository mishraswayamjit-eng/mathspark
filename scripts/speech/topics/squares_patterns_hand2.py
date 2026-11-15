"""Hand-written narration: past papers 2020 to 2023. A missing key or a None falls back to the rules."""

NTH_AD = "The nth term equals A plus, open bracket, n minus 1, close bracket, times d."
PRIME_STEPS_8TH = ("The 6th term is 27 plus 11, which is 38. The 7th is 38 plus 13, which is 51. "
                   "The 8th is 51 plus 17, which is 68.")

HAND = {
    "EXT_G5_FP_2020_010": {
        "q": "The nine interior intersection points on a 4 by 4 grid of squares are shown. A 4 by 4 grid has 3 times 3, which is 9, interior points. How many interior intersection points are there on a 16 by 16 grid of squares?",
        "hints": [
            "A 4 by 4 grid has 3 lines inside each way, giving 3 times 3 points. How many inside lines does a 16 by 16 grid have each way?",
            "An n by n grid has, n minus 1, times, n minus 1, interior points.",
        ],
        "steps": [
            "For a 4 by 4 grid: 4 minus 1, times, 4 minus 1, is 3 times 3, which equals 9. Correct.",
            "For a 16 by 16 grid: 16 minus 1, times, 16 minus 1, is 15 times 15.",
            "15 times 15 equals 225.",
        ],
    },
    "EXT_G5_FP_2020_025": {
        "hints": [
            "Find the first perfect square above 1300. Try 36 squared and 37 squared.",
            "The next perfect square, minus the number.",
        ],
        "steps": [
            "36 squared is 1296, which is below 1300. 37 squared is 1369.",
            "1369 minus 1300 equals 69.",
        ],
    },
    "EXT_G5_FP_2020_028": {
        "q": "Ajay writes the sequence: 3, 14, 25, 36, and so on. Which of the following numbers can appear in his sequence?",
        "hints": [
            None,
            "Each term equals 3 plus 11 times something. So the term, minus 3, must be divisible by 11.",
        ],
        "steps": [
            "Subtract 3 from each option, and test divisibility by 11.",
            "114 minus 3 is 111, which is not a multiple of 11. 111 minus 3 is 108. No. 110 minus 3 is 107. No.",
            "113 minus 3 is 110, which equals 11 times 10. Yes.",
            "Answer: 113, the 11th term.",
        ],
    },
    "EXT_G5_FP_2021_005": {
        "q": "What would be the 12th term of the series: 15, 19, 23, 27, and so on?",
        "hints": [
            "Find the common difference. Then use: the nth term equals the first term plus, open bracket, n minus 1, close bracket, times d.",
            NTH_AD,
        ],
        "steps": [
            "d is 19 minus 15, which equals 4.",
            "The 12th term is 15 plus, 11 times 4. That is 15 plus 44, which equals 59.",
        ],
    },
    "EXT_G5_FP_2021_025": {
        "q": "Which will be the 8th term in the given series of the numbers? 10, 12, 15, 20, 27, and so on.",
        "hints": [
            "Look at the gaps: 2, 3, 5, 7, and so on. These are special numbers. What comes next?",
            "The gaps are prime numbers: 2, 3, 5, 7, 11, 13, 17, and so on.",
        ],
        "steps": [
            "The gaps are 2, 3, 5, 7, which are primes. The next gaps are 11, 13, 17.",
            PRIME_STEPS_8TH,
        ],
    },
    "EXT_G5_FP_2021_032": {
        "hints": [
            "One third of one quarter is 1 over 12. Find the number first. Then take 3 over 10 of it, and square it.",
            "One third times one quarter equals 1 over 12.",
        ],
        "steps": [
            "One third of one quarter is 1 over 12 of the number, and that equals 15. So the number is 15 times 12, which equals 180.",
            "3 over 10 of 180 is 54.",
            "54 squared is 54 times 54, which equals 2916.",
        ],
    },
    "EXT_G5_FP_2021_036": {
        "hints": [
            None,
            "0.000326 equals 326 divided by 1,000,000. And 1,000,000 is itself a perfect square: it is 1000 squared.",
        ],
        "steps": [
            "The perfect square just below 326 is 324, which is 18 times 18.",
            "So the perfect square is 0.000324. That is 0.018 times 0.018.",
            "Subtract: 0.000326 minus 0.000324 equals 0.000002.",
        ],
    },
    "EXT_G5_FP_2022_002": {
        "q": "In the given series, find the number in place of K: 9, 13, 21, 37, K, 133.",
        "hints": [
            "Look at the gaps: 4, 8, 16, and so on. Each gap is double the one before. Keep doubling to find K.",
            "Gaps that double: 4, 8, 16, 32, 64, and so on.",
        ],
        "steps": [
            "The gaps: 13 minus 9 is 4. 21 minus 13 is 8. 37 minus 21 is 16. They are doubling.",
            "The next gap is 32. So K is 37 plus 32, which equals 69.",
            "Check: the next gap is 64, and 69 plus 64 equals 133. Correct.",
            "69 is not among options A to C. So the answer is: None of these.",
        ],
    },
    "EXT_G5_FP_2022_003": {
        "hints": [
            "Find the greatest three-digit perfect square. 30 squared is 900, 31 squared is 961, and 32 squared is 1024, which is too big.",
            "The greatest 3-digit square is the biggest square below 1000.",
        ],
        "steps": [
            "32 squared is 1024, which has 4 digits. 31 squared is 961, and that is the greatest 3-digit square.",
            "1015 minus 961 equals 54.",
        ],
    },
    "EXT_G5_FP_2022_007": {
        "hints": [
            "The greatest two-digit prime is 97, and the smallest is 11. Square each, then add.",
            "97 squared equals, open bracket, 100 minus 3, close bracket, squared, which is 9409.",
        ],
        "steps": [
            "97 squared is 9409, and 11 squared is 121.",
            "The sum is 9409 plus 121, which equals 9530.",
        ],
    },
    "EXT_G5_FP_2022_033": {
        "q": "Find the 11th term of the given series: 19, 31, 43, 55, and so on.",
        "hints": [
            "Find the common difference. Then use: the nth term equals A plus, open bracket, n minus 1, close bracket, times d.",
            NTH_AD,
        ],
        "steps": [
            "d is 31 minus 19, which equals 12.",
            "The 11th term is 19 plus, 10 times 12. That is 19 plus 120, which equals 139.",
        ],
    },
    "EXT_G5_FP_2022_036": {
        "q": "What should be subtracted from the product of 13 times 14, to get the square of the smallest two-digit odd number?",
        "hints": [
            "The smallest two-digit odd number is 11. Square it. Then work out 13 times 14, and find the difference.",
            "The difference equals the product minus the square.",
        ],
        "steps": [
            "13 times 14 equals 182.",
            "The smallest two-digit odd number is 11, and 11 squared is 121.",
            "182 minus 121 equals 61.",
        ],
    },
    "EXT_G5_FP_2023_016": {
        "q": "The given series 26, 30, 34, 38, and so on, is increasing by 4 each time. What will be the 59th term of the series?",
        "hints": [
            "The nth term equals the first term plus, open bracket, n minus 1, close bracket, times 4. Use n minus 1 equals 58.",
            NTH_AD,
        ],
        "steps": [
            "A is 26, d is 4, and n is 59.",
            "The 59th term is 26 plus, 58 times 4. That is 26 plus 232, which equals 258.",
        ],
    },
    "EXT_G5_FP_2023_026": {
        "q": "Find the 10th term of the given series: 126, 124, 121, 116, 109, 98, and so on.",
        "hints": [
            "Look at the gaps going down: 2, 3, 5, 7, 11, and so on. These are special numbers! Keep going with the same list.",
            "The gaps are the prime numbers 2, 3, 5, 7, 11, 13, 17, 19, 23, and so on.",
        ],
        "steps": [
            "The gaps: from 126 to 124 is 2. From 124 to 121 is 3. From 121 to 116 is 5. From 116 to 109 is 7. From 109 to 98 is 11. These are primes.",
            "The next gaps are 13, 17, 19, 23.",
            "The 7th term is 98 minus 13, which is 85. The 8th is 85 minus 17, which is 68. The 9th is 68 minus 19, which is 49. The 10th is 49 minus 23, which is 26.",
        ],
    },
    "EXT_G5_FP_2023_028": {
        "steps": [
            "100 has the digit 0 repeated, and 101 has the digit 1 repeated. The smallest with different digits is 102.",
            "102 squared is 102 times 102, which equals 10404.",
            "Answer: 10404.",
        ],
    },
    "EXT_G5_FP_2023_035": {
        "hints": [
            None,
            "11 squared is 121, 13 squared is 169, 17 squared is 289, and 19 squared is 361.",
        ],
        "steps": [
            "The squares are 121, 169, 289, 361.",
            "121 plus 169 equals 290. 289 plus 361 equals 650.",
            "The total is 290 plus 650, which equals 940.",
        ],
    },
    "EXT_G5_FP_2023_038": {
        "q": "Find the 9th term of the given series: X C V I I, then L X X X I X, then L X X X I I I, then L X X I X, then L X X I I I, and so on.",
        "options": ["L I I I", "L V I I", "L X I", "L I X"],
        "hints": [
            "Change the Roman numerals into numbers: X C V I I is 97, L X X X I X is 89, and so on. Do you recognise this list of numbers? Think primes.",
            "Roman numerals: L is 50, X is 10, V is 5, I is 1, and X C is 90. The series is the prime numbers going down.",
        ],
        "steps": [
            "97, 89, 83, 79, 73. These are primes, going down.",
            "The next primes are 71, 67, 61, 59.",
            "The terms: 1st 97, 2nd 89, 3rd 83, 4th 79, 5th 73, 6th 71, 7th 67, 8th 61, 9th 59.",
            "59 is 50 plus 9. That is L plus I X, which is written L I X.",
        ],
    },
}
