"""Lessons written one by one: Grade 4 circles, G4A_CIRCLE_013 to 024."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["G4A_CIRCLE_013"] = lesson([
    B("A circle has a radius of 6 centimetres. Which of these cannot be the length of a chord: 4, 9, 12 or 13 centimetres?",
      G("Circle: radius 6 cm."), GQ("q2", "NOT a chord length: 4, 9, 12 or 13 cm?"), F("G4A_CIRCLE_013")),
    B("A chord joins two points on the circle. Chords can be tiny, near the edge. But there is a limit to how long one can be.",
      L("l1", "Chord: joins two points on the circle")),
    B("Which chord is the longest one of all?",
      ask=choose(["the radius", "the diameter"], 1,
                 "A radius starts at the centre, so it is not a chord. The longest chord goes right across through the centre: the diameter.")),
    B("The diameter. For this circle that is 2 times 6, which is 12 centimetres.", W("l2", "2 × 6 = 12"),
      note("l2", "12", "longest chord", "below")),
    B("So a chord can be any length up to 12, but never more. 4 fits. 9 fits. 12 is the diameter itself, so it fits too.",
      W("l3", "4 < 12"), W("l4", "9 < 12")),
    B("But 13 is more than 12. No chord can be longer than the diameter.", W("l5", "13 > 12"), ring("l5", "13")),
    B("So 13 centimetres cannot be a chord of this circle.", A("a", "Cannot be: 13 cm", label=True), ring("a", "13")),
    B("Careful with 12: it looks too big next to a radius of 6, but it is exactly the diameter. Compare with the diameter, not the radius."),
])

LESSONS["G4A_CIRCLE_014"] = lesson([
    B("A tray is 20 centimetres long and 8 centimetres wide. Round biscuits of radius 2 centimetres are laid on it in straight rows. What is the most that can fit?",
      G("Tray 20 cm by 8 cm. Biscuits of radius 2 cm, in rows."), GQ("q2", "Greatest number of biscuits = ?"),
      F("G4A_CIRCLE_014")),
    B("How much room does one biscuit need? Its full width, in every direction. What is the full width of a biscuit?",
      ask=choose(["2 cm", "4 cm", "8 cm"], 1,
                 "2 centimetres is only the radius, from the centre to the edge. The full width is the diameter, twice that.")),
    B("Here's the trap: a biscuit takes up its diameter, not its radius. 2 times 2 is 4 centimetres.",
      W("l1", "2 × 2 = 4"), note("l1", "4", "one biscuit", "below")),
    B("Along the 20 centimetre length: 20 divided by 4 is 5. So 5 biscuits fit in a row.", W("l2", "20 ÷ 4 = 5")),
    B("Across the 8 centimetre width: 8 divided by 4 is 2. So there is room for 2 rows.", W("l3", "8 ÷ 4 = 2")),
    B("2 rows of 5 biscuits. 5 times 2 is 10.", W("l4", "5 × 2 = 10")),
    B("The tray holds 10 biscuits.", A("a", "10 biscuits", label=True), ring("a", "10")),
    B("So: find the full width of one circle, see how many fit each way, then multiply."),
])

LESSONS["G4A_CIRCLE_015"] = lesson([
    B("A wire is bent into a circle of radius 7 centimetres. Then the same wire is bent into a square. What is the side of the square? Use 22 over 7 for pi.",
      G("Wire: circle of radius 7 cm, then a square."), GQ("q2", "Side of the square = ?  (π = 22/7)"),
      F("G4A_CIRCLE_015")),
    B("The wire goes once round the circle. So the length of the wire is the circle's what?",
      ask=choose(["diameter", "area", "circumference"], 2,
                 "The wire is the curved edge of the circle. The distance round a circle is its circumference.")),
    B("The circumference is 2 times pi times the radius.", L("l1", "Circumference = 2 × π × radius"),
      W("l2", "2 × 22/7 × 7")),
    B("The 7 underneath and the radius 7 cancel each other. That leaves 2 times 22, which is 44.",
      strike("l2", "/7"), strike("l2", "× 7"), W("l3", "2 × 22 = 44")),
    B("So the wire is 44 centimetres long. Now it becomes a square with 4 equal sides.", note("l3", "44", "the wire", "below")),
    B("44 divided by 4 is 11.", W("l4", "44 ÷ 4 = 11")),
    B("The side of the square is 11 centimetres.", A("a", "Side of square = 11 cm", label=True), ring("a", "11")),
    B("Same wire, same length. The circumference of the circle becomes the perimeter of the square."),
])

LESSONS["G4A_CIRCLE_016"] = lesson([
    B("The radius of a big circle equals the diameter of a small circle. The small circle's radius is 3 centimetres. What is the big circle's diameter?",
      G("Big radius = small diameter. Small radius = 3 cm."), GQ("q2", "Diameter of the big circle = ?"),
      F("G4A_CIRCLE_016")),
    B("Lots of radius and diameter words here! Go one step at a time. Start with the small circle. Its diameter is twice its radius.",
      W("l1", "2 × 3 = 6"), note("l1", "6", "small diameter", "below")),
    B("The small diameter is 6 centimetres. The question says that this is the same as the big circle's what?",
      ask=choose(["its radius", "its diameter"], 0,
                 "Read the first sentence again: the radius of the big circle equals the diameter of the small circle.")),
    B("It is the big circle's radius. So the big radius is 6 centimetres.", L("l2", "big radius = 6 cm")),
    B("Careful: don't stop at 6! We want the big circle's diameter, which is twice its radius.", box("q2", "Diameter")),
    B("2 times 6 is 12.", W("l3", "2 × 6 = 12")),
    B("The diameter of the big circle is 12 centimetres.", A("a", "Big diameter = 12 cm", label=True), ring("a", "12")),
    B("We doubled twice: 3 to 6, then 6 to 12. Label each number as you go, so you always know what it is."),
])

LESSONS["G4A_CIRCLE_017"] = lesson([
    B("Three equal circles with centres A, B and C each have a radius of 4 centimetres. Each touches the other two. What is the perimeter of triangle A B C?",
      G("3 circles, radius 4 cm, each touching the other two."), GQ("q2", "Perimeter of triangle ABC = ?"),
      F("G4A_CIRCLE_017")),
    B("Look at one side of the triangle, from A to B. It starts at one centre and ends at the other, passing through the point where the circles touch.",
      L("l1", "AB = radius + radius")),
    B("So how long is the side A B?",
      ask=choose(["4 cm", "8 cm", "16 cm"], 1,
                 "From A to the touching point is one radius, 4 centimetres. From there to B is another radius.")),
    B("One radius and then another: 4 plus 4 is 8 centimetres.", W("l2", "4 + 4 = 8")),
    B("The circles are all the same size, so the other two sides are 8 centimetres as well."),
    B("The triangle has 3 sides of 8. 3 times 8 is 24.", W("l3", "3 × 8 = 24")),
    B("The perimeter of triangle A B C is 24 centimetres.", A("a", "Perimeter of ABC = 24 cm", label=True), ring("a", "24")),
    B("Whenever circles touch, the line between their centres is one radius plus the other radius."),
])

LESSONS["G4A_CIRCLE_018"] = lesson([
    B("Ten equal circles sit inside a rectangle in 2 rows of 5, touching each other and the sides. The rectangle's perimeter is 84 centimetres. What is each circle's radius?",
      G("10 circles in a rectangle: 2 rows of 5."), GQ("q2", "Perimeter = 84 cm. Radius of each circle = ?"),
      F("G4A_CIRCLE_018")),
    B("Let's measure the rectangle in diameters. The length holds 5 circles, so it is 5 diameters. The width holds 2 circles, so it is 2 diameters.",
      L("l1", "length = 5 diameters, width = 2 diameters")),
    B("So length plus width is 5 plus 2, which is 7 diameters.", W("l2", "5 + 2 = 7")),
    B("Now, the perimeter is 84. Is 84 equal to those 7 diameters?",
      ask=choose(["Yes", "No, 7 diameters is only half of it"], 1,
                 "The perimeter is two lengths and two widths. One length plus one width is only halfway round.")),
    B("That's the trap. Length plus width is half the perimeter. Half of 84 is 42.", W("l3", "84 ÷ 2 = 42")),
    B("So 7 diameters make 42. 42 divided by 7 is 6. Each diameter is 6 centimetres.", W("l4", "42 ÷ 7 = 6")),
    B("One last step: the question asks for the radius. Half of 6 is 3.", W("l5", "6 ÷ 2 = 3")),
    B("The radius of each circle is 3 centimetres.", A("a", "Radius = 3 cm", label=True), ring("a", "3")),
    B("Check: the length is 5 times 6, which is 30. The width is 2 times 6, which is 12. 30 plus 12 is 42, and double is 84.",
      W("c1", "5 × 6 = 30"), W("c2", "2 × 6 = 12"), W("c3", "2 × (30 + 12) = 84")),
])

LESSONS["G4A_CIRCLE_019"] = lesson([
    B("A small circle of radius 3 centimetres lies inside a big circle of radius 10 centimetres, touching it at one point. How far apart are the two centres?",
      G("Small circle (radius 3 cm) inside big circle (radius 10 cm)."), GQ("q2", "They touch at one point. Centres are ? apart"),
      F("G4A_CIRCLE_019")),
    B("Stand at the touching point and look inwards. Both centres are straight ahead of you, on one line.",
      L("l1", "touching point, small centre, big centre: one line")),
    B("The big centre is 10 centimetres from the touching point. The small centre is 3 centimetres from it. Both in the same direction.",
      L("l2", "big centre: 10 cm in.  small centre: 3 cm in.")),
    B("So how far is it from one centre to the other?",
      ask=choose(["10 + 3", "10 − 3", "10 × 3"], 1,
                 "Both centres are on the same side of the touching point. One is 3 in and the other is 10 in. The gap between them is the difference.")),
    B("10 minus 3 is 7.", W("l3", "10 − 3 = 7")),
    B("The centres are 7 centimetres apart.", A("a", "Centres are 7 cm apart", label=True), ring("a", "7")),
    B("Here's the trap. When circles touch from outside, we add the radii. When one is inside the other, we subtract."),
])

LESSONS["G4A_CIRCLE_020"] = lesson([
    B("Three circles of radius 2, 3 and 4 centimetres are in a row, centres on one line. The middle one touches the other two. How far is it from the first centre to the last centre?",
      G("Circles of radius 2 cm, 3 cm, 4 cm in a row, touching."), GQ("q2", "First centre to last centre = ?"),
      F("G4A_CIRCLE_020")),
    B("Let's take the trip in three parts. Part one: from the first centre out to its edge. That is its radius, 2 centimetres.",
      L("l1", "first circle: 2 cm")),
    B("Part two: we must cross the whole middle circle, from one side to the other. How far is that?",
      ask=choose(["3 cm", "6 cm", "9 cm"], 1,
                 "We go in one side of the middle circle and out the other. That is its full width, the diameter, which is twice 3.")),
    B("That's the trap: the middle circle is crossed completely, so we need its diameter. 2 times 3 is 6.",
      W("l2", "2 × 3 = 6"), note("l2", "6", "middle circle", "below")),
    B("Part three: from the edge of the last circle in to its centre. That is its radius, 4 centimetres. We stop at the centre.",
      L("l3", "last circle: 4 cm")),
    B("Add the three parts. 2 plus 6 plus 4 is 12.", W("l4", "2 + 6 + 4 = 12")),
    B("The distance between the first and last centres is 12 centimetres.",
      A("a", "First to last centre = 12 cm", label=True), ring("a", "12")),
    B("Centre to centre: one radius for each end circle, but a whole diameter for any circle in between."),
])

LESSONS["G4A_CIRCLE_021"] = lesson([
    B("A circle has a circumference of 88 centimetres. It fits exactly inside a square, touching all four sides. What is the side of the square? Use 22 over 7 for pi.",
      G("Circle: circumference 88 cm, fits exactly in a square."), GQ("q2", "Side of the square = ?  (π = 22/7)"),
      F("G4A_CIRCLE_021")),
    B("The circle touches opposite sides of the square. So the side of the square equals the circle's diameter. We need the radius first.",
      L("l1", "side of square = diameter")),
    B("Circumference is 2 times 22 over 7 times r. 2 times 22 is 44. So it is 44 times r, divided by 7.",
      L("l2", "Circumference = 2 × 22/7 × r"), W("l3", "2 × 22 = 44")),
    B("44 times something makes 88. That something is 2.", W("l4", "88 ÷ 44 = 2")),
    B("So r divided by 7 is 2. That means r is 2 times 7, which is 14 centimetres.", W("l5", "2 × 7 = 14"),
      note("l5", "14", "radius", "below")),
    B("The radius is 14. Is that the side of the square?",
      ask=choose(["Yes, 14 cm", "No, the side is the diameter"], 1,
                 "The radius only reaches from the centre to one side of the square. The circle stretches right across, so the side is the diameter.")),
    B("The side is the diameter: 2 times 14 is 28.", W("l6", "2 × 14 = 28")),
    B("The side of the square is 28 centimetres.", A("a", "Side of square = 28 cm", label=True), ring("a", "28")),
    B("Another trap is sharing 88 among 4 sides. The 88 goes round the circle, not round the square."),
])

LESSONS["G4A_CIRCLE_022"] = lesson([
    B("A circle of radius 7 centimetres is cut out of a square sheet of side 14 centimetres. What area of paper is left? Use 22 over 7 for pi.",
      G("Square sheet of side 14 cm. Circle of radius 7 cm cut out."), GQ("q2", "Area of paper left = ?  (π = 22/7)"),
      F("G4A_CIRCLE_022")),
    B("The paper left is the square with the circle taken away. So we need two areas.",
      L("l1", "left = square − circle")),
    B("The square: 14 times 14. 14 times 10 is 140, and 14 times 4 is 56. Together, 196.",
      W("l2", "14 × 10 = 140"), W("l3", "14 × 4 = 56"), W("l4", "140 + 56 = 196")),
    B("Now the circle. Which rule gives the area of a circle?",
      ask=choose(["2 × π × radius", "π × radius × radius"], 1,
                 "2 times pi times the radius is the distance round, the circumference. For the space inside, the radius is used twice.")),
    B("Pi times radius times radius: 22 over 7, times 7, times 7. One 7 cancels the 7 underneath, leaving 22 times 7.",
      W("l5", "22/7 × 7 × 7"), strike("l5", "/7"), strike("l5", "× 7")),
    B("22 times 7 is 154.", W("l6", "22 × 7 = 154")),
    B("Take the circle from the square. 196 minus 154 is 42.", W("l7", "196 − 154 = 42")),
    B("The area of paper left is 42 square centimetres.", A("a", "Paper left = 42 sq cm", label=True), ring("a", "42")),
    B("Careful to take away the circle's area, not its circumference. Area from area, always."),
])

LESSONS["G4A_CIRCLE_023"] = lesson([
    B("Five points are marked on a circle. Every pair of points is joined by a straight line. How many chords are drawn?",
      G("5 points on a circle. Every pair is joined."), GQ("q2", "How many chords?")),
    B("Let's count in order so we don't count any chord twice. Call the points 1, 2, 3, 4 and 5.",
      L("l0", "points: 1, 2, 3, 4, 5")),
    B("From point 1, chords go to each of the other 4 points. That is 4 chords.", L("l1", "from point 1: 4 chords")),
    B("Now point 2. It is already joined to point 1. So how many new chords start from point 2?",
      ask=choose(["4", "3", "5"], 1,
                 "Point 2 can join points 3, 4 and 5. Its chord to point 1 is already drawn, so we don't count it again.")),
    B("3 new chords. Then point 3 gives 2 new ones, and point 4 gives just 1. Point 5 is already joined to everyone.",
      L("l2", "point 2: 3 new"), L("l3", "point 3: 2 new"), L("l4", "point 4: 1 new")),
    B("Add them up: 4 plus 3 plus 2 plus 1 is 10.", W("l5", "4 + 3 + 2 + 1 = 10")),
    B("10 chords are drawn.", A("a", "10 chords", label=True), ring("a", "10")),
    B("The trap is 5 times 4, which is 20. That counts every chord twice, once from each end. And half of 20 is 10.",
      W("c1", "5 × 4 = 20"), W("c2", "20 ÷ 2 = 10")),
])

LESSONS["G4A_CIRCLE_024"] = lesson([
    B("Two square trays each have a side of 24 centimetres. One is filled by 9 plates in 3 rows of 3. The other by 16 plates in 4 rows of 4. How much longer is a plate's radius in the first tray?",
      G("Two trays of side 24 cm: 3 rows of 3, and 4 rows of 4."), GQ("q2", "Difference between the plates' radii = ?"),
      F("G4A_CIRCLE_024")),
    B("First tray: 3 plates fit across 24 centimetres. So each plate is 24 divided by 3, which is 8 centimetres wide.",
      W("l1", "24 ÷ 3 = 8")),
    B("8 centimetres is the full width of a plate. Is that its radius or its diameter?",
      ask=choose(["its radius", "its diameter"], 1,
                 "The full width of a round plate, from one side to the other, is its diameter. The radius is half of that.")),
    B("It is the diameter. So the radius is half of 8, which is 4 centimetres.", W("l2", "8 ÷ 2 = 4"),
      note("l2", "4", "first radius", "below")),
    B("Second tray: 4 plates across. 24 divided by 4 is 6 centimetres wide, so the radius is half of 6, which is 3.",
      W("l3", "24 ÷ 4 = 6"), W("l4", "6 ÷ 2 = 3"), note("l4", "3", "second radius", "below")),
    B("Now compare the radii. 4 minus 3 is 1.", W("l5", "4 − 3 = 1")),
    B("The radius in the first tray is 1 centimetre longer.", A("a", "1 cm longer", label=True), ring("a", "1")),
    B("The trap is comparing the diameters, 8 and 6. The question asks about the radii, so halve first, then subtract."),
])
