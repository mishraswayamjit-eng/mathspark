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
            "Face value is the digit itself. Place value is the digit times the worth of its place: 1, 10, 100, and so on. When could these two be equal in every place?",
            "Test each choice in the tens place. 9 in the tens place is worth 9 times 10, which is 90, and that is not 9. Now test the other digits the same way.",
            "Here is how to test a digit. 4 in the hundreds place has face value 4, but place value 4 times 100, which is 400. They differ, so 4 does not work. Look for a digit that stays the same when multiplied by 10 or 100.",
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
            "Place value is the digit times 1, 10, 100 or 1000, depending on its place. Think about which of these products can ever be odd.",
            "Multiply any digit by 10: the result ends in 0, so it is even. Check what happens with 1000, and with 1, in the same way.",
            "An example: 5 in the hundreds place is worth 5 times 100, which is 500. That is even, even though 5 is odd. So the hundreds place can never give an odd place value. Test the places in the choices like this.",
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
            "Find the place value of 6, and the place value of 2, in 76025. How many times, means you divide the bigger place value by the smaller one.",
            "6 is in the thousands place, so it is worth 6000. 2 is in the tens place, so it is worth 20. Now divide 6000 by 20.",
            "An example: in 8040, the 8 is worth 8000, and the 4 is worth 40. 8000 divided by 40 equals 200. So the place value of 8 is 200 times that of 4.",
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
            "Each step to the left makes a digit worth 10 times more. So for one 8 to be worth 1000 times the other, how many places apart must the two 8s be?",
            "1000 equals 10 times 10 times 10, so the two 8s must be three places apart, like units and thousands, or tens and ten-thousands. In each number, find the places of the two 8s.",
            "An example: in 5052, one 5 is worth 5000, and the other is worth 50. 5000 divided by 50 equals 100, so one is only 100 times the other. Two places apart gives 100 times. You need three places apart.",
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
            "Each step to the left makes a digit worth 10 times more. For one 3 to be worth 100 times the other, how many places apart must the two 3s be?",
            "100 equals 10 times 10, so the two 3s must be two places apart, like tens and thousands. In each number, write down the places of the two 3s.",
            "An example: in 7479, one 7 is worth 7000, and the other is worth 70. 7000 divided by 70 equals 100, so one 7 is 100 times the other. Look for the number where the 3s sit like this.",
        ],
        "steps": [
            "For one 3 to be worth 100 times the other, the two 3s must be two places apart, because 10 times 10 equals 100.",
            "In 134639 the 3s are worth 30000 and 30. 30000 divided by 30 equals 1000, so this is not a match. In 752339 they are worth 300 and 30. 300 divided by 30 equals 10, not a match.",
            "In 307638 the 3s are worth 300000 and 30. 300000 divided by 30 equals 10000, not a match.",
            "In 863135 the 3s are worth 3000 and 30. 3000 divided by 30 equals 100. So the number is 863135.",
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
            "An odd number ends in an odd digit. Which of the digits 5, 8, 0, 7 and 4 are odd? One of them must go in the units place.",
            "To make the number as big as possible, put the biggest digits on the left. Try both ways. End with 5, and arrange 8, 7, 4, 0 from biggest to smallest. Then end with 7, and arrange 8, 5, 4, 0. Which number is greater?",
            "An example with 1, 6, 3: the greatest odd number ends in 1 or 3. Ending in 1 gives 631. Ending in 3 gives 613. 631 is greater, and its middle digit is 3.",
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
            "An even number ends in an even digit. Which of the digits 2, 7, 3, 9 and 6 are even? One of them must go in the units place.",
            "To make the number as small as possible, put the smallest digits on the left. Try both ways. End with 2, and arrange 3, 6, 7, 9 from smallest to biggest. Then end with 6, and arrange 2, 3, 7, 9. Which number is smaller, and where is the 7?",
            "An example with 1, 4, 5: the smallest even number must end in 4, so it is 154. The 5 is in the tens place, so its place value is 5 times 10, which is 50.",
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
