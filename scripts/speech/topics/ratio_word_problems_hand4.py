"""Hand-written narration that was in the part file but in no helper file.

EXT_G5_WS_B3_038 had hand-written lines in data/question-speech/parts/ratio-word-problems.json
that the script could not reproduce (it fell back to the general rule). They are kept here,
word for word, so that running the script leaves the entry exactly as it was.
"""

HAND = {
    "EXT_G5_WS_B3_038": {
        "q": "A worker is paid 8 rupees per hour up to 30 hours. Overtime is twice the usual wage. If he is paid 336 rupees, how many hours did he work overtime?",
        "hints": [
            "Split the pay into two parts: the pay for the first 30 hours at the usual wage, and the extra pay for overtime.",
            "The first 30 hours earn 30 times 8, which is 240 rupees. Take that away from 336 rupees to get the overtime pay. Each overtime hour pays twice 8 rupees. How many such hours make up the overtime pay?",
            "Example: 5 rupees an hour up to 10 hours, double for overtime, total pay 80 rupees. Usual pay: 10 times 5 equals 50 rupees. Overtime pay: 80 minus 50 equals 30 rupees. At 10 rupees an hour, that is 30 divided by 10, which is 3 overtime hours.",
        ],
        "steps": [
            "Regular equals 30 times 8, which is 240 rupees.",
            "Overtime pay equals 336 minus 240, which is 96 rupees.",
            "Overtime hours equals 96 divided by 16, which is 6.",
        ],
    },
}
