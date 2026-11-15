"""Hand-written narration: past papers 2020 to 2025. None (or a missing key) means 'use the rules'."""

HAND = {
    "EXT_G5_FP_2020_019": {
        "q": "If 5 over 8 of the teachers of a coaching class play chess, 3 over 8 of the teachers play carrom, and 1 over 4 play both chess and carrom, what fraction of the teachers play neither of the two games?",
        "hints": [
            None,
            "Add the chess and carrom fractions, 5 over 8 plus 3 over 8. Then take away the 1 over 4 who were counted twice. That gives the fraction who play at least one game.",
            "A similar one: 1 over 2 of a class like apples, 1 over 3 like mangoes, and 1 over 6 like both. At least one fruit: 1 over 2, plus 1 over 3, minus 1 over 6, equals 2 over 3. Neither fruit: 1 minus 2 over 3, which is 1 over 3.",
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
            "First bracket, in sixtieths: 30 minus 15, plus 12, minus 10, all over 60, equals 17 over 60.",
            "Second bracket, in ninetieths: 36 minus 50, plus 54, minus 35, all over 90, equals 5 over 90, which simplifies to 1 over 18.",
            "Dividing by 1 over 18 is the same as multiplying by 18. 17 over 60, times 18, equals 306 over 60.",
            "306 over 60 equals 51 over 10, which is the mixed number 5 and 1 over 10.",
        ],
    },
    "EXT_G5_FP_2022_010": {
        "q": "Which of the following fractions should be added to 2 over 5, to get 5 over 2?",
        "hints": [
            "Something is added to 2 over 5 to make 5 over 2. To find the missing part, subtract 2 over 5 from 5 over 2.",
            "To subtract, give both fractions the same denominator: a number that both 5 and 2 divide into.",
            "Try a smaller one: what must be added to 1 over 2 to get 3 over 4? 3 over 4, minus 1 over 2, equals 3 over 4, minus 2 over 4, which is 1 over 4.",
        ],
        "steps": [
            "5 over 2 equals 25 over 10, and 2 over 5 equals 4 over 10.",
            "25 over 10, minus 4 over 10, equals 21 over 10.",
        ],
    },
    "EXT_G5_FP_2022_013": {
        "q": "Find the common number in place of each box. 15 and 7 over 17, plus 10 and box over 17, plus 7 and box over 17, plus box over 17, equals 34.",
        "hints": [
            "Add the whole numbers first: 15 plus 10 plus 7. Whatever is still needed to reach 34 must come from the four fractions.",
            None,
            "Try a smaller one: 1 and 1 over 5, plus 2 and box over 5, plus box over 5, makes 4. The whole numbers make 3, so the fifths must make 1, which is 5 over 5. Then 1 and two boxes make 5, so each box is 2.",
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
