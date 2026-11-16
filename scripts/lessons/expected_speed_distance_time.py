# -*- coding: utf-8 -*-
"""Expected computations for the 'speed-distance-time' lesson quiz.

See expected_addition_subtraction.py for the format. Unit changes are worked
from first principles here (1 km = 1000 m, 1 hour = 60 minutes = 3600 seconds)
and not with the 5/18 shortcut the lesson teaches, so the two can disagree if
either is off.
"""

EXPECT = {
    # Level 1: speed = distance / time
    "sd-l1-q1": "150 / 3",
    "sd-l1-q2": "100 / 20",
    "sd-l1-q3": "480 / 6",
    "sd-l1-q4": "max(45 / 3, 26 / 2)",
    "sd-l1-q5": "702 / 9",
    "sd-l1-q6": "16500 / 125",
    "sd-l1-q7": "84 / 7",
    "sd-l1-q8": "2550 / 3",
    # Level 2: distance and time
    "sd-l2-q1": "45 * 4",
    "sd-l2-q2": "280 / 70",
    "sd-l2-q3": ("40 * 30 / 60", "60"),
    "sd-l2-q4": ("2 / 6 * 60", "60"),
    "sd-l2-q5": "50 * 3",
    "sd-l2-q6": ("15 * (24 + 40 / 60)", "60"),
    "sd-l2-q7": ("30 / 90 * 60", "60"),
    "sd-l2-q8": ("900 / 18 * 60 / 1000", "60 1000"),
    # Level 3: changing units
    "sd-l3-q1": ("7 * 1000", "1000"),
    "sd-l3-q2": ("36 * 1000 / 3600", "1000 3600"),
    "sd-l3-q3": ("90 * 1000 / 3600", "1000 3600"),
    "sd-l3-q4": ("15 * 3600 / 1000", "3600 1000"),
    "sd-l3-q5": ("30 * 3600 / 1000", "3600 1000"),
    "sd-l3-q6": ("10 * 3600 / 1000", "3600 1000"),
    "sd-l3-q7": ("12 * 1000 / 60 * 4", "1000 60"),
    "sd-l3-q8": ("500 / 25 * 3600 / 1000", "3600 1000"),
    # Level 4: a train passing a pole covers its own length
    "sd-l4-q1": "180 / 20",
    "sd-l4-q2": "240 / 12",
    "sd-l4-q3": "25 * 8",
    "sd-l4-q4": ("100 / (36 * 1000 / 3600)", "1000 3600"),
    "sd-l4-q5": ("300 / (72 * 1000 / 3600)", "1000 3600"),
    "sd-l4-q6": ("250 / 10 * 3600 / 1000", "3600 1000"),
    "sd-l4-q7": ("54 * 1000 / 3600 * 20", "1000 3600"),
    "sd-l4-q8": ("200 / 9 * 3600 / 1000", "3600 1000"),
    # Level 5: journeys with a twist
    "sd-l5-q1": ("(5 * 60 + 45) - (2 * 60 + 15)", "60"),
    "sd-l5-q2": "2.5 * 60",
    "sd-l5-q3": "200 / 5 + 300 / 6",
    "sd-l5-q4": "240 / (240 / 4 - 20)",
    # speed in km/h x time in hours (6:45 pm to 9:15 pm)
    "sd-l5-q5": ("(30 * 3600 / 1000) * ((9 * 60 + 15) - (6 * 60 + 45)) / 60", "3600 1000 60"),
    "sd-l5-q6": ("680 / (680 / 8 - 17) * 60", "60"),
    # one walk = 55 / 2; one ride = 37 - that; both rides = double
    "sd-l5-q7": ("(37 - 55 / 2) * 2", "2"),
    "sd-l5-q8": "5 * (100 / 4 + 300 / 5)",
}

# Sentences whose claim is not written as a sum. Each carries its own proof.
ALLOW = {
    # 6:45 pm to 9:15 pm is 150 minutes, which is 2.5 hours
    "The journey takes 2 hours 30 minutes, which is 2.5 hours.":
        ["(9 * 60 + 15) - (6 * 60 + 45) == 2 * 60 + 30", "(2 * 60 + 30) / 60 == 2.5"],
    "From 6:45 to 8:45 is 2 hours. From 8:45 to 9:15 is 30 minutes.":
        ["(8 * 60 + 45) - (6 * 60 + 45) == 2 * 60", "(9 * 60 + 15) - (8 * 60 + 45) == 30"],
    "18 km/h means 18,000 m in 3,600 seconds.":
        ["18 * 1000 == 18000", "60 * 60 == 3600"],
    "5 m/s is the same as 18 km/h.":
        ["5 * 3600 / 1000 == 18"],
    "72 km/h means 72 km in 60 minutes. 72 ÷ 18 = 4, so 18 km is a quarter of 72 km.":
        ["18 * 4 == 72"],
    "30 minutes is half an hour, and 15 minutes is a quarter of an hour.":
        ["60 / 2 == 30", "60 / 4 == 15"],
    "1 hour = 60 minutes, so 20 minutes is one third of an hour.":
        ["60 / 3 == 20"],
    "6 km/h is 6,000 m in 60 minutes. 6,000 ÷ 60 = 100, so he walks 100 m each minute.":
        ["6 * 1000 == 6000"],
    "2.5 hours is 2 hours and half an hour. 80 × 2 = 160, and half of 80 is 40. 160 + 40 = 200.":
        ["80 / 2 == 40", "2 + 0.5 == 2.5"],
    # hints that state a fraction of an hour or of a distance
    "2 km is one third of 6 km. Take the same part of 60 minutes.":
        ["6 / 3 == 2"],
    "30 km is one third of 90 km. Take one third of 60 minutes.":
        ["90 / 3 == 30"],
    "Find the distance for 24 minutes. Then 40 seconds is two thirds of a minute.":
        ["60 * 2 / 3 == 40"],
    "90 is five lots of 18.":
        ["5 * 18 == 90"],
    "The speed is 200 ÷ 9 m/s. Multiply 200 by 18 first, then divide by 9 and by 5.":
        ["200 * 18 / 9 / 5 == 200 / 9 * 3600 / 1000"],
}
