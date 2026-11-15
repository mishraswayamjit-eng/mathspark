"""Hand-written narration, geometry past papers 2023 to 2025 and the three source worksheets."""
from geometry_hand1 import E, units

HAND = {}

HAND["EXT_G5_FP_2023_004"] = E(
    "The perimeter of a square is equal to the perimeter of a rectangle with length 22 metres and breadth 16 metres. "
    "Find the area of the square.",
    ["324 square metres", "400 square metres", "484 square metres", "none of these"],
    ["Find the rectangle's perimeter first: 2 times, length plus breadth. The square has the same perimeter, so divide by 4 to get its side.",
     "For a square, perimeter equals 4 times side, and area equals side times side."],
    ["Rectangle perimeter: 2 times, 22 plus 16, which is 76 metres.",
     "The square has the same perimeter, so its side is 76 divided by 4, which is 19 metres.",
     "Area of the square: 19 times 19, which is 361 square metres.",
     "361 square metres is not one of the choices given, so the answer is, none of these."],
)

HAND["EXT_G5_FP_2023_010"] = E(
    "A clock is showing 12 45 p m now. When the hour hand has turned through 214 degrees, what will the time be?",
    ["8:07 p m", "7 28 p m", "8 13 p m", "7 53 p m"],
    ["The hour hand turns 30 degrees each hour. How many hours and minutes is 214 degrees? "
     "It turns 0.5 degrees each minute. Then add to 12 45.",
     "Hour hand: 30 degrees per hour, which is half a degree per minute."],
    ["214 degrees divided by 30 degrees equals 7 hours, with 4 degrees left over.",
     "4 degrees divided by half a degree equals 8 minutes. So that is 7 hours 8 minutes.",
     "12 45 p m, plus 7 hours 8 minutes, is 7 53 p m."],
)

HAND["EXT_G5_FP_2023_017"] = E(
    "The area of a right-angled triangle is equal to 18 times the base of the same triangle, numerically. Find the height of the triangle.",
    units("units", 54, 9, 36, 27),
    ["Write area equals half of base times height, and set it equal to 18 times base. The base appears on both sides!",
     "Area of a triangle equals half of base times height."],
    ["Half of base times height equals 18 times base.",
     "Cancel the base from both sides: half of the height equals 18.",
     "Height equals 18 times 2, which is 36 units."],
)

HAND["EXT_G5_FP_2023_039"] = E(
    "The two sides of a triangle are 16 centimetres and 7 centimetres. Which of the following can be the possible perimeter of this triangle?",
    ["none of these", "34 centimetres", "31 centimetres", "46 centimetres"],
    ["In any triangle, the third side must be more than the difference of the other two, and less than their sum. "
     "Find that range for the third side, then the range of the perimeter.",
     "Triangle rule: the difference of two sides is less than the third side, and the third side is less than the sum of two sides."],
    ["The third side is between 16 minus 7, which is 9, and 16 plus 7, which is 23. It is not equal to either.",
     "The perimeter is between 16 plus 7 plus 9, which is 32, and 16 plus 7 plus 23, which is 46. But it is not equal to 32 or 46.",
     "31 does not work. 46 does not work. But 34 works, with the third side equal to 11 centimetres."],
)

HAND["EXT_G5_FP_2023_040"] = E(
    "Which of the two angles given below are supplementary to each other?",
    ["127.5 degrees and 53.5 degrees", "83.6 degrees and 95.4 degrees", "111.8 degrees and 68.2 degrees", "115.7 degrees and 65.3 degrees"],
    ["Supplementary angles add up to exactly 180 degrees. Add the two angles in each option.",
     "Supplementary means the sum equals 180 degrees."],
    ["127.5 plus 53.5 equals 181. Not a match.",
     "83.6 plus 95.4 equals 179. Not a match.",
     "111.8 plus 68.2 equals 180. That matches.",
     "115.7 plus 65.3 equals 181. Not a match."],
)

HAND["EXT_G5_FP_2024_001"] = E(
    "The area of a square and a rectangle are equal. If the side of the square is 56 centimetres, "
    "and the breadth of the rectangle is 49 centimetres, find the perimeter of the rectangle.",
    ["230 centimetres", "224 centimetres", "222 centimetres", "None of these"],
    ["Find the area of the square: side times side. The rectangle has the same area, so use it to get the rectangle's length.",
     "Area of a square equals side squared. Length equals area divided by breadth. Perimeter equals 2 times, length plus breadth."],
    ["Area of the square: 56 times 56, which is 3136 square centimetres.",
     "The rectangle has the same area, so its length is 3136 divided by 49, which is 64 centimetres.",
     "Perimeter of the rectangle: 2 times, 64 plus 49. That is 2 times 113, which is 226 centimetres.",
     "226 centimetres is not one of the choices given, so the answer is, none of these."],
)

HAND["EXT_G5_FP_2024_005"] = E(
    "What is the angle between the hour hand and the minute hand of a clock at 7 20 p m?",
    units("degrees", 90, 100, 120, 108),
    ["The hour hand does not stay on the 7. By 7 20 it has moved a little. It moves half a degree every minute. "
     "The minute hand moves 6 degrees every minute.",
     "Hour hand angle equals hours times 30, plus minutes times 0.5. Minute hand angle equals minutes times 6."],
    ["Hour hand: 7 times 30, plus 20 times 0.5. That is 210 plus 10, which is 220 degrees.",
     "Minute hand: 20 times 6, which is 120 degrees.",
     "The angle between them equals 220 minus 120, which is 100 degrees."],
)

HAND["EXT_G5_FP_2024_019"] = E(
    "If the perimeter of an equilateral triangle having side 12 centimetres is equal to the perimeter of a rectangle, "
    "which of the following can be the sides of the rectangle?",
    ["length 10 centimetres and breadth 5 centimetres", "length 14 centimetres and breadth 6 centimetres",
     "length 8 centimetres and breadth 6 centimetres", "length 13 centimetres and breadth 5 centimetres"],
    ["Find the triangle's perimeter first. All 3 sides are equal. A rectangle's perimeter is 2 times, length plus breadth. "
     "So length plus breadth must be half of that.",
     "Equilateral triangle perimeter equals 3 times side. Rectangle perimeter equals 2 times, length plus breadth."],
    ["Triangle perimeter equals 3 times 12, which is 36 centimetres.",
     "Rectangle: 2 times, length plus breadth, equals 36. So length plus breadth equals 18.",
     "Check: 10 plus 5 is 15, not a match. 14 plus 6 is 20, not a match. 8 plus 6 is 14, not a match. 13 plus 5 is 18. That matches."],
)

HAND["EXT_G5_FP_2024_033"] = E(
    "The side of a square is 30 centimetres. If one side is increased to 5 over 4 of the original, "
    "and another side is decreased to 3 over 5 of the original, "
    "what will be the difference in the area of the square and the area of the newly formed rectangle?",
    units("square centimetres", 300, 225, 275, 240),
    ["Find the two new sides: 30 times 5 over 4, and 30 times 3 over 5. Multiply for the rectangle's area. "
     "Compare it with the square's area, 30 times 30.",
     "Area of a square equals side times side. Area of a rectangle equals length times breadth."],
    ["New length equals 30 times 5 over 4, which is 37.5 centimetres. New breadth equals 30 times 3 over 5, which is 18 centimetres.",
     "Rectangle area equals 37.5 times 18, which is 675 square centimetres.",
     "Square area equals 30 times 30, which is 900 square centimetres.",
     "Difference equals 900 minus 675, which is 225 square centimetres."],
)

HAND["EXT_G5_FP_2024_034"] = E(
    "Shraddha is facing East. She turns 135 degrees in clockwise direction, and then 315 degrees in anti-clockwise direction. "
    "In which direction is she facing now?",
    ["North-West", "South", "West", "South-East"],
    ["Clockwise from East goes to South, at 90 degrees, then South-West, at 135 degrees. "
     "Turning 315 degrees anti-clockwise is the same as a small turn the other way: 360 degrees minus 315 degrees.",
     "Turning x degrees anti-clockwise is the same as turning 360 degrees minus x degrees, clockwise."],
    ["East, plus 135 degrees clockwise, gives South-West.",
     "315 degrees anti-clockwise equals 360 degrees minus 315 degrees, which is 45 degrees clockwise.",
     "South-West, plus 45 degrees clockwise, gives West."],
)

HAND["EXT_G5_FP_2025_002"] = E(
    "The circumference of a circle is equal to the perimeter of a square. "
    "If the area of the circle is 616 square centimetres, find the area of the square.",
    units("square centimetres", 484, 196, 576, 441),
    ["Use the circle's area, pi times r times r, with pi equal to 22 over 7, to find r. "
     "Then find the circumference, and share it among the 4 equal sides of the square.",
     "Circle area equals pi r squared. Circumference equals 2 pi r. Square perimeter equals 4 times side."],
    ["22 over 7, times r squared, equals 616. So r squared equals 616 times 7, divided by 22, which is 196. So r equals 14 centimetres.",
     "Circumference equals 2, times 22 over 7, times 14, which is 88 centimetres.",
     "Square perimeter equals 88. So the side equals 88 divided by 4, which is 22 centimetres.",
     "Area equals 22 times 22, which is 484 square centimetres."],
)

HAND["EXT_G5_FP_2025_011"] = E(
    "What is the angle between the hour and minute hand at 9 33 p m?",
    units("degrees", 88.5, 91.5, 87.5, 84.5),
    ["Hour hand equals 9 times 30, plus a bit more for the 33 minutes, at half a degree per minute. Minute hand equals 33 times 6.",
     "Hour hand angle equals hours times 30, plus minutes times 0.5. Minute hand angle equals minutes times 6."],
    ["Hour hand: 9 times 30, plus 33 times 0.5. That is 270 plus 16.5, which is 286.5 degrees.",
     "Minute hand: 33 times 6, which is 198 degrees.",
     "The angle between them equals 286.5 minus 198, which is 88.5 degrees."],
)

HAND["EXT_G5_FP_2025_012"] = E(
    "The area of a rectangle is 468 square centimetres. If the breadth of the rectangle is 18 centimetres, find the perimeter of the rectangle.",
    units("centimetres", 86, 72, 88, 96),
    ["Use area equals length times breadth to find the length first. Then use the perimeter formula.",
     "Length equals area divided by breadth. Perimeter equals 2 times, length plus breadth."],
    ["Length equals 468 divided by 18, which is 26 centimetres.",
     "Perimeter equals 2 times, 26 plus 18. That is 2 times 44, which is 88 centimetres."],
)

HAND["EXT_G5_FP_2025_029"] = E(
    "What is the sum of the supplementary and complementary angle of 58 degrees?",
    units("degrees", 144, 154, 164, 148),
    ["Complementary angles add up to 90 degrees. Supplementary angles add up to 180 degrees. Find both partners of 58 degrees, then add them.",
     "Complementary equals 90 degrees minus the angle. Supplementary equals 180 degrees minus the angle."],
    ["Complementary angle equals 90 degrees minus 58 degrees, which is 32 degrees.",
     "Supplementary angle equals 180 degrees minus 58 degrees, which is 122 degrees.",
     "Sum equals 32 degrees plus 122 degrees, which is 154 degrees."],
)

HAND["EXT_G5_FP_2025_034"] = E(
    "Square P Q R S has an area of 196 square centimetres. A rectangle A B C D has an area four times the area of this square. "
    "Which of the following can be the sides of the rectangle?",
    ["44 and 16", "52 and 18", "56 and 14", "28 and 36"],
    ["Find the rectangle's area: 4 times 196. Then multiply the two sides in each option, and see which gives that area.",
     "Area of a rectangle equals length times breadth."],
    ["Rectangle area equals 4 times 196, which is 784 square centimetres.",
     "44 times 16 is 704, not a match. 52 times 18 is 936, not a match. 28 times 36 is 1008, not a match.",
     "56 times 14 is 784. That matches."],
)

HAND["EXT_G5_WS_B5_012"] = E(
    "6 squared plus Z squared equals 10 squared. Find the value of Z.",
    ["4", "64", "16", "8"],
    ["We need Z squared equals 10 squared minus 6 squared, which is 100 minus 36.",
     "Z squared equals 64. What number squared gives 64?",
     "A similar one: 3 squared plus Z squared equals 5 squared. Z squared equals 25 minus 9, which is 16. So Z equals 4."],
    ["Z squared equals 10 squared minus 6 squared. That is 100 minus 36, which is 64.",
     "Z equals the square root of 64, which is 8."],
)

HAND["EXT_G5_WS_B6_021"] = E(
    "The sides of a square are 2 A plus 5, centimetres, and 3 A minus 1, centimetres. Find the perimeter.",
    ["68 centimetres", "24 centimetres", "36 centimetres", "data inadequate"],
    ["All four sides of a square are equal. So the two expressions for the side must be equal to each other.",
     "Write 2 A plus 5 equals 3 A minus 1, and solve for A. Then put your value of A back into 2 A plus 5 to get the side, "
     "and remember the perimeter is 4 times the side.",
     "Try a similar one. A square has sides x plus 3, centimetres, and 2 x minus 1, centimetres. "
     "x plus 3 equals 2 x minus 1 gives x equals 4. "
     "The side is 4 plus 3, which is 7 centimetres, and the perimeter is 4 times 7, which is 28 centimetres."],
    ["Equal sides: 2 A plus 5 equals 3 A minus 1.",
     "6 equals A. Subtract 2 A, and add 1.",
     "Side equals 2 times 6, plus 5, which is 17 centimetres.",
     "Perimeter equals 4 times 17, which is 68 centimetres."],
)

HAND["EXT_G5_WS_B6_022"] = E(
    "The angles of a triangle are y degrees, y minus 15, degrees, and 7 y plus 24, degrees. What is the smallest angle?",
    ["19 degrees", "6 degrees", "4 degrees", "none of these"],
    ["The three angles of a triangle always add up to 180 degrees.",
     "y, plus y minus 15, plus 7 y plus 24, equals 180. Solve for y, then find each angle.",
     "A similar one: angles 2 x, 3 x and 4 x. The sum equals 9 x, which equals 180, so x equals 20. "
     "The angles are 40 degrees, 60 degrees and 80 degrees. The smallest equals 40 degrees."],
    ["y, plus y minus 15, plus 7 y plus 24, equals 180.",
     "9 y plus 9 equals 180. So 9 y equals 171. So y equals 19.",
     "The angles are 19 degrees; 19 minus 15, which is 4 degrees; and 7 times 19, plus 24, which is 157 degrees.",
     "The smallest angle equals 4 degrees."],
)
