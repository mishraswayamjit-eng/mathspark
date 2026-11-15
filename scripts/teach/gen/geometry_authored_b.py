"""Geometry lessons written for one question each: the 2016 and 2017 papers (continued)."""
from geometry_lib import (B, FIG, LV, T, W, arc, choose, divide, group, lesson, mark)

LESSONS = {}


# Three times the measure of an angle is the measure of its supplement.
LESSONS["EXT_G5_FP_2016_037"] = lesson([
    B("An angle and its supplement sit together on a straight line. We are told the supplement is 3 times as big as the angle. How big is the angle?",
      W("l1", "3 × angle = its supplement. Angle = ?", tone="given", label=True),
      FIG("f1", kind="angles", layout="onLine", parts=[{"label": "angle"}, {"label": "supplement"}])),
    B("We do not know the angle, so let's give it a name: x. Then the supplement, which is 3 times as big, is 3 x.",
      W("l2", "angle = x, supplement = 3x", label=True),
      FIG("f2", kind="angles", layout="onLine", parts=[{"label": "x"}, {"label": "3x"}])),
    B("Look at the drawing. x and 3 x lie along a straight line. So what do they add up to?",
      ask=choose(["90°", "360°", "180°"], 2,
                 "A straight line is a half turn, and a half turn is 180 degrees. 90 is for a square corner.")),
    B("A straight line is a half turn, 180 degrees. So x, plus 3 x, equals 180.",
      W("l3", "x + 3x = 180")),
    B("1 x and 3 more x's make 4 x. So 4 x equals 180.",
      group("l3", [T("x", 1), T("3x")], "4x"), W("l4", "4x = 180")),
    B("4 x means 4 times x. How do we undo times 4?",
      ask=choose(["divide by 4", "subtract 4", "multiply by 4"], 0,
                 "Times and divide are partners. To undo times 4, we divide by 4, on both sides.")),
    B("Divide both sides by 4. To divide by 4, halve and halve again. Half of 180 is 90, and half of 90 is 45.",
      divide("l4", "4"), W("l5", "180 ÷ 2 = 90"), W("l6", "90 ÷ 2 = 45")),
    B("So x equals 45. The angle is 45 degrees.",
      W("l7", "x = 45", tone="answer"), mark("l7", "x = 45", "circle")),
    B("Let's check. The supplement is 3 times 45, which is 135. And 45 plus 135 makes 180, a straight line. It works.",
      W("l8", "3 × 45 = 135"), W("l9", "45 + 135 = 180"),
      FIG("f3", kind="angles", layout="onLine", parts=[{"label": "45°", "size": 45}, {"label": "135°", "size": 135}])),
    B("So when a question gives a link between an angle and its supplement, call the angle x, write both on a straight line, and make them add up to 180."),
], "authored", check=("x", 45))


# Triangle sides (2a + 6), (3a + 5), (a + 7) cm; a = 3. Perimeter?
LESSONS["EXT_G5_FP_2016_038"] = lesson([
    B("Here is a triangle whose sides are written with the letter a: 2 a plus 6, 3 a plus 5, and a plus 7. We are told a is 3, and we want the perimeter.",
      W("l1", "Triangle sides: (2a + 6), (3a + 5), (a + 7) cm; a = 3", tone="given", label=True),
      W("l2", "Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="scalene", sides={"ab": "(2a + 6) cm", "bc": "(3a + 5) cm", "ca": "(a + 7) cm"})),
    B("Wherever we see a, we put 3. But first: what does 2 a mean when a is 3?",
      ask=choose(["23", "2 × 3", "2 + 3"], 1,
                 "A number written right next to a letter means times. So 2 a is 2 times 3, not 23.")),
    B("The first side is 2 times 3, plus 6. 2 times 3 is 6, and 6 plus 6 is 12 centimetres.",
      W("l3", "2 × 3 + 6 = 12")),
    B("The second side is 3 times 3, plus 5. 3 times 3 is 9, and 9 plus 5 is 14 centimetres.",
      W("l4", "3 × 3 + 5 = 14")),
    B("The third side is the easy one: 3 plus 7 is 10 centimetres. Now every side has a real length.",
      W("l5", "3 + 7 = 10"),
      FIG("f2", kind="triangle", shape="scalene", sides={"ab": "12 cm", "bc": "14 cm", "ca": "10 cm"})),
    B("Perimeter is the walk all the way round the triangle. Which sum gives it?",
      ask=choose(["12 + 14", "12 + 14 + 10", "12 × 14"], 1,
                 "The walk goes along every side, and a triangle has 3 of them. So we add all 3 lengths.")),
    B("Add them one at a time. 12 plus 14 is 26. Then 26 plus 10 is 36.",
      W("l6", "Perimeter = side + side + side", label=True), W("l7", "12 + 14 = 26"), W("l8", "26 + 10 = 36")),
    B("So the perimeter is 36 centimetres.",
      W("l9", "Perimeter = 36 cm", tone="answer", label=True), mark("l9", "36 cm", "circle"),
      FIG("f3", kind="triangle", shape="scalene", sides={"ab": "12 cm", "bc": "14 cm", "ca": "10 cm"},
          highlight=["ab", "bc", "ca"], note="Perimeter = 36 cm")),
    B("Here is another way to check. Add the letters first: the 3 sides together are 6 a plus 18. And 6 times 3, plus 18, is 36 too.",
      W("l10", "6 × 3 + 18 = 36")),
    B("So: put the number in place of the letter to get each side, then add all the sides for the walk round."),
], "authored")


# Clock shows 11:00 a.m. The hour hand turns through 165°. What is the time?
LESSONS["EXT_G5_FP_2017_005"] = lesson([
    B("The clock shows 11 o'clock in the morning. Then the hour hand, the short one, turns through 165 degrees. What time is it now?",
      W("l1", "Clock shows 11:00 a.m. Hour hand turns 165°.", tone="given", label=True),
      W("l2", "New time = ?", tone="given", label=True),
      FIG("f1", kind="clock", hour=11, minute=0, highlight=["hour"])),
    B("Here is the key fact. The hour hand goes right round the clock face, one full turn, in 12 hours. And a full turn is 360 degrees.",
      W("l3", "Hour hand: full turn = 360° in 12 hours", label=True)),
    B("So how far does the hour hand turn in just 1 hour?",
      ask=choose(["360 ÷ 60", "360 ÷ 12", "360 × 12"], 1,
                 "360 degrees are shared equally among 12 hours, so we divide 360 by 12. Dividing by 60 is for the minute hand.")),
    B("360 divided by 12 is 30. So every hour, the hour hand moves 30 degrees, from one number to the next.",
      W("l4", "360 ÷ 12 = 30")),
    B("Now, how many 30s are there in 165? 5 thirties make 150. That leaves 15 degrees over.",
      W("l5", "5 × 30 = 150"), W("l6", "165 − 150 = 15")),
    B("The 150 degrees are 5 whole hours. What about the 15 degrees left over?",
      ask=choose(["15 minutes", "half an hour", "a quarter of an hour"], 1,
                 "30 degrees is a whole hour, and 15 is half of 30. So it is half an hour. The trap is to read 15 degrees as 15 minutes.")),
    B("15 is half of 30, so it is half an hour, which is 30 minutes. Altogether the hand has moved for 5 hours and 30 minutes.",
      W("l7", "165 ÷ 30 = 5.5"), W("l8", "165° = 5 hours 30 minutes", label=True)),
    B("Now add that to 11 o'clock. 1 hour takes us to 12 noon, and 4 more hours take us to 4 in the afternoon.",
      W("l9", "11:00 a.m. + 5 hours = 4:00 p.m.", label=True)),
    B("Then the extra 30 minutes. The time is 4:30 in the afternoon.",
      W("l10", "Time = 4:30 p.m.", tone="answer", label=True), mark("l10", "4:30 p.m.", "circle"),
      FIG("f2", kind="clock", hour=4, minute=30, highlight=["hour"])),
    B("So remember: the hour hand turns 30 degrees every hour. Divide the turn by 30 for the hours, and change what is left over into minutes."),
], "authored")


# Square and equilateral triangle with the same perimeter; triangle side 8 cm.
LESSONS["EXT_G5_FP_2017_018"] = lesson([
    B("We have an equilateral triangle with a side of 8 centimetres. A square has the same perimeter as the triangle. How long is the side of the square?",
      W("l1", "Equilateral triangle: side 8 cm", tone="given", label=True),
      W("l2", "Square: same perimeter. Side = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="equilateral", sides={"bc": "8 cm"})),
    B("Equilateral means all 3 sides are equal. So every side of this triangle is 8 centimetres. Which sum gives the walk all the way round it?",
      FIG("f2", kind="triangle", shape="equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"}, highlight=["ab", "bc", "ca"]),
      ask=choose(["8 + 8", "8 × 8", "8 + 8 + 8"], 2,
                 "The walk goes along all 3 sides, so we add 8 three times. That is the same as 3 times 8.")),
    B("3 sides of 8 centimetres: 3 times 8 is 24. The triangle's perimeter is 24 centimetres.",
      W("l3", "Triangle perimeter = 3 × side", label=True), W("l4", "3 × 8 = 24")),
    B("The square has the same perimeter. So the walk round the square is 24 centimetres too.",
      FIG("f3", kind="rectangle", square=True, length="?", note="Perimeter = 24 cm")),
    B("A square has equal sides, and together they make 24. So how long is one side?",
      ask=choose(["24 ÷ 3", "24 ÷ 4", "24 × 4"], 1,
                 "A square has 4 sides, not 3. So the 24 centimetres are shared into 4 equal parts.")),
    B("24 shared among 4 equal sides: 24 divided by 4 is 6. The side of the square is 6 centimetres.",
      W("l5", "24 ÷ 4 = 6"), W("l6", "Side of square = 6 cm", tone="answer", label=True), mark("l6", "6 cm", "circle"),
      FIG("f4", kind="rectangle", square=True, length="6 cm", breadth="6 cm", highlight=["border"])),
    B("Check: 4 sides of 6 make 24, exactly the same walk as the triangle.",
      W("l7", "4 × 6 = 24")),
    B("Notice that the same perimeter does not mean the same side. The square has more sides to share the walk, so each one is shorter: 6, not 8."),
], "authored")
