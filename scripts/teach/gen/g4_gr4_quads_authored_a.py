"""Lessons written one by one: Grade 4 quadrilaterals, past-paper and worksheet questions."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_quads")
LESSONS = {}


def GQ(id, text):
    """A second line of the question, in the question's ink."""
    return W(id, text, tone="given", label=True)


LESSONS["EXT_G4_FP_2020_017"] = lesson([
    B("Here's a rectangle. Its length is 8 feet, and the length is 2 more than the width. We need the area.",
      G("Length = 8 ft, 2 more than the width. Area = ?"), F("EXT_G4_FP_2020_017")),
    B("For area we need the length and the width. We know the length. So how wide is the rectangle?",
      ask=choose(["8 + 2 = 10 ft", "8 − 2 = 6 ft", "2 ft"], 1,
                 "The length is the bigger side here: it is 2 more than the width. So the width must be 2 less than 8.")),
    B("The length is 2 more, so the width is 2 less. 8 minus 2 is 6 feet.",
      W("l1", "8 − 2 = 6"), note("l1", "6", "width", "below")),
    B("Careful: the 2 is not the width. It only tells us how much shorter the width is.",
      box("q", "2 more")),
    B("Now, area is length times width. 8 times 6 is 48.",
      L("f1", "Area = length × width"), W("l2", "8 × 6 = 48")),
    B("So the area is 48 square feet.", A("a", "Area = 48 sq ft", label=True), ring("a", "48")),
    B("Quick check: is 8 really 2 more than 6? Yes. So our sides fit the question.", W("c", "6 + 2 = 8")),
    B("The plan: find the missing side first, then multiply the two sides."),
])

LESSONS["EXT_G4_FP_2020_028"] = lesson([
    B("A wire is bent into a rectangle, 16 centimetres by 12 centimetres. Then the same wire is bent into a square. How long is each side of the square?",
      G("Wire: rectangle 16 cm by 12 cm, then a square. Side = ?"), F("EXT_G4_FP_2020_028")),
    B("The wire goes all the way round the rectangle. So the length of the wire is the rectangle's what?",
      ask=choose(["area", "perimeter", "length"], 1,
                 "The wire is the edge of the shape, not the space inside. The distance round the edge is the perimeter.")),
    B("One length and one width make 16 plus 12, which is 28. That is halfway round.",
      W("l1", "16 + 12 = 28"), note("l1", "28", "halfway round", "below")),
    B("Double it for the whole wire. 2 times 28 is 56 centimetres.",
      W("l2", "2 × 28 = 56"), note("l2", "56", "the wire", "below")),
    B("Now the same 56 centimetres is bent into a square, and a square has 4 equal sides. What do we do with 56?",
      ask=choose(["56 ÷ 4", "56 ÷ 2", "56 × 4"], 0,
                 "The wire is shared equally among the 4 sides of the square. Sharing equally means dividing by 4.")),
    B("56 divided by 4. Half of 56 is 28, and half of 28 is 14.", W("l3", "56 ÷ 4 = 14")),
    B("So each side of the square is 14 centimetres.", A("a", "Side of the square = 14 cm", label=True), ring("a", "14")),
    B("Check: 4 sides of 14 make 56, the whole wire. It fits.", W("c", "4 × 14 = 56")),
    B("Same wire means same perimeter. Find the perimeter first, then share it among the new sides."),
])

LESSONS["EXT_G4_FP_2021_038"] = lesson([
    B("A square has side a, and its perimeter is 28 centimetres. A rectangle is 3 a long and 2 a wide. We want the rectangle's area.",
      G("Square: side a, perimeter = 28 cm"), GQ("q2", "Rectangle: 3a by 2a. Area = ?"), F("EXT_G4_FP_2021_038")),
    B("First we need a. The square's 4 equal sides add up to 28. So how long is one side?",
      ask=choose(["28 ÷ 2 = 14", "28 ÷ 4 = 7", "28 × 4 = 112"], 1,
                 "A square has 4 equal sides, and together they make 28. So we share 28 into 4 equal parts.")),
    B("28 divided by 4 is 7. So a is 7 centimetres.", W("l1", "28 ÷ 4 = 7"), note("l1", "7", "a", "below")),
    B("Now the rectangle. 3 a means 3 times 7, which is 21. And 2 a means 2 times 7, which is 14.",
      W("l2", "3 × 7 = 21"), W("l3", "2 × 7 = 14")),
    B("Area is length times width: 21 times 14. Let's split 14 into 10 and 4.",
      W("l4", "21 × 14 = 21 × 10 + 21 × 4")),
    B("21 times 10 is 210. 21 times 4 is 84. Together that makes 294.", W("l5", "210 + 84 = 294")),
    B("Now look at the choices: 149, 274, 245, or None. Our 294 is not there! What should we do?",
      L("o", "Choices: 149, 274, 245, None"),
      ask=choose(["Pick the closest, 274", "Choose None"], 1,
                 "When the working is sound, trust it. 274 is close, but close is not equal. The choice None is there for exactly this.")),
    B("Here's the trap: 274 looks a lot like 294. Never grab a number just because it is close.",
      box("o", "274"), A("a", "Area = 294 cm², so the answer is None", label=True), ring("a", "None")),
    B("Let's check our sum another way. 20 times 14 is 280, and one more 14 makes 294. Still 294.",
      W("c1", "20 × 14 = 280"), W("c2", "280 + 14 = 294")),
    B("So: find a first, build the sides, then multiply. And trust your working, even when the answer is None."),
])

LESSONS["EXT_G4_FP_2022_013"] = lesson([
    B("The perimeter of a square is 132 centimetres. We want its area.",
      G("Square: perimeter = 132 cm. Area = ?"), F("EXT_G4_FP_2022_013")),
    B("For area we need the side. The 4 equal sides add up to 132. How do we find one side?",
      ask=choose(["132 ÷ 4", "132 ÷ 2", "132 × 4"], 0,
                 "A square has 4 equal sides. Together they make 132, so we share 132 into 4 equal parts.")),
    B("132 divided by 4. Half of 132 is 66, and half of 66 is 33. So each side is 33 centimetres.",
      W("l1", "132 ÷ 2 = 66"), W("l2", "66 ÷ 2 = 33"), note("l2", "33", "side", "below")),
    B("Area is side times side: 33 times 33. Split one 33 into 30 and 3.",
      L("f1", "Area = side × side"), W("l3", "33 × 33 = 33 × 30 + 33 × 3")),
    B("33 times 30 is 990. And 33 times 3 is 99.", W("l4", "33 × 30 = 990"), W("l5", "33 × 3 = 99")),
    B("Add the two parts. 990 plus 99 makes 1089.", W("l6", "990 + 99 = 1089")),
    B("Now be careful, because two of the choices say 1089! The side was in centimetres. So which unit does the area have?",
      L("o", "1089 cm.sq or 1089 m.sq ?"),
      ask=choose(["square metres", "square centimetres"], 1,
                 "Look back at the question: the perimeter is in centimetres. So the little squares we count are square centimetres.")),
    B("So the area is 1089 square centimetres. Always read the unit as well as the number.",
      A("a", "Area = 1089 cm.sq", label=True), ring("a", "1089 cm.sq")),
    B("Check the side: 4 times 33 is 132. That is our perimeter.", W("c", "4 × 33 = 132")),
    B("For a square: divide the perimeter by 4 to get the side. Then side times side gives the area."),
])

LESSONS["EXT_G4_FP_2023_012"] = lesson([
    B("A square and an equilateral triangle have the same perimeter. Each side of the triangle is 12 centimetres. We want the area of the square.",
      G("Square and equilateral triangle: same perimeter"), GQ("q2", "Triangle side = 12 cm. Area of square = ?"),
      F("EXT_G4_FP_2023_012")),
    B("Start with the shape we know. An equilateral triangle has 3 equal sides. So its perimeter is 3 times 12, which is 36.",
      W("l1", "3 × 12 = 36"), F("EXT_G4_FP_2023_012", 0)),
    B("The square has the same perimeter, 36 centimetres. How long is each side of the square?",
      ask=choose(["12 cm", "36 ÷ 3 = 12 cm", "36 ÷ 4 = 9 cm"], 2,
                 "12 centimetres is the triangle's side. The square shares the same 36 centimetres among 4 sides, so its sides are shorter.")),
    B("36 shared among 4 equal sides is 9. So the square's side is 9 centimetres, not 12.",
      W("l2", "36 ÷ 4 = 9"), F("EXT_G4_FP_2023_012", 1)),
    B("Now the area. Side times side: 9 times 9 is 81.", W("l3", "9 × 9 = 81")),
    B("So the area of the square is 81 square centimetres.",
      A("a", "Area of square = 81 sq.cm", label=True), ring("a", "81"), F("EXT_G4_FP_2023_012", 3)),
    B("Check: 4 sides of 9 make 36, the same as the triangle. Good.", W("c", "4 × 9 = 36")),
    B("The trap was using 12 for the square. Same perimeter does not mean same side!"),
])

LESSONS["EXT_G4_FP_2024_011"] = lesson([
    B("A square and an equilateral triangle have equal perimeters. The triangle's sides are 16 centimetres each. What is the area of the square?",
      G("Perimeter of square = perimeter of triangle"), GQ("q2", "Triangle side = 16 cm. Area of square = ?"),
      F("EXT_G4_FP_2024_011")),
    B("We can't use 16 for the square. That is the triangle's side. So what should we find first?",
      box("q2", "Triangle side = 16 cm"),
      ask=choose(["16 × 16", "the triangle's perimeter", "16 ÷ 4"], 1,
                 "The only thing the two shapes share is the perimeter. So we begin with the triangle's perimeter.")),
    B("All 3 sides of the triangle are 16 centimetres. 3 times 16 is 48.", W("l1", "3 × 16 = 48"),
      note("l1", "48", "perimeter", "below")),
    B("The square has that same perimeter, 48, shared among 4 equal sides. 48 divided by 4 is 12.",
      W("l2", "48 ÷ 4 = 12"), note("l2", "12", "side of square", "below")),
    B("Now the area of the square is side times side. 12 times 12 is 144.", W("l3", "12 × 12 = 144")),
    B("So the area of the square is 144 square centimetres.",
      A("a", "Area of square = 144 cm.sq", label=True), ring("a", "144")),
    B("Check the perimeters. Square: 4 times 12 is 48. Triangle: 48 as well. They match.", W("c", "4 × 12 = 48")),
    B("Remember the path: triangle's perimeter, then the square's side, then the square's area."),
])

LESSONS["EXT_G4_FP_2024_024"] = lesson([
    B("Eight equal circles sit inside a rectangle, in 2 rows of 4. They touch each other and the sides. Each radius is 4 centimetres. What is the rectangle's area?",
      G("8 circles in a rectangle: 2 rows of 4"), GQ("q2", "Radius = 4 cm. Area of rectangle = ?"),
      F("EXT_G4_FP_2024_024")),
    B("The circles are packed tight, so they tell us how big the rectangle is. How wide is one whole circle?",
      ask=choose(["4 cm", "8 cm", "16 cm"], 1,
                 "4 centimetres is the radius: from the centre to the edge. Right across the circle is the diameter, and that is twice as much.")),
    B("Here's the trap: a circle takes up its whole diameter, not its radius. 2 times 4 is 8 centimetres.",
      W("l1", "2 × 4 = 8"), note("l1", "8", "diameter", "below"), F("EXT_G4_FP_2024_024", 0)),
    B("Along the length, 4 circles sit side by side. So the length is 4 times 8, which is 32 centimetres.",
      W("l2", "4 × 8 = 32"), F("EXT_G4_FP_2024_024", 1)),
    B("Up the side there are 2 rows. So the breadth is 2 times 8, which is 16 centimetres.",
      W("l3", "2 × 8 = 16"), F("EXT_G4_FP_2024_024", 2)),
    B("Area is length times breadth: 32 times 16. Split 16 into 10 and 6.",
      W("l4", "32 × 16 = 32 × 10 + 32 × 6")),
    B("32 times 10 is 320. 32 times 6 is 192. Add them and we get 512.",
      W("l5", "320 + 192 = 512")),
    B("So the area of the rectangle is 512 square centimetres.",
      A("a", "Area = 512 cm.sq", label=True), ring("a", "512")),
    B("So: change the radius to a diameter, count the circles each way, then multiply."),
])

LESSONS["EXT_G4_FP_2024_032"] = lesson([
    B("A rectangle has a perimeter of 76 centimetres. Four pairs of sides are offered. Which pair cannot be its length and breadth?",
      G("Rectangle: perimeter = 76 cm"), GQ("q2", "Which pair CANNOT be the length and breadth?"),
      F("EXT_G4_FP_2024_032")),
    B("The perimeter is two lengths and two breadths. So what must one length and one breadth add up to?",
      ask=choose(["76", "38", "152"], 1,
                 "76 is all four sides. One length and one breadth is only halfway round, so we halve 76.")),
    B("Half of 76 is 38. So a pair fits only if it adds up to 38.", W("l1", "76 ÷ 2 = 38"), box("l1", "38")),
    B("Now test each pair. 22 plus 16 is 38. That one fits.", W("l2", "22 + 16 = 38")),
    B("11 plus 27 is 38. That fits too.", W("l3", "11 + 27 = 38")),
    B("24 plus 16 is 40. That's not 38!", W("l4", "24 + 16 = 40"), ring("l4", "40")),
    B("Test the last one, just to be sure. 29 plus 9 is 38. It fits.", W("l5", "29 + 9 = 38")),
    B("With 24 and 16, the perimeter would be 2 times 40, which is 80, not 76.", W("c", "2 × 40 = 80")),
    B("So the pair that cannot be the sides is 24 centimetres and 16 centimetres.",
      A("a", "Cannot be: 24 cm & 16 cm", label=True), ring("a", "24 cm & 16 cm")),
    B("Notice the word cannot. Three pairs work, and we want the one that doesn't. Always read which one the question wants."),
])

LESSONS["EXT_G4_FP_2025_028"] = lesson([
    B("A rectangle is 12 centimetres broad, and its perimeter is 52 centimetres. We want its area.",
      G("Rectangle: breadth = 12 cm, perimeter = 52 cm. Area = ?"), F("EXT_G4_FP_2025_028")),
    B("For area we need the length too. The perimeter is two lengths and two breadths, so half of it is one length plus one breadth.",
      W("l1", "52 ÷ 2 = 26"), note("l1", "26", "length + breadth", "below")),
    B("Length and breadth together make 26. The breadth is 12. So what is the length?",
      ask=choose(["52 − 12 = 40", "26 − 12 = 14", "26 + 12 = 38"], 1,
                 "52 is the whole way round, with two breadths in it. Use the half instead: length plus breadth is 26, so the length is 26 minus 12.")),
    B("26 minus 12 is 14. The length is 14 centimetres.", W("l2", "26 − 12 = 14")),
    B("Now the area: length times breadth, 14 times 12. 14 times 10 is 140, and 14 times 2 is 28.",
      W("l3", "14 × 10 = 140"), W("l4", "14 × 2 = 28")),
    B("140 plus 28 makes 168. So the area is 168 square centimetres.",
      W("l5", "140 + 28 = 168"), A("a", "Area = 168 cm sq", label=True), ring("a", "168")),
    B("Check the perimeter: 14 plus 12 is 26, and double 26 is 52. It fits.", W("c", "2 × 26 = 52")),
    B("So: halve the perimeter, take away the side you know, then multiply the two sides."),
])

LESSONS["EXT_G4_WS2_CH20_003"] = lesson([
    B("Here is a rectangle. How many right angles does it have?",
      G("A rectangle has how many right angles?"), F("EXT_G4_WS2_CH20_003")),
    B("A right angle is a square corner, like the corner of a book. It measures 90 degrees.",
      L("l1", "Right angle = square corner = 90°"), mark("l1", "square corner")),
    B("Look at the picture. How many corners does a rectangle have?",
      ask=choose(["2", "3", "4"], 2, "Count them in the picture: top left, top right, bottom right, bottom left.")),
    B("4 corners. Now think of a door, or a page of your notebook. Every corner is a neat square corner."),
    B("That is what makes a rectangle a rectangle: all 4 of its angles are right angles.",
      A("a", "A rectangle has 4 right angles", label=True), ring("a", "4 right angles")),
    B("If even one corner leaned over, the shape would not be a rectangle any more."),
    B("So remember: a rectangle means 4 right angles, every time."),
])

LESSONS["EXT_G4_WS2_CH20_004"] = lesson([
    B("Here is a quadrilateral: a shape with 4 sides and 4 corners. How many diagonals does it have?",
      G("How many diagonals does a quadrilateral have?"), F("EXT_G4_WS2_CH20_004")),
    B("A diagonal is a straight line joining two corners that are not next to each other. Let's draw one, from A across to C.",
      L("l1", "Diagonal: joins opposite corners"), F("EXT_G4_WS2_CH20_004", 0)),
    B("Is there another one? Which two corners are still not joined?",
      ask=choose(["A and B", "B and D", "C and D"], 1,
                 "A and B are neighbours, and so are C and D. The line joining neighbours is a side. The corners still across from each other are B and D.")),
    B("B and D are opposite each other. Join them, and we have a second diagonal.",
      L("l2", "A to C, B to D"), F("EXT_G4_WS2_CH20_004", 1)),
    B("Any more? Every other pair of corners, like A and B, is already joined by a side. So that is all of them."),
    B("A quadrilateral has 2 diagonals.", A("a", "2 diagonals", label=True), ring("a", "2")),
    B("The trap is to say 4, because there are 4 sides. Diagonals join opposite corners, and there are only 2 opposite pairs."),
])

LESSONS["EXT_G4_WS2_CH20_005"] = lesson([
    B("Three angles of a quadrilateral are 80 degrees, 90 degrees and 100 degrees. We want the fourth angle.",
      G("Quadrilateral: angles 80°, 90°, 100° and ?"), F("EXT_G4_WS2_CH20_005")),
    B("Here is the key fact. The four angles of any quadrilateral add up to 360 degrees.",
      L("l1", "4 angles add up to 360°"), box("l1", "360°")),
    B("First add the three angles we know. 80 plus 90 is 170, and 100 more makes 270.",
      W("l2", "80 + 90 = 170"), W("l3", "170 + 100 = 270")),
    B("Three angles make 270. All four must make 360. So how do we find the fourth?",
      ask=choose(["360 + 270", "270 − 90", "360 − 270"], 2,
                 "All four angles must make 360. Three of them already make 270. The fourth is whatever is left, so we subtract.")),
    B("360 minus 270 is 90. The fourth angle is 90 degrees.",
      W("l4", "360 − 270 = 90"), A("a", "Fourth angle = 90°", label=True), ring("a", "90°")),
    B("Check: 80, 90, 100 and 90 add up to 360. It works.", W("c", "80 + 90 + 100 + 90 = 360")),
    B("So for a missing angle in a quadrilateral: add the three you know, and take the total from 360."),
])
