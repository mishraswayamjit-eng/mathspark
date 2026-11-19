"""Hand-written lines for gr4_factors: the older chapter questions (Q_CH06_..., Q_CH16_...).

Some still print their hints and steps as terse notes ("Factors of 12: 1,2,3,4,6,12", "HCF(9,16)=1"); each is
said as a sentence, with the same numbers in the same order. The hints and steps of Q_CH06_002, 003, 004, 006,
007, 012, 013, 014, 016, 018 and Q_CH16_012 were rewritten in the bank, so their old hand lines are gone; any
new hand lines for them are in gr4_factors_hand3.py.
"""

HAND = {
    "Q_CH06_001": {
        "h": {1: "1, 2, 3, 4, 6, 12.", 2: "Count them: 6 factors."},
        "s": {0: "The factors of 12 are 1, 2, 3, 4, 6 and 12."},
    },
    "Q_CH06_005": {
        "h": {0: "The factors of 12 are 1, 2, 3, 4, 6 and 12. The factors of 18 are 1, 2, 3, 6, 9 and 18.",
              1: "The common factors are 1, 2, 3 and 6. The highest is 6."},
        "s": {0: "The common factors are 1, 2, 3 and 6."},
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
    "Q_CH06_014": {
        "q": "48 apples and 36 oranges are to be packed in boxes. Each box must have the same number of fruits, all of the same type. "
             "What is the maximum number of fruits in each box?",
    },
    "Q_CH06_018": {
        "o": {2: "it equals the sum of its factors, excluding itself: 1 plus 2 plus 3 equals 6"},
    },
    "Q_CH16_012": {
        "q": "Which number does not belong to the group: 31, 41, 51, 61, 71?",
    },
}
