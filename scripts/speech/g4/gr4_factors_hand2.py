"""Hand-written lines for gr4_factors: the older chapter questions (Q_CH06_..., Q_CH16_...) whose hints and
steps are printed as terse notes ("Factors of 12: 1,2,3,4,6,12", "HCF(9,16)=1"). Each is said as a sentence,
with the same numbers in the same order.
"""

HAND = {
    "Q_CH06_001": {
        "h": {1: "1, 2, 3, 4, 6, 12.", 2: "Count them: 6 factors."},
        "s": {0: "The factors of 12 are 1, 2, 3, 4, 6 and 12."},
    },
    "Q_CH06_002": {
        "h": {0: "Prime means divisible only by 1 and itself."},
        "s": {0: "29 is not divisible by 2, 3 or 5. The square root of 29 is about 5.4. Check 2, 3 and 5: none divide 29."},
    },
    "Q_CH06_003": {
        "h": {0: "If the sum of the digits is divisible by 3, the number is divisible by 3.",
              1: "A: 4 plus 5 plus 3 plus 2 equals 14, no. B: 7 plus 2 plus 5 plus 1 equals 15, yes. "
                 "C: 8 plus 2 plus 0 plus 6 equals 16, no. D: 5 plus 1 plus 2 plus 3 equals 11, no."},
    },
    "Q_CH06_004": {
        "h": {0: "For divisibility by 4, check if the last 2 digits form a number divisible by 4.",
              1: "18 divided by 4 equals 4.5, no. 34 divided by 4 equals 8.5, no. "
                 "16 divided by 4 equals 4, yes. 31 divided by 4 equals 7.75, no."},
        "s": {0: "The last 2 digits are 16. 16 divided by 4 equals 4."},
    },
    "Q_CH06_005": {
        "h": {0: "The factors of 12 are 1, 2, 3, 4, 6 and 12. The factors of 18 are 1, 2, 3, 6, 9 and 18.",
              1: "The common factors are 1, 2, 3 and 6. The highest is 6."},
        "s": {0: "The common factors are 1, 2, 3 and 6."},
    },
    "Q_CH06_006": {
        "h": {0: "The multiples of 6 are 6, 12, 18, 24, 30 and so on. The multiples of 8 are 8, 16, 24, 32 and so on.",
              1: "The first common multiple is 24."},
        "s": {0: "The L C M of 6 and 8 is 24."},
    },
    "Q_CH06_007": {
        "h": {1: "All the factors must be prime. 10, 15, and 4 are not prime.",
              2: "60 equals 2 squared, times 3, times 5."},
        "s": {0: "60 equals 2 times 30, which equals 2 times 2 times 15, which equals 2 times 2 times 3 times 5.",
              1: "That equals 2 times 2 times 3 times 5."},
    },
    "Q_CH06_009": {
        "h": {0: "Co-prime means the H C F is 1: no common factor except 1.",
              1: "8 and 12: the H C F is 4. 15 and 35: the H C F is 5. 6 and 9: the H C F is 3. "
                 "9 and 16: the factors of 9 are 1, 3, 9, and the factors of 16 are 1, 2, 4, 8, 16. The only common factor is 1."},
        "s": {0: "The H C F of 9 and 16 is 1."},
    },
    "Q_CH06_010": {
        "o": {0: "No, the digit sum is 18", 1: "Yes, the digit sum is 18", 2: "Yes, the digit sum is 9", 3: "No, the digit sum is 17"},
    },
    "Q_CH06_011": {
        "h": {0: "Composite means it has more than 2 factors. 1 is neither. 2 and 3 are prime.",
              1: "4 equals 2 times 2. It has the factors 1, 2 and 4. More than 2 factors!"},
        "s": {0: "4 has the factors 1, 2 and 4. 3 factors is more than 2."},
    },
    "Q_CH06_012": {
        "h": {0: "The rule for 11 uses the alternating sum of the digits. Add 8 plus 9, then take away 2 plus 4. "
                 "That is 17 minus 6, which equals 11."},
        "s": {0: "Add 8 plus 9, then take away 2 plus 4. That is 17 minus 6, which equals 11. 11 divided by 11 equals 1.",
              1: "It is divisible by 11."},
    },
    "Q_CH06_013": {
        "h": {0: "Find the L C M of 12 and 18.",
              1: "12 equals 2 squared times 3, and 18 equals 2 times 3 squared. "
                 "The L C M is 2 squared times 3 squared, which is 36 minutes.",
              2: "9:00, plus 36 minutes, is 9 36 a m."},
        "s": {0: "The L C M of 12 and 18 is 36.",
              1: "9:00, plus 36 minutes, is 9 36 a m."},
    },
    "Q_CH06_014": {
        "q": "48 apples and 36 oranges are to be packed in boxes. Each box must have the same number of fruits, all of the same type. "
             "What is the maximum number of fruits in each box?",
        "h": {0: "We need the largest number that divides both 48 and 36. That is the H C F.",
              1: "48 equals 2 to the fourth power, times 3. 36 equals 2 squared times 3 squared. "
                 "The H C F is 2 squared times 3, which is 12."},
        "s": {0: "The H C F of 48 and 36 is 12."},
    },
    "Q_CH06_016": {
        "h": {0: "For 8, check if the last 3 digits are divisible by 8.",
              1: "214 divided by 8 equals 26.75, no. 648 divided by 8 equals 81, yes. "
                 "234 divided by 8 equals 29.25, no. 342 divided by 8 equals 42.75, no."},
        "s": {0: "The last 3 digits are 648. 648 divided by 8 equals 81."},
    },
    "Q_CH06_018": {
        "o": {2: "it equals the sum of its factors, excluding itself: 1 plus 2 plus 3 equals 6"},
        "h": {0: "A perfect number equals the sum of its proper divisors: all its factors except itself.",
              1: "The factors of 6 are 1, 2, 3 and 6. The proper divisors are 1, 2 and 3. "
                 "Their sum is 1 plus 2 plus 3, which equals 6."},
        "s": {0: "1 plus 2 plus 3 equals 6, which is the number itself."},
    },
    "Q_CH16_012": {
        "q": "Which number does not belong to the group: 31, 41, 51, 61, 71?",
        "h": {1: "31 is prime. 41 is prime. 51 equals 3 times 17, so it is not prime. 61 is prime. 71 is prime.",
              2: "51 is the only composite number, so it doesn't belong!"},
        "s": {0: "Check each number for primality.",
              1: "51 equals 3 times 17. It's composite, not prime!",
              2: "51 doesn't belong. It's the only non-prime."},
    },
}
