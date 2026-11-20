"""Grade 4 angles lessons written for one question each: past exam papers (EXT_G4_FP_...)."""
from g4_gr4_angles_lib import (A, B, FIG, G, L, W, angles, ask, box, clock, compass, lesson, mark, note, ring, strike)

LESSONS = {}

S180 = "Supplementary angles sit side by side on a straight line, and a straight line is a half turn. That is 180 degrees."
C90 = "Complementary angles fit together into a square corner. A square corner is a right angle, and that is 90 degrees."


# ── EXT_G4_FP_2020_025: north, 135° left, then 225° right ────────────────────
LESSONS["EXT_G4_FP_2020_025"] = lesson([
    B("A man faces north. He turns 135 degrees to the left, then 225 degrees to the right. Which way does he face at the end?",
      G("l1", "Facing north: 135° left, then 225° right"),
      compass("f1", "N", [(135, "a"), (225, "c")])),
    B("Here is the key idea. A left turn and a right turn are opposites, so they undo each other. Which of his two turns is bigger?",
      ask=ask("fp20a", "the right turn, 225°", ["the left turn, 135°", "they are the same"],
              "Compare the two numbers. 225 is more than 135, so the right turn is the bigger one.")),
    B("So the left turn cancels part of the right turn. What is left over is 225 take away 135.",
      strike("l1", "135° left", "cancels"), W("l2", "225 − 135 = 90")),
    B("Taking away 125 would leave 100, and 10 more away leaves 90. So all his turning comes to just 90 degrees to the right.",
      W("l2a", "225 − 125 = 100"), W("l2b", "100 − 10 = 90"),
      mark("l2", "= 90", "box"), L("l3", "Left over: 90° to the right")),
    B("90 degrees is a quarter turn. Start facing north and make a quarter turn to the right. Where do you face?",
      compass("f2", "N", [(90, "c")]),
      ask=ask("fp20b", "East", ["West", "South-East", "South-West"],
              "Picture a compass, with north at the top. A quarter turn to the right goes the way clock hands move, and that takes you to east.")),
    B("East. He ends up facing east.",
      A("l4", "He faces East"), ring("l4", "East"), compass("f3", "N", [(90, "c")], end=True)),
    B("The trap is to stop after the first turn. 135 to the left only takes him to south-west, and he still has the big right turn to make."),
    B("So with left and right turns, cancel first. Take the smaller from the bigger, then make the turn that is left."),
])


# ── Sum of the complement and the supplement (4 past-paper questions) ────────
def comp_supp_sum(qid, n, given, v):
    comp, supp = 90 - n, 180 - n
    total = comp + supp
    tens, ones = n - n % 10, n % 10
    ct, st = comp - comp % 10, supp - supp % 10
    opening = [
        "Our angle is %d degrees. It has two partners, its complement and its supplement. We find both, then add them together.",
        "Start with %d degrees. We need its complementary angle and its supplementary angle, and then the sum of those two.",
        "Here is %d degrees. The question wants two other angles, the complement and the supplement, added together.",
        "The angle measures %d degrees. We have two jobs: find its complementary angle and its supplementary angle. Then we add them.",
    ][v] % n
    closing = [
        "Two partners, two take aways, one addition. Complement from 90, supplement from 180, then add.",
        "So the plan is: take the angle from 90, take the angle from 180, and add the two answers.",
        "Remember the two totals. 90 for complementary, 180 for supplementary. Find each partner, then add.",
        "C for complementary, C for corner: 90. S for supplementary, S for straight line: 180. Find both partners, then add them.",
    ][v]
    return lesson([
        B(opening, G("l1", given), angles("f1", "single", [("%d°" % n, n)])),
        B("First the complement. Complementary angles fit together into a square corner. How much do they make together?",
          ask=ask(qid + "a", "90°", ["180°", "360°"],
                  "A square corner is a right angle, a quarter turn. That is 90 degrees. 180 is for a straight line.")),
        B("So the complement is 90 take away %d. 90 take away %d is %d, and %d more away leaves %d." % (n, tens, 90 - tens, ones, comp),
          W("l2a", "90 − %d = %d" % (tens, 90 - tens)),
          W("l2", "90 − %d = %d" % (n, comp)), note("l2", "= %d" % comp, "complement"),
          angles("f2", "inRightAngle", [("%d°" % n, n), ("%d°" % comp, comp)], highlight=["p1"])),
        B("Now the supplement. Supplementary angles sit together on a straight line, and a straight line is 180 degrees. Which sum gives the supplement?",
          ask=ask(qid + "b", "180 − %d" % n, ["90 − %d" % n, "180 + %d" % n],
                  "The two angles on the line make 180 together. So take %d away from 180." % n)),
        B("180 take away %d. Here is a quick way: 180 is 90 more than 90, so the supplement is 90 more than the complement. %d and 90 make %d." % (n, comp, supp),
          W("l3", "180 − %d = %d" % (n, supp)), note("l3", "= %d" % supp, "supplement"),
          angles("f3", "onLine", [("%d°" % n, n), ("%d°" % supp, supp)], highlight=["p1"])),
        B("Careful now. The question wants the sum of the two partners. Not the angle itself. Just the complement and the supplement.",
          ring("l2", "= %d" % comp), ring("l3", "= %d" % supp)),
        B("%d plus %d. The tens first: %d and %d make %d. Then the ones: %d and %d make %d. Altogether, %d."
          % (comp, supp, ct, st, ct + st, comp % 10, supp % 10, comp % 10 + supp % 10, total),
          W("l4a", "%d + %d = %d" % (ct, st, ct + st)), W("l4", "%d + %d = %d" % (comp, supp, total))),
        B("So the sum is %d degrees." % total, A("l5", "Sum = %d°" % total), ring("l5", "%d°" % total)),
        B(closing),
    ])


LESSONS["EXT_G4_FP_2021_016"] = comp_supp_sum("EXT_G4_FP_2021_016", 35, "Angle = 35°. Complement + supplement = ?", 0)
LESSONS["EXT_G4_FP_2023_008"] = comp_supp_sum("EXT_G4_FP_2023_008", 48, "Complement + supplement of 48° = ?", 1)
LESSONS["EXT_G4_FP_2024_003"] = comp_supp_sum("EXT_G4_FP_2024_003", 48, "Angle 48°: complement + supplement = ?", 2)
LESSONS["PYQ_2018_Q29"] = comp_supp_sum("PYQ_2018_Q29", 35, "Angle 35°. Complementary + supplementary = ?", 3)


# ── EXT_G4_FP_2021_029: angle is one fifth of its supplement ─────────────────
LESSONS["EXT_G4_FP_2021_029"] = lesson([
    B("An angle is one fifth of its supplement. We have to find the angle.",
      G("l1", "Angle = 1/5 of its supplement. Angle = ?")),
    B("First, what do an angle and its supplement make together?",
      ask=ask("fp21a", "180°", ["90°", "360°"], S180)),
    B("Now think in equal parts. If the angle is 1 part, its supplement is 5 of those parts, because the angle is one fifth of it. Here is the picture.",
      L("l2", "Angle = 1 part, supplement = 5 parts"),
      FIG("f1", kind="barModel", bars=[
          {"label": "Angle", "segments": [{"units": 1, "label": "1 part", "tone": "a"}]},
          {"label": "Supplement", "segments": [{"units": 1, "tone": "b"}] * 5, "brace": "5 parts"}])),
    B("How many equal parts make the whole 180 degrees?",
      ask=ask("fp21b", "6 parts", ["5 parts", "4 parts"],
              "Count both bars. 1 part for the angle and 5 parts for the supplement. Together that is 6 parts. The trap is to count only the 5.")),
    B("1 and 5 make 6 parts. Those 6 equal parts share 180 degrees.",
      W("l3", "1 + 5 = 6"), L("l4", "6 parts = 180°"), box("l4", "6 parts")),
    B("So one part is 180 divided by 6. 6 times 30 is 180, so one part is 30.",
      W("l5", "180 ÷ 6 = 30")),
    B("The angle is 1 part. So the angle is 30 degrees.",
      A("l6", "Angle = 30°"), ring("l6", "30°")),
    B("Let's check. The supplement is 180 take away 30, which is 150. And one fifth of 150 is 30. It works.",
      W("l7", "180 − 30 = 150"), W("l8", "150 ÷ 5 = 30")),
    B("So when one angle is a fraction of the other, count all the parts, share out the total, and check."),
])


# ── EXT_G4_FP_2022_008: supplement of an obtuse angle ────────────────────────
LESSONS["EXT_G4_FP_2022_008"] = lesson([
    B("Take any obtuse angle and find its supplement. The question says the supplement is always the same kind of angle. Which kind?",
      G("l1", "Supplement of an obtuse angle is always ...?")),
    B("First, how big is an obtuse angle?",
      ask=ask("fp22a", "more than 90°, less than 180°", ["less than 90°", "exactly 90°"],
              "Obtuse means wide open. It is bigger than a right angle, 90 degrees, but smaller than a straight line, 180 degrees.")),
    B("Let's try one. 110 degrees is obtuse. Its supplement is what is left of the straight line: 180 take away 110, which is 70.",
      L("l2", "Try 110° (obtuse)"), W("l3", "180 − 110 = 70"),
      angles("f1", "onLine", [("110°", 110), ("70°", 70)], highlight=["p1"])),
    B("70 is less than 90. What do we call an angle that is smaller than a right angle?",
      W("l4", "70 < 90"),
      ask=ask("fp22b", "an acute angle", ["an obtuse angle", "a right angle"],
              "Small, sharp angles, less than 90 degrees, are called acute.")),
    B("Acute. But does it always happen? Try a very wide one, 170 degrees. 180 take away 170 leaves only 10. Acute again.",
      L("l5", "Try 170° (obtuse)"), W("l6", "180 − 170 = 10")),
    B("Here is why. The straight line is 180, which is two lots of 90. The obtuse angle takes more than 90 of it. So what is left must be less than 90.",
      W("l7", "90 + 90 = 180")),
    B("So the supplement of an obtuse angle is always an acute angle.",
      A("l8", "Always an Acute Angle"), ring("l8", "Acute Angle")),
    B("On a straight line, the two partners balance. If one is wider than a square corner, the other must be narrower."),
])


# ── EXT_G4_FP_2024_017: the hands at 7:20 ────────────────────────────────────
LESSONS["EXT_G4_FP_2024_017"] = lesson([
    B("What is the angle between the two hands of a clock at 20 past 7? Here is the clock.",
      G("l1", "Angle between the hands at 7:20 = ?"), clock("f1", 7, 20)),
    B("A clock has 12 numbers, so the full turn of 360 degrees is cut into 12 equal gaps. Each gap is 360 divided by 12, which is 30 degrees.",
      W("l2", "360 ÷ 12 = 30"), L("l3", "1 gap = 30°"), box("l3", "30°")),
    B("At 20 minutes past, the minute hand points at the 4. Count the gaps from the 4 to the 7.",
      ask=ask("fp24a", "3 gaps", ["4 gaps", "2 gaps"],
              "Count the jumps: 4 to 5, 5 to 6, 6 to 7. That is 3 gaps.")),
    B("3 gaps of 30 make 90 degrees. That takes us from the 4 up to the 7.",
      W("l4", "3 × 30 = 90")),
    B("Here is the trap. At 7:20 the hour hand is not on the 7 any more. It has been creeping towards the 8 for 20 minutes. How far has it gone?",
      ask=ask("fp24b", "one third of a gap", ["half a gap", "it has not moved"],
              "20 minutes is one third of an hour. So the hour hand has gone one third of the way from the 7 to the 8.")),
    B("One third of a gap is 30 divided by 3, which is 10 degrees.",
      W("l5", "30 ÷ 3 = 10"), note("l5", "= 10", "hour hand past 7")),
    B("So the angle is the 90, plus the extra 10. That makes 100 degrees.",
      W("l6", "90 + 10 = 100"), A("l7", "Angle = 100°"), ring("l7", "100°")),
    B("So count the gaps, 30 degrees each, then add the bit the hour hand has crept on. It never waits on its number."),
])


# ── EXT_G4_FP_2024_038: south-west, clockwise to north ───────────────────────
LESSONS["EXT_G4_FP_2024_038"] = lesson([
    B("A man is walking south-west. He turns clockwise until he faces north. How many degrees does he turn?",
      G("l1", "South-west, turns clockwise to north. Degrees = ?"), compass("f1", "SW")),
    B("A compass has 8 directions, and they share a full turn of 360 degrees. So each step to the next direction is 360 divided by 8, which is 45 degrees.",
      W("l2", "360 ÷ 8 = 45"), L("l3", "1 step = 45°"), box("l3", "45°")),
    B("Now go clockwise from south-west, the way clock hands move. How many steps is it to north?",
      ask=ask("fp38a", "3 steps", ["2 steps", "5 steps"],
              "Clockwise from south-west we pass west, then north-west, then we reach north. That is 3 steps. 5 steps is the other way round.")),
    B("West, north-west, north. 3 steps.",
      L("l4", "SW → W → NW → N: 3 steps"), compass("f2", "SW", [(135, "c")], end=True)),
    B("3 steps of 45. 2 of them make 90, and 45 more makes 135.",
      W("l5", "45 + 45 = 90"), W("l6", "3 × 45 = 135")),
    B("So he turned 135 degrees. Now look at the choices. Is 135 there?",
      L("l7", "Choices: 90, 225°, 180°, None of these"),
      ask=ask("fp38b", "No, so it is None of these", ["Yes, it is 225°", "Yes, it is 90"],
              "Read the choices again. 90, 225 and 180 are there, but 135 is not. When our answer is not listed, we pick None of these.")),
    B("135 is not on the list. So the answer is None of these.",
      A("l8", "135° is not listed: None of these"), ring("l8", "None of these")),
    B("225 is the trap. It is the turn the other way round, anticlockwise. Trust your working, even when the answer is None of these."),
])


# ── EXT_G4_FP_2025_013: the hands at 18 minutes past 5 ───────────────────────
LESSONS["EXT_G4_FP_2025_013"] = lesson([
    B("What is the angle between the hands at 18 minutes past 5? The hands do not land neatly on the numbers, so we measure how far each hand has turned from the top of the clock.",
      G("l1", "Angle between the hands at 18 minutes past 5 = ?"), clock("f1", 5, 18)),
    B("The minute hand goes all the way round, 360 degrees, in 60 minutes. So each minute it turns 360 divided by 60, which is 6 degrees.",
      W("l2", "360 ÷ 60 = 6")),
    B("In 18 minutes it turns 18 times 6. 10 sixes are 60 and 8 sixes are 48, so that is 108 degrees.",
      W("l3", "60 + 48 = 108"), W("l4", "18 × 6 = 108"), note("l4", "= 108", "minute hand")),
    B("Now the hour hand. From one number to the next is 30 degrees. At 5 o'clock exactly, how far round from the 12 is it?",
      W("l5", "360 ÷ 12 = 30"),
      ask=ask("fp25a", "150°", ["5°", "30°"],
              "From the 12 to the 5 is 5 gaps, and each gap is 30 degrees. 5 times 30 is 150.")),
    B("5 times 30 is 150. But here is the trap. In 18 minutes the hour hand has crept on, past the 5.",
      W("l6", "5 × 30 = 150")),
    B("The hour hand takes 60 minutes to cross one gap of 30 degrees. So it moves 1 degree every 2 minutes. In 18 minutes, that is 9 degrees.",
      W("l7", "18 ÷ 2 = 9")),
    B("So the hour hand is at 150 and 9 more, which is 159 degrees.",
      W("l8", "150 + 9 = 159"), note("l8", "= 159", "hour hand")),
    B("The angle between the hands is the gap between those two. 159 take away 108 leaves 51.",
      W("l9", "159 − 108 = 51")),
    B("So the angle is 51 degrees.", A("l10", "Angle = 51°"), ring("l10", "51°")),
    B("Measure both hands from the 12, then subtract. And don't forget the hour hand's little creep: 1 degree for every 2 minutes."),
])


# ── EXT_G4_FP_2025_031: which pair is supplementary (with halves) ────────────
LESSONS["EXT_G4_FP_2025_031"] = lesson([
    B("We have 4 pairs of angles, and only one pair is supplementary. We have to test them.",
      G("l1", "Which pair of angles is supplementary?")),
    B("What must a supplementary pair add up to?",
      ask=ask("fp31a", "180°", ["90°", "360°"], S180)),
    B("So we add each pair and look for exactly 180. First pair: 62 and 128. The 2 and the 8 make 10, and 60 and 120 make 180. That is 190. Too much.",
      W("l2a", "60 + 120 = 180"), W("l2", "62 + 128 = 190"), note("l2", "= 190", "too big")),
    B("Second pair: 73 and a half, and 107 and a half. The whole numbers, 73 and 107, make 180. Then the two halves make 1 more. 181. So close!",
      W("l3", "73 + 107 = 180"), W("l4", "73.5 + 107.5 = 181"), note("l4", "= 181", "1 too many")),
    B("Third pair: 85 and a half, and 93 and a half. 85 and 93 make 178, and the two halves make 1 more. 179. Just short.",
      W("l5", "85 + 93 = 178"), W("l6", "85.5 + 93.5 = 179"), note("l6", "= 179", "1 short")),
    B("Last pair: 140 and a half, and 39 and a half. The whole numbers, 140 and 39, make 179. What happens when we add the two halves?",
      W("l7", "140 + 39 = 179"),
      ask=ask("fp31b", "we get exactly 180", ["we stay at 179", "we get 181"],
              "Two halves make 1 whole. So we add 1 more to 179, and that makes 180.")),
    B("179, and 1 more from the two halves. Exactly 180.",
      W("l8", "140.5 + 39.5 = 180"), box("l8", "= 180")),
    B("So the supplementary pair is 140 and a half degrees, and 39 and a half degrees.",
      A("l9", "Supplementary pair: 140.5° & 39.5°"), ring("l9", "140.5° & 39.5°")),
    B("Did you see how close the others were? 181 and 179. Near enough is not good enough. Supplementary means exactly 180."),
])
