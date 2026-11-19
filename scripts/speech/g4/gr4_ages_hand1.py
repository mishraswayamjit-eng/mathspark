"""Hand-written narration for gr4_ages: lines the rules do not say well enough.

HAND[question id] = {"q": ..., "options": [...], "hints": [...], "steps": [...]}; None leaves a line to the rules.
"""
N = None

HAND = {
    "EXT_G4_FP_2021_010": {
        "q": "The sum of the ages of a mother and daughter, 5 years ago, was 5 x. What will the sum be, 5 years hence?",
    },
    "EXT_G4_FP_2021_019": {
        "q": "The ages of a husband and wife, 6 years ago, added up to 48. At present, the husband, wife and son add up to 63. What is the son's age, 6 years hence?",
    },
    "EXT_G4_FP_2022_035": {
        "q": "The sum of the ages of Nirav and Vipul, 3 years ago, was 38. What is Vipul's age after 2 years, if he is 2 years younger than Nirav?",
        "hints": [N, N, "Similar example: 2 years ago the ages of Asha and Ravi added up to 26. Now the sum is 26 plus 2 times 2, which is 30. Ravi is 4 years younger, so take 4 away and halve: 30 minus 4, then divided by 2, is 13. Ravi is 13 now. After 3 years he will be 13 plus 3, which is 16."],
        "steps": [N, "Vipul is 2 years younger. Take away Nirav's 2 extra years, then share equally. 44 minus 2, then divided by 2, equals 21."],
    },
    "PYQ_2016_Q10": {
        "steps": [N, N, N, "Check: in 2020 Sarika is 14 and Surya is 7, and 14 is twice 7. So the year is 2020."],
    },
    "PYQ_2019_Q05": {
        "q": "The sum of the ages of a husband and wife 6 years ago was 48 years. The sum of the ages of the husband, wife and son at present is 63 years. What will be the age of the son, 6 years hence?",
    },
    "G4A_AGES_005": {
        "hints": [N, N, "Example: someone born in 2010 turns 2021 minus 2010, which is 11, on the birthday in 2021."],
    },
    "G4A_AGES_036": {
        "hints": [N, N, "A similar one: a father is 4 times as old as his son, and in 5 years their ages will total 60. Today they total 60 minus 10, which is 50. That is 5 parts, so the son is 10 and the father is 40."],
    },
    "G4A_AGES_033": {
        "q": "Asha is 8 years old. She tells her older sister Bina: When I am as old as you are now, you will be 20 years old. How old is Bina now?",
    },
}

LINES = {}
