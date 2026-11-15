"""Lines written by hand for the money-percent topic, keyed by question id.

Keys inside a question: "q", "o0".."o3" (options), "h0".."h2" (hints), "s0".. (steps).
Anything not listed here is produced by the rules in money_percent_rules.py.
"""
LINES = {
    "EXT_G5_FP_2016_014": {
        "h1": "Selling price equals cost price times 120, divided by 100, for 20 percent profit.",
    },
    "EXT_G5_FP_2016_021": {
        "h1": "Selling price of 1 equals cost price of 1, times 120, divided by 100. "
              "Number per rupee equals 1 divided by the selling price of one.",
        "s0": "Cost of 1 toffee equals 1 over 6 of a rupee.",
        "s1": "Selling price of 1 toffee equals 1 over 6, times 6 over 5, which is 1 over 5 of a rupee.",
    },
    "EXT_G5_FP_2016_039": {
        "s2": "1 percent equals 4500 divided by 150, which is 30. So the principal is 30 times 100, which is 3000 rupees.",
    },
    "EXT_G5_FP_2017_003": {
        "q": "A wholesaler allows a discount of 20 percent on the list price to a retailer. "
             "The retailer sells at 8 percent discount on the list price. The profit percent of the retailer is what?",
        "h1": "Profit percent equals, open bracket, selling price minus cost price, close bracket, divided by cost price, "
              "times 100. Choose a list price of 100 to make it easy.",
        "s0": "Let the list price be 100 rupees.",
        "s3": "Profit equals 92 minus 80, which is 12. Then 12 divided by 80, times 100, is 15 percent.",
    },
    "EXT_G5_FP_2017_021": {
        "h0": "If 90 percent are gone, what percent are left? Find that percent of 250000. "
              "Don't pick 225000, that's the number that disappeared.",
    },
    "EXT_G5_FP_2018_012": {
        "s1": "Try 10 more wins: wins equals 255, games equals 510. Then 255 divided by 510 equals 0.5, "
              "which is 50 percent. That works.",
        "s2": "Check 5: 250 divided by 505 is less than 50 percent. That does not work.",
    },
    "EXT_G5_FP_2019_004": {
        "h0": "Use principal equals simple interest times 100, divided by, open bracket, rate times time, close bracket. "
              "First work out rate times time, which is 9 times 3.",
        "s2": "Check: 9 percent of 700 is 63 a year. Times 3, that is 189. It matches.",
    },
    "EXT_G5_FP_2020_012": {
        "s0": "Money spent when buying equals 100 plus 300, which is 400 rupees.",
        "s1": "Money received when selling equals 200 plus 400, which is 600 rupees.",
    },
    "EXT_G5_FP_2021_002": {
        "s0": "Cost price: 1000 divided by 5 is 200 groups. Times 2 rupees, that is 400 rupees.",
        "s1": "Selling price: 1000 divided by 2 is 500 groups. Times 1 rupee, that is 500 rupees.",
    },
    "EXT_G5_FP_2022_005": {
        "s2": "Check: 8 percent of 400 is 32 a year. Times 5, that is 160. It matches.",
    },
    "EXT_G5_FP_2022_015": {
        "s1": "40 percent of the maximum equals 168, so 1 percent equals 4.2.",
    },
    "EXT_G5_FP_2022_037": {
        "h1": "25 percent equals one quarter. If one quarter of A equals 4, then A equals 4 times 4.",
    },
    "EXT_G5_FP_2023_009": {
        "s1": "Rate equals simple interest times 100, divided by, open bracket, principal times time, close bracket. "
              "That is 3852 times 100, divided by, open bracket, 6420 times 4, close bracket. "
              "That equals 385200 divided by 25680, which is 15.",
    },
    "EXT_G5_FP_2023_023": {
        "h0": "Loss equals cost price minus selling price, so cost price equals selling price plus loss. "
              "Find the cost price, then compare it with 542 rupees.",
    },
    "EXT_G5_FP_2024_017": {
        "h0": "The amount repaid includes the borrowed money plus interest. Subtract to find the interest, "
              "then use simple interest equals principal times rate times time, divided by 100, to find the rate.",
    },
    "EXT_G5_FP_2024_024": {
        "h0": "Find total cost, then total selling price, in two parts! "
              "Remember, 26 minus 14 bats are left for the second price.",
    },
    "EXT_G5_FP_2025_006": {
        "h0": "Profit would be twice the loss, which is 2 times 80, that is 160 rupees. "
              "Use that to find the cost price first.",
        "s0": "Profit would be 2 times 80, which is 160 rupees, at a selling price of 375 rupees.",
        "s2": "The original selling price, at a loss of 80 rupees, equals 215 minus 80, which is 135 rupees.",
    },
    "EXT_G5_FP_2025_024": {
        "h1": "Selling price equals cost price times, open bracket, 100 minus loss percent, close bracket, divided by 100. "
              "So cost price equals selling price times 100, divided by, open bracket, 100 minus loss percent, close bracket.",
    },
}
