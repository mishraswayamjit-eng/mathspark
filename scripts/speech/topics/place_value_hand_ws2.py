"""Hand-written narration: Grade 5 worksheet questions, second half (place value)."""

PRIMES_2_DIGIT = "11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89 and 97"

HAND = {
    "EXT_G5_WS_01_014": {
        "q": "How many two-digit even numbers have an odd digit in the tens place?",
        "hints": [
            "Two-digit even numbers end in 0, 2, 4, 6 or 8. That is 5 choices. The tens digit must be odd.",
            "The odd digits for the tens place are 1, 3, 5, 7, 9. That is 5 choices. The even digits for the units place are 0, 2, 4, 6, 8. That is 5 choices.",
            "Try this: how many two-digit numbers have 1 in the tens place, and are even? 10, 12, 14, 16, 18. That is 5 numbers.",
        ],
        "steps": [
            "The odd digits for the tens place are 1, 3, 5, 7, 9. That is 5 choices.",
            "The even digits for the units place are 0, 2, 4, 6, 8. That is 5 choices.",
            "The total is 5 times 5. And 5 times 5 equals 25.",
        ],
    },
    "EXT_G5_WS_01_015": {
        "q": "Using the digits 7, 0, 3 and 9, each only once, how many distinct four-digit numbers can be formed?",
        "hints": [
            "For a four-digit number, the first digit cannot be 0.",
            "The thousands place has 3 choices: 7, 3 or 9, but not 0. The remaining 3 digits can go in any order in the other 3 places.",
            "Try this with the digits 1, 0 and 2, making three-digit numbers. The first digit has 2 choices, 1 or 2. Then 2 factorial for the rest. That is 2 times 2, which equals 4.",
        ],
        "steps": [
            "The thousands place cannot be 0, so it has 3 choices: 7, 3 or 9.",
            "The remaining 3 digits fill 3 places in any order. 3 factorial equals 6 arrangements.",
            "The total of four-digit numbers: 3 times 6 equals 18.",
        ],
    },
    "EXT_G5_WS_01_016": {
        "q": "How many four-digit numbers less than 5000 can be formed using the digits 2, 5, 0 and 8, each only once?",
        "hints": [
            "For a number less than 5000, the thousands digit must be less than 5.",
            "From the digits 2, 5, 0 and 8, the digits less than 5 that can be in the thousands place: only 2. Not 0, since that makes a 3-digit number.",
            "With 2 in the thousands place, the remaining digits, 5, 0 and 8, go in 3 factorial, which is 6 arrangements.",
        ],
        "steps": [
            "The thousands digit must be less than 5, and not 0. Only 2 works.",
            "The remaining digits, 5, 0 and 8, can be arranged in 3 factorial ways. 3 factorial equals 6.",
            "The total numbers: 1 times 6 equals 6.",
        ],
    },
    # Source is poor here: hints 2 and 3 think aloud (and hint 2 swaps wrongly), the steps are filler.
    "EXT_G5_WS_B2_011": {
        "q": "If the digits 5 and 6 are interchanged in the number 469571, by how much is the new number more than, or less than, the original number?",
        "hints": [
            "First find where 5 and 6 are in the number 469571, then swap them.",
            "The original is 469571. Swap 5 and 6: 569471. The 5 in hundred-thousands becomes 6, and the 6 in ten-thousands becomes 5. Wait, let me re-examine.",
            "Actually, look at 469571. The 5 is at the hundreds place, worth 500, and the 6 is at ten-thousands, worth 60000. Swapping, 5 goes to ten-thousands, worth 50000, and 6 goes to hundreds, worth 600. The new number is 459671. Need to be more careful.",
        ],
        "steps": [
            "This is a place value and digit manipulation problem. Note the given information.",
            "Apply the relevant formula or method to compute the answer.",
            "The answer is B.",
        ],
    },
    "EXT_G5_WS_B3_010": {
        "q": "In a bundle of notes of 5 rupees denomination, the notes are numbered serially from 40801 to 40901. What is the total amount of money in this bundle?",
        "hints": [
            "How many notes are there from 40801 to 40901?",
            "The count is 40901 minus 40801, plus 1, which is 101 notes. The total is 101 times 5.",
            "Try this: notes from 1 to 5 make 5 notes. 5 times 5 rupees equals 25 rupees.",
        ],
        "steps": [
            "The number of notes is 40901 minus 40801, plus 1, which is 101.",
            "The total amount is 101 times 5, which is 505 rupees.",
            "The answer is option B.",
        ],
    },
    "EXT_G5_WS_B4_018": {
        "q": "In writing all the prime numbers from 1 to 100, how many times is the digit 7 used?",
        "hints": [
            "List all the prime numbers up to 100, then count how many times the digit 7 appears.",
            "The primes are 2, 3, 5, 7, " + PRIMES_2_DIGIT + ". Which contain 7?",
            "A similar example: count the digit 3 in primes up to 50: 3, 13, 23, 31, 37, 43. That's 3, then 13 with one 3, 23 with one 3, 31 with one 3, 37 with one 3, and 43 with one 3. That makes 6 threes.",
        ],
        "steps": [
            "The primes containing the digit 7 are 7, 17, 37, 47, 67, 71, 73, 79 and 97.",
            "Each contains exactly one 7. No prime has two 7s, since 77 equals 7 times 11.",
            "The total count of the digit 7 is 9.",
        ],
    },
    "EXT_G5_WS_B4_019": {
        "q": "How many times is the digit 3 used in writing all the two-digit prime numbers?",
        "hints": [
            "List all the two-digit primes, then count the digit 3 in each.",
            "The two-digit primes are " + PRIMES_2_DIGIT + ".",
            "A similar example: count the digit 1 in two-digit primes: 11, which has two 1s, then 13, 17, 19, 31, 41, 61, 71. The count is 2 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1 plus 1, which equals 9.",
        ],
        "steps": [
            "The two-digit primes with the digit 3 are 13, 23, 31, 37, 43, 53, 73 and 83.",
            "Count the 3s: each has exactly one 3. 33 is not prime.",
            "The total is 8.",
        ],
    },
    "EXT_G5_WS_B4_020": {
        "q": "Using all the one-digit prime numbers, each only once, how many even numbers can be formed?",
        "hints": [
            "One-digit primes are 2, 3, 5 and 7. For an even number, the last digit must be even.",
            "The only even digit among 2, 3, 5 and 7 is 2. So 2 must be in the units place.",
            "With 2 fixed at the units place, the remaining digits, 3, 5 and 7, fill the other 3 positions. 3 factorial equals 6 arrangements.",
        ],
        "steps": [
            "The one-digit primes are 2, 3, 5 and 7. Only 2 is even.",
            "For an even 4-digit number using all four digits, the units digit must be 2.",
            "The remaining 3 digits, 3, 5 and 7, can go in 3 factorial, which is 6 arrangements.",
        ],
    },
}
