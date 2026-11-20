"""Lessons written one by one: Grade 4 quadrilaterals, past-year questions and Q_CH14_022, Q_CH20_001 to 004."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring

F = figure_getter("gr4_quads")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["PYQ_2016_Q24"] = lesson([
    B("A rectangle 4 centimetres long and 1 centimetre broad is cut into 4 equal squares. How much more is the total perimeter of the squares than the perimeter of the rectangle?",
      G("Rectangle 4 cm by 1 cm, cut into 4 equal squares."), GQ("q2", "Squares' perimeters − rectangle's perimeter = ?"),
      F("PYQ_2016_Q24")),
    B("First the squares. The rectangle is 1 centimetre broad, so each square has a side of 1 centimetre. Its perimeter is 4 times 1, which is 4.",
      W("l1", "4 × 1 = 4"), note("l1", "4", "one square", "below")),
    B("There are 4 squares. 4 times 4 is 16 centimetres in all.", W("l2", "4 × 4 = 16"), note("l2", "16", "all 4 squares", "below")),
    B("Now the rectangle. Length plus breadth is 4 plus 1, which is 5. Double it: 10 centimetres.",
      W("l3", "2 × (4 + 1) = 10"), note("l3", "10", "rectangle", "below")),
    B("The squares have 16 and the rectangle has 10. The pieces are the same paper! So why do the squares have more?",
      ask=choose(["The cuts make new edges", "The squares are bigger", "The paper got bigger"], 0,
                 "Each cut opens up two fresh edges, one on each side of the cut. Those edges were hidden inside the rectangle before.")),
    B("Every cut makes new edges. So the squares have more perimeter. 16 minus 10 is 6.", W("l4", "16 − 10 = 6")),
    B("The squares have 6 centimetres more.", A("a", "6 cm more", label=True), ring("a", "6")),
    B("Check with the cuts. 3 cuts, each making 2 new edges of 1 centimetre. 3 times 2 is 6. It matches!", W("c", "3 × 2 = 6")),
    B("Read the last words of the question carefully. It asks how much more, so we find both totals and subtract."),
])

LESSONS["PYQ_2016_Q29"] = lesson([
    B("A square and an equilateral triangle have equal perimeters. Which shape has the longer side?",
      G("Square and equilateral triangle: equal perimeter."), GQ("q2", "Compare the side of each."), F("PYQ_2016_Q29")),
    B("There are no numbers here, so let's choose our own. Say both perimeters are 12 centimetres. 12 is easy to share.",
      L("l1", "Try: perimeter = 12 cm for both")),
    B("The square shares 12 among 4 equal sides. 12 divided by 4 is 3.", W("l2", "12 ÷ 4 = 3"), note("l2", "3", "square's side", "below")),
    B("The triangle shares the same 12 among only 3 sides. What is each side of the triangle?",
      ask=choose(["3 cm", "4 cm", "12 cm"], 1,
                 "The triangle has 3 equal sides, so we share 12 into 3 parts, not 4.")),
    B("12 divided by 3 is 4. So the triangle's side is 4 centimetres.",
      W("l3", "12 ÷ 3 = 4"), note("l3", "4", "triangle's side", "below")),
    B("3 is less than 4. The square's side is shorter than the triangle's side.", W("l4", "3 < 4")),
    B("Why? It is like sharing a chocolate bar. Share the same bar among more friends, and each piece is smaller."),
    B("So the true statement is: side of square is less than side of triangle.",
      A("a", "Side of square < side of triangle", label=True), ring("a", "<")),
    B("When a question has no numbers, try an easy number of your own. Then look for the reason behind what you see."),
])

LESSONS["PYQ_2017_Q21"] = lesson([
    B("The length of a rectangle is twice its breadth, and both are natural numbers. Which of these can be its perimeter: 232, 138, 334 or 146?",
      G("Rectangle: length = 2 × breadth, natural numbers."), GQ("q2", "Perimeter: 232, 138, 334 or 146 cm?"),
      F("PYQ_2017_Q21")),
    B("Let's count the perimeter in breadths. One length is 2 breadths. Walk round: 2, then 1, then 2, then 1. How many breadths is that?",
      ask=choose(["4 breadths", "6 breadths", "3 breadths"], 1,
                 "Each length counts as 2 breadths. So we add 2 and 1 and 2 and 1.")),
    B("2 plus 1 plus 2 plus 1 is 6. So the perimeter is 6 breadths. It must be in the 6 times table!",
      W("l1", "2 + 1 + 2 + 1 = 6"), L("l2", "Perimeter = 6 × breadth")),
    B("A number in the 6 times table is even, and also in the 3 times table. All four choices are even, so we test for 3.",
      L("l3", "6 times table: even, and in the 3 times table")),
    B("Here is a handy test for 3: add the digits. For 232, 2 plus 3 plus 2 is 7. 7 is not in the 3 times table, so 232 is out.",
      W("l4", "2 + 3 + 2 = 7")),
    B("For 138, 1 plus 3 plus 8 is 12. 12 is in the 3 times table. So 138 works!", W("l5", "1 + 3 + 8 = 12"), ring("l5", "12")),
    B("Check the other two. 3 plus 3 plus 4 is 10, and 1 plus 4 plus 6 is 11. Neither is in the 3 times table.",
      W("l6", "3 + 3 + 4 = 10"), W("l7", "1 + 4 + 6 = 11")),
    B("So the perimeter can be 138 centimetres.", A("a", "Perimeter can be 138 cm", label=True), ring("a", "138")),
    B("Let's make sure. 138 divided by 6 is 23. So the breadth is 23 and the length is 46. Both natural numbers.",
      W("c1", "138 ÷ 6 = 23"), W("c2", "2 × 23 = 46")),
    B("The big idea: turn the whole perimeter into breadths. Then you know which times table it must be in. Only 138 fits."),
])

LESSONS["PYQ_2017_Q35"] = lesson([
    B("The perimeter of a square is 14 centimetres. What could one side measure?",
      G("Square: perimeter = 14 cm. One side = ?"), F("PYQ_2017_Q35")),
    B("A square has 4 equal sides, so we share 14 among 4. Half of 14 is 7, and half of 7 is 3.5.",
      W("l1", "14 ÷ 2 = 7"), W("l2", "7 ÷ 2 = 3.5")),
    B("So the side is 3.5 centimetres. That is 3 whole centimetres and half a centimetre more.",
      W("l3", "14 ÷ 4 = 3.5"), note("l3", "3.5", "cm", "below")),
    B("But 3.5 centimetres is not written like that in the choices. How many millimetres make half a centimetre?",
      L("l4", "1 cm = 10 mm"),
      ask=choose(["5 mm", "50 mm", "2 mm"], 0,
                 "1 centimetre is 10 millimetres. Half a centimetre is half of 10.")),
    B("Half of 10 is 5. So half a centimetre is 5 millimetres.", W("l5", "10 ÷ 2 = 5")),
    B("One side is 3 centimetres and 5 millimetres.", A("a", "Side = 3 cm 5 mm", label=True), ring("a", "3 cm 5 mm")),
    B("Careful with one choice: 3.5 millimetres. The number looks right, but the unit is far too small. Always read the unit."),
    B("Check: 4 sides of 3.5 make 14. It fits.", W("c", "4 × 3.5 = 14")),
])

LESSONS["PYQ_2018_Q39"] = lesson([
    B("A rectangle 3 centimetres long and 1 centimetre broad is cut into 3 square pieces. How much more is the total perimeter of the squares than the perimeter of the rectangle?",
      G("Rectangle 3 cm by 1 cm, cut into 3 squares."), GQ("q2", "Squares' perimeters − rectangle's perimeter = ?"),
      F("PYQ_2018_Q39")),
    B("Each piece is a square of side 1 centimetre. One square has a perimeter of 4 times 1, which is 4.",
      W("l1", "4 × 1 = 4")),
    B("There are 3 squares. What is their total perimeter?",
      ask=choose(["4 cm", "12 cm", "8 cm"], 1, "One square has 4 centimetres. There are 3 squares, so we need 3 lots of 4.")),
    B("3 times 4 is 12 centimetres.", W("l2", "3 × 4 = 12"), note("l2", "12", "all 3 squares", "below")),
    B("Now the rectangle. 3 plus 1 is 4, and double is 8 centimetres.",
      W("l3", "2 × (3 + 1) = 8"), note("l3", "8", "rectangle", "below")),
    B("12 minus 8 is 4. The squares have 4 centimetres more.",
      W("l4", "12 − 8 = 4"), A("a", "4 cm more", label=True), ring("a", "4")),
    B("Where did the extra come from? Each cut opens 2 new edges of 1 centimetre. 2 cuts, so 2 times 2 is 4. It matches.",
      W("c", "2 × 2 = 4")),
    B("Cutting never changes the area, but it always adds perimeter, because new edges appear."),
])

LESSONS["PYQ_2019_Q30"] = lesson([
    B("A square has a perimeter of 36 centimetres. Three such squares are joined in a straight row to make a rectangle. What is the rectangle's perimeter?",
      G("Square: perimeter 36 cm. 3 squares joined in a row."), GQ("q2", "Perimeter of the rectangle = ?"),
      F("PYQ_2019_Q30")),
    B("Tempting idea: 3 squares, so 3 times 36. Do you think that's right? Think about the edges where the squares join.",
      ask=THINK),
    B("That's the trap! Where two squares join, those edges end up inside the rectangle. They are not on the boundary any more."),
    B("So let's find the real sides. One side of a square is 36 divided by 4, which is 9 centimetres.", W("l1", "36 ÷ 4 = 9")),
    B("Three squares side by side. How long is the rectangle?",
      ask=choose(["9 cm", "27 cm", "36 cm"], 1, "Three sides of 9 centimetres sit end to end along the length. So we need 3 lots of 9.")),
    B("3 times 9 is 27. The rectangle is 27 centimetres long and still 9 centimetres wide.", W("l2", "3 × 9 = 27")),
    B("27 plus 9 is 36. That is halfway round. Double it: 72.", W("l3", "27 + 9 = 36"), W("l4", "2 × 36 = 72")),
    B("The perimeter of the rectangle is 72 centimetres.", A("a", "Perimeter = 72 cm", label=True), ring("a", "72")),
    B("So when shapes are joined, don't add their perimeters. Find the new sides, then go round the outside."),
])

LESSONS["Q_CH14_022"] = lesson([
    B("The perimeter of a rectangle is 42 centimetres, and its length is 13 centimetres. What is the breadth?",
      G("Rectangle: perimeter = 42 cm, length = 13 cm. Breadth = ?"), F("Q_CH14_022")),
    B("The perimeter is two lengths and two breadths. So half of it is one length plus one breadth. Half of 42 is 21.",
      W("l1", "42 ÷ 2 = 21"), note("l1", "21", "length + breadth", "below")),
    B("Length plus breadth is 21, and the length is 13. How do we find the breadth?",
      ask=choose(["42 − 13", "21 − 13", "21 + 13"], 1,
                 "42 is the whole way round. One length and one breadth make only 21. So we take 13 away from 21.")),
    B("21 minus 13 is 8.", W("l2", "21 − 13 = 8")),
    B("The breadth is 8 centimetres.", A("a", "Breadth = 8 cm", label=True), ring("a", "8")),
    B("The trap is taking 13 from 42 straight away. That removes one length, but another length and two breadths are still there."),
    B("Check: 13 plus 8 is 21, and double 21 is 42. It fits.", W("c", "2 × (13 + 8) = 42")),
])

LESSONS["Q_CH20_001"] = lesson([
    B("What do all the angles of a quadrilateral add up to? Let's work it out instead of just remembering it.",
      G("Sum of all angles of a quadrilateral = ?"), F("Q_CH20_001")),
    B("Here's a fact you know: the three angles of a triangle add up to 180 degrees.",
      L("l1", "Triangle: angles add up to 180°")),
    B("Now draw one diagonal across the quadrilateral, from corner to corner. How many triangles does it make?",
      F("Q_CH20_001", 0),
      ask=choose(["2", "3", "4"], 0, "One straight cut from corner to corner splits the shape into two pieces, and each piece has three sides.")),
    B("2 triangles. And together their angles make up all four angles of the quadrilateral.", mark("l1", "180°", "circle")),
    B("Each triangle gives 180. So we need 2 times 180, which is 360.", W("l2", "2 × 180 = 360")),
    B("The angles of a quadrilateral add up to 360 degrees.", A("a", "Sum of angles = 360°", label=True), ring("a", "360°")),
    B("A square is a good check. It has 4 right angles of 90 degrees, and 4 times 90 is 360.", W("c", "4 × 90 = 360")),
    B("So remember: a quadrilateral is two triangles stuck together, and two lots of 180 make 360."),
])

LESSONS["Q_CH20_002"] = lesson([
    B("How many axes of symmetry does a rectangle have, if it is not a square?",
      G("Rectangle (not a square): axes of symmetry = ?"), F("Q_CH20_002")),
    B("An axis of symmetry is a fold line. Fold along it, and one half lands exactly on the other half.",
      L("l1", "Axis of symmetry = a fold line that matches")),
    B("Take a sheet of paper. Fold it so the top edge meets the bottom edge. The halves match. That is 1 axis.",
      L("l2", "fold across the middle: yes"), F("Q_CH20_002", 0)),
    B("Now fold it so the left edge meets the right edge. The halves match again. That is 2.",
      L("l3", "fold down the middle: yes"), F("Q_CH20_002", 1)),
    B("What about folding corner to corner, along a diagonal? Will the halves match?",
      ask=choose(["Yes, they match", "No, the corners miss"], 1,
                 "Try it with a sheet of paper. The corners stick out past each other, because the long side and the short side are different.")),
    B("The corners don't land on each other, because the length and the breadth are different. So the diagonals are not axes.",
      L("l4", "fold along a diagonal: no"), F("Q_CH20_002", 2)),
    B("A rectangle that is not a square has 2 axes of symmetry.", A("a", "2 axes of symmetry", label=True), ring("a", "2")),
    B("A square has 4, because its diagonals work as well. That is why the question says not a square."),
])

LESSONS["Q_CH20_003"] = lesson([
    B("A square has a side of 11 centimetres. What is its perimeter?",
      G("Square: side 11 cm. Perimeter = ?"), F("Q_CH20_003")),
    B("Perimeter is the distance all the way round. A square has 4 equal sides. So which sum do we need?",
      ask=choose(["11 × 11", "4 × 11", "2 × 11"], 1,
                 "Walk round the square: 4 sides, each 11 centimetres. So we need 4 lots of 11.")),
    B("4 lots of 11.", L("l1", "Perimeter = 4 × side"), mark("l1", "4", "circle")),
    B("4 times 10 is 40, and 4 times 1 is 4. Together that makes 44.", W("l2", "4 × 11 = 40 + 4"), W("l3", "40 + 4 = 44")),
    B("The perimeter is 44 centimetres.", A("a", "Perimeter = 44 cm", label=True), ring("a", "44")),
    B("Careful: 11 times 11 gives the area, the space inside. We wanted the distance round the edge."),
    B("Check by walking: 11, 11, 11 and 11 make 44.", W("c", "11 + 11 + 11 + 11 = 44")),
])

LESSONS["Q_CH20_004"] = lesson([
    B("A square has a side of 9 metres. What is its area?", G("Square: side 9 m. Area = ?"), F("Q_CH20_004")),
    B("Area is the space inside. For a square it is side times side. So we need 9 times 9.",
      L("l1", "Area = side × side")),
    B("9 times 9 is 81.", W("l2", "9 × 9 = 81")),
    B("Now watch out. Two of the choices say 81! One says 81 metres. The other says 81 square metres. Which one is an area?",
      L("o", "81 m  or  81 sq. m ?"),
      ask=choose(["81 m", "81 sq. m"], 1,
                 "Metres measure a length, like the side of the square. Area counts squares, so it is measured in square metres.")),
    B("Area is counted in squares, each 1 metre by 1 metre. So the area is 81 square metres.",
      A("a", "Area = 81 sq. m", label=True), ring("a", "81 sq. m")),
    B("Another trap: 4 times 9 is 36. That is the perimeter, the distance round the edge.", W("l3", "4 × 9 = 36"),
      note("l3", "36", "perimeter", "below")),
    B("So for area: side times side, and always say square units. Here that is 81 square metres."),
])
