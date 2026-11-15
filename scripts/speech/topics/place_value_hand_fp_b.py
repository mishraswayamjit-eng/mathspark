"""Hand-written narration: Grade 5 past papers 2020 to 2022 (place value)."""

PV = "Place value equals the digit, times the value of its place."

HAND = {
    "EXT_G5_FP_2020_005": {
        "q": "If x plus 21 is an odd number, then find the 3rd even number coming after it.",
        "hints": [
            "The first even number after an odd number is 1 more. After that, even numbers go up in 2s.",
            "After an odd number, call it O, the 1st even number is O plus 1, the 2nd is O plus 3, and the 3rd is O plus 5.",
            "",
        ],
        "steps": [
            "The 1st even number is x plus 21, plus 1, which equals x plus 22.",
            "The 2nd is x plus 24.",
            "The 3rd is x plus 26. So the answer is x plus 26.",
        ],
    },
    "EXT_G5_FP_2020_016": {
        "q": "In which of the numbers given below will the difference between the place values of the digits 9 and 7 be 83000?",
        "hints": [
            "For each number, find the place value of 9, and of 7, and subtract. You are looking for 83000.",
            "Place value equals the digit, times the value of its place. Ten-thousands is 10000, thousands is 1000, and so on.",
            "",
        ],
        "steps": [
            "In 1907000, the 9 is worth 900000, and the 7 is worth 7000. The difference is 893000. That does not work.",
            "In 109700, the 9 is worth 9000, and the 7 is worth 700. The difference is 8300. That does not work.",
            "In 197000, the 9 is worth 90000, and the 7 is worth 7000. 90000 minus 7000 equals 83000. That works.",
            "In 91700, the 9 is worth 90000, and the 7 is worth 700. The difference is 89300. That does not work.",
        ],
    },
    "EXT_G5_FP_2020_023": {
        "q": "The sum of two consecutive prime numbers is 42. What is the difference of those two prime numbers?",
        "hints": [
            "Each prime is close to half of 42, which is 21. List the primes around 21, and find the consecutive pair that adds to 42.",
            "The primes near 21 are 17, 19, 23 and 29.",
            "",
        ],
        "steps": [
            "Half of 42 is 21. The primes just below and above 21 are 19 and 23.",
            "19 plus 23 equals 42, and there is no prime between them.",
            "The difference is 23 minus 19, which is 4.",
        ],
    },
    "EXT_G5_FP_2020_036": {
        "q": "The sum of three consecutive natural numbers is 66. Which of the following can be one of those numbers?",
        "hints": [
            "The middle number of three consecutive numbers is the average: 66 divided by 3. Then find the numbers on either side.",
            "Three consecutive numbers are n minus 1, n, and n plus 1. Their sum is 3 n.",
            "",
        ],
        "steps": [
            "The middle number is 66 divided by 3, which is 22.",
            "The numbers are 21, 22 and 23.",
            "The option that matches is 23.",
        ],
    },
    "EXT_G5_FP_2020_037": {
        "q": "Jack is reading a book whose pages are numbered from 1. The page numbers of the book have a total of 555 digits. How many pages are there in Jack's book?",
        "hints": [
            "Count the digits in stages: pages 1 to 9, with 1 digit each, pages 10 to 99, with 2 digits each, then the 3-digit pages. Subtract as you go.",
            "The digits used are 9 times 1, plus 90 times 2. That is 189, up to page 99.",
            "",
        ],
        "steps": [
            "Pages 1 to 9 use 9 digits.",
            "Pages 10 to 99: that is 90 pages, times 2, which is 180 digits. The total so far is 189.",
            "The digits left are 555 minus 189, which is 366, for the 3-digit pages. So 366 divided by 3 equals 122 pages.",
            "The total pages are 99 plus 122, which is 221.",
        ],
    },
    "EXT_G5_FP_2021_004": {
        "q": "Which of the following numbers is divisible by 11?",
        "hints": [
            "The divisibility rule of 11: add the digits in the 1st, 3rd, 5th places, and so on. Add the digits in the 2nd, 4th, 6th places, and so on. Then subtract. The difference must be 0 or 11.",
            "The test for 11: the sum of the digits at odd places, minus the sum of the digits at even places, equals 0, 11, 22, and so on.",
            "",
        ],
        "steps": [
            "For 3116365: 3 plus 1 plus 3 plus 5, minus the sum 1 plus 6 plus 6. That is 12 minus 13, which equals minus 1. That does not work.",
            "For 901351: 9 plus 1 plus 5, minus the sum 0 plus 3 plus 1. That is 15 minus 4, which equals 11. That works.",
            "For 11111: 3 minus 2 equals 1. That does not work. For 8790321: 21 minus 9 equals 12. That does not work.",
            "The answer is 901351, which equals 11 times 81941.",
        ],
    },
    "EXT_G5_FP_2021_007": {
        "q": "The digit 6 is used twice in each of the given numbers. In only one number, the place value of one 6 is 1000 times the other 6. Find it.",
        "hints": [
            "Find the place value of each 6 in every option. You want one 6 to be worth exactly 1000 times the other.",
            PV,
            "",
        ],
        "steps": [
            "In 66728, the place values are 60000 and 6000. The ratio is 10. That does not work.",
            "In 68726, the place values are 60000 and 6. The ratio is 10000. That does not work.",
            "In 86762, the place values are 6000 and 60. The ratio is 100. That does not work.",
            "In 68762, the first 6 is worth 60000, and the second 6 is in the tens place, worth 60. 60000 divided by 60 equals 1000. That works.",
        ],
    },
    "EXT_G5_FP_2021_026": {
        "q": "A number is perfectly divisible by 18. The number consists only of 4s. For example, 444, and so on. What is the minimum number of 4s in this number?",
        "hints": [
            "18 equals 2 times 9. A number made of 4s is always even, so the rule for 9 decides: the digit sum must be a multiple of 9.",
            "Divisible by 9 means the sum of the digits is a multiple of 9.",
            "",
        ],
        "steps": [
            "The number ends in 4, so it is even, which means divisible by 2.",
            "For 9: the digit sum is 4 times the number of 4s, and it must be a multiple of 9.",
            "4 and 9 share no factor, so the number of 4s must be a multiple of 9. The smallest is 9. The number is 444444444.",
        ],
    },
    "EXT_G5_FP_2022_008": {
        "q": "If Z plus 41 represents an even number, then which of the following represents the 19th odd number coming before it?",
        "hints": [
            "Try a real even number, say 50. The odd numbers before it are 49, 47, 45, and so on. Find the 19th and compare.",
            "Before an even number E, the nth odd number is E minus 1, minus, open bracket, n minus 1, close bracket, times 2.",
            "",
        ],
        "steps": [
            "Let E equal Z plus 41.",
            "The 19th odd number before E is E minus 1, minus 18 times 2. That equals E minus 37.",
            "That is Z plus 41, minus 37, which equals Z plus 4.",
        ],
    },
    "EXT_G5_FP_2022_009": {
        "q": "How many odd three-digit square numbers are there in all?",
        "hints": [
            "An odd number times itself is odd, and an even number times itself is even. So count only the odd numbers whose squares have three digits.",
            "Three-digit squares start at 10 times 10, which is 100, and stop at 31 times 31, which is 961, because 32 times 32, which is 1024, has four digits. Now count the odd numbers from 10 to 31.",
            "A similar one: odd two-digit squares. Two-digit squares come from the numbers 4 to 9, and the odd numbers there are 5, 7 and 9. So there are 3 of them: 25, 49 and 81.",
        ],
        "steps": [
            "A square number is odd only when the number being squared is odd.",
            "Three-digit squares run from 10 times 10, which is 100, to 31 times 31, which is 961, since 32 times 32, which is 1024, is too big.",
            "The odd numbers from 10 to 31 are 11, 13, 15, 17, 19, 21, 23, 25, 27, 29 and 31. That is 11 numbers, so there are 11 odd three-digit squares.",
            "11 is not one of the numbers offered: 10, 12 or 13. So the answer is None of these.",
        ],
    },
    "EXT_G5_FP_2022_025": {
        "q": "In the number sixty-seven lakhs, ninety-four thousand, five hundred and twenty-one, what is the place value of the digit which is exactly in the middle?",
        "hints": [
            "Write the number in digits first: 67 lakhs is 67,00,000 and so on. The number has 7 digits. Which one is exactly in the middle?",
            PV,
            "",
        ],
        "steps": [
            "The number is 67,94,521. Its digits are 6, 7, 9, 4, 5, 2, 1. That is 7 digits.",
            "The middle digit, the 4th, is 4. It is in the thousands place.",
            "The place value is 4000.",
        ],
    },
    "EXT_G5_FP_2022_032": {
        "q": "Find the sum of the numbers which are divisible by 3, out of the following: 861, 435, 218, 764 and 1263.",
        "hints": [
            "A number is divisible by 3 if the sum of its digits is divisible by 3. Test each number, then add only those that pass.",
            "The divisibility rule of 3: the digit sum is a multiple of 3.",
            "",
        ],
        "steps": [
            "For 861: 8 plus 6 plus 1 equals 15. Yes. For 435: 4 plus 3 plus 5 equals 12. Yes. For 218, the sum is 11. No. For 764, it is 17. No. For 1263, it is 12. Yes.",
            "The sum is 861 plus 435 plus 1263, which equals 2559.",
        ],
    },
}
