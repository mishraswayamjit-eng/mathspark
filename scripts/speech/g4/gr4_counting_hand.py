"""Hand-written lines for gr4_counting.

HAND[question id] = {"q": str, "o": {index: str}, "h": {index: str}, "s": {index: str}}
Lines not given here are narrated by the rules.
"""

HAND = {
    # ── Past papers: the question is printed as a terse note ──
    "EXT_G4_FP_2020_026": {
        "q": "There are 8 points on a circle. How many line segments can be drawn joining any two of them?",
    },
    "EXT_G4_FP_2021_004": {
        "q": "A, B, C and D play chess. Each plays 2 games with every other player. How many games are played in total?",
    },
    "EXT_G4_FP_2021_014": {
        "q": "Some points are on a circle. A maximum of 15 line segments can be drawn joining them. How many points are there?",
    },
    "EXT_G4_FP_2023_031": {
        "q": "Using the digits 4, 7, 6 and 9, each only once, how many 4-digit odd numbers can be made?",
    },
    "EXT_G4_FP_2023_035": {
        "q": "15 people are at a meeting, and each shakes hands once with every other person. How many handshakes are there in total?",
    },
    "EXT_G4_FP_2024_029": {
        "q": "Using the digits 1, 5, 3 and 7, each once, how many numbers greater than 5000 can be made?",
    },
    "EXT_G4_FP_2025_019": {
        "q": "Using 7, 6, 9 and 4, each once, how many 4-digit odd numbers can be made?",
    },

    # ── Newly written questions: lines with bracketed lists ──
    "G4A_COUNTING_025": {
        "h": {2: "A similar problem: among numbers from 10 to 39, tens digit 1 gives 1 number, which is 10. "
                 "Tens digit 2 gives 2 numbers, 20 and 21. And tens digit 3 gives 3 numbers, 30, 31 and 32. "
                 "That is 1 plus 2 plus 3, which is 6 numbers."},
        "s": {0: "Tens digit 1 gives 1 number, which is 10. Tens digit 2 gives 2 numbers, 20 and 21. "
                 "Tens digit 3 gives 3 numbers, and so on.",
              1: "Tens digit 9 gives 9 numbers, from 90 to 98."},
    },
    "G4A_COUNTING_030": {
        "s": {0: "Ending in 0: the hundreds digit has 3 choices, 1, 2 or 3, and the tens digit then has 2 choices. "
                 "3 times 2 equals 6."},
    },
    "PYQ_2016_Q17": {
        "h": {2: "Here is a similar one: P, Q and R play, and each player plays three games with every other player. "
                 "The pairs are P and Q, P and R, and Q and R, which is 3 pairs. "
                 "Each pair plays 3 games, so 3 times 3, which is 9, games are played."},
    },
    "G4A_COUNTING_002": {
        "s": {0: "Count the children in front of Meera and behind her. 7 minus 1 equals 6 in front, and 5 minus 1 equals 4 behind."},
    },
    "G4A_COUNTING_031": {
        "h": {2: "A similar problem: a bell takes 8 seconds to ring 3 times. That is 2 gaps, so each gap is 4 seconds. "
                 "Ringing 6 times has 5 gaps, and that takes 5 times 4, which is 20 seconds."},
    },
    "G4A_COUNTING_033": {
        "h": {2: "A similar problem: from 1 to 50, the digit 4 is in the ones place 5 times, in 4, 14, 24, 34 and 44. "
                 "It is in the tens place 10 times, from 40 to 49. That makes 15 times."},
    },
    "G4A_COUNTING_034": {
        "s": {0: "Count the multiples of 2 and the multiples of 3. 60 divided by 2 equals 30, and 60 divided by 3 equals 20."},
    },
    "G4A_COUNTING_043": {
        "h": {2: "A similar problem: 9 children are in a queue and Arun is at the very front. "
                 "The other children, 9 minus 1, which is 8, are behind him."},
    },
}
