"""Geometry lessons written for one question each: rectangles from a perimeter, turns, letters."""
from geometry_lib import (B, FIG, LV, W, arc, choose, group, lesson, mark)
from geometry_rules import times_beats

LESSONS = {}


def two_to_one(perimeter, opening, given, find, closing):
    """A rectangle whose length is twice its breadth, known only by its perimeter.
    Taught with parts: breadth 1 part, length 2 parts, so the walk round is 6 parts."""
    part = perimeter // 6
    assert part * 6 == perimeter
    length, breadth = 2 * part, part
    half = length + breadth
    area = length * breadth
    asked = "Area = ?" if find == "area" else "Length = ?"
    beats = [
        B(opening, W("l1", given, tone="given", label=True),
          W("l2", "Perimeter = %d cm. %s" % (perimeter, asked), tone="given", label=True),
          FIG("f1", kind="rectangle", proportion=2, length="length", breadth="breadth", note="Perimeter = %d cm" % perimeter)),
        B("We do not know either side yet, so let's think in parts. Call the breadth 1 part. The length is twice as long, so it is 2 parts.",
          FIG("f2", kind="rectangle", proportion=2, length="2 parts", breadth="1 part")),
        B("Now walk all the way round the rectangle: a length, a breadth, another length, another breadth. How many parts is the whole walk?",
          ask=choose(["3 parts", "4 parts", "6 parts"], 2,
                     "One length and one breadth make 3 parts, but that is only halfway round. The whole walk is 2 plus 1 plus 2 plus 1, which is 6 parts.")),
        B("The whole walk is 6 parts, and we know the walk is %d centimetres. So 1 part is %d divided by 6, which is %d centimetres." % (perimeter, perimeter, part),
          W("l3", "2 + 1 + 2 + 1 = 6"), W("l4", "%d ÷ 6 = %d" % (perimeter, part))),
        B("So the breadth, 1 part, is %d centimetres. And the length, 2 parts, is 2 times %d, which is %d centimetres." % (part, part, length),
          W("l5", "2 × %d = %d" % (part, length)),
          FIG("f3", kind="rectangle", proportion=2, length="%d cm" % length, breadth="%d cm" % breadth)),
        B("Let's check the walk. %d plus %d is %d, and that is halfway. Double it: %d plus %d is %d. Just what we were told." % (
            length, breadth, half, half, half, perimeter),
          W("l6", "%d + %d = %d" % (length, breadth, half)), W("l7", "%d + %d = %d" % (half, half, perimeter))),
    ]
    if find == "length":
        beats += [
            B("The question asks for the length. The length is %d centimetres." % length,
              W("l8", "Length = %d cm" % length, tone="answer", label=True), mark("l8", "%d cm" % length, "circle"),
              FIG("f4", kind="rectangle", proportion=2, length="%d cm" % length, breadth="%d cm" % breadth, highlight=["length"])),
            B(closing),
        ]
    else:
        beats += [
            B("Now for the area, the space inside. Which sum gives it?",
              ask=choose(["%d + %d" % (length, breadth), "%d × %d" % (length, breadth), "2 × (%d + %d)" % (length, breadth)], 1,
                         "Adding the sides is for the walk round the edge. Area is rows of little squares, so we multiply the length by the breadth.")),
        ]
        beats += times_beats(length, breadth, "l8")
        beats += [
            B("So the area is %d square centimetres." % area,
              W("l9", "Area = %d sq. cm" % area, tone="answer", label=True), mark("l9", "%d sq. cm" % area, "circle"),
              FIG("f4", kind="rectangle", proportion=2, length="%d cm" % length, breadth="%d cm" % breadth,
                  inside="%d sq. cm" % area, highlight=["fill"])),
            B(closing),
        ]
    return lesson(beats, "authored")


LESSONS["EXT_G5_FP_2017_019"] = two_to_one(
    48,
    "Here is a rectangle whose breadth is half of its length. The perimeter is 48 centimetres, and we want the area.",
    "Rectangle: breadth = half the length", "area",
    "So when you know how the sides compare, think in parts. Find one part from the perimeter, then the sides, then the area.")

LESSONS["EXT_G5_FP_2019_001"] = two_to_one(
    90,
    "Here is a rectangle whose length is twice its breadth. The perimeter is 90 centimetres, and we want the area.",
    "Rectangle: length = twice the breadth", "area",
    "So: breadth 1 part, length 2 parts, the walk round 6 parts. One part from the perimeter gives both sides, and the sides give the area.")

LESSONS["EXT_G5_FP_2022_029"] = two_to_one(
    84,
    "The perimeter of a rectangle is 84 centimetres, and its breadth is half of its length. We want the length.",
    "Rectangle: breadth = half the length", "length",
    "The trap here is 42. That is half the perimeter: the length and the breadth together, not the length alone.")


# Cycling North-East, turns left, now cycling West. How many degrees?
LESSONS["EXT_G5_FP_2017_023"] = lesson([
    B("A man is cycling towards the North-East. He turns to his left until he is cycling towards the West. How big was his turn?",
      W("l1", "Facing North-East. Turns left. Now facing West.", tone="given", label=True),
      W("l2", "Turn = ?", tone="given", label=True),
      FIG("f1", kind="compass", facing="NE")),
    B("First, which way round the compass is a turn to the left?",
      ask=choose(["clockwise", "anticlockwise"], 1,
                 "Face North-East and lift your left arm. It points round towards North. That is the anticlockwise way, against the hands of a clock.")),
    B("A left turn goes anticlockwise. Now, the compass has 8 points, spaced evenly round a full turn of 360 degrees. 360 divided by 8 is 45. So each step from one point to the next is 45 degrees.",
      W("l3", "Full turn = 360°, 8 compass points", label=True), W("l4", "360 ÷ 8 = 45")),
    B("Let's take the turn one step at a time. The first step to the left goes from North-East to North. That is 45 degrees.",
      W("l5", "North-East to North: 45°", label=True),
      FIG("f2", kind="compass", facing="NE", turns=[{"degrees": 45, "direction": "anticlockwise"}], showEnd=True)),
    B("The second step goes from North to North-West. Another 45 degrees, so 90 degrees so far.",
      W("l6", "45 + 45 = 90"),
      FIG("f3", kind="compass", facing="NE", turns=[{"degrees": 45, "direction": "anticlockwise"},
                                                    {"degrees": 45, "direction": "anticlockwise"}], showEnd=True)),
    B("He is facing North-West now. But he needs to face West. What is his total turn going to be?",
      ask=choose(["90", "90 + 45", "90 + 90"], 1,
                 "A turn of 90 degrees only reaches North-West. West is one more step of 45 degrees further round.")),
    B("One more step, from North-West to West. 90 plus 45 is 135. That is 3 steps of 45 degrees.",
      W("l7", "90 + 45 = 135"), W("l8", "3 × 45 = 135"),
      FIG("f4", kind="compass", facing="NE", turns=[{"degrees": 135, "direction": "anticlockwise"}], showEnd=True)),
    B("So he turned 135 degrees to his left.",
      W("l9", "Turn = 135° to the left", tone="answer", label=True), mark("l9", "135°", "circle")),
    B("So for any turn on a compass: count the steps between the points, and each step is 45 degrees."),
], "authored")


# Rectangle with length (4a + 3b) and breadth (3a − b). Perimeter?
LESSONS["EXT_G5_FP_2017_030"] = lesson([
    B("This rectangle has its sides written with letters. The length is 4 a plus 3 b, and the breadth is 3 a minus b. We want the perimeter.",
      W("l1", "Rectangle: length (4a + 3b), breadth (3a − b)", tone="given", label=True),
      W("l2", "Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="4a + 3b", breadth="3a − b")),
    B("Perimeter is the walk all the way round: 2 lengths and 2 breadths. So we add the length and the breadth, and then double.",
      W("l3", "Perimeter = 2 × (length + breadth)", label=True)),
    B("First, the length plus the breadth. Which terms are we allowed to add together?",
      W("l4", "(4a + 3b) + (3a − b)", label=True),
      ask=choose(["a's with a's, and b's with b's", "a's with b's", "all the numbers: 4 + 3 + 3"], 0,
                 "a and b are different things, like apples and bananas. We can only add apples to apples, and bananas to bananas.")),
    B("The a's first. 4 a plus 3 a makes 7 a.",
      group("l4", ["4a", "3a"], "7a")),
    B("Now the b's. Careful: minus b means take away 1 b. So 3 b take away 1 b leaves 2 b. One length and one breadth make 7 a plus 2 b.",
      group("l4", ["3b", "− b"], "2b"),
      LV("l5", "(4a + 3b) + (3a − b) = 7a + 2b", {"a": 2, "b": 3}, {"a": 5, "b": 1})),
    B("Is 7 a plus 2 b the perimeter?",
      ask=choose(["Yes, that is all 4 sides", "No, it is only halfway round"], 1,
                 "One length and one breadth are only 2 of the 4 sides. That is halfway round, so we still have to double it.")),
    B("It is only halfway round, so we double it. The 2 multiplies both terms: 2 times 7 a is 14 a, and 2 times 2 b is 4 b.",
      LV("l6", "2 × (7a + 2b) = 14a + 4b", {"a": 2, "b": 3}, {"a": 5, "b": 1}), arc("l6", "2", ["7a", "2b"])),
    B("So the perimeter is 14 a plus 4 b.",
      W("l7", "Perimeter = 14a + 4b", tone="answer", label=True), mark("l7", "14a + 4b", "circle"),
      FIG("f2", kind="rectangle", length="4a + 3b", breadth="3a − b", highlight=["border"], note="Perimeter = 14a + 4b")),
    B("Let's test it with easy numbers. Say a is 1 and b is 1. Then the length is 7 and the breadth is 2, so the perimeter is 2 times 9, which is 18. And 14 plus 4 is 18 as well.",
      W("l8", "2 × (7 + 2) = 18"), W("l9", "14 + 4 = 18")),
    B("So with letters the method is the same as with numbers: add length and breadth, keeping a's with a's and b's with b's, and then double everything."),
], "authored")


# The perimeter of a square ground is 120 m. What is its area?
LESSONS["EXT_G5_FP_2017_040"] = lesson([
    B("Here is a square piece of ground. The walk all the way round it, its perimeter, is 120 metres. We want its area.",
      W("l1", "Square ground: perimeter 120 m. Area = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", square=True, length="?", note="Perimeter = 120 m")),
    B("For the area we need the side, and we are not given it. But the perimeter is made of the sides. So how do we get one side from 120?",
      ask=choose(["120 ÷ 2", "120 ÷ 4", "120 × 4"], 1,
                 "A square has 4 equal sides, and together they make 120. So one side is 120 shared into 4 equal parts.")),
    B("4 equal sides share the 120 metres. 120 divided by 4 is 30. So each side is 30 metres.",
      W("l2", "Side = perimeter ÷ 4", label=True), W("l3", "120 ÷ 4 = 30"),
      FIG("f2", kind="rectangle", square=True, length="30 m", breadth="30 m", inside="Area = ?")),
    B("Now the area, the space inside the square. Which sum gives it?",
      ask=choose(["30 × 4", "30 + 30", "30 × 30"], 2,
                 "30 times 4 takes us straight back to the perimeter. Area is the space inside: side times side.")),
    B("Area of a square is side times side. 3 times 3 is 9, and the two zeros come along: 30 times 30 is 900.",
      W("l4", "Area of square = side × side", label=True), W("l5", "30 × 30 = 900")),
    B("So the area is 900 square metres.",
      W("l6", "Area = 900 sq. m", tone="answer", label=True), mark("l6", "900 sq. m", "circle"),
      FIG("f3", kind="rectangle", square=True, length="30 m", breadth="30 m", inside="900 sq. m", highlight=["fill"])),
    B("Check the side: 4 times 30 is 120, the perimeter we were given.",
      W("l7", "4 × 30 = 120")),
    B("So the chain is: perimeter, then side, then area. And notice the units: plain metres for the walk round, square metres for the space inside."),
], "authored")
