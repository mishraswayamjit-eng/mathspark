"""Hand-written fixes for past papers 2024 and 2025."""


def S(*texts):
    return [{"text": t, "latex": ""} for t in texts]


HAND = {
    "EXT_G5_FP_2024_001": {
        "steps": S(
            "Area of the square: 56 × 56 = 3136 sq.cm.",
            "The rectangle has the same area, so its length is 3136 ÷ 49 = 64 cm.",
            "Perimeter of the rectangle: 2 × (64 + 49) = 2 × 113 = 226 cm.",
            "226 cm is not one of the choices given, so the answer is \"None of these\".",
        ),
        "why": "The last step reasoned from option letters ('not in options A–C').",
    },
    "EXT_G5_FP_2024_002": {
        "steps": S(
            "A 10% profit means Rs.440 is 110% of the cost price.",
            "So 1% of the cost price is 440 ÷ 110 = 4, and the cost price is 100 × 4 = 400, that is Rs.400.",
            "For a 17% profit the selling price is 117% of the cost price: 117 × 4 = 468.",
            "So it should be sold for Rs.468.",
        ),
        "why": "Step 2 wrote '117% of 400 = 117 × 4 = Rs.468', which reads as an untrue sum (400 = 468); the steps used arrows.",
    },
    "EXT_G5_FP_2024_009": {
        "steps": S(
            "Dividing by 9/4 is the same as multiplying by 4/9. So the bracket is 3/4 × 4/9 = 12/36, which simplifies to 1/3.",
            "So 1/3 of A is 9/4.",
            "A is 3 times as much: 3 × 9/4 = 27/4.",
            "So the fraction in place of A is 27/4.",
        ),
        "why": "Step 1 wrote '3/4 ÷ 9/4 = 3/4 × 4/9', which read left to right is not a true sum.",
    },
    "EXT_G5_FP_2024_012": {
        "steps": S(
            "Put d = 6 into both sides of each statement and see whether the two sides match.",
            "5d + 19 = 7d − 17: the left side is 30 + 19 = 49, the right side is 42 − 17 = 25. Not equal.",
            "8 + 4d = 6d − 6: the left side is 8 + 24 = 32, the right side is 36 − 6 = 30. Not equal.",
            "12d − 14 = 16 + 7d: the left side is 72 − 14 = 58, the right side is 16 + 42 = 58. Equal.",
            "So the true statement is 12d − 14 = 16 + 7d.",
        ),
        "why": "The steps were labelled by option letter ('Option A: ...').",
    },
    "EXT_G5_FP_2024_030": {
        "hints": [
            "Work out the left side and the right side of each statement separately, then see whether they are equal.",
            "A quick first test: look only at the last digits. The last digit of the sum on the left must match the last digit of the square on the right.",
            "For example, is 6² + 8² equal to 10²? 36 + 64 = 100 and 10 × 10 = 100, so yes. Test each statement like this.",
        ],
        "steps": S(
            "8² + 12²: 64 + 144 = 208, but 15² is 225. Not equal.",
            "11² + 59²: 121 + 3481 = 3602, but 60² is 3600. Not equal.",
            "13² + 84²: 169 + 7056 = 7225, but 87² is 7569. Not equal.",
            "12² + 35²: 144 + 1225 = 1369, and 37² is 37 × 37 = 1369. Equal.",
            "So the true statement is 12² + 35² = 37².",
        ),
        "why": "Hint 2 listed the answer among 'Pythagorean triples'; the steps were labelled by option letter.",
    },
    "EXT_G5_FP_2024_036": {
        "steps": S(
            "Try ×, −, ÷: 3 ÷ 14 is not a whole number, so 12 × 6 − 3 ÷ 14 cannot be 16.",
            "Try −, ÷, +: 12 − 6 ÷ 3 + 14 = 12 − 2 + 14 = 24. That is not 16.",
            "Try ×, ÷, +: 12 × 6 ÷ 3 + 14 = 24 + 14 = 38. That is not 16.",
            "Try +, ×, −: 12 + 6 × 3 − 14 = 12 + 18 − 14 = 16. This one works.",
            "So the signs are +, × and −, in that order.",
        ),
        "why": "The steps were labelled by option letter, and one wrote an untrue sum ('= 72 − 0.21…').",
    },
    "EXT_G5_FP_2025_017": {
        "steps": S(
            "First find q: q = 2 × 7 − 9 = 14 − 9 = 5.",
            "2p − 3q + 5 is 14 − 15 + 5 = 4, and 4q − 2p is 20 − 14 = 6.",
            "p + q − 12 is 7 + 5 − 12 = 0, and 7q − 5p + 3 is 35 − 35 + 3 = 3.",
            "The four values are 4, 6, 0 and 3. The greatest is 6.",
            "So the expression with the greatest value is 4q − 2p.",
        ),
        "why": "Six steps labelled by option letter; the limit is five and the working should name the expressions.",
    },
    "EXT_G5_FP_2025_020": {
        "steps": S(
            "1% of 800 is 8, so 6.5% of 800 is 6.5 × 8 = 52.",
            "1% of 250 is 2.5, so 8% of 250 is 8 × 2.5 = 20.",
            "So 52 = 20 + M, which gives M = 52 − 20 = 32.",
        ),
        "why": "Steps wrote '6.5% of 800 = 6.5 × 8 = 52', which reads as an untrue sum (800 = 52).",
    },
    "EXT_G5_FP_2025_024": {
        "steps": S(
            "A 35% loss means Rs.78 is only 65% of the cost price, because 100 − 35 = 65.",
            "So 1% of the cost price is 78 ÷ 65 = 1.2, and the cost price is 100 × 1.2 = 120, that is Rs.120.",
            "For a 15% profit the selling price is 115% of the cost price: 115 × 1.2 = 138.",
            "So it should be sold for Rs.138.",
        ),
        "why": "Step 2 wrote '115% of 120 = 115 × 1.2 = Rs.138', which reads as an untrue sum (120 = 138); the steps used arrows.",
    },
    "EXT_G5_FP_2025_027": {
        "steps": S(
            "Make the units match. 24 m/s in km/h is 24 × 18 ÷ 5 = 86.4 km/h.",
            "Time = Distance ÷ Speed: 432 ÷ 86.4 = 5 hours.",
            "5 hours is not one of the choices given, so the answer is \"None of these\".",
        ),
        "why": "The last step reasoned from option letters ('not among options A–C').",
    },
    "EXT_G5_FP_2025_031": {
        "hints": [
            "Work out each pair of squares and add them. Does the total match the number on the right?",
            "Start with the smallest numbers: 7² is 49 and 11² is 121. Add them and compare with 150. Then do the same for the other three statements.",
            "For example, to test whether 5² + 12² makes 169: 25 + 144 = 169, so that statement would be true.",
        ],
        "why": "Hint 2 worked through the answer's own numbers (18² and 23²); there was no third hint.",
    },
    "EXT_G5_FP_2025_032": {
        "steps": S(
            "Find the gaps between the terms: 197 − 193 = 4, 193 − 185 = 8, 185 − 173 = 12, 173 − 157 = 16.",
            "The gaps grow by 4 each time, so the next gaps are 20, 24 and 28.",
            "6th term: 157 − 20 = 137. 7th term: 137 − 24 = 113.",
            "8th term: 113 − 28 = 85.",
        ),
        "why": "Step 1 wrote the gaps as '197→193 = −4', which reads as an untrue sum.",
    },
    "EXT_G5_FP_2025_035": {
        "hints": [
            "Without brackets the left side comes to 57, which is too big. A bracket around part of the divisor makes you divide by a bigger number.",
            "A bracket changes the order: whatever is inside it is worked out first. Try each choice and work the sum through.",
            "Try a smaller one: 24 ÷ 2 × 3 = 36, but with a bracket 24 ÷ (2 × 3) = 24 ÷ 6 = 4. The bracket changed the answer.",
        ],
        "steps": S(
            "Without brackets: 192 ÷ 12 × 3 − 4 + 13 = 48 − 4 + 13 = 57. That is not 19, so a bracket is needed.",
            "Bracket (12 × 3): 192 ÷ 36 is not a whole number, so the result cannot be 19.",
            "Bracket (3 − 4 + 13): 3 − 4 + 13 = 12, and 192 ÷ 12 × 12 = 192. That is not 19.",
            "Bracket (12 × 3 − 4): 12 × 3 − 4 = 32, then 192 ÷ 32 + 13 = 6 + 13 = 19. This one works.",
            "So the bracket goes around 12 × 3 − 4.",
        ),
        "why": "Hint 1 said the sum without brackets is 61 (it is 57); the steps were labelled by option letter and one wrote an untrue sum.",
    },
}
