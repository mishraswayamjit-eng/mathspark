"""Hand-written narration for gr4_decimals: lines the rules cannot say well.

HAND is sparse: {question id: {"q": ..., "o0".."o3": ..., "h0".."h2": ..., "s0"..: ...}}.
Lines left out go to the rules in gr4_decimals_rules.py.
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
    # Past papers
    "PYQ_2016_Q30": {
        "q": "What is the sum of the smallest and the greatest of the following numbers: 0.023, 0.23, 0.0023 and 2.3?",
    },
    "PYQ_2017_Q17": {
        "q": "Instead of writing 9.7, a student wrote 0.97. By how much was he wrong?",
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
    # Hand-crafted chapter questions, whose hints and steps are written as terse notes
    "Q_CH11_001": {
        "h2": "Example: 45.3 divided by 10 equals 4.53. The decimal moved 1 place left. Now try 12.5 divided by 10.",
    },
    "Q_CH11_002": {
        "h2": "Example: 34.5 divided by 100 equals 0.345. That is 2 places left. Now try with 12.5.",
    },
    "Q_CH11_003": {
        "h1": "10000 has 4 zeros, so move the decimal 4 places to the left.",
        "h2": "Start at 12.5 and move left 4 times: 1.25, then 0.125, then 0.0125, then 0.00125.",
    },
    "Q_CH11_004": {
        "h1": "5 times 5 equals 25, and the remainder is 3. Now bring down a 0: 30 divided by 5 equals 6.",
        "h2": "Using long division: 28.0 divided by 5. 5 into 28 is 5, remainder 3. Then 30 divided by 5 equals 6. The answer is 5.6.",
        "s0": "Set up the long division: 28.0 divided by 5.",
    },
    "Q_CH11_005": {
        "s0": "Set up: 11.2 divided by 4.",
        "s1": "4 into 11 goes 2 times, since 4 times 2 is 8. The remainder is 11 minus 8, which is 3.",
        "s2": "Bring down 2 to get 32. 4 into 32 goes 8 times, since 4 times 8 is 32.",
    },
    "Q_CH11_006": {
        "h1": "Multiply both numbers by 100: 1.264 times 100 equals 126.4, and 0.04 times 100 equals 4. Now divide 126.4 by 4.",
        "h2": "126.4 divided by 4: 4 into 12 is 3. 4 into 6 is 1, remainder 2. Bring down the 4, and 24 divided by 4 is 6. The answer is 31.6.",
        "s1": "Now divide 126.4 by 4 using long division.",
        "s2": "4 into 12 is 3. 4 into 6 is 1, remainder 2. Bring down the 4: 24 divided by 4 is 6. So 126.4 divided by 4 equals 31.6.",
    },
    "Q_CH11_007": {
        "h1": "Multiply both by 100: 3.43 times 100 equals 343, and 0.07 times 100 equals 7. Now divide 343 by 7.",
        "s1": "Now divide: 343 divided by 7.",
        "s2": "7 times 4 is 28, and 34 minus 28 is 6. Bring down the 3: 63 divided by 7 is 9. So 343 divided by 7 equals 49.",
    },
    "Q_CH11_008": {
        "h1": "Move the decimal 1 place to the left.",
        "h2": "7.06: move the decimal 1 place left, to get 0.706.",
    },
    "Q_CH11_009": {
        "h1": "100 has 2 zeros, so move the decimal 2 places left.",
        "h2": "652.7 becomes 65.27, then 6.527. The answer is 6.527.",
    },
    "Q_CH11_011": {
        "h1": "What is 3 divided by 4? Think: 4 times 7 is 28, so 4 goes into 30 seven times, with remainder 2.",
        "h2": "3 divided by 4 equals 0.75. That is because, for 3.00 divided by 4, 4 into 30 is 7 remainder 2, and 4 into 20 is 5.",
        "s1": "4 into 3.00: 4 into 30 is 7, because 4 times 7 is 28, with remainder 2.",
    },
    "Q_CH11_012": {
        "s0": "Write it as a fraction: 3 decimal places means over 1000. 0.125 equals 125 over 1000.",
        "s1": "Find the H C F of 125 and 1000. Both are divisible by 125.",
    },
    "Q_CH11_013": {
        "q": "Which is the greatest: 0.5, 0.05, 0.55 or 0.505?",
        "h2": "Comparing: 0.550 is greater than 0.505, which is greater than 0.500, which is greater than 0.050. The greatest is 0.550, which is 0.55.",
        "s1": "Compare the tenths place first: all have 0 or 5.",
    },
    "Q_CH11_014": {
        "h1": "34.560 plus 7.800, plus 0.004. Now add column by column from the right.",
        "s0": "Align the decimal points and add zeros.",
        "s1": "Add from the right: thousandths, 4. Hundredths, 6. Tenths, 13: write 3, carry 1.",
        "s2": "Ones: 4 plus 7, plus the carried 1, equals 12. Tens: 3.",
        "s3": "The answer is 42.364.",
    },
    "Q_CH11_015": {
        "h1": "50.00 minus 23.75: start from the hundredths. 0 minus 5? You'll need to borrow!",
        "h2": "Borrow step by step: 50.00 becomes 49.9, with 10 in the hundredths place. Then 10 minus 5 is 5, 9 minus 7 is 2, 9 minus 3 is 6, and 4 minus 2 is 2.",
        "s1": "Hundredths: 0 minus 5 needs a borrow, so 10 minus 5 equals 5.",
        "s3": "The answer is 26.25.",
    },
    "Q_CH11_016": {
        "h0": "First multiply without the decimals: what is 25 times 4?",
        "h1": "25 times 4 equals 100. Now count the total decimal places in both numbers: 1 plus 1 equals 2.",
        "h2": "Put 2 decimal places in 100, to get 1.00, which is 1.0.",
        "s0": "Ignore the decimals and multiply: 25 times 4 equals 100.",
        "s1": "Count the decimal places: 2.5 has 1, and 0.4 has 1. The total is 2.",
        "s2": "Place the decimal: 100 becomes 1.00, which is 1.0.",
    },
    "Q_CH11_017": {
        "h0": "Multiply the numbers without decimals first: what is 3 times 6?",
        "h1": "3 times 6 equals 18. Now count the decimal places: 0.03 has 2 places, and 0.6 has 1 place. The total is 3.",
        "h2": "Put 3 decimal places in 18, to get 0.018.",
        "s0": "Multiply without decimals: 3 times 6 equals 18.",
        "s1": "Count the decimal places: 0.03 has 2, and 0.6 has 1. That makes 3 in total.",
        "s2": "Place 3 decimal places: 18 becomes 0.018.",
    },
    "Q_CH11_020": {
        "s0": "Identify each digit's place value.",
        "s1": "The digit 8 is the second digit after the decimal point. The 2nd place after the decimal is the hundredths.",
    },
    "Q_CH11_021": {
        "h1": "After the decimal: 0 is in the tenths, 6 in the hundredths, 3 in the thousandths, and 9 in the ten-thousandths.",
        "h2": "6 is in the hundredths place. Its value is 6 times 0.01, which is 0.06.",
        "s0": "Identify the place of the 6 in 2.0639.",
        "s1": "6 is in the hundredths place. One hundredth is 1 over 100, which is 0.01.",
        "s2": "The value is 6 times 0.01, which is 0.06.",
    },
    "Q_CH11_022": {
        "h1": "Apples: what is 2.5 times 120? Oranges: what is 1.25 times 80?",
        "s0": "The cost of the apples is 2.5 times 120. And 2.5 times 120 is 300.",
        "s1": "The cost of the oranges is 1.25 times 80. And 1.25 times 80 is 100.",
        "s2": "The total is 300 plus 100, which is 400.",
    },
    "Q_CH11_023": {
        "h0": "Dividing by 10 moves the decimal 1 place to the left.",
        "h1": "809 can be written as 809.0. Now move the decimal 1 place left.",
        "s1": "Divide by 10: move the decimal 1 place left. 809.0 becomes 80.9.",
    },
    "Q_CH11_024": {
        "q": "Arrange in ascending order: 3.3, 3.03, 3.303 and 3.33.",
        "h0": "Make all the decimals the same length: 3.300, 3.030, 3.303 and 3.330.",
        "h2": "So the ascending order is: 3.03, 3.3, 3.303, 3.33.",
        "s0": "Equalize the decimal places. 3.300, 3.030, 3.303, 3.330.",
        "s1": "Compare digit by digit from the left. 3.030 is less than 3.300, which is less than 3.303, which is less than 3.330.",
        "s2": "The ascending order is: 3.03, 3.3, 3.303, 3.33.",
    },
    "Q_CH11_025": {
        "q": "What is the product 0.25 times 0.4, times 0.8?",
        "h0": "Do it step by step. First multiply 0.25 by 0.4, then multiply the result by 0.8.",
        "h1": "0.25 times 0.4: multiply 25 times 4 to get 100. The decimal places are 2 plus 1, which is 3. So we get 0.100, which is 0.1.",
        "h2": "Now 0.1 times 0.8: multiply 1 times 8 to get 8. The decimal places are 1 plus 1, which is 2. So we get 0.08.",
        "s0": "First: 0.25 times 0.4. 25 times 4 equals 100. 2 plus 1 makes 3 decimal places, so we get 0.100, which is 0.1.",
        "s1": "Then: 0.1 times 0.8. 1 times 8 equals 8. 1 plus 1 makes 2 decimal places, so we get 0.08.",
    },
    "Q_CH12_002": {
        "h1": "The number of dollars is 100 divided by 40.",
    },
    "Q_CH12_022": {
        "q": "240 paise equals how many rupees?",
    },
    "Q_CH12_023": {
        "q": "4.06 rupees equals how many paise?",
        "s1": "Move the decimal 2 places right: 4.06 becomes 406. 4.06 times 100 equals 406.",
    },
}

LINES = {}
