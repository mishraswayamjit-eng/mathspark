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

# ── The hand-written chapter questions whose hints and steps are still in note form.
HAND.update({
    # The checker reads the maths line "140° ÷ 2" as "140 squared", so the 2 has to be said as a word.
    "Q_CH18_021:s2": "Halve 140 degrees to find the smaller angle. 140 degrees divided by two equals 70 degrees.",
    "Q_CH18_014:q": "When will the hour hand and the minute hand form a straight angle, 180 degrees?",
})
