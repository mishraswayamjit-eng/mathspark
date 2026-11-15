"""Hand-written narration: past papers 2016 to 2019. None (or a missing key) means 'use the rules'."""

HAND = {
    "EXT_G5_FP_2016_004": {
        "q": "A watch keeps exact time, but it has only the hour hand. When the hour hand is 4 over 5 of the distance between 12 and 1, what is the correct time?",
        "hints": [
            "The hour hand takes one full hour, that is 60 minutes, to go from 12 to 1. So 4 over 5 of the way means 4 over 5 of 60 minutes.",
            "A fraction of a distance is the same fraction of the time taken.",
        ],
        "steps": [
            "From 12 to 1, the hour hand takes 60 minutes.",
            "4 over 5 of 60 is 60 divided by 5, times 4. That is 12 times 4, which equals 48 minutes.",
            "The time is 12 48.",
        ],
    },
    "EXT_G5_FP_2016_012": {
        "q": "Which of the following fractions is greater than 1 over 3, but less than 7 over 8?",
        "hints": [
            "Change everything into 24ths. 1 over 3 and 7 over 8 both fit into 24ths.",
            "Common denominator: the L C M of 3, 8 and the option denominators, which is 24.",
        ],
        "steps": [
            "1 over 3 equals 8 over 24, and 7 over 8 equals 21 over 24. We need a fraction between 8 over 24 and 21 over 24.",
            "1 over 4 equals 6 over 24, which is too small. 23 over 24 is too big. 11 over 12 equals 22 over 24, which is too big.",
            "17 over 24 is between 8 over 24 and 21 over 24. So the answer is 17 over 24.",
        ],
    },
    "EXT_G5_FP_2016_029": {
        "q": "Simplify: 1 over 2, minus 1 over 4, minus 1 over 3, plus 1 over 6.",
        "hints": [
            "Make all the fractions have the same bottom number, the denominator. The L C M of 2, 4, 3 and 6 is 12.",
            "Same denominator first, then add or subtract only the numerators.",
        ],
        "steps": [
            "1 over 2 equals 6 over 12. 1 over 4 equals 3 over 12. 1 over 3 equals 4 over 12. And 1 over 6 equals 2 over 12.",
            "6 minus 3, minus 4, plus 2, all over 12, equals 1 over 12.",
            "The answer is 1 over 12.",
        ],
    },
    "EXT_G5_FP_2017_002": {
        "q": "A water tank is 5 over 6 full. When 30 litres of water are removed from the tank, the tank is 4 over 5 full. How much water does the tank hold when full?",
        "hints": [
            "The 30 litres removed is the difference between the two fractions. Subtract: 5 over 6, minus 4 over 5. Use 30 as the common denominator.",
            "If a fraction of the whole is a known amount, the whole equals the amount divided by the fraction.",
        ],
        "steps": [
            "5 over 6, minus 4 over 5, equals 25 over 30, minus 24 over 30, which is 1 over 30.",
            "1 over 30 of the tank is 30 litres.",
            "The full tank is 30 times 30, which is 900 litres.",
        ],
    },
    "EXT_G5_FP_2017_024": {
        "q": "What is the value of this fraction? On top: 2 over 3, plus 1 over 3. On the bottom: 2 over 3, minus 1 over 3.",
        "hints": [
            "Work out the top and the bottom separately. The fraction line means top divided by bottom.",
            "Add or subtract fractions with the same denominator by combining the numerators.",
        ],
        "steps": [
            "Top: 2 over 3, plus 1 over 3, equals 3 over 3, which is 1.",
            "Bottom: 2 over 3, minus 1 over 3, equals 1 over 3.",
            "1 divided by 1 over 3, equals 1 times 3, which is 3.",
        ],
    },
    "EXT_G5_FP_2018_008": {
        "q": "On a number line, point A is at 1 over 5, and point B is at 1 over 3. Point C is exactly between point A and B. What fraction could be at C?",
        "hints": [
            None,
            "The midpoint equals the first plus the second, all divided by 2.",
        ],
        "steps": [
            "1 over 5 equals 3 over 15, and 1 over 3 equals 5 over 15.",
            "The middle of 3 over 15 and 5 over 15 is 4 over 15, because halfway between 3 and 5 is 4.",
            "C is 4 over 15.",
        ],
    },
    "EXT_G5_FP_2018_013": {
        "q": "Yesterday at a museum, 4 over 5 of the visitors were adults. 120 children visited the museum. 3 over 8 of the adults were male. How many male adults visited the museum?",
        "hints": [
            "If 4 over 5 are adults, what fraction are children? The 120 children are that fraction of all visitors.",
            "The whole equals the part divided by the fraction.",
        ],
        "steps": [
            "Children: 1 minus 4 over 5 equals 1 over 5 of the visitors, which is 120.",
            "All visitors: 120 times 5 equals 600. Adults: 600 minus 120 equals 480.",
            "Male adults: 3 over 8 of 480. That is 480 divided by 8, times 3, which is 180.",
        ],
    },
    "EXT_G5_FP_2018_023": {
        "q": "Simplify: 1, plus 1 over 2, plus 1 over 4, plus 1 over 7, plus 1 over 14, plus 1 over 28.",
        "hints": [
            None,
            "Use the L C M, 28, as the common denominator.",
        ],
        "steps": [
            "1 equals 28 over 28. 1 over 2 equals 14 over 28. 1 over 4 equals 7 over 28. 1 over 7 equals 4 over 28. 1 over 14 equals 2 over 28. And then 1 over 28.",
            "Total: 28 plus 14, plus 7, plus 4, plus 2, plus 1, all over 28. That is 56 over 28, which equals 2.",
        ],
    },
    "EXT_G5_FP_2019_011": {
        "q": "Which of the following fractions is equivalent to 36 over 54?",
        "hints": [
            "Simplify 36 over 54 by dividing top and bottom by the same number. Their H C F is 18. Then check the options.",
            "Equivalent fractions have the same value when simplified.",
        ],
        "steps": [
            "36 over 54 equals 2 over 3, dividing by 18.",
            "14 over 21 equals 2 over 3, dividing by 7. That matches.",
            "The others: 15 over 24 equals 5 over 8. 6 over 14 equals 3 over 7. And 7 over 18 is already simplest. None of these match.",
            "The answer is 14 over 21.",
        ],
    },
    "EXT_G5_FP_2019_019": {
        "hints": [
            "7 over 6 is bigger than 1. For the others, see how far each is from 1: the biggest gap means the smallest fraction.",
            "The gap to 1 equals the denominator minus the numerator, all divided by the denominator.",
        ],
        "steps": [
            "7 over 6 is more than 1, so it's the biggest.",
            "Gaps to 1: 11 over 12 is 1 over 12 short. 10 over 11 is 1 over 11 short. 21 over 22 is 1 over 22 short.",
            "1 over 11 is the largest gap, so 10 over 11 is the smallest.",
        ],
    },
}
