"""Hand-written narration: past-paper questions 2016 to 2019 of the measurement-speed topic."""

TDS = "Time equals distance divided by speed."
MS_TO_KMH = "Metres per second to kilometres per hour: multiply by 18 over 5."
KMH_TO_MS = "Kilometres per hour to metres per second: multiply by 5 over 18."

HAND = {}

HAND["EXT_G5_FP_2016_013"] = {
    "q": "Amar walks a certain distance from A to B, and rides back from B to A, taking a total time of 37 minutes. "
         "He could walk both ways, A to B and B to A, in 55 minutes. How long will it take Amar to ride both ways?",
    "options": ["12 minutes", "18 minutes", "19 minutes", "15 minutes"],
    "hints": [
        "Walking both ways takes 55 minutes, so walking one way takes half of that. "
        "Then, ride one way equals 37, minus walk one way.",
        "Walk one way, plus ride one way, equals 37 minutes. Walk one way equals 55 divided by 2.",
        "",
    ],
    "steps": [
        "Walk one way equals 55 divided by 2, which is 27.5 minutes.",
        "Ride one way equals 37 minus 27.5, which is 9.5 minutes.",
        "Ride both ways equals 2 times 9.5, which is 19 minutes.",
    ],
}

HAND["EXT_G5_FP_2017_007"] = {
    "q": "A seagull travelled 16500 miles from Finland to Australia. It travelled at a rate of 125 miles per day. "
         "In how many days did the seagull reach Australia?",
    "options": ["145", "125", "132", "150"],
    "hints": [
        TDS + " Try dividing 16500 by 125, or divide both by 25 first, to make it easier.",
        TDS,
        "",
    ],
    "steps": [
        "Days equals 16500 divided by 125.",
        "Divide both by 25. That gives 660 divided by 5, which equals 132.",
        "The answer is 132 days.",
    ],
}

HAND["EXT_G5_FP_2017_029"] = {
    "q": "A motorcycle is moving at the rate of 30 metres per second. Its speed, in kilometres per hour, is:",
    "options": ["90 kilometres per hour", "60 kilometres per hour", "108 kilometres per hour", "45 kilometres per hour"],
    "hints": [
        "To change metres per second into kilometres per hour, multiply by 18 divided by 5, or by 3.6.",
        MS_TO_KMH,
        "",
    ],
    "steps": [
        "1 kilometre is 1000 metres, and 1 hour is 3600 seconds. So, to change metres per second into "
        "kilometres per hour, multiply by 3600 and divide by 1000, which is the same as multiplying by 18 over 5.",
        "30 times 18 over 5. First, 30 divided by 5 equals 6. Then, 6 times 18 equals 108.",
        "So the speed is 108 kilometres per hour.",
    ],
}

HAND["EXT_G5_FP_2017_038"] = {
    "q": "A train 200 metres long passes a pole in 9 seconds. The speed of the train, in kilometres per hour, is:",
    "options": ["90 kilometres per hour", "60 kilometres per hour", "72 kilometres per hour", "80 kilometres per hour"],
    "hints": [
        "Passing a pole means covering its own length, 200 metres. Find the speed in metres per second, "
        "then change to kilometres per hour, by multiplying by 18 over 5.",
        "Speed equals distance divided by time. " + MS_TO_KMH,
        "",
    ],
    "steps": [
        "Speed equals 200 divided by 9 metres per second, which is 200 over 9 metres per second.",
        "In kilometres per hour: 200 over 9, times 18 over 5. That equals 200 times 2, divided by 5, "
        "which is 400 divided by 5. That equals 80 kilometres per hour.",
    ],
}

HAND["EXT_G5_FP_2018_020"] = {
    "q": "Walking at a speed of 6 kilometres per hour, what distance would he cover in 3 minutes?",
    "options": ["300 metres", "150 metres", "100 metres", "200 metres"],
    "hints": [
        "How many metres does he walk in 1 hour? Then in 1 minute?",
        "6 kilometres per hour is 6000 metres in 60 minutes, which is 100 metres per minute.",
        "",
    ],
    "steps": [
        "6 kilometres equals 6000 metres, in 60 minutes.",
        "In 1 minute: 6000 divided by 60 equals 100 metres.",
        "In 3 minutes: 3 times 100 equals 300 metres.",
    ],
}

HAND["EXT_G5_FP_2018_036"] = {
    "q": "In what time will a train 100 metres long, running at a speed of 36 kilometres per hour, "
         "pass a man standing by the rails?",
    "options": ["100 seconds", "1 minute", "10 seconds", "36 seconds"],
    "hints": [
        "Change 36 kilometres per hour to metres per second, by multiplying by 5 over 18. "
        "The train must travel its own length to pass the man.",
        TDS + " " + KMH_TO_MS,
        "",
    ],
    "steps": [
        "36 kilometres per hour equals 36 times 5, divided by 18, which is 10 metres per second.",
        "Time equals 100 divided by 10, which is 10 seconds.",
    ],
}

HAND["EXT_G5_FP_2019_006"] = {
    "q": "A man walks 900 metres in 18 minutes. How much distance would he cover in an hour?",
    "options": ["2 kilometres", "3 kilometres", "2.5 kilometres", "5 kilometres"],
    "hints": [
        "Find how far he walks in 1 minute. An hour has 60 minutes. Then change metres to kilometres.",
        "Unitary method: distance in 1 minute, times 60. 1000 metres equals 1 kilometre.",
        "",
    ],
    "steps": [
        "In 1 minute: 900 divided by 18 equals 50 metres.",
        "In 60 minutes: 50 times 60 equals 3000 metres.",
        "3000 metres equals 3 kilometres.",
    ],
}

HAND["EXT_G5_FP_2019_023"] = {
    "q": "At a speed of 72 kilometres per hour, a car will cover a distance of 18 kilometres in how much time?",
    "options": ["9 minutes", "15 minutes", "24 minutes", "18 minutes"],
    "hints": [
        TDS + " 18 divided by 72 is a fraction of an hour. Change that into minutes.",
        TDS + " 1 hour equals 60 minutes.",
        "",
    ],
    "steps": [
        "Time equals 18 divided by 72, which is one quarter of an hour.",
        "One quarter, times 60, equals 15 minutes.",
    ],
}
