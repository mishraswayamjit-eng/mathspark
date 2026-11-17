"""Hand-written narration for imported place-value questions: IPM textbook items (IPMTB_grade5_).

Only the strings the rules in place_value_imported_rules.py cannot make sound right.
{id: {"q": "...", "hints": {index: "..."}, "steps": {index: "..."}}}

The textbook's own wording ("5 digited number") is kept. A question printed as an unfinished
sentence ("... you get -----", "... you get.") is closed with "what number?".
"""

HAND = {
    "IPMTB_grade5_ch02_q001": {
        "steps": {
            3: "The place value of 5 is the digit, times the value of its place. That is 5 times 1,00,000, which is 5,00,000.",
        },
    },
    "IPMTB_grade5_ch02_q003": {"q": "If one is added to the greatest 5 digited number, you get what number?"},
    "IPMTB_grade5_ch02_q004": {"q": "If one is subtracted from largest 3 digited number, you get what number?"},
    "IPMTB_grade5_ch02_q026": {
        "q": "If 1 is added to the greatest 6 digited number, you get what number?",
        "steps": {
            2: "When we add 1 to 9,99,999, all the 9s roll over, just like an odometer on a car. 9 plus 1 equals 10, carry 1, and this keeps happening for every digit!",
        },
    },
    "IPMTB_grade5_ch02_q027": {"q": "If 1 is subtracted from smallest 4 digited number, you get what number?"},
    "IPMTB_grade5_ch02_q028": {"q": "The difference between the smallest 5 digited number and greatest 4 digited number is what?"},
    "IPMTB_grade5_ch02_q030": {"q": "If 1 is added to the greatest 5 digited number, you get what number?"},
    "IPMTB_grade5_ch02_q009": {
        "hints": {
            1: "Remember: the place value of a digit is the digit, times the value of its position. Ones means times 1, tens means times 10, hundreds means times 100, and so on. Which digit gives the same result no matter what you multiply it by?",
        },
        "steps": {
            1: "Now let's test the digit 0. Put it anywhere, ones, tens, hundreds, thousands, and calculate its place value. 0 times 1 equals 0. 0 times 10 equals 0. 0 times 100 equals 0. 0 times 1000 equals 0.",
        },
    },
    "IPMTB_grade5_ch02_q016": {
        "steps": {
            0: "Identify the even digits from 2, 8, 7, 3, 1. Even digits are divisible by 2. The even digits are 2 and 8.",
        },
    },
    "IPMTB_grade5_ch02_q018": {
        "hints": {
            2: "Here's a similar problem: How many two-digit odd numbers are there? The smallest two-digit odd number is 11 and the largest is 99. Using the formula: 99 minus 11, then divided by 2, plus 1. That is 88 divided by 2, plus 1, which is 45. So there are 45 two-digit odd numbers! Try the same approach for three-digit even numbers.",
        },
        "steps": {
            2: "Even numbers form a sequence: 100, 102, 104, and so on, up to 998. Each number is 2 more than the previous one. To count how many numbers are in this sequence, we use a handy formula: the count is last minus first, divided by the step, plus 1.",
            3: "Let's plug in our values: the count is 998 minus 100, divided by 2, plus 1. That is 898 divided by 2, plus 1. Which is 449 plus 1, and that equals 450.",
        },
    },
    "IPMTB_grade5_ch02_q020": {
        "steps": {
            0: "Identify all one-digit prime numbers. A prime number has exactly 2 factors, 1 and itself. They are 2, 3, 5 and 7.",
        },
    },
    "IPMTB_grade5_ch02_q021": {
        "steps": {
            3: "The result is 73971. This is a 5-digit number, so the middle digit is the 3rd digit. Let's count: 7, 3, 9, 7, 1. The middle digit is 9!",
        },
    },
    "IPMTB_grade5_ch02_q029": {
        "steps": {
            3: "Let's do the addition step by step. Think of it like this: 9,999 plus 100. Add the ones: 9 plus 0 equals 9. Add the tens: 9 plus 0 equals 9. Add the hundreds: 9 plus 1 equals 10, so write 0, carry 1. Add the thousands: 9 plus 0, plus 1 carried, equals 10.",
        },
    },
    "IPMTB_grade5_ch02_q033": {
        "hints": {
            2: "Here's a similar problem: Find the maximum place value of digit 5 in 25,15,350. The 5s appear at: ones place, but wait, it's 0 there, no 5! Tens place, which is 50. Hundreds place, nope, it's 3. Thousands place, which is 5,000. Ten-thousands place, which is 50,000, nope, it's 1. And lakhs place, which is 5,00,000. The maximum place value of 5 would be 5,00,000.",
        },
    },
    "IPMTB_grade5_ch02_q034": {
        "steps": {
            7: "Now compare all the place values: 4,00,000 is greater than 30,000, which is greater than 7,000, which is greater than 800, which is greater than 90, which is greater than 6. The minimum, or smallest, place value is 6, which belongs to the digit 6!",
        },
    },
    "IPMTB_grade5_ch02_q035": {
        "hints": {
            1: "Write out the place value of each digit. 9 is in the lakhs place, so its place value is 9,00,000. 3 is in the ten-thousands place: 30,000. 7 is in the thousands place: 7,000. 4 is in the hundreds place: 400. 5 is in the tens place: 50. And 1 is in the ones place: 1. Now find the maximum and minimum place values!",
            2: "Here's a similar problem: Find the difference between the maximum and minimum place value in 5,23,461. The place values are: 5 gives 5,00,000. 2 gives 20,000. 3 gives 3,000. 4 gives 400. 6 gives 60. 1 gives 1. The maximum place value is 5,00,000. The minimum place value is 1. The difference is 5,00,000 minus 1, which is 4,99,999.",
        },
    },
    "IPMTB_grade5_ch02_q040": {
        "hints": {
            2: "Here's a similar problem: Form the smallest odd number using 3, 0, 5, 8, 2. The odd digits are 3 and 5. To make the number smallest, put the smallest odd digit, 3, at the end. Remaining digits: 0, 5, 8, 2. We can't start with 0, so the smallest non-zero digit, 2, goes first: 2, then three blanks, then 3. Then arrange 0, 5, 8 in ascending order: 20,583.",
        },
        "steps": {
            4: "Put it all together: 2, 0, 4, 6, 1 makes 20,461. That's the smallest possible odd number using these digits!",
        },
    },
    "IPMTB_grade5_ch02_q042": {
        "steps": {
            4: "We can also verify this by counting systematically. The hundreds digit can be 1 to 9: that is 9 choices. The tens digit can be 0 to 9: that is 10 choices. And the units digit must be odd, 1, 3, 5, 7, or 9: that is 5 choices. 9 times 10 times 5 equals 450.",
        },
    },
    "IPMTB_grade5_ch02_q043": {
        "hints": {
            2: "Here's a similar example: Using digits 2, 5, 8, 6, the greatest number is 8652, and the smallest number is 2568. The difference is 8652 minus 2568, which is 6084. See how it works? Now try the same idea with 3, 1, 4, 7!",
        },
    },
    "IPMTB_grade5_ch02_q044": {
        "steps": {
            0: "Identify all one-digit prime numbers. A prime number has exactly 2 factors. So: 2, with factors 1 and 2. 3, with factors 1 and 3. 5, with factors 1 and 5. 7, with factors 1 and 7. Note: 1 is not prime, it has only 1 factor, and 4, 6, 8, 9 are not prime.",
            1: "To make the smallest 4-digit number, we want the smallest digit in the thousands place, then the next smallest, and so on. The smallest arrangement would be 2, 3, 5, 7, giving us 2,357.",
        },
    },
    "IPMTB_grade5_ch02_q048": {
        "hints": {
            2: "Here's a similar problem: Using digits 2, 4, 0, 8, 6, the greatest is 86420, and the smallest is 20468. Subtract: 86420 minus 20468 equals 65952. The middle digit, the 3rd digit, is 9. See how we found the middle digit? Now try the same approach with your digits!",
        },
        "steps": {
            3: "The result is 86931. This is a 5-digit number, so the 'middle' digit is the 3rd digit. Let's count: 8 is 1st, 6 is 2nd, 9 is 3rd, 3 is 4th, 1 is 5th.",
        },
    },
    "IPMTB_grade5_ch05_q020": {
        "steps": {
            1: "Starting from the right: 5 is in the ones place. 2 is in the tens place. 1 is in the hundreds place. 6 is in the thousands place. 4 is in the ten-thousands place. 3 is in the lakhs place. 7 is in the ten-lakhs, or 70 lakhs, place.",
        },
    },
}
