"""Lines written by hand for the imported textbook items (ids IPMTB_grade5_...), where the rules in
algebra_imported_rules.py do not give a line worth hearing.

HAND[question id] = {"q": "...", "options": {index: "..."}, "hints": {index: "..."}, "steps": {index: "..."}}
Anything not listed falls back to the rules.
"""

P = "IPMTB_grade5_"
OB = "open bracket"
CB = "close bracket"

HAND = {}

# The hint prints the symbols in brackets: (x), (*), (=).
HAND[P + "ch08_q016"] = {
    "hints": {
        1: "Start by letting the unknown number be x. Now read the sentence again: The number, x, when multiplied by, "
           "times, 4 gives, equals, 20. Just string those symbols together!",
    },
}

# "multiplied by (x + y)": the brackets are the point of the question.
HAND[P + "ch09_q010"] = {
    "q": "What will be the answer when 4 is multiplied by, %s, x plus y, %s?" % (OB, CB),
}
HAND[P + "ch09_q028"] = {
    "q": "What will be the answer when 3 is multiplied by, %s, x plus y, %s?" % (OB, CB),
}

HAND[P + "ch09_q014"] = {
    "steps": {
        3: "Let's verify: S times T equals 7 times 10, which is 70, and that is D. It checks out!",
    },
}

# The maths line under this step repeats the working already in the text.
HAND[P + "ch09_q029"] = {
    "steps": {
        7: "Notice something cool: 2 c plus 2 A minus 2 b equals 2 times, %s, c plus A minus b, %s. "
           "That is 2 times, %s, 1 plus 2 minus 3, %s, which is 2 times 0, which is 0. "
           "You can factor out the 2 to make it even simpler!" % (OB, CB, OB, CB),
    },
}
