"""Hand-written narration for imported place-value questions: AI-written word problems (AIGEN_grade5_).

Only the strings the rules in place_value_imported_rules.py cannot make sound right.
{id: {"q": "...", "hints": {index: "..."}, "steps": {index: "..."}}}
"""

HAND = {
    "AIGEN_grade5_05e3dee5-df17-4b19-bfa5-f2b873646c7d": {
        "hints": {
            2: "Here's a similar problem: If a digit's place value in the thousands place is 8,000, the digit is 8,000 divided by 1,000, which is 8. If that digit is 4 more than the units digit, then the units digit is 8 minus 4, which is 4. If the tens digit is 3 times the units digit, then the tens digit is 3 times 4, which is 12. Wait, that's not a single digit! So you'd need to re-check. Always verify each digit is 0 to 9.",
        },
    },
    "AIGEN_grade5_0c3a73ba-62ba-4fd4-8249-9a65100e4bb7": {
        "hints": {
            2: "Here's a similar problem: In the number 63,204, if you multiply the place value of 2, which is 200 because it is in the hundreds place, by the face value of 6, which is just 6, you get 200 times 6, which is 1,200. Now try the original problem the same way!",
        },
    },
    "AIGEN_grade5_1075cba6-ed27-49f0-a925-414a7d5d0d4d": {
        "hints": {
            1: "First, find what place the digit 5 is in. Then calculate: the place value of 5 is 5 times the value of that place. The face value of 5 is always just 5.",
        },
    },
    "AIGEN_grade5_1793fb6c-a077-417e-af22-3f3fd11525a6": {
        "hints": {
            1: "The units digit is 2. The ten-thousands digit is 2 plus 3, which is 5. The thousands digit is 7. The hundreds digit is half of 7, rounded down, which is 3. Now find the tens digit!",
        },
        "steps": {
            3: "The hundreds digit is half the thousands digit, rounded down. 7 divided by 2 is 3.5. Rounded down, that is 3.",
        },
    },
    # The printed question is longer than a narration may be, so "the digit in the lakhs place"
    # is said as "the lakhs digit" in the list of clues. Nothing is left out.
    "AIGEN_grade5_20ea0eaf-d2fc-4e33-9d93-64ce1ba52ca1": {
        "q": "During Diwali, Arjun and his sister Meera play a number puzzle game. Arjun thinks of a 6-digit number and gives these clues: The lakhs digit is the largest single-digit prime number. The ten-thousands digit is the remainder when 29 is divided by 4. The thousands digit is the square root of 81. The hundreds digit is half the lakhs digit, rounded down. The tens digit is the ten-thousands digit minus 1. The units digit is the sum of the hundreds and tens digits. Meera figures out the number! What is the difference between the place value of the digit in the lakhs place and the place value of the digit in the thousands place?",
    },
    "AIGEN_grade5_54ce7dae-0b5f-4ae5-b4a7-ef9876cb50ea": {
        "hints": {
            2: "Here's a similar problem: If a digit 3 is in the ten-thousands place and digit 6 is in the thousands place, the difference in their place values is 3 times 10000, minus 6 times 1000. That is 30000 minus 6000, which is 24000. Use the same approach for your problem!",
        },
    },
    "AIGEN_grade5_578a4973-9cc6-4c60-bf80-a19e9e9dbc5e": {
        "steps": {
            4: "So the full 6-digit number is: 8, 4, 0, 8, 5, 0. That makes 840850.",
        },
    },
    "AIGEN_grade5_7dfbff5d-8316-45a3-ab9d-3aba8b1994d8": {
        "steps": {
            1: "Lakhs digit is tens digit plus 3: 4 plus 3 equals 7.",
        },
    },
    "AIGEN_grade5_dbdee766-0e97-4938-86de-7dd493ff43d9": {
        "steps": {
            1: "Lakhs digit is tens digit plus 3: 2 plus 3 equals 5.",
        },
    },
    "AIGEN_grade5_bededa81-f160-4900-acf0-be30c0a9d05c": {
        "steps": {
            0: "From Clue 1, the ten-thousands digit is 7. So the number looks like: 7, then four blanks.",
        },
    },
    "AIGEN_grade5_f4e5ebb5-48e9-4336-82ea-09cdcba6b3b0": {
        "hints": {
            2: "Here's a similar problem: In the number 53,271, if we swap digits 3 and 2, the original has 3 in thousands, worth 3,000, and 2 in hundreds, worth 200. After swapping we get 52,371. The difference is 53,271 minus 52,371, which is 900. Notice: 3 minus 2, times 1,000, take away 3 minus 2, times 100. That is 1,000 minus 100, which is 900.",
        },
        "steps": {
            3: "We can also verify using place value logic: moving 6 from thousands to hundreds means it loses 6 times 1000, minus 6 times 100, which is 5,400 in value. Moving 4 from hundreds to thousands means it gains 4 times 1000, minus 4 times 100, which is 3,600 in value. The net change is 5,400 minus 3,600, which is 1,800. The number decreases by 1,800 rupees.",
        },
    },
}
