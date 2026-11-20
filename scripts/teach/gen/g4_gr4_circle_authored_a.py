"""Lessons written one by one: Grade 4 circles, past-paper and worksheet questions."""
from g4_gr4_quads_lib import A, B, FIG, G, L, T, THINK, W, box, choose, figure_getter, group, lesson, mark, note, ring, strike

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


def CIRCLE(**kw):
    spec = {"kind": "circle"}
    spec.update(kw)
    return FIG("f", spec)


LESSONS["EXT_G4_FP_2020_006"] = lesson([
    B("Pick one point on a circle. How many diameters can be drawn from that point?",
      G("How many diameters from one point on a circle?"), CIRCLE(note="One point on the circle")),
    B("First, what is a diameter? It is a straight line right across the circle that passes through the centre.",
      L("l1", "Diameter: passes through the centre"), mark("l1", "through the centre"), F("EXT_G4_FP_2020_006", 0)),
    B("From our point we can draw lots of straight lines across the circle. A line that misses the centre is called what?",
      ask=choose(["a diameter", "a chord", "a radius"], 1,
                 "A line joining two points on the circle is a chord. It only earns the name diameter if it passes through the centre.")),
    B("So from our point there are plenty of chords. But a diameter has to aim straight at the centre.",
      L("l2", "misses the centre: just a chord")),
    B("And there is only one way to aim straight at the centre: go through it and carry on to the other side.",
      F("EXT_G4_FP_2020_006", 3)),
    B("So from one point on the circle, only 1 diameter can be drawn.", A("a", "Only 1 diameter", label=True), ring("a", "1")),
    B("The trap is the word many. A whole circle has endless diameters, but each one starts from a different point."),
])

LESSONS["EXT_G4_FP_2021_024"] = lesson([
    B("For this circle, the area is 3 times the circumference, just as numbers. We have to find the radius.",
      G("Area of circle = 3 × circumference (as numbers)"), GQ("q2", "Radius = ?"), F("EXT_G4_FP_2021_024")),
    B("We need the two rules. Area is pi times r times r. Circumference is 2 times pi times r.",
      L("l1", "Area = π × r × r"), L("l2", "Circumference = 2 × π × r")),
    B("3 lots of the circumference is 3 times 2 times pi times r. 3 times 2 is 6, so that is 6 times pi times r.",
      W("l3", "3 × 2 = 6"), L("l4", "3 × circumference = 6 × π × r")),
    B("Now put the two side by side. Pi times r times r on the left. Pi times r times 6 on the right. Both have pi times r.",
      L("l5", "π × r × r  =  π × r × 6"), group("l5", [T("π × r"), T("π × r", 2)], "the same")),
    B("Cover up the pi times r on both sides. What must the last r be, to make the two sides equal?",
      ask=choose(["2", "3", "6"], 2,
                 "On the left, one r is still showing. On the right, the 6 is showing. For the sides to be equal, these two must be the same.")),
    B("The r that is left must equal 6. So the radius is 6.", A("a", "Radius = 6", label=True), ring("a", "6")),
    B("Check. With a radius of 6, r times r is 36. And 6 times r is 36 too. Both sides are 36 lots of pi.",
      W("c", "6 × 6 = 36")),
    B("No big sums were needed. When both sides share the same pieces, cover them up and compare what is left."),
])

LESSONS["EXT_G4_FP_2022_020"] = lesson([
    B("The circumference and the area of a circle are the same number. We want the diameter.",
      G("Circumference and area of a circle: same number"), GQ("q2", "Diameter = ?"), F("EXT_G4_FP_2022_020")),
    B("Write the two rules. Circumference is 2 times pi times r. Area is pi times r times r.",
      L("l1", "Circumference = 2 × π × r"), L("l2", "Area = π × r × r")),
    B("They are equal. Pi times r times 2 on one side, pi times r times r on the other. Both sides have pi times r.",
      L("l3", "π × r × 2  =  π × r × r"), group("l3", [T("π × r"), T("π × r", 2)], "the same")),
    B("Cover up the pi times r on both sides. What is left on each side?",
      ask=choose(["2 and r", "2 and 2", "r and r"], 0,
                 "On the left, after covering pi times r, the 2 is left. On the right, one r is left.")),
    B("A 2 is left on one side and an r on the other. So r must be 2. The radius is 2 centimetres.",
      L("l4", "r = 2")),
    B("Careful! Is 2 our answer? Read the question again. It asks for the diameter, not the radius.",
      box("q2", "Diameter")),
    B("The diameter is twice the radius. 2 times 2 is 4.", W("l5", "2 × 2 = 4")),
    B("The diameter is 4 centimetres.", A("a", "Diameter = 4 cm", label=True), ring("a", "4")),
    B("Check: with radius 2, the circumference is 2 times 2 lots of pi, and the area is 2 times 2 lots of pi. Both are 4 lots of pi."),
])

LESSONS["EXT_G4_FP_2022_033"] = lesson([
    B("Eight equal circles sit inside a rectangle in 2 rows of 4, touching each other and the sides. Each radius is 7 centimetres. What is the area of the rectangle?",
      G("8 circles in a rectangle: 2 rows of 4"), GQ("q2", "Radius = 7 cm. Area of rectangle = ?"),
      F("EXT_G4_FP_2022_033")),
    B("The circles fill the rectangle from side to side. So how much room does one whole circle take up, from edge to edge?",
      ask=choose(["7 cm", "14 cm", "28 cm"], 1,
                 "7 centimetres only reaches from the centre to the edge. From edge to edge is the diameter, which is two radii.")),
    B("That's the trap: use the diameter, not the radius. 2 times 7 is 14 centimetres.",
      W("l1", "2 × 7 = 14"), note("l1", "14", "diameter", "below"), F("EXT_G4_FP_2022_033", 0)),
    B("4 circles fit along the length. 4 times 14 is 56 centimetres.", W("l2", "4 × 14 = 56"), F("EXT_G4_FP_2022_033", 1)),
    B("2 circles fit up the side. 2 times 14 is 28 centimetres.", W("l3", "2 × 14 = 28"), F("EXT_G4_FP_2022_033", 2)),
    B("Area is length times breadth: 56 times 28. Split 28 into 20 and 8.", W("l4", "56 × 28 = 56 × 20 + 56 × 8")),
    B("56 times 20 is 1120. 56 times 8 is 448.", W("l5", "56 × 20 = 1120"), W("l6", "56 × 8 = 448")),
    B("Add the parts: 1120 plus 448 makes 1568.", W("l7", "1120 + 448 = 1568")),
    B("The area of the rectangle is 1568 square centimetres.", A("a", "Area = 1568 sq.cm", label=True), ring("a", "1568")),
    B("So: radius to diameter, count the circles each way to get the sides, then multiply."),
])

LESSONS["EXT_G4_FP_2023_033"] = lesson([
    B("The circumference of a circle is 132 centimetres. We want its area.",
      G("Circle: circumference = 132 cm. Area = ?"), L("p", "π = 22/7"), F("EXT_G4_FP_2023_033")),
    B("We can't get the area straight from the circumference. What must we find first?",
      ask=choose(["the radius", "the perimeter", "half of 132"], 0,
                 "The area rule is pi times radius times radius. So we need the radius, and the circumference can give it to us.")),
    B("Circumference is 2 times 22 over 7 times r. 2 times 22 is 44. So it is 44 times r, divided by 7.",
      L("l1", "Circumference = 2 × 22/7 × r"), W("l2", "2 × 22 = 44")),
    B("44 times something makes 132. Try it: 44 and 44 and 44 make 132. That is 3 lots.",
      W("l3a", "44 + 44 + 44 = 132"), W("l3", "132 ÷ 44 = 3")),
    B("So r divided by 7 is 3. That means r is 3 times 7, which is 21 centimetres.", W("l4", "3 × 7 = 21"),
      note("l4", "21", "radius", "below")),
    B("Now the area: 22 over 7, times 21, times 21. Let the 7 divide first: 21 divided by 7 is 3.",
      W("l5", "22/7 × 21 × 21"), strike("l5", "7"), W("l6", "21 ÷ 7 = 3")),
    B("That leaves 22 times 3 times 21. 22 times 3 is 66.", W("l7", "22 × 3 = 66")),
    B("66 times 21: 66 times 20 is 1320, and one more 66 makes 1386.", W("l8", "66 × 20 = 1320"), W("l9", "1320 + 66 = 1386")),
    B("The area is 1386 square centimetres.", A("a", "Area = 1386 sq.cm", label=True), ring("a", "1386")),
    B("Two stages: circumference gives the radius, then the radius gives the area. Don't rush the last multiplying."),
])

LESSONS["EXT_G4_FP_2025_015"] = lesson([
    B("A circle's circumference equals the perimeter of a rectangle, 14 centimetres by 8 centimetres. We want the circle's radius.",
      G("Circumference = perimeter of rectangle 14 cm by 8 cm"), GQ("q2", "Radius = ?  (π = 22/7)"),
      F("EXT_G4_FP_2025_015")),
    B("Start with the rectangle. 14 plus 8 is 22, and that is halfway round. Double it: 44 centimetres.",
      W("l1", "14 + 8 = 22"), W("l2", "2 × 22 = 44")),
    B("So the circle's circumference is 44 centimetres too. The rule is 2 times 22 over 7 times r.",
      L("l3", "Circumference = 2 × 22/7 × r")),
    B("2 times 22 is 44. So the circumference is 44 times r, divided by 7. And we know it equals 44.",
      W("l4", "2 × 22 = 44"), L("l5", "44 × r ÷ 7 = 44")),
    B("44 times r, divided by 7, gives back 44. So what must r divided by 7 be?",
      ask=choose(["1", "7", "44"], 0,
                 "44 times something gives 44 again. Only multiplying by 1 leaves a number unchanged.")),
    B("r divided by 7 is 1. So r is 7. The radius is 7 centimetres.",
      A("a", "Radius = 7 cm", label=True), ring("a", "7")),
    B("Check: 2 times 22 over 7 times 7. The 7s cancel, leaving 2 times 22, which is 44. It fits.",
      W("c", "2 × 22/7 × 7 = 44")),
    B("Careful with 14: that is the diameter of this circle, and also a side of the rectangle. The radius is 7."),
])

LESSONS["EXT_G4_WS2_CH21_001"] = lesson([
    B("What do we call the distance from the centre of a circle to any point on the circle?",
      G("Centre to any point on the circle: called the ?"), F("EXT_G4_WS2_CH21_001")),
    B("Imagine drawing a circle with a compass. The needle sits at the centre, and the pencil goes round.",
      CIRCLE(radius="?", highlight=["radius"])),
    B("The gap between the needle and the pencil never changes. So every point on the circle is the same distance from the centre.",
      L("l1", "centre to circle: always the same")),
    B("That fixed distance has a name. Which one is it?",
      ask=choose(["diameter", "radius", "circumference"], 1,
                 "The diameter goes all the way across. The circumference goes all the way round. From the centre out to the circle is the radius.")),
    B("It is the radius: from the centre to the circle.", A("a", "The radius", label=True), ring("a", "radius"),
      CIRCLE(radius="radius", highlight=["radius"])),
    B("Think of the spokes of a cycle wheel. Each spoke runs from the centre to the rim, and each one is a radius."),
    B("So: centre to edge is the radius. Right across through the centre is the diameter."),
])

LESSONS["EXT_G4_WS2_CH21_002"] = lesson([
    B("How does the diameter of a circle compare with its radius?",
      G("The diameter of a circle is: ?"), F("EXT_G4_WS2_CH21_002")),
    B("A radius goes from the centre out to the circle. A diameter goes right across the circle, through the centre.",
      L("l1", "radius: centre to circle"), L("l2", "diameter: right across, through the centre")),
    B("Walk along a diameter. You start on the circle, reach the centre, and carry on to the other side. How many radii did you walk?",
      ask=choose(["1", "2", "3"], 1,
                 "From the edge to the centre is one radius. From the centre on to the other edge is one more.")),
    B("One radius to the centre, and one more to the far side. 2 radii make a diameter.",
      L("l3", "diameter = radius + radius"), CIRCLE(radius="radius", diameter="diameter", highlight=["diameter"])),
    B("So the diameter is twice the radius.", A("a", "Diameter = 2 × radius", label=True), ring("a", "2 × radius")),
    B("And the other way round: the radius is half the diameter. Don't mix up which one is bigger!"),
    B("The diameter is always the longer one, because it goes all the way across."),
])

LESSONS["EXT_G4_WS2_CH21_003"] = lesson([
    B("Which is the longest chord of a circle?", G("The longest chord of a circle is the: ?"), F("EXT_G4_WS2_CH21_003")),
    B("A chord is a straight line joining two points on the circle.", L("l1", "Chord: joins two points on the circle")),
    B("Picture a short chord near the edge of the circle. Now slide it towards the middle. Does it get longer or shorter?",
      ask=choose(["longer", "shorter", "it stays the same"], 0,
                 "Near the edge the circle is narrow, so the chord is short. Towards the middle the circle is wider, so the chord grows.")),
    B("It gets longer and longer. It is longest when it reaches the widest part of the circle: right through the centre.",
      L("l2", "longest chord: through the centre"), mark("l2", "through the centre")),
    B("And a chord through the centre has a special name. It is the diameter.",
      A("a", "The diameter", label=True), ring("a", "diameter"), CIRCLE(diameter="diameter", highlight=["diameter"])),
    B("A radius can't be the answer. It starts at the centre, so it is not a chord at all."),
    B("So remember: every diameter is a chord, and it is the longest chord the circle has."),
])

LESSONS["EXT_G4_WS2_CH21_004"] = lesson([
    B("The radius of a circle is 7 centimetres. What is its diameter?",
      G("Circle: radius = 7 cm. Diameter = ?"), F("EXT_G4_WS2_CH21_004")),
    B("The radius goes from the centre to the circle. The diameter goes right across, through the centre.",
      L("l1", "diameter = radius + radius")),
    B("So is the diameter bigger or smaller than the radius?",
      ask=choose(["bigger: twice as long", "smaller: half as long"], 0,
                 "The diameter crosses the whole circle. The radius only gets as far as the centre. So the diameter is the longer one.")),
    B("The diameter is two radii, end to end. 2 times 7 is 14.", W("l2", "2 × 7 = 14")),
    B("The diameter is 14 centimetres.", A("a", "Diameter = 14 cm", label=True), ring("a", "14")),
    B("Careful not to halve. Half of 7 would be smaller than the radius, and a diameter can never be shorter than a radius."),
    B("Check: 7 and 7 make 14.", W("c", "7 + 7 = 14")),
])

LESSONS["EXT_G4_WS2_CH21_005"] = lesson([
    B("What is the boundary of a circle called?", G("The boundary of a circle is called the: ?"), F("EXT_G4_WS2_CH21_005")),
    B("The boundary is the edge: the curved line that goes all the way round the circle.",
      L("l1", "boundary = the curved line all the way round"), CIRCLE(highlight=["edge"])),
    B("For a square or a rectangle, the distance round the edge is the perimeter. A circle has its own special word for it.",
      L("l2", "square, rectangle: perimeter")),
    B("Which word is it?",
      ask=choose(["area", "diameter", "circumference"], 2,
                 "Area is the space inside. The diameter is a straight line across. The word for the curved line round the outside is circumference.")),
    B("It is the circumference.", A("a", "The circumference", label=True), ring("a", "circumference")),
    B("A way to remember: circumference starts like circle and circus. All of them are about going round."),
    B("So: radius and diameter are straight lines inside the circle. The circumference is the curved line around it."),
])
