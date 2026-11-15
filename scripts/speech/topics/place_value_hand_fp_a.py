"""Hand-written narration: Grade 5 past papers 2016 to 2019 (place value)."""

PV = "Place value equals the digit, times the value of its place."

HAND = {
    "EXT_G5_FP_2016_018": {
        "q": "In one crore, how many tens are there?",
        "hints": [
            "Write one crore in digits: that is 1 followed by 7 zeros. How many tens fit in it? Divide by 10.",
            "1 crore is 1,00,00,000. That is also written as 10,000,000. And 1 lakh is 1,00,000.",
            "",
        ],
        "steps": [
            "1 crore is 10,000,000.",
            "The number of tens is 10,000,000 divided by 10, which is 1,000,000.",
            "1,000,000 is 10 lakh. So the answer is ten lakh tens.",
        ],
    },
    "EXT_G5_FP_2016_019": {
        "q": "What will be the place value of the digit 4, in the smallest five-digit odd number formed by using all the given digits only once: 1, 8, 4, 0 and 7?",
        "hints": [
            "An odd number must end in 1 or 7. For the smallest number, put small digits at the front, but 0 can't be first. Try both endings.",
            "For the smallest number, put the smallest non-zero digit first, then the rest in increasing order. The last digit must be odd.",
            "",
        ],
        "steps": [
            "If it ends in 7, the remaining digits are 1, 8, 4 and 0. The smallest is 10487.",
            "If it ends in 1, the remaining digits are 8, 4, 0 and 7. The smallest is 40781.",
            "So the smallest is 10487.",
            "The digit 4 is in the hundreds place. So 4 times 100 equals 400.",
        ],
    },
    "EXT_G5_FP_2016_024": {
        "q": "In the case of how many digits in the number 2138574, are their positions in the number, and their positions when the digits of the number are arranged in ascending order, identical?",
        "hints": [
            "Arrange the digits from smallest to biggest, write that number underneath, and compare position by position.",
            "Line up the two numbers, and tick every place where the digits match.",
            "",
        ],
        "steps": [
            "The original digits are 2, 1, 3, 8, 5, 7, 4.",
            "In ascending order, they are 1, 2, 3, 4, 5, 7, 8.",
            "Compare place by place. 2 is not 1. 1 is not 2. 3 equals 3, a match. 8 is not 4. 5 equals 5, a match. 7 equals 7, a match. 4 is not 8.",
            "There are three matches: the digits 3, 5 and 7.",
        ],
    },
    "EXT_G5_FP_2016_025": {
        "q": "Mister Sam's age in the year 2000 was a multiple of 8, and in the year 2001 it was a multiple of 7. In which year was Mister Sam born?",
        "hints": [
            "Test each birth year. His age in 2000 is 2000 minus the birth year. His age in 2001 is one more. Both conditions must work.",
            "Ages in consecutive years differ by 1. We need a multiple of 8 followed by a multiple of 7, like 48 and 49.",
            "",
        ],
        "steps": [
            "1962 gives age 38, which is not a multiple of 8. That does not work.",
            "1960 gives age 40, which is a multiple of 8. But 41 is not a multiple of 7. That does not work.",
            "1956 gives age 44. That does not work.",
            "1952 gives age 48, which is 8 times 6. The next year he is 49, which is 7 times 7. Both work, so he was born in 1952.",
        ],
    },
    "EXT_G5_FP_2016_040": {
        "q": "If f minus 9 is an even number, which of the following could be the 25th odd number coming after it?",
        "hints": [
            "Try a real number. Let f minus 9 equal 10, which is even. The odd numbers after it are 11, 13, 15, and so on. The 25th is 10, plus 1, plus 24 times 2. Then compare with f.",
            "After an even number E, the 1st odd number is E plus 1. The nth odd number is E plus 1, plus, open bracket, n minus 1, close bracket, times 2.",
            "",
        ],
        "steps": [
            "Let E equal f minus 9, which is even.",
            "The 25th odd number after E is E plus 1, plus 24 times 2. That equals E plus 49.",
            "That is f minus 9, plus 49, which equals f plus 40.",
        ],
    },
    "EXT_G5_FP_2017_028": {
        "q": "If x plus 37 is an even number, then the 17th odd number coming after it is represented by what?",
        "hints": [
            "Try a real even number, say 10. The odd numbers after it are 11, 13, 15, and so on. What is the 17th one? Compare with 10.",
            "After an even number E, the nth odd number is E plus 1, plus, open bracket, n minus 1, close bracket, times 2.",
            "",
        ],
        "steps": [
            "Let E equal x plus 37, which is even.",
            "The 17th odd number after E is E plus 1, plus 16 times 2. That equals E plus 33.",
            "That is x plus 37, plus 33, which equals x plus 70.",
        ],
    },
    "EXT_G5_FP_2017_033": {
        "q": "Form the greatest odd number using the digits 7, 5, 2, 0 and 4, each only once.",
        "hints": [
            "An odd number must end in an odd digit, 7 or 5. For the greatest number, the biggest digits must come first. Compare ending in 5, and ending in 7.",
            "For the greatest number, put the biggest digits at the front. For an odd number, the last digit is odd.",
            "",
        ],
        "steps": [
            "End with 5. The rest, 7, 4, 2 and 0, arranged greatest first, give 74205.",
            "End with 7. The rest, 5, 4, 2 and 0, give 54207.",
            "74205 is greater. So the answer is 74205.",
            "75420 is even, so it can't be the answer.",
        ],
    },
    "EXT_G5_FP_2017_039": {
        "q": "In which of the following numbers is the digit in the tens place exactly four times the digit in the thousands place?",
        "hints": [
            "For each number, find the thousands digit, the 1st, and the tens digit, the 3rd. Is the tens digit exactly 4 times the thousands digit?",
            "The thousands digit is the 1st digit of a 4-digit number. The tens digit is the 3rd digit.",
            "",
        ],
        "steps": [
            "8621: thousands digit 8, tens digit 2. That does not work.",
            "2386: thousands digit 2, tens digit 8. And 8 equals 4 times 2. That works.",
            "8326: thousands digit 8, tens digit 2. That does not work. 4538: thousands digit 4, tens digit 3. That does not work.",
            "The answer is 2386.",
        ],
    },
    "EXT_G5_FP_2018_002": {
        "q": "If the digit 2 is placed in between the digits 3 and 5 of the number 43541, by how much is the new number more than the previous number?",
        "hints": [
            "Write the new number first: put 2 between the 3 and the 5. Then subtract the old number.",
            "Write both numbers neatly and subtract.",
            "",
        ],
        "steps": [
            "The old number is 43541. Putting 2 between 3 and 5 gives the digits 4, 3, 2, 5, 4, 1. That is 432541.",
            "The difference is 432541 minus 43541, which is 389000.",
        ],
    },
    "EXT_G5_FP_2018_005": {
        "q": "A palindrome number is a number which remains the same when read backwards. For example, 707 or 5225. A three-digit palindrome number is added to 2017, to get a 4-digit palindrome number. What is the sum of the digits of the three-digit palindrome number added to 2017?",
        "hints": [
            "The answer is between 2118 and 3016, so it starts with 2, or 3. A palindrome starting with 2 ends with 2. Use the last digit: 7, plus the last digit of your number, must end in 2.",
            "A palindrome reads the same both ways, like 2552.",
            "",
        ],
        "steps": [
            "The 3-digit palindrome looks like A, B, A. Look at the last digit: 7 plus A must end in 2. So A equals 5.",
            "So the number is 5, B, 5. 2017 plus 5, B, 5, equals 2522 plus 10 B. We want a palindrome of the form 2, Y, Y, 2.",
            "B equals 3 gives 2552, which reads the same backwards. So the number is 535.",
            "The sum of the digits is 5 plus 3 plus 5, which equals 13.",
        ],
    },
    "EXT_G5_FP_2018_022": {
        "q": "Using the digits 9, 5, 0, 7 and 3, each only once, the greatest 5-digit number is formed. What is the difference between the place value of the digit 5, and of 3, in the number formed?",
        "hints": [
            "For the greatest number, put the biggest digit first, then the next biggest, and so on. Write the number, then find the place value of 5, and of 3, in it.",
            PV,
            "",
        ],
        "steps": [
            "The greatest number is 97530.",
            "5 is in the hundreds place, so it is worth 500. 3 is in the tens place, so it is worth 30.",
            "The difference is 500 minus 30, which is 470.",
        ],
    },
    "EXT_G5_FP_2018_033": {
        "q": "If x plus 37 represents an even number, then what would the 17th odd number prior to it be?",
        "hints": [
            "Try a real even number, such as 50. The odd numbers before it are 49, 47, 45, and so on, going down. Find the 17th and compare.",
            "Before an even number E, the nth odd number prior is E minus 1, minus, open bracket, n minus 1, close bracket, times 2.",
            "",
        ],
        "steps": [
            "Let E equal x plus 37, which is even.",
            "The 17th odd number before E is E minus 1, minus 16 times 2. That equals E minus 33.",
            "That is x plus 37, minus 33, which equals x plus 4.",
        ],
    },
    "EXT_G5_FP_2019_014": {
        "q": "What is the 27th even number coming after 27?",
        "hints": [
            "The first even number after 27 is 28. Then count up in 2s.",
            "The nth even number after an odd number, call it O, is O plus 1, plus, open bracket, n minus 1, close bracket, times 2.",
            "",
        ],
        "steps": [
            "The 1st even number after 27 is 28.",
            "The 27th is 28, plus 26 times 2. That is 28 plus 52, which equals 80.",
        ],
    },
    "EXT_G5_FP_2019_020": {
        "q": "Using the digits 2, 3, 4 and 5, each only once, all four-digit numbers are made. In how many numbers will the digit 5 be in the hundreds place?",
        "hints": [
            "Put 5 in the hundreds place. Then count the ways to arrange the other three digits, 2, 3 and 4, in the remaining 3 places.",
            "The arrangements of 3 different digits are 3 times 2 times 1, which equals 6.",
            "",
        ],
        "steps": [
            "Fix 5 in the hundreds place: blank, 5, blank, blank.",
            "The digits 2, 3 and 4 fill the other three places.",
            "The first place has 3 choices, the next has 2 choices, and the last has 1 choice. So 3 times 2 times 1 equals 6.",
            "They are 2534, 2543, 3524, 3542, 4523 and 4532.",
        ],
    },
    "EXT_G5_FP_2019_030": {
        "q": "Rearrange the digits of the number 75003064 to form the smallest number.",
        "hints": [
            "The first digit can't be 0, otherwise it isn't an 8-digit number. Put the smallest non-zero digit first, then all the zeros, then the rest in increasing order.",
            "For the smallest number, put the smallest non-zero digit first, then the 0s, then the others in ascending order.",
            "",
        ],
        "steps": [
            "The digits are 7, 5, 0, 0, 3, 0, 6 and 4. There are three zeros.",
            "The first digit is the smallest non-zero digit, which is 3. Then come 0, 0, 0.",
            "Then 4, 5, 6, 7. That gives 30004567.",
        ],
    },
    "EXT_G5_FP_2019_037": {
        "q": "In the number 87459, how many times is the place value of 7 to that of 5?",
        "hints": [
            "Find the place value of 7, in the thousands place, and of 5, in the tens place. Then divide.",
            PV,
            "",
        ],
        "steps": [
            "In 87459, 7 is in the thousands place, so it is worth 7000. 5 is in the tens place, so it is worth 50.",
            "7000 divided by 50 equals 140 times.",
        ],
    },
}
