"""Geometry lessons written for one question each: the 2019 paper."""
from geometry_lib import (B, FIG, LV, T, W, both, choose, divide, group, lesson, mark, strike)

LESSONS = {}


# The supplementary angle of an obtuse angle will always be...
LESSONS["EXT_G5_FP_2019_012"] = lesson([
    B("Here is an obtuse angle on a straight line, with its supplementary angle beside it. What kind of angle will that partner always be?",
      W("l1", "Supplement of an obtuse angle is always ...?", tone="given", label=True),
      FIG("f1", kind="angles", layout="onLine", parts=[{"label": "obtuse"}, {"label": "?"}])),
    B("First, the names. An obtuse angle is bigger than a right angle, 90 degrees, but smaller than a straight line, 180 degrees.",
      W("l2", "Obtuse: between 90° and 180°", label=True)),
    B("And supplementary angles share a straight line, so the two of them make 180 degrees together.",
      W("l3", "angle + supplement = 180°", label=True)),
    B("Let's try a real one. Say the obtuse angle is 120 degrees. Its supplement is 180 take away 120, which is 60 degrees.",
      W("l4", "Try 120°", label=True), W("l5", "180 − 120 = 60"),
      FIG("f2", kind="angles", layout="onLine", parts=[{"label": "120°", "size": 120}, {"label": "60°", "size": 60}])),
    B("Now think about every obtuse angle. It takes up more than 90 of the 180 degrees on the line. So how much is left for its partner?",
      ask=choose(["more than 90°", "exactly 90°", "less than 90°"], 2,
                 "The line holds 180 degrees, which is 2 lots of 90. If one angle takes more than 90, there must be less than 90 left over.")),
    B("There is always less than 90 left. Even a huge obtuse angle like 170 degrees leaves 10 degrees, which is still less than 90.",
      W("l6", "Try 170°", label=True), W("l7", "180 − 170 = 10"), W("l8", "10 < 90")),
    B("And an angle that is less than 90 degrees has a name: an acute angle. So the supplement of an obtuse angle is always acute.",
      W("l9", "Always an acute angle", tone="answer", label=True), mark("l9", "acute angle", "circle"),
      FIG("f3", kind="angles", layout="onLine", highlight=["p1"], parts=[{"label": "obtuse", "size": 120}, {"label": "acute"}])),
    B("So on a straight line, a big angle always has a small partner. Obtuse goes with acute, and a right angle goes with a right angle."),
], "authored")


# Square of side 15 cm and rectangle of length 25 cm have the same area. Difference of perimeters?
LESSONS["EXT_G5_FP_2019_022"] = lesson([
    B("A square has a side of 15 centimetres. A rectangle with a length of 25 centimetres has the same area. We want the difference between their perimeters.",
      W("l1", "Square: side 15 cm. Rectangle: length 25 cm.", tone="given", label=True),
      W("l2", "Same area. Difference of perimeters = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", square=True, length="15 cm", inside="Area = ?")),
    B("Start with what we can find: the area of the square, side times side. For 15 times 15, split one 15 into 10 and 5. 15 times 10 is 150.",
      W("l3", "15 × 10 = 150")),
    B("And 15 times 5 is 75. Together, 150 plus 75 makes 225. So the square's area is 225 square centimetres.",
      W("l4", "15 × 5 = 75"), W("l5", "150 + 75 = 225"), W("l6", "15 × 15 = 225")),
    B("The rectangle has the same area, 225, and its length is 25. How do we find its breadth?",
      FIG("f2", kind="rectangle", length="25 cm", breadth="?", inside="225 sq. cm", proportion=2.5),
      ask=choose(["225 − 25", "225 ÷ 25", "225 × 25"], 1,
                 "Area is length times breadth. So to get back from the area to the breadth, we divide by the length.")),
    B("225 divided by 25 is 9, because 9 times 25 is 225. So the breadth is 9 centimetres.",
      W("l7", "225 ÷ 25 = 9"), FIG("f3", kind="rectangle", length="25 cm", breadth="9 cm", proportion=2.5)),
    B("Now the rectangle's perimeter, the walk all the way round. Which sum gives it?",
      ask=choose(["25 + 9", "25 × 9", "2 × (25 + 9)"], 2,
                 "25 plus 9 is only one length and one breadth, which is halfway round. We have to double it for the whole walk.")),
    B("25 plus 9 is 34, and that is halfway. Double it: the rectangle's perimeter is 68 centimetres.",
      W("l8", "25 + 9 = 34"), W("l9", "2 × 34 = 68")),
    B("The square's perimeter is easier: 4 equal sides of 15. 4 times 15 is 60 centimetres.",
      W("l10", "4 × 15 = 60")),
    B("The difference is 68 take away 60, which is 8 centimetres.",
      W("l11", "68 − 60 = 8"), W("l12", "Difference = 8 cm", tone="answer", label=True), mark("l12", "8 cm", "circle")),
    B("Here is something worth noticing. The two shapes cover the same space, but the long thin one has the longer edge. Same area does not mean same perimeter."),
], "authored")


# In which pair are the perimeters of the equilateral triangle (side E) and square (side S) equal?
LESSONS["EXT_G5_FP_2019_024"] = lesson([
    B("E is the side of an equilateral triangle, and S is the side of a square. We have to find the pair where the two shapes have the same perimeter.",
      W("l1", "E = side of equilateral triangle, S = side of square", tone="given", label=True),
      W("l2", "Which pair gives equal perimeters?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="equilateral", sides={"ab": "E", "bc": "E", "ca": "E"})),
    B("The triangle has 3 equal sides, so its walk round is 3 times E. What is the walk round the square?",
      W("l3", "Triangle perimeter = 3 × E", label=True),
      ask=choose(["3 × S", "4 × S", "S × S"], 1,
                 "A square has 4 equal sides, so its walk round is 4 times S. S times S would be the space inside, the area.")),
    B("The square has 4 equal sides, so its perimeter is 4 times S. Now we test each pair.",
      W("l4", "Square perimeter = 4 × S", label=True),
      FIG("f2", kind="rectangle", square=True, length="S", breadth="S")),
    B("First pair: E is 9 and S is 9. 3 times 9 is 27, but 4 times 9 is 36. Not equal.",
      W("l5", "3 × 9 = 27"), W("l6", "4 × 9 = 36")),
    B("Second pair: E is 8 and S is 9. 3 times 8 is 24, and the square is still 36. Not equal.",
      W("l7", "3 × 8 = 24")),
    B("Notice something. The square has more sides to walk along. So for the two walks to match, which side has to be the longer one?",
      ask=choose(["the triangle's side, E", "the square's side, S", "neither: they must be equal"], 0,
                 "The triangle has only 3 sides to make the same walk that the square makes with 4. So each of the triangle's sides has to be longer.")),
    B("The triangle's side has to be longer. Try E is 12 and S is 10. 3 times 12 is 36, but 4 times 10 is 40. Close, but not equal.",
      W("l8", "3 × 12 = 36"), W("l9", "4 × 10 = 40")),
    B("Last pair: E is 16 and S is 12. 3 times 16 is 48, and 4 times 12 is 48. Equal!",
      W("l10", "3 × 16 = 48"), W("l11", "4 × 12 = 48"), mark("l10", "48", "circle"), mark("l11", "48", "circle")),
    B("So the perimeters are equal when E is 16 and S is 12.",
      W("l12", "E = 16 and S = 12", tone="answer", label=True), mark("l12", "E = 16 and S = 12", "circle"),
      FIG("f3", kind="table", headers=["E, S", "3 × E", "4 × S"],
          rows=[["9, 9", "27", "36"], ["8, 9", "24", "36"], ["16, 12", "48", "48"], ["12, 10", "36", "40"]],
          highlight=["r2"])),
    B("So when the choices are given, write the rule for each shape, then test the pairs one by one until both sides match."),
], "authored")


# Triangle with angles x°, (x + 10)° and (2x − 6)°. Greatest angle?
LESSONS["EXT_G5_FP_2019_028"] = lesson([
    B("The 3 angles of this triangle are written with x. They are x, x plus 10, and 2 x minus 6. We want the greatest angle.",
      W("l1", "Triangle angles: x°, (x + 10)°, (2x − 6)°", tone="given", label=True),
      W("l2", "Greatest angle = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="scalene", angles={"a": "x°", "b": "(x + 10)°", "c": "(2x − 6)°"})),
    B("We cannot compare the angles until we know x. So what do we know about the 3 angles of any triangle?",
      ask=choose(["they add up to 180°", "they add up to 360°", "they are all equal"], 0,
                 "Tear the corners off a paper triangle and line them up. They make a straight line, a half turn. That is 180 degrees.")),
    B("The 3 angles add up to 180 degrees. So we add ours and set the total equal to 180.",
      LV("l3", "x + (x + 10) + (2x − 6) = 180", {"x": 44})),
    B("Gather the x's: 1 x, another x, and 2 x make 4 x. Then the plain numbers: plus 10 and minus 6 together make plus 4.",
      group("l3", [T("x", 1), T("x", 2), T("2x")], "4x"), LV("l4", "4x + 4 = 180", {"x": 44})),
    B("Take 4 away from both sides. 180 take away 4 leaves 176.",
      strike("l4", "+ 4", "− 4"), both("l4", "− 4"), LV("l5", "4x = 176", {"x": 44})),
    B("Divide both sides by 4, by halving twice. Half of 176 is 88, and half of 88 is 44. So x equals 44.",
      divide("l5", "4"), W("l6", "176 ÷ 2 = 88"), W("l7", "88 ÷ 2 = 44"), LV("l8", "x = 44", {"x": 44})),
    B("x is 44. Is 44 degrees the greatest angle?",
      ask=choose(["Yes: x is the greatest", "Not yet: work out all 3 angles"], 1,
                 "x is only one of the angles. We have to work out the other two before we can say which is the greatest.")),
    B("The first angle is 44 degrees. The second is 44 plus 10, which is 54 degrees. The third is 2 times 44, minus 6, which is 82 degrees.",
      W("l9", "44 + 10 = 54"), W("l10", "2 × 44 − 6 = 82"),
      FIG("f2", kind="triangle", shape="scalene", angles={"a": "44°", "b": "54°", "c": "82°"}, highlight=["c"])),
    B("Check that they make a triangle: 44 plus 54 plus 82 is 180. Good.",
      W("l11", "44 + 54 + 82 = 180")),
    B("The angles are 44, 54 and 82 degrees. So the greatest angle is 82 degrees.",
      W("l12", "Greatest angle = 82°", tone="answer", label=True), mark("l12", "82°", "circle")),
    B("Careful with the last angle: 2 times 44 is 88, but we still have to take away the 6. So: angles add up to 180, find x, then work out every angle."),
], "authored")


# Right-angled triangle with sides 9 cm, 40 cm and 41 cm. Area?
LESSONS["EXT_G5_FP_2019_036"] = lesson([
    B("Here is a right-angled triangle. Its 3 sides are 9 centimetres, 40 centimetres and 41 centimetres. We want its area.",
      W("l1", "Right-angled triangle: sides 9 cm, 40 cm, 41 cm", tone="given", label=True),
      W("l2", "Area = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"})),
    B("For the area we need a base, and a height that stands straight up from it, at a right angle. So which two sides meet at the right angle?",
      ask=choose(["9 and 41", "40 and 41", "9 and 40"], 2,
                 "The longest side, 41, is the slanting one, opposite the right angle. The two shorter sides, 9 and 40, make the square corner.")),
    B("The two shorter sides make the right angle. So the base is 40 and the height is 9. Now watch: I draw a rectangle around the triangle, 40 long and 9 tall.",
      FIG("f2", kind="triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"}, enclose=True, highlight=["ab", "bc"])),
    B("The rectangle's area is base times height. 4 times 9 is 36, so 40 times 9 is 360.",
      W("l3", "Rectangle area = base × height", label=True), W("l3b", "4 × 9 = 36"), W("l4", "40 × 9 = 360")),
    B("The slanting side cuts that rectangle into two equal triangles. So what is the area of ours?",
      ask=choose(["360", "360 ÷ 2", "360 × 2"], 1,
                 "Our triangle is only half of the rectangle. So we need half of 360.")),
    B("The triangle is half of the rectangle. Half of 360 is 180. That is the rule: half of base times height.",
      W("l5", "Triangle area = ½ × base × height", label=True), mark("l5", "½", "circle"), W("l6", "½ × 40 × 9 = 180")),
    B("So the area is 180 square centimetres.",
      W("l7", "Area = 180 sq. cm", tone="answer", label=True), mark("l7", "180 sq. cm", "circle"),
      FIG("f3", kind="triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"}, enclose=True,
          highlight=["fill"], note="Area = 180 sq. cm")),
    B("Notice that we never used the 41. The longest side is not a base or a height here, so it plays no part in the area. And do not forget the half."),
], "authored")
