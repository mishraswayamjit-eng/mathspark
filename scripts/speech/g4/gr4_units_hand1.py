"""Hand-written narration for gr4_units: lines the rules cannot say well.

HAND is sparse: {question id: {"q": ..., "o0".."o3": ..., "h0".."h2": ..., "s0"..: ...}}.
Lines left out go to the rules in gr4_units_rules.py.
"""

HAND = {
    # Past papers whose question is printed as a telegram
    "EXT_G4_FP_2020_029": {
        "q": "A gold ring weighs 5 grams 15 milligrams. What is that as a decimal, in grams?",
    },
    "EXT_G4_FP_2021_009": {
        "q": "What is 2 metres, plus 2 decimetres, plus 15 centimetres?",
        "h2": "Similar example: 3 metres, plus 4 decimetres, plus 12 centimetres. 3 metres is 3 times 100, which is 300 centimetres. And 4 decimetres is 4 times 10, which is 40 centimetres. Then 300 plus 40, plus 12, equals 352 centimetres.",
    },
    "EXT_G4_FP_2021_017": {
        "q": "In a bag of beans, each bean weighs 2.5 grams. The weight of the beans is 0.5 kilograms. How many beans are there?",
    },
    "EXT_G4_FP_2022_031": {
        "q": "Express 11 kilograms and 11 grams as a decimal, in kilograms.",
    },
    "EXT_G4_FP_2022_039": {
        "q": "The juice of 4 mangoes is 250 millilitres. The juice of how many mangoes is 1 decalitre?",
    },
    "EXT_G4_FP_2024_014": {
        "q": "A shopkeeper sells 1 gross of eggs for 864 rupees. What is the cost of 1 score?",
    },
    "EXT_G4_FP_2025_023": {
        "q": "1 score of oranges costs 130 rupees, and 1 dozen apples cost 180 rupees. You buy 12 oranges and 17 apples. What is the cost?",
        "h2": "Similar example: 1 score of bananas costs 90 rupees and 1 dozen pears cost 120 rupees. One banana costs 90 divided by 20, which is 4.50 rupees. One pear costs 120 divided by 12, which is 10 rupees. So 10 bananas cost 45 rupees and 5 pears cost 50 rupees. Together that is 45 plus 50, which is 95 rupees.",
    },
    "EXT_G4_FP_2025_034": {
        "q": "160 hectograms of rice is distributed among 25 people. Each gets how many grams?",
    },
    "PYQ_2016_Q38": {
        "q": "Which of the following is equal to 11.11 kilograms?",
    },
    "PYQ_2017_Q15": {
        "q": "What is 2 metres, plus 2 decimetres, plus 15 centimetres?",
    },
    "PYQ_2019_Q37": {
        "q": "Express 7 kilograms 70 grams as a decimal.",
    },
    # Newly written questions
    "G4A_UNITS_015": {
        "h0": "A dozen is 12. Find how many lots of 12 are needed to reach at least 150.",
    },
    "G4A_UNITS_025": {
        "h1": "The well is 260 centimetres deep, and each day and night together the frog gains 50 minus 20, which is 30 centimetres. Find when the frog is within one 50 centimetre climb of the top.",
    },
    "G4A_UNITS_045": {
        "h2": "A similar problem: a crayon 8 centimetres long and a chalk 6 centimetres long, end to end, make a line 8 plus 6, which is 14 centimetres long.",
    },
    # Hand-crafted chapter questions, whose hints and steps are written as terse notes
    # (no hint or step line is kept here for the questions in data/bank-import/g4/renarrate.json:
    #  their help was rewritten, and the rules read the new sentences)
    "Q_CH12_001": {
        "s0": "Perimeter is the total length around a shape.",
        "s1": "Litre is for capacity or volume, kilogram is for mass or weight, and metre is for length.",
    },
    "Q_CH12_003": {
        "q": "How do we convert decametre to decimetre?",
    },
    "Q_CH12_004": {
        "h1": "Centi means 1 over 100. So a centilitre is 1 over 100 of a litre!",
        "h2": "1 centilitre equals 1 over 100 of a litre. That's the 1 over 100 relationship.",
        "s1": "Check each: a metre is 1 over 1000 of a kilometre, not 1 over 100. A gram is 1 over 10 of a decagram, not 1 over 100. A kilogram is 1 over 1000 of a tonne, not 1 over 100.",
        "s2": "A centilitre is 1 over 100 of a litre. Centi literally means hundredth!",
    },
    "Q_CH12_007": {
        "s1": "0.3 score is 0.3 times 20. And 0.3 times 20 is 6.",
    },
    "Q_CH12_008": {
        "h1": "We need to know how many gross equal 1 dozen. We know that 1 gross equals 12 dozens.",
        "h2": "1 dozen equals 1 over 12 of a gross.",
        "s1": "So 1 dozen equals 1 over 12 of a gross.",
        "s2": "1 over 12 of a gross makes a dozen.",
    },
    "Q_CH12_009": {
        "q": "4 kilometres, plus 40 metres, plus 400 centimetres, equals how many metres?",
    },
}

LINES = {}
