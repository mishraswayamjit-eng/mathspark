"""Hand-written narration for gr4_decimals, for the hints and steps rewritten in the bank
(data/bank-import/g4/renarrate.json). The new help is plain sentences, so the rules read nearly
all of it; only the lines below needed a hand.
"""

HAND = {
    # '2.00d5' is a number with a letter in one place: say the letter apart from the digits
    "PYQ_2017_Q25": {
        "h1": "Write 2.005 as 2.0050 so that it has four decimal places, like 2.00 d 5. The two numbers match until the thousandths place, where one has d and the other has 5. Test the digits there.",
        "h2": "A similar example: for how many digits d is 3.0 d 2 greater than 3.07? Write 3.07 as 3.070. If d is 8 or 9 the number is bigger. If d is 7 we get 3.072, which is also bigger than 3.070. Any smaller digit makes it smaller. So there are 3 values: 7, 8 and 9.",
        "s1": "Compare 2.00 d 5 with 2.0050 from the left. The ones, tenths and hundredths match. In the thousandths place we compare d with 5.",
        "s2": "If d is 6, 7, 8 or 9, then d is more than 5, so 2.00 d 5 is greater. That is 4 values.",
        "s3": "Do not forget when d is 5. Then the number is 2.0055, and 2.0055 is greater than 2.0050 because of its last digit. If d is 4 or less, the number is smaller.",
    },
}

LINES = {}
