"""Lines written by hand for the new Grade 5 questions, where the rules do not give a line worth hearing.

HAND[question id] = {"q": line, "o": {index: line}, "h": {index: line}, "s": {index: line}}
Only the lines listed are replaced; every other line of the question comes from the rules.
"""

HAND = {
    "G5A_ALGEBRA_013": {
        "h": {2: "Similar problem: the nth term is 4 n plus 3. How many terms are below 50? 4 n must be less than 47, "
                 "so n can be at most 11: the 11th term is 47, and the 12th is 51. There are 11 terms."},
    },
    "G5A_BODMAS_001": {
        "o": ["4 minus 2, in brackets", "6 plus 3, in brackets", "3 times 4, in brackets", "6 plus 3 times 4, in brackets"],
        "s": {4: "So the brackets go round 6 plus 3."},
    },
    "G5A_BODMAS_002": {
        "q": "The signs plus, minus and times are put into the three boxes, each sign used exactly once: "
             "8, box, 2, box, 5, box, 3. What is the greatest value the expression can have?",
        "h": {
            0: "There are only six ways to place the three signs. Think about which pair of numbers gains most "
               "from the times sign, and which number is best to take away.",
            1: "Put the times sign in each of the three boxes in turn. For each one, choose the better place for "
               "the plus and minus signs, remembering that multiplying is done first.",
            2: "A similar one: with plus and times in 6, box, 3, box, 4, the choices are 6 plus 3 times 4, "
               "which is 6 plus 12 equals 18, and 6 times 3 plus 4, which is 18 plus 4 equals 22. "
               "So the greatest value is 22.",
        },
        "s": {
            0: "With the times sign in the first box, the better choice is 8 times 2 plus 5 minus 3. 16 plus 5 minus 3 equals 18.",
            1: "With the times sign in the middle box, the better choice is 8 plus 2 times 5 minus 3. 8 plus 10 minus 3 equals 15.",
            2: "With the times sign in the last box, the better choice is 8 minus 2 plus 5 times 3, "
               "which takes away only the small 2. 8 minus 2 plus 15 equals 21.",
        },
    },
    "G5A_BODMAS_003": {
        "q": "Simplify: 72 divided by 6 times 3, minus a square bracket. Inside the square bracket: 15 minus a curly bracket. "
             "Inside the curly bracket: 9 minus a round bracket. Inside the round bracket: 7 minus 2 times 2.",
        "h": {2: "A similar one: 30 minus a square bracket. Inside the square bracket: 12 minus a curly bracket. "
                 "Inside the curly bracket: 8 minus a round bracket. Inside the round bracket: 5 minus 1 times 2. "
                 "Round brackets: 5 minus 2 equals 3. Curly: 8 minus 3 equals 5. Square: 12 minus 5 equals 7. "
                 "So 30 minus 7 equals 23."},
    },
    "G5A_BODMAS_004": {
        "q": "The digits 2, 3 and 4 are written in the three boxes, each digit used once: "
             "24 divided by box, plus 6 times box, minus box. What is the greatest value the expression can have?",
        "h": {2: "A similar one: digits 1, 2, 5 in 30 divided by box, plus 2 times box, minus box. "
                 "Try 30 divided by 1 plus 2 times 5 minus 2, which is 30 plus 10 minus 2 equals 38. "
                 "And try 30 divided by 2 plus 2 times 5 minus 1, which is 15 plus 10 minus 1 equals 24. "
                 "The first is greater."},
    },
    "G5A_BODMAS_006": {
        "h": {1: "In each statement, find the division and multiplication parts and do those first. Then add and "
                 "subtract from left to right and compare with the number after the equals sign."},
    },
    "G5A_BODMAS_010": {
        "q": "In 24, box, 8, box, 2, box, 5, equals 25, each box holds one of the signs plus, minus, times and divide, "
             "and no sign is used twice. There is only one way to make the statement true. Which sign is not used?",
        "o": ["the subtraction sign, minus", "the addition sign, plus", "the division sign, divide",
              "the multiplication sign, times"],
        "h": {2: "A similar one: 20, box, 6, box, 3, box, 4, equals 22. Try 20 minus 6 divided by 3 plus 4: "
                 "the division gives 2, then 20 minus 2 plus 4 equals 22. The sign not used there is the times sign."},
        "s": {3: "The signs used are minus, divide and plus, so the sign not used is the multiplication sign, times."},
    },
    "G5A_DIVISIBILITY_012": {
        "h": {2: "Similar problem: 2 P 13 Q is divisible by 8 and 11. The last three digits, 13 Q, must be divisible by 8, "
                 "so Q equals 6, because 136 equals 8 times 17. For 11, compare 2 plus 1 plus 6 equals 9 with P plus 3: "
                 "they are equal when P equals 6. So P plus Q equals 12."},
        "s": {0: "For 8, the last three digits must be divisible by 8. Among 460 to 469 only 464 works, "
                 "which is 8 times 58, so Q equals 4."},
    },
    "G5A_PLACEVALUE_009": {
        "q": "How many 3-digit numbers have digits whose product is 12? For example, 143 is one of them, "
             "because 1 times 4 times 3 equals 12.",
        "h": {2: "Similar problem: digits with product 8. The sets are 1, 1, 8, which gives 3 numbers; 1, 2, 4, "
                 "which gives 6 numbers; and 2, 2, 2, which gives 1 number. So there are 3 plus 6 plus 1 equals 10 such numbers."},
    },
    "G5A_PLACEVALUE_014": {
        "h": {2: "Similar problem with 45 more: 45 divided by 9 equals 5, so the tens digit is 5 more than the ones digit. "
                 "The numbers are 61, 72, 83 and 94. 50 is left out because its reverse is not a 2-digit number. "
                 "So there are 4 of them."},
    },
    "G5A_PLACEVALUE_018": {
        "h": {2: "Similar problem: how many 3-digit palindromes are multiples of 5? The last digit must be 0 or 5, "
                 "and it equals the first digit, which cannot be 0. So the first digit is 5, which is 1 choice, "
                 "and the middle digit is free, which is 10 choices: 1 times 10 equals 10."},
    },
    "G5A_SEQUENCES_001": {
        "h": {2: "Similar problem: 2, 5, 7, 12, 19, 31, and so on. Each term is the sum of the two before it: "
                 "2 plus 5 equals 7, and 5 plus 7 equals 12. So the 7th term is 19 plus 31 equals 50 "
                 "and the 8th term is 31 plus 50 equals 81."},
    },
    "G5A_SEQUENCES_002": {
        "s": {0: "The odd positions hold 5, 8, 11, 14, and so on: add 3. "
                 "The even positions hold 40, 35, 30, 25, and so on: subtract 5."},
    },
    "G5A_VARIATION_012": {
        "q": "A money box has only 1 rupee, 2 rupee and 5 rupee coins. The numbers of 1 rupee, 2 rupee and 5 rupee coins "
             "are in the ratio 5 is to 3 is to 2. The total value of all the coins is 210 rupees. "
             "How many 5 rupee coins are in the box?",
    },
}
