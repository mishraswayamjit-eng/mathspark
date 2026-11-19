"""Hand-written lines for gr4_factors: past-paper questions (EXT_G4_FP_..., PYQ_...) and newly written ones (G4A_...).

HAND[question id] = {"q": str, "o": {index: str}, "h": {index: str}, "s": {index: str}}
Lines not given here are narrated by the rules.
"""

HAND = {
    "EXT_G4_FP_2020_007": {
        "q": "What is the product of the smallest prime greater than 50 and the greatest prime less than 50?",
    },
    "EXT_G4_FP_2020_015": {
        "q": "A roll number is not a multiple of 3, is not a perfect square, and the sum of its digits is prime. Which number is it?",
    },
    "EXT_G4_FP_2020_016": {
        "q": "Of these four square numbers, one can be written as the sum of two primes in two different ways. Which one?",
    },
    "EXT_G4_FP_2020_020": {
        "q": "What is the H C F of 24 and 72?",
    },
    "EXT_G4_FP_2020_036": {
        "q": "How many 2-digit numbers are divisible by 4, 6 and 8?",
    },
    "EXT_G4_FP_2020_040": {
        "q": "The number 2, star, 1, star is divisible by 11. The digits at the star places are the same. Which digit is it?",
    },
    "EXT_G4_FP_2021_020": {
        "q": "Which two digits in 73251 should be interchanged to make it divisible by 6?",
    },
    "EXT_G4_FP_2021_025": {
        "q": "What is the L C M of 14, 35, 40, 56 and 28?",
    },
    "EXT_G4_FP_2021_040": {
        "q": "What is the difference between the L C M and the H C F of 45 and 75?",
    },
    "EXT_G4_FP_2022_003": {
        "q": "The H C F of two numbers is 15, and their L C M is 600. One number is 120. Find the other.",
    },
    "EXT_G4_FP_2022_027": {
        "q": "What is the greatest digit that can replace each A in 3 A, A 48, so that the number is divisible by 12?",
    },
    "EXT_G4_FP_2022_034": {
        "q": "What is the difference between the L C M and the H C F of 16 and 36?",
    },
    "EXT_G4_FP_2022_036": {
        "q": "The number 9, star, 3, star is divisible by 11. The digit at each star place is the same. Find the digit.",
    },
    "EXT_G4_FP_2022_037": {
        "q": "Q represents the greatest 2-digit number. Which of these represents the smallest 2-digit prime?",
    },
    "EXT_G4_FP_2023_005": {
        "q": "What is the sum of the L C M and the H C F of 65 and 91?",
    },
    "EXT_G4_FP_2023_018": {
        "q": "The number 1, A, 9, A, 5 is divisible by 7, and the digit in place of each A is the same. What is A?",
    },
    "EXT_G4_FP_2023_026": {
        "q": "What is the sum of the first 10 two-digit prime numbers, in Roman numerals?",
    },
    "EXT_G4_FP_2023_027": {
        "q": "The L C M and H C F of two numbers are 2040 and 8. One number is 120. Find the other.",
    },
    "EXT_G4_FP_2023_040": {
        "q": "Which of these is true?",
    },
    "EXT_G4_FP_2024_008": {
        "q": "What is the square of the sum of the one-digit prime numbers?",
    },
    "EXT_G4_FP_2024_010": {
        "q": "What is the L C M of 36 and 84, divided by the H C F of 36 and 84?",
    },
    "EXT_G4_FP_2024_021": {
        "q": "The numbers A 59, 5 B 2 and 6 C 9 are each divisible by 9. "
             "What is the greatest odd number that can be formed by the digits A, B and C?",
    },
    "EXT_G4_FP_2024_027": {
        "q": "The 5-digit number A 048 A is divisible by 11, and the digit at each A place is the same. What is A?",
    },
    "EXT_G4_FP_2024_034": {
        "q": "The L C M of which two numbers is a square number?",
    },
    "EXT_G4_FP_2025_001": {
        "q": "Add all the one-digit primes, then multiply by the greatest 2-digit number. "
             "What is the sum of the face values of the digits of the product?",
    },
    "EXT_G4_FP_2025_006": {
        "q": "What is the sum of the square of the greatest one-digit prime and the square of the smallest two-digit prime?",
    },
    "EXT_G4_FP_2025_008": {
        "q": "Which pair has a different H C F from the others? 30 and 45, 45 and 60, 15 and 75, or 30 and 90?",
        "o": {0: "30 and 45", 1: "45 and 60", 2: "15 and 75", 3: "30 and 90"},
        "s": {3: "The pair with a different H C F is 30 and 90."},
    },
    "EXT_G4_FP_2025_022": {
        "q": "What fraction of the 2-digit numbers are 2-digit primes?",
    },
    "EXT_G4_FP_2025_024": {
        "q": "A number is divisible by 9. Which of these must be completely true?",
    },
    "EXT_G4_FP_2025_025": {
        "q": "What is the greatest 3-digit number divisible by 12 and 18?",
    },
    "EXT_G4_FP_2025_026": {
        "q": "What is the square of the greatest 2-digit multiple of 13?",
    },
    "EXT_G4_FP_2025_030": {
        "q": "The 5-digit number 25 N 48 is a multiple of 12. What digit does N represent?",
    },
    "EXT_G4_FP_2025_040": {
        "q": "What is the difference between the L C M and the H C F of 24 and 32?",
    },

    # ── Real past papers with only filler hints and steps ──
    "PYQ_2016_Q13": {
        "q": "The three digit numbers, 5 star 7, 5 7 heart, and psi 5 9, are all divisible by 11. "
             "What is the greatest number formed by the values of star, heart and psi?",
    },
    "PYQ_2018_Q16": {
        "q": "A four digit number, 8, star, 2, star, is divisible by 9. The same digit is represented by each star. "
             "Find the digit represented by the star.",
    },
    "PYQ_2019_Q21": {
        "q": "A four digit number, 9, star, 8, star, is divisible by 9, and each star represents the same digit. "
             "Find the digit at the star place.",
    },

    # ── Newly written questions: lines the rules read clumsily ──
    "G4A_FACTORS_008": {
        "h": {2: "A similar one: a board 30 centimetres by 45 centimetres. The numbers dividing both are 1, 3, 5 and 15, "
                 "so the largest square tile has a side of 15 centimetres."},
    },
    "G4A_FACTORS_009": {
        "h": {2: "A similar one: two primes add up to 20. Can 3 be one of them? 20 minus 3 equals 17, which is prime, so yes. "
                 "Can 11? 20 minus 11 equals 9, which is 3 times 3, and is not prime, so no."},
    },
    "G4A_FACTORS_012": {
        "s": {0: "List the factors of each number. 15 has 1, 3, 5, 15, and 21 has 1, 3, 7, 21."},
    },
    "G4A_FACTORS_017": {
        "h": {2: "A similar one, with 20 steps and every 2nd and every 5th step: 10 steps and 4 steps, with 2 steps, 10 and 20, "
                 "counted twice. So 10 plus 4 minus 2, which is 12, are touched, and 20 minus 12, which is 8, are not."},
    },
    "G4A_FACTORS_021": {
        "h": {2: "A similar problem: the smallest number with exactly 4 factors. 1 has one factor. 2, 3 and 5 have two each. "
                 "4 has three: 1, 2, 4. And 6 has four: 1, 2, 3, 6. So the smallest is 6."},
        "s": {0: "Numbers up to 11 have at most four factors. For example, 6 has 1, 2, 3, 6, and 10 has 1, 2, 5, 10."},
    },
    "G4A_FACTORS_022": {
        "s": {1: "Count the factors. 1 has one. 4 has three: 1, 2, 4. 9 has three: 1, 3, 9. 16 has five.",
              2: "25 has three: 1, 5, 25. 36 has nine. And 49 has three: 1, 7, 49."},
    },
    "G4A_FACTORS_026": {
        "h": {2: "A similar problem: in rows of 4 the last row has 3, and in rows of 5 the last row has 4, with between 30 and 50 children. "
                 "One more child would fill every row, so that number is a common multiple of 4 and 5, which is 40. "
                 "The class has 40 minus 1, which is 39 children."},
    },
    "G4A_FACTORS_028": {
        "h": {2: "A similar problem: two primes add up to 15. One of them must be the even prime 2, so the other is 15 minus 2, "
                 "which is 13, and that is prime. Their product is 2 times 13, which is 26."},
    },
    "G4A_FACTORS_030": {
        "h": {2: "A similar problem: how many numbers from 1 to 60 are multiples of 2 but not of 3? "
                 "There are 60 divided by 2, which is 30, multiples of 2. "
                 "Those that are also multiples of 3 are the multiples of 6, and 60 divided by 6 equals 10. "
                 "So 30 minus 10, which is 20, numbers fit."},
    },
}
