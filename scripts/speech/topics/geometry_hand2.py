"""Hand-written narration, geometry past papers 2019 to 2022."""
from geometry_hand1 import E, units

HAND = {}

HAND["EXT_G5_FP_2019_001"] = E(
    "The length of a rectangle is twice its breadth. If the perimeter of the rectangle is 90 centimetres, find the area of the rectangle.",
    units("square centimetres", 225, 550, 450, 600),
    ["If the breadth is 1 part, then the length is 2 parts, so length plus breadth is 3 parts. "
     "Half the perimeter gives length plus breadth. Find one part first.",
     "Length plus breadth equals perimeter divided by 2. Area equals length times breadth."],
    ["Length plus breadth equals 90 divided by 2, which is 45. Since the length is 2 times the breadth, 3 times the breadth equals 45. "
     "So the breadth is 15 centimetres, and the length is 30 centimetres.",
     "Area equals 30 times 15, which is 450 square centimetres."],
)

HAND["EXT_G5_FP_2019_012"] = E(
    "The supplementary angle of an obtuse angle will always be:",
    ["supplementary angle", "acute angle", "right angle", "reflex angle"],
    ["An obtuse angle is between 90 degrees and 180 degrees. Subtract it from 180 degrees. What size range do you get?",
     "The supplement equals 180 degrees minus the angle."],
    ["For an obtuse angle x: x is more than 90 degrees, and less than 180 degrees.",
     "The supplement, 180 degrees minus x, is between 0 degrees and 90 degrees.",
     "An angle less than 90 degrees is an acute angle."],
)

HAND["EXT_G5_FP_2019_018"] = E(
    "An angle measures 35 minus x, degrees. What will be the measure of the complementary angle of it?",
    ["65 minus x, degrees", "65 plus x, degrees", "35 plus x, degrees", "55 plus x, degrees"],
    ["Complementary angles add to 90 degrees. Subtract the whole bracket from 90. Watch the sign in front of x!",
     "The complement equals 90 degrees minus the angle."],
    ["The complement equals 90 minus, open bracket, 35 minus x, close bracket.",
     "Open the bracket: 90 minus 35 plus x. The minus changes the sign of minus x.",
     "That equals 55 plus x, degrees."],
)

HAND["EXT_G5_FP_2019_022"] = E(
    "The area of a square and a rectangle are the same. If the side of the square is 15 centimetres, "
    "and the length of the rectangle is 25 centimetres, then the difference between the perimeter of the square and the rectangle is?",
    units("centimetres", 26, 10, 9, 8),
    ["Find the area of the square. Use it to find the rectangle's breadth: area divided by length. Then find both perimeters, and subtract.",
     "Breadth equals area divided by length. Perimeter of a rectangle equals 2 times, length plus breadth. "
     "Perimeter of a square equals 4 times side."],
    ["Square area equals 15 times 15, which is 225 square centimetres.",
     "Rectangle breadth equals 225 divided by 25, which is 9 centimetres.",
     "Rectangle perimeter equals 2 times, 25 plus 9, which is 68 centimetres. Square perimeter equals 4 times 15, which is 60 centimetres.",
     "Difference equals 68 minus 60, which is 8 centimetres."],
)

HAND["EXT_G5_FP_2019_024"] = E(
    "Given below are the sides of equilateral triangles and of squares in each of the alternatives. "
    "In which one does the perimeter of the equilateral triangle and the square become equal?",
    ["E equals 9, and S equals 9", "E equals 8, and S equals 9", "E equals 16, and S equals 12", "E equals 12, and S equals 10"],
    ["Triangle perimeter equals 3 times E. Square perimeter equals 4 times S. Work both out for each option.",
     "Equilateral triangle: 3 times side. Square: 4 times side."],
    ["Option A: 3 times 9 is 27, and 4 times 9 is 36. Not equal.",
     "Option B: 24 and 36. Not equal.",
     "Option C: 3 times 16 is 48, and 4 times 12 is 48. They are equal.",
     "Option D: 36 and 40. Not equal. Answer: E equals 16, and S equals 12."],
)

HAND["EXT_G5_FP_2019_028"] = E(
    "The three angles of a triangle are x degrees, x plus 10, degrees, and 2 x minus 6, degrees. "
    "Which one of the following is the greatest angle of this triangle?",
    units("degrees", 88, 54, 82, 102),
    ["Angles of a triangle add up to 180 degrees. Add the three angles and find x. Then work out each angle.",
     "The angle sum of a triangle equals 180 degrees."],
    ["x, plus x plus 10, plus 2 x minus 6, equals 180. So 4 x plus 4 equals 180. Then 4 x equals 176. So x equals 44.",
     "The angles are 44 degrees, 54 degrees and 82 degrees. Check: 44 plus 54 plus 82 equals 180. Correct.",
     "The greatest is 82 degrees."],
)

HAND["EXT_G5_FP_2019_036"] = E(
    "The three sides of a right-angled triangle are 9 centimetres, 40 centimetres and 41 centimetres. What is the area of this triangle?",
    units("square centimetres", 180, 90, 210, 820),
    ["In a right-angled triangle, the two shorter sides are the base and height. The longest side, 41, is the hypotenuse. "
     "Don't use it for the area.",
     "Area of a triangle equals half of base times height."],
    ["Base equals 40 centimetres, and height equals 9 centimetres, the two shorter sides.",
     "Area equals half of 40 times 9, which is 180 square centimetres."],
)

HAND["EXT_G5_FP_2020_007"] = E(
    "What is the complementary angle of the angle x minus 35, degrees?",
    ["x plus 35, degrees", "35 minus x, degrees", "125 minus x, degrees", "x minus 55, degrees"],
    ["Complementary angles add to 90 degrees. Subtract the whole bracket from 90. Be careful with the signs.",
     "The complement equals 90 degrees minus the angle."],
    ["The complement equals 90 minus, open bracket, x minus 35, close bracket.",
     "Open the bracket: 90 minus x plus 35.",
     "That equals 125 minus x, degrees."],
)

HAND["EXT_G5_FP_2020_011"] = E(
    "A right-angled triangle has sides measuring 7 centimetres, 24 centimetres and 25 centimetres. "
    "Which of the following calculations could work out to be its area in square centimetres?",
    ["7 times 24 times 25, divided by 2", "7 times 12", "12 times 12.5", "3.5 times 12"],
    ["The two shorter sides, 7 and 24, are the base and the height. The longest side, 25, is the hypotenuse, and is not used for the area.",
     "Area of a triangle equals half of base times height."],
    ["Base equals 7 centimetres, height equals 24 centimetres.",
     "Area equals half of 7 times 24, which is 7 times 12, because half of 24 is 12.",
     "Answer: 7 times 12, which equals 84 square centimetres."],
)

HAND["EXT_G5_FP_2020_027"] = E(
    "The length and width of a rectangle are 12 centimetres and 8 centimetres respectively. "
    "Another rectangle, whose area is the same as the first rectangle, has length 16 centimetres. What could be the width of this rectangle?",
    units("centimetres", 8, 10, 4, 6),
    ["Find the area of the first rectangle. The second rectangle has the same area, so divide it by 16.",
     "Width equals area divided by length."],
    ["Area equals 12 times 8, which is 96 square centimetres.",
     "Width equals 96 divided by 16, which is 6 centimetres."],
)

HAND["EXT_G5_FP_2021_006"] = E(
    "An angle measures 25 minus y, degrees. Which of the following is the complementary angle to this given angle?",
    ["65 minus y, degrees", "25 plus y, degrees", "y minus 65, degrees", "65 plus y, degrees"],
    ["Complementary angles add up to 90 degrees. Subtract the whole bracket from 90, and be careful with the minus sign.",
     "The complement equals 90 degrees minus the angle."],
    ["The complement equals 90 minus, open bracket, 25 minus y, close bracket.",
     "That equals 90 minus 25 plus y. Minus times minus equals plus.",
     "That equals 65 plus y, degrees."],
)

HAND["EXT_G5_FP_2022_016"] = E(
    "The perimeter of a rectangle is 96 centimetres. If the breadth is 6 centimetres less than the length, find the area of the rectangle.",
    units("square centimetres", 432, 315, 891, 567),
    ["Length plus breadth equals half the perimeter. And breadth equals length minus 6. "
     "Put these together to find the length, then the breadth, then the area.",
     "Length plus breadth equals perimeter divided by 2. Area equals length times breadth."],
    ["Length plus breadth equals 96 divided by 2, which is 48. With breadth equal to length minus 6, "
     "we get 2 times the length, minus 6, equals 48. So the length is 27 centimetres.",
     "Breadth equals 27 minus 6, which is 21 centimetres.",
     "Area equals 27 times 21, which is 567 square centimetres."],
)

HAND["EXT_G5_FP_2022_020"] = E(
    "Mishti is facing south-west. She turns 180 degrees in clockwise direction, and then turns 225 degrees in anti-clockwise direction. "
    "In which direction is she facing now?",
    ["South-East", "South", "East", "South-West"],
    ["A 180 degree turn takes her to the opposite direction. Then count 45 degree steps anti-clockwise. "
     "Each step moves to the next direction: North, then North-West, then West, and so on.",
     "Each 45 degree step is one direction: North, North-East, East, South-East, South, South-West, West, North-West."],
    ["South-West, plus 180 degrees, gives North-East, the opposite direction.",
     "225 degrees divided by 45 degrees equals 5 steps anti-clockwise from North-East: North, North-West, West, South-West, South.",
     "Now facing South."],
)

HAND["EXT_G5_FP_2022_028"] = E(
    "3 A plus 5, 7 A plus 10, and 4 A plus 15, are the sides of a triangle. For A equals 5, what would be the perimeter of the triangle?",
    units("units", 125, 120, 80, 100),
    ["Put A equals 5 into each side. Then add the three sides.",
     "The perimeter of a triangle equals the sum of its three sides."],
    ["3 A plus 5 equals 15 plus 5, which is 20.",
     "7 A plus 10 equals 35 plus 10, which is 45.",
     "4 A plus 15 equals 20 plus 15, which is 35.",
     "Perimeter equals 20 plus 45 plus 35, which is 100 units."],
)

HAND["EXT_G5_FP_2022_029"] = E(
    "The perimeter of a rectangle is 84 centimetres. If the breadth of the rectangle is half of the length, find the length of the rectangle.",
    units("centimetres", 42, 28, 21, 14),
    ["Length plus breadth equals half of 84. If the breadth is half of the length, then length plus breadth is 1.5 times the length.",
     "Length plus breadth equals perimeter divided by 2."],
    ["Length plus breadth equals 84 divided by 2, which is 42.",
     "Breadth equals length divided by 2. So length, plus length divided by 2, equals 1.5 times the length, which equals 42.",
     "Length equals 42 divided by 1.5, which is 28 centimetres. The breadth is 14 centimetres."],
)
