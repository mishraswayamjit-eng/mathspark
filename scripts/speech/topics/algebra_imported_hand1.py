"""Lines written by hand for the imported story problems (ids AIGEN_grade5_...), where the rules in
algebra_imported_rules.py do not give a line worth hearing.

HAND[question id] = {"q": "...", "options": {index: "..."}, "hints": {index: "..."}, "steps": {index: "..."}}
Anything not listed falls back to the rules.
"""

P = "AIGEN_grade5_"

HAND = {}

# The printed hint trails off: "34 ÷ 3 =... (you get the idea!)".
HAND[P + "2a3a9d94-355a-4b80-8058-323a8e29595f"] = {
    "hints": {
        2: "Here's a similar problem: Arjun buys 3 packs of stickers. He loses 4 stickers, then splits the rest equally "
           "into 6 groups of 5 stickers each. Total stickers in groups equals 6 times 5, which is 30. "
           "Before losing: 30 plus 4 equals 34. Per pack: 34 divided by 3, and so on. You get the idea!",
    },
}

# The check is printed as a chain of arrows: 16 → Tuesday → Wednesday.
HAND[P + "3916a850-b5f2-449b-969c-40f7a4975588"] = {
    "steps": {
        6: "Ananya had 16 stickers on Monday! Let's verify. Start with 16. Tuesday: 16 plus 32 equals 48. "
           "Wednesday: 48 minus 17 equals 31.",
    },
}

# A long hint that thinks aloud through three tries; said as briefly as the numbers allow.
HAND[P + "d9d91fe0-40c4-46c4-8d06-105ed62d59ff"] = {
    "hints": {
        2: "Here's a similar problem: A teacher buys x notebooks at 30 rupees each and a pen for 50 rupees. "
           "She pays 500 rupees and gets 100 rupees back. Total spent is 400 rupees. "
           "So 30 x plus 50 equals 400, so 30 x equals 350, so x is 350 divided by 30, about 11.67. "
           "Hmm, that doesn't work cleanly. Try another: she pays 500 rupees, gets 70 back, so spent 430 rupees. "
           "30 x plus 50 equals 430, so 30 x equals 380. Actually: she gets 50 back, so spent 450 rupees. "
           "30 x plus 50 equals 450, so 30 x equals 400, so x is 400 over 30. "
           "A clean one: she buys x pens at 25 rupees each and a box for 75 rupees. Pays 500, gets 50 back. "
           "Spent 450 rupees. So 25 x plus 75 equals 450, 25 x equals 375, and x equals 15 pens.",
    },
}

# "=?n" and "=?" are blanks to fill in.
HAND[P + "e14c9928-5051-4b07-b14c-d5a2d2b8b9ee"] = {
    "hints": {
        1: "Add up all the n terms: 2 n plus 3 n plus n plus 4 n plus 2 n equals how many n? "
           "Then add up all the number terms: 3 plus minus 1, plus 7 plus minus 5, plus 6 equals what?",
    },
}
