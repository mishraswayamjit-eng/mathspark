"""Hand-written narration for gr4_equations: lines the rules do not say well enough.

HAND[question id] = {"q": ..., "options": [...], "hints": [...], "steps": [...]}; None leaves a line to the rules.
"""
N = None

HAND = {
    "EXT_G4_FP_2020_005": {
        "steps": [N, N, N, "Check: 3 times 3, minus 7, equals 2. And 8, minus 2 times 3, equals 2. Both sides match."],
    },
    "EXT_G4_FP_2021_028": {
        "q": "The sum of 2 natural numbers is 16, and their difference is 8. What is their product?",
    },
    "EXT_G4_FP_2021_036": {
        "q": "One third, plus one half, plus 1 over x, equals 4. Find x.",
        "hints": [N, N, "A similar example: one quarter, plus one half, plus 1 over x, equals 2. First, one quarter plus one half equals three quarters. Then 1 over x must be 2 minus three quarters, which is 5 over 4. Turn it upside down: x equals 4 over 5."],
        "steps": [N, "Find what 1 over x must be, by taking this from 4. Write 4 as 24 over 6. 24 over 6, minus 5 over 6, equals 19 over 6."],
    },
    "EXT_G4_FP_2022_002": {
        "q": "Find A in the equation: 6 A plus 8 equals 4 A plus 18.",
        "hints": [N, "Take 4 A away from both sides. How many A are left on the left side?"],
    },
    "EXT_G4_FP_2022_023": {
        "q": "If 8 P plus 7 equals 39, and Q equals P plus 3, find the value of 2 P plus 3 Q.",
        "steps": [N, N, N, "Now work out 2 P plus 3 Q, with P as 4 and Q as 7. 2 times 4, plus 3 times 7, equals 29."],
    },
    "EXT_G4_FP_2023_006": {
        "q": "Mishti has 97 pens, and Manav has 11. Mishti gives some, so that she has twice Manav's. How many are given?",
    },
    "EXT_G4_FP_2023_020": {
        "steps": [N, N, "Second one: 44, minus 4 times 8, equals 12. And 3 times 8, minus 12, equals 12. Equal.",
                  "Third one: 62, plus 3 times 8, equals 86. But 11 times 8, plus 2, equals 90. Not equal."],
    },
    "EXT_G4_FP_2023_021": {
        "q": "Solve the equation: 7 times, open bracket, 3 P minus 4, close bracket, equals 4 times, open bracket, 5 plus 3 P, close bracket, plus 6.",
        "hints": [N, N, "A similar example: 3 times, open bracket, 2 P minus 1, close bracket, equals 2 times, open bracket, P plus 4, close bracket, plus 1. Open the brackets: 6 P minus 3 equals 2 P plus 9. Take 2 P from both sides: 4 P minus 3 equals 9. Add 3 to both sides: 4 P equals 12. Divide by 4: P equals 3."],
        "steps": [N, N, N, "Check with P as 6: 7 times 14 equals 98, and 4 times 23, plus 6, equals 98. Both sides match."],
    },
    "EXT_G4_FP_2023_028": {
        "q": "If m plus n equals 18, n plus p equals 24, and m plus p equals 36, find the value of p.",
        "hints": [N, N, "A similar example: A plus b equals 10, b plus c equals 14, and A plus c equals 12. Find c. Adding all three gives 36, which is twice A plus b plus c. So A plus b plus c is 18. Take away A plus b, which is 10, to get c equals 8."],
    },
    "EXT_G4_FP_2024_012": {
        "q": "Find y: 16 y minus 36 equals 4 y plus, open bracket, 8 times 9, close bracket.",
        "hints": [N, N, "A similar example: 10 y minus 12 equals 4 y plus, open bracket, 6 times 5, close bracket. The bracket is 30. Take 4 y from both sides: 6 y minus 12 equals 30. Add 12 to both sides: 6 y equals 42. Divide by 6: y equals 7."],
    },
    "EXT_G4_FP_2024_028": {
        "q": "The sum of two consecutive odd numbers is 16. What is the sum of their squares?",
        "hints": [N, N, "A similar example: two consecutive odd numbers add up to 8. Half of 8 is 4, so the numbers are 3 and 5. Their squares are 3 times 3, which is 9, and 5 times 5, which is 25. Then 9 plus 25 equals 34."],
    },
    "EXT_G4_FP_2024_037": {
        "q": "12 x minus 19 equals 53. Find the value of 5 x plus 29.",
    },
    "EXT_G4_FP_2025_020": {
        "q": "Find the value of m: 4 m over 3, plus 17, equals 2 m plus 3.",
    },
    "EXT_G4_FP_2025_035": {
        "q": "If 3 m plus 7 equals 28, find the value of 2 m plus 25.",
    },
    "PYQ_2016_Q07": {
        "q": "If m equals 21, and n equals 3, and m equals n times p, find the value of m divided by p.",
    },
    "PYQ_2018_Q25": {
        "q": "If 19 over star, plus 17 over star, equals 2, then what same number does the star represent?",
        "hints": [N, N, "A similar example: 13 over star, plus 11 over star, equals 3. Add the tops: 13 plus 11 equals 24. So 24 divided by the star is 3, and the star is 24 divided by 3, which is 8."],
        "steps": [N, N, "Check by putting 18 in place of the star. 19 over 18, plus 17 over 18, equals 36 over 18, which is 2."],
    },
    "PYQ_2018_Q31": {
        "q": "Tom has 100 marbles and four boxes. He puts the marbles in the four boxes, such that each box has 2 more marbles than the one before. The total marbles in the first 3 boxes are?",
    },
    "PYQ_2019_Q29": {
        "q": "Find the value of the variable T, when 31 minus T equals 2 T plus 7.",
    },
    "G4A_EQUATIONS_009": {
        "q": "In these two sums, the star stands for one number and the triangle stands for another number. Star plus star equals 18, and star plus triangle equals 14. What number does the triangle stand for?",
        "hints": [N, "Star plus star equals 18 means two equal numbers add to 18. Find the star first.",
                  "A similar one: star plus star equals 12, and star plus triangle equals 10. Then star equals 6, and triangle equals 10 minus 6, which is 4."],
        "steps": ["Two equal numbers make 18, so find the star. 18 divided by 2 equals 9.",
                  "Put 9 in the second sum: 9 plus triangle equals 14. 14 minus 9 equals 5.",
                  "The triangle stands for 5."],
    },
    "G4A_EQUATIONS_023": {
        "hints": [N, N, "Similar problem: Mira has 3 times as many stickers as Nita. After each gets 4 more, Mira has twice as many. Try Nita as 4: then Mira has 12, and afterwards they have 8 and 16. 16 is twice 8, so Nita had 4."],
        "steps": ["Test Sonu as 10. Then Ravi has 4 times 10, which is 40 marbles."],
    },
    "G4A_EQUATIONS_028": {
        "hints": [N, N, "Similar problem: 1 box weighs the same as 2 tins and 3 nuts, and 1 tin weighs the same as 2 nuts. Then 1 box is 4 nuts plus 3 nuts, which is 7 nuts, and 3 boxes are 21 nuts."],
    },
    "Q_CH14_001": {
        "q": "Find the value of A: A plus 5 equals 12.",
        "hints": ["To find A, you need to get A alone on one side. What can you do to both sides?"],
        "steps": ["We need to isolate A. Subtract 5 from both sides. A plus 5 minus 5 equals 12 minus 5."],
    },
    "Q_CH14_007": {
        "hints": ["32 divided by g equals 4. If 32 divided by what, equals 4, what number goes in the blank?",
                  "Think: 4 times what, equals 32?"],
    },
    "Q_CH14_014": {
        "q": "Find the value of A: 6 A minus 32 equals 2 A.",
        "hints": ["Get all A terms on one side: subtract 2 A from both sides."],
        "steps": ["Subtract 2 A from both sides: 6 A minus 2 A minus 32 equals 0. So 4 A minus 32 equals 0."],
    },
    "Q_CH14_017": {
        "hints": ["Substitute x equals 5 into each equation, and check which one makes the left side equal the right side.",
                  "A: 3 times 5, plus 2, equals 17, which is not 18. B: 2 times 5, minus 3, equals 7. That is correct. C: 4 times 5, plus 1, equals 21, which is not 20. D: 5 plus 10 equals 15, which is not 16.",
                  "Only B is true: 2 times 5, minus 3, equals 10 minus 3, which is 7. That is correct."],
        "steps": ["Check A: 3 times 5, plus 2, equals 15 plus 2, which is 17. That is not equal to 18.",
                  "Check B: 2 times 5, minus 3, equals 10 minus 3, which is 7, the same as 7. That is correct."],
    },
    "Q_CH14_021": {
        "hints": ["Let brother's age be x. Riya's age is twice brother's age plus 3, which is 2 x plus 3. And Riya is 17."],
    },
    "Q_CH14_025": {
        "hints": ["Let the three consecutive numbers be n, n plus 1, and n plus 2. Their sum equals 36.",
                  "n, plus n plus 1, plus n plus 2, equals 36. So 3 n plus 3 equals 36."],
        "steps": ["Let the numbers be n, n plus 1, and n plus 2. n, plus n plus 1, plus n plus 2, equals 36.",
                  N, N, "Divide by 3: n equals 11. The numbers are 11, 12 and 13."],
    },
}

LINES = {}
