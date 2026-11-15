"""Hand-written fixes for past papers 2021 to 2023."""


def S(*texts):
    return [{"text": t, "latex": ""} for t in texts]


HAND = {
    "EXT_G5_FP_2021_015": {
        "steps": S(
            "Top: x × y = 3 × (−2) = −6.",
            "Bottom: x − y = 3 − (−2) = 3 + 2 = 5.",
            "Divide the top by the bottom: −6 divided by 5 is the fraction −6/5.",
        ),
        "why": "The last step was a tautology ('(−6)/5 = −6/5').",
    },
    "EXT_G5_FP_2021_030": {
        "steps": S(
            "Divide 13601 by 87. The remainder is what must be taken away.",
            "87 × 156 = 13572. That is the largest multiple of 87 that fits into 13601, because the next one, 87 × 157 = 13659, is too big.",
            "13601 − 13572 = 29, so the remainder is 29.",
            "So 29 must be subtracted.",
        ),
        "why": "Step 3 wrote '13601 ÷ 87 = 156 remainder 29', which is not a true sum as written.",
    },
    "EXT_G5_FP_2021_032": {
        "steps": S(
            "One third of one fourth is 1/3 × 1/4 = 1/12. So 1/12 of the number is 15.",
            "The number is 12 × 15 = 180.",
            "Three tenths (3/10) of 180: 180 ÷ 10 = 18, and 3 × 18 = 54.",
            "The square of 54 is 54 × 54 = 2916.",
        ),
        "why": "Step 1 chained '1/3 of 1/4 = 1/12 of the number = 15', which reads as an untrue sum; step 2 skipped its working.",
    },
    "EXT_G5_FP_2021_035": {
        "steps": S(
            "First bracket, in sixtieths: (30 − 15 + 12 − 10)/60 = 17/60.",
            "Second bracket, in ninetieths: (36 − 50 + 54 − 35)/90 = 5/90, which simplifies to 1/18.",
            "Dividing by 1/18 is the same as multiplying by 18: 17/60 × 18 = 306/60.",
            "306/60 = 51/10, which is the mixed number 5 1/10.",
        ),
        "why": "Step 3 wrote '17/60 ÷ 1/18 = 17/60 × 18', which read left to right is not a true sum.",
    },
    "EXT_G5_FP_2021_039": {
        "steps": S(
            "A number that leaves remainder 8 every time is 8 more than a common multiple of 12, 15, 20 and 54. The least such number uses their LCM.",
            "Prime factors: 12 = 2 × 2 × 3, 15 = 3 × 5, 20 = 2 × 2 × 5 and 54 = 2 × 3 × 3 × 3.",
            "Take each prime the most times it appears in any one number: 2 × 2 × 3 × 3 × 3 × 5 = 540. So the LCM is 540.",
            "Add the remainder: 540 + 8 = 548.",
        ),
        "why": "Step 1 packed four factorisations with powers into one line, in a form that reads as untrue sums ('12 = 2² × 3').",
    },
    "EXT_G5_FP_2022_010": {
        "hints": [
            "Something is added to 2/5 to make 5/2. To find the missing part, subtract 2/5 from 5/2.",
            "To subtract, give both fractions the same denominator: a number that both 5 and 2 divide into.",
            "Try a smaller one: what must be added to 1/2 to get 3/4? 3/4 − 1/2 = 3/4 − 2/4 = 1/4.",
        ],
        "why": "Hint 1 named the denominator of the answer; there was no third hint.",
    },
    "EXT_G5_FP_2022_013": {
        "hints": [
            "Add the whole numbers first: 15 + 10 + 7. Whatever is still needed to reach 34 must come from the four fractions.",
            "All four fractions are seventeenths, so add their top numbers: 7 and three equal boxes. How many seventeenths make the amount still needed?",
            "Try a smaller one: 1 1/5 + 2 (□)/5 + (□)/5 makes 4. The whole numbers make 3, so the fifths must make 1, which is 5/5. Then 1 and two boxes make 5, so each box is 2.",
        ],
        "why": "Hint 1 trailed off ('Three boxes plus 7 over 17 …'); there was no third hint.",
    },
    "EXT_G5_FP_2022_017": {
        "steps": S(
            "'Of' means multiply. 5/6 of 72: 72 ÷ 6 = 12, and 12 × 5 = 60.",
            "Inside the bracket: 2/5 of 40 is 16 and 1/9 of 27 is 3, so the bracket is 16 + 3 = 19.",
            "Multiply the bracket by 2: 2 × 19 = 38.",
            "Subtract: 60 − 38 = 22.",
        ),
        "why": "Step 1 wrote '5/6 of 72 = 72 ÷ 6 × 5 = 60', which reads as an untrue sum (72 = 60).",
    },
    "EXT_G5_FP_2022_018": {
        "steps": S(
            "Put Z = 7 into both sides of each equation and see whether the two sides match.",
            "5 + 2Z = 3Z + 2: the left side is 5 + 14 = 19, the right side is 21 + 2 = 23. Not equal.",
            "4Z + 7 = 2Z + 28: the left side is 28 + 7 = 35, the right side is 14 + 28 = 42. Not equal.",
            "5Z + 6 = 7Z − 8: the left side is 35 + 6 = 41, the right side is 49 − 8 = 41. Equal.",
            "So the true equation is 5Z + 6 = 7Z − 8.",
        ),
        "why": "The steps were labelled by option letter ('Option A: ...').",
    },
    "EXT_G5_FP_2022_030": {
        "steps": S(
            "Speed: 600 ÷ 25 = 24 metres every second.",
            "One hour has 3600 seconds, so in 1 hour the car covers 24 × 3600 = 86400 metres.",
            "86400 ÷ 1000 = 86.4, so that is 86.4 km.",
            "86.4 km is not one of the choices given, so the answer is \"None of these\".",
        ),
        "why": "The last step reasoned from option letters ('not among options A–C').",
    },
    "EXT_G5_FP_2022_039": {
        "hints": [
            "Find the HCF (the biggest number that divides both) and the LCM (the smallest number both divide into). Then add them.",
            "Break both into prime factors: 12 = 2 × 2 × 3 and 90 = 2 × 3 × 3 × 5. The HCF uses the primes they share; the LCM uses each prime the most times it appears.",
            "Try a smaller one: 4 = 2 × 2 and 6 = 2 × 3. The HCF is 2 and the LCM is 2 × 2 × 3 = 12, so the sum is 12 + 2 = 14.",
        ],
        "why": "Hint 2 wrote the factorisations with powers in a form that reads as untrue sums ('12 = 2² × 3'); there was no third hint.",
    },
    "EXT_G5_FP_2023_003": {
        "steps": S(
            "First 100 m: 100 ÷ 4 = 25 s. Remaining 300 m: 300 ÷ 5 = 60 s.",
            "One round takes 25 + 60 = 85 s, so five rounds take 85 × 5 = 425 s.",
            "425 s is 7 minutes 5 seconds, because 7 × 60 = 420 and 5 seconds are left.",
            "7 minutes 5 seconds is not one of the choices given, so the answer is \"none of these\".",
        ),
        "why": "The last step reasoned from option letters ('not among options A–C').",
    },
    "EXT_G5_FP_2023_004": {
        "steps": S(
            "Rectangle perimeter: 2 × (22 + 16) = 76 m.",
            "The square has the same perimeter, so its side is 76 ÷ 4 = 19 m.",
            "Area of the square: 19 × 19 = 361 sq.m.",
            "361 sq.m is not one of the choices given, so the answer is \"none of these\".",
        ),
        "why": "The last step jumped to 'none of these' without saying that 361 sq.m is not among the choices.",
    },
    "EXT_G5_FP_2023_007": {
        "steps": S(
            "1% of 150 is 1.5, so 16% of 150 is 16 × 1.5 = 24.",
            "1% of 600 is 6, so 13% of 600 is 13 × 6 = 78.",
            "So Z + 24 = 78, which gives Z = 78 − 24 = 54.",
        ),
        "why": "Steps wrote '16% of 150 = 16 × 1.5 = 24', which reads as an untrue sum (150 = 24).",
    },
    "EXT_G5_FP_2023_009": {
        "steps": S(
            "Interest = Amount − Principal: 10272 − 6420 = 3852, so the simple interest is Rs.3852.",
            "Rate = (SI × 100) ÷ (P × T): 3852 × 100 ÷ (6420 × 4) = 385200 ÷ 25680 = 15.",
            "So the rate is 15% per annum. 15% is not one of the choices given, so the answer is \"none of these\".",
        ),
        "why": "The last step reasoned from option letters ('not among options B–D').",
    },
    "EXT_G5_FP_2023_015": {
        "steps": S(
            "'Of' means multiply: 3/5 of 25 is 15, and 7/13 of 39 is 21.",
            "Inside the bracket: 9 + 15 − 21 = 3.",
            "Dividing by 4/3 is the same as multiplying by 3/4: 3 × 3/4 = 9/4.",
            "9/4 = 2.25, so the answer is 2.25.",
        ),
        "why": "Step 3 wrote '3 ÷ 4/3 = 3 × 3/4', which read left to right is not a true sum.",
    },
    "EXT_G5_FP_2023_021": {
        "steps": S(
            "Since 4x − 7 is 12, add 7 to find 4x: 4x = 12 + 7 = 19.",
            "12x is 3 times 4x, so 12x = 3 × 19 = 57.",
            "So 12x − 14 is 57 − 14 = 43.",
        ),
        "why": "The steps used arrows and equations that read as untrue sums ('4x − 7 = 12 → 4x = 19').",
    },
    "EXT_G5_FP_2023_023": {
        "steps": S(
            "A loss means the cost price is more than the selling price: 336 + 84 = 420, so the cost price is Rs.420.",
            "Sold for Rs.542, the profit is 542 − 420 = 122, that is Rs.122.",
            "Rs.122 is not one of the choices given, so the answer is \"none of these\".",
        ),
        "why": "The last step reasoned from option letters ('not in options A–C').",
    },
    "EXT_G5_FP_2023_032": {
        "steps": S(
            "The loss of Rs.60 is 12% of the cost price. So 1% of the cost price is 60 ÷ 12 = 5, and the cost price is 100 × 5 = 500, that is Rs.500.",
            "Sold at Rs.620, the profit is 620 − 500 = 120, that is Rs.120.",
            "Profit percent: 120 ÷ 500 × 100 = 24, so the profit is 24%.",
            "24% is not one of the choices given, so the answer is \"none of these\".",
        ),
        "why": "The last step reasoned from option letters ('not among options B–D').",
    },
}
