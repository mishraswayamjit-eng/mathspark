"""Grade 4 angles lessons written for one question each: G4A_ANGLES_012 to G4A_ANGLES_022."""
from g4_gr4_angles_lib import (A, B, FIG, G, L, W, angles, ask, box, clock, compass, lesson, mark, note, ring)

LESSONS = {}

C90 = "Complementary angles fit together into a square corner. A square corner is a right angle, and that is 90 degrees."
TURN360 = "All the way round a point is a full turn, and a full turn is 360 degrees. 180 is only half way round."


# ── G4A_ANGLES_012: 2:10 to 2:50, minute hand against hour hand ──────────────
LESSONS["G4A_ANGLES_012"] = lesson([
    B("From 2:10 to 2:50 both hands of a clock keep turning. How many more degrees does the minute hand turn than the hour hand?",
      G("l1", "2:10 to 2:50. Minute hand turn − hour hand turn = ?")),
    B("First, how much time passes from 2:10 to 2:50?",
      ask=ask("f12a", "40 minutes", ["60 minutes", "50 minutes"],
              "Both times are in the same hour. From 10 minutes past to 50 minutes past is 50 take away 10, which is 40 minutes.")),
    B("40 minutes pass.", W("l2", "50 − 10 = 40")),
    B("The minute hand does a full turn, 360 degrees, in 60 minutes. That is 6 degrees every minute. So in 40 minutes it turns 40 times 6, which is 240.",
      W("l3", "360 ÷ 60 = 6"), W("l4", "40 × 6 = 240"), note("l4", "= 240", "minute hand")),
    B("The hour hand is much slower. It crosses one gap of 30 degrees in 60 minutes. That is 1 degree every 2 minutes. So how far does it turn in 40 minutes?",
      L("l5", "Hour hand: 30° in 60 minutes"),
      ask=ask("f12b", "20°", ["40°", "30°"],
              "1 degree for every 2 minutes. 40 minutes is 20 lots of 2 minutes, so the hour hand turns 20 degrees.")),
    B("20 degrees. A small turn, but it counts.", W("l6", "40 ÷ 2 = 20"), note("l6", "= 20", "hour hand")),
    B("The question says how many more. Do we add the two turns, or subtract?",
      ask=ask("f12c", "subtract: 240 − 20", ["add: 240 + 20"],
              "How many more asks how far ahead the minute hand is. That is a difference, so we take the smaller turn away from the bigger one.")),
    B("240 take away 20 is 220. The minute hand turns 220 degrees more.",
      W("l7", "240 − 20 = 220"), A("l8", "The minute hand turns 220° more"), ring("l8", "220°")),
    B("240 is the minute hand alone and 20 is the hour hand alone. Both are waiting in the choices. Only the difference answers how many more."),
])


# ── G4A_ANGLES_013: the hour hand has turned 75° since noon ──────────────────
LESSONS["G4A_ANGLES_013"] = lesson([
    B("At 12 noon the hour hand points straight up. Later it has turned exactly 75 degrees. What time is it?",
      G("l1", "From 12 noon the hour hand turns 75°. Time = ?"), clock("f1", 12, 0, show=False)),
    B("The hour hand goes right round, 360 degrees, in 12 hours. So how far does it turn in 1 hour?",
      L("l2", "12 hours = full turn = 360°"),
      ask=ask("f13a", "30°", ["6°", "60°"],
              "360 degrees shared among 12 hours is 30 degrees for each hour.")),
    B("30 degrees every hour.", W("l3", "360 ÷ 12 = 30")),
    B("So every 30 degrees is 1 hour. How many 30s fit into 75? 30 and 30 make 60. One more 30 would be 90, which is too many. So 2 whole hours.",
      W("l4", "30 + 30 = 60"), W("l5", "60 + 30 = 90")),
    B("2 hours use up 60 degrees. 75 take away 60 leaves 15 degrees still to explain.", W("l6", "75 − 60 = 15")),
    B("15 degrees is half of 30. So how much time does that last bit take?",
      ask=ask("f13b", "30 minutes", ["15 minutes", "50 minutes"],
              "30 degrees takes a whole hour. 15 is half of 30, so it takes half an hour, and half an hour is 30 minutes. The degrees are not the minutes.")),
    B("Half of the turn, so half of the hour: 30 minutes.", L("l7", "15° = half an hour = 30 minutes")),
    B("So 2 hours and 30 minutes have passed since 12 noon. The time is 2:30 in the afternoon.",
      A("l8", "The time is 2:30 pm"), ring("l8", "2:30 pm"), clock("f2", 2, 30, show=False)),
    B("The trap is to read degrees as if they were minutes. The hour hand is slow: 30 degrees for an hour, 15 for half an hour."),
])


# ── G4A_ANGLES_014: Sana at 12:20 ────────────────────────────────────────────
LESSONS["G4A_ANGLES_014"] = lesson([
    B("At 12:20 Sana says the angle between the hands is 120 degrees. We have to find how far her answer is from the true angle.",
      G("l1", "12:20. Sana says 120°. How far from the true angle?"), clock("f1", 12, 20)),
    B("Sana says two things: the minute hand is on the 4, and the hour hand is on the 12. Let's check each. First, each gap on a clock is 360 divided by 12, which is 30 degrees.",
      W("l2", "360 ÷ 12 = 30")),
    B("At 20 minutes past, the minute hand is exactly on the 4. From the 12 to the 4 is 4 gaps, and 4 times 30 is 120. So far, Sana is right.",
      W("l3", "4 × 30 = 120")),
    B("Now the hour hand. Is it exactly on the 12 at 12:20?",
      ask=ask("f14a", "No, it has crept towards the 1", ["Yes, it stays on the 12"],
              "The hour hand moves all the time. In the 20 minutes since 12 o'clock, it has moved a little way towards the 1.")),
    B("How far has it crept? 20 minutes is one third of an hour. In a whole hour the hour hand moves 30 degrees. So it has moved one third of 30, which is 10 degrees.",
      W("l4", "30 ÷ 3 = 10"), note("l4", "= 10", "hour hand")),
    B("It has crept 10 degrees towards the 4, where the minute hand is. So is the true angle bigger or smaller than Sana's 120?",
      ask=ask("f14b", "smaller", ["bigger"],
              "The hour hand has moved towards the minute hand. The two hands are closer together, so the angle is smaller.")),
    B("The true angle is 120 take away 10, which is 110.",
      W("l5", "120 − 10 = 110"), L("l6", "True angle = 110°")),
    B("The question asks how far Sana's answer is from the true one. 120 take away 110 is 10.",
      W("l7", "120 − 110 = 10"), A("l8", "Sana is out by 10°"), ring("l8", "10°")),
    B("110 sits in the choices as a trap. It is the true angle, but the question asks for the difference. Sana forgot that the hour hand never waits."),
])


# ── G4A_ANGLES_015: three turns from North-East ──────────────────────────────
LESSONS["G4A_ANGLES_015"] = lesson([
    B("Farhan faces north-east and makes three turns: 90 clockwise, 225 anticlockwise, then 135 clockwise. Where does he end up facing?",
      G("l1", "North-East: 90° clockwise, 225° anti, 135° clockwise"), compass("f1", "NE")),
    B("We could follow every turn. But here is a quicker idea: clockwise and anticlockwise are opposites, so they cancel. How much does he turn clockwise altogether?",
      ask=ask("f15a", "225°", ["135°", "90°"],
              "Two of the turns are clockwise: the 90 and the 135. Add them. 90 and 135 make 225.")),
    B("90 and 135 make 225, clockwise.", W("l2", "90 + 135 = 225")),
    B("And anticlockwise he turns 225. Look at that! 225 one way, and 225 the other way.",
      L("l3", "Clockwise 225°, anticlockwise 225°"), W("l4", "225 − 225 = 0")),
    B("So what do all his turns come to?",
      ask=ask("f15b", "nothing: they cancel out", ["a full turn", "a half turn"],
              "Turning 225 one way and then 225 back the other way undoes everything. It is like taking 5 steps forward and 5 steps back.")),
    B("The turns cancel, so he ends up facing the way he started: north-east.",
      A("l5", "He faces North-East again"), ring("l5", "North-East")),
    B("Let's check it the slow way. From north-east, 90 clockwise is south-east. Then 225 anticlockwise is 5 steps back: east, north-east, north, north-west, west.",
      L("l6", "NE → SE, then back 5 steps → W")),
    B("From west, 135 clockwise is 3 steps: north-west, north, north-east. Home again.",
      L("l7", "W → NW → N → NE"), ring("l7", "NE")),
    B("When turns go both ways, add up each direction first. Often a lot of it cancels."),
])


# ── G4A_ANGLES_016: working backwards from South ─────────────────────────────
LESSONS["G4A_ANGLES_016"] = lesson([
    B("Ravi turns 135 degrees clockwise and then 90 degrees anticlockwise. Now he faces south. Which way was he facing at the start?",
      G("l1", "135° clockwise, then 90° anticlockwise. Ends: South"), L("l2", "Started facing = ?")),
    B("We know where Ravi ends, not where he starts. So we work backwards, like rewinding a film. When you rewind, which turn gets undone first?",
      ask=ask("f16a", "the last one: 90° anticlockwise", ["the first one: 135° clockwise"],
              "Rewinding goes backwards through time. The last thing he did was the 90 anticlockwise turn, so that one is undone first.")),
    B("To undo a turn, turn the same amount the opposite way. So to undo 90 anticlockwise, we turn 90 clockwise, starting from south.",
      L("l3", "Undo 90° anticlockwise: 90° clockwise"), compass("f1", "S", [(90, "c")], end=True)),
    B("90 clockwise from south is a quarter turn, and it takes us to west. So between his two turns, Ravi was facing west.",
      L("l4", "South → West")),
    B("Now undo the first turn, 135 clockwise. Which way do we turn to undo it?",
      ask=ask("f16b", "135° anticlockwise", ["135° clockwise"],
              "Undoing means going the opposite way. He turned clockwise, so we go back anticlockwise.")),
    B("The compass directions are 45 degrees apart, so 135 is 3 steps. Anticlockwise from west: south-west, south, south-east.",
      W("l5", "3 × 45 = 135"), L("l6", "West → SW → S → SE"), compass("f2", "W", [(135, "a")], end=True)),
    B("So Ravi was facing south-east before he turned.",
      A("l7", "He started facing South-East"), ring("l7", "South-East")),
    B("Check it forwards. From south-east, 135 clockwise goes south, south-west, west. Then 90 anticlockwise from west goes back to south. Yes!"),
    B("South-west is the trap. You get it by doing the turns again from south, instead of undoing them. Working backwards means last turn first, and the opposite way."),
])


# ── G4A_ANGLES_017: the robot and 13 presses ─────────────────────────────────
LESSONS["G4A_ANGLES_017"] = lesson([
    B("A robot faces north. Each press of the button turns it 45 degrees clockwise. Which way does it face after 13 presses?",
      G("l1", "Facing North. 13 presses of 45° clockwise. Now?"), compass("f1", "N")),
    B("Each press of 45 degrees is one step round the 8 compass directions. How many presses bring the robot right back to north?",
      ask=ask("f17a", "8 presses", ["4 presses", "12 presses"],
              "There are 8 compass directions, one step apart. So 8 presses take the robot once all the way round, back to north.")),
    B("8 presses make 8 times 45, which is 360 degrees. A full turn. The robot faces north again.",
      W("l2", "8 × 45 = 360")),
    B("So the first 8 of the 13 presses change nothing. 13 take away 8 leaves 5 presses that matter.",
      W("l3", "13 − 8 = 5"), box("l3", "= 5")),
    B("Now count 5 steps clockwise from north. Careful: north is where it starts. The first press takes it to north-east. Where does the 5th press land?",
      ask=ask("f17b", "South-West", ["South", "West"],
              "Count the presses, not the starting place. North-east, east, south-east, south, south-west. The 5th press lands on south-west.")),
    B("North-east, east, south-east, south, south-west. The robot faces south-west.",
      L("l4", "1 NE, 2 E, 3 SE, 4 S, 5 SW"),
      A("l5", "The robot faces South-West"), ring("l5", "South-West"),
      compass("f2", "N", [(225, "c")], end=True)),
    B("South is the trap. You get it if you count north as step 1. North is the start, before any press."),
    B("When something goes round and round, throw away the full turns first. Then count what is left."),
])


# ── G4A_ANGLES_018: three angles round a point, 1, 2 and 3 parts ─────────────
LESSONS["G4A_ANGLES_018"] = lesson([
    B("Three angles fill the whole turn round a point. The second is twice the first, and the third is three times the first. What kind of angle is the largest?",
      G("l1", "3 angles fill a full turn: first, 2 × first, 3 × first"), L("l2", "The largest is what kind of angle?")),
    B("Read carefully: the angles fill the whole turn round a point. So what do they add up to?",
      ask=ask("f18a", "360°", ["180°", "90°"], TURN360)),
    B("Call the first angle 1 part. Then the second is 2 parts and the third is 3 parts.",
      L("l3", "1 part, 2 parts, 3 parts"),
      FIG("f1", kind="barModel", bars=[
          {"label": "First", "segments": [{"units": 1, "tone": "a"}]},
          {"label": "Second", "segments": [{"units": 1, "tone": "b"}] * 2},
          {"label": "Third", "segments": [{"units": 1, "tone": "c"}] * 3}])),
    B("How many parts are there altogether?",
      ask=ask("f18b", "6 parts", ["5 parts", "3 parts"], "Add them all: 1 and 2 and 3 make 6 parts.")),
    B("6 parts make 360. 6 times 60 is 360, so one part is 60 degrees.",
      W("l4", "1 + 2 + 3 = 6"), W("l5", "6 × 60 = 360"), W("l6", "360 ÷ 6 = 60")),
    B("The largest angle is 3 parts. 3 times 60 is 180.", W("l7", "3 × 60 = 180")),
    B("180 degrees. What kind of angle is exactly 180?",
      ask=ask("f18c", "a straight angle", ["an obtuse angle", "a reflex angle"],
              "Obtuse angles stop just before 180, and reflex angles start just after it. Exactly 180 makes a straight line: a straight angle.")),
    B("So the largest of the three is a straight angle.",
      A("l8", "The largest is a straight angle (180°)"), ring("l8", "straight angle"),
      angles("f2", "aroundPoint", [("60°", 60), ("120°", 120), ("180°", 180)], highlight=["p2"])),
    B("The three angles are 60, 120 and 180. 120 is obtuse, but it is not the largest. Find every size exactly before you name it.",
      W("l9", "2 × 60 = 120")),
])


# ── G4A_ANGLES_019: three of the four angles add up to 250° ──────────────────
LESSONS["G4A_ANGLES_019"] = lesson([
    B("Two straight lines cross and make 4 angles. Three of them add up to 250 degrees. We want the smallest of the 4 angles.",
      G("l1", "Lines cross. 3 of the 4 angles add up to 250°."), L("l2", "Smallest angle = ?"),
      angles("f1", "crossing", [("a",), ("b",), ("c",), ("d",)])),
    B("The 4 angles go all the way round the crossing point. So what do all 4 add up to?",
      ask=ask("f19a", "360°", ["180°", "250°"], TURN360)),
    B("360 for all 4, and 250 for three of them. So the angle that was left out is 360 take away 250, which is 110.",
      W("l3", "360 − 250 = 110")),
    B("Is 110 the smallest? Find the others before you decide. The angle beside the 110 shares a straight line with it, and a straight line is 180. So how big is it?",
      L("l4", "Angles on a straight line = 180°"),
      ask=ask("f19b", "70°", ["110°", "55°"],
              "Angles side by side on a straight line make 180. 180 take away 110 leaves 70.")),
    B("180 take away 110 is 70.", W("l5", "180 − 110 = 70")),
    B("Angles opposite each other at a crossing are equal. So the 4 angles are 110, 70, 110 and 70.",
      angles("f2", "crossing", [("110°",), ("70°",), ("110°",), ("70°",)], highlight=["p1", "p3"]),
      L("l6", "110°, 70°, 110°, 70°")),
    B("So the smallest angle is 70 degrees.", A("l7", "Smallest angle = 70°"), ring("l7", "70°")),
    B("Check the clue. The three that were added are 110, 70 and 70. And they do make 250.",
      W("l8", "110 + 70 + 70 = 250")),
    B("110 was the first number we found, but it was not the answer. Find all 4 angles, then pick the one the question wants."),
])


# ── G4A_ANGLES_020: 30° more than its complement ─────────────────────────────
LESSONS["G4A_ANGLES_020"] = lesson([
    B("An angle is 30 degrees more than its complement. We want the supplement of this angle. There is a lot to keep track of, so let's go slowly.",
      G("l1", "An angle is 30° more than its complement."), L("l2", "Its supplement = ?"),
      FIG("f1", kind="barModel", bars=[
          {"label": "Complement", "segments": [{"units": 2, "label": "?", "tone": "a"}]},
          {"label": "Angle", "segments": [{"units": 2, "label": "?", "tone": "a"}, {"units": 1, "label": "30°", "tone": "b"}]}])),
    B("An angle and its complement add up to how much?",
      ask=ask("f20a", "90°", ["180°", "360°"], C90)),
    B("The angle is its complement, plus an extra 30. Cut off that extra 30, and two equal pieces are left. Together they make 90 take away 30, which is 60.",
      W("l3", "90 − 30 = 60")),
    B("Two equal pieces make 60, so each one is 30. That is the complement.",
      W("l4", "60 ÷ 2 = 30"), L("l5", "Complement = 30°")),
    B("The angle is 30 more than that. 30 and 30 make 60. So the angle is 60 degrees.",
      W("l6", "30 + 30 = 60"), L("l7", "Angle = 60°")),
    B("Now stop, and read the question again. What does it ask for?",
      ask=ask("f20b", "the supplement of the angle", ["the angle itself", "the complement"],
              "The last line asks for the supplement of this angle. That is the partner that makes a straight line with it.")),
    B("The supplement makes 180 with the angle. 180 take away 60 is 120.",
      mark("l2", "supplement"), W("l8", "180 − 60 = 120")),
    B("So the supplement of the angle is 120 degrees.", A("l9", "Supplement = 120°"), ring("l9", "120°")),
    B("We found three numbers: complement 30, angle 60, supplement 120. All three are tempting. Answer the one that was asked."),
])


# ── G4A_ANGLES_021: P, Q and R ───────────────────────────────────────────────
LESSONS["G4A_ANGLES_021"] = lesson([
    B("Angles P and Q add up to 90. Angles Q and R add up to 180. We have to find what is always true, whatever the size of P.",
      G("l1", "P + Q = 90°.   Q + R = 180°.   What is always true?")),
    B("No sizes are given, so let's choose one ourselves and see what happens. Say P is 20 degrees. P and Q make 90. So what is Q?",
      L("l2", "Try P = 20°"),
      ask=ask("f21a", "70°", ["160°", "20°"],
              "P and Q are complementary, so they make 90. 90 take away 20 is 70.")),
    B("Q is 70. Now Q and R make 180. So R is 180 take away 70, which is 110.",
      W("l3", "90 − 20 = 70"), W("l4", "180 − 70 = 110")),
    B("So P is 20 and R is 110. R is 90 more than P. But was that just luck? Let's try another size.",
      W("l5", "110 − 20 = 90")),
    B("This time let P be 40. Then Q is 90 take away 40, which is 50. And R is 180 take away 50, which is 130.",
      L("l6", "Try P = 40°"), W("l7", "90 − 40 = 50"), W("l8", "180 − 50 = 130")),
    B("P is 40 and R is 130. How much more is R than P this time?",
      ask=ask("f21b", "90 more again", ["50 more", "they are equal"],
              "130 take away 40 is 90. So R is 90 more than P, the same as before.")),
    B("90 again. Here is why. Q is in both pairs. With P it makes 90. With R it makes 180, which is 90 more. So R must be 90 bigger than P.",
      W("l9", "130 − 40 = 90"), box("l9", "= 90")),
    B("So what is always true is this: angle R is 90 degrees more than angle P.",
      A("l10", "Angle R is 90° more than angle P"), ring("l10", "90° more")),
    B("When a question says whatever the size, test it with two different numbers. A rule that is really true works every time."),
])


# ── G4A_ANGLES_022: where can the ray OC go ──────────────────────────────────
LESSONS["G4A_ANGLES_022"] = lesson([
    B("Angle A O B is 70 degrees. A ray O C makes 30 degrees with O B. Riya says angle A O C must be 100. Is she right?",
      G("l1", "Angle AOB = 70°. Angle BOC = 30°. Angle AOC = ?"),
      angles("f1", "single", [("AOB = 70°", 70)])),
    B("Riya pictured the ray O C on the far side of O B, away from O A. Then the two angles sit side by side, and we add them. 70 and 30 make 100.",
      W("l2", "70 + 30 = 100"), note("l2", "= 100", "OC outside"),
      angles("f2", "single", [("AOC = 100°", 100)])),
    B("So 100 is possible. But there is no picture in the question. Is the far side the only place where O C can go?",
      ask=ask("f22a", "No, it can be on either side of OB", ["Yes, only on the far side"],
              "The question only says O C makes 30 degrees with O B. It does not say which side. O C could also lie on the near side, between O A and O B.")),
    B("Put O C on the near side, inside angle A O B. Now the 30 is a slice cut out of the 70. So angle A O C is 70 take away 30, which is 40.",
      W("l3", "70 − 30 = 40"), note("l3", "= 40", "OC inside"),
      angles("f3", "single", [("AOC = 40°", 40)])),
    B("So angle A O C could be 100, or it could be 40. Could it be any size in between as well?",
      ask=ask("f22b", "No, only those two", ["Yes, anything from 40° to 100°"],
              "Angle B O C is fixed at exactly 30. A ray that is 30 degrees from O B has only two places to go: one on each side of O B.")),
    B("Only two places, one on each side of O B. So there are only two possible answers.",
      L("l4", "OC outside: 100°.   OC inside: 40°.")),
    B("So angle A O C could be 100 degrees or 40 degrees.",
      A("l5", "It could be 100° or 40°"), ring("l5", "100° or 40°")),
    B("Riya's adding was fine. Her slip was the word must. When there is no picture, ask yourself: is there another way to draw it?"),
])
