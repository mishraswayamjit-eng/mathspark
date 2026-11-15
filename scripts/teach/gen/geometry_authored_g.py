"""Geometry lessons written for one question each: the 2023 paper."""
from geometry_lib import (B, FIG, W, choose, lesson, mark, strike)
from geometry_rules import times_beats

LESSONS = {}


# Square with the same perimeter as a 22 m by 16 m rectangle. Area of the square?
_area_2023_004 = times_beats(19, 19, "l8")
LESSONS["EXT_G5_FP_2023_004"] = lesson([
    B("A rectangle is 22 metres long and 16 metres wide. A square has the same perimeter as this rectangle. We want the area of the square.",
      W("l1", "Rectangle: length 22 m, breadth 16 m", tone="given", label=True),
      W("l2", "Square: same perimeter. Area of square = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="22 m", breadth="16 m", proportion=1.4)),
    B("Start with the rectangle's perimeter, the walk all the way round it. Which sum gives it?",
      ask=choose(["22 + 16", "2 × (22 + 16)", "22 × 16"], 1,
                 "22 plus 16 is only one length and one breadth, which is halfway round. We double it for the whole walk.")),
    B("22 plus 16 is 38, and that is halfway. Double it: 2 times 38 is 76. The rectangle's perimeter is 76 metres.",
      W("l3", "22 + 16 = 38"), W("l4", "2 × 38 = 76")),
    B("The square has the same walk round, 76 metres, shared among 4 equal sides. To divide by 4, halve and halve again. Half of 76 is 38, and half of 38 is 19.",
      W("l5", "76 ÷ 2 = 38"), W("l6", "38 ÷ 2 = 19"),
      FIG("f2", kind="rectangle", square=True, length="19 m", breadth="19 m", inside="Area = ?")),
    B("So each side of the square is 19 metres. Now, which sum gives the square's area?",
      ask=choose(["19 × 4", "22 × 16", "19 × 19"], 2,
                 "The square shares the rectangle's perimeter, not its area. Its own area is its side times its side.")),
    B("The area of a square is side times side.",
      W("l7", "Area of square = side × side", label=True)),
] + _area_2023_004 + [
    B("So the area is 361 square metres. Now look at the choices: 324, 400 and 484. Our 361 is not among them.",
      W("l9", "Choices: 324, 400, 484 sq. m", label=True)),
    B("When your answer is not on the list, check the working before you decide. 4 times 19 is 76, so the side is right. So the answer is: none of these.",
      W("l10", "4 × 19 = 76"), W("l11", "361 sq. m: none of these", tone="answer", label=True),
      mark("l11", "none of these", "circle"),
      FIG("f3", kind="rectangle", square=True, length="19 m", breadth="19 m", inside="361 sq. m", highlight=["fill"])),
    B("So: perimeter of the rectangle, then the side of the square, then its area. And trust careful working, even when the list of choices does not have it."),
], "authored")


# Clock shows 12:45 pm; the hour hand turns through 214°. New time?
LESSONS["EXT_G5_FP_2023_010"] = lesson([
    B("The clock shows 12:45 in the afternoon. Then the hour hand, the short one, turns through 214 degrees. What time is it now?",
      W("l1", "Clock shows 12:45 p.m. Hour hand turns 214°.", tone="given", label=True),
      W("l2", "New time = ?", tone="given", label=True),
      FIG("f1", kind="clock", hour=12, minute=45, highlight=["hour"])),
    B("The hour hand goes once round the clock, a full turn of 360 degrees, in 12 hours. 360 divided by 12 is 30. So it turns 30 degrees every hour.",
      W("l3", "Hour hand: full turn = 360° in 12 hours", label=True), W("l4", "360 ÷ 12 = 30")),
    B("An hour is 60 minutes, and in that time the hour hand moves 30 degrees. So how far does it move in 1 minute?",
      W("l5", "1 hour = 60 minutes", label=True),
      ask=choose(["6 degrees", "2 degrees", "half a degree"], 2,
                 "30 degrees are spread over 60 minutes. 30 is half of 60, so each minute gets half a degree. 6 degrees a minute is the speed of the minute hand.")),
    B("It moves half a degree a minute. Put the other way round: each whole degree takes the hour hand 2 minutes.",
      W("l6", "Hour hand: 30° an hour, 1° every 2 minutes", label=True)),
    B("Now, how many whole hours are in 214 degrees? 7 thirties make 210. That leaves 4 degrees over.",
      W("l7", "7 × 30 = 210"), W("l8", "214 − 210 = 4")),
    B("The 210 degrees are 7 whole hours. How long do the last 4 degrees take?",
      ask=choose(["4 minutes", "8 minutes", "2 minutes"], 1,
                 "Each degree takes the hour hand 2 minutes. So 4 degrees take 4 times 2 minutes.")),
    B("4 degrees, at 2 minutes each, is 8 minutes. So the hand has been moving for 7 hours and 8 minutes.",
      W("l9", "4 × 2 = 8"), W("l10", "214° = 7 hours 8 minutes", label=True)),
    B("Add the 7 hours first. 7 hours after 12:45 is 7:45 in the evening.",
      W("l11", "12:45 p.m. + 7 hours = 7:45 p.m.", label=True)),
    B("Then the 8 minutes. 45 plus 8 is 53. The time is 7:53 in the evening.",
      W("l12", "45 + 8 = 53"), W("l13", "Time = 7:53 p.m.", tone="answer", label=True), mark("l13", "7:53 p.m.", "circle"),
      FIG("f2", kind="clock", hour=7, minute=53, highlight=["hour"])),
    B("So for the hour hand: 30 degrees is an hour, and each leftover degree is 2 minutes. Find the hours, then the minutes, then add them to the starting time."),
], "authored")


# Area of a right-angled triangle equals 18 times its base. Height?
LESSONS["EXT_G5_FP_2023_017"] = lesson([
    B("Here is a right-angled triangle. We are not told its base or its height. We only know that its area is 18 times its base. We want the height.",
      W("l1", "Right-angled triangle: area = 18 × base", tone="given", label=True),
      W("l2", "Height = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="right", sides={"ab": "height = ?", "bc": "base"})),
    B("We do know the rule for the area of any triangle: half of base times height. It is half of the rectangle drawn around it.",
      W("l3", "Area = ½ × base × height", label=True),
      FIG("f2", kind="triangle", shape="right", sides={"ab": "height = ?", "bc": "base"}, enclose=True)),
    B("So now we have the same area written in two ways. They must be equal.",
      W("l4", "½ × base × height = 18 × base", label=True)),
    B("Look at both sides. Each one is something, times the base. What does that tell us?",
      ask=choose(["height = 18", "½ × height = 18", "base = 18"], 1,
                 "Both sides are something times the base. For them to be equal, the somethings must be equal: half of the height on the left, and 18 on the right.")),
    B("The times base is on both sides, so we can cancel it from both. What is left is: half of the height equals 18.",
      strike("l4", "× base", nth=1), strike("l4", "× base", nth=2), W("l5", "½ × height = 18", label=True)),
    B("Half of the height is 18. So how do we get the whole height?",
      ask=choose(["18 ÷ 2", "18 × 2", "18 + 2"], 1,
                 "If half of something is 18, the whole thing is twice as much. So we double 18.")),
    B("Double 18 is 36. So the height is 36 units.",
      W("l6", "18 × 2 = 36"), W("l7", "Height = 36 units", tone="answer", label=True), mark("l7", "36 units", "circle"),
      FIG("f3", kind="triangle", shape="right", sides={"ab": "36", "bc": "base"}, highlight=["ab"])),
    B("Let's test it with a base of 10. Half of 10 times 36 is 180. And 18 times 10 is 180 too. It works.",
      W("l8", "½ × 10 × 36 = 180"), W("l9", "18 × 10 = 180")),
    B("So when the same thing multiplies both sides, cancel it. The trap here is to halve 18. Half of the height is 18, so the height itself is double."),
], "authored")


# Two sides of a triangle are 16 cm and 7 cm. A possible perimeter?
LESSONS["EXT_G5_FP_2023_039"] = lesson([
    B("Two sides of a triangle are 16 centimetres and 7 centimetres. We do not know the third side, but we have to say what the perimeter could be.",
      W("l1", "Triangle: two sides 16 cm and 7 cm", tone="given", label=True),
      W("l2", "Possible perimeter = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="scalene", sides={"bc": "16 cm", "ab": "7 cm", "ca": "?"})),
    B("The third side cannot be just anything. Picture the 7 side as a door, hinged to one end of the 16 side. Swing it wide open, flat, and the far ends are 16 plus 7 apart: 23.",
      W("l3", "16 + 7 = 23")),
    B("Swing the door shut, flat against the 16 side, and the gap between the far ends is 16 take away 7: 9.",
      W("l4", "16 − 7 = 9")),
    B("Can the third side be exactly 23, or exactly 9?",
      ask=choose(["Yes, both are fine", "No: the triangle would be flat"], 1,
                 "At exactly 23 or exactly 9 the door lies flat along the line, and there is no triangle left. The third side has to be in between.")),
    B("So the third side is more than 9 and less than 23. That is true for every triangle: more than the difference of the other two sides, less than their sum.",
      W("l5", "third side: between 9 and 23", label=True)),
    B("Now the perimeter. The two known sides make 23. Add the smallest and the largest third side: 23 plus 9 is 32, and 23 plus 23 is 46.",
      W("l6", "23 + 9 = 32"), W("l7", "23 + 23 = 46"), W("l8", "perimeter: between 32 and 46", label=True)),
    B("The choices are 34, 31 and 46. Which one lies between 32 and 46?",
      W("l9", "Choices: 34, 31, 46", label=True),
      ask=choose(["31", "34", "46"], 1,
                 "31 is below 32. And 46 is the flat edge itself, which is not allowed. Only 34 lies properly in between.")),
    B("34 is between 32 and 46. It gives a third side of 34 take away 23, which is 11, safely between 9 and 23.",
      W("l10", "32 < 34 < 46"), W("l11", "34 − 23 = 11"),
      FIG("f2", kind="triangle", shape="scalene", sides={"bc": "16 cm", "ab": "7 cm", "ca": "11 cm"}, highlight=["ca"])),
    B("So a possible perimeter is 34 centimetres.",
      W("l12", "Possible perimeter = 34 cm", tone="answer", label=True), mark("l12", "34 cm", "circle")),
    B("Remember the door. The third side of a triangle is always less than the sum of the other two, and more than their difference."),
], "authored")


# Which two angles are supplementary?
LESSONS["EXT_G5_FP_2023_040"] = lesson([
    B("We are given 4 pairs of angles, all with decimals. We have to find the pair that is supplementary.",
      W("l1", "Which two angles are supplementary?", tone="given", label=True),
      FIG("f1", kind="angles", layout="onLine", parts=[{"label": "angle"}, {"label": "partner"}])),
    B("Supplementary angles fit together on a straight line, like this. So what must the pair add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "A straight line is a half turn, and a half turn is 180 degrees. 90 is for a square corner.")),
    B("The pair must make exactly 180 degrees. So we add each pair. Here is a tip: look at the decimal parts first.",
      W("l2", "Supplementary: the pair adds up to 180°", label=True), mark("l2", "180°", "box")),
    B("First pair: 127.5 and 53.5. The two point 5s make 1 whole, and the total comes to 181. One too many.",
      W("l3", "127.5 + 53.5 = 181")),
    B("Second pair: 83.6 and 95.4. Point 6 and point 4 make 1 whole, and the total is 179. One short.",
      W("l4", "83.6 + 95.4 = 179")),
    B("Third pair: 111.8 and 68.2. Point 8 and point 2 make 1 whole, and this time the total is exactly 180.",
      W("l5", "111.8 + 68.2 = 180"), mark("l5", "180", "circle")),
    B("Check the last pair too: 115.7 and 65.3 make 181. So only one pair works.",
      W("l6", "115.7 + 65.3 = 181")),
    B("The supplementary pair is 111.8 degrees and 68.2 degrees.",
      W("l7", "111.8° and 68.2°", tone="answer", label=True), mark("l7", "111.8° and 68.2°", "circle"),
      FIG("f2", kind="angles", layout="onLine", parts=[{"label": "111.8°", "size": 111.8}, {"label": "68.2°", "size": 68.2}])),
    B("Notice how close the other pairs came: 179 and 181. Supplementary means exactly 180, so add carefully, decimals and all."),
], "authored")
