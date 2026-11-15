"""Hand-written narration: past-paper questions 2016 to 2019 (unitary method, men and days).

Each entry gives the question, the hints and the steps as spoken. Answer choices are spoken by rule.
"""

HAND = {
    "EXT_G5_FP_2016_007": {
        "q": "A worker is paid 3 rupees per hour, up to 40 hours. Overtime is twice the payment for regular time. If he is paid 168 rupees, how many hours of overtime did he work?",
        "hints": [
            "First, find what he earns for the regular 40 hours. The money left over is overtime pay, and overtime pays 6 rupees each hour.",
            "The overtime rate is 2 times 3 rupees, which is 6 rupees per hour. Hours equal the money, divided by the rate per hour.",
            "",
        ],
        "steps": [
            "Regular pay is 40 times 3, which is 120 rupees.",
            "Overtime pay is 168 minus 120, which is 48 rupees.",
            "The overtime rate is 2 times 3, which is 6 rupees per hour.",
            "Overtime hours are 48 divided by 6, which is 8 hours.",
        ],
    },
    "EXT_G5_FP_2016_017": {
        "q": "If 40 grams of talc powder costs 12 rupees, what is the cost of 70 grams of talc powder?",
        "hints": [
            "Find the cost of just 1 gram first. Then multiply by 70.",
            "Unitary method: find the value of 1, then multiply.",
            "",
        ],
        "steps": [
            "The cost of 1 gram is 12 divided by 40, which is 0.30 rupees.",
            "The cost of 70 grams is 70 times 0.30, which is 21 rupees.",
        ],
    },
    "EXT_G5_FP_2016_034": {
        "q": "If 12 buckets can hold 108 litres of water, how many buckets will be required to store 162 litres of water?",
        "hints": [
            "Find how many litres one bucket holds. Then see how many such buckets are needed for 162 litres.",
            "Unitary method: litres per bucket equal the total, divided by the number of buckets.",
            "",
        ],
        "steps": [
            "1 bucket holds 108 divided by 12, which is 9 litres.",
            "Buckets for 162 litres: 162 divided by 9, which is 18.",
        ],
    },
    "EXT_G5_FP_2017_008": {
        "q": "A piece of work can be done by 72 men in 40 hours. How many hours will 9 men take, to complete the same work?",
        "hints": [
            "Fewer men take more time. The total work, which is men times hours, stays the same. 9 men is how many times fewer than 72 men?",
            "Men times hours is constant. This is inverse proportion.",
            "",
        ],
        "steps": [
            "The total work is 72 times 40, which is 2880 man hours.",
            "The time for 9 men is 2880 divided by 9, which is 320 hours.",
            "Check: 72 men is 8 times 9 men, so it takes 8 times the time. 40 times 8 is 320.",
        ],
    },
    "EXT_G5_FP_2017_022": {
        "q": "A worker gets 504 rupees for 7 days of work. How many days should he work, to get 792 rupees?",
        "hints": [
            "Find the pay for one day first. Then see how many days make 792 rupees.",
            "Unitary method: 1 day's pay equals the total, divided by the days.",
            "",
        ],
        "steps": [
            "Find the pay for one day: 504 divided by 7 is 72. So he earns 72 rupees a day.",
            "Now see how many days, at 72 rupees a day, make 792 rupees: 792 divided by 72 is 11.",
            "So, he should work 11 days.",
        ],
    },
    "EXT_G5_FP_2017_031": {
        "q": "A dozen pencils cost 18 rupees. How much would you pay for 18 pencils?",
        "hints": [
            "1 dozen is 12 pencils. Find the cost of one pencil first.",
            "Unitary method: find the value of 1.",
            "",
        ],
        "steps": [
            "12 pencils cost 18 rupees, so 1 pencil costs 1.50 rupees.",
            "18 pencils cost 18 times 1.50, which is 27 rupees.",
        ],
    },
    "EXT_G5_FP_2018_010": {
        "q": "Nine men complete a certain work in 32 days. Then, in how many days will 72 men complete the same work?",
        "hints": [
            "More men finish faster. 72 men is how many times 9 men? Then divide the days by that number.",
            "Men times days is constant. This is inverse proportion.",
            "",
        ],
        "steps": [
            "The total work is 9 times 32, which is 288 man days.",
            "Days for 72 men: 288 divided by 72, which is 4 days.",
            "Check: 72 is 8 times 9, so 32 divided by 8 is 4.",
        ],
    },
    "EXT_G5_FP_2018_025": {
        "q": "After selling 15 dozens of bananas, a man gains 45 rupees. How many dozens of bananas should he sell, so as to gain 84 rupees?",
        "hints": [
            "Find how much he gains on just one dozen. Then divide 84 by that.",
            "Unitary method: the gain per dozen equals the total gain, divided by the dozens.",
            "",
        ],
        "steps": [
            "Find the gain on one dozen: 45 divided by 15 is 3. So he gains 3 rupees on each dozen.",
            "Now see how many dozens give a gain of 84 rupees: 84 divided by 3 is 28.",
            "So, he should sell 28 dozens.",
        ],
    },
    "EXT_G5_FP_2019_009": {
        "q": "Five persons consume 1 kilogram of rice in a day. Determine the amount of rice that will be consumed by 20 people in a week.",
        "hints": [
            "20 people is how many times 5 people? That tells you the rice for one day. A week has 7 days.",
            "More people means more rice. This is direct proportion. 1 week is 7 days.",
            "",
        ],
        "steps": [
            "20 divided by 5 is 4. So 20 people eat 4 times 1, which is 4 kilograms in a day.",
            "In a week: 4 times 7, which is 28 kilograms.",
        ],
    },
    "EXT_G5_FP_2019_015": {
        "q": "A five litre can of liquid soap costs 370 rupees. What would be the cost of a three litre can of the same liquid soap?",
        "hints": [
            "Find the cost of 1 litre first. Then multiply by 3.",
            "Unitary method.",
            "",
        ],
        "steps": [
            "1 litre costs 370 divided by 5, which is 74 rupees.",
            "3 litres cost 3 times 74, which is 222 rupees.",
        ],
    },
    "EXT_G5_FP_2019_029": {
        "q": "A machine produces 150 toys in one minute. How many toys will it produce in 18 seconds?",
        "hints": [
            "Find how many toys in 1 second: 150 divided by 60. Then multiply by 18.",
            "1 minute is 60 seconds. Unitary method.",
            "",
        ],
        "steps": [
            "Toys in 1 second: 150 divided by 60, which is 2.5.",
            "In 18 seconds: 2.5 times 18, which is 45 toys.",
        ],
    },
}
