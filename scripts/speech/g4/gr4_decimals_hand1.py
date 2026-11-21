"""Hand-written narration for gr4_decimals: lines the rules cannot say well.

HAND is sparse: {question id: {"q": ..., "o0".."o3": ..., "h0".."h2": ..., "s0"..: ...}}.
Lines left out go to the rules in gr4_decimals_rules.py.

Hint and step lines written for the rewritten teaching help (data/bank-import/g4/renarrate.json)
are in gr4_decimals_hand2.py; this file holds no hint or step line for those questions.
"""

HAND = {
    "EXT_G4_FP_2020_012": {
        "q": "Express 8 hours 45 minutes as a decimal fraction.",
    },
    "EXT_G4_FP_2021_026": {
        "q": "Which is the correct order of decimals?",
        "h0": "This is about comparing decimals. The sign between the numbers means, is less than. So each number must be smaller than the one after it.",
        "s3": "The correct order is: 4.004 is less than 4.04, which is less than 4.4, which is less than 4.444.",
    },
    "EXT_G4_FP_2022_024": {
        "q": "Arrange the decimals 0.0075, 0.219, 0.082, 0.07 and 0.008 in descending order. What is the sum of the 1st and the 4th?",
    },
    "EXT_G4_FP_2024_031": {
        "s2": "The others give: 6 over 24 is one quarter, 5 over 80 is 1 over 16, and 8 over 36 is 2 over 9. None of those is 1 over 8.",
    },
    "G4A_DECIMALS_001": {
        "h2": "A similar one: in 0.917, the digits after the point are 9 in the tenths, 1 in the hundredths, and 7 in the thousandths. So the thousandths digit there is 7.",
    },
    "G4A_DECIMALS_018": {
        "q": "Which of these is the greatest? 0.58, 3 over 5, 5 over 8, or 0.65?",
    },
    "G4A_DECIMALS_029": {
        "q": "Each of the digits 0, 3, 5 and 8 is used once to fill the boxes in a number with one box before the decimal point and three boxes after it. What is the difference between the greatest and the smallest numbers that can be made?",
        "h2": "A similar one: the digits 0, 2 and 7, with one box before the decimal point and two boxes after it. The greatest is 7.20 and the smallest is 0.27. The difference is 7.20 minus 0.27, which is 6.93.",
    },
    "G4A_DECIMALS_034": {
        "q": "Arrange from smallest to greatest: 0.4, 3 over 8, 0.38, and 7 over 20.",
        "s3": "From smallest to greatest: 7 over 20, 3 over 8, 0.38, and 0.4.",
    },
    "G4A_DECIMALS_039": {
        "s1": "Pair them up: 2.50 plus 5.00, 3.00 plus 4.50, and 3.50 plus 4.00, each make 7.50 rupees. For example, 2.50 plus 5.00 equals 7.50.",
    },
    "G4A_DECIMALS_040": {
        "s3": "Altogether, 16 plus 4, which is 20 pieces, can be cut.",
    },
    "G4A_DECIMALS_042": {
        "q": "A decimal number is written as 4, point, box, box, with one digit in each box. The three digits of the number are all different, and they add up to 9. How many such numbers can be made?",
        "h2": "A similar problem: for 2, point, box, box, with all digits different and adding up to 6, the boxes must make 4. The pairs are 0 and 4, 1 and 3, 2 and 2, 3 and 1, 4 and 0. The pair 2 and 2 repeats a digit, so 4 numbers remain: 2.04, 2.13, 2.31 and 2.40.",
    },
    "G4A_DECIMALS_043": {
        "q": "Each of the digits 0, 4, 5 and 9 is used exactly once to fill the boxes in a number with two boxes before the decimal point and two boxes after it. Which number that can be made is closest to 50?",
        "h2": "A similar problem: with the digits 0, 2, 3 and 9, which number, with two boxes before the decimal point and two after it, is closest to 30? Just below 30 the best is 29.30, which is 0.70 away. Just above 30 the best is 30.29, which is 0.29 away. So 30.29 is closest.",
    },
    "G4A_DECIMALS_049": {
        "h2": "A similar problem: a cap costs 5 rupees more than a ball, and 1 cap and 2 balls cost 41 rupees. Take away the extra 5 rupees: 41 minus 5 is 36, which is the cost of 3 balls. So a ball costs 12 rupees, and a cap costs 12 plus 5, which is 17 rupees.",
    },
    "G4A_DECIMALS_050": {
        "h2": "A similar problem: Lata had to multiply a number by 10 but divided by 10 and got 0.9. Her number was 0.9 times 10, which is 9, so she should have got 9 times 10, which is 90.",
    },
    "G4A_DECIMALS_051": {
        "q": "In the number 5, point, box, 8, the box holds one digit. The number is greater than 5.4 and less than 5.68. How many different digits can go in the box?",
        "h1": "5.4 is the same as 5.40. Find the smallest digit that makes 5, point, box, 8 greater than 5.40.",
        "h2": "A similar problem: 3, point, box, 5 is greater than 3.2 and less than 3.55. Write 3.2 as 3.20. Then 3.25, 3.35 and 3.45 fit, but 3.15 is too small and 3.55 is not less than 3.55. So 3 digits fit.",
    },
    # Past papers (questions only; their hints and steps were rewritten, see gr4_decimals_hand2.py)
    "PYQ_2016_Q30": {
        "q": "What is the sum of the smallest and the greatest of the following numbers: 0.023, 0.23, 0.0023 and 2.3?",
    },
    "PYQ_2017_Q25": {
        "q": "Suppose d is a digit. For how many values of d is 2.00 d 5 greater than 2.005?",
    },
    "PYQ_2018_Q06": {
        "q": "Which is the smallest decimal fraction of the given ones?",
    },
    "PYQ_2018_Q08": {
        "q": "What is the place value of the digit 5 in the number 7.256?",
    },
    "PYQ_2019_Q19": {
        "q": "If the decimal fraction 0.0357 is multiplied by 100, what will the answer be?",
    },
    # Questions only (hints and steps rewritten, in the first round or the redo round)
    "Q_CH11_013": {
        "q": "Which is the greatest: 0.5, 0.05, 0.55 or 0.505?",
    },
    "Q_CH11_024": {
        "q": "Arrange in ascending order: 3.3, 3.03, 3.303 and 3.33.",
    },
    "Q_CH11_025": {
        "q": "What is the product 0.25 times 0.4, times 0.8?",
    },
    "Q_CH12_022": {
        "q": "240 paise equals how many rupees?",
    },
    "Q_CH12_023": {
        "q": "4.06 rupees equals how many paise?",
    },
}

LINES = {}
