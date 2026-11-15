"""Hand-written narration: past papers 2024 to 2025, and worksheets 01, B2, B3.

A missing key or a None falls back to the rules.
"""

NTH_AD = "The nth term equals A plus, open bracket, n minus 1, close bracket, times d."

HAND = {
    "EXT_G5_FP_2024_006": {
        "hints": [
            "Think of squares near 4618. 60 squared is 3600, and 70 squared is 4900, so the answer is between. Try 67 squared and 68 squared.",
            None,
        ],
        "steps": [
            "67 squared is 4489, which is too small. 68 squared is 4624, just above 4618.",
            "The number to add is 4624 minus 4618, which equals 6.",
        ],
    },
    "EXT_G5_FP_2024_016": {
        "q": "Find the sum of the 11th and 18th term of the given series: 3, 7, 11, 15, 19, and so on.",
        "hints": [
            "Find the common difference first: how much does each term go up? Then use: the nth term equals A plus, open bracket, n minus 1, close bracket, times d.",
            "The nth term equals the first term plus, open bracket, n minus 1, close bracket, times d. Here, A is 3 and d is 4.",
        ],
        "steps": [
            "d is 7 minus 3, which equals 4.",
            "The 11th term is 3 plus, 10 times 4, which equals 43.",
            "The 18th term is 3 plus, 17 times 4, which equals 71.",
            "The sum is 43 plus 71, which equals 114. That is not in options A to C, so the answer is None of these.",
        ],
    },
    "EXT_G5_FP_2024_029": {
        "q": "What would be the 9th term of the given series: 405, 363, 321, 279, 237, and so on?",
        "hints": [
            "This series goes down. Find the difference, it is negative! Then use: the nth term equals A plus, open bracket, n minus 1, close bracket, times d.",
            "For a falling series, d is negative: the nth term equals A minus, open bracket, n minus 1, close bracket, times the drop.",
        ],
        "steps": [
            "The drop each time is 405 minus 363, which equals 42.",
            "The 9th term is 405 minus, 8 times 42. That is 405 minus 336, which equals 69.",
        ],
    },
    "EXT_G5_FP_2024_030": {
        "options": [
            "8 squared plus 12 squared equals 15 squared",
            "12 squared plus 35 squared equals 37 squared",
            "11 squared plus 59 squared equals 60 squared",
            "13 squared plus 84 squared equals 87 squared",
        ],
        "hints": [
            None,
            None,
            "For example, is 6 squared plus 8 squared equal to 10 squared? 36 plus 64 equals 100, and 10 times 10 equals 100, so yes. Test each statement like this.",
        ],
        "steps": [
            "8 squared plus 12 squared: 64 plus 144 equals 208, but 15 squared is 225. Not equal.",
            "11 squared plus 59 squared: 121 plus 3481 equals 3602, but 60 squared is 3600. Not equal.",
            "13 squared plus 84 squared: 169 plus 7056 equals 7225, but 87 squared is 7569. Not equal.",
            "12 squared plus 35 squared: 144 plus 1225 equals 1369, and 37 squared is 37 times 37, which equals 1369. Equal.",
            "So the true statement is 12 squared plus 35 squared equals 37 squared.",
        ],
    },
    "EXT_G5_FP_2025_013": {
        "hints": [
            "Two-digit odd numbers start at 11, and go 11, 13, 15, and so on, up to 39. Count how many there are, then use the pairing trick for the sum.",
            "The sum equals the number of terms, divided by 2, times, open bracket, first plus last, close bracket. The number of terms equals, open bracket, last minus first, close bracket, divided by d, plus 1.",
        ],
        "steps": [
            "The numbers are 11, 13, 15, and so on, up to 39. The jump, d, is 2.",
            "The count is, open bracket, 39 minus 11, close bracket, divided by 2, plus 1, which equals 15.",
            "The sum is 15 divided by 2, times, open bracket, 11 plus 39, close bracket. That is 15 times 25, which equals 375.",
        ],
    },
    "EXT_G5_FP_2025_021": {
        "hints": [
            "Add 97 to each option, and check whether it is a perfect square. Use 30 squared is 900, 31 squared is 961, and 32 squared is 1024, as markers.",
            None,
        ],
        "steps": [
            "852 plus 97 equals 949. That is between 30 squared and 31 squared, so it is not a square.",
            "768 plus 97 equals 865. That is between 29 squared and 30 squared, so it is not a square.",
            "489 plus 97 equals 586. That is between 24 squared and 25 squared, so it is not a square.",
            "927 plus 97 equals 1024, which is 32 squared. Yes.",
        ],
    },
    "EXT_G5_FP_2025_022": {
        "q": "What would be the sum of the first 8 terms of the given series: 7, 11, 15, 19, and so on?",
        "hints": [
            None,
            "The sum of n terms equals n divided by 2, times, open bracket, first plus last, close bracket.",
        ],
        "steps": [
            "The 8 terms are 7, 11, 15, 19, 23, 27, 31, 35.",
            "First plus last is 7 plus 35, which equals 42.",
            "The sum is 8 divided by 2, times 42. That is 4 times 42, which equals 168.",
        ],
    },
    "EXT_G5_FP_2025_031": {
        "options": [
            "7 squared plus 11 squared equals 150",
            "9 squared plus 16 squared equals 327",
            "19 squared plus 27 squared equals 1190",
            "18 squared plus 23 squared equals 853",
        ],
        "hints": [
            None,
            "Start with the smallest numbers: 7 squared is 49, and 11 squared is 121. Add them, and compare with 150. Then do the same for the other three statements.",
            "For example, to test whether 5 squared plus 12 squared makes 169: 25 plus 144 equals 169, so that statement would be true.",
        ],
        "steps": [
            "7 squared plus 11 squared is 49 plus 121, which equals 170, not 150.",
            "9 squared plus 16 squared is 81 plus 256, which equals 337, not 327.",
            "19 squared plus 27 squared is 361 plus 729, which equals 1090, not 1190.",
            "18 squared plus 23 squared is 324 plus 529, which equals 853. Correct.",
        ],
    },
    "EXT_G5_FP_2025_032": {
        "q": "Find the 8th term of the series: 197, 193, 185, 173, 157, and so on.",
        "hints": [
            "The gap between terms is not constant. Write down the gaps: 4, 8, 12, and so on. Do you see a pattern in the gaps?",
            "When gaps themselves form a pattern, keep extending the gaps: minus 4, minus 8, minus 12, minus 16, minus 20, and so on.",
        ],
        "steps": [
            "Find the gaps between the terms: 197 minus 193 is 4. 193 minus 185 is 8. 185 minus 173 is 12. 173 minus 157 is 16.",
            "The gaps grow by 4 each time, so the next gaps are 20, 24 and 28.",
            "The 6th term: 157 minus 20 equals 137. The 7th term: 137 minus 24 equals 113.",
            "The 8th term: 113 minus 28 equals 85.",
        ],
    },
    "EXT_G5_WS_01_018": {
        "hints": [
            None,
            "The nth even number before an odd number equals the odd number, minus, open bracket, 2 n minus 1, close bracket.",
            "Try the 3rd even number before 11: 10, 8, 6. That's 11 minus 5, which equals 6. The formula gives 11 minus, open bracket, 2 times 3, minus 1, close bracket. That is 11 minus 5, which equals 6.",
        ],
        "steps": [
            "105 is odd, so the 1st even number before it is 104.",
            "Each even number before that is 2 less. To go from the 1st to the 23rd, you step back 22 times: 22 times 2 is 44.",
            "104 minus 44 equals 60. So the 23rd even number prior to 105 is 60.",
        ],
    },
    "EXT_G5_WS_01_020": {
        "q": "If K is an even number, which is the 12th odd number before it?",
        "hints": [
            "The first odd number before even K is K minus 1. The next is K minus 3, then K minus 5, and so on.",
            "The nth odd number before even K is K minus, open bracket, 2 n minus 1, close bracket.",
            "Try the 3rd odd number before 10: 9, 7, 5. That's 10 minus 5. The formula gives 10 minus, open bracket, 2 times 3, minus 1, close bracket. That is 10 minus 5, which equals 5. Correct!",
        ],
        "steps": [
            "The nth odd number before even K is K minus, open bracket, 2 n minus 1, close bracket.",
            "Substitute n equals 12. We get K minus, open bracket, 2 times 12, minus 1, close bracket, which is K minus 23.",
            "Answer: K minus 23.",
        ],
    },
    "EXT_G5_WS_B2_006": {
        "hints": [
            None,
            None,
            "An example with the first 3: 2 plus 4 plus 6 equals 12, and 1 plus 3 plus 5 equals 9. The difference is 12 minus 9, which is 3. That is 1 for each of the 3 pairs.",
        ],
        "steps": [
            "The sum of the first 25 even natural numbers is 2 plus 4, and so on, up to 50. That equals 2 times, open bracket, 1 plus 2, and so on, up to 25, close bracket. That is 2 times 325, which equals 650.",
            "The sum of the first 25 odd natural numbers is 1 plus 3, and so on, up to 49. That equals 25 squared, which is 625.",
            "The difference is 650 minus 625, which equals 25.",
        ],
    },
    "EXT_G5_WS_B2_012": {
        "hints": [
            None,
            "For consecutive numbers, the average equals the middle number. So the middle number, the 3rd, is 24.",
            "Try the average of 5 consecutive numbers from 10: 10, 11, 12, 13 and 14. The average is 12, the middle number.",
        ],
        "steps": [
            "For 5 consecutive numbers, the average equals the middle number, which is 24.",
            "The 5 numbers are: 22, 23, 24, 25, 26.",
            "The smallest is 22.",
        ],
    },
    "EXT_G5_WS_B2_013": {
        "hints": [
            None,
            "So the 4th number is 31, and three more odd numbers come after it. Odd numbers go up by 2 each time. Count on from 31, three times.",
            "An example: 5 consecutive odd numbers have an average of 9. The middle number, the 3rd, is 9. So the numbers are 5, 7, 9, 11, 13, and the largest is 13.",
        ],
        "steps": [
            "The average of 7 consecutive odd numbers equals the middle number, which is 31.",
            "The numbers are 25, 27, 29, 31, 33, 35, 37.",
            "The largest is 37.",
        ],
    },
    "EXT_G5_WS_B3_003": {
        "hints": [
            None,
            None,
            "Try: 3 times 5 is 15, which ends in 5. 7 times 5 is 35, which ends in 5. Once 5 is in the product, the units digit stays 5.",
        ],
        "steps": [
            "The odd numbers from 16 to 25 are 17, 19, 21, 23, 25.",
            "Since 25 is in the list, and contains the factor 5, and all the numbers are odd, the product will end in 5.",
            "The units digit is 5.",
        ],
    },
}
