"""Grade 4 angles lessons written for one question each: G4A_ANGLES_001 to G4A_ANGLES_011."""
from g4_gr4_angles_lib import (A, B, FIG, G, L, W, angles, ask, box, clock, compass, lesson, mark, note, ring)

LESSONS = {}

LINE180 = "Angles side by side on a straight line make a half turn together. A half turn is 180 degrees."
TURN360 = "All the way round a point is a full turn, and a full turn is 360 degrees. 180 is only half way round."


# ── G4A_ANGLES_001: three angles on a straight line ──────────────────────────
LESSONS["G4A_ANGLES_001"] = lesson([
    B("Three angles lie side by side on a straight line. Two of them are 48 degrees and 67 degrees. We want the third.",
      G("l1", "On a straight line: 48°, 67° and ?"),
      angles("f1", "onLine", [("48°", 48), ("67°", 67), ("?",)])),
    B("What do the angles on a straight line add up to?",
      ask=ask("e1a", "180°", ["360°", "90°"], LINE180 + " 360 is for angles all the way round a point.")),
    B("So all three angles together make 180. First, add the two we know.",
      L("l2", "Angles on a straight line = 180°"), box("l2", "180°")),
    B("48 and 67. 40 and 60 make 100. 8 and 7 make 15. So that is 115.",
      W("l3", "40 + 60 = 100"), W("l4", "8 + 7 = 15"), W("l5", "48 + 67 = 115")),
    B("We have 115. Is that our answer?",
      ask=ask("e1b", "No, take it away from 180", ["Yes, the answer is 115°"],
              "115 is the two angles we were given, added together. The third angle is the piece that is still missing from the straight line.")),
    B("The third angle is what is left of the 180. Take away 100 first, which leaves 80. Then 15 more, which leaves 65.",
      W("l6", "180 − 100 = 80"), W("l7", "80 − 15 = 65"), W("l8", "180 − 115 = 65")),
    B("So the third angle is 65 degrees.",
      A("l9", "Third angle = 65°"), ring("l9", "65°"),
      angles("f2", "onLine", [("48°", 48), ("67°", 67), ("65°", 65)], highlight=["p2"])),
    B("Check by adding all three: 115 and 65 make 180. One whole straight line.", W("l10", "115 + 65 = 180")),
    B("So for angles on a line: add what you know, then take it away from 180."),
])


# ── G4A_ANGLES_002: the pizza ────────────────────────────────────────────────
LESSONS["G4A_ANGLES_002"] = lesson([
    B("A pizza is cut from the centre into 8 equal slices, and Ria eats 3. What angle do the remaining slices make at the centre?",
      G("l1", "8 equal slices, 3 eaten. Angle of the rest = ?"),
      FIG("f1", kind="fractionBars", shape="circle", bars=[{"parts": 8, "shaded": 5}])),
    B("All the slices meet at the centre, and together they go the whole way round. How many degrees is the whole way round?",
      ask=ask("e2a", "360°", ["180°", "90°"], TURN360)),
    B("360 shared among 8 equal slices. Half of 360 is 180, half of 180 is 90, and half of 90 is 45. So each slice is 45 degrees.",
      W("l2", "360 ÷ 2 = 180"), W("l3", "180 ÷ 2 = 90"), W("l4", "90 ÷ 2 = 45"), W("l5", "360 ÷ 8 = 45")),
    B("Ria eats 3 of the 8 slices. How many slices are left?",
      ask=ask("e2b", "5 slices", ["3 slices", "11 slices"],
              "There were 8 slices to begin with, and 3 are eaten. 8 take away 3 leaves 5.")),
    B("5 slices are left, and each one is 45 degrees.", W("l6", "8 − 3 = 5")),
    B("5 times 45. 4 slices are half the pizza, which is 180 degrees. One more slice of 45 makes 225.",
      W("l7", "4 × 45 = 180"), W("l8", "180 + 45 = 225"), W("l9", "5 × 45 = 225")),
    B("So the remaining slices make an angle of 225 degrees.",
      A("l10", "The remaining slices make 225°"), ring("l10", "225°")),
    B("A check: the 3 eaten slices make 135. And 135 and 225 make 360, the whole pizza.",
      W("l11", "3 × 45 = 135"), W("l12", "135 + 225 = 360")),
    B("135 is the trap. It is the part that was eaten. Always look at which slices the question asks about."),
])


# ── G4A_ANGLES_003: the hour hand from 3 p.m. to 7:30 p.m. ───────────────────
LESSONS["G4A_ANGLES_003"] = lesson([
    B("How many degrees does the hour hand turn between 3 p.m. and half past 7 the same evening?",
      G("l1", "Hour hand, 3 p.m. to 7:30 p.m. Degrees turned = ?")),
    B("The hour hand goes once round the clock, 360 degrees, in 12 hours. So in 1 hour it turns 360 divided by 12, which is 30 degrees.",
      L("l2", "12 hours = full turn = 360°"), W("l3", "360 ÷ 12 = 30")),
    B("How long is it from 3 p.m. to half past 7?",
      ask=ask("e3a", "4 and a half hours", ["4 hours", "5 hours"],
              "From 3 to 7 is 4 hours. Then there is half an hour more, up to half past 7.")),
    B("4 whole hours, and then half an hour.", L("l4", "3 p.m. to 7:30 p.m. = 4 and a half hours")),
    B("For the 4 whole hours, the hand turns 4 times 30, which is 120 degrees.", W("l5", "4 × 30 = 120")),
    B("Don't stop there! The hour hand keeps moving during the last half hour. Half an hour gives half of 30, which is 15.",
      W("l6", "30 ÷ 2 = 15"), note("l6", "= 15", "the half hour")),
    B("120 and 15 make 135. The hour hand turns through 135 degrees.",
      W("l7", "120 + 15 = 135"), A("l8", "The hour hand turns 135°"), ring("l8", "135°")),
    B("The hour hand is slow but steady. 30 degrees for every hour, and 15 for every half hour."),
])


# ── G4A_ANGLES_004: a three-quarter turn anticlockwise from East ─────────────
LESSONS["G4A_ANGLES_004"] = lesson([
    B("Arjun faces east. He makes a three-quarter turn anticlockwise. Which way does he face now?",
      G("l1", "Facing East. Three-quarter turn anticlockwise. Now?"), compass("f1", "E")),
    B("A quarter turn takes you from one main direction to the next. A three-quarter turn is 3 of those, one after another.",
      L("l2", "Three-quarter turn = 3 quarter turns")),
    B("Anticlockwise means the opposite way to clock hands. Starting from east, which direction comes first going anticlockwise?",
      ask=ask("e4a", "North", ["South"],
              "Clock hands go from east down to south. Anticlockwise is the other way, so from east we go up to north.")),
    B("First quarter turn: east to north.",
      L("l3", "1st: East → North"), compass("f2", "E", [(90, "a")], end=True)),
    B("Second quarter turn, still anticlockwise: north to west.", L("l4", "2nd: North → West")),
    B("Third quarter turn: west to south.",
      L("l5", "3rd: West → South"), compass("f3", "E", [(270, "a")], end=True)),
    B("So Arjun is facing south.", A("l6", "Arjun faces South"), ring("l6", "South")),
    B("A neat check: three quarters anticlockwise lands in the same place as one quarter clockwise. And one step clockwise from east is south."),
    B("Take quarter turns one at a time, and always check which way round you are going."),
])


# ── G4A_ANGLES_005: the ladder against the wall ──────────────────────────────
LESSONS["G4A_ANGLES_005"] = lesson([
    B("A ladder leans on a wall and makes 58 degrees with the ground. What angle does it make with the wall? Look: the ladder, the wall and the ground make a triangle.",
      G("l1", "Ladder makes 58° with the ground. With the wall = ?"),
      FIG("f1", kind="triangle", shape="right", sides={"ab": "wall", "bc": "ground", "ca": "ladder"},
          angles={"c": "58°", "a": "?"})),
    B("The wall stands upright and the ground is level. So what angle do the wall and the ground make?",
      ask=ask("e5a", "90°", ["180°", "58°"],
              "Upright meeting level makes a square corner, like the corner of a room. A square corner is a right angle, 90 degrees.")),
    B("The three angles of any triangle add up to 180 degrees. The right angle uses 90 of that. So the other two angles share what is left: 90.",
      L("l2", "Angles of a triangle = 180°"), W("l3", "180 − 90 = 90")),
    B("So the two angles at the ends of the ladder make 90 together. One of them is 58. Which sum finds the other?",
      ask=ask("e5b", "90 − 58", ["180 − 58", "90 + 58"],
              "The two ladder angles make 90 together, and one is 58. So take 58 away from 90. Taking it from 180 forgets the right angle.")),
    B("90 take away 50 is 40, and 8 more away is 32.",
      W("l4", "90 − 50 = 40"), W("l5", "40 − 8 = 32"), W("l6", "90 − 58 = 32")),
    B("So the ladder makes an angle of 32 degrees with the wall.",
      A("l7", "Angle with the wall = 32°"), ring("l7", "32°"),
      FIG("f2", kind="triangle", shape="right", sides={"ab": "wall", "bc": "ground", "ca": "ladder"},
          angles={"c": "58°", "a": "32°"}, highlight=["a"])),
    B("Check: 58 and 32 make 90, and the right angle adds 90 more. 180 in all.",
      W("l8", "58 + 32 = 90"), W("l9", "90 + 58 + 32 = 180")),
    B("In a triangle with a right angle, the other two angles always make 90 together."),
])


# ── G4A_ANGLES_006: 6:00 to 6:30, how much smaller ───────────────────────────
LESSONS["G4A_ANGLES_006"] = lesson([
    B("At 6 o'clock the hands make a straight line, 180 degrees. By 6:30 the angle is smaller. We want to know how much smaller.",
      G("l1", "6:00: angle is 180°. How much smaller at 6:30?"), clock("f1", 6, 0)),
    B("First we need the angle at half past 6. The minute hand has gone half way round, and now it points at the 6. Where is the hour hand?",
      clock("f2", 6, 30),
      ask=ask("e6a", "halfway between 6 and 7", ["still on the 6", "on the 7"],
              "The hour hand moves too. In half an hour it goes half of the way from the 6 to the 7.")),
    B("Halfway between the 6 and the 7. That is the first trap. If it had stayed on the 6, the two hands would be together."),
    B("One gap between two numbers is 30 degrees, because 360 shared among 12 gaps is 30. So half a gap is 15.",
      W("l2", "360 ÷ 12 = 30"), W("l3", "30 ÷ 2 = 15")),
    B("So at half past 6, the angle between the hands is just 15 degrees.",
      L("l4", "Angle at 6:30 = 15°")),
    B("Now read the question again. Does it ask for the angle at 6:30?",
      ask=ask("e6b", "No, how much smaller it became", ["Yes, so the answer is 15°"],
              "The question says: by how many degrees has the angle become smaller. So we compare 180 at the start with 15 now.")),
    B("The angle went from 180 down to 15. The drop is 180 take away 15, which is 165.",
      W("l5", "180 − 15 = 165")),
    B("So the angle has become smaller by 165 degrees.",
      A("l6", "The angle is smaller by 165°"), ring("l6", "165°")),
    B("Two traps in one question. The hour hand creeps, and the question asks for the change, not the new angle. Read the last line twice."),
])


# ── G4A_ANGLES_007: the lighthouse lamp ──────────────────────────────────────
LESSONS["G4A_ANGLES_007"] = lesson([
    B("A lighthouse lamp makes one full turn every 40 seconds, at a steady speed. How many degrees does it turn in 15 seconds?",
      G("l1", "Full turn every 40 seconds. Turn in 15 seconds = ?")),
    B("How many degrees is one full turn?",
      ask=ask("e7a", "360°", ["180°", "100°"],
              "A full turn takes you all the way round, back to where you started. That is 360 degrees.")),
    B("So the lamp turns 360 degrees in 40 seconds.", L("l2", "40 seconds = full turn = 360°")),
    B("Find the turn in 1 second first. 360 shared among 40 seconds. Cross a zero off each number: 36 divided by 4, which is 9.",
      W("l3", "36 ÷ 4 = 9"), W("l4", "360 ÷ 40 = 9")),
    B("9 degrees every second. Now, which sum gives the turn in 15 seconds?",
      ask=ask("e7b", "15 × 9", ["360 ÷ 15", "15 × 40"],
              "Each second gives 9 degrees, and there are 15 seconds. So it is 15 times 9.")),
    B("15 times 9. 10 nines are 90, and 5 nines are 45. 90 and 45 make 135.",
      W("l5", "10 × 9 = 90"), W("l6", "5 × 9 = 45"), W("l7", "15 × 9 = 135")),
    B("So the lamp turns through 135 degrees.", A("l8", "The lamp turns 135°"), ring("l8", "135°")),
    B("Does that make sense? 15 seconds is less than half of 40 seconds. And 135 is less than half a turn, 180. Good.",
      W("l9", "135 < 180")),
    B("Find what happens in 1 second, then multiply. That works for anything that turns at a steady speed."),
])


# ── G4A_ANGLES_008: the supplement is 3 times the complement ─────────────────
LESSONS["G4A_ANGLES_008"] = lesson([
    B("The supplement of an angle is 3 times its complement. We must find the angle. There is a lovely idea hiding in here.",
      G("l1", "Supplement = 3 × complement. Angle = ?")),
    B("Take any angle. Its complement tops it up to 90. Its supplement tops it up to 180. So how much bigger is the supplement than the complement?",
      L("l2", "Complement: tops the angle up to 90°"), L("l3", "Supplement: tops the angle up to 180°"),
      ask=ask("e8a", "always 90° bigger", ["always twice as big", "it depends on the angle"],
              "Both start from the same angle. One goes up to 90 and the other goes up to 180, which is 90 further. So the supplement is always 90 more.")),
    B("180 is 90 more than 90. So the supplement is always the complement, plus 90.",
      W("l4", "180 − 90 = 90"), L("l5", "Supplement = complement + 90°"), box("l5", "+ 90°")),
    B("Now use the clue. The supplement is 3 times the complement. Picture the complement as 1 block. Then the supplement is 3 of those blocks.",
      FIG("f1", kind="barModel", bars=[
          {"label": "Complement", "segments": [{"units": 1, "tone": "a"}]},
          {"label": "Supplement", "segments": [{"units": 1, "tone": "a"}, {"units": 1, "tone": "b"}, {"units": 1, "tone": "b"}]}])),
    B("The supplement has 2 blocks more than the complement. And we know the extra is 90. So 2 blocks make 90. How big is 1 block?",
      W("l6", "3 − 1 = 2"),
      ask=ask("e8b", "45°", ["30°", "90°"],
              "2 equal blocks make 90, so each block is half of 90. That is 45.")),
    B("Half of 90 is 45. So the complement is 45 degrees.",
      W("l7", "90 ÷ 2 = 45"), L("l8", "Complement = 45°")),
    B("The angle and its complement make 90. So the angle is 90 take away 45, which is 45 as well.",
      W("l9", "90 − 45 = 45"), A("l10", "Angle = 45°"), ring("l10", "45°")),
    B("Check. The supplement of 45 is 180 take away 45, which is 135. And 3 times 45 is 135. It works.",
      W("l11", "180 − 45 = 135"), W("l12", "3 × 45 = 135")),
    B("The key was one fact: a supplement is always 90 more than the complement of the same angle."),
])


# ── G4A_ANGLES_009: one angle is 4 times the angle beside it ─────────────────
LESSONS["G4A_ANGLES_009"] = lesson([
    B("Two straight lines cross. One angle is 4 times the angle beside it. We want the largest angle.",
      G("l1", "Lines cross: one angle = 4 × the one beside it. Largest?"),
      angles("f1", "crossing", [("big",), ("small",), ("big",), ("small",)])),
    B("Two angles beside each other at a crossing sit on one straight line. So what do those two add up to?",
      ask=ask("e9a", "180°", ["360°", "90°"], LINE180 + " 360 is for all 4 angles round the point.")),
    B("Now think in parts. Call the smaller angle 1 part. The angle beside it is 4 times as big, so it is 4 parts.",
      L("l2", "Small = 1 part, big = 4 parts")),
    B("How many parts make the 180?",
      ask=ask("e9b", "5 parts", ["4 parts", "3 parts"],
              "1 part for the small angle and 4 parts for the big one. 1 and 4 make 5 parts.")),
    B("5 parts make 180, so one part is 180 divided by 5. 5 thirties are 150 and 5 sixes are 30. So 5 times 36 is 180. One part is 36.",
      W("l3", "1 + 4 = 5"), W("l4", "150 + 30 = 180"), W("l5", "180 ÷ 5 = 36")),
    B("36 is the small angle. The big one is 4 parts, 4 times 36. Double 36 is 72, and double 72 is 144.",
      W("l6", "2 × 36 = 72"), W("l7", "2 × 72 = 144"), W("l8", "4 × 36 = 144")),
    B("Opposite angles at a crossing are equal. So the 4 angles are 144, 36, 144 and 36. The largest is 144 degrees.",
      angles("f2", "crossing", [("144°",), ("36°",), ("144°",), ("36°",)], highlight=["p0", "p2"]),
      A("l9", "Largest angle = 144°"), ring("l9", "144°")),
    B("Check: 36 and 144 make 180, a straight line.", W("l10", "36 + 144 = 180")),
    B("36 is the trap. It is the small angle, and the question wants the largest. And angles beside each other share a straight line, so they share 180, not 360."),
])


# ── G4A_ANGLES_010: five angles round a point ────────────────────────────────
LESSONS["G4A_ANGLES_010"] = lesson([
    B("5 angles meet at a point and fill the whole turn. One is 80 degrees, and the other 4 are equal. How big is each equal angle?",
      G("l1", "Round a point: 80° and 4 equal angles. Each = ?"),
      angles("f1", "aroundPoint", [("80°", 80), ("?",), ("?",), ("?",), ("?",)])),
    B("The angles fill the whole turn round the point. How many degrees is that?",
      ask=ask("e10a", "360°", ["180°", "90°"], TURN360)),
    B("First take away the angle we know. 360 take away 60 is 300, and 20 more away is 280.",
      L("l2", "Whole turn = 360°"), W("l3", "360 − 60 = 300"), W("l3b", "300 − 20 = 280"),
      W("l4", "360 − 80 = 280")),
    B("280 is left for the equal angles. How many angles share it?",
      ask=ask("e10b", "4 angles", ["5 angles"],
              "There are 5 angles in all, but the 80 has already been taken out. Only the 4 equal angles share the 280.")),
    B("280 shared among 4. 28 divided by 4 is 7, so 280 divided by 4 is 70.",
      W("l5", "28 ÷ 4 = 7"), W("l6", "280 ÷ 4 = 70")),
    B("So each of the equal angles is 70 degrees.",
      A("l7", "Each equal angle = 70°"), ring("l7", "70°"),
      angles("f2", "aroundPoint", [("80°", 80), ("70°", 70), ("70°", 70), ("70°", 70), ("70°", 70)])),
    B("Check: 4 times 70 is 280, and 80 more makes 360. A whole turn.",
      W("l8", "4 × 70 = 280"), W("l9", "280 + 80 = 360")),
    B("Take away what you know, then share the rest. And share it only among the angles that are still unknown."),
])


# ── G4A_ANGLES_011: the smaller angle at 2:40 ────────────────────────────────
LESSONS["G4A_ANGLES_011"] = lesson([
    B("What is the smaller angle between the hands of a clock at 2:40? Here is the clock.",
      G("l1", "Smaller angle between the hands at 2:40 = ?"), clock("f1", 2, 40)),
    B("The 12 numbers cut the full turn of 360 degrees into 12 equal gaps. Each gap is 30 degrees.",
      W("l2", "360 ÷ 12 = 30")),
    B("At 40 minutes past, the minute hand is on the 8. Measure from the top of the clock, the 12. From the 12 round to the 8 is 8 gaps, and 8 times 30 is 240.",
      W("l3", "8 × 30 = 240"), note("l3", "= 240", "minute hand")),
    B("Now the hour hand. At 2 o'clock it is 2 gaps from the top, 60 degrees. But it moves 30 degrees in 60 minutes: 1 degree every 2 minutes. How far does it move in 40 minutes?",
      W("l4", "2 × 30 = 60"),
      ask=ask("e11a", "20°", ["10°", "40°"],
              "1 degree for every 2 minutes. 40 minutes is 20 lots of 2 minutes. So the hour hand moves 20 degrees.")),
    B("20 degrees. So the hour hand is at 60 and 20 more: 80 degrees from the top.",
      W("l5", "40 ÷ 2 = 20"), W("l6", "60 + 20 = 80"), note("l6", "= 80", "hour hand")),
    B("The angle between the hands is the difference. 240 take away 80 is 160.", W("l7", "240 − 80 = 160")),
    B("Is 160 the smaller angle? The two ways round the clock make 360 together, so the other way round is 200. Yes, 160 is the smaller one.",
      W("l8", "360 − 160 = 200")),
    B("The trap is to leave the hour hand on the 2. From the 2 to the 8 is 6 gaps, which would be 180. But the hour hand has crept 20 degrees closer.",
      W("l9", "6 × 30 = 180"), W("l10", "180 − 20 = 160")),
    B("So the smaller angle is 160 degrees.", A("l11", "Smaller angle = 160°"), ring("l11", "160°")),
    B("Measure both hands from the top of the clock, then subtract. And remember that the hour hand never sits still."),
])
