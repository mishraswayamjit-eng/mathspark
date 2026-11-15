"""Geometry lessons written for one question each: the 2025 paper."""
from geometry_lib import (B, FIG, W, choose, lesson, mark, strike)
from geometry_rules import take_away_beats

LESSONS = {}


# Circle of area 616 sq. cm; its circumference equals the perimeter of a square. Area of the square?
LESSONS["EXT_G5_FP_2025_002"] = lesson([
    B("A circle has an area of 616 square centimetres. Its circumference is the same as the perimeter of a square. We want the area of that square.",
      W("l1", "Circle: area 616 sq. cm", tone="given", label=True),
      W("l2", "Square: perimeter = circumference. Area = ?", tone="given", label=True),
      FIG("f1", kind="circle", radius="r = ?", note="Area = 616 sq. cm")),
    B("It is a chain: the circle's area gives its radius, the radius gives the circumference, and that gives the square. The area of a circle is pi times the radius times the radius, and for pi we use 22 over 7.",
      W("l3", "Area of circle = π × r × r, with π = 22/7", label=True)),
    B("So 22 over 7, times r times r, is 616. To undo that, divide by 22 and multiply by 7. 616 divided by 22 is 28, and 28 times 7 is 196.",
      W("l4", "616 ÷ 22 = 28"), W("l5", "28 × 7 = 196"), W("l6", "r × r = 196", label=True)),
    B("r times r is 196. So what is r?",
      ask=choose(["98", "14", "49"], 1,
                 "We need a number that multiplies by itself to make 196, not half of 196. 14 times 14 is 196.")),
    B("14 times 14 is 196, so the radius is 14 centimetres.",
      W("l7", "14 × 14 = 196"), FIG("f2", kind="circle", radius="14 cm")),
    B("Now the circumference, the walk round the circle: 2 times pi times the radius. 14 divided by 7 is 2, so it is 2 times 22 times 2, which is 88 centimetres.",
      W("l8", "Circumference = 2 × π × r", label=True), W("l9", "2 × 22/7 × 14 = 88")),
    B("The square's perimeter is the same: 88 centimetres. How do we get one side of the square?",
      ask=choose(["88 ÷ 2", "88 × 4", "88 ÷ 4"], 2,
                 "A square has 4 equal sides, and together they make 88. So one side is 88 shared into 4 equal parts.")),
    B("88 divided by 4 is 22. Each side of the square is 22 centimetres.",
      W("l10", "88 ÷ 4 = 22"),
      FIG("f3", kind="rectangle", square=True, length="22 cm", breadth="22 cm", inside="Area = ?")),
    B("Last step: the square's area, side times side. 22 times 20 is 440, and 22 times 2 is 44. Together that makes 484.",
      W("l11", "22 × 20 = 440"), W("l12", "440 + 44 = 484"), W("l13", "22 × 22 = 484")),
    B("So the area of the square is 484 square centimetres.",
      W("l14", "Area of square = 484 sq. cm", tone="answer", label=True), mark("l14", "484 sq. cm", "circle"),
      FIG("f4", kind="rectangle", square=True, length="22 cm", breadth="22 cm", inside="484 sq. cm", highlight=["fill"])),
    B("A long chain, but each link is small: area to radius, radius to circumference, circumference to side, side to area. Write each link down before starting the next."),
], "authored")


# Angle between the hands at 9:33.
LESSONS["EXT_G5_FP_2025_011"] = lesson([
    B("The clock shows 9:33. We want the angle between the hour hand and the minute hand.",
      W("l1", "Clock at 9:33. Angle between the hands = ?", tone="given", label=True),
      FIG("f1", kind="clock", hour=9, minute=33, showAngle=True)),
    B("We measure how far each hand has turned from the 12 at the top, one hand at a time. The whole clock face is a full turn, 360 degrees.",
      W("l2", "Clock face: 360°, 12 hours, 60 minutes", label=True)),
    B("The minute hand first. It goes all the way round, 360 degrees, in 60 minutes, so it turns 6 degrees every minute.",
      W("l3", "360 ÷ 60 = 6"), FIG("f2", kind="clock", hour=9, minute=33, highlight=["minute"])),
    B("At 33 minutes it has turned 33 times 6. 30 times 6 is 180, and 3 times 6 is 18. Together, 198 degrees.",
      W("l4", "30 × 6 = 180"), W("l5", "180 + 18 = 198"), W("l6", "33 × 6 = 198")),
    B("Now the hour hand. At 9:33, where exactly is it pointing?",
      ask=choose(["exactly at the 9", "just past halfway from 9 to 10", "exactly at the 10"], 1,
                 "The hour hand never stops. 33 minutes is a little more than half an hour, so the hand is a little more than halfway from the 9 to the 10.")),
    B("Take the 9 first. Each hour is 360 divided by 12, which is 30 degrees. So from the 12 round to the 9 is 9 times 30, which is 270 degrees.",
      W("l7", "360 ÷ 12 = 30"), W("l8", "9 × 30 = 270")),
    B("Now the creep. The hour hand moves 30 degrees in 60 minutes, so half a degree each minute. In 33 minutes that is half of 33, which is 16.5 degrees.",
      W("l9", "33 × ½ = 16.5"), FIG("f3", kind="clock", hour=9, minute=33, highlight=["hour"])),
    B("So the hour hand is at 270 plus 16.5, which is 286.5 degrees.",
      W("l10", "270 + 16.5 = 286.5")),
    B("The hour hand is at 286.5 degrees and the minute hand is at 198 degrees. How do we get the angle between them?",
      ask=choose(["286.5 − 198", "286.5 + 198", "270 − 198"], 0,
                 "The angle between the hands is the gap between their two positions, so we subtract. And we use 286.5, not 270, because the hour hand has moved past the 9.")),
    B("To take away 198, take away 200 and then give 2 back. 286.5 take away 200 is 86.5, and 2 more makes 88.5.",
      W("l11", "286.5 − 200 = 86.5"), W("l12", "86.5 + 2 = 88.5"), W("l13", "286.5 − 198 = 88.5")),
    B("The angle between the hands is 88.5 degrees.",
      W("l14", "Angle = 88.5°", tone="answer", label=True), mark("l14", "88.5°", "circle"),
      FIG("f4", kind="clock", hour=9, minute=33, showAngle=True, highlight=["angle"])),
    B("So work the two hands separately: 6 degrees a minute for the minute hand, and 30 degrees an hour plus half a degree a minute for the hour hand. Then subtract."),
], "authored")


# Rectangle of area 468 cm² and breadth 18 cm. Perimeter?
LESSONS["EXT_G5_FP_2025_012"] = lesson([
    B("A rectangle has an area of 468 square centimetres, and its breadth is 18 centimetres. We want its perimeter.",
      W("l1", "Rectangle: area 468 cm², breadth 18 cm", tone="given", label=True),
      W("l2", "Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="?", breadth="18 cm", inside="468 cm²")),
    B("For the perimeter we need both sides, and we only have the breadth. The area will give us the length. How?",
      ask=choose(["468 − 18", "468 × 18", "468 ÷ 18"], 2,
                 "Area is length times breadth. So to get back from the area to the length, we divide by the breadth.")),
    B("We need 468 divided by 18: how many 18s make 468? Start with a big chunk. 20 lots of 18 make 360. That leaves 468 take away 360, which is 108.",
      W("l3", "Length = area ÷ breadth", label=True), W("l4", "18 × 20 = 360"), W("l5", "468 − 360 = 108")),
    B("And 6 lots of 18 make 108. So altogether that is 20 lots and 6 lots: 26. The length is 26 centimetres.",
      W("l6", "18 × 6 = 108"), W("l7", "468 ÷ 18 = 26"),
      FIG("f2", kind="rectangle", length="26 cm", breadth="18 cm", proportion=1.4)),
    B("Now the perimeter, the walk all the way round. Which sum gives it?",
      ask=choose(["26 + 18", "2 × (26 + 18)", "26 × 18"], 1,
                 "26 plus 18 is only one length and one breadth, which is halfway round. We double it for the whole walk.")),
    B("26 plus 18 is 44, and that is halfway. Double it: 2 times 44 is 88.",
      W("l8", "Perimeter = 2 × (length + breadth)", label=True), W("l9", "26 + 18 = 44"), W("l10", "2 × 44 = 88")),
    B("So the perimeter is 88 centimetres.",
      W("l11", "Perimeter = 88 cm", tone="answer", label=True), mark("l11", "88 cm", "circle"),
      FIG("f3", kind="rectangle", length="26 cm", breadth="18 cm", proportion=1.4, highlight=["border"], note="Perimeter = 88 cm")),
    B("Check the length by multiplying back: 26 times 18 is 468, the area we were given.",
      W("l12", "26 × 18 = 468")),
    B("So: divide the area by the side you know to find the other side, then add the two sides and double."),
], "authored")


# Sum of the supplementary and the complementary angle of 58°.
_comp_2025_029 = take_away_beats(90, 58, "l4")
_supp_2025_029 = take_away_beats(180, 58, "l6")
LESSONS["EXT_G5_FP_2025_029"] = lesson([
    B("Our angle is 58 degrees. It has two partners: a complementary angle and a supplementary angle. We want the two partners added together.",
      W("l1", "Angle: 58°", tone="given", label=True),
      W("l2", "Supplementary angle + complementary angle = ?", tone="given", label=True),
      FIG("f1", kind="angles", layout="single", parts=[{"label": "58°", "size": 58}])),
    B("Take the complementary angle first. It fits with 58 degrees inside a square corner, a right angle. So what do the two of them make together?",
      FIG("f2", kind="angles", layout="inRightAngle", parts=[{"label": "58°", "size": 58}, {"label": "?"}]),
      ask=choose(["180°", "90°", "360°"], 1,
                 "A right angle is a quarter turn, and a quarter turn is 90 degrees. 180 is for a straight line, which comes next.")),
    B("A right angle is 90 degrees. So the complementary angle is 90 take away 58.",
      W("l3", "complement = 90° − angle", label=True)),
] + _comp_2025_029 + [
    B("Now the supplementary angle. It fits with 58 degrees on a straight line, and a straight line is a half turn: 180 degrees. So it is 180 take away 58.",
      W("l5", "supplement = 180° − angle", label=True),
      FIG("f3", kind="angles", layout="onLine", parts=[{"label": "58°", "size": 58}, {"label": "?"}])),
] + _supp_2025_029 + [
    B("The complement is 32 degrees and the supplement is 122 degrees. What does the question want us to do with them?",
      ask=choose(["122 − 32", "32 + 122", "90 + 180"], 1,
                 "The question asks for the sum, and sum means add. So we add the two partner angles: 32 and 122.")),
    B("32 plus 122 is 154. The sum is 154 degrees.",
      W("l7", "32 + 122 = 154"), W("l8", "Sum = 154°", tone="answer", label=True), mark("l8", "154°", "circle")),
    B("So: complement from 90, supplement from 180, and then read the question again to see what it wants. Here it wanted the two added together."),
], "authored")


# Square of area 196 sq. cm; rectangle with 4 times the area. Which sides?
LESSONS["EXT_G5_FP_2025_034"] = lesson([
    B("Square P Q R S has an area of 196 square centimetres. Rectangle A B C D has an area 4 times as big. We have to pick the sides the rectangle could have.",
      W("l1", "Square PQRS: area 196 sq. cm", tone="given", label=True),
      W("l2", "Rectangle ABCD: 4 times the area. Sides = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", square=True, inside="196 sq. cm")),
    B("First, the rectangle's area. Which sum gives it?",
      ask=choose(["196 + 4", "196 ÷ 4", "4 × 196"], 2,
                 "4 times as big means multiply by 4. Adding 4 would only make it 4 square centimetres bigger.")),
    B("4 times 196. 196 is 4 less than 200, so do 4 times 200, which is 800, and take away 4 times 4, which is 16. That leaves 784.",
      W("l3", "4 × 200 = 800"), W("l4", "800 − 16 = 784"), W("l5", "4 × 196 = 784")),
    B("So the two sides of the rectangle must multiply to make 784. Here is a quick test: 784 ends in a 4, so the last digits of the two sides must multiply to give something ending in 4.",
      W("l6", "length × breadth = 784", label=True), mark("l6", "784", "box")),
    B("Try 52 and 18. 2 times 8 is 16, which ends in 6. Out. Try 28 and 36. 8 times 6 is 48, which ends in 8. Out as well.",
      W("l7", "52 × 18: 2 × 8 = 16, ends in 6", label=True), strike("l7", "52 × 18"),
      W("l8", "28 × 36: 8 × 6 = 48, ends in 8", label=True), strike("l8", "28 × 36")),
    B("That leaves 44 and 16, and 56 and 14. Work out the first. 44 times 10 is 440, and 44 times 6 is 264. Together 704. Not 784.",
      W("l8b", "Still possible: 44 and 16, 56 and 14", label=True),
      W("l9", "44 × 10 = 440"), W("l10", "44 × 6 = 264"), W("l11", "440 + 264 = 704")),
    B("Now 56 and 14. 56 times 10 is 560, and 56 times 4 is 224. Together 784. That is the one.",
      W("l12", "56 × 10 = 560"), W("l13", "56 × 4 = 224"), W("l14", "560 + 224 = 784"), mark("l14", "784", "circle")),
    B("So the sides of the rectangle can be 56 centimetres and 14 centimetres.",
      W("l15", "Sides: 56 cm and 14 cm", tone="answer", label=True), mark("l15", "56 cm and 14 cm", "circle")),
    B("And here is why it works so neatly. 14 times 14 is 196, so the square's side is 14. Put 4 of those squares in a row, and you get a rectangle 56 long and 14 tall.",
      W("l16", "14 × 14 = 196"), W("l17", "4 × 14 = 56"),
      FIG("f2", kind="rectangle", length="56 cm", breadth="14 cm", proportion=3, grid={"cols": 4, "rows": 1})),
    B("So: find the area you need, then test the pairs. Checking the last digit first saves a lot of multiplying."),
], "authored")
