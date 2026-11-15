"""Hand-written narration: worksheet questions 001 to 008. None (or a missing key) means 'use the rules'."""

HAND = {
    "EXT_G5_WS_B7_001": {
        "hints": [
            "A fraction is parts you want, over total equal parts. Here, the parts you want are the ones that are not shaded.",
            None,
            "A similar one: a bar has 6 equal parts, and 4 are shaded. Then 6 minus 4, which is 2, are unshaded. So the unshaded fraction is 2 over 6.",
        ],
        "steps": [
            "The bar is divided into 8 equal parts, so the bottom number of the fraction is 8.",
            "5 parts are shaded, so 8 minus 5, which is 3 parts, are unshaded.",
            "So the unshaded portion is 3 out of 8, which is 3 over 8.",
        ],
    },
    "EXT_G5_WS_B7_002": {
        "q": "The numerator of a fraction is 21, and the denominator is 16 less than the numerator. Express this fraction as a mixed number.",
        "hints": [
            "First find the denominator. 16 less than the numerator means subtract 16 from 21.",
            None,
            "Try a different one: 17 over 3. 17 divided by 3 gives 5 with remainder 2, because 3 times 5 is 15, and 17 minus 15 is 2. So 17 over 3, as a mixed number, is 5 and 2 over 3.",
        ],
        "steps": [
            "The denominator is 16 less than 21. 21 minus 16 equals 5. So the fraction is 21 over 5.",
            "Divide 21 by 5. 5 times 4 is 20, and 21 minus 20 leaves 1 left over.",
            "So there are 4 wholes and 1 fifth left. 21 over 5, as a mixed number, is 4 and 1 over 5.",
        ],
    },
    "EXT_G5_WS_B7_003": {
        "q": "Which of the following is the lowest form of 187 over 136?",
        "hints": [
            "To reach the lowest form, divide the top and the bottom by the same number, until no number other than 1 divides both.",
            "187 and 136 are both multiples of 17. Try dividing each of them by 17.",
            "Try a smaller one: 51 over 34. Both are multiples of 17. 51 divided by 17 is 3, and 34 divided by 17 is 2. So 51 over 34, in lowest form, is 3 over 2.",
        ],
        "steps": [
            "Look for a number that divides both 187 and 136. Both are multiples of 17.",
            "187 divided by 17 equals 11, and 136 divided by 17 equals 8.",
            "11 and 8 share no factor other than 1, so the lowest form of 187 over 136 is 11 over 8.",
        ],
    },
    "EXT_G5_WS_B7_004": {
        "hints": [
            "A portion is a fraction: how many two-digit numbers are perfect squares, over how many two-digit numbers there are.",
            "The two-digit numbers run from 10 to 99. That is 99 minus 9, which is 90 numbers. Now list the two-digit squares, starting with 4 times 4, which is 16, and count them. Write the fraction and simplify it.",
            "A similar one: what portion of the one-digit numbers, 1 to 9, are perfect squares? The squares are 1, 4 and 9. So it is 3 out of 9, which is 3 over 9, or 1 over 3.",
        ],
        "steps": [
            "Two-digit numbers: 90.",
            "Two-digit perfect squares: 16, 25, 36, 49, 64 and 81. That makes 6.",
            "The fraction is 6 over 90, which equals 1 over 15.",
        ],
    },
    "EXT_G5_WS_B7_005": {
        "q": "Which numbers should replace the star and the triangle, in that order? Star over 96, equals 3 over 16, equals 12 over triangle.",
        "options": ["18 and 64", "6 and 4", "18 and 80", "18 and 4"],
        "hints": [
            None,
            "Compare 3 over 16 with star over 96. What was 16 multiplied by to make 96? Multiply 3 by the same number. Then compare 3 over 16 with 12 over triangle. What was 3 multiplied by to make 12?",
            "Try a smaller one: the fractions star over 12, 2 over 3, and 8 over triangle are all equal. 3 times 4 is 12, so star is 2 times 4, which is 8. And 2 times 4 is 8, so triangle is 3 times 4, which is 12.",
        ],
        "steps": [
            None,
            "From 3 over 16 to star over 96: 16 times 6 is 96, so star is 3 times 6, which is 18.",
            "From 3 over 16 to 12 over triangle: 3 times 4 is 12, so triangle is 16 times 4, which is 64.",
            "So star is 18, and triangle is 64.",
        ],
    },
    "EXT_G5_WS_B7_006": {
        "q": "Find the number in place of the asterisk: 45 over 36 equals what, over 32?",
        "hints": [
            "The two fractions are equal. It is easier if you first write 45 over 36 in its lowest form.",
            "Both 45 and 36 are in the 9 times table, so divide top and bottom by 9. Then ask: what must the new bottom number be multiplied by to make 32? Do the same to the top.",
            "Try a smaller one: 6 over 9 and asterisk over 15 are equal. In lowest form, 6 over 9 is 2 over 3. Since 3 times 5 is 15, the asterisk is 2 times 5, which is 10.",
        ],
        "steps": [
            "Write 45 over 36 in lowest form: divide top and bottom by 9, to get 5 over 4.",
            "Now 5 over 4 and asterisk over 32 are equal. 4 times 8 is 32, so multiply the top by 8 as well.",
            "5 times 8 is 40, so the number in place of the asterisk is 40.",
        ],
    },
    "EXT_G5_WS_B7_007": {
        "q": "Find the value of b, if b minus 8, all over 42, equals 5 over 7.",
        "hints": [
            "Two equal fractions. First make 5 over 7 into an equal fraction with 42 at the bottom, so the tops can be compared.",
            "7 times 6 is 42, so multiply the top of 5 over 7 by 6 as well. That number equals b minus 8. To find b, add the 8 back.",
            "Try a smaller one: c minus 2, all over 12, and 3 over 4 are equal. 4 times 3 is 12, so 3 over 4 equals 9 over 12. Then c minus 2 is 9, so c is 11.",
        ],
        "steps": [
            "Make 5 over 7 into a fraction with 42 at the bottom. 7 times 6 is 42, and 5 times 6 is 30, so 5 over 7 equals 30 over 42.",
            "Now b minus 8, all over 42, and 30 over 42 are equal, so the tops are equal: b minus 8 is 30.",
            "Add 8 back: b equals 30 plus 8, which is 38.",
        ],
    },
    "EXT_G5_WS_B7_008": {
        "hints": [
            None,
            "Each part is 2 divided by 5, which is 2 over 5 long. Now count how many parts there are from 0 to point A on the number line, and add up that many parts.",
            "A similar one: a line from 0 to 3 is cut into 4 equal parts. Each part is 3 over 4. A point on the 3rd mark is at 3 over 4, plus 3 over 4, plus 3 over 4, which is 9 over 4.",
        ],
        "steps": [
            "The line from 0 to 2 is cut into 5 equal parts, so each part is 2 divided by 5, which is 2 over 5 long.",
            "Point A is on the 2nd mark after 0, so it is 2 parts away from 0.",
            "2 over 5, plus 2 over 5, equals 4 over 5. So point A represents 4 over 5.",
        ],
    },
}
