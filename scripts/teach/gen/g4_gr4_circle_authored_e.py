"""Lessons written one by one: Grade 4 circles, PYQ_2019_Q15 and Q_CH21_001 to 011."""
from g4_gr4_quads_lib import A, B, FIG, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


def CIRCLE(**kw):
    spec = {"kind": "circle"}
    spec.update(kw)
    return FIG("f", spec)


LESSONS["PYQ_2019_Q15"] = lesson([
    B("Eight equal circles sit in a rectangle in 2 rows of 4, touching each other and the sides. Each radius is 6 centimetres. Find the perimeter of the rectangle.",
      G("8 circles in a rectangle: 2 rows of 4"), GQ("q2", "Radius = 6 cm. Perimeter of rectangle = ?"),
      F("PYQ_2019_Q15")),
    B("The circles fill the rectangle from side to side. How much room does one circle take, from edge to edge?",
      ask=choose(["6 cm", "12 cm", "24 cm"], 1,
                 "6 centimetres only reaches from the centre to the edge. From edge to edge is the diameter, two radii.")),
    B("That's the first trap: use the diameter, not the radius. 2 times 6 is 12 centimetres.",
      W("l1", "2 × 6 = 12"), note("l1", "12", "diameter", "below"), F("PYQ_2019_Q15", 0)),
    B("The length holds 4 circles: 4 times 12 is 48. The breadth holds 2 circles: 2 times 12 is 24.",
      W("l2", "4 × 12 = 48"), W("l3", "2 × 12 = 24"), F("PYQ_2019_Q15", 1)),
    B("Now the perimeter. Length plus breadth is 48 plus 24, which is 72. Are we finished?",
      W("l4", "48 + 24 = 72"),
      ask=choose(["Yes, 72 cm", "No, that is halfway round"], 1,
                 "One length and one breadth cover only two of the four sides. The other two sides are still to come.")),
    B("72 is only halfway round. That's the second trap! Double it: 2 times 72 is 144.",
      note("l4", "72", "halfway round", "below"), W("l5", "2 × 72 = 144")),
    B("The perimeter of the rectangle is 144 centimetres.", A("a", "Perimeter = 144 cm", label=True), ring("a", "144")),
    B("Two things to remember: a circle takes up its diameter, and a perimeter goes round all four sides."),
])

LESSONS["Q_CH21_001"] = lesson([
    B("A circle is all the points that are the same distance from one fixed point. What is that fixed point called?",
      G("All points equidistant from a fixed point called the: ?"), F("Q_CH21_001")),
    B("Equidistant is a long word. It just means the same distance away.", L("l1", "equidistant = the same distance away")),
    B("Think of a goat tied to a post by a rope. It walks round as far out as the rope lets it. What shape is its path?",
      ask=choose(["a square", "a circle", "a triangle"], 1,
                 "The rope keeps the goat the same distance from the post all the time. That makes a perfectly round path.")),
    B("A circle! The goat is always the same distance from the post. So the post is the fixed point, right in the middle."),
    B("That middle point of a circle is called the centre.", A("a", "The centre", label=True), ring("a", "centre"),
      CIRCLE(radius="same distance", highlight=["radius"])),
    B("And the rope? Its length is the radius. Careful: the radius is a distance, but the question asks for a point."),
    B("So: the centre is the point in the middle. The radius is how far the circle is from it."),
])

LESSONS["Q_CH21_003"] = lesson([
    B("The radius of a circle is 9.5 centimetres. What is its diameter?",
      G("Circle: radius = 9.5 cm. Diameter = ?"), F("Q_CH21_003")),
    B("The diameter goes right across the circle through the centre. That is one radius, then another radius.",
      L("l1", "diameter = radius + radius")),
    B("So what do we do to 9.5?",
      ask=choose(["halve it", "double it", "leave it"], 1,
                 "The diameter is the longer one. It is made of two radii, so we need 2 lots of 9.5.")),
    B("Double it. 2 times 9 is 18. And 2 times 0.5 is two halves, which make 1.",
      W("l2", "2 × 9 = 18"), W("l3", "2 × 0.5 = 1")),
    B("18 plus 1 is 19.", W("l4", "18 + 1 = 19"), W("l5", "2 × 9.5 = 19")),
    B("The diameter is 19 centimetres.", A("a", "Diameter = 19 cm", label=True), ring("a", "19")),
    B("Don't let the decimal worry you. Double the whole part, double the half, and put them together."),
])

LESSONS["Q_CH21_004"] = lesson([
    B("What is the longest chord of a circle called?", G("The longest chord of a circle is called the: ?"), F("Q_CH21_004")),
    B("A chord is a straight line joining two points on the circle.", L("l1", "Chord: straight line, two points on the circle")),
    B("A chord near the edge is short. As it slides towards the middle it grows. Where is it longest?",
      ask=choose(["touching the edge", "through the centre"], 1,
                 "A circle is widest right across its middle. So the longest chord is the one that passes through the centre.")),
    B("Through the centre. No chord can be longer than that one.", L("l2", "longest chord: through the centre"),
      F("Q_CH21_004", 1)),
    B("A chord through the centre is called the diameter.", A("a", "The diameter", label=True), ring("a", "diameter")),
    B("Watch the other names. An arc is curved, and the circumference goes round. A radius stops at the centre, so it is not a chord."),
    B("So the diameter is a chord, and it is the longest one a circle can have."),
])

LESSONS["Q_CH21_005"] = lesson([
    B("How many axes of symmetry does a circle have?", G("How many axes of symmetry does a circle have?"), F("Q_CH21_005")),
    B("An axis of symmetry is a fold line. Fold along it, and the two halves match exactly.",
      L("l1", "Axis of symmetry = a fold line that matches")),
    B("Take a paper circle. Fold it top to bottom, through the centre. The halves match. Now fold it side to side. They match again.",
      L("l2", "top to bottom: yes.  side to side: yes.")),
    B("Now tilt the fold a little, still through the centre. Do the halves still match?",
      ask=choose(["Yes, they still match", "No, not any more"], 0,
                 "A circle is equally round everywhere. However you turn it, a fold through the centre gives two equal halves.")),
    B("They do! Any fold through the centre works. Every diameter is an axis of symmetry.",
      L("l3", "every diameter is an axis"), F("Q_CH21_005", 1)),
    B("And how many diameters are there? You can keep tilting the line a tiny bit more, for ever. There is no end to them."),
    B("So a circle has an infinite number of axes of symmetry. Infinite means without end.",
      A("a", "Infinite", label=True), ring("a", "Infinite")),
    B("A square has 4 and a rectangle has 2. The circle beats them all, because it is the same in every direction."),
])

LESSONS["Q_CH21_006"] = lesson([
    B("Find the circumference of a circle with radius 21 centimetres. Use 22 over 7 for pi.",
      G("Circle: radius 21 cm. Circumference = ? (π = 22/7)"), F("Q_CH21_006")),
    B("The circumference is the distance round the circle. It is pi times the diameter.",
      L("l1", "Circumference = π × diameter")),
    B("We are given the radius, 21. So what is the diameter?",
      ask=choose(["21 cm", "42 cm", "10.5 cm"], 1,
                 "The diameter is two radii, end to end. So we double 21.")),
    B("Double 21 is 42. Careful not to skip this step: pi times the radius alone gives only half of the way round.",
      W("l2", "2 × 21 = 42")),
    B("Now 22 over 7, times 42. Let the 7 divide first: 42 divided by 7 is 6.",
      W("l3", "22/7 × 42"), strike("l3", "7"), W("l4", "42 ÷ 7 = 6")),
    B("That leaves 22 times 6. 20 times 6 is 120, and 2 times 6 is 12. Together, 132.",
      W("l5", "20 × 6 = 120"), W("l5b", "2 × 6 = 12"), W("l6", "120 + 12 = 132")),
    B("The circumference is 132 centimetres.", A("a", "Circumference = 132 cm", label=True), ring("a", "132")),
    B("Does it look sensible? Going round is a bit more than 3 times the diameter. 3 times 42 is 126, so 132 fits.",
      W("c", "3 × 42 = 126")),
])

LESSONS["Q_CH21_007"] = lesson([
    B("Find the circumference of a circle with diameter 14 centimetres. Use 22 over 7 for pi.",
      G("Circle: diameter 14 cm. Circumference = ? (π = 22/7)"), F("Q_CH21_007")),
    B("The circumference is pi times the diameter.", L("l1", "Circumference = π × diameter")),
    B("Look carefully at what we are given. Is 14 the radius or the diameter?",
      box("q", "diameter 14 cm"),
      ask=choose(["the radius", "the diameter"], 1,
                 "Read the question once more. It says diameter 14 centimetres. So there is no need to double it.")),
    B("It is already the diameter. That's the trap: don't double it again! We just need 22 over 7, times 14.",
      W("l2", "22/7 × 14")),
    B("Let the 7 divide first. 14 divided by 7 is 2.", strike("l2", "7"), W("l3", "14 ÷ 7 = 2")),
    B("That leaves 22 times 2, which is 44.", W("l4", "22 × 2 = 44")),
    B("The circumference is 44 centimetres.", A("a", "Circumference = 44 cm", label=True), ring("a", "44")),
    B("Sensible? A bit more than 3 times the diameter. 3 times 14 is 42, so 44 fits.", W("c", "3 × 14 = 42")),
])

LESSONS["Q_CH21_008"] = lesson([
    B("The circumference of a circle is 440 metres. Find its radius. Use 22 over 7 for pi.",
      G("Circle: circumference = 440 m. Radius = ? (π = 22/7)"), F("Q_CH21_008")),
    B("The circumference is 22 over 7 times the diameter. Think of it in parts: if the diameter is 7 parts, the circumference is 22 of the same parts.",
      L("l1", "circumference: 22 parts.  diameter: 7 parts.")),
    B("The circumference, 440, is 22 parts. So how big is one part?",
      ask=choose(["440 ÷ 22", "440 ÷ 7", "440 × 22"], 0,
                 "22 equal parts make 440. To find one part, share 440 into 22.")),
    B("440 divided by 22 is 20. One part is 20 metres.", W("l2", "440 ÷ 22 = 20")),
    B("The diameter is 7 parts. 7 times 20 is 140 metres.", W("l3", "7 × 20 = 140"), note("l3", "140", "diameter", "below")),
    B("Stop! Is 140 our answer? The question asks for the radius, and 140 is the diameter.", box("q", "Radius")),
    B("The radius is half the diameter. Half of 140 is 70.", W("l4", "140 ÷ 2 = 70")),
    B("The radius is 70 metres.", A("a", "Radius = 70 m", label=True), ring("a", "70")),
    B("Check: the diameter is 140. 140 divided by 7 is 20, and 22 times 20 is 440. It fits.", W("c", "22/7 × 140 = 440")),
])

LESSONS["Q_CH21_009"] = lesson([
    B("The circumference of a round park is 176 metres. Find its diameter. Use 22 over 7 for pi.",
      G("Park: circumference = 176 m. Diameter = ? (π = 22/7)"), F("Q_CH21_009")),
    B("The circumference is 22 over 7 times the diameter. In parts: when the diameter is 7 parts, the circumference is 22 parts.",
      L("l1", "circumference: 22 parts.  diameter: 7 parts.")),
    B("So 22 parts make 176. One part is 176 divided by 22. 22 times 8 is 176, so one part is 8.",
      W("l2", "22 × 8 = 176"), W("l3", "176 ÷ 22 = 8")),
    B("One part is 8 metres. How do we get the diameter?",
      ask=choose(["8 × 7", "8 × 22", "8 ÷ 2"], 0, "The diameter is 7 of those parts. So we need 7 lots of 8.")),
    B("7 times 8 is 56.", W("l4", "7 × 8 = 56")),
    B("The diameter of the park is 56 metres.", A("a", "Diameter = 56 m", label=True), ring("a", "56")),
    B("This time the question wants the diameter, so we stop here. Halving would give the radius, which nobody asked for."),
    B("Check: 56 divided by 7 is 8, and 22 times 8 is 176. It fits.", W("c", "22/7 × 56 = 176")),
])

LESSONS["Q_CH21_010"] = lesson([
    B("Find the area of a circle with radius 7 centimetres. Use 22 over 7 for pi.",
      G("Circle: radius 7 cm. Area = ? (π = 22/7)"), F("Q_CH21_010")),
    B("The area is the space inside the circle. The rule is pi times the radius times the radius.",
      L("l1", "Area = π × radius × radius")),
    B("Which sum is that for our circle?",
      ask=choose(["2 × 22/7 × 7", "22/7 × 7", "22/7 × 7 × 7"], 2,
                 "The rule with the 2 is for the distance round. For the space inside, the radius is used twice.")),
    B("22 over 7, times 7, times 7. The radius goes in twice, and there is no 2.", W("l2", "22/7 × 7 × 7")),
    B("One of the 7s cancels the 7 underneath. That leaves 22 times 7.", strike("l2", "/7"), strike("l2", "× 7")),
    B("22 times 7: 20 times 7 is 140, and 2 times 7 is 14. Together, 154.",
      W("l3", "20 × 7 = 140"), W("l3b", "2 × 7 = 14"), W("l4", "140 + 14 = 154")),
    B("The area is 154 square centimetres.", A("a", "Area = 154 cm²", label=True), ring("a", "154")),
    B("Remember: radius times radius for area, and the answer is in square units. 154 for a radius of 7 is a number worth knowing."),
])

LESSONS["Q_CH21_011"] = lesson([
    B("Find the area of a circle with diameter 14 centimetres. Use 22 over 7 for pi.",
      G("Circle: diameter 14 cm. Area = ? (π = 22/7)"), F("Q_CH21_011")),
    B("The area rule is pi times the radius times the radius. But look at what we are given.",
      L("l1", "Area = π × radius × radius"), box("q", "diameter 14 cm")),
    B("We have the diameter, and the rule needs the radius. What is the radius?",
      ask=choose(["14 cm", "28 cm", "7 cm"], 2, "The radius is half of the diameter. Half of 14 is what we need.")),
    B("Half of 14 is 7. That's the trap here: using 14 in the rule would make the area far too big.", W("l2", "14 ÷ 2 = 7")),
    B("Now 22 over 7, times 7, times 7. One 7 cancels the 7 underneath, leaving 22 times 7.",
      W("l3", "22/7 × 7 × 7"), strike("l3", "/7"), strike("l3", "× 7")),
    B("22 times 7: 20 times 7 is 140, and 2 times 7 is 14. Together, 154.",
      W("l4", "20 × 7 = 140"), W("l4b", "2 × 7 = 14"), W("l5", "140 + 14 = 154")),
    B("The area is 154 square centimetres.", A("a", "Area = 154 cm²", label=True), ring("a", "154")),
    B("Before using any circle rule, check: have I got the radius or the diameter? Then change it if you need to."),
])
