"""Hand-written narration: Grade 5 worksheet questions (place value).

Where a step is only a label ("Divide", "Find the difference") its maths line is read
after it, which the checker allows.
"""

HAND = {
    "EXT_G5_WS_01_001": {
        "q": "How many tens form six hundred hundreds?",
        "hints": [
            "First figure out what six hundred hundreds means as a single number.",
            "Six hundred hundreds is 600 times 100, which is 60,000. Now divide by 10 to find how many tens.",
            "A simpler example: how many tens in two hundred? 200 divided by 10 equals 20 tens. Now do 60,000 divided by 10.",
        ],
        "steps": [
            "Find the value of six hundred hundreds.",
            "Divide by 10 to convert to tens.",
        ],
    },
    "EXT_G5_WS_01_002": {
        "q": "Which of the following digits has the same place value and face value, irrespective of the place it is in?",
        "hints": [
            "Think about what happens when you put each digit in different places: tens, hundreds, and so on.",
            "Place value equals the digit, times the position value. Face value is the digit itself. Which digit always gives the same result?",
            "Try 0 in the tens place. Its place value is 0 times 10, which is 0, and its face value is 0. They match! For 9 in the tens place, 90 is not equal to 9.",
        ],
        "steps": [
            "Face value is the digit itself. Place value equals the digit, times the position value.",
            "For 0: 0 times any position is 0. The face value is 0. They always match.",
            "So 0 always has the same place value and face value.",
        ],
    },
    "EXT_G5_WS_01_003": {
        "q": "If the place value of a digit is an odd number, which place is that digit in?",
        "hints": [
            "Think about what happens when you multiply any digit by 10, 100 or 1000. Is the result ever odd?",
            "The tens place value is always a multiple of 10, so it is even. The hundreds place value is always a multiple of 100, so it is even.",
            "Try 3 in the tens place: that gives 30, which is even. 7 in the units place gives 7, which is odd. Only the units place can give odd values.",
        ],
        "steps": [
            "The place value in the tens place is the digit times 10, which is always even.",
            "The place value in the hundreds or thousands place is the digit times 100 or 1000, which is always even.",
            "The place value in the units place is the digit times 1, which is the digit itself. This can be odd.",
            "Only the units place can produce an odd place value.",
        ],
    },
    "EXT_G5_WS_01_004": {
        "q": "In the number 69512, what is the difference between the digits that have the greatest and the least place values?",
        "hints": [
            "Identify which digit is in the highest place, the ten-thousands, and which is in the lowest, the units.",
            "In 69512, the digit in the ten-thousands place is 6, and the digit in the units place is 2.",
            "A simpler example: in 853, the digit in the hundreds place, the highest, is 8. The digit in the units place, the lowest, is 3. The difference is 8 minus 3, which is 5.",
        ],
        "steps": [
            "The digit in the greatest place, the ten-thousands, is 6.",
            "The digit in the least place, the units, is 2.",
            "Find the difference: 6 minus 2 equals 4.",
        ],
    },
    "EXT_G5_WS_01_005": {
        "q": "In the number 76025, how many times is the place value of 6 to that of 2?",
        "hints": [
            "Find the place value of 6, and the place value of 2, separately in 76025.",
            "6 is in the thousands place, so its place value is 6000. 2 is in the tens place, so its place value is 20.",
            "Try this: in 5030, the place value of 5 is 5000, and the place value of 3 is 30. The ratio is 5000 divided by 30.",
        ],
        "steps": [
            "The place value of 6, in the thousands place: 6 times 1000 equals 6000.",
            "The place value of 2, in the tens place: 2 times 10 equals 20.",
            "Divide: 6000 divided by 20 equals 300.",
        ],
    },
    "EXT_G5_WS_01_006": {
        "q": "The digit 8 is used twice in each of the following numbers. In which number is the place value of one 8, a thousand times that of the other 8?",
        "hints": [
            "For one 8 to be 1000 times the other, the two 8s must be exactly 3 place-positions apart.",
            "3 positions apart means units and thousands, or tens and ten-thousands.",
            "Check 85168. 8 is in the ten-thousands place, worth 80000, and in the units place, worth 8. 80000 divided by 8 is 10000. Check 68815. 8 is in the thousands place, worth 8000, and the hundreds place, worth 800. 8000 divided by 800 is 10.",
        ],
        "steps": [
            "Check 68815. The 8s are in the thousands place, worth 8000, and the hundreds place, worth 800. 8000 divided by 800 is 10, not 1000.",
            "Check 65818. The 8s are in the hundreds place, worth 800, and the units place, worth 8. 800 divided by 8 is 100, not 1000.",
            "Check 81586. The 8s are in the ten-thousands place, worth 80000, and the tens place, worth 80. 80000 divided by 80 is 1000. That works.",
            "This is the one where one 8 is 1000 times the other: 81586.",
        ],
    },
    "EXT_G5_WS_01_007": {
        "q": "In which of the following is the place value of one 3, a hundred times that of the other 3 in the same number?",
        "hints": [
            "For one 3 to be 100 times the other, the two 3s must be exactly 2 place-positions apart.",
            "2 positions apart means units and hundreds, or tens and thousands, or hundreds and ten-thousands.",
            "Check each number: find where the two 3s are, and compare their place values.",
        ],
        "steps": [
            "Check 134639. There is a 3 in the ten-thousands place, worth 30000, and a 3 in the tens place, worth 30. 30000 divided by 30 is 1000, not 100.",
            "Check 752339. There is a 3 in the hundreds place, worth 300, and a 3 in the tens place, worth 30. 300 divided by 30 is 10, not 100.",
            "Check 863135. There is a 3 in the thousands place, worth 3000, and a 3 in the tens place, worth 30. 3000 divided by 30 is 100. That works.",
            "This is the answer: 863135.",
        ],
    },
    "EXT_G5_WS_01_011": {
        "q": "What is the successor of the greatest four-digit number formed by using the digits 1, 5, 0 and 8, each only once?",
        "hints": [
            "First, form the greatest four-digit number using 1, 5, 0 and 8, each once.",
            "To make the greatest number, arrange the digits in descending order: 8, 5, 1, 0. That gives 8510.",
            "Try this: the greatest 3-digit number with 3, 7 and 1 is 731. Its successor is 732.",
        ],
        "steps": [
            "Arrange the digits in descending order for the greatest number: 8, 5, 1, 0. That gives 8510.",
            "Find the successor, by adding 1: 8510 plus 1 equals 8511.",
        ],
    },
    "EXT_G5_WS_01_012": {
        "q": "Which digit is exactly in the middle of the greatest odd number formed by using the digits 5, 8, 0, 7 and 4, each only once?",
        "hints": [
            "First form the greatest odd number with 5, 8, 0, 7 and 4, each used once. It must end in an odd digit.",
            "For the greatest odd number, start with the largest digits, and end with the largest odd digit. The options for the units place are 5 or 7. With 5 at the end: 87405. With 7 at the end: 85407. Compare: 87405 is greater than 85407.",
            "The greatest is 87405. The middle digit, the 3rd, is 4. Check again: 8, 7, 4, 0, 5. The middle is 4. But one option is 5. Ending in 7 gives 85407, with middle 4. Ending in 5 gives 87405, with middle 4.",
        ],
        "steps": [
            "The greatest odd number must end in an odd digit, 5 or 7.",
            "Try ending in 5. The remaining digits, 8, 7, 4, 0, in descending order, give 87405.",
            "Try ending in 7. The remaining digits, 8, 5, 4, 0, in descending order, give 85407.",
            "87405 is greater than 85407, so the greatest odd number is 87405.",
            "The middle digit, the 3rd, of 87405 is 4.",
        ],
    },
    "EXT_G5_WS_01_013": {
        "q": "What is the place value of 7, in the smallest even number formed by using the digits 2, 7, 3, 9 and 6, each only once?",
        "hints": [
            "Form the smallest even number using 2, 7, 3, 9 and 6. It must end in an even digit.",
            "The even digits available are 2 and 6. For the smallest number, start with the smallest digits. If it ends in 2, you get 36792. If it ends in 6, you get 23796.",
            "23796 is less than 36792, so the smallest even number is 23796. Where is 7? In the hundreds place. Its place value is 700.",
        ],
        "steps": [
            "The smallest even number must end in an even digit: 2 or 6.",
            "Ending in 2, arrange the rest in ascending order. That gives 36792.",
            "Ending in 6, arrange the rest in ascending order. That gives 23796.",
            "23796 is less than 36792, so the smallest even number is 23796.",
            "7 is in the hundreds place. Its place value is 700.",
        ],
    },
}
