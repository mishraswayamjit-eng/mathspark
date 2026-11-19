"""Lines written by hand for gr4_angles, keyed "<question id>:<slot>".

Slots: q, o0..o3 (options), h0..h2 (hints), s0.. (steps). Anything not listed here is narrated by
the rules in gr4_angles_rules.py.
"""

HAND = {
    # ── Past papers: the printed questions are in note form, so they are read as full sentences.
    "EXT_G4_FP_2020_025:q": "A man facing north turns 135 degrees left, then 225 degrees right. Which way is he facing?",
    "EXT_G4_FP_2021_016:q": "An angle is 35 degrees. What is the sum of its complementary and supplementary angles?",
    "EXT_G4_FP_2021_029:q": "An angle is 1 5th of its supplementary angle. Find the angle.",
    "EXT_G4_FP_2022_008:q": "The supplementary angle of an obtuse angle is always what?",
    "EXT_G4_FP_2023_008:q": "What is the sum of the complementary and supplementary angles of 48 degrees?",
    "EXT_G4_FP_2024_003:q": "What is the sum of the complementary and supplementary angles of 48 degrees?",
    "EXT_G4_FP_2024_017:q": "What is the angle between the hour hand and the minute hand at 7 20 p m?",
    "EXT_G4_FP_2024_038:q": "A man walking south-west turns clockwise to face north. How many degrees has he turned?",
    "EXT_G4_FP_2025_013:q": "What is the angle between the hour hand and the minute hand at 18 minutes past 5?",
    # The checker reads the maths line "30° ÷ 3" as "30 cubed", so the 3 has to be said as a word.
    "EXT_G4_FP_2024_017:s2": "20 minutes is one third of an hour, so the hour hand has moved one third of a gap past 7. "
                             "30 degrees divided by three equals 10 degrees.",
    "PYQ_2017_Q20:q": "In 300 seconds, the minute hand of a clock moves how many degrees?",
    "PYQ_2019_Q40:q": "When a boy asks a teacher, what is the time now, the teacher replies, the angle between the hour hand "
                      "and the minute hand of my watch makes an angle of 45 degrees now. What time is it now?",

    # ── Newly written questions.
    "G4A_ANGLES_020:s0": "The angle and its complement add up to 90 degrees. Take away the extra 30 degrees and halve. "
                         "90 minus 30, then divided by 2, equals 30.",
}

# ── The hand-written chapter questions (Q_CH18_001 to 025): their hints and steps are in note form.
HAND.update({
    "Q_CH18_001:h0": "Remember the angle types. Acute is less than 90 degrees. Right is exactly 90 degrees. "
                     "Obtuse is between 90 degrees and 180 degrees. Straight is 180 degrees. Reflex is more than 180 degrees.",
    "Q_CH18_001:s0": "Acute means the angle is more than 0 degrees and less than 90 degrees. Right means the angle is 90 degrees. "
                     "Obtuse means the angle is more than 90 degrees and less than 180 degrees.",
    "Q_CH18_001:s1": "The answer is an obtuse angle.",
    "Q_CH18_002:s0": "180 degrees is less than 250 degrees, which is less than 360 degrees.",
    "Q_CH18_003:h1": "Dividers measure distance. Set squares draw specific angles, 45 degrees or 60 degrees. A compass draws circles.",
    "Q_CH18_003:s1": "The answer is a protractor.",
    "Q_CH18_004:h1": "The complement is 90 degrees minus 67 and a half degrees.",
    "Q_CH18_004:h2": "90 degrees minus 67.5 degrees equals 22.5 degrees, which is 22 and a half degrees.",
    "Q_CH18_004:s1": "The complement is 90 degrees minus 67 and a half degrees, which is 22 and a half degrees.",
    "Q_CH18_004:s2": "The answer is 22 and a half degrees.",
    "Q_CH18_005:h1": "The supplement is 180 degrees minus 55 degrees.",
    "Q_CH18_005:s1": "The supplement is 180 degrees minus 55 degrees, which is 125 degrees.",
    "Q_CH18_006:h2": "The supplement is 180 degrees minus 55 degrees, which is 125 degrees.",
    "Q_CH18_006:s0": "Find x. x equals 90 degrees minus 35 degrees, which is 55 degrees.",
    "Q_CH18_006:s1": "The supplement of x is 180 degrees minus 55 degrees, which is 125 degrees.",
    "Q_CH18_007:h0": "First find the angle. The angle is 180 degrees minus 125 degrees, which is 55 degrees.",
    "Q_CH18_007:h2": "The complement is 35 degrees.",
    "Q_CH18_007:s1": "Find the complement: 90 degrees minus 55 degrees equals 35 degrees.",
    "Q_CH18_007:s2": "The complement is 35 degrees.",
    "Q_CH18_008:h1": "Opposite angles are equal. There are 2 pairs: one pair of equal angles, and another pair of equal angles.",
    "Q_CH18_008:s2": "The answer is 2 pairs.",
    "Q_CH18_009:h1": "Equal! The angle opposite to 70 degrees is also 70 degrees.",
    "Q_CH18_009:s1": "The angle opposite to 70 degrees is 70 degrees.",
    "Q_CH18_010:h0": "A linear pair of angles adds up to 180 degrees. They form a straight line together.",
    "Q_CH18_010:h1": "The other angle is 180 degrees minus 65 degrees.",
    "Q_CH18_010:s0": "In a linear pair, the sum is 180 degrees. 65 degrees plus what equals 180 degrees?",
    "Q_CH18_010:s1": "The other angle is 180 degrees minus 65 degrees, which is 115 degrees.",
    "Q_CH18_011:h1": "The clock face is a circle, 360 degrees, divided into 12 hours. "
                     "Each hour is 360 degrees divided by 12, which is 30 degrees.",
    "Q_CH18_011:h2": "From 12 to 3 is 3 spaces, times 30 degrees, which is 90 degrees.",
    "Q_CH18_011:s0": "Each hour mark is 360 degrees divided by 12, which is 30 degrees.",
    "Q_CH18_011:s1": "At 3 o'clock, 3 spaces times 30 degrees equals 90 degrees.",
    "Q_CH18_011:s2": "The angle is 90 degrees, a right angle!",
    "Q_CH18_012:h0": "At 9 30, the minute hand is at 6, pointing down. Where is the hour hand?",
    "Q_CH18_012:h1": "At 9 30, the hour hand is between 9 and 10. It's halfway, so at the 9 and a half position.",
    "Q_CH18_012:h2": "From 6 to 9 and a half is 3.5 spaces, times 30 degrees, which is 105 degrees.",
    "Q_CH18_012:s0": "The minute hand is at 6. 30 minutes is the 6 o'clock position.",
    "Q_CH18_012:s1": "The hour hand at 9 30 is halfway between 9 and 10, which is the 9.5 position.",
    "Q_CH18_012:s2": "The gap is 9.5 minus 6, which is 3.5 spaces. The angle is 3.5 times 30 degrees, which is 105 degrees.",
    "Q_CH18_013:h1": "At 10:00, 2 spaces make 60 degrees, which is acute. At 4:00, 4 spaces make 120 degrees, which is obtuse! "
                     "At 3 30, it is about 75 degrees, which is acute. At 6:00, 6 spaces make 180 degrees, which is straight.",
    "Q_CH18_013:s0": "At 10:00, from 12 to 10 is 2 spaces, which is 60 degrees. That is acute.",
    "Q_CH18_013:s1": "At 4:00, 4 spaces make 120 degrees. That is obtuse!",
    "Q_CH18_013:s2": "At 3 30, it is about 75 degrees, which is acute. At 6:00, it is 180 degrees, which is straight, not obtuse.",
    "Q_CH18_014:q": "When will the hour hand and the minute hand form a straight angle, 180 degrees?",
    "Q_CH18_014:h1": "At 6:00, the minute hand is at 12 and the hour hand is at 6. They are directly opposite, which is 180 degrees.",
    "Q_CH18_014:h2": "At 3 45, the angle is about 157.5 degrees, not exactly 180 degrees. At 9 15, it's about 172.5 degrees.",
    "Q_CH18_014:s0": "At 6:00, the minute hand is at 12 and the hour hand is at 6. That is 6 spaces, which is 180 degrees.",
    "Q_CH18_014:s1": "At 3 45, the hands are close to opposite, but not exactly 180 degrees.",
    "Q_CH18_016:h1": "60 degrees is 2 spaces on the clock. Which time gives exactly 2 spaces?",
    "Q_CH18_016:h2": "At 2 o'clock, the hands are 2 spaces apart, which is 60 degrees.",
    "Q_CH18_016:s0": "The complement of 30 degrees is 90 degrees minus 30 degrees, which is 60 degrees.",
    "Q_CH18_016:s1": "60 degrees is 2 spaces on the clock, which is 2 o'clock.",
    "Q_CH18_017:h0": "Draw a compass: North is up, East is right, South is down, West is left. North-East is between North and East.",
    "Q_CH18_017:h1": "North to East is 90 degrees. North to North-East is 45 degrees, halfway. "
                     "So North-East is at 45 degrees from North.",
    "Q_CH18_017:h2": "North-East to South: from 45 degrees to 180 degrees is 135 degrees.",
    "Q_CH18_017:s0": "North-East is at 45 degrees from North, clockwise.",
    "Q_CH18_017:s2": "The angle from North-East to South is 180 degrees minus 45 degrees, which is 135 degrees.",
    "Q_CH18_018:h0": "The hour hand goes around the whole clock, 360 degrees, in 12 hours.",
    "Q_CH18_018:h1": "Per hour, that is 360 degrees divided by 12.",
    "Q_CH18_018:h2": "That equals 30 degrees per hour.",
    "Q_CH18_018:s0": "A full rotation is 360 degrees. The time for a full rotation is 12 hours. "
                     "360 degrees divided by 12 equals 30 degrees.",
    "Q_CH18_018:s1": "The hour hand moves 30 degrees per hour.",
    "Q_CH18_019:h0": "The minute hand goes around the whole clock, 360 degrees, in 60 minutes.",
    "Q_CH18_019:h1": "Per minute, that is 360 degrees divided by 60.",
    "Q_CH18_019:h2": "That equals 6 degrees per minute.",
    "Q_CH18_019:s0": "A full rotation is 360 degrees. The time is 60 minutes. 360 degrees divided by 60 equals 6 degrees.",
    "Q_CH18_019:s1": "The minute hand moves 6 degrees per minute.",
    "Q_CH18_020:h0": "Complementary means the sum is 90 degrees. The ratio is 2 is to 3, so the total parts are 2 plus 3, which is 5.",
    "Q_CH18_020:h1": "Each part is 90 degrees divided by 5, which is 18 degrees.",
    "Q_CH18_020:h2": "The smaller angle is 2 times 18 degrees, which is 36 degrees.",
    "Q_CH18_020:s0": "The total is 90 degrees, because they are complementary. The parts are 2 plus 3, which is 5. "
                     "90 degrees divided by 5 equals 18 degrees per part.",
    "Q_CH18_020:s1": "The smaller is 2 times 18 degrees, which is 36 degrees. The larger is 3 times 18 degrees, which is 54 degrees.",
    "Q_CH18_021:h0": "Let the angles be x, and x plus 40 degrees. They're supplementary, so x, plus x plus 40 degrees, equals 180 degrees.",
    "Q_CH18_021:h2": "The larger is 70 degrees plus 40 degrees, which is 110 degrees.",
    "Q_CH18_021:s0": "Let the smaller be x, and the larger be x plus 40 degrees. So x, plus x plus 40 degrees, equals 180 degrees.",
    "Q_CH18_021:s2": "The larger is 70 degrees plus 40 degrees, which is 110 degrees.",
    "Q_CH18_022:s0": "Angles around a point add up to 360 degrees. 110 degrees plus 85 degrees plus x degrees equals 360 degrees.",
    "Q_CH18_023:s0": "The sum is 180 degrees, a straight line. x plus 2 x plus 3 x equals 180 degrees.",
    "Q_CH18_024:h0": "At 4 30, the minute hand is at 6, pointing down. The hour hand is between 4 and 5. Halfway is 4.5.",
    "Q_CH18_024:h1": "From 4.5 to 6 is 1.5 spaces.",
    "Q_CH18_024:s0": "The minute hand is at 6. The hour hand is at 4.5, halfway between 4 and 5. "
                     "The gap is 6 minus 4.5, which is 1.5 spaces.",
    "Q_CH18_024:s1": "The angle is 1.5 times 30 degrees, which is 45 degrees.",
    "Q_CH18_024:s2": "The angle at 4 30 is 45 degrees.",
    "Q_CH18_025:h0": "Start at North, 0 degrees, and turn 225 degrees clockwise. "
                     "North is 0 degrees, East is 90 degrees, South is 180 degrees, West is 270 degrees.",
    "Q_CH18_025:h1": "225 degrees is between South, at 180 degrees, and West, at 270 degrees. It's 45 degrees past South.",
    "Q_CH18_025:h2": "45 degrees past South, towards West, is South-West.",
    "Q_CH18_025:s0": "On the compass, North is 0 degrees, East is 90 degrees, South is 180 degrees, West is 270 degrees. "
                     "225 degrees is between South and West.",
    "Q_CH18_025:s1": "225 degrees is 180 degrees plus 45 degrees. That is South, plus 45 degrees towards West.",
    "Q_CH18_025:s2": "The direction is South-West.",
})
