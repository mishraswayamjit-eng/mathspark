"""Hand-written narration: past papers 2024 and 2025. None (or a missing key) means 'use the rules'."""

HAND = {
    "EXT_G5_FP_2024_009": {
        "q": "Open bracket, 3 over 4, divided by 9 over 4, close bracket, times A, equals 9 over 4. Find the fraction in place of A.",
        "hints": [
            "Solve the bracket first: dividing by a fraction means multiplying by its flip, the reciprocal.",
            "A over B, divided by C over D, equals A over B, times D over C. If X times A equals Y, then A equals Y divided by X.",
        ],
        "steps": [
            "Dividing by 9 over 4 is the same as multiplying by 4 over 9. So the bracket is 3 over 4, times 4 over 9, which equals 12 over 36. That simplifies to 1 over 3.",
            "So 1 over 3 of A is 9 over 4.",
            "A is 3 times as much: 3 times 9 over 4 equals 27 over 4.",
            "So the fraction in place of A is 27 over 4.",
        ],
    },
    "EXT_G5_FP_2024_021": {
        "hints": [
            "Which fractions are close to 1, and which are close to one half? For the close ones, see how much each is short of 1.",
            "Fractions with a smaller gap to 1 are bigger. The gap equals the denominator minus the numerator, all divided by the denominator.",
        ],
        "steps": [
            "9 over 19 and 10 over 21 are less than one half, so they are small.",
            "Gap to 1: 15 over 17 is short by 2 over 17. 11 over 13 is short by 2 over 13.",
            "2 over 17 is smaller than 2 over 13, so 15 over 17 is closest to 1.",
            "Decimals check: 0.882 against 0.846. So the greatest is 15 over 17.",
        ],
    },
    "EXT_G5_FP_2024_031": {
        "q": "If the given two fractions are equivalent, then what number should replace the box? 52 over 68 equals box over 153.",
        "hints": [
            "Simplify 52 over 68 first, by dividing both numbers by 4. Then ask: what do I multiply 17 by to get 153?",
            "Equivalent fractions: multiply, or divide, top and bottom by the same number.",
        ],
        "steps": [
            "52 over 68 equals 13 over 17, dividing by 4.",
            "153 divided by 17 equals 9, so multiply the top by 9 too.",
            "13 times 9 equals 117.",
        ],
    },
    "EXT_G5_FP_2025_014": {
        "q": "3 over 4, 5 over 6, and 4 over 5. Out of the given fractions, what is the difference between the greatest and the smallest fraction?",
        "hints": [
            "Make all three fractions have the same denominator, the L C M of 4, 6 and 5. Then compare the tops.",
            None,
        ],
        "steps": [
            "The L C M of 4, 6 and 5 is 60.",
            "3 over 4 equals 45 over 60. 5 over 6 equals 50 over 60. 4 over 5 equals 48 over 60.",
            "The greatest is 50 over 60. The smallest is 45 over 60.",
            "The difference is 5 over 60, which equals 1 over 12.",
        ],
    },
    "EXT_G5_FP_2025_018": {
        "q": "If 12 over 52 equals y over 13, which equals m over 39. Find the value of m minus y.",
        "hints": [
            "Simplify 12 over 52 by dividing top and bottom by 4. Then match the denominators 13 and 39.",
            None,
        ],
        "steps": [
            "12 over 52 equals 3 over 13, dividing by 4. So y equals 3.",
            "3 over 13 equals 9 over 39, multiplying by 3. So m equals 9.",
            "m minus y equals 9 minus 3, which is 6.",
        ],
    },
}
