"""Hand-written narration for the imported fractions questions (ids AIGEN_grade5_...).

Same shape as fractions_hand*.py: None (or a missing key) means 'use the rules'.
A step that has a maths line is said as its text followed by that maths line.
"""

P = "AIGEN_grade5_"

HAND = {
    P + "0799b640-0073-4a01-9861-29cced10698d": {
        "hints": [
            "After giving one third away, think about what fraction of the total is still remaining. "
            "Then work out what happens when one quarter of that remaining amount is also given away.",
            "If she gave away one third, she kept two thirds of the total. Then she gave away one quarter of that two thirds, "
            "so she kept three quarters of two thirds. What fraction of the original does she have before eating the 5 ladoos?",
            "Here's a similar problem. Ravi had some marbles. He lost one half of them, then gave away one third of the rest, "
            "and had 10 left. After losing half, he has one half of the total. After giving one third of the rest, "
            "he keeps two thirds times one half, which is one third of the total. So one third of the total equals 10, "
            "meaning the total is 30. Use the same approach for Priya's ladoos!",
        ],
        "steps": [
            "Let the total number of ladoos Priya made be N.",
            "She gave one third to neighbours, so she kept two thirds of N.",
            "Then she gave one quarter of the remaining to cousins, so she kept three quarters of the remaining. "
            "After the cousins, that is three quarters times two thirds N, which is 6 over 12 N, or one half of N.",
            "After eating 5 ladoos, she had 25 left. So before eating: one half of N, minus 5, equals 25.",
            "Solve for N: one half of N equals 25 plus 5, which is 30.",
            "Multiply both sides by 2: N equals 60.",
            "Priya made 60 ladoos in the beginning! Let's verify. Start with 60. She gave 20 to neighbours, "
            "which is one third, and was left with 40. She gave 10 to cousins, which is one quarter of 40, "
            "and was left with 30. She ate 5, and was left with 25.",
        ],
    },
    P + "7029fb7b-b253-42b2-895f-0ba3a875389f": {
        "q": "Ravi's grandmother gave him 600 rupees as a Pongal gift. He spent one quarter of the total on new books. "
             "From the remaining money, he gave 2 over 5 to his sister for bangles. Then, from what was left after that, "
             "he spent one third on sweets for the family. How much money, in rupees, does Ravi still have?",
        "options": ["270 rupees", "200 rupees", "160 rupees", "180 rupees"],
        "hints": [
            "Work step by step. After each spending, figure out what's left, before applying the next fraction. "
            "Don't apply all the fractions to the original 600 rupees!",
            "Start by finding one quarter of 600 rupees. That's what he spent on books. "
            "Subtract it from 600 rupees to get the remaining amount.",
            "Here's a similar problem. Meena has 400 rupees. She spends one half on clothes, so 200 rupees are left. "
            "Then she gives one quarter of the remaining to charity: one quarter times 200 is 50 rupees, "
            "so 150 rupees are left. Then she spends one third of 150 rupees, which is 50 rupees, on food, "
            "leaving 100 rupees. See how each fraction applies to what's left, not the original?",
        ],
        "steps": [
            "Ravi starts with 600 rupees. He spends one quarter on books. One quarter times 600 equals 150.",
            "Money remaining after books: 600 minus 150 equals 450.",
            "He gives 2 over 5 of the remaining 450 rupees to his sister. 2 over 5, times 450, equals 180.",
            "Money remaining after giving to sister: 450 minus 180 equals 270.",
            "He spends one third of the remaining 270 rupees on sweets. One third times 270 equals 90.",
            "Money Ravi still has: 270 minus 90 equals 180.",
            "So Ravi has 180 rupees left!",
        ],
    },
    P + "bf07efef-d936-4bea-aca0-bd914e8044d0": {
        "q": "During a school cricket tournament, Arjun collected donation money from his classmates. "
             "He spent 2 over 5 of the total amount on new cricket balls. From the remaining money, "
             "he spent three quarters on a new bat. After buying both, he had 90 rupees left. "
             "How much money did Arjun collect in total from his classmates?",
        "options": ["540 rupees", "600 rupees", "450 rupees", "360 rupees"],
        "hints": [
            "Think backwards! After spending 2 over 5 on balls, what fraction of the total is left? "
            "Then, from that leftover, what fraction remains after buying the bat?",
            "Start by finding what fraction remains after the cricket balls: 1 minus 2 over 5 leaves 3 over 5 of the total.",
            "Here's a similar problem. Meena had some money. She spent one third on books, then one half of the remaining "
            "on a bag, and had 100 rupees left. Remaining after books is two thirds of the total. After the bag, "
            "it is one half times two thirds, which is one third of the total. So one third of the total is 100 rupees, "
            "meaning the total is 300 rupees. Use the same approach for Arjun's problem!",
        ],
        "steps": [
            "Let the total money collected be T.",
            "Arjun spent 2 over 5 of T on cricket balls. So the remaining money after buying balls is: "
            "T minus 2 over 5 T, which equals 3 over 5 T.",
            "From this remaining amount, he spent three quarters on a bat. So the amount spent on the bat is: "
            "three quarters times 3 over 5 T, which equals 9 over 20 T.",
            "The money left after both purchases is the remaining one quarter of the leftover amount: "
            "one quarter times 3 over 5 T, which equals 3 over 20 T.",
            "We know this leftover equals 90 rupees: 3 over 20 T equals 90.",
            "Solve for T by multiplying both sides by 20 over 3: T equals 90 times 20 over 3. "
            "90 times 20 over 3 is 30 times 20, which is 600.",
            "So Arjun collected 600 rupees in total! Let's verify. Balls: 2 over 5 times 600 is 240 rupees. "
            "Remaining: 360 rupees. Bat: three quarters times 360 is 270 rupees. "
            "Left: 360 minus 270, which is 90 rupees.",
        ],
    },
}
