"""Geometry lessons written for one question each: the 2020 and 2022 papers."""
from geometry_lib import (B, FIG, W, choose, group, lesson, mark)
from geometry_rules import times_beats

LESSONS = {}


# Right-angled triangle 7, 24, 25: which calculation gives its area?
LESSONS["EXT_G5_FP_2020_011"] = lesson([
    B("Here is a right-angled triangle with sides of 7, 24 and 25 centimetres. This time we are not asked for the area itself, but for a calculation that gives it.",
      W("l1", "Right-angled triangle: sides 7 cm, 24 cm, 25 cm", tone="given", label=True),
      W("l2", "Which calculation gives its area?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="right", sides={"ab": "7 cm", "bc": "24 cm", "ca": "25 cm"})),
    B("The area needs a base, and a height standing straight up from it. So which two sides meet at the right angle?",
      ask=choose(["7 and 24", "7 and 25", "24 and 25"], 0,
                 "The longest side, 25, is the slanting one, opposite the right angle. The two shorter sides, 7 and 24, make the square corner.")),
    B("The two shorter sides make the right angle, so they are the base and the height. Draw the rectangle around the triangle: the triangle is exactly half of it.",
      FIG("f2", kind="triangle", shape="right", sides={"ab": "7 cm", "bc": "24 cm", "ca": "25 cm"}, enclose=True, highlight=["ab", "bc"])),
    B("So the area is half of base times height: a half, times 24, times 7.",
      W("l3", "Triangle area = ½ × base × height", label=True), W("l4", "½ × 24 × 7", label=True)),
    B("We can do the half straight away, on the 24. So which of these is the same calculation?",
      ask=choose(["24 × 7", "12 × 7", "12 × 3.5"], 1,
                 "The half is used only once. Halve the 24 to get 12, and leave the 7 alone.")),
    B("Half of 24 is 12, so the area is 12 times 7. And 12 times 7 is the same as 7 times 12.",
      group("l4", ["½", "24"], "12"), W("l5", "½ × 24 × 7 = 12 × 7"), W("l6", "12 × 7 = 7 × 12")),
    B("So the calculation is 7 times 12.",
      W("l7", "Area = 7 × 12", tone="answer", label=True), mark("l7", "7 × 12", "circle")),
    B("7 times 12 is 84 square centimetres. Look at the traps. 3.5 times 12 halves twice and gives only 42. And the 25 should never appear: the slanting side is neither base nor height.",
      W("l8", "7 × 12 = 84"), W("l9", "3.5 × 12 = 42"),
      FIG("f3", kind="triangle", shape="right", sides={"ab": "7 cm", "bc": "24 cm", "ca": "25 cm"}, enclose=True,
          highlight=["fill"], note="Area = 84 sq. cm")),
    B("So for a right-angled triangle: the two sides at the right angle are base and height, and the area is half of their product. Halve once, and only once."),
], "authored")


# Rectangle 12 cm by 8 cm; another with the same area has length 16 cm. Width?
LESSONS["EXT_G5_FP_2020_027"] = lesson([
    B("The first rectangle is 12 centimetres long and 8 centimetres wide. A second rectangle has the same area, but it is 16 centimetres long. How wide is it?",
      W("l1", "First rectangle: 12 cm by 8 cm", tone="given", label=True),
      W("l2", "Second: same area, length 16 cm. Width = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="12 cm", breadth="8 cm", proportion=1.5)),
    B("The two rectangles share one thing. So what should we work out first?",
      ask=choose(["the perimeter: 2 × (12 + 8)", "the area: 12 × 8", "the sum: 12 + 8"], 1,
                 "The two rectangles have the same area, so the area is the bridge from the first one to the second.")),
    B("The area of the first rectangle is length times width. 12 times 8 is 96 square centimetres.",
      W("l3", "Area = length × width", label=True), W("l4", "12 × 8 = 96"),
      FIG("f2", kind="rectangle", length="12 cm", breadth="8 cm", proportion=1.5, inside="96 sq. cm", highlight=["fill"])),
    B("The second rectangle also covers 96 square centimetres, and it is 16 long. How do we find its width?",
      FIG("f3", kind="rectangle", length="16 cm", breadth="?", proportion=2.6, inside="96 sq. cm"),
      ask=choose(["96 − 16", "8 − 4", "96 ÷ 16"], 2,
                 "Area is length times width. So to get back from the area to the width, we divide by the length. Adding 4 to one side and taking 4 off the other does not keep the area the same.")),
    B("96 divided by 16 is 6, because 16 times 6 is 96. So the width is 6 centimetres.",
      W("l5", "96 ÷ 16 = 6"), W("l6", "16 × 6 = 96")),
    B("So the second rectangle is 6 centimetres wide.",
      W("l7", "Width = 6 cm", tone="answer", label=True), mark("l7", "6 cm", "circle"),
      FIG("f4", kind="rectangle", length="16 cm", breadth="6 cm", proportion=2.6, inside="96 sq. cm", highlight=["breadth"])),
    B("Notice what happened. The length grew from 12 to 16, so the width had to shrink from 8 to 6 to hold the same area. Same area: multiply for the first, divide for the second."),
], "authored")


# Perimeter 96 cm, breadth 6 cm less than the length. Area?
_area_2022_016 = times_beats(27, 21, "l9")
LESSONS["EXT_G5_FP_2022_016"] = lesson([
    B("The perimeter of a rectangle is 96 centimetres, and its breadth is 6 centimetres less than its length. We want the area.",
      W("l1", "Rectangle: perimeter 96 cm, breadth = length − 6 cm", tone="given", label=True),
      W("l2", "Area = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="length", breadth="length − 6", note="Perimeter = 96 cm")),
    B("The perimeter is the walk all the way round: 2 lengths and 2 breadths. So what do one length and one breadth add up to?",
      ask=choose(["96 ÷ 4", "96 ÷ 2", "96 − 6"], 1,
                 "One length and one breadth take us exactly halfway round. So together they are half of 96.")),
    B("Half of 96 is 48. So the length and the breadth together make 48 centimetres.",
      W("l3", "96 ÷ 2 = 48"), W("l4", "length + breadth = 48", label=True)),
    B("Now picture the two sides as bars. The breadth bar is 6 short of the length bar. If we give the breadth that extra 6, we have two equal bars, and together they make 48 plus 6, which is 54.",
      W("l5", "48 + 6 = 54"),
      FIG("f2", kind="barModel", bars=[
          {"label": "length", "segments": [{"units": 9, "label": "length"}]},
          {"label": "breadth", "segments": [{"units": 7, "label": "breadth"}, {"units": 2, "label": "6", "tone": "unknown"}]}])),
    B("Two equal bars make 54, and each one is as long as the length. So what is the length?",
      ask=choose(["48 ÷ 2", "54 ÷ 2", "54 − 6"], 1,
                 "With the extra 6 added, there are two bars of the same size making 54. So one of them is half of 54.")),
    B("Half of 54 is 27, so the length is 27 centimetres. The breadth is 6 less: 27 take away 6 is 21 centimetres.",
      W("l6", "54 ÷ 2 = 27"), W("l7", "27 − 6 = 21"),
      FIG("f3", kind="rectangle", length="27 cm", breadth="21 cm", inside="Area = ?")),
    B("Check before going on: 27 plus 21 is 48, just as it should be.",
      W("l8", "27 + 21 = 48")),
] + _area_2022_016 + [
    B("So the area is 567 square centimetres.",
      W("l10", "Area = 567 sq. cm", tone="answer", label=True), mark("l10", "567 sq. cm", "circle"),
      FIG("f4", kind="rectangle", length="27 cm", breadth="21 cm", inside="567 sq. cm", highlight=["fill"])),
    B("The trap is to halve 48 and call both sides the same. They are not equal: one is 6 longer. So deal with the difference first, then halve."),
], "authored")


# Facing south-west; 180° clockwise, then 225° anticlockwise.
LESSONS["EXT_G5_FP_2022_020"] = lesson([
    B("Mishti is facing South-West. She turns 180 degrees clockwise, and then 225 degrees anticlockwise. Which way is she facing at the end?",
      W("l1", "Facing South-West. Turns 180° clockwise,", tone="given", label=True),
      W("l2", "then 225° anticlockwise. Facing = ?", tone="given", label=True),
      FIG("f1", kind="compass", facing="SW")),
    B("We take one turn at a time. The first turn is 180 degrees, which is a half turn. Where does a half turn leave you facing?",
      ask=choose(["the same way as before", "the opposite way", "a quarter of the way round"], 1,
                 "A half turn spins you round to face exactly the other way. It does not even matter which way you turn.")),
    B("A half turn leaves her facing the opposite way. The opposite of South-West is North-East.",
      W("l3", "South-West, half turn: North-East", label=True),
      FIG("f2", kind="compass", facing="SW", turns=[{"degrees": 180, "direction": "clockwise"}], showEnd=True)),
    B("Now the second turn, 225 degrees. The compass has 8 points, spaced evenly round a full turn of 360 degrees. So each step from one point to the next is 45 degrees.",
      W("l4", "8 points in 360°: each step is 45°", label=True), W("l5", "360 ÷ 8 = 45")),
    B("How many steps of 45 make 225? 5 times 45 is 225. So she turns 5 steps.",
      W("l6", "5 × 45 = 225")),
    B("Those 5 steps are anticlockwise. Starting from North-East, which way does anticlockwise take her first?",
      ask=choose(["towards North", "towards East"], 0,
                 "Clockwise from North goes to North-East and then East. Anticlockwise is the other way round, so from North-East she goes back towards North.")),
    B("Count 5 steps anticlockwise from North-East: North, North-West, West, South-West, South.",
      W("l7", "N, NW, W, SW, S", label=True), mark("l7", "S", "circle", nth=2),
      FIG("f3", kind="compass", facing="NE", turns=[{"degrees": 225, "direction": "anticlockwise"}], showEnd=True)),
    B("So Mishti is facing South.",
      W("l8", "Facing South", tone="answer", label=True), mark("l8", "South", "circle")),
    B("Here is a quick check. 180 one way and 225 back the other way leaves just 45 degrees anticlockwise. And 1 step anticlockwise from South-West is South.",
      W("l9", "225 − 180 = 45")),
    B("So for turning questions: take one turn at a time, and count in steps of 45 degrees round the compass."),
], "authored")


# Sides (3a + 5), (7a + 10), (4a + 15); a = 5. Perimeter?
LESSONS["EXT_G5_FP_2022_028"] = lesson([
    B("The sides of this triangle are written with the letter a: 3 a plus 5, 7 a plus 10, and 4 a plus 15. When a is 5, what is the perimeter?",
      W("l1", "Triangle sides: (3a + 5), (7a + 10), (4a + 15)", tone="given", label=True),
      W("l2", "a = 5. Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="scalene", sides={"ab": "3a + 5", "bc": "7a + 10", "ca": "4a + 15"})),
    B("Wherever we see a, we put 5. But first: what does 7 a mean when a is 5?",
      ask=choose(["7 + 5", "75", "7 × 5"], 2,
                 "A number written right next to a letter means times. So 7 a is 7 times 5, not 75.")),
    B("The first side is 3 times 5, plus 5. 3 times 5 is 15, and 15 plus 5 is 20.",
      W("l3", "3 × 5 + 5 = 20")),
    B("The second side is 7 times 5, plus 10. 7 times 5 is 35, and 35 plus 10 is 45.",
      W("l4", "7 × 5 = 35"), W("l5", "7 × 5 + 10 = 45")),
    B("The third side is 4 times 5, plus 15. 4 times 5 is 20, and 20 plus 15 is 35. Now every side has a real length.",
      W("l6", "4 × 5 + 15 = 35"),
      FIG("f2", kind="triangle", shape="scalene", sides={"ab": "20", "bc": "45", "ca": "35"})),
    B("Perimeter is the walk all the way round the triangle. Which sum gives it?",
      ask=choose(["20 + 45 + 35", "20 + 45", "20 × 45 × 35"], 0,
                 "The walk goes along every side, and a triangle has 3 of them. So we add all 3 lengths.")),
    B("Add them one at a time. 20 plus 45 is 65. Then 65 plus 35 is 100.",
      W("l7", "Perimeter = side + side + side", label=True), W("l8", "20 + 45 = 65"), W("l9", "65 + 35 = 100")),
    B("So the perimeter is 100 units.",
      W("l10", "Perimeter = 100 units", tone="answer", label=True), mark("l10", "100 units", "circle"),
      FIG("f3", kind="triangle", shape="scalene", sides={"ab": "20", "bc": "45", "ca": "35"},
          highlight=["ab", "bc", "ca"], note="Perimeter = 100 units")),
    B("Another way to check: add the letters first. The 3 sides together are 14 a plus 30. And 14 times 5, plus 30, is 100 too.",
      W("l11", "14 × 5 + 30 = 100")),
    B("So: put the number in place of the letter to get each side, then add all 3 sides for the walk round."),
], "authored")
