"""Hand-written narration: past papers 2020 to 2025. None (or a missing key) means 'use the rules'."""

HAND = {
    "EXT_G5_FP_2020_019": {
        "q": "If 5 over 8 of the teachers of a coaching class plays chess, 3 over 8 teachers play carrom, and 1 over 4 play both chess and carrom. What fraction of the teachers play neither of the two games?",
        "hints": [
            "Those who play chess or carrom equals chess plus carrom minus both, because the both group is counted twice. Then take it away from the whole, which is 1.",
            "Union equals A plus B minus both. Neither equals 1 minus union.",
        ],
        "steps": [
            "Play chess or carrom: 5 over 8, plus 3 over 8, minus 1 over 4. That is 1 minus 1 over 4, which equals 3 over 4.",
            "Neither equals 1 minus 3 over 4, which is 1 over 4.",
        ],
    },
    "EXT_G5_FP_2021_035": {
        "q": "Solve: open bracket, 1 over 2, minus 1 over 4, plus 1 over 5, minus 1 over 6, close bracket. Divided by: open bracket, 2 over 5, minus 5 over 9, plus 3 over 5, minus 7 over 18, close bracket.",
        "hints": [
            "Solve each square bracket separately, using its own common denominator: 60 for the first, 90 for the second. Then divide. Dividing means multiplying by the flip.",
            "First bracket, the L C D is 60. Second bracket, the L C D is 90. A divided by B equals A times the flip of B.",
        ],
        "steps": [
            "First bracket: 30 minus 15, plus 12, minus 10, all over 60, equals 17 over 60.",
            "Second bracket: 36 minus 50, plus 54, minus 35, all over 90, equals 5 over 90, which is 1 over 18.",
            "17 over 60, divided by 1 over 18, equals 17 over 60, times 18. That is 306 over 60, which equals 5.1.",
            "That equals 5 and 1 over 10.",
        ],
    },
    "EXT_G5_FP_2022_010": {
        "q": "Which of the following fractions should be added to 2 over 5, to get 5 over 2?",
        "hints": [
            "Subtract: 5 over 2, minus 2 over 5. Use 10 as the common denominator.",
            "The missing part equals the total minus the known part.",
        ],
        "steps": [
            "5 over 2 equals 25 over 10, and 2 over 5 equals 4 over 10.",
            "25 over 10, minus 4 over 10, equals 21 over 10.",
        ],
    },
    "EXT_G5_FP_2022_013": {
        "q": "Find the common number in place of each box. 15 and 7 over 17, plus 10 and box over 17, plus 7 and box over 17, plus box over 17, equals 34.",
        "hints": [
            "Add the whole numbers first: 15 plus 10 plus 7. Whatever is left to reach 34 must come from the fractions. Three boxes plus 7, over 17.",
            None,
        ],
        "steps": [
            "Whole parts: 15 plus 10 plus 7 equals 32. So the fractions must add to 34 minus 32, which is 2.",
            "7 plus box, plus box, plus box, all over 17, equals 2, which is 34 over 17. So 7, plus 3 times box, equals 34.",
            "3 times box equals 27. So the box is 9.",
        ],
    },
    "EXT_G5_FP_2023_002": {
        "q": "What is the value of y in: y minus 3 over 4, equals 5 over 12, minus 1 over 3?",
        "hints": [
            "Solve the right side first, using 12 as the common denominator. Then move 3 over 4 across to the other side. Its sign changes.",
            "If y minus A equals B, then y equals B plus A.",
        ],
        "steps": [
            "Right side: 5 over 12, minus 1 over 3, equals 5 over 12, minus 4 over 12, which is 1 over 12.",
            "y equals 1 over 12, plus 3 over 4. That is 1 over 12, plus 9 over 12, which equals 10 over 12.",
            "y equals 5 over 6.",
        ],
    },
    "EXT_G5_FP_2023_008": {
        "q": "What should be multiplied by the sum of 4 over 3 and 5 over 12, to get the final answer as 9 over 7?",
        "hints": [
            "First add 4 over 3 and 5 over 12, with common denominator 12. Then ask: what, times that sum, equals 9 over 7? So the missing number is 9 over 7, divided by the sum.",
            "If A times B equals C, then A equals C divided by B. And dividing by a fraction is the same as multiplying by its flip.",
        ],
        "steps": [
            "The sum: 4 over 3, plus 5 over 12, equals 16 over 12, plus 5 over 12. That is 21 over 12, which equals 7 over 4.",
            "What, times 7 over 4, equals 9 over 7? The missing number is 9 over 7, divided by 7 over 4, which is 9 over 7, times 4 over 7.",
            "That equals 36 over 49.",
        ],
    },
    "EXT_G5_FP_2023_031": {
        "q": "Which of the following fractions is equivalent to 259 over 333?",
        "hints": [
            "Simplify 259 over 333 first. Both numbers are multiples of 37. Then simplify each option too.",
            None,
        ],
        "steps": [
            "259 equals 7 times 37, and 333 equals 9 times 37. So 259 over 333 equals 7 over 9.",
            "148 over 222 equals 2 over 3, no match. 55 over 77 equals 5 over 7, no match. 56 over 108 equals 14 over 27, no match.",
            "77 over 99 equals 7 over 9, a match. So the answer is 77 over 99.",
        ],
    },
}
