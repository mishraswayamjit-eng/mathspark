"""Grade 4 angles lessons written for one question each: Q_CH18_001 to Q_CH18_012."""
from g4_gr4_angles_lib import (A, B, G, L, W, angles, ask, box, clock, lesson, mark, note, ring)

LESSONS = {}

S180 = "Supplementary angles sit side by side on a straight line, and a straight line is a half turn. That is 180 degrees."
C90 = "Complementary angles fit together into a square corner. A square corner is a right angle, and that is 90 degrees."
LINE180 = "Two angles side by side on a straight line make a half turn together. A half turn is 180 degrees."


# ── Q_CH18_001: more than 90° but less than 180° ─────────────────────────────
LESSONS["Q_CH18_001"] = lesson([
    B("Here is an angle that is more than 90 degrees but less than 180 degrees. What is it called?",
      G("l1", "More than 90° but less than 180°: called?"), angles("f1", "single", [("?", 130)])),
    B("Angle names go by size. The small ones, less than 90, are acute. Exactly 90, the square corner, is a right angle.",
      L("l2", "Less than 90°: acute"), L("l3", "Exactly 90°: right angle")),
    B("Now jump to the far end. An angle that opens past a straight line, more than 180, is called reflex.",
      L("l4", "More than 180°: reflex")),
    B("Our angle is wider than the square corner, but it has not opened out flat. Which name is left for it?",
      ask=ask("c1a", "obtuse", ["acute", "reflex"],
              "Acute is for angles under 90, and reflex is for angles over 180. The name for the ones in between is obtuse.")),
    B("Obtuse. An angle between 90 and 180 degrees is an obtuse angle.",
      A("l5", "Between 90° and 180°: obtuse"), ring("l5", "obtuse"), angles("f2", "single", [("obtuse", 130)])),
    B("Obtuse means blunt. An acute angle is sharp, like a pencil tip. An obtuse angle is blunt and wide, like a book lying nearly flat."),
    B("So, in order of size: acute, right, obtuse, straight, reflex. Obtuse sits between the square corner and the straight line."),
])


# ── Q_CH18_002: an angle of 250° ─────────────────────────────────────────────
LESSONS["Q_CH18_002"] = lesson([
    B("What kind of angle is 250 degrees? Here it is. It is a big one.",
      G("l1", "An angle measuring 250° is a ...?"), angles("f1", "single", [("250°", 250)])),
    B("To name an angle, we compare it with the fence posts. 90 is a right angle, 180 is a straight line, and 360 is a full turn.",
      L("l2", "90° right     180° straight     360° complete")),
    B("Is 250 more than 180, or less?",
      ask=ask("c2a", "more than 180", ["less than 180"],
              "Look at the hundreds. 180 has 1 hundred and 250 has 2 hundreds. So 250 is the bigger number.")),
    B("More than 180. So the angle has opened past a straight line. It cannot be obtuse, because obtuse stops at 180.",
      W("l3", "250 > 180")),
    B("But 250 is less than 360, so it is not a full turn either. It is not a complete angle.",
      W("l4", "250 < 360")),
    B("Past a straight line, but short of a full turn. What do we call an angle like that?",
      ask=ask("c2b", "a reflex angle", ["a straight angle", "a complete angle"],
              "A straight angle is exactly 180, and a complete angle is exactly 360. Anything in between those two is a reflex angle.")),
    B("So 250 degrees is a reflex angle.",
      A("l5", "250° is a reflex angle"), ring("l5", "reflex angle")),
    B("A reflex angle is the long way round. Whenever the size is between 180 and 360, the angle is reflex."),
])


# ── Q_CH18_003: the instrument that measures an angle ────────────────────────
LESSONS["Q_CH18_003"] = lesson([
    B("Open your geometry box. Which of these tools is used to measure an angle?",
      G("l1", "Which instrument is used to measure an angle?")),
    B("First, what are angles measured in?",
      ask=ask("c3a", "degrees", ["centimetres", "grams"],
              "Centimetres are for lengths and grams are for weights. The size of an angle, how far it opens, is measured in degrees.")),
    B("Degrees. So we need a tool that has degrees marked on it. Let's check each tool's job.",
      L("l2", "Angles are measured in degrees"), mark("l2", "degrees")),
    B("A compass holds a pencil and draws circles. A pair of dividers has two sharp points, for comparing lengths. No degrees on either.",
      L("l3", "Compass: draws circles"), L("l4", "Dividers: compare lengths")),
    B("A set square has a few fixed corners, so it helps to draw some angles. But it cannot measure any angle you like.",
      L("l5", "Set square: a few fixed angles")),
    B("One tool is left. It is a half circle, with degrees marked all round its curved edge, from 0 to 180. What is it called?",
      L("l6", "Half circle marked from 0° to 180°"),
      ask=ask("c3b", "a protractor", ["a compass", "a ruler"],
              "The half circle with the degree marks is the protractor. A ruler measures length, and a compass draws circles.")),
    B("The protractor. That is the tool that measures an angle.",
      A("l7", "A protractor measures angles"), ring("l7", "protractor")),
    B("Each tool has its own job. A ruler for lengths, a compass for circles, and a protractor for angles."),
])


# ── Q_CH18_004: the complementary angle of 67½° ──────────────────────────────
LESSONS["Q_CH18_004"] = lesson([
    B("We want the complementary angle of 67 and a half degrees.",
      G("l1", "Complementary angle of 67½° = ?"),
      angles("f1", "inRightAngle", [("67½°", 67.5), ("?",)])),
    B("What do two complementary angles add up to?",
      ask=ask("c4a", "90°", ["180°", "100°"], C90)),
    B("So we take 67 and a half away from 90. Let's do it in two bites: the whole 67 first, then the half.",
      L("l2", "90 − 67½ = ?"), mark("l2", "67"), mark("l2", "½", "circle")),
    B("90 take away 67. 90 take away 60 is 30, and 7 more away leaves 23.",
      W("l3", "90 − 60 = 30"), W("l4", "30 − 7 = 23")),
    B("The half still has to come off. What is half less than 23?",
      ask=ask("c4b", "22½", ["23½", "22"],
              "We are taking away, so the answer goes just below 23. Half way back from 23 towards 22 is 22 and a half.")),
    B("Half less than 23 is 22 and a half.", L("l5", "23 − ½ = 22½")),
    B("So the complementary angle is 22 and a half degrees.",
      A("l6", "Complementary angle = 22½°"), ring("l6", "22½°"),
      angles("f2", "inRightAngle", [("67½°", 67.5), ("22½°", 22.5)], highlight=["p1"])),
    B("Check. 67 and 22 make 89. The two halves make 1 more. 90 exactly.",
      W("l7", "67 + 22 = 89"), W("l8", "89 + 1 = 90")),
    B("Whole number first, then the half. Both are taken away, so the answer ends up just below 23, not above it."),
])


# ── Q_CH18_005: the supplementary angle of 55° ───────────────────────────────
LESSONS["Q_CH18_005"] = lesson([
    B("We want the supplementary angle of 55 degrees. Here is 55 degrees on a straight line, with its partner beside it.",
      G("l1", "Supplementary angle of 55° = ?"), angles("f1", "onLine", [("55°", 55), ("?",)])),
    B("What do two supplementary angles add up to?",
      ask=ask("c5a", "180°", ["90°", "360°"], S180)),
    B("So 55 and its partner make 180. The partner is 180 take away 55.",
      W("l2", "55 + ? = 180"), ring("l2", "?")),
    B("Take the 50 away first. 180 take away 50 is 130. Then the 5. What is 130 take away 5?",
      W("l3", "180 − 50 = 130"),
      ask=ask("c5b", "125", ["135", "35"],
              "130 take away 5 is 125. It must end up below 130, because we are taking away.")),
    B("125. So 180 take away 55 is 125.",
      W("l4", "130 − 5 = 125"), W("l5", "180 − 55 = 125")),
    B("The supplementary angle is 125 degrees.",
      A("l6", "Supplementary angle = 125°"), ring("l6", "125°"),
      angles("f2", "onLine", [("55°", 55), ("125°", 125)], highlight=["p1"])),
    B("Check: 55 and 125. The two 5s make 10, and 50 and 120 make 170. 170 and 10 is 180.",
      W("l7", "50 + 120 = 170"), W("l8", "55 + 125 = 180")),
    B("The tempting slip is 35. That is 90 take away 55, the complementary angle. S for supplementary, S for straight line: 180.",
      W("l9", "90 − 55 = 35"), note("l9", "= 35", "complementary")),
])


# ── Q_CH18_006: x + 35° = 90°, the supplement of x ───────────────────────────
LESSONS["Q_CH18_006"] = lesson([
    B("This question has two parts. First we find x. Then we find the supplement of x.",
      G("l1", "x + 35° = 90°. Supplement of x = ?"), angles("f1", "inRightAngle", [("x",), ("35°", 35)])),
    B("x and 35 make 90. So x is the missing piece of a square corner. Which sum finds it?",
      ask=ask("c6a", "90 − 35", ["90 + 35", "180 − 35"],
              "90 is the whole and 35 is one part. To find the other part, take 35 away from 90.")),
    B("90 take away 30 is 60, and 5 more away is 55. So x is 55 degrees.",
      W("l2", "90 − 30 = 60"), W("l3", "90 − 35 = 55"), L("l4", "x = 55°")),
    B("Careful. 55 is x, but the question does not stop there. It asks for the supplement of x.",
      box("l4", "x = 55°"), mark("l1", "Supplement of x")),
    B("A supplement is the partner that makes a straight line, 180 degrees. So which sum do we need now?",
      ask=ask("c6b", "180 − 55", ["180 − 35", "90 − 55"],
              "We want the supplement of x, and x is 55. So we take 55 away from 180. 180 take away 35 would be the supplement of the other angle.")),
    B("180 take away 50 is 130, and 5 more away is 125.",
      W("l5", "180 − 50 = 130"), W("l6", "180 − 55 = 125"),
      angles("f2", "onLine", [("55°", 55), ("125°", 125)], highlight=["p1"])),
    B("So the supplement of x is 125 degrees.",
      A("l7", "Supplement of x = 125°"), ring("l7", "125°")),
    B("Check: 55 and 125 make 180. And in a two part question, read the last line again before you choose.",
      W("l8", "55 + 125 = 180")),
])


# ── Q_CH18_007: the supplement is 125°, find the complement ──────────────────
LESSONS["Q_CH18_007"] = lesson([
    B("We are not told the angle. We are told its supplement, 125 degrees. And we are asked for its complement.",
      G("l1", "Supplement of an angle = 125°. Its complement = ?"),
      angles("f1", "onLine", [("angle",), ("125°", 125)])),
    B("So first we must find the angle itself. An angle and its supplement make how much together?",
      ask=ask("c7a", "180°", ["90°", "360°"], S180)),
    B("So the angle is 180 take away 125. Count up from 125: 5 more gets to 130, and 50 more gets to 180. That is 55.",
      W("l2", "125 + 5 = 130"), W("l3", "130 + 50 = 180"), W("l4", "180 − 125 = 55"), L("l5", "The angle = 55°")),
    B("Now for what the question asks: the complement of this angle. A complement is the partner that makes a square corner. Which sum is it?",
      ask=ask("c7b", "90 − 55", ["90 − 125", "180 − 55"],
              "The complement belongs to the angle itself, which is 55. Complementary angles make 90, so take 55 away from 90.")),
    B("90 take away 55 is 35.",
      W("l6", "90 − 55 = 35"), angles("f2", "inRightAngle", [("55°", 55), ("35°", 35)], highlight=["p1"])),
    B("So the complement is 35 degrees.", A("l7", "Complement = 35°"), ring("l7", "35°")),
    B("Check both. 55 and 125 make 180: that is the supplement. 55 and 35 make 90: that is the complement.",
      W("l8", "55 + 125 = 180"), W("l9", "55 + 35 = 90")),
    B("One choice says the angle has no complement. That only happens when an angle is 90 or more. Ours is 55, so it has one. Find the angle first, then its partner."),
])


# ── Q_CH18_008: pairs of vertically opposite angles ──────────────────────────
LESSONS["Q_CH18_008"] = lesson([
    B("Two lines cross, like the letter X. How many pairs of vertically opposite angles do they make?",
      G("l1", "Two lines cross. Pairs of opposite angles = ?"),
      angles("f1", "crossing", [("a",), ("b",), ("c",), ("d",)])),
    B("Two crossing lines make 4 angles round the crossing point. I have called them a, b, c and d.",
      L("l2", "4 angles: a, b, c, d")),
    B("Vertically opposite angles face each other across the crossing point. Which angle is straight across from a?",
      ask=ask("c8a", "c", ["b", "d"],
              "b and d are next door to a, one on each side. The one straight across the crossing point is c.")),
    B("a faces c. That is one pair.",
      L("l3", "Pair 1: a and c"), angles("f2", "crossing", [("a",), ("b",), ("c",), ("d",)], highlight=["p0", "p2"])),
    B("Two angles are left, b and d. They face each other too. That is a second pair.",
      L("l4", "Pair 2: b and d"), angles("f3", "crossing", [("a",), ("b",), ("c",), ("d",)], highlight=["p1", "p3"])),
    B("Every angle is in a pair now. So there are 2 pairs of vertically opposite angles.",
      A("l5", "2 pairs of vertically opposite angles"), ring("l5", "2 pairs")),
    B("The slip to avoid is saying 4. That is the number of angles. They match up across the point, 2 by 2, so there are 2 pairs."),
])


# ── Q_CH18_009: two lines intersect, one angle is 70° ────────────────────────
LESSONS["Q_CH18_009"] = lesson([
    B("Two lines cross, and one of the angles is 70 degrees. We want the angle opposite to it, straight across the crossing point.",
      G("l1", "Lines intersect: one angle is 70°. Opposite = ?"),
      angles("f1", "crossing", [("70°", 70), ("p",), ("?",), ("q",)])),
    B("Look at the angle next door, called p. It shares a straight line with the 70. What do two angles on a straight line make together?",
      ask=ask("c9a", "180°", ["90°", "360°"], LINE180)),
    B("So p is 180 take away 70, which is 110.",
      W("l2", "180 − 70 = 110"),
      angles("f2", "crossing", [("70°", 70), ("110°",), ("?",), ("q",)], highlight=["p0", "p1"])),
    B("Now p and our mystery angle share the other straight line. So the mystery angle is 180 take away 110. What is that?",
      ask=ask("c9b", "70°", ["110°", "20°"],
              "180 take away 110 leaves 70. You can check: 110 and 70 make 180.")),
    B("70. The very same as the angle we started with!", W("l3", "180 − 110 = 70")),
    B("That always happens. Angles straight across a crossing are called vertically opposite, and they are always equal.",
      L("l4", "Vertically opposite angles are equal"),
      A("l5", "Opposite angle = 70°"), ring("l5", "70°"),
      angles("f3", "crossing", [("70°", 70), ("110°",), ("70°",), ("110°",)], highlight=["p0", "p2"])),
    B("So next time there is nothing to work out: the opposite angle is equal. 110 is the neighbour on the line, not the angle across."),
])


# ── Q_CH18_010: a linear pair, one angle 65° ─────────────────────────────────
LESSONS["Q_CH18_010"] = lesson([
    B("Two angles form a linear pair, and one of them is 65 degrees. We want the other one.",
      G("l1", "Linear pair: one angle is 65°. The other = ?"), angles("f1", "onLine", [("65°", 65), ("?",)])),
    B("The word linear has line inside it. A linear pair is two angles side by side on a straight line. So what do they add up to?",
      ask=ask("c10a", "180°", ["90°", "360°"], LINE180)),
    B("So 65, plus the other angle, makes 180.",
      L("l2", "Linear pair: adds up to 180°"), W("l3", "65 + ? = 180"), ring("l3", "?")),
    B("We need 180 take away 65. First take away 60, which leaves 120. Then take 5 more. What is left?",
      W("l4", "180 − 60 = 120"),
      ask=ask("c10b", "115", ["125", "25"],
              "5 less than 120 is 115. We are taking away, so we land below 120.")),
    B("115. So 180 take away 65 is 115.",
      W("l5", "120 − 5 = 115"), W("l6", "180 − 65 = 115")),
    B("The other angle is 115 degrees.",
      A("l7", "The other angle = 115°"), ring("l7", "115°"),
      angles("f2", "onLine", [("65°", 65), ("115°", 115)], highlight=["p1"])),
    B("Check: 65 and 115. 60 and 110 make 170, and the two 5s make 10 more. 180.",
      W("l8", "60 + 110 = 170"), W("l9", "65 + 115 = 180")),
    B("The two angles of a linear pair do not have to be equal. They just have to make a straight line together: 180 degrees."),
])


# ── Q_CH18_011: the hands at 3 o'clock ───────────────────────────────────────
LESSONS["Q_CH18_011"] = lesson([
    B("What is the angle between the hour hand and the minute hand at 3 o'clock? Here is the clock.",
      G("l1", "Angle between the hands at 3 o'clock = ?"), clock("f1", 3, 0)),
    B("The 12 numbers cut the clock face into 12 equal gaps, and all the way round is a full turn of 360 degrees. So how big is one gap?",
      L("l2", "12 gaps = full turn = 360°"),
      ask=ask("c11a", "30°", ["12°", "60°"],
              "Share 360 among the 12 gaps. 12 times 30 is 360, so each gap is 30 degrees.")),
    B("360 divided by 12 is 30. Each gap is 30 degrees.",
      W("l3", "360 ÷ 12 = 30"), box("l3", "= 30")),
    B("At 3 o'clock the minute hand points straight up at the 12, and the hour hand points at the 3. How many gaps are between them?",
      ask=ask("c11b", "3 gaps", ["2 gaps", "4 gaps"],
              "Count the jumps: 12 to 1, 1 to 2, 2 to 3. That is 3 gaps.")),
    B("3 gaps of 30 make 90 degrees.", W("l4", "3 × 30 = 90")),
    B("So the angle is 90 degrees.", A("l5", "Angle = 90°"), ring("l5", "90°")),
    B("And look at the clock. The hands make a perfect square corner, and 90 degrees is a right angle. Count the gaps, then times by 30."),
])


# ── Q_CH18_012: the hands at 9:30 ────────────────────────────────────────────
LESSONS["Q_CH18_012"] = lesson([
    B("What is the angle between the hour hand and the minute hand at 9:30? This one has a catch.",
      G("l1", "Angle between the hands at 9:30 = ?"), clock("f1", 9, 30)),
    B("Each gap between two numbers on a clock is 30 degrees, because 360 shared among 12 gaps is 30.",
      W("l2", "360 ÷ 12 = 30"), L("l3", "1 gap = 30°")),
    B("At half past, the minute hand points at the 6. Now the catch. Where is the hour hand at half past 9?",
      ask=ask("c12a", "halfway between 9 and 10", ["exactly on the 9", "exactly on the 10"],
              "The hour hand keeps moving all the time. In half an hour it goes half of the way from the 9 to the 10.")),
    B("Halfway between the 9 and the 10. So we count in two parts. First, from the 6 to the 9. That is 3 gaps, and 3 times 30 is 90.",
      W("l4", "3 × 30 = 90")),
    B("Then the extra half gap, past the 9. Half of 30 is 15.",
      W("l5", "30 ÷ 2 = 15"), note("l5", "= 15", "half a gap")),
    B("Add the two parts. 90 and 15 make 105.", W("l6", "90 + 15 = 105")),
    B("So the angle is 105 degrees.", A("l7", "Angle = 105°"), ring("l7", "105°")),
    B("90 is the trap. That is what you get if you leave the hour hand on the 9. At half past, the hour hand is always half a gap further on."),
])
