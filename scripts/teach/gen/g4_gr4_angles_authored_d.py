"""Grade 4 angles lessons written for one question each: Q_CH18_013 to Q_CH18_025."""
from g4_gr4_angles_lib import (A, B, FIG, G, L, W, angles, ask, box, clock, compass, group, lesson, mark, note, ring,
                               strike)

LESSONS = {}

S180 = "Supplementary angles sit side by side on a straight line, and a straight line is a half turn. That is 180 degrees."
C90 = "Complementary angles fit together into a square corner. A square corner is a right angle, and that is 90 degrees."
LINE180 = "Angles side by side on a straight line make a half turn together. A half turn is 180 degrees."


# ── Q_CH18_013: when is the angle between the hands obtuse ───────────────────
LESSONS["Q_CH18_013"] = lesson([
    B("At which of these 4 times do the clock hands make an obtuse angle? We need to test each time.",
      G("l1", "At which time is the angle between the hands obtuse?"), L("l2", "3:30     4:00     10:00     6:00")),
    B("First, what makes an angle obtuse?",
      ask=ask("d13a", "between 90° and 180°", ["less than 90°", "exactly 180°"],
              "Obtuse means wider than a right angle, 90 degrees, but not yet a straight line, 180 degrees.")),
    B("On a clock, each gap between two numbers is 30 degrees. So 90 degrees is 3 gaps, and 180 degrees is 6 gaps. We want more than 3 gaps, but fewer than 6.",
      W("l3", "3 × 30 = 90"), W("l4", "6 × 30 = 180")),
    B("Start with the o'clock times. At 10 o'clock the minute hand points straight up, and the hour hand is on the 10, only 2 gaps away. 60 degrees. That is acute.",
      W("l5", "2 × 30 = 60"), strike("l2", "10:00", "60°: acute")),
    B("At 6 o'clock the hands are 6 gaps apart, pointing opposite ways. Exactly 180. That is a straight angle, and an obtuse angle must be less than 180.",
      strike("l2", "6:00", "180°: straight")),
    B("Now half past 3. The minute hand is on the 6. Careful: where is the hour hand?",
      clock("f1", 3, 30),
      ask=ask("d13b", "halfway between 3 and 4", ["exactly on the 3"],
              "By half past, the hour hand has gone half of the way to the next number. So it is halfway between the 3 and the 4.")),
    B("So from the hour hand to the 6 is 2 and a half gaps. 60, and 15 more, is 75 degrees. Acute again. Leaving the hand on the 3 would give 90, and that is the trap.",
      W("l6", "60 + 15 = 75"), strike("l2", "3:30", "75°: acute")),
    B("That leaves 4 o'clock. The hands are 4 gaps apart, and 4 times 30 is 120. More than 90, and less than 180.",
      W("l7", "4 × 30 = 120"), W("l8", "90 < 120 < 180"), clock("f2", 4, 0)),
    B("So the angle is obtuse at 4 o'clock.", A("l9", "Obtuse at 4:00"), ring("l9", "4:00")),
    B("For each time: find both hands, count the gaps, and times by 30. Then name the angle."),
])


# ── Q_CH18_014: when do the hands form a straight angle ──────────────────────
LESSONS["Q_CH18_014"] = lesson([
    B("When do the two hands of a clock form a straight angle, 180 degrees? We have three times to test.",
      G("l1", "When do the hands form a straight angle (180°)?"), L("l2", "3:45     6:00     9:15     all of these")),
    B("A straight angle means the hands point in exactly opposite directions. Each gap between two numbers on a clock is 30 degrees. So 180 degrees is how many gaps?",
      L("l3", "1 gap = 30°"),
      ask=ask("d14a", "6 gaps", ["3 gaps", "12 gaps"],
              "6 times 30 is 180. So the hands must be exactly 6 gaps apart, half way round the clock from each other.")),
    B("6 gaps of 30 make 180. So we want the hands exactly 6 gaps apart.", W("l4", "6 × 30 = 180")),
    B("At 6 o'clock the minute hand points straight up, and the hour hand is exactly on the 6, straight down. 6 gaps apart. A perfect straight line.",
      clock("f1", 6, 0), ring("l2", "6:00")),
    B("Now 3:45. The minute hand is on the 9, and the 9 is opposite the 3. But is the hour hand still on the 3?",
      clock("f2", 3, 45),
      ask=ask("d14b", "No, it has moved towards the 4", ["Yes, it stays on the 3"],
              "The hour hand never stops. After 45 minutes it has gone three quarters of the way from the 3 to the 4.")),
    B("It has crept most of the way to the 4. So the hands are not exactly opposite any more.",
      strike("l2", "3:45", "not opposite")),
    B("It is the same story at 9:15. The minute hand is on the 3, opposite the 9. But the hour hand has moved a little past the 9. Close to a straight line, but not exact.",
      clock("f3", 9, 15), strike("l2", "9:15", "not opposite")),
    B("So the hands form a straight angle only at 6 o'clock.",
      A("l5", "A straight angle at 6:00"), ring("l5", "6:00")),
    B("All of these was the trap. It only looks true if the hour hand waits on its number. It never does, except exactly on the hour."),
])


# ── Q_CH18_015: when is the angle between the hands greatest ─────────────────
LESSONS["Q_CH18_015"] = lesson([
    B("At which of these 4 times is the angle between the clock hands the greatest? We have to compare them.",
      G("l1", "At which time is the angle between the hands greatest?"), L("l2", "4:30     6:15     9:00     12:15")),
    B("Every gap between two numbers on a clock is the same size, 30 degrees. So to begin with we can just count gaps. The most gaps wins.",
      L("l3", "1 gap = 30°")),
    B("9 o'clock is the easy one. The hour hand is exactly on the 9 and the minute hand is on the 12. That is 3 gaps.",
      L("l4", "9:00 → 3 gaps")),
    B("At half past 4, the minute hand is on the 6. The hour hand is halfway between the 4 and the 5. So how many gaps is it from there to the 6?",
      ask=ask("d15a", "1 and a half gaps", ["2 gaps", "2 and a half gaps"],
              "From halfway past the 4, it is half a gap to reach the 5, and then one more gap to the 6. That is 1 and a half gaps.")),
    B("1 and a half gaps. That is small. Not our winner.", L("l5", "4:30 → 1 and a half gaps")),
    B("Now the two quarter past times. In 15 minutes, a quarter of an hour, the hour hand creeps a quarter of a gap forward. That little creep decides everything."),
    B("At 12:15 the minute hand is on the 3. The hour hand has crept a little past the 12, towards the 3. So the angle shrinks: a bit less than 3 gaps.",
      clock("f1", 12, 15), L("l6", "12:15 → a bit less than 3 gaps")),
    B("At 6:15 the minute hand is on the 3 again. But the hour hand has crept past the 6, away from the 3. Is the angle bigger or smaller than 3 gaps?",
      clock("f2", 6, 15),
      ask=ask("d15b", "bigger than 3 gaps", ["smaller than 3 gaps", "exactly 3 gaps"],
              "From the 3 to the 6 is 3 gaps. The hour hand has moved on past the 6, further from the 3. So the angle has grown a little.")),
    B("A bit more than 3 gaps. That beats 9 o'clock, which is exactly 3.",
      L("l7", "6:15 → a bit more than 3 gaps"), box("l7", "a bit more than 3 gaps")),
    B("So the greatest angle is at 6:15.", A("l8", "Greatest angle at 6:15"), ring("l8", "6:15")),
    B("3 gaps are exactly 90 degrees. So 6:15 is just past a right angle, and 12:15 is just short of one.",
      W("l9", "3 × 30 = 90")),
    B("The hour hand's small creep matters. Always ask which way it creeps: towards the other hand, or away from it."),
])


# ── Q_CH18_016: 1 o'clock is 30°. When is the angle complementary to it ──────
LESSONS["Q_CH18_016"] = lesson([
    B("At 1 o'clock the hands are 30 degrees apart. We want the time when the angle is complementary to that.",
      G("l1", "At 1 o'clock the angle is 30°. Complementary angle at?"), clock("f1", 1, 0)),
    B("First find the angle we are looking for. Complementary angles add up to how much?",
      ask=ask("d16a", "90°", ["180°", "360°"], C90)),
    B("So the angle we want is 90 take away 30. That is 60 degrees.", W("l2", "90 − 30 = 60")),
    B("On a clock, each gap between two numbers is 30 degrees. That is why 1 o'clock gives 30: the hands are 1 gap apart. How many gaps make 60?",
      ask=ask("d16b", "2 gaps", ["3 gaps", "6 gaps"], "30 and 30 make 60. So 60 degrees is 2 gaps.")),
    B("2 gaps of 30 make 60. So we need the hands 2 gaps apart.", W("l3", "2 × 30 = 60")),
    B("On the hour, the minute hand points straight up. The hour hand must be 2 gaps away from it, and that is on the 2. So the time is 2 o'clock.",
      clock("f2", 2, 0), A("l4", "At 2 o'clock"), ring("l4", "2 o'clock")),
    B("Check the other times. 5 o'clock and 7 o'clock are both 5 gaps from the top, 150 degrees. 6 o'clock is 180, a straight line. None of them is 60.",
      W("l5", "5 × 30 = 150"), W("l6", "6 × 30 = 180")),
    B("Two steps: first find the angle you need, then turn it into gaps on the clock."),
])


# ── Q_CH18_017: the angle between North-East and South ───────────────────────
LESSONS["Q_CH18_017"] = lesson([
    B("What is the angle between north-east and south? Here is the compass.",
      G("l1", "Angle between North-East and South = ?"), compass("f1", "NE")),
    B("North, east, south and west are the 4 main directions. They share a full turn of 360 degrees equally. So from one to the next is a quarter turn, 90 degrees.",
      W("l2", "360 ÷ 4 = 90")),
    B("North-east sits exactly halfway between north and east. So how far is it from north-east round to east?",
      ask=ask("d17a", "45°", ["90°", "30°"],
              "North-east is halfway between two directions that are 90 apart. Half of 90 is 45.")),
    B("Half of 90 is 45. That is the first part of the turn.",
      W("l3", "90 ÷ 2 = 45"), L("l4", "NE to E = 45°")),
    B("Then from east on to south is one more quarter turn, 90 degrees.",
      L("l5", "E to S = 90°"), compass("f2", "NE", [(135, "c")], end=True)),
    B("Add the two parts. 45 and 90 make 135.", W("l6", "45 + 90 = 135")),
    B("So the angle between north-east and south is 135 degrees.", A("l7", "Angle = 135°"), ring("l7", "135°")),
    B("The slip is to stop at 90 and forget the first little piece, from north-east to east. Walk round the compass one stop at a time, and add as you go."),
])


# ── Q_CH18_018: the hour hand in one hour ────────────────────────────────────
LESSONS["Q_CH18_018"] = lesson([
    B("How many degrees does the hour hand of a clock move in one hour?",
      G("l1", "How many degrees does the hour hand move in one hour?")),
    B("Think about the hour hand's whole trip. How long does it take to go once all the way round the clock?",
      ask=ask("d18a", "12 hours", ["1 hour", "24 hours"],
              "The hour hand is the slow one. It points at each of the 12 numbers in turn, one number each hour. So once round takes 12 hours.")),
    B("12 hours for one full turn, and a full turn is 360 degrees.",
      L("l2", "12 hours = full turn = 360°")),
    B("It moves steadily, so each hour gets an equal share. Which sum gives the share for 1 hour?",
      ask=ask("d18b", "360 ÷ 12", ["360 ÷ 60", "360 × 12"],
              "The 360 degrees are shared equally among 12 hours. Sharing means dividing, so it is 360 divided by 12.")),
    B("360 divided by 12. 12 times 3 is 36, so 12 times 30 is 360. The answer is 30.",
      W("l3", "12 × 3 = 36"), W("l4", "360 ÷ 12 = 30")),
    B("So the hour hand moves 30 degrees in one hour.",
      A("l5", "The hour hand moves 30° in one hour"), ring("l5", "30°")),
    B("You can see it on a clock. In one hour the hour hand goes from one number to the next, say from 2 to 3. That gap is 30 degrees.",
      clock("f1", 3, 0, show=False)),
    B("Do not mix it up with the minute hand. That one is fast: it does the whole 360 in one hour. The hour hand does just 30."),
])


# ── Q_CH18_019: the minute hand in 1 minute ──────────────────────────────────
LESSONS["Q_CH18_019"] = lesson([
    B("How many degrees does the minute hand of a clock move in 1 minute?",
      G("l1", "How many degrees does the minute hand move in 1 minute?")),
    B("The minute hand goes once all the way round the clock in 1 hour. How many minutes is that?",
      ask=ask("d19a", "60 minutes", ["12 minutes", "100 minutes"],
              "There are 60 minutes in 1 hour. So the minute hand takes 60 minutes to go once round.")),
    B("60 minutes for one full turn, and a full turn is 360 degrees.",
      L("l2", "60 minutes = full turn = 360°")),
    B("Each minute gets an equal share of the 360. So we divide 360 by 60.", W("l3", "360 ÷ 60 = ?")),
    B("Here is a trick. Cross off a zero from each number. 360 divided by 60 is the same as 36 divided by 6. And what is 36 divided by 6?",
      W("l4", "36 ÷ 6 = ?"),
      ask=ask("d19b", "6", ["5", "30"], "6 times 6 is 36. So 36 divided by 6 is 6.")),
    B("6. So the minute hand moves 6 degrees in 1 minute.",
      W("l5", "360 ÷ 60 = 6"), A("l6", "The minute hand moves 6° in 1 minute"), ring("l6", "6°")),
    B("Check: 60 minutes, at 6 degrees each. 60 times 6 is 360, the full turn.", W("l7", "60 × 6 = 360")),
    B("Do not mix it up with 30 degrees. That is the gap between two numbers, and the minute hand takes 5 whole minutes to cross it. 5 times 6 is 30.",
      W("l8", "5 × 6 = 30")),
])


# ── Q_CH18_020: complementary angles in the ratio 2:3 ────────────────────────
LESSONS["Q_CH18_020"] = lesson([
    B("Two complementary angles are in the ratio 2 to 3. We want the smaller angle.",
      G("l1", "Complementary angles in the ratio 2:3. Smaller = ?")),
    B("What do two complementary angles add up to?",
      ask=ask("d20a", "90°", ["180°", "360°"], C90)),
    B("A ratio of 2 to 3 means the 90 is cut into equal parts. The smaller angle gets 2 parts and the larger angle gets 3 parts.",
      L("l2", "Smaller = 2 parts, larger = 3 parts"),
      FIG("f1", kind="barModel", bars=[
          {"label": "Smaller", "segments": [{"units": 1, "tone": "a"}] * 2},
          {"label": "Larger", "segments": [{"units": 1, "tone": "b"}] * 3}])),
    B("How many equal parts are there altogether?",
      ask=ask("d20b", "5 parts", ["6 parts", "3 parts"],
              "2 parts for one angle and 3 parts for the other. 2 and 3 make 5 parts altogether.")),
    B("5 parts share 90 degrees. So one part is 90 divided by 5. 5 tens are 50 and 5 eights are 40, so 5 times 18 is 90. One part is 18.",
      W("l3", "2 + 3 = 5"), W("l4", "50 + 40 = 90"), W("l5", "90 ÷ 5 = 18")),
    B("The smaller angle is 2 parts. 2 times 18 is 36.", W("l6", "2 × 18 = 36")),
    B("So the smaller angle is 36 degrees.", A("l7", "Smaller angle = 36°"), ring("l7", "36°")),
    B("Check. The larger angle is 3 parts, 3 times 18, which is 54. And 36 and 54 make 90.",
      W("l8", "3 × 18 = 54"), W("l9", "36 + 54 = 90")),
    B("54 is waiting in the choices as a trap. It is the larger angle. Always look back to see which one the question asks for."),
])


# ── Q_CH18_021: supplementary angles that differ by 40° ──────────────────────
LESSONS["Q_CH18_021"] = lesson([
    B("Two supplementary angles differ by 40 degrees. So one is 40 bigger than the other. We want the larger one.",
      G("l1", "Supplementary angles differ by 40°. Larger = ?"),
      FIG("f1", kind="barModel", bars=[
          {"label": "Smaller", "segments": [{"units": 3, "label": "smaller", "tone": "a"}]},
          {"label": "Larger", "segments": [{"units": 3, "label": "smaller", "tone": "a"}, {"units": 1, "label": "40°", "tone": "b"}]}])),
    B("What do two supplementary angles add up to?",
      ask=ask("d21a", "180°", ["90°", "360°"], S180)),
    B("So the two angles make 180 together. Now look at the two bars. The larger angle is the smaller one, with an extra 40 on the end.",
      L("l2", "Larger = smaller + 40°"), mark("l2", "+ 40°")),
    B("Suppose we cut that extra 40 off the larger angle. What are we left with?",
      ask=ask("d21b", "two equal angles", ["nothing at all", "one angle of 180°"],
              "Without its extra 40, the larger bar is exactly as long as the smaller bar. So we are left with two equal angles.")),
    B("Two equal angles. And together they make 180 take away 40, which is 140.", W("l3", "180 − 40 = 140")),
    B("Two equal angles sharing 140. Each one is half of 140, which is 70. That is the smaller angle.",
      W("l4", "140 ÷ 2 = 70"), L("l5", "Smaller angle = 70°")),
    B("Here is the trap. The question asks for the larger angle. So give the 40 back. 70 and 40 make 110.",
      W("l6", "70 + 40 = 110")),
    B("So the larger angle is 110 degrees.", A("l7", "Larger angle = 110°"), ring("l7", "110°")),
    B("Check both facts. 70 and 110 make 180, so they are supplementary. And 110 take away 70 is 40.",
      W("l8", "70 + 110 = 180"), W("l9", "110 − 70 = 40")),
    B("So when you know the total and the difference: take off the difference, halve, then add the difference back for the bigger one."),
])


# ── Q_CH18_022: three angles meeting at a point ──────────────────────────────
LESSONS["Q_CH18_022"] = lesson([
    B("Three angles meet at a point. Two of them are 110 degrees and 85 degrees, and the third is x. We want x.",
      G("l1", "Angles at a point: 110°, 85° and x°. x = ?"),
      angles("f1", "aroundPoint", [("110°", 110), ("85°", 85), ("x°",)])),
    B("The three angles go all the way round the point, with no gaps. How much is a turn all the way round?",
      ask=ask("d22a", "360°", ["180°", "90°"],
              "All the way round a point is a full turn, and a full turn is 360 degrees. 180 is only half way round, a straight line.")),
    B("A full turn is 360. So 110, plus 85, plus x, makes 360.",
      L("l2", "Full turn = 360°"), W("l3", "110 + 85 + x = 360")),
    B("First add the two angles we know. 110 and 80 is 190, and 5 more makes 195.",
      W("l4", "110 + 80 = 190"), W("l5", "110 + 85 = 195"), group("l3", ["110", "85"], "195")),
    B("195 of the 360 is used up. x is whatever is left. Which sum finds it?",
      ask=ask("d22b", "360 − 195", ["360 + 195", "195 − 180"],
              "360 is the whole turn, and 195 is the part we know. Take the part from the whole: 360 take away 195.")),
    B("360 take away 195. Take away 200 first, which leaves 160. But that took 5 too many, so give 5 back: 165.",
      W("l6", "360 − 200 = 160"), W("l7", "160 + 5 = 165"), W("l8", "360 − 195 = 165")),
    B("So x equals 165.",
      W("l9", "x = 165", tone="answer"), ring("l9", "x = 165"),
      angles("f2", "aroundPoint", [("110°", 110), ("85°", 85), ("165°", 165)], highlight=["p2"])),
    B("Check: 195 and 165 make 360. A full turn.", W("l10", "195 + 165 = 360")),
    B("Angles round a point make 360. Angles on a straight line make 180. Look at which picture you have before you start."),
], check=("x", 165))


# ── Q_CH18_023: x°, 2x° and 3x° on a straight line ───────────────────────────
LESSONS["Q_CH18_023"] = lesson([
    B("Three angles sit on a straight line. They are x, 2 x and 3 x. We want to find x.",
      G("l1", "On a straight line: x°, 2x° and 3x°. x = ?"),
      angles("f1", "onLine", [("x°",), ("2x°",), ("3x°",)])),
    B("What do the angles on a straight line add up to?",
      ask=ask("d23a", "180°", ["90°", "360°"], LINE180)),
    B("So x, plus 2 x, plus 3 x, equals 180.", W("l2", "x + 2x + 3x = 180")),
    B("Think of x as one equal slice. Then 2 x is 2 slices, and 3 x is 3 slices. How many slices are there in all?",
      ask=ask("d23b", "6 slices", ["5 slices", "3 slices"],
              "Do not forget the first x. It is 1 slice by itself. 1 and 2 and 3 make 6 slices.")),
    B("1 and 2 and 3 make 6. So 6 x equals 180.",
      group("l2", ["x", "2x", "3x"], "6x"), W("l3", "6x = 180")),
    B("6 slices make 180, so one slice is 180 divided by 6. 6 times 30 is 180, so x is 30.",
      {"op": "divide", "line": "l3", "by": "6"}, W("l3b", "6 × 30 = 180"),
      W("l4", "x = 30", tone="answer"), ring("l4", "x = 30")),
    B("Check. The three angles are 30, 60 and 90. Add them up, and they make 180. A straight line.",
      W("l5", "2 × 30 = 60"), W("l6", "3 × 30 = 90"), W("l7", "30 + 60 + 90 = 180")),
    B("So count how many x there are altogether, then share the 180 among them."),
], check=("x", 30))


# ── Q_CH18_024: the hands at 4:30 ────────────────────────────────────────────
LESSONS["Q_CH18_024"] = lesson([
    B("What is the angle between the clock hands at 4:30? Here is the clock.",
      G("l1", "Angle between the clock hands at 4:30 = ?"), clock("f1", 4, 30)),
    B("The 12 numbers cut the full turn of 360 degrees into 12 equal gaps. So each gap is 30 degrees.",
      W("l2", "360 ÷ 12 = 30"), L("l3", "1 gap = 30°")),
    B("At half past 4 the minute hand is on the 6. Where is the hour hand?",
      ask=ask("d24a", "halfway between 4 and 5", ["exactly on the 4", "exactly on the 5"],
              "The hour hand keeps moving. In half an hour it goes half of the way from the 4 to the 5.")),
    B("Halfway between the 4 and the 5. That is the catch. If it were still on the 4, we would count 2 gaps to the 6 and say 60. But it has moved.",
      W("l4", "2 × 30 = 60"), strike("l4", "60", "hand has moved")),
    B("From where it really is, it is half a gap up to the 5, and then one whole gap from the 5 to the 6.",
      L("l5", "half a gap + 1 gap"), mark("l5", "half a gap")),
    B("Half a gap is half of 30, which is 15. One whole gap is 30.", W("l6", "30 ÷ 2 = 15")),
    B("15 and 30 make 45.", W("l7", "15 + 30 = 45")),
    B("So the angle is 45 degrees.", A("l8", "Angle = 45°"), ring("l8", "45°")),
    B("At half past any hour, the hour hand sits halfway between two numbers. Start counting from there, not from the number."),
])


# ── Q_CH18_025: facing North, 225° clockwise ─────────────────────────────────
LESSONS["Q_CH18_025"] = lesson([
    B("A person faces north and turns clockwise through 225 degrees. Which way is he facing now?",
      G("l1", "Facing North, turns clockwise through 225°. Now?"), compass("f1", "N")),
    B("225 is a big turn, so let's break it up. A half turn is 180 degrees. From north, where does a half turn take you?",
      L("l2", "Half turn = 180°"),
      ask=ask("d25a", "South", ["East", "West"],
              "A half turn makes you face the opposite way. The opposite of north is south.")),
    B("South. That uses up 180 of the 225. 225 take away 180 leaves 45 still to turn.",
      W("l3", "225 − 180 = 45")),
    B("The 8 compass directions are 45 degrees apart, because 360 shared among 8 is 45. So 45 degrees is exactly one more step.",
      W("l4", "360 ÷ 8 = 45"), L("l5", "1 step = 45°")),
    B("So from south, go one more step clockwise. Which direction comes next?",
      ask=ask("d25b", "South-West", ["South-East", "West"],
              "Clockwise goes north, east, south, west. So after south we are heading towards west, and the direction between south and west is south-west.")),
    B("South-west. He is facing south-west.",
      A("l6", "He faces South-West"), ring("l6", "South-West"), compass("f2", "N", [(225, "c")], end=True)),
    B("Or count steps. 225 is 5 steps of 45: north-east, east, south-east, south, south-west. The same answer.",
      W("l7", "5 × 45 = 225")),
    B("South-east is the trap. You land there if you count too few steps. Go round one stop at a time, the way clock hands move."),
])
