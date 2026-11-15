"""Hand-written narration: past-paper questions 2023 to 2025 and worksheet questions of the measurement-speed topic."""
from measurement_speed_hand1 import KMH_TO_MS, MS_TO_KMH, TDS
from measurement_speed_hand2 import DST, M_KM

HAND = {}

HAND["EXT_G5_FP_2023_003"] = {
    "q": "Shraddha runs five rounds around a 400 metre track in her school. For each round, she runs the first "
         "100 metres at 4 metres per second, and the remaining 300 metres at 5 metres per second. "
         "How much time did Shraddha take to complete the five rounds?",
    "options": ["6 minutes 45 seconds", "7 minutes 15 seconds", "7 minutes 25 seconds", "none of these"],
    "hints": [
        "Find the time for one round, in two parts. Time equals distance divided by speed. "
        "Add them, then multiply by 5, and change seconds into minutes.",
        TDS,
        "",
    ],
    "steps": [
        "First 100 metres: 100 divided by 4 equals 25 seconds. Remaining 300 metres: 300 divided by 5 equals 60 seconds.",
        "One round equals 25 plus 60, which is 85 seconds. Five rounds equals 85 times 5, which is 425 seconds.",
        "425 seconds equals 7 minutes 5 seconds, because 7 times 60 equals 420.",
        "That is not among options A to C. So, none of these.",
    ],
}

HAND["EXT_G5_FP_2024_008"] = {
    "q": "Nirav covers a distance of 680 kilometres in 8 hours, from A to B. On his return journey from B to A, "
         "he reduced his speed by 17 kilometres per hour. In how much time will he be back to A from B?",
    "options": ["None of these", "600 minutes", "720 minutes", "660 minutes"],
    "hints": [
        "Find his speed from A to B first: distance divided by time. Subtract 17 for the return, then find the time. "
        "The answer needs to be in minutes.",
        "Speed equals distance divided by time, and time equals distance divided by speed.",
        "",
    ],
    "steps": [
        "Speed from A to B equals 680 divided by 8, which is 85 kilometres per hour.",
        "Return speed equals 85 minus 17, which is 68 kilometres per hour.",
        "Time equals 680 divided by 68, which is 10 hours.",
        "10 times 60 equals 600 minutes.",
    ],
}

HAND["EXT_G5_FP_2024_023"] = {
    "q": "A train departs from London at 6 45 p m, and reaches Paris at 9 15 p m, on the same day. "
         "If the speed of the train is 32.5 metres per second, find the distance between London and Paris.",
    "options": ["294.5 kilometres", "292.5 kilometres", "306.5 kilometres", "None of these"],
    "hints": [
        "First find how long the journey takes. Then change that time into seconds, "
        "because the speed is in metres per second.",
        DST + " " + M_KM,
        "",
    ],
    "steps": [
        "6 45 p m, to 9 15 p m, is 2 hours 30 minutes, which equals 9000 seconds.",
        "Distance equals 32.5 times 9000, which is 292,500 metres.",
        "292,500 divided by 1000 equals 292.5 kilometres.",
    ],
}

HAND["EXT_G5_FP_2025_008"] = {
    "q": "A train crosses a pole in 28 seconds, running at a speed of 108 kilometres per hour. "
         "Find the length of the train.",
    "options": ["1008 metres", "980 metres", "720 metres", "840 metres"],
    "hints": [
        "Change the speed from kilometres per hour to metres per second first. "
        "Crossing a pole means the train covers exactly its own length.",
        KMH_TO_MS + " Length equals speed times time.",
        "",
    ],
    "steps": [
        "108 kilometres per hour equals 108 times 5, divided by 18, which is 30 metres per second.",
        "Length equals 30 times 28, which is 840 metres.",
    ],
}

HAND["EXT_G5_FP_2025_027"] = {
    "q": "To cover a distance of 432 kilometres, travelling at a speed of 24 metres per second, "
         "how much time will be required?",
    "options": ["4 hours 40 minutes", "5.5 hours", "4 hours", "None of these"],
    "hints": [
        "The distance is in kilometres, but the speed is in metres per second. "
        "Make the units match: change 24 metres per second to kilometres per hour.",
        MS_TO_KMH + " " + TDS,
        "",
    ],
    "steps": [
        "24 metres per second equals 24 times 18, divided by 5, which is 86.4 kilometres per hour.",
        "Time equals 432 divided by 86.4, which is 5 hours.",
        "5 hours is not among options A to C. So, none of these.",
    ],
}

HAND["EXT_G5_WS_B3_021"] = {
    "q": "If Anay can type 126 words in 3 minutes, how many words can he type in half a minute?",
    "options": ["42", "189", "21", "84"],
    "hints": [
        "Read the question carefully. This tests your understanding of rate problems. "
        "Identify what information is given, and what you need to find.",
        "Write down the key formula or relationship for rate problems. "
        "Think step by step about how to connect the given values to the answer.",
        "Try a simpler version of the problem first, then apply the same method to the actual numbers.",
    ],
    "steps": [
        "Rate equals 126 divided by 3, which is 42 words per minute.",
        "Half a minute equals 42 divided by 2, which is 21.",
    ],
}

HAND["EXT_G5_WS_B3_036"] = {
    "q": "A factory worker can produce 36 toys a day, working 9 hours a day. "
         "If the factory has 56 workers in all, how many toys are produced every hour?",
    "options": ["14", "224", "504", "324"],
    "hints": [
        "Toys per worker, per hour, equals 36 divided by 9, which is 4.",
        "Total per hour equals 4 times 56 workers, which is 224.",
        "Try: 10 toys a day, in 5 hours, is 2 per hour. 3 workers make 6 per hour.",
    ],
    "steps": [
        "Per worker, per hour, equals 36 divided by 9, which is 4.",
        "Total per hour equals 4 times 56, which is 224.",
        "The answer is option B.",
    ],
}
