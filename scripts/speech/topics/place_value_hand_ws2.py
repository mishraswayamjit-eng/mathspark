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
            "A four-digit number cannot begin with 0. So think about which digits are allowed in the thousands place.",
            "The thousands place can be 7, 3 or 9: that is 3 choices. After that, count how many ways the other three digits can fill the remaining three places.",
            "An example with 1, 0, 2: a three-digit number can start with 1 or 2. That is 2 choices. The other two digits can then be placed in 2 ways. 2 times 2 equals 4 numbers: 102, 120, 201 and 210.",
        ],
        "steps": [
            "The thousands place cannot be 0, so it can be 7, 3 or 9. That is 3 choices.",
            "The 3 digits left over fill the other three places: 3 choices for the hundreds, then 2 for the tens, then 1 for the units. 3 times 2 times 1 equals 6 ways.",
            "Multiply the choices: 3 times 6 equals 18. So 18 different four-digit numbers can be formed.",
        ],
    },
    "EXT_G5_WS_01_016": {
        "q": "How many four-digit numbers less than 5000 can be formed using the digits 2, 5, 0 and 8, each only once?",
        "hints": [
            "A number less than 5000 must have a thousands digit smaller than 5. And a four-digit number cannot begin with 0.",
            "From 2, 5, 0 and 8, only 2 can go in the thousands place. Now count the ways to arrange 5, 0 and 8 in the other three places.",
            "An example: numbers less than 300, using 1, 4, 6 once each, must start with 1. Then 4 and 6 can go in 2 ways: 146 and 164. So there are 2 such numbers.",
        ],
        "steps": [
            "A number less than 5000 needs a thousands digit below 5, and it cannot be 0. From 2, 5, 0 and 8, only 2 works.",
            "The digits 5, 0 and 8 fill the other three places: 3 choices for the hundreds, then 2 for the tens, then 1 for the units. 3 times 2 times 1 equals 6 ways.",
            "So 6 four-digit numbers less than 5000 can be formed: 2058, 2085, 2508, 2580, 2805 and 2850.",
        ],
    },
    "EXT_G5_WS_B2_011": {
        "q": "If the digits 5 and 6 are interchanged in the number 469571, by how much is the new number more than, or less than, the original number?",
        "hints": [
            "Find the digits 5 and 6 in 469571, and say which place each one is in. Then swap them, and compare the new number with the old one.",
            "The 6 is in the ten-thousands place, and the 5 is in the hundreds place. After the swap, the new number is 459671. Is that bigger or smaller than 469571, and by how much?",
            "A similar one: swap 2 and 7 in 1274, to get 1724. The new number is more, by 1724 minus 1274, which is 450.",
        ],
        "steps": [
            "In 469571 the digit 6 is in the ten-thousands place, and the digit 5 is in the hundreds place.",
            "Swap them: the new number is 459671.",
            "The ten-thousands digit went down from 6 to 5, so the new number is smaller than the original.",
            "Subtract to find by how much: 469571 minus 459671 equals 9900. So the new number is less by 9900.",
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
            "Count the notes from 40801 to 40901. Subtract and add 1, because both the first and the last note are counted. 40901 minus 40801, plus 1, equals 101 notes.",
            "Each note is worth 5 rupees, so multiply: 101 times 5 equals 505.",
            "So the bundle holds 505 rupees in all.",
        ],
    },
    "EXT_G5_WS_B4_018": {
        "q": "In writing all the prime numbers from 1 to 100, how many times is the digit 7 used?",
        "hints": [
            "Write out all the prime numbers from 1 to 100. Then go through your list and tick every 7 you see, in the tens place or the ones place.",
            "Do it in two parts. First, the primes that end in 7, starting 7, 17, 37, and so on. Then the primes that begin with 7, in the seventies. Careful: 27, 57, 77 and 87 are not prime.",
            "Try a smaller one: the digit 3 in the primes up to 50. Ending in 3: 3, 13, 23, 43. Starting with 3: 31, 37. That is 6 threes.",
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
            "The one-digit primes are 2, 3, 5 and 7. An even number must end in an even digit. Which of these four digits is even?",
            "The digit 2 has to go in the ones place. Now arrange 3, 5 and 7 in the other three places. List them in order: 3572, 3752, and so on, and count.",
            "Try a smaller one: using 2, 3 and 5 once each, the even numbers must end in 2. They are 352 and 532, so there are 2.",
        ],
        "steps": [
            "The one-digit primes are 2, 3, 5 and 7. All four digits are used, so each number has four digits.",
            "An even number ends in an even digit, and 2 is the only even one. So 2 goes in the ones place.",
            "The digits 3, 5 and 7 fill the other three places: 3572, 3752, 5372, 5732, 7352 and 7532.",
            "So 6 even numbers can be formed.",
        ],
    },
}
