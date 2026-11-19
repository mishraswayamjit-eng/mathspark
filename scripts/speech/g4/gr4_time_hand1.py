"""Hand-written narration for gr4_time. HAND[question id][part] is text, or {index: text} for lists."""

HAND = {
    "EXT_G4_FP_2020_009": {"q": "The 17th of a month is a Saturday. What day was the first day of the month?"},
    "EXT_G4_FP_2020_033": {"q": "At half past six, what is the angle between the hour hand and the minute hand?"},
    "EXT_G4_FP_2021_011": {"q": "In 300 seconds, the minute hand moves how many degrees?"},
    "EXT_G4_FP_2021_015": {"q": "1st January 2006 was a Sunday. What day was 1st January 2010?"},
    "EXT_G4_FP_2021_022": {"q": "Teacher: the angle between the hands is 45 degrees. What is the time?"},
    "EXT_G4_FP_2022_010": {"q": "How many weeks are there in 8 times 7 times 6 times 5 times 4 times 3 times 2 times 1 minutes?"},
    "EXT_G4_FP_2022_026": {"q": "It is 4 30 p m on April 15th. The minute hand turns 30 times. What are the date and time then?"},
    "EXT_G4_FP_2023_002": {"q": "What is the time 2023 minutes after 12:00 a m on 2nd March 2023?"},
    "EXT_G4_FP_2023_034": {"q": "What is the angle between the hour hand and the minute hand at 8 30 a m?"},
    "EXT_G4_FP_2023_038": {"q": "Republic Day 2023 was on a Thursday. In which year will it be on a Tuesday?"},
    "EXT_G4_FP_2024_025": {"q": "It is 10 30 a m on 21st April 2024. The minute hand turns 42 times. What are the date and time then?"},
    "EXT_G4_FP_2024_036": {"q": "Independence Day 2024 was on a Thursday. In which year will it be on a Wednesday?"},
    "EXT_G4_FP_2025_029": {"q": "A bus leaves Pune for Mumbai every 36 minutes, starting from 7 a m. You arrive at 8 50 a m. When is the next bus?"},
    "PYQ_2018_Q14": {"q": "A watch falls slow by 30 seconds in every hour. It is set to correct time at 8:00 a m. What time would this watch show at 10 p m the same day?"},
    "Q_CH17_001": {
        "steps": {
            0: "Rule: divisible by 4 means a leap year. But century years must be divisible by 400.",
            1: "2024 divided by 4 equals 506. 2100 divided by 400 is not a whole number. 1900 divided by 400 is not a whole number.",
        },
    },
    "Q_CH17_003": {"hints": {2: "1 extra day means the day advances by 1: from Sunday to Monday."}},
    "Q_CH17_005": {"steps": {0: "Count from 26 January 1993 to 26 January 1997: 4 years."}},
    "Q_CH17_007": {"hints": {0: "1992 is a leap year! From 14 February 1992 to 14 February 1993 is 366 days, because it crosses 29 February 1992."}},
    "Q_CH17_012": {
        "steps": {
            0: "Hours: 5 minus 2 equals 3 hours. Minutes: 10 minus 40 equals minus 30, which is negative!",
            1: "Borrow 1 hour: 2 hours, and 60 plus 10, minus 40, equals 2 hours 30 minutes.",
        },
    },
    "Q_CH17_013": {"steps": {0: "For p m, add 12 to the hour. 3 plus 12 equals 15."}},
    "Q_CH17_014": {
        "hints": {
            0: "In 100 years: 76 normal years, giving 76 odd days, plus 24 leap years, giving 48 odd days, equals 124 odd days. But wait, the century year might not be leap.",
            1: "100 years equals 5 odd days, after careful calculation. 400 years equals 4 times 5, plus 1 for the extra leap day from the 400th year, which is 20 plus 1, which is 21. 21 divided by 7 equals 3 weeks, which is 0 odd days.",
        },
    },
    "Q_CH17_015": {
        "hints": {2: "If 1 May is Saturday, then 2 May is Sunday, the 1st Sunday. 9 May is Sunday, the 2nd Sunday."},
        "steps": {2: "Sundays in May: 2nd, 9th, 16th, and so on. The 2nd Sunday is 9th May."},
    },
    "Q_CH17_017": {"hints": {0: "Count days from 1 January to 25 December. That's 358 days. 365 minus 7 equals 358. Let's count properly."}},
    "Q_CH17_018": {"steps": {0: "April has 30 days, which is 4 weeks plus 2 days. Two days occur 5 times."}},
    "Q_CH17_025": {
        "hints": {
            0: "We need to go backwards 1 day, from Monday to Sunday, which means we need total odd days equal to 6, or 7 minus 1.",
            1: "Odd days: 2000 has 2, a leap year. 2001 has 1. 2002 has 1. 2003 has 1. 2004 has 2, a leap year. After 2000: 2 odd days, so Wednesday. After 2001: plus 1 makes 3, so Thursday. After 2002: plus 1 makes 4, so Friday. After 2003: plus 1 makes 5, so Saturday. After 2004: plus 2 makes 7, which is 0, so Monday again. Hmm.",
            2: "Wait: from 2000 to 2001, 2 October falls after February, so the leap year effect depends on position. 2000: advance 1, because October is after February, so there is only 1 odd day from October to October in a year where the leap day is before. Monday plus 1 is Tuesday, in 2001. Plus 1 is Wednesday, in 2002. Plus 1 is Thursday, in 2003. Plus 2 is Saturday, in 2004, a leap year crossed. Plus 1 is Sunday, in 2005.",
        },
        "steps": {1: "Year by year: 2001 is Tuesday, 2002 is Wednesday, 2003 is Thursday, 2004 is Saturday, because the leap year adds 2, and 2005 is Sunday."},
    },
}

LINES = {}
