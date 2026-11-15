"""Hand-written fixes for past papers 2018 to 2020."""


def S(*texts):
    return [{"text": t, "latex": ""} for t in texts]


HAND = {
    "EXT_G5_FP_2018_007": {
        "steps": S(
            "Test each statement. The supplement of 30° is 180° − 30° = 150°, which is more than 90°. So the first statement is not true.",
            "For an acute angle (between 0° and 90°), the complement is 90° minus the angle, which is also between 0° and 90°. So the second statement is true.",
            "For 30° the complement is 60° and the supplement is 150°. Together they make 210°, not 360°. So the third statement is not true.",
            "So the true statement is: the complementary angle of an acute angle is always an acute angle.",
        ),
        "why": "The last step was filler ('Answer: statement B') and the steps were labelled by letter.",
    },
    "EXT_G5_FP_2018_013": {
        "steps": S(
            "Adults are 4/5 of the visitors, so children are 1 − 4/5 = 1/5 of the visitors.",
            "That 1/5 is 120 children, so there were 5 × 120 = 600 visitors in all.",
            "Adults: 600 − 120 = 480.",
            "Male adults are 3/8 of 480: 480 ÷ 8 = 60, and 3 × 60 = 180.",
            "So 180 male adults visited the museum.",
        ),
        "why": "Steps chained '1 − 4/5 = 1/5 of visitors = 120' and '3/8 of 480 = 480 ÷ 8 × 3', which read as untrue sums.",
    },
    "EXT_G5_FP_2018_024": {
        "hints": [
            "The HCF must divide all three numbers. Start with the smallest, 54: which of the choices divide 54 exactly? Then test those on 288 and 360.",
            "Or break each number into prime factors. 54 = 2 × 3 × 3 × 3. Do the same for 288 and 360, then pick out the primes that all three share.",
            "Try a smaller one: 12 = 2 × 2 × 3, 20 = 2 × 2 × 5 and 28 = 2 × 2 × 7. All three share 2 × 2, so their HCF is 4.",
        ],
        "why": "Hint 2 wrote the factorisations with powers in a form that reads as untrue sums ('288 = 2⁵ × 3²'); there was no third hint.",
    },
    "EXT_G5_FP_2018_025": {
        "steps": S(
            "Find the gain on one dozen: 45 ÷ 15 = 3, so he gains Rs.3 on each dozen.",
            "Now see how many dozens give a gain of Rs.84: 84 ÷ 3 = 28.",
            "So he should sell 28 dozens.",
        ),
        "why": "Step 2 ('Dozens for Rs.84 = 84 ÷ 3 = 28') reads as an untrue sum, and no step stated the answer in words.",
    },
    "EXT_G5_FP_2018_038": {
        "steps": S(
            "Since 2x − 3 is 10, add 3 to find 2x: 2x = 10 + 3 = 13.",
            "4x is double 2x, so 4x = 2 × 13 = 26.",
            "So 4x − 5 is 26 − 5 = 21.",
        ),
        "why": "The steps used arrows and equations that read as untrue sums ('2x − 3 = 10 → 2x = 13').",
    },
    "EXT_G5_FP_2018_040": {
        "steps": S(
            "The number leaves remainder 5, so it divides 167 − 5 = 162 and 95 − 5 = 90 exactly.",
            "The largest number that divides both is their HCF. 162 = 18 × 9 and 90 = 18 × 5, and 9 and 5 share no factor, so the HCF is 18.",
            "A divisor must be bigger than its remainder, and 18 is bigger than 5. Check: 18 × 9 + 5 = 167 and 18 × 5 + 5 = 95.",
            "So the number is 18.",
        ),
        "why": "Step 2 wrote the factorisations with powers in a form that reads as untrue sums ('162 = 2 × 3⁴').",
    },
    "EXT_G5_FP_2019_024": {
        "steps": S(
            "Perimeter of an equilateral triangle = 3 × side, and perimeter of a square = 4 × side. Test each pair.",
            "E = 9, S = 9: 3 × 9 = 27 but 4 × 9 = 36. E = 8, S = 9: 3 × 8 = 24 but 4 × 9 = 36. Not equal.",
            "E = 12, S = 10: 3 × 12 = 36 but 4 × 10 = 40. Not equal.",
            "E = 16, S = 12: 3 × 16 = 48 and 4 × 12 = 48. Equal.",
            "So the perimeters are equal when E = 16 and S = 12.",
        ),
        "why": "The steps were labelled by option letter and two of them gave bare numbers without the working.",
    },
    "EXT_G5_FP_2019_027": {
        "steps": S(
            "An hour has 60 minutes, so 12 minutes is 12/60 of an hour.",
            "Simplify: 12/60 = 1/5.",
            "As a decimal, 1/5 = 2/10 = 0.2, which is the same as 0.20.",
            "So 12 minutes is 0.20 of an hour.",
        ),
        "why": "The solution was a single line.",
    },
    "EXT_G5_FP_2019_033": {
        "hints": [
            "A number that divides both 513 and 456 also divides their difference. So start by subtracting.",
            "Work out 513 − 456. The HCF must be a factor of that difference. Test the difference itself first: does it divide both numbers exactly?",
            "Try a smaller one: for 35 and 28 the difference is 7. 7 divides both 35 and 28 exactly, so their HCF is 7.",
        ],
        "why": "Hint 1 stated the answer ('513 − 456 = 57 ... test whether 57 divides both'); there was no third hint.",
    },
    "EXT_G5_FP_2020_021": {
        "hints": [
            "Her answer is how many times too big? Compare 20 with 2. Then do the opposite to put it right.",
            "20 is 10 times as big as 2, so her answer is 10 times too big. What undoes multiplying by 10? Then look for a choice that does the same job.",
            "Remember that dividing can be written as multiplying by a decimal. For example, dividing by 4 is the same as multiplying by 0.25, because 0.25 is one quarter.",
        ],
        "why": "Hint 2 stated the answer ('same as × 0.1'); there was no third hint.",
    },
    "EXT_G5_FP_2020_024": {
        "hints": [
            "He should be paid only for the days he worked. Find the pay for ONE day first: 27000 ÷ 30.",
            "Then multiply one day's pay by the 18 days he worked.",
            "Try a smaller one: Rs.1000 for 10 days is Rs.100 a day. For 4 days of work the pay is 4 × 100, which is Rs.400.",
        ],
        "why": "Hint 1 was flagged for its wording ('actually') and hint 2 only named the method; there was no third hint.",
    },
    "EXT_G5_FP_2020_026": {
        "steps": S(
            "Start inside the round bracket. Multiply first: 2 × 10 = 20, then 25 − 20 = 5.",
            "'Of' means multiply, so 3 of 5 is 3 × 5 = 15.",
            "Now the square bracket: 5 + 15 = 20.",
            "Finally, 778 − 20 = 758.",
        ),
        "why": "Step 2 wrote '3 of 5 = 3 × 5 = 15', which reads as an untrue sum (5 = 15), and the steps used arrows.",
    },
    "EXT_G5_FP_2020_029": {
        "hints": [
            "Break each number into prime factors, or test each choice: does it divide all three numbers exactly?",
            "The digits of each number add up to 9, so each one can be divided by 3, and then by 3 again. Count how many 3s each number contains.",
            "Try a smaller one: 36 = 2 × 2 × 3 × 3 and 45 = 3 × 3 × 5. They share 3 × 3, so their HCF is 9.",
        ],
        "steps": S(
            "Break each number into prime factors: 513 = 3 × 3 × 3 × 19 and 1134 = 2 × 3 × 3 × 3 × 3 × 7.",
            "And 1215 = 3 × 3 × 3 × 3 × 3 × 5.",
            "The only prime in all three is 3, and each number has at least three 3s: 3 × 3 × 3 = 27.",
            "So the HCF is 27.",
        ),
        "why": "Hint 2 gave the whole factorisation in a form that reads as untrue sums ('1134 = 2 × 3⁴ × 7'), and the steps relied on it.",
    },
    "EXT_G5_FP_2020_032": {
        "steps": S(
            "Work in two stages. First, 5% of Rs.100 is Rs.5.",
            "Now find 5% of Rs.5: 5 × 5 ÷ 100 = 0.25.",
            "So the answer is Rs.0.25.",
        ),
        "why": "Step 2 wrote '5% of 5 = 5 × 5 ÷ 100 = 0.25', which reads as an untrue sum (5 = 0.25).",
    },
    "EXT_G5_FP_2020_033": {
        "steps": S(
            "Try real numbers. 7 leaves remainder 2 when divided by 5, and 9 leaves remainder 4. So take X as 7 and Y as 9.",
            "Then X + Y is 7 + 9 = 16.",
            "16 is 3 fives (15) and 1 more, so the remainder is 1.",
            "It works for any such numbers: the remainders add to 2 + 4 = 6, and 6 is one five and 1 more. So the remainder is 1.",
        ),
        "why": "Step 2 wrote '16 ÷ 5 = 3 remainder 1', which is not a true sum as written.",
    },
}
