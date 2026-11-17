"""Hand-written narration for imported arithmetic questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

Only the lines the rules in arithmetic_imported_rules.py do not read well. Same shape as the
other override tables: {"q": "...", "options": {i: "..."}, "hints": {i: "..."}, "steps": {i: "..."}}.
"""

OVERRIDES = {
    # The question is long: the rule line runs past the 700-character limit.
    "AIGEN_grade5_7a67b583-64a0-4f43-8fb2-d843df1ba190": {
        "q": "Rahul is tracking the daily profit or loss of his father's samosa stall at a mela in Lucknow. "
             "He uses positive numbers for profit and negative numbers for loss. Here are the results for 7 days. "
             "Day 1: plus 120 rupees. Day 2: minus 85 rupees. Day 3: minus 40 rupees. Day 4: plus 95 rupees. "
             "Day 5: minus 110 rupees. Day 6: plus 150 rupees. Day 7: minus 60 rupees. "
             "Rahul's father promised that if the week's total profit is more than 50 rupees, he gets a bonus of 30 rupees. "
             "If the total is from 0 to 50 rupees, inclusive, he gets a bonus of 10 rupees. "
             "If there is an overall loss, he gets no bonus. "
             "After adding the bonus, if any, to the weekly total, what is the final amount Rahul records?",
        "hints": {
            2: "Here's a similar problem: Suppose a shop earns plus 50 rupees, minus 30 rupees, plus 20 rupees, minus 15 rupees over 4 days. "
               "Positives: 50 plus 20 equals 70. Negatives: negative 30 plus negative 15 equals minus 45. "
               "Total equals 70 plus negative 45, that is 70 minus 45, which is 25 rupees. "
               "If the bonus rule says more than 20 rupees gets a 5 rupee bonus, then final equals 25 plus 5, which is 30 rupees. "
               "Follow the same approach for Rahul's problem!",
        },
    },
    # Letters and digits side by side: each one is said on its own.
    "IPM2020_G5_Q01": {
        "q": "In the multiplication, A 6 B C, times 7, equals D 9 E 98, each distinct letter represents a single distinct digit. Find D.",
    },
    "AIGEN_grade5_49848a61-8cfa-4821-ba6a-da096f074ea5": {
        "hints": {
            1: "Rank the earnings: Kiran, 5,12,345 rupees, is more than Ravi, 4,75,628 rupees, who is more than Meena, 3,89,457 rupees, "
               "who is more than Priya, 2,98,076 rupees. Now add the top two and the bottom two separately.",
        },
    },
    "AIGEN_grade5_29a8cab7-422c-47b2-9cb2-de6fe2807a7d": {
        "steps": {
            4: "Vikram is at minus 17 and Zara is at 0. The distance between them is the absolute value of 0 minus negative 17, which is 17 steps.",
        },
    },
    "AIGEN_grade5_cd575693-1598-4372-9b86-9dd65817d191": {
        "hints": {
            2: "Here's a similar problem: Suppose scores are minus 5, plus 3, plus 8, minus 2. The worst is minus 5 and the best is plus 8. "
               "Original total equals minus 5 plus 3 plus 8 plus negative 2, which is 4. "
               "New total, replacing minus 5 with plus 8, equals 8 plus 3 plus 8 plus negative 2, which is 17. "
               "Increase equals 17 minus 4, which is 13. "
               "Notice this equals best minus worst, which is 8 minus negative 5, that is 8 plus 5, which is 13.",
        },
    },
    "IPMTB_grade5_ch05_q015": {
        "steps": {
            2: "So Manisha will be 39 years old after 10 years! Think of it like a number line: 19, plus 10, gives 29, plus 10, gives 39.",
        },
    },
    # Choices that name two ages need a pause between them.
    "IPMTB_grade5_ch05_q011": {
        "options": {0: "Sujata 20 years, Madhuri 27 years"},
    },
    "IPMTB_grade5_ch05_q040": {
        "options": {
            0: "Seeta 6 years, Reeta 6 years",
            1: "Seeta 9 years, Reeta 3 years",
            2: "Seeta 15 years, Reeta 9 years",
            3: "Seeta 7 years, Reeta 5 years",
        },
    },
    "IPMTB_grade5_ch06_q023": {
        "hints": {
            1: "Start by identifying the three groups: group 1, 30 men earning 2000 rupees each, group 2, 10 men earning 2500 rupees each, "
               "and group 3, 30 women earning 1500 rupees each. Calculate each group's total separately, then add them together.",
        },
    },
}
