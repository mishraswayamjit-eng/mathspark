"""Lessons written one by one: Grade 4 circles, G4A_CIRCLE_001 to 012."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["G4A_CIRCLE_001"] = lesson([
    B("A round plate has a diameter of 18 centimetres. What is its radius?",
      G("Plate: diameter = 18 cm. Radius = ?"), F("G4A_CIRCLE_001")),
    B("The diameter goes right across the plate, through the centre. The radius only goes from the centre to the edge.",
      L("l1", "diameter = radius + radius")),
    B("So to get from the diameter to the radius, do we double or halve?",
      ask=choose(["double", "halve"], 1,
                 "The radius is the shorter one. It reaches only halfway across the plate. So we halve the diameter.")),
    B("The radius is half the diameter. Half of 18 is 9.", W("l2", "18 ÷ 2 = 9")),
    B("The radius is 9 centimetres.", A("a", "Radius = 9 cm", label=True), ring("a", "9")),
    B("Check: 9 and 9 make 18, the full diameter.", W("c", "9 + 9 = 18")),
    B("Radius to diameter: double. Diameter to radius: halve. Ask yourself which one should be bigger."),
])

LESSONS["G4A_CIRCLE_002"] = lesson([
    B("Kiran wants to draw a circle of diameter 12 centimetres with a compass. How far apart should the needle and the pencil tip be?",
      G("Circle of diameter 12 cm, drawn with a compass."), GQ("q2", "Needle to pencil tip = ?"), F("G4A_CIRCLE_002")),
    B("Think about how a compass works. The needle stays at the centre. The pencil travels round on the circle.",
      L("l1", "needle: centre.  pencil: on the circle")),
    B("So the gap between the needle and the pencil is which part of the circle?",
      ask=choose(["the diameter", "the radius", "the circumference"], 1,
                 "The gap runs from the centre to a point on the circle. Centre to circle is the radius.")),
    B("It is the radius. That's the trap: the question gives the diameter, but the compass is set to the radius.",
      box("q", "diameter 12 cm")),
    B("The radius is half the diameter. Half of 12 is 6.", W("l2", "12 ÷ 2 = 6")),
    B("The needle and the pencil tip should be 6 centimetres apart.", A("a", "6 cm apart", label=True), ring("a", "6")),
    B("If Kiran opened the compass to 12, the circle would come out twice as wide as he wanted."),
])

LESSONS["G4A_CIRCLE_003"] = lesson([
    B("A circle has a radius of 8 centimetres. How long is the longest chord that can be drawn in it?",
      G("Circle: radius = 8 cm. Longest chord = ?"), F("G4A_CIRCLE_003")),
    B("A chord is a straight line joining two points on the circle. Short ones sit near the edge, longer ones nearer the middle.",
      L("l1", "Chord: joins two points on the circle")),
    B("Where does the very longest chord pass?",
      ask=choose(["near the edge", "through the centre"], 1,
                 "A circle is widest across its middle. So the longest straight line inside it passes through the centre.")),
    B("Through the centre. And a chord through the centre is the diameter.", L("l2", "longest chord = diameter")),
    B("The diameter is twice the radius. 2 times 8 is 16.", W("l3", "2 × 8 = 16")),
    B("The longest chord is 16 centimetres.", A("a", "Longest chord = 16 cm", label=True), ring("a", "16")),
    B("The question never says the word diameter. You have to spot that the longest chord is the diameter."),
])

LESSONS["G4A_CIRCLE_004"] = lesson([
    B("A circle has a radius of 6 centimetres. Point P is 4 centimetres from the centre. Where is P?",
      G("Circle: radius 6 cm. P is 4 cm from the centre."), GQ("q2", "Where is P?"), F("G4A_CIRCLE_004")),
    B("Every point on the circle is exactly 6 centimetres from the centre. That is what the radius tells us.",
      L("l1", "on the circle: exactly 6 cm away")),
    B("Start at the centre and walk towards the circle. After 4 centimetres you stop. Have you reached the circle yet?",
      ask=choose(["Yes", "No, not yet"], 1, "The circle is 6 centimetres away from the centre. You have only walked 4, so you are not there yet.")),
    B("Not yet. 4 is less than 6.", W("l2", "4 < 6")),
    B("So P is closer to the centre than the circle is. P is inside the circle.",
      A("a", "P is inside the circle", label=True), ring("a", "inside")),
    B("Here is the rule. Less than the radius: inside. Equal to the radius: on the circle. More than the radius: outside."),
    B("So just compare the distance with the radius. Here 4 is less than 6, so P is inside."),
])

LESSONS["G4A_CIRCLE_005"] = lesson([
    B("O is the centre of a circle. A and B are two points on the circle. O A is 7 centimetres. How long is O B?",
      G("O is the centre. A and B are on the circle."), GQ("q2", "OA = 7 cm. OB = ?"), F("G4A_CIRCLE_005")),
    B("O A joins the centre to a point on the circle. What do we call a line like that?",
      ask=choose(["a radius", "a diameter", "a chord"], 0,
                 "A line from the centre to the circle is a radius. A diameter would go right across, and a chord joins two points on the circle.")),
    B("O A is a radius. And O B also joins the centre to a point on the circle. So O B is a radius too.",
      L("l1", "OA: a radius.  OB: a radius.")),
    B("Now the big fact about circles: every radius of the same circle has the same length.",
      L("l2", "all radii are equal"), mark("l2", "equal")),
    B("So O B is the same as O A: 7 centimetres.", A("a", "OB = 7 cm", label=True), ring("a", "7")),
    B("No sum was needed at all! It doesn't matter where B is on the circle. It is always one radius from the centre."),
])

LESSONS["G4A_CIRCLE_006"] = lesson([
    B("Four equal circles, each of radius 3 centimetres, sit in a row, each touching the next. How far is it from the centre of the first to the centre of the last?",
      G("4 circles in a row, each of radius 3 cm, touching."), GQ("q2", "First centre to last centre = ?"),
      F("G4A_CIRCLE_006")),
    B("Start small. Take two circles that touch. From one centre you travel a radius to the touching point, then another radius to the next centre.",
      L("l1", "centre to next centre = radius + radius")),
    B("So neighbouring centres are 3 plus 3, which is 6 centimetres apart.", W("l2", "3 + 3 = 6")),
    B("Now the tricky part. There are 4 centres in the row. How many gaps are there between the first and the last?",
      ask=choose(["4 gaps", "3 gaps", "2 gaps"], 1,
                 "Hold up 4 fingers and count the spaces between them. There is always one gap fewer than the number of things.")),
    B("That's the trap: 4 circles, but only 3 gaps between their centres.", L("l3", "4 centres: 3 gaps"), box("l3", "3 gaps")),
    B("3 gaps of 6 centimetres. 3 times 6 is 18.", W("l4", "3 × 6 = 18")),
    B("The distance from the first centre to the last is 18 centimetres.",
      A("a", "First to last centre = 18 cm", label=True), ring("a", "18")),
    B("The whole row is longer than that, because half a circle sticks out at each end. Centre to centre, count the gaps."),
])

LESSONS["G4A_CIRCLE_007"] = lesson([
    B("Six round bangles, each of radius 4 centimetres, lie in a straight row, each touching the next. How long is the row from end to end?",
      G("6 bangles in a row, each of radius 4 cm, touching."), GQ("q2", "Length of the row = ?"), F("G4A_CIRCLE_007")),
    B("How much of the row does one bangle take up? Its full width, from one side to the other. Which measure is that?",
      ask=choose(["the radius, 4 cm", "the diameter, 8 cm"], 1,
                 "The radius only reaches from the centre to the edge. The full width of a bangle is its diameter, twice the radius.")),
    B("The full width is the diameter. 2 times 4 is 8 centimetres.", W("l1", "2 × 4 = 8"), note("l1", "8", "one bangle", "below")),
    B("The bangles touch, so there are no spaces between them. The row is just 6 bangles, side by side."),
    B("6 times 8 is 48.", W("l2", "6 × 8 = 48")),
    B("The row is 48 centimetres long.", A("a", "Row = 48 cm", label=True), ring("a", "48")),
    B("This time we want end to end, so every whole bangle counts. If it had asked centre to centre, we would count gaps instead."),
])

LESSONS["G4A_CIRCLE_008"] = lesson([
    B("A circle is drawn inside a square of side 10 centimetres, just touching all four sides. What is the radius of the circle?",
      G("Circle inside a square of side 10 cm, touching all sides."), GQ("q2", "Radius = ?"), F("G4A_CIRCLE_008")),
    B("The circle touches the left side and the right side of the square. So how wide is the circle, right across?",
      ask=choose(["5 cm", "10 cm", "20 cm"], 1,
                 "The circle reaches from one side of the square to the opposite side. So it is exactly as wide as the square.")),
    B("The circle is as wide as the square. So its diameter is 10 centimetres.", L("l1", "diameter = side of square = 10 cm")),
    B("But the question asks for the radius, not the diameter.", box("q2", "Radius")),
    B("The radius is half the diameter. Half of 10 is 5.", W("l2", "10 ÷ 2 = 5")),
    B("The radius of the circle is 5 centimetres.", A("a", "Radius = 5 cm", label=True), ring("a", "5")),
    B("A circle that fits snugly in a square has the square's side as its diameter. Then halve for the radius."),
])

LESSONS["G4A_CIRCLE_009"] = lesson([
    B("A circle of radius 6 centimetres fits exactly inside a square, touching all four sides. What is the perimeter of the square?",
      G("Circle of radius 6 cm fits exactly inside a square."), GQ("q2", "Perimeter of the square = ?"),
      F("G4A_CIRCLE_009")),
    B("The circle touches opposite sides of the square. So the side of the square is as long as which part of the circle?",
      ask=choose(["the radius", "the diameter"], 1,
                 "The circle stretches right across the square, from one side to the other. Right across a circle is its diameter.")),
    B("The side of the square equals the diameter. 2 times 6 is 12 centimetres.",
      W("l1", "2 × 6 = 12"), note("l1", "12", "side of square", "below")),
    B("Careful: the side is 12, not 6. The radius only reaches halfway across the square."),
    B("A square has 4 equal sides. 4 times 12 is 48.", W("l2", "4 × 12 = 48")),
    B("The perimeter of the square is 48 centimetres.", A("a", "Perimeter = 48 cm", label=True), ring("a", "48")),
    B("Two steps: radius to diameter gives the side, then 4 sides give the perimeter."),
])

LESSONS["G4A_CIRCLE_010"] = lesson([
    B("Two coins lie flat and touch each other. One has a radius of 5 centimetres and the other 3 centimetres. How far apart are their centres?",
      G("Two touching coins: radius 5 cm and radius 3 cm."), GQ("q2", "Distance between the centres = ?"),
      F("G4A_CIRCLE_010")),
    B("Travel from one centre to the other. First you go from the centre of the big coin out to its edge. How far is that?",
      ask=choose(["5 cm", "10 cm", "3 cm"], 0,
                 "Centre to edge is the radius. The big coin has a radius of 5 centimetres.")),
    B("5 centimetres, one radius of the big coin. Now you are at the point where the coins touch.",
      L("l1", "big coin: centre to edge = 5 cm")),
    B("From there you go to the centre of the small coin. That is one radius of the small coin: 3 centimetres.",
      L("l2", "small coin: edge to centre = 3 cm")),
    B("So the whole trip is 5 plus 3, which is 8.", W("l3", "5 + 3 = 8")),
    B("The centres are 8 centimetres apart.", A("a", "Centres are 8 cm apart", label=True), ring("a", "8")),
    B("When two circles touch from outside, the distance between their centres is one radius plus the other radius."),
])

LESSONS["G4A_CIRCLE_011"] = lesson([
    B("Two circles share the same centre. The big one has a radius of 9 centimetres and the small one 5 centimetres. How wide is the ring between them?",
      G("Same centre: radius 9 cm and radius 5 cm."), GQ("q2", "Width of the ring = ?"), F("G4A_CIRCLE_011")),
    B("Walk out from the centre in a straight line. After 5 centimetres you cross the small circle. After 9 centimetres you reach the big circle.",
      L("l1", "small circle at 5 cm, big circle at 9 cm")),
    B("The ring is the stretch between the two circles. How do we find its width?",
      ask=choose(["9 + 5", "9 − 5", "9 × 5"], 1,
                 "The ring is the gap between the 5 centimetre mark and the 9 centimetre mark. To find a gap, we subtract.")),
    B("9 minus 5 is 4.", W("l2", "9 − 5 = 4")),
    B("The ring is 4 centimetres wide.", A("a", "Ring = 4 cm wide", label=True), ring("a", "4")),
    B("Check: 5 centimetres to the small circle, then 4 more across the ring, brings you to 9.", W("c", "5 + 4 = 9")),
    B("For circles with the same centre, the gap between them is the difference of the radii."),
])

LESSONS["G4A_CIRCLE_012"] = lesson([
    B("The diameter of a circle is 12 centimetres longer than its radius. What is the radius?",
      G("Diameter = radius + 12 cm. Radius = ?"), F("G4A_CIRCLE_012")),
    B("We always know one thing about a diameter. It is made of two radii, end to end.",
      L("l1", "diameter = radius + radius")),
    B("And the question tells us the diameter is the radius plus 12 centimetres.",
      L("l2", "diameter = radius + 12 cm")),
    B("Look at the two lines together. Both start with one radius. So what must the 12 centimetres be?",
      ask=choose(["half a radius", "the other radius", "the diameter"], 1,
                 "Line one says radius plus radius. Line two says radius plus 12. The second part of each must match.")),
    B("The extra 12 is the second radius! So the radius is 12 centimetres.",
      mark("l1", "radius", "circle", 2), mark("l2", "12 cm", "circle"),
      A("a", "Radius = 12 cm", label=True), ring("a", "12")),
    B("Check: the diameter is 12 plus 12, which is 24. And 24 is 12 more than 12. It fits.",
      W("c1", "12 + 12 = 24"), W("c2", "24 − 12 = 12")),
    B("The trap is to halve 12 and say 6. Don't halve just because you see the word diameter. Read what the 12 really is."),
])
