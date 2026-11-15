"""Geometry lessons written for one question each: worksheet one-offs and the 2016 to 2017 papers."""
from geometry_lib import (B, FIG, LV, T, W, both, choose, divide, group, lesson, mark, strike)

LESSONS = {}

HALF_TURN_IF_NOT = "A straight line is a half turn, and a half turn is 180 degrees. 90 is for a square corner, and 360 is for a full turn."


# 6² + Z² = 10². Find the value of Z.
LESSONS["EXT_G5_WS_B5_012"] = lesson([
    B("Here is our puzzle. 6 squared, plus Z squared, equals 10 squared. We need to find Z.",
      LV("l1", "6² + Z² = 10²", {"Z": 8}, tone="given"),
      FIG("f1", kind="triangle", shape="right", sides={"ab": "6", "bc": "Z", "ca": "10"})),
    B("A sum like this comes from a right-angled triangle. The squares of the two short sides add up to the square of the longest side. Let's start with the squares we can work out. What is 6 squared?",
      ask=choose(["12", "36", "62"], 1,
                 "Squared means the number times itself, not times 2. So 6 squared is 6 times 6, which is 36.")),
    B("6 squared is 6 times 6, which is 36. And 10 squared is 10 times 10, which is 100.",
      W("l2", "6² = 36"), W("l3", "10² = 100")),
    B("So now our puzzle reads: 36, plus Z squared, equals 100.",
      LV("l4", "36 + Z² = 100", {"Z": 8}), mark("l4", "Z²", "circle")),
    B("To get Z squared on its own, we take 36 away from both sides. 100 take away 36 leaves 64.",
      strike("l4", "36 +", "− 36"), both("l4", "− 36"), W("l5", "100 − 36 = 64"), LV("l6", "Z² = 64", {"Z": 8})),
    B("Z squared is 64. Are we finished?",
      ask=choose(["Yes: Z is 64", "No: halve 64", "No: find what squares to 64"], 2,
                 "64 is Z squared, not Z. We still need the number that, multiplied by itself, makes 64.")),
    B("Which number times itself makes 64? 8 times 8. So Z equals 8.",
      W("l7", "√64 = 8"), LV("l8", "Z = 8", {"Z": 8}, tone="answer"), mark("l8", "Z = 8", "circle"),
      FIG("f2", kind="triangle", shape="right", sides={"ab": "6", "bc": "8", "ca": "10"}, highlight=["bc"])),
    B("Let's check. 6 squared is 36 and 8 squared is 64. 36 plus 64 is 100, and 100 is 10 squared. It works.",
      W("l9", "36 + 64 = 100"), W("l10", "6² + 8² = 10²")),
    B("So the plan is: work out the squares you know, subtract to find the missing square, then find its square root. Do not stop at the square."),
], "authored")


# Square sides (2a+5)cm and (3a−1)cm. Find perimeter.
LESSONS["EXT_G5_WS_B6_021"] = lesson([
    B("Here is a square. Two of its sides are written with a letter: 2 a plus 5, and 3 a minus 1. We want the perimeter.",
      W("l1", "Square: sides (2a + 5) cm and (3a − 1) cm", tone="given", label=True),
      W("l2", "Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", square=True, length="(2a + 5) cm", breadth="(3a − 1) cm")),
    B("Before any working, think about the shape. What do we know about the sides of a square?",
      ask=choose(["only opposite sides are equal", "all 4 sides are equal", "the sides add up to 180"], 1,
                 "A square is special: all 4 of its sides are the same length. So these two sides must be equal to each other.")),
    B("All 4 sides are equal, so these two sides are equal. And that gives us an equation.",
      LV("l3", "2a + 5 = 3a − 1", {"a": 6})),
    B("There are more a's on the right, so let's collect them there. We take 2 a away from both sides. On the right, 3 a take away 2 a leaves just a.",
      strike("l3", "2a", "− 2a"), both("l3", "− 2a"), LV("l4", "5 = a − 1", {"a": 6})),
    B("Now undo the minus 1 by adding 1 to both sides. 5 plus 1 is 6. So a equals 6.",
      strike("l4", "− 1", "+ 1"), both("l4", "+ 1"), LV("l5", "a = 6", {"a": 6})),
    B("We have found that a equals 6. Is 6 the side of the square?",
      ask=choose(["No: put 6 into 2a + 5", "Yes: the side is 6", "No: the side is 4 × 6"], 0,
                 "a is only the value of the letter. The side is 2 a plus 5, so we put 6 in place of a.")),
    B("Put 6 in place of a. 2 times 6, plus 5, is 17. And the other side: 3 times 6, minus 1, is also 17. They agree, just as a square should.",
      W("l6", "2 × 6 + 5 = 17"), W("l7", "3 × 6 − 1 = 17"),
      FIG("f2", kind="rectangle", square=True, length="17 cm", breadth="17 cm")),
    B("Perimeter is the walk all the way round, along all 4 equal sides. 4 times 17 is 68.",
      W("l8", "Perimeter of square = 4 × side", label=True), W("l9", "4 × 17 = 68")),
    B("So the perimeter is 68 centimetres.",
      W("l10", "Perimeter = 68 cm", tone="answer", label=True), mark("l10", "68 cm", "circle"),
      FIG("f3", kind="rectangle", square=True, length="17 cm", breadth="17 cm", highlight=["border"], note="Perimeter = 68 cm")),
    B("So the chain is: equal sides give an equation, the equation gives a, a gives the side, and the side gives the perimeter. The trap is to stop at a."),
], "authored")


# Triangle angles y°, (y−15)°, (7y+24)°. Smallest angle?
LESSONS["EXT_G5_WS_B6_022"] = lesson([
    B("Here is a triangle whose 3 angles are written with the letter y. They are y, y minus 15, and 7 y plus 24. We want the smallest angle.",
      W("l1", "Triangle angles: y°, (y − 15)°, (7y + 24)°", tone="given", label=True),
      W("l2", "Smallest angle = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="scalene", angles={"a": "y°", "b": "(y − 15)°", "c": "(7y + 24)°"})),
    B("Whatever y is, these are the 3 angles of a triangle. What do the 3 angles of a triangle always add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "Tear the corners off a paper triangle and line them up. They make a straight line, a half turn. That is 180 degrees.")),
    B("The 3 angles of a triangle make 180 degrees. So we add our 3 angles and set them equal to 180.",
      LV("l3", "y + (y − 15) + (7y + 24) = 180", {"y": 19})),
    B("Gather the y's first. 1 y, another y, and 7 y make 9 y. Then the plain numbers: minus 15 and plus 24 together make plus 9.",
      group("l3", [T("y", 1), T("y", 2), T("7y")], "9y"), LV("l4", "9y + 9 = 180", {"y": 19})),
    B("Take 9 away from both sides. 180 take away 9 leaves 171.",
      strike("l4", "+ 9", "− 9"), both("l4", "− 9"), LV("l5", "9y = 171", {"y": 19})),
    B("Now divide both sides by 9. 171 divided by 9 is 19. So y equals 19.",
      divide("l5", "9"), W("l6", "171 ÷ 9 = 19"), LV("l7", "y = 19", {"y": 19})),
    B("y is 19. Is 19 degrees our answer?",
      ask=choose(["Yes: y is the smallest angle", "Not yet: work out all 3 angles"], 1,
                 "y is one of the angles, but there are two more. We have to work out all 3 before we can say which is the smallest.")),
    B("The first angle is y, which is 19 degrees. The second is 19 minus 15, which is 4 degrees. The third is 7 times 19, plus 24, which is 157 degrees.",
      W("l8", "19 − 15 = 4"), W("l9", "7 × 19 + 24 = 157"),
      FIG("f2", kind="triangle", shape="scalene", angles={"a": "19°", "b": "4°", "c": "157°"}, highlight=["b"])),
    B("Check that they really make a triangle. 19 plus 4 plus 157 makes 180. Good.",
      W("l10", "19 + 4 + 157 = 180")),
    B("The 3 angles are 19, 4 and 157 degrees. So the smallest angle is 4 degrees.",
      W("l11", "Smallest angle = 4°", tone="answer", label=True), mark("l11", "4°", "circle")),
    B("So: the angles add up to 180, that gives y, and then y gives every angle. The trap is to stop at y, because y is not always the smallest."),
], "authored")


# Rectangle: one side 8 cm, perimeter 40 cm. Find the area.
LESSONS["EXT_G5_FP_2016_015"] = lesson([
    B("Here is a rectangle. One side is 8 centimetres and the perimeter is 40 centimetres. We want the area.",
      W("l1", "Rectangle: one side 8 cm, perimeter 40 cm", tone="given", label=True),
      W("l2", "Area = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="?", breadth="8 cm", note="Perimeter = 40 cm")),
    B("For the area we need both sides, and we only have one. The perimeter will give us the other. Remember, the perimeter is the walk all the way round: 2 lengths and 2 breadths.",
      W("l2b", "Perimeter = 2 lengths + 2 breadths", label=True)),
    B("The whole walk is 40. So how far is just one length plus one breadth?",
      ask=choose(["40 ÷ 4", "40 − 8", "40 ÷ 2"], 2,
                 "One length and one breadth take us exactly halfway round. So it is half of 40. Dividing by 4 only works for a square.")),
    B("One length and one breadth are halfway round. Half of 40 is 20.",
      W("l3", "length + breadth = half the perimeter", label=True), W("l4", "40 ÷ 2 = 20")),
    B("The two sides together make 20, and one of them is 8. So the other side is 20 take away 8, which is 12 centimetres.",
      W("l5", "20 − 8 = 12"), FIG("f2", kind="rectangle", length="12 cm", breadth="8 cm", inside="Area = ?")),
    B("Now we have both sides, 12 and 8. Which sum gives the area?",
      ask=choose(["12 × 8", "12 + 8", "2 × (12 + 8)"], 0,
                 "Area is the space inside, rows of little squares. So we multiply the length by the breadth. Adding is for the walk round the edge.")),
    B("Area is length times breadth. 12 times 8 is 96.",
      W("l6", "Area = length × breadth", label=True), W("l7", "12 × 8 = 96")),
    B("So the area is 96 square centimetres.",
      W("l8", "Area = 96 cm²", tone="answer", label=True), mark("l8", "96 cm²", "circle"),
      FIG("f3", kind="rectangle", length="12 cm", breadth="8 cm", inside="96 cm²", highlight=["fill"])),
    B("Check the walk round. 12 plus 8 is 20, and double 20 is 40. That is the perimeter we were given.",
      W("l9", "2 × (12 + 8) = 40")),
    B("So: halve the perimeter to get length plus breadth, take away the side you know, then multiply the two sides. The trap is to treat the perimeter as if it were a side."),
], "authored")
