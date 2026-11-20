"""Grade 4 angles lessons written for one question each: past papers (PYQ_...) and the
worksheet questions (EXT_G4_WS2_CH18_...)."""
from g4_gr4_angles_lib import (A, B, G, L, W, angles, ask, box, clock, compass, lesson, mark, note, ring)

LESSONS = {}

S180 = "Supplementary angles sit side by side on a straight line, and a straight line is a half turn. That is 180 degrees."
C90 = "Complementary angles fit together into a square corner. A square corner is a right angle, and that is 90 degrees."


# ── PYQ_2016_Q14: facing South, then North-East ──────────────────────────────
LESSONS["PYQ_2016_Q14"] = lesson([
    B("A man faces south. Later he faces north-east. We have to say how he turned: how many degrees, and which way round.",
      G("l1", "Facing South, then North-East. How did he turn?"), compass("f1", "S")),
    B("The 8 compass directions share a full turn of 360 degrees. So each step from one direction to the next is 360 divided by 8, which is 45 degrees.",
      W("l2", "360 ÷ 8 = 45"), L("l3", "1 step = 45°")),
    B("Let's go anticlockwise from south first. That is the opposite way to clock hands. How many steps is it to north-east?",
      ask=ask("p14a", "3 steps", ["5 steps", "1 step"],
              "Anticlockwise from south we pass south-east, then east, and then we reach north-east. That is 3 steps.")),
    B("South-east, east, north-east. 3 steps of 45 make 135 degrees, anticlockwise.",
      L("l4", "S → SE → E → NE: 3 steps"), W("l5", "3 × 45 = 135"),
      compass("f2", "S", [(135, "a")], end=True)),
    B("Now the other way, clockwise. South-west, west, north-west, north, north-east. That is 5 steps, and 5 times 45 is 225 degrees.",
      W("l6", "5 × 45 = 225")),
    B("So there are two true ways to say it: 135 anticlockwise, or 225 clockwise. Now the trap. One choice says 135 clockwise. Is that true?",
      ask=ask("p14b", "No, that ends at North-West", ["Yes, 135 is 135"],
              "The size matches, but the direction does not. 135 clockwise from south passes south-west and west, and stops at north-west. The way round matters.")),
    B("The right size, but the other way round, so it lands on north-west. And none of the choices says 225 clockwise.",
      L("l7", "135° clockwise from S ends at NW")),
    B("So the true statement is: he turned 135 degrees in the anticlockwise direction.",
      A("l8", "He turned 135° anticlockwise"), ring("l8", "135° anticlockwise")),
    B("With turning questions, always check two things: how far, and which way round."),
])


# ── PYQ_2016_Q34: supplementary angle to 57 1/4° ─────────────────────────────
LESSONS["PYQ_2016_Q34"] = lesson([
    B("We need the supplementary angle to 57 and a quarter degrees.",
      G("l1", "Supplementary angle to 57 1/4° = ?")),
    B("What do two supplementary angles add up to?",
      ask=ask("p34a", "180°", ["90°", "360°"], S180)),
    B("So we take 57 and a quarter away from 180. A mixed number is easier in two bites: first the whole number, then the quarter.",
      L("l2", "180 − 57 1/4 = ?"), mark("l2", "57"), mark("l2", "1/4", "circle")),
    B("First the 57. 180 take away 50 is 130, and 7 more away leaves 123.",
      W("l3", "180 − 50 = 130"), W("l4", "130 − 7 = 123")),
    B("The quarter still has to come off. What is a quarter less than 123?",
      ask=ask("p34b", "122 3/4", ["123 1/4", "121 3/4"],
              "We are taking away, so the answer drops just below 123. Break one whole into 4 quarters and take 1 quarter off. That leaves 122 and three quarters.")),
    B("Take one whole from 123, leaving 122, and cut that whole into 4 quarters. Take 1 quarter away, and three quarters are left.",
      W("l5", "1 − 1/4 = 3/4"), L("l6", "123 − 1/4 = 122 3/4")),
    B("So the supplementary angle is 122 and three quarters degrees.",
      A("l7", "Supplementary angle = 122 3/4°"), ring("l7", "122 3/4°")),
    B("Check by adding. 57 and 122 make 179. A quarter and three quarters make 1 more. 180 exactly.",
      W("l8", "57 + 122 = 179"), W("l9", "1/4 + 3/4 = 1"), W("l10", "179 + 1 = 180")),
    B("The slip to watch for is adding the quarter back on, instead of taking it off. Whole number first, then the fraction, and both are taken away."),
])


# ── PYQ_2017_Q20: the minute hand in 300 seconds ─────────────────────────────
LESSONS["PYQ_2017_Q20"] = lesson([
    B("In 300 seconds, how many degrees does the minute hand of a clock move?",
      G("l1", "In 300 seconds the minute hand moves ___ degrees")),
    B("The minute hand works in minutes, not seconds. So first, how many minutes is 300 seconds?",
      L("l2", "1 minute = 60 seconds"),
      ask=ask("p20a", "5 minutes", ["30 minutes", "50 minutes"],
              "There are 60 seconds in a minute. 60 times 5 is 300, so 300 seconds is 5 minutes.")),
    B("300 divided by 60 is 5. So we are really asking: how far does the minute hand move in 5 minutes?",
      W("l3", "300 ÷ 60 = 5")),
    B("In 60 minutes the minute hand goes right round the clock once. That is a full turn, 360 degrees.",
      L("l4", "60 minutes = full turn = 360°"), clock("f1", 12, 5, show=False)),
    B("So in 1 minute it turns 360 divided by 60. That is 6 degrees each minute.",
      W("l5", "360 ÷ 60 = 6")),
    B("5 minutes, at 6 degrees each minute. Which sum tells us how far?",
      ask=ask("p20b", "5 × 6", ["5 × 30", "5 + 6"],
              "Each minute is 6 degrees, and there are 5 minutes, so it is 5 times 6. 30 degrees is the size of a whole gap between two numbers, not of 1 minute.")),
    B("5 times 6 is 30. The minute hand moves 30 degrees.",
      W("l6", "5 × 6 = 30"), A("l7", "It moves 30 degrees"), ring("l7", "30")),
    B("And that makes sense. In 5 minutes the minute hand goes from one number to the next, like from 12 to 1. That gap is 360 divided by 12, which is 30 as well.",
      W("l8", "360 ÷ 12 = 30")),
    B("So change the seconds to minutes first. Then it is 6 degrees for every minute."),
])


# ── PYQ_2017_Q40: which pair is complementary ────────────────────────────────
LESSONS["PYQ_2017_Q40"] = lesson([
    B("Here are 4 pairs of angles. Only one pair is complementary, and we have to find it.",
      G("l1", "Which pair of angles is complementary?"),
      L("p1", "30° & 30°        40° & 30°"), L("p2", "22° & 68°        34° & 66°")),
    B("What must two complementary angles add up to?",
      ask=ask("p40a", "90°", ["180°", "100°"], C90)),
    B("So we add each pair and look for 90. 30 and 30 make 60. Too small. 40 and 30 make 70. Still too small.",
      W("l2", "30 + 30 = 60"), W("l3", "40 + 30 = 70")),
    B("Next pair: 22 and 68. Add the ones first: 2 and 8 make 10. Then the tens: 20 and 60 make 80. What is the total?",
      W("l4", "2 + 8 = 10"), W("l5", "20 + 60 = 80"),
      ask=ask("p40b", "90", ["80", "100"], "80 from the tens, and 10 more from the ones. 80 and 10 make 90.")),
    B("22 plus 68 is exactly 90. That is our pair.",
      W("l6", "22 + 68 = 90"), box("l6", "= 90")),
    B("Let's make sure of the last one too. 34 and 66: 4 and 6 make 10, and 30 and 60 make 90, so that is 100. Too big.",
      W("l7", "34 + 66 = 100"), note("l7", "= 100", "too big")),
    B("So the complementary pair is 22 degrees and 68 degrees.",
      A("l8", "Complementary pair: 22° & 68°"), ring("l8", "22° & 68°")),
    B("Complementary means the two angles fill a square corner exactly. So add the pair, and look for 90 on the dot."),
])


# ── PYQ_2019_Q25: which pair is complementary ────────────────────────────────
LESSONS["PYQ_2019_Q25"] = lesson([
    B("4 pairs of angles, and only one pair is complementary. Let's test them one at a time.",
      G("l1", "Which pair of angles is complementary?"),
      L("p1", "55° & 45°        65° & 25°"), L("p2", "35° & 48°        17° & 63°")),
    B("Complementary angles fit together into a square corner. So what must the pair add up to?",
      ask=ask("p25a", "90°", ["180°", "100°"],
              "A square corner is a right angle, and a right angle is 90 degrees. So the pair must add up to 90.")),
    B("First pair: 55 and 45. The two 5s make 10, and 50 and 40 make 90. So that is 100. Too big.",
      W("l2", "50 + 40 = 90"), W("l3", "55 + 45 = 100"), note("l3", "= 100", "too big")),
    B("Second pair: 65 and 25. The two 5s make 10 again, and 60 and 20 make 80. So what is the total?",
      W("l4", "60 + 20 = 80"),
      ask=ask("p25b", "90", ["80", "85"], "80 from the tens, and 10 more from the two 5s. 80 and 10 make 90.")),
    B("65 plus 25 is exactly 90. That is the pair we want.",
      W("l5", "65 + 25 = 90"), box("l5", "= 90")),
    B("A careful mathematician checks the rest. 35 and 48 make 83. 17 and 63 make 80. Neither is 90.",
      W("l6", "35 + 48 = 83"), W("l7", "17 + 63 = 80")),
    B("So the complementary pair is 65 degrees and 25 degrees.",
      A("l8", "Complementary pair: 65° & 25°"), ring("l8", "65° & 25°")),
    B("The first pair was the tempting one, because 55 and 45 look so neat. But they make 100. Always do the adding."),
])


# ── PYQ_2019_Q40: the hands make 45°. What time is it? ───────────────────────
LESSONS["PYQ_2019_Q40"] = lesson([
    B("The teacher's watch shows an angle of 45 degrees between its hands. We have 4 times to choose from, so let's test them.",
      G("l1", "Angle between the hands = 45°. What time is it?"), L("l2", "1:15     2:30     8:30     7:30")),
    B("On a clock, the full turn of 360 degrees is shared by 12 numbers. So each gap between two numbers is 30 degrees.",
      W("l3", "360 ÷ 12 = 30"), L("l4", "1 gap = 30°")),
    B("45 degrees is one whole gap of 30, and half a gap, 15, more. So we want hands that are 1 and a half gaps apart.",
      W("l5", "30 + 15 = 45"), L("l6", "45° = 1 and a half gaps"), box("l6", "1 and a half gaps")),
    B("Three of the times are half past something. At half past, the minute hand is on the 6. But where is the hour hand at half past 7?",
      clock("f1", 7, 30),
      ask=ask("p19a", "halfway between 7 and 8", ["exactly on the 7", "exactly on the 8"],
              "In half an hour, the hour hand goes half of the way to the next number. So at half past 7 it sits halfway between the 7 and the 8.")),
    B("That is the trap: the hour hand does not wait on the 7. Now count from the 6. From 6 to 7 is one gap. Then half a gap more. 1 and a half gaps!",
      L("l7", "7:30 → 1 gap + half a gap"), mark("l7", "1 gap + half a gap")),
    B("And 1 and a half gaps is 45 degrees. So half past 7 fits.", ring("l2", "7:30")),
    B("Now the others. At half past 8 the hour hand is one gap further on: 2 and a half gaps, 75 degrees. At half past 2 it is 3 and a half gaps from the 6. Both are too wide.",
      W("l8", "45 + 30 = 75")),
    B("And at quarter past 1, the minute hand is on the 3 and the hour hand is a little past the 1. That is nearly 2 gaps, which is more than 45 degrees."),
    B("So the time is 7:30.", A("l9", "The time is 7:30"), ring("l9", "7:30")),
    B("With clock angles, count gaps of 30 degrees. And always ask: where has the hour hand crept to?"),
])


# ── EXT_G4_WS2_CH18_001: end points of a line segment ────────────────────────
LESSONS["EXT_G4_WS2_CH18_001"] = lesson([
    B("How many end points does a line segment have? Let's picture one.",
      G("l1", "A line segment has how many end points?")),
    B("Think of a piece of string pulled tight between your two hands. That is a line segment: a straight path with a start and a stop.",
      L("l2", "Line segment:  A •————————• B")),
    B("I have named the two ends A and B. Count the points where the segment stops.",
      ring("l2", "A"), ring("l2", "B"),
      ask=ask("ws1a", "2", ["1", "0"],
              "Put one finger on A, where it starts, and another on B, where it stops. That is 2 end points.")),
    B("2 end points. One at each end.",
      A("l3", "A line segment has 2 end points"), ring("l3", "2")),
    B("Now compare. A ray starts at a point and goes on for ever one way, like the beam of a torch. It has only 1 end point.",
      L("l4", "Ray: 1 end point   •————————→")),
    B("And a line goes on for ever both ways. It has no end points at all.",
      L("l5", "Line: 0 end points   ←————————→")),
    B("So a line has no ends, a ray has 1, and a line segment has 2. Only the segment has a length you can measure."),
])


# ── EXT_G4_WS2_CH18_002: lines through two points ────────────────────────────
LESSONS["EXT_G4_WS2_CH18_002"] = lesson([
    B("Mark two different points, A and B. How many straight lines can pass through both of them?",
      G("l1", "How many lines pass through two distinct points?"), L("l2", "• A                • B")),
    B("Start with just one point, A. How many lines can pass through a single point?",
      ask=ask("ws2a", "as many as you like", ["only 1", "only 2"],
              "Put your ruler on the point and keep turning it, like the spokes of a wheel. Every turn gives a new line. There is no limit.")),
    B("Through one point, lines can go in every direction, like the spokes of a wheel.",
      L("l3", "Through 1 point: lines in every direction")),
    B("Now the line must pass through B as well. Lay your ruler so it touches A and B together. Can you still turn it?",
      ask=ask("ws2b", "No, it is held in place", ["Yes, any way I like"],
              "Try it with a ruler and two dots. Once the ruler touches both dots, any turn makes it slip off one of them.")),
    B("The two points pin the ruler down. Only one straight line fits through both.",
      L("l4", "A •————————————• B"), mark("l4", "•————————————•")),
    B("So through two distinct points, exactly one line can pass.",
      A("l5", "Through 2 points: exactly One line"), ring("l5", "One")),
    B("That is why we can name a line by just two of its points, like line A B. Two points, one line."),
])


# ── EXT_G4_WS2_CH18_003: collinear points ────────────────────────────────────
LESSONS["EXT_G4_WS2_CH18_003"] = lesson([
    B("What do we call three or more points that all lie on the same line?",
      G("l1", "Three or more points on the same line are called?")),
    B("Here are three points, A, B and C, all sitting on one straight line, like beads on a string.",
      L("l2", "——•————•————•——"), L("l3", "    A        B        C")),
    B("The word we want has two pieces. Co means together, as in co-operate. And linear comes from the word line.",
      L("l4", "co + linear = together + on a line")),
    B("So what do we call points that lie together on one line?",
      ask=ask("ws3a", "Collinear", ["Parallel", "Concurrent"],
              "Listen for the word line hiding inside it. Co, together, and linear, on a line: collinear. Parallel and concurrent are words about lines, not about points.")),
    B("Collinear. Points on the same line are collinear points.",
      A("l5", "They are called Collinear points"), ring("l5", "Collinear")),
    B("If one point steps off the line, the three are no longer all on one line. Then we call them non-collinear.",
      L("l6", "Not all on one line: non-collinear")),
    B("A quick test: lay a ruler along the points. If one straight edge touches them all, they are collinear."),
])


# ── EXT_G4_WS2_CH18_004: an angle less than 90° ──────────────────────────────
LESSONS["EXT_G4_WS2_CH18_004"] = lesson([
    B("Angles get their names from how wide they open. Our measuring stick is the right angle, the square corner of a page. That is 90 degrees.",
      G("l1", "An angle less than 90° is called?"),
      angles("f1", "single", [("90°", 90)], note="A right angle is exactly 90°")),
    B("Now close the angle up a little, so it is less than 90. Does it look sharper or blunter than the square corner?",
      angles("f2", "single", [("less than 90°", 50)]),
      ask=ask("ws4a", "sharper, more pointed", ["blunter, more open"],
              "Look at the picture. As the two arms close up, the angle gets narrow and pointed, like the tip of a pencil.")),
    B("Sharp and pointed. The word for that is acute. Acute means sharp.",
      L("l2", "Less than 90° = acute (sharp)"), mark("l2", "acute")),
    B("So an angle less than 90 degrees is called an acute angle.",
      A("l3", "It is called an Acute angle"), ring("l3", "Acute angle"),
      angles("f3", "single", [("acute", 50)])),
    B("Here are the other names, so you can tell them apart. Exactly 90 is a right angle. More than 90 but less than 180 is obtuse. Exactly 180 is a straight angle.",
      L("l4", "90° right     90° to 180° obtuse     180° straight")),
    B("A way to remember: a cute little angle. Acute angles are the small ones."),
])


# ── EXT_G4_WS2_CH18_005: a right angle measures ──────────────────────────────
LESSONS["EXT_G4_WS2_CH18_005"] = lesson([
    B("A right angle is a square corner, like the corner of your book. How many degrees is it?",
      G("l1", "A right angle measures?"), angles("f1", "inRightAngle", [("?",)])),
    B("Start with a full turn. Spin all the way round until you face the same way again. That is 360 degrees.",
      L("l2", "Full turn = 360°"),
      angles("f2", "aroundPoint", [("?",), ("?",), ("?",), ("?",)], highlight=["p0"])),
    B("A right angle is a quarter turn. 4 square corners fit round a point, like the place where 4 floor tiles meet. So how do we find one quarter of 360?",
      ask=ask("ws5a", "360 ÷ 4", ["360 ÷ 2", "360 × 4"],
              "A quarter means one of 4 equal parts. So we share 360 into 4 equal parts. That is 360 divided by 4.")),
    B("360 divided by 4. Half of 360 is 180, and half of 180 is 90.",
      W("l3", "360 ÷ 2 = 180"), W("l4", "180 ÷ 2 = 90"), W("l5", "360 ÷ 4 = 90")),
    B("So a right angle measures 90 degrees.",
      A("l6", "A right angle = 90°"), ring("l6", "90°"), angles("f3", "inRightAngle", [("90°",)])),
    B("Check: 4 right angles make 4 times 90, which is 360. One full turn.",
      W("l7", "4 × 90 = 360")),
    B("So a quarter turn is 90, a half turn is 180, and a full turn is 360. Keep those three in your pocket."),
])


# ── EXT_G4_WS2_CH18_006: an angle of 180° ────────────────────────────────────
LESSONS["EXT_G4_WS2_CH18_006"] = lesson([
    B("What do we call an angle of 180 degrees? Let's see what it looks like first.",
      G("l1", "An angle of 180° is called a?")),
    B("A full turn is 360 degrees. What part of a full turn is 180?",
      L("l2", "Full turn = 360°"),
      ask=ask("ws6a", "a half turn", ["a quarter turn", "a full turn"],
              "180 and 180 make 360. So 180 is half of a full turn.")),
    B("Two lots of 180 make 360. So 180 degrees is a half turn.",
      W("l3", "180 + 180 = 360")),
    B("Point one arm ahead of you. Now turn the other arm half way round. The two arms point in opposite directions. What shape do they make?",
      angles("f1", "single", [("180°", 180)]),
      ask=ask("ws6b", "a straight line", ["a square corner", "a full circle"],
              "Look at the picture. One arm goes left and one goes right. Together they lie flat, in one straight line.")),
    B("A straight line. So an angle of 180 degrees is called a straight angle.",
      A("l4", "180° is a Straight angle"), ring("l4", "Straight angle")),
    B("The other names in the list: a right angle is 90, a reflex angle is bigger than 180, and a complete angle is the full 360.",
      L("l5", "Right 90°     straight 180°     complete 360°")),
    B("The name tells you the picture. Straight angle, straight line, 180 degrees."),
])


# ── EXT_G4_WS2_CH18_007: what type of angle is 135° ──────────────────────────
LESSONS["EXT_G4_WS2_CH18_007"] = lesson([
    B("What type of angle is 135 degrees? Here it is.",
      G("l1", "What type of angle is 135°?"), angles("f1", "single", [("135°", 135)])),
    B("To name an angle, we compare it with two fence posts: 90 degrees, the right angle, and 180 degrees, the straight line.",
      L("l2", "Fence posts: 90° and 180°")),
    B("First fence post. Is 135 more than 90, or less?",
      ask=ask("ws7a", "more than 90", ["less than 90"],
              "135 has a hundred in it, and 90 does not reach a hundred. So 135 is the bigger number.")),
    B("More than 90. So it is wider than a square corner. It cannot be acute, and it cannot be a right angle.",
      W("l3", "135 > 90")),
    B("Second fence post. 135 is less than 180, so it has not opened as far as a straight line. It cannot be reflex.",
      W("l4", "135 < 180")),
    B("So 135 sits between 90 and 180. What is the name for an angle in that band?",
      ask=ask("ws7b", "obtuse", ["acute", "reflex"],
              "Acute is for angles under 90. Reflex is for angles over 180. The band in between, from 90 to 180, is called obtuse.")),
    B("Obtuse. 135 degrees is an obtuse angle.",
      A("l5", "135° is an Obtuse angle"), ring("l5", "Obtuse"), angles("f2", "single", [("obtuse", 135)])),
    B("So to name any angle, ask two questions. Is it past 90? Is it past 180?"),
])


# ── EXT_G4_WS2_CH18_008: two angles that add up to 90° ───────────────────────
LESSONS["EXT_G4_WS2_CH18_008"] = lesson([
    B("Two angles add up to 90 degrees. So together they fill a square corner, like this. What is such a pair called?",
      G("l1", "Two angles that add up to 90° are called?"),
      angles("f1", "inRightAngle", [("angle 1", 55), ("angle 2",)])),
    B("Here is an example: 30 degrees and 60 degrees. Together they make 90, a perfect square corner.",
      W("l2", "30 + 60 = 90"), angles("f2", "inRightAngle", [("30°", 30), ("60°", 60)])),
    B("Each angle completes the other to make the corner. One of the names sounds like the word complete. Which one?",
      ask=ask("ws8a", "Complementary", ["Supplementary", "Adjacent"],
              "Say them aloud. Complete, complementary. They start the same way. Supplementary is for two angles that make a straight line.")),
    B("Complementary. Two angles that add up to 90 degrees are complementary angles.",
      A("l3", "They are called Complementary angles"), ring("l3", "Complementary")),
    B("Its cousin is supplementary: two angles that add up to 180 degrees, a straight line.",
      L("l4", "Supplementary: add up to 180°")),
    B("Here is how to keep them apart. C for complementary, C for corner. S for supplementary, S for straight."),
    B("And the other two names say where angles are, not what they add up to. Adjacent means next door. Vertically opposite means across a crossing."),
])
