"""Hand-written narration for imported questions (AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

Only the lines the rules in squares_patterns_imported_rules.py do not say well. "q" is a string;
"options", "hints" and "steps" map a position (from 0) to its line. Anything left out is by rule.
"""

HAND = {
    # A table of rings, stones and running totals.
    "AIGEN_grade5_325bc4eb-3bda-417d-9f07-fd3ffd99600e": {
        "steps": {
            1: "List out the stones needed per ring, and keep a running total. "
               "Ring 1 needs 5 stones, total 5. Ring 2 needs 8, total 13. Ring 3 needs 11, total 24. "
               "Ring 4 needs 14, total 38. Ring 5 needs 17, total 55. Ring 6 needs 20, total 75. "
               "Ring 7 needs 23, total 98. Ring 8 needs 26, total 124.",
        },
    },
    "AIGEN_grade5_b5495610-aeff-4c64-b3a6-d3658e9e4932": {
        "steps": {
            1: "Let's verify: 256 is more than 15 squared, which is 225, and less than 17 squared, which is 289. "
               "This matches the father's clue!",
        },
    },
    # Maths lines with a power or a labelled side, which the rules leave out.
    "AIGEN_grade5_c5bfda2b-73f7-4fbe-8216-f7cfa6212a05": {
        "steps": {
            0: "Identify the pattern: each day the number of packets doubles. "
               "Day n equals 3 times 2 to the power, n minus 1.",
        },
    },
    "AIGEN_grade5_c6ab10b2-4525-4d4d-a7bd-2b183f0da88f": {
        "steps": {
            2: "The problem says Raju's grandfather added 5 meters to each side. "
               "So the original side was 5 meters less than the new side. "
               "The original side equals 24 minus 5, which is 19 metres.",
        },
    },
    "IPMTB_grade5_ch03_q004": {
        "hints": {
            1: "Write out the digits of each number: 1, 2, 3. Then 2, 3, 4. Then 3, 4, 5. Then 4, 5, 6. "
               "What do you notice about how each number is formed?",
        },
        "steps": {
            0: "Let's write out each number and look at its individual digits. 123 has the digits 1, 2 and 3.",
            3: "The next number should be 3 consecutive digits starting from 5: 5, 6, 7, which makes 567.",
        },
    },
    "IPMTB_grade5_ch03_q016": {
        "hints": {1: "List out just the denominators: 2, 3, 4, 5, 6, blank, blank. What comes next?"},
    },
    "IPMTB_grade5_ch03_q026": {
        "steps": {
            4: "We can also see a neat pairing pattern: the series groups numbers by their starting digit, in pairs. "
               "123 and 132. 231 and 213. 312 and blank. Each pair starts with the same digit, and the last two digits swap. "
               "So after 312, the next number swaps the last two digits, to give: 312 becomes 321.",
        },
    },
    "IPMTB_grade5_ch03_q029": {
        "hints": {
            1: "Start by expressing each number as a cube: 125 equals 5 cubed, 64 equals 4 cubed, and 8 equals 2 cubed. "
               "What pattern do you see in the bases 5, 4, blank, 2, blank?",
            2: "Here's a similar problem: Fill in the blanks: 81, 27, star, 3, star. "
               "Notice 81 equals 3 to the power four, and 27 equals 3 cubed. So the pattern is powers of 3 going down: "
               "3 to the power four, 3 cubed, 3 squared, 3 to the power one, 3 to the power zero. "
               "That is 81, 27, 9, 3 and 1. Use the same kind of thinking for your problem!",
        },
    },
    # The dots in this series stand for the missing number.
    "IPMTB_grade5_ch03_q039": {
        "q": "Fill in the blanks. 9, 25, 49, blank, 121.",
        "hints": {
            1: "Write each number as a square: 9 equals 3 squared, 25 equals 5 squared, 49 equals 7 squared, then the blank, "
               "and 121 equals 11 squared. What pattern do you see in the bases 3, 5, 7, blank, 11?",
        },
        "steps": {
            0: "Let's recognize each number as a perfect square. 9 equals 3 squared, 25 equals 5 squared, "
               "49 equals 7 squared, then the blank, and 121 equals 11 squared.",
        },
    },
    "IPMTB_grade5_ch03_q040": {
        "hints": {
            2: "Here's a similar problem: Find the next three numbers in 2, 20, 200, blank, blank, blank. "
               "Each term is multiplied by 10, so the next three are 2000, 20000 and 200000. "
               "Now apply the same thinking to the given series!",
        },
    },
    "IPMTB_grade5_ch04_q006": {
        "steps": {
            3: "Now let's check each option. C, 2: not in our list. B, 3: not in our list. "
               "C, 0: yes, it's in our list! For example, 10 squared equals 100. D, 7: not in our list.",
        },
    },
    # The print gives the unit twice, as "sq.cm" and in words; the voice says it once.
    "IPMTB_grade5_ch04_q010": {
        "hints": {
            2: "Let's try a similar problem! If a square has a side of 12 centimetres, its area equals 12 times 12, "
               "which is 144 square centimetres. Notice how we write square centimetres for area, not just centimetres! "
               "That's because area covers a flat surface, like a rangoli pattern on the floor.",
        },
        "steps": {
            4: "Now, don't forget the units! Since area measures a surface, like the floor of a room, "
               "we use square centimetres, not just centimetres. The area equals 441 square centimetres.",
        },
    },
    "IPMTB_grade5_ch04_q011": {
        "steps": {
            1: "Now let's check: is 1000 a perfect square? We find the square root of 1000. "
               "We know that 31 squared equals 961, and 32 squared equals 1024. "
               "Since 31 squared, which is 961, is less than 1000, which is less than 1024, that is 32 squared, "
               "1000 is not a perfect square.",
            2: "Since 31 squared, which is 961, is only a 3 digit number, and 32 squared, which is 1024, is a 4 digit number, "
               "the least 4 digit perfect square must be 32 squared.",
        },
    },
    "IPMTB_grade5_ch04_q029": {
        "hints": {
            2: "Here's a similar problem: If a square has a side of 15 centimetres, its area equals 15 times 15, "
               "which is 225 square centimetres. Notice the unit is square centimetres, "
               "because we multiplied centimetres by centimetres!",
        },
        "steps": {
            4: "Now add the correct unit. Since we multiplied centimetres by centimetres, the unit is square centimetres. "
               "The area equals 676 square centimetres.",
        },
    },
}
