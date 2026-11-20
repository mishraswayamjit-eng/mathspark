"""Grade 4 triangle lessons written for one question each: Q_CH19_011 to 025."""
from g4_gr4_triangles_lib import (ANS, B, FIG, G, QF, W, ch, lesson, mark, strike, tri)

LESSONS = {}

_MEDIAN = dict(kind="polygon", points=[[4, 0], [0, 8], [5, 8], [10, 8]], corners=["corner", None, "middle", None],
               edges=[None, "5 cm", "5 cm", None], dashed=[{"from": 0, "to": 2}])

# Interior angles 55° and 70°. Exterior angle next to the third angle?
LESSONS["Q_CH19_011"] = lesson([
    B("2 interior angles of a triangle are 55 degrees and 70 degrees. We want the exterior angle next to the third angle.",
      G("l1", "Two interior angles: 55° and 70°."), W("l2", "Exterior angle next to the third angle = ?", tone="given"),
      QF("Q_CH19_011")),
    B("Interior angles are the ones inside the triangle. An exterior angle is made outside, when one side is stretched on past a corner."),
    B("First find the third inside angle. 55 plus 70 is 125, and 180 minus 125 is 55.",
      W("l3", "3 angles = 180°"), W("l4", "55 + 70 = 125"), W("l5", "180 − 125 = 55")),
    B("So the third interior angle is 55. Now stretch a side past that corner. The inside angle and the outside angle sit side by side on a straight line.",
      FIG(kind="angles", layout="onLine", parts=[{"label": "55°", "size": 55}, {"label": "?", "size": 125}])),
    B("What do 2 angles on a straight line add up to?",
      ask=ch(["90°", "180°", "360°"], 1,
             "A straight line is a half turn, and a half turn is 180 degrees.")),
    B("180. So the exterior angle is 180 minus 55. Take away 50 to get 130, then 5 more to get 125.",
      W("l6", "180 − 50 = 130"), W("l7", "130 − 5 = 125"), W("l8", "180 − 55 = 125")),
    B("So the exterior angle is 125 degrees.",
      ANS("l9", "Exterior angle = 125°", "125°")),
    B("Did you spot it? 125 is also 55 plus 70, the other 2 inside angles added together. That always happens with an exterior angle.",
      mark("l4", "55 + 70 = 125", "box")),
    B("The trap is 110. That is the outside angle next to the 70, which is a different corner. The one we want, next to the third angle, is 125.",
      W("l10", "180 − 70 = 110")),
])

# Exterior angle 130°, one opposite interior angle 50°. The other?
LESSONS["Q_CH19_012"] = lesson([
    B("An exterior angle of a triangle is 130 degrees. One of the opposite interior angles is 50 degrees. What is the other one?",
      G("l1", "Exterior angle = 130°. One opposite interior angle = 50°."),
      W("l2", "The other opposite interior angle = ?", tone="given"), QF("Q_CH19_012")),
    B("An exterior angle sits outside the triangle, next to one corner. The 2 opposite interior angles are the inside angles at the other 2 corners."),
    B("Start with the inside angle right beside the exterior angle. Together they lie on a straight line, so they make 180. 180 minus 130 is 50.",
      W("l3", "180 − 130 = 50"),
      FIG(kind="angles", layout="onLine", parts=[{"label": "50°", "size": 50}, {"label": "130°", "size": 130}])),
    B("So that inside angle is 50, and we are told another inside angle is 50 as well. And the 3 inside angles make 180.",
      W("l4", "50 + 50 + ? = 180")),
    B("What is the last inside angle?",
      ask=ch(["180 − 100 = 80", "180 − 50 = 130", "50 again"], 0,
             "The 2 inside angles we know are 50 and 50, which make 100. Take 100 away from 180.")),
    B("80 degrees. 50 plus 50 is 100, and 180 minus 100 is 80.",
      W("l5", "50 + 50 = 100"), W("l6", "180 − 100 = 80"), ANS("l7", "Other angle = 80°", "80°")),
    B("Now look at this. The 2 opposite angles, 50 and 80, add up to 130. That is exactly the exterior angle!",
      W("l8", "50 + 80 = 130")),
    B("It is always true: an exterior angle equals the 2 opposite interior angles added together. So the quick way is 130 minus 50, which is 80.",
      W("l9", "130 − 50 = 80")),
    B("Either way, the other angle is 80 degrees."),
])

# Isosceles, each base angle 70°. Vertex angle?
LESSONS["Q_CH19_013"] = lesson([
    B("In an isosceles triangle each base angle is 70 degrees. We want the vertex angle.",
      G("l1", "Isosceles triangle. Each base angle = 70°. Vertex angle = ?"), QF("Q_CH19_013")),
    B("An isosceles triangle has 2 equal base angles at the bottom, and 1 vertex angle at the top, between the equal sides."),
    B("Each base angle is 70. How many base angles are there?",
      ask=ch(["1", "2", "3"], 1,
             "An isosceles triangle has 2 base angles, and they are equal. So there are 2 angles of 70.")),
    B("2 of them. Together they make 70 plus 70, which is 140.",
      W("l2", "70 + 70 = 140")),
    B("The 3 angles of a triangle make 180. So the vertex angle is whatever is left.",
      W("l3", "3 angles = 180°")),
    B("180 minus 140 is 40. The vertex angle is 40 degrees.",
      W("l4", "180 − 140 = 40"), ANS("l5", "Vertex angle = 40°", "40°")),
    B("The trap is to take away only one 70 and say 110. Both base angles have to come off.",
      W("l6", "180 − 70 = 110"), strike("l6", "180 − 70 = 110")),
    B("Check: 70 plus 70 plus 40 makes 180. So for the vertex angle, double the base angle and take it from 180.",
      W("l7", "70 + 70 + 40 = 180")),
])

# Isosceles, vertex angle 50°. Each base angle?
LESSONS["Q_CH19_014"] = lesson([
    B("The vertex angle of an isosceles triangle is 50 degrees. How big is each base angle?",
      G("l1", "Isosceles triangle. Vertex angle = 50°. Each base angle = ?"), QF("Q_CH19_014")),
    B("The vertex angle is at the top. The 2 base angles at the bottom are equal, like twins."),
    B("The 3 angles of a triangle make 180. So what do the 2 base angles share?",
      ask=ch(["180 − 50 = 130", "180 + 50 = 230", "just 50"], 0,
             "Take the vertex angle out of the 180. What is left belongs to the 2 base angles.")),
    B("130. That is both base angles together.",
      W("l2", "180 − 50 = 130")),
    B("So how big is each base angle?",
      ask=ch(["130°", "65°", "55°"], 1,
             "The 2 base angles are equal, and they share 130. So each one is half of 130.")),
    B("Half of 130. Half of 100 is 50, and half of 30 is 15. 50 plus 15 is 65.",
      W("l3", "100 ÷ 2 = 50"), W("l4", "30 ÷ 2 = 15"), W("l5", "130 ÷ 2 = 65")),
    B("So each base angle is 65 degrees.",
      ANS("l6", "Each base angle = 65°", "65°")),
    B("Check: 50 plus 65 plus 65 makes 180.",
      W("l7", "50 + 65 + 65 = 180"), tri("isosceles", a="50°", b="65°", c="65°")),
    B("When you know the vertex angle: take it from 180, then halve what is left."),
])

# The side opposite the right angle is called the:
LESSONS["Q_CH19_015"] = lesson([
    B("In a right-angled triangle, what do we call the side opposite the right angle?",
      G("l1", "The side opposite the right angle is called the ...?"), QF("Q_CH19_015")),
    B("A right-angled triangle has one square corner. 2 sides meet at that corner. The third side does not touch it: it lies across from the right angle."),
    B("Look at the highlighted side. Compared with the other 2 sides, it is...",
      ask=ch(["the shortest", "the longest", "the same length"], 1,
             "In any triangle the longest side lies opposite the biggest angle. Here the biggest angle is the right angle.")),
    B("The longest. The biggest angle always faces the longest side, and the right angle is the biggest angle in this triangle."),
    B("This special longest side has a special name: the hypotenuse.",
      W("l2", "Side opposite the right angle: hypotenuse"), mark("l2", "hypotenuse", "underline")),
    B("What about the other words? The base and the height are the 2 sides that meet at the right angle.",
      W("l3", "Base and height: meet at the right angle")),
    B("And a median is a line from a corner to the middle of the opposite side. It is not a side at all."),
    B("So the side opposite the right angle is called the hypotenuse.",
      ANS("l4", "Hypotenuse")),
    B("Hypotenuse is a long word for a long side: the longest side of a right-angled triangle."),
])

# How many axes of symmetry does a scalene triangle have?
LESSONS["Q_CH19_016"] = lesson([
    B("How many axes of symmetry does a scalene triangle have?",
      G("l1", "Axes of symmetry of a scalene triangle = ?"), QF("Q_CH19_016")),
    B("An axis of symmetry is a fold line. Fold the shape along it, and the 2 halves match exactly."),
    B("In a triangle, a fold line goes through a corner. For the halves to match, the 2 sides that meet at that corner must land on each other. So they must be equal.",
      tri("isosceles", hl=["ab", "ca"], note="Equal sides fold onto each other")),
    B("Now, what does scalene mean?",
      ask=ch(["all 3 sides are equal", "2 sides are equal", "no sides are equal"], 2,
             "Scalene is the name for a triangle whose 3 sides are all different lengths.")),
    B("No sides are equal. So at every corner, a longer side would be folded onto a shorter one. The halves can never match."),
    B("No pair of equal sides means no fold line at all. A scalene triangle has 0 axes of symmetry.",
      ANS("l2", "0 axes of symmetry", "0")),
    B("Compare the others. An isosceles triangle has 1 fold line, through the corner between its equal sides. An equilateral triangle has 3.",
      W("l3", "Isosceles: 1"), W("l4", "Equilateral: 3"), W("l5", "Scalene: 0")),
    B("So the number of fold lines tells you how many sides match. For a scalene triangle, that is 0."),
])

# Sides 8 cm, 11 cm and 15 cm. Perimeter?
LESSONS["Q_CH19_017"] = lesson([
    B("A triangle has sides of 8, 11 and 15 centimetres. We want its perimeter.",
      G("l1", "Triangle with sides 8 cm, 11 cm, 15 cm. Perimeter = ?"), QF("Q_CH19_017")),
    B("The perimeter is the walk all the way round the triangle, along every side."),
    B("So what do we do with the 3 lengths?",
      ask=ch(["add them", "multiply them", "pick the biggest"], 0,
             "Walking round means going along one side, then the next, then the last. The distances add up.")),
    B("Add them. Start with 8 plus 11, which is 19.",
      W("l2", "8 + 11 = 19")),
    B("Then 19 plus 15. 19 plus 10 is 29, and 5 more is 34.",
      W("l3", "19 + 10 = 29"), W("l4", "29 + 5 = 34")),
    B("So the perimeter is 34 centimetres.",
      ANS("l5", "Perimeter = 34 cm", "34 cm")),
    B("Check by adding in another order. 15 plus 11 is 26, and 26 plus 8 is 34. The same answer.",
      W("l6", "15 + 11 = 26"), W("l7", "26 + 8 = 34")),
    B("Perimeter always means add. Multiplying the sides gives a huge number that means nothing here."),
])

# Perimeter 36 cm, two sides 12 cm and 9 cm. Third side?
LESSONS["Q_CH19_018"] = lesson([
    B("The perimeter of a triangle is 36 centimetres. 2 of its sides are 12 centimetres and 9 centimetres. How long is the third side?",
      G("l1", "Perimeter 36 cm. Two sides: 12 cm and 9 cm. Third side = ?"), QF("Q_CH19_018")),
    B("The perimeter is all 3 sides added together. So 12, plus 9, plus the missing side, makes 36.",
      W("l2", "12 + 9 + ? = 36")),
    B("What should we do first?",
      ask=ch(["add 12 and 9", "take 9 away from 12", "add 12, 9 and 36"], 0,
             "First find how much of the perimeter the 2 known sides use up. Add 12 and 9.")),
    B("12 plus 9 is 21. The 2 known sides use up 21 centimetres.",
      W("l3", "12 + 9 = 21")),
    B("21 is one of the choices. Is it the third side?",
      ask=ch(["yes, it is 21", "no, take it away from 36"], 1,
             "21 is the 2 known sides together. The third side is what is still needed to reach 36.")),
    B("36 minus 21. Take away 20 to get 16, then 1 more to get 15.",
      W("l4", "36 − 20 = 16"), W("l5", "16 − 1 = 15"), W("l6", "36 − 21 = 15")),
    B("So the third side is 15 centimetres.",
      ANS("l7", "Third side = 15 cm", "15 cm")),
    B("Check: 12 plus 9 plus 15 makes 36. It works.",
      W("l8", "12 + 9 + 15 = 36")),
    B("To find a missing side: add the sides you know, then take that from the perimeter."),
])

# Right-angled triangle with legs 6 cm and 8 cm. Area?
LESSONS["Q_CH19_019"] = lesson([
    B("A right-angled triangle has legs of 6 centimetres and 8 centimetres. We want its area.",
      G("l1", "Right-angled triangle with legs 6 cm and 8 cm. Area = ?"), QF("Q_CH19_019")),
    B("The legs are the 2 sides that meet at the right angle. Put 2 of these triangles together and they make a rectangle, 6 by 8.",
      FIG(kind="polygon", points=[[0, 0], [10, 0], [10, 7.5], [0, 7.5]], edges=[None, "6 cm", "8 cm", None],
          dashed=[{"from": 0, "to": 2}], note="Two of the triangles make a rectangle")),
    B("What is the area of that rectangle?",
      ask=ch(["6 + 8 = 14", "6 × 8 = 48", "8 − 6 = 2"], 1,
             "The area of a rectangle is its length times its breadth. Adding gives a length, not the space inside.")),
    B("6 times 8 is 48. That is the whole rectangle.",
      W("l2", "6 × 8 = 48")),
    B("Our triangle is one of the 2 equal halves. So what is its area?",
      ask=ch(["48", "half of 48", "twice 48"], 1,
             "2 equal triangles fill the rectangle. So one triangle is half of 48.")),
    B("Half of 48 is 24. The area of the triangle is 24 square centimetres.",
      W("l3", "48 ÷ 2 = 24"), ANS("l4", "Area = 24 cm²", "24 cm²")),
    B("The 10 in the choices is the length of the third, slanted side of this triangle. That is a length, not an area."),
    B("For a right-angled triangle: multiply the 2 legs, then halve."),
])

# A median joins a vertex to the _______ of the opposite side.
LESSONS["Q_CH19_020"] = lesson([
    B("A median of a triangle joins a vertex to a special point of the opposite side. Which point?",
      G("l1", "A median joins a vertex to the ____ of the opposite side.")),
    B("A vertex is a corner. Every corner of a triangle has an opposite side: the one side that it does not touch."),
    B("A median is a line from a corner across to its opposite side. But it does not land just anywhere. Listen to the word: median sounds like middle."),
    B("So where on the opposite side does a median land?",
      ask=ch(["at one end of it", "exactly in the middle", "anywhere at all"], 1,
             "Median and middle come from the same idea. A median lands exactly in the middle of the opposite side.")),
    B("Exactly in the middle. It cuts that side into 2 equal parts, like the 2 parts of 5 centimetres here.",
      FIG(**_MEDIAN)),
    B("The point in the middle of a side has its own name: the midpoint.",
      W("l2", "Middle point of a side = midpoint")),
    B("If the line went to an end point of the side, it would just run along a side of the triangle. That is no median."),
    B("So a median joins a vertex to the midpoint of the opposite side.",
      ANS("l3", "Midpoint")),
    B("Median, middle, midpoint. The 3 words belong together."),
])

# How many medians does a triangle have?
LESSONS["Q_CH19_021"] = lesson([
    B("How many medians does a triangle have?",
      G("l1", "How many medians does a triangle have?")),
    B("A median is a line from a corner of the triangle to the middle of the opposite side. Here is one.",
      FIG(**_MEDIAN)),
    B("How many corners does a triangle have?",
      ask=ch(["2", "3", "6"], 1,
             "Tri means 3. A triangle has 3 corners and 3 sides.")),
    B("3 corners. And each corner has exactly 1 opposite side, the side it does not touch."),
    B("So from each corner we can draw exactly 1 median. 3 corners, 1 median each: 3 medians.",
      W("l2", "3 × 1 = 3")),
    B("So a triangle has 3 medians.",
      ANS("l3", "3 medians")),
    B("Why not 6? Because each corner gives only 1 median, not 2."),
    B("A lovely fact for later: all 3 medians cross at one single point, the balance point of the triangle."),
])

# Angles 40°, 60°, 80°: which side is the longest?
LESSONS["Q_CH19_022"] = lesson([
    B("A triangle has angles of 40, 60 and 80 degrees. Which of its sides is the longest?",
      G("l1", "Angles: 40°, 60°, 80°. Which side is the longest?"), QF("Q_CH19_022")),
    B("Think of an angle as an open mouth. The wider the mouth opens, the longer the side it has to stretch across."),
    B("So the biggest angle faces the longest side, and the smallest angle faces the shortest side.",
      W("l2", "Biggest angle faces the longest side")),
    B("Which is the biggest angle here?",
      ask=ch(["40°", "60°", "80°"], 2,
             "Compare the 3 numbers. 80 is more than 60, and 60 is more than 40.")),
    B("80 degrees. So the longest side is the one opposite the 80. Opposite means across from it: the side that angle does not touch.",
      mark("l1", "80°", "circle")),
    B("So the longest side is the side opposite 80 degrees.",
      ANS("l3", "The side opposite 80°")),
    B("And the side opposite 40 is the shortest. The side opposite 60 is in between."),
    B("Could all the sides be equal? Only if all the angles were equal, and these are not."),
    B("Big angle, long side. Small angle, short side. Here the 80 wins."),
])

# Can a triangle have two right angles?
LESSONS["Q_CH19_023"] = lesson([
    B("Can a triangle have 2 right angles? Let's try to build one and see what happens.",
      G("l1", "Can a triangle have two right angles?")),
    B("A right angle is 90 degrees, a square corner.",
      W("l2", "Right angle = 90°")),
    B("2 right angles together make how much?",
      ask=ch(["90°", "180°", "360°"], 1,
             "Each right angle is 90. And 90 plus 90 is 180.")),
    B("180 degrees.",
      W("l3", "90 + 90 = 180")),
    B("But the 3 angles of a triangle add up to 180 altogether. The 2 right angles have used up all of it.",
      W("l4", "3 angles = 180°")),
    B("So how much is left for the third angle?",
      ask=ch(["90°", "0°", "180°"], 1,
             "180 minus 180 is 0. Nothing at all is left.")),
    B("0 degrees. An angle of 0 is no corner at all! The 2 sides would stand straight up, side by side, and never meet.",
      W("l5", "180 − 180 = 0")),
    B("Making the triangle bigger, or its sides longer, changes nothing. The angles still have to add up to 180."),
    B("And a right-angled isosceles triangle has only 1 right angle. Its angles are 90, 45 and 45.",
      W("l6", "90 + 45 + 45 = 180")),
    B("So the answer is no. 90 plus 90 is 180, and that leaves 0 for the third angle.",
      ANS("l7", "No: 90 + 90 = 180 leaves 0", "No")),
])

# Equilateral triangle with perimeter 45 cm. Each side?
LESSONS["Q_CH19_024"] = lesson([
    B("The perimeter of an equilateral triangle is 45 centimetres. How long is each side?",
      G("l1", "Equilateral triangle, perimeter 45 cm. Each side = ?"), QF("Q_CH19_024")),
    B("Equilateral means 3 equal sides. Together the 3 sides make the perimeter, 45.",
      W("l2", "side + side + side = 45")),
    B("How do we find 1 side?",
      ask=ch(["45 ÷ 3", "45 × 3", "45 ÷ 2"], 0,
             "The 45 is shared equally among 3 sides. Sharing equally means dividing, and there are 3 sides.")),
    B("45 divided by 3. Split 45 into 30 and 15. 30 divided by 3 is 10, and 15 divided by 3 is 5. 10 plus 5 is 15.",
      W("l3", "30 ÷ 3 = 10"), W("l4", "15 ÷ 3 = 5"), W("l5", "45 ÷ 3 = 15")),
    B("So each side is 15 centimetres.",
      ANS("l6", "Each side = 15 cm", "15 cm")),
    B("Check: 15 plus 15 plus 15 makes 45.",
      W("l7", "15 + 15 + 15 = 45"), tri("equilateral", ab="15 cm", bc="15 cm", ca="15 cm")),
    B("2 slips to dodge. Multiplying by 3 makes one side longer than the whole perimeter. And dividing by 2 forgets that a triangle has 3 sides."),
    B("Perimeter of an equilateral triangle, divided by 3, gives the side."),
])

# Right-angled triangle: base 12 cm, area 42 cm². Height?
LESSONS["Q_CH19_025"] = lesson([
    B("A right-angled triangle has a base of 12 centimetres and an area of 42 square centimetres. What is its height?",
      G("l1", "Right-angled triangle: base 12 cm, area 42 cm². Height = ?"), QF("Q_CH19_025")),
    B("We know how to go forwards: the area is half of base times height. This time we go backwards, from the area to the height.",
      W("l2", "Area = half of base × height")),
    B("The triangle is half of a rectangle with the same base and height. So the rectangle's area is twice 42. What is twice 42?",
      ask=ch(["84", "21", "54"], 0,
             "Twice means 2 lots. 42 plus 42 is 84.")),
    B("84. So the base times the height is 84.",
      W("l3", "2 × 42 = 84"), W("l4", "12 × height = 84")),
    B("12 times what makes 84?",
      ask=ch(["84 ÷ 12 = 7", "84 − 12 = 72", "84 + 12 = 96"], 0,
             "To undo times 12, we divide by 12. So the height is 84 divided by 12.")),
    B("84 divided by 12 is 7, because 12 times 7 is 84.",
      W("l5", "84 ÷ 12 = 7"), W("l6", "12 × 7 = 84")),
    B("So the height is 7 centimetres.",
      ANS("l7", "Height = 7 cm", "7 cm")),
    B("Check forwards: 12 times 7 is 84, and half of 84 is 42. That matches the area.",
      W("l8", "84 ÷ 2 = 42")),
    B("The trap is 42 divided by 12, which gives 3.5. That forgets the half. Double the area first, then divide by the base. That gives 7.",
      W("l9", "42 ÷ 12 = 3.5"), strike("l9", "42 ÷ 12 = 3.5")),
])
