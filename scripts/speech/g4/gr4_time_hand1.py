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
    # The clock face in this question is printed in Roman numerals; they are said as number words.
    "PYQ_2017_Q23": {
        "hints": {
            1: "Work out how many 5-minute steps make 50 minutes. Then count the steps for each choice, going forward past twelve where you need to.",
            2: "Here is a similar one. How long does the minute hand take to go from eight to two? Going forward, it passes nine, ten, eleven, twelve, one and two, which is 6 steps. 6 times 5 equals 30, so it takes 30 minutes.",
        },
        "steps": {
            1: "From nine forward to three, the hand passes 12 and moves 6 steps, which is 30 minutes. From ten to six is 8 steps and from four to twelve is 8 steps, which is 40 minutes each.",
            2: "From six, the hand moves 6 steps up to twelve and then 4 more steps on to four. That is 10 steps.",
        },
    },
}

LINES = {}
