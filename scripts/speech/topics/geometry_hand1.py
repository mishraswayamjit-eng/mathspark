"""Hand-written narration, geometry past papers 2016 to 2018.

The variable a is written as a capital A so the voice says the letter, not the word "a".
L and B in the printed working are said as "length" and "breadth".
"""


def E(q, options, hints, steps):
    hints = list(hints) + [""] * (3 - len(hints))
    return {"q": q, "options": list(options), "hints": hints, "steps": list(steps)}


def units(word, *numbers):
    return ["%s %s" % (n, word) for n in numbers]


HAND = {}

HAND["EXT_G5_FP_2016_015"] = E(
    "The length of one side of the rectangle is 8 centimetres, and its perimeter is 40 centimetres. Find the area of the rectangle.",
    ["160 square centimetres", "96 square centimetres", "144 square centimetres", "Data inadequate"],
    ["Perimeter equals 2 times, length plus breadth. Half of 40 gives length plus breadth. Then find the other side.",
     "Length plus breadth equals perimeter divided by 2. Area equals length times breadth."],
    ["Length plus breadth equals 40 divided by 2, which is 20.",
     "The other side equals 20 minus 8, which is 12 centimetres.",
     "Area equals 8 times 12, which is 96 square centimetres."],
)

HAND["EXT_G5_FP_2016_037"] = E(
    "Three times the measure of an angle is the measure of its supplement. What is the measure of the angle?",
    units("degrees", 30, 20, 60, 45),
    ["The supplement of an angle x is 180 degrees minus x. Write, three times the angle equals its supplement, as a balance.",
     "Supplementary angles add up to 180 degrees. Here, 3 x equals 180 degrees minus x."],
    ["Let the angle be x. Its supplement equals 180 degrees minus x.",
     "3 x equals 180 degrees minus x. So 4 x equals 180 degrees.",
     "x equals 180 degrees divided by 4, which is 45 degrees. Check: 3 times 45 is 135, and 180 minus 45 is 135. They match."],
)

HAND["EXT_G5_FP_2016_038"] = E(
    "The three sides of a triangle are: 2 A plus 6, centimetres; 3 A plus 5, centimetres; and A plus 7, centimetres. "
    "What is the perimeter of the triangle, if the value of A equals 3?",
    units("centimetres", 26, 28, 36, 34),
    ["Put A equals 3 into each side, to get three lengths. Perimeter means add all three sides.",
     "The perimeter of a triangle equals the sum of its three sides."],
    ["2 A plus 6 equals 2 times 3, plus 6, which is 12 centimetres.",
     "3 A plus 5 equals 3 times 3, plus 5, which is 14 centimetres.",
     "A plus 7 equals 3 plus 7, which is 10 centimetres.",
     "Perimeter equals 12 plus 14 plus 10, which is 36 centimetres."],
)

HAND["EXT_G5_FP_2017_005"] = E(
    "A clock is showing 11:00 A M now. When the hour hand has turned through 165 degrees, what will be the time?",
    ["2:05 p m", "4 30 p m", "12 30 p m", "5 30 p m"],
    ["The hour hand turns 30 degrees in every hour. How many hours is 165 degrees?",
     "Hour hand: 30 degrees per hour. Hours passed equals the angle divided by 30."],
    ["165 divided by 30 equals 5.5 hours, which is 5 hours 30 minutes.",
     "11:00 A M, plus 5 hours 30 minutes, is 4 30 p m."],
)

HAND["EXT_G5_FP_2017_018"] = E(
    "The perimeter of a square and an equilateral triangle are the same. "
    "If the side of the triangle is 8 centimetres, then the side of the square is:",
    units("centimetres", 8, 24, 6, 12),
    ["Find the triangle's perimeter. It has 3 equal sides. Share that perimeter equally among the 4 sides of the square.",
     "Equilateral triangle: perimeter equals 3 times side. Square: perimeter equals 4 times side."],
    ["Triangle perimeter equals 3 times 8, which is 24 centimetres.",
     "Square perimeter equals 24 centimetres. So the side equals 24 divided by 4, which is 6 centimetres."],
)

HAND["EXT_G5_FP_2017_019"] = E(
    "The breadth of a rectangle is half the length of the rectangle. "
    "If the perimeter of the rectangle is 48 centimetres, then its area is:",
    units("square centimetres", 288, 128, 256, 196),
    ["If the breadth is 1 part, the length is 2 parts. Perimeter equals 2 times, length plus breadth, which is 2 times 3 parts. Find one part first.",
     "Perimeter equals 2 times, length plus breadth. Area equals length times breadth."],
    ["Length plus breadth equals 48 divided by 2, which is 24. The length is 2 times the breadth, so 3 times the breadth equals 24. "
     "So the breadth is 8 centimetres, and the length is 16 centimetres.",
     "Area equals 16 times 8, which is 128 square centimetres."],
)

HAND["EXT_G5_FP_2017_023"] = E(
    "A man is cycling towards the North-East direction. He turns to his left, and is now cycling towards West direction. "
    "How many degrees to his left did he turn?",
    units("degrees", 90, 145, 135, 180),
    ["Turning left means anti-clockwise. Go from North-East to North, then North-West, then West, counting 45 degrees each step.",
     "Each step between neighbouring directions, North, North-East, East and so on, is 45 degrees."],
    ["North-East to North is 45 degrees, to the left.",
     "North to North-West is another 45 degrees. The total is 90 degrees.",
     "North-West to West is another 45 degrees. The total is 135 degrees."],
)

HAND["EXT_G5_FP_2017_030"] = E(
    "The length of a rectangle is 4 A plus 3 b, and the breadth is 3 A minus b. Find its perimeter.",
    ["7 A plus 2 b", "14 A plus 4 b", "14 A minus 2 b", "None of these"],
    ["First add the length and breadth, combining like terms. Then multiply by 2.",
     "Perimeter equals 2 times, length plus breadth."],
    ["Length plus breadth equals 4 A plus 3 b, plus 3 A minus b, which is 7 A plus 2 b.",
     "Perimeter equals 2 times, 7 A plus 2 b, which is 14 A plus 4 b."],
)

HAND["EXT_G5_FP_2017_040"] = E(
    "The perimeter of a square ground is 120 metres. What is its area?",
    units("square metres", 900, 600, 300, 360),
    ["Find one side first: perimeter divided by 4. Then area equals side times side.",
     "For a square, perimeter equals 4 times side, and area equals side times side."],
    ["Side equals 120 divided by 4, which is 30 metres.",
     "Area equals 30 times 30, which is 900 square metres."],
)

HAND["EXT_G5_FP_2018_001"] = E(
    "If 1 gram of grass seeds is needed to plant 1 square metre, how much grass seed will be needed "
    "to plant an entire field that is 110 metres long and 70 metres wide?",
    units("kilograms", 77, 15, 7.7, 37.5),
    ["Find the area of the field first: length times width. Each square metre needs 1 gram. "
     "Then change grams into kilograms, by dividing by 1000.",
     "Area of a rectangle equals length times breadth. 1000 grams equals 1 kilogram."],
    ["Area equals 110 times 70, which is 7700 square metres.",
     "Grass seed equals 7700 times 1 gram, which is 7700 grams.",
     "7700 grams divided by 1000 equals 7.7 kilograms."],
)

HAND["EXT_G5_FP_2018_007"] = E(
    "Which of the following statements is true?",
    ["The supplementary angle of an angle is always less than 90 degrees.",
     "The complementary angle of an acute angle is always an acute angle.",
     "The complementary and the supplementary angle of a given angle always sum up to 360 degrees.",
     "All the given statements are false."],
    ["Test each statement with an example angle, like 30 degrees. "
     "The complement equals 90 degrees minus the angle, and the supplement equals 180 degrees minus the angle.",
     "An acute angle is less than 90 degrees. The complement equals 90 degrees minus x. The supplement equals 180 degrees minus x."],
    ["Statement A: the supplement of 30 degrees is 150 degrees, which is more than 90 degrees. So A is not true.",
     "Statement B: if x is acute, between 0 degrees and 90 degrees, then 90 degrees minus x is also between 0 degrees and 90 degrees. "
     "So it is acute, and B is true.",
     "Statement C: 90 minus x, plus 180 minus x, equals 270 minus 2 x, which isn't always 360 degrees. So C is not true.",
     "Answer: statement B."],
)

HAND["EXT_G5_FP_2018_009"] = E(
    "The perimeter of a rectangle is 72 centimetres. The length and breadth of the rectangle are:",
    ["9 and 4", "14 and 4", "19 and 15", "21 and 15"],
    ["Perimeter equals 2 times, length plus breadth. So length plus breadth must be half of 72. Add the two numbers in each option.",
     "Length plus breadth equals perimeter divided by 2."],
    ["Length plus breadth equals 72 divided by 2, which is 36.",
     "9 plus 4 is 13, not a match. 14 plus 4 is 18, not a match. 19 plus 15 is 34, not a match.",
     "21 plus 15 is 36. That matches."],
)

HAND["EXT_G5_FP_2018_014"] = E(
    "The measure of an angle is 38 minus x, degrees. What will be the measure of the complementary angle of it?",
    ["72 minus x, degrees", "62 minus x, degrees", "52 minus x, degrees", "52 plus x, degrees"],
    ["Complementary angles add to 90 degrees. Subtract the angle from 90, and be careful with the minus sign in front of x.",
     "The complement equals 90 degrees minus the angle."],
    ["The complement equals 90 minus, open bracket, 38 minus x, close bracket.",
     "Remove the bracket: 90 minus 38 plus x. Minus times minus gives plus.",
     "That equals 52 plus x, degrees."],
)

HAND["EXT_G5_FP_2018_018"] = E(
    "The two sides of a square are 3 A minus 7, centimetres, and 2 A minus 1, centimetres. "
    "Which of the following can be its perimeter?",
    units("centimetres", 21, 28, 44, 42),
    ["All sides of a square are equal, so 3 A minus 7 equals 2 A minus 1. Solve for A, then find the side and the perimeter.",
     "In a square, all sides are equal. Perimeter equals 4 times side."],
    ["3 A minus 7 equals 2 A minus 1. So A equals 6.",
     "Side equals 3 times 6, minus 7, which is 11 centimetres. Check: 2 times 6, minus 1, is 11. It matches.",
     "Perimeter equals 4 times 11, which is 44 centimetres."],
)

HAND["EXT_G5_FP_2018_029"] = E(
    "The perimeter of an equilateral triangle is 16 A plus 7 b. If A equals 2 and b equals 4, then the side of the triangle is?",
    ["30", "20", "15", "None of these"],
    ["Put A equals 2 and b equals 4 into the perimeter. An equilateral triangle has 3 equal sides.",
     "The side of an equilateral triangle equals perimeter divided by 3."],
    ["Perimeter equals 16 times 2, plus 7 times 4. That is 32 plus 28, which is 60.",
     "Side equals 60 divided by 3, which is 20."],
)
