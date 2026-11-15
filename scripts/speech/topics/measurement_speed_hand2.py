"""Hand-written narration: past-paper questions 2020 to 2022 of the measurement-speed topic."""
from measurement_speed_hand1 import KMH_TO_MS, MS_TO_KMH

DST = "Distance equals speed times time."
M_KM = "1000 metres equals 1 kilometre."

HAND = {}

HAND["EXT_G5_FP_2020_020"] = {
    "q": "An ant moves 15 feet per minute. How many feet does it travel in 24 minutes and 40 seconds?",
    "options": ["360 feet", "370 feet", "385 feet", "365 feet"],
    "hints": [
        "Split the time: 24 minutes, and 40 seconds. In 40 seconds, the ant covers two thirds of a minute's distance.",
        DST,
        "",
    ],
    "steps": [
        "24 minutes: 24 times 15 equals 360 feet.",
        "40 seconds equals two thirds of a minute. So, two thirds times 15 equals 10 feet.",
        "Total equals 360 plus 10, which is 370 feet.",
    ],
}

HAND["EXT_G5_FP_2020_040"] = {
    "q": "An insect flies at the rate of 10 metres per second. What is its speed in kilometres per hour?",
    "options": ["18 kilometres per hour", "60 kilometres per hour", "36 kilometres per hour", "24 kilometres per hour"],
    "hints": [
        "To change metres per second into kilometres per hour, multiply by 18 divided by 5, or 3.6.",
        MS_TO_KMH,
        "",
    ],
    "steps": [
        "10 times 18, divided by 5, equals 10 times 3.6, which is 36 kilometres per hour.",
        "Check: in 1 hour, which equals 3600 seconds, it flies 36,000 metres, which equals 36 kilometres.",
    ],
}

HAND["EXT_G5_FP_2021_033"] = {
    "q": "An aeroplane departs from Mumbai at 6 20 p m, and reaches Dubai at 8 50 p m. "
         "If the speed of the aeroplane is 212.5 metres per second, find the distance between Mumbai and Dubai.",
    "options": ["1912.5 kilometres", "1812.5 kilometres", "1952.5 kilometres", "1932.5 kilometres"],
    "hints": [
        "Find the flying time and change it to seconds, because the speed is in metres per second. "
        "Then change metres into kilometres.",
        DST + " " + M_KM,
        "",
    ],
    "steps": [
        "From 6 20 p m, to 8 50 p m, is 2 hours 30 minutes, which equals 9000 seconds.",
        "Distance equals 212.5 times 9000, which is 1,912,500 metres.",
        "That equals 1912.5 kilometres.",
    ],
}

HAND["EXT_G5_FP_2022_012"] = {
    "q": "A train 120 metres long, running with a speed of 36 kilometres per hour, will pass a pole in blank seconds.",
    "options": ["15", "12", "10", "20"],
    "hints": [
        "Change 36 kilometres per hour to metres per second, by multiplying by 5 over 18. "
        "Passing a pole means covering its own length.",
        "Time equals length divided by speed. " + KMH_TO_MS,
        "",
    ],
    "steps": [
        "36 kilometres per hour equals 36 times 5, divided by 18, which is 10 metres per second.",
        "Time equals 120 divided by 10, which is 12 seconds.",
    ],
}

HAND["EXT_G5_FP_2022_030"] = {
    "q": "A car travels 600 metres in 25 seconds. How much distance will the car cover in 1 hour?",
    "options": ["84.6 kilometres", "80 kilometres", "85.4 kilometres", "None of these"],
    "hints": [
        "Find the speed in metres per second. In 1 hour there are 3600 seconds. Then change metres to kilometres.",
        DST + " " + M_KM,
        "",
    ],
    "steps": [
        "Speed equals 600 divided by 25, which is 24 metres per second.",
        "In 1 hour: 24 times 3600 equals 86,400 metres, which is 86.4 kilometres.",
        "86.4 is not among options A to C. So, none of these.",
    ],
}
