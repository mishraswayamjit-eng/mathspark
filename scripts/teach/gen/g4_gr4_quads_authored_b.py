"""Lessons written one by one: Grade 4 quadrilaterals, G4A_QUADS_001 to 013."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_quads")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["G4A_QUADS_001"] = lesson([
    B("A shape has four sides, all equal, but none of its angles is a right angle. What is it called?",
      G("4 equal sides, no right angles. What is it called?"), F("G4A_QUADS_001")),
    B("We have two clues. Clue one: all four sides are equal. Which shapes have four equal sides?",
      ask=choose(["square and rectangle", "square and rhombus", "rectangle and trapezium"], 1,
                 "A rectangle only needs its opposite sides equal. The two shapes with all four sides equal are the square and the rhombus.")),
    B("So it is either a square or a rhombus.", L("l1", "4 equal sides: square or rhombus")),
    B("Clue two: none of its angles is a right angle. A square always has four right angles. So it can't be a square.",
      strike("l1", "square", "has right angles")),
    B("What is left is the rhombus. Think of a square that has been pushed over, like a diamond.",
      A("a", "It is a rhombus", label=True), ring("a", "rhombus")),
    B("So: four equal sides and no right angles means a rhombus."),
    B("When a question gives two clues, use both. The first clue narrows it down, and the second one decides."),
])

LESSONS["G4A_QUADS_002"] = lesson([
    B("One angle of a parallelogram is 70 degrees. We want the angle right next to it.",
      G("Parallelogram: one angle = 70°. Angle next to it = ?"), F("G4A_QUADS_002")),
    B("In a parallelogram, two angles next to each other always add up to 180 degrees. If one is small, its neighbour is big.",
      L("l1", "Neighbours add up to 180°"), box("l1", "180°")),
    B("So how do we find the angle next to 70 degrees?",
      ask=choose(["It is 70° too", "360 − 70", "180 − 70"], 2,
                 "The equal angle is the one opposite, across the shape. The neighbour is different: together the two must make 180.")),
    B("180 minus 70 is 110.", W("l2", "180 − 70 = 110")),
    B("So the angle next to it is 110 degrees.", A("a", "Angle next to it = 110°", label=True), ring("a", "110°")),
    B("Careful: 70 degrees is the angle opposite, not the one next door. Opposite angles are equal. Neighbours make 180."),
    B("Check: 70 plus 110 makes 180. It works.", W("c", "70 + 110 = 180")),
])

LESSONS["G4A_QUADS_003"] = lesson([
    B("The perimeter of a rhombus is 52 centimetres. How long is each side?",
      G("Rhombus: perimeter = 52 cm. Each side = ?"), F("G4A_QUADS_003")),
    B("What is special about a rhombus? All four of its sides are the same length, just like a square.",
      L("l1", "Rhombus: 4 equal sides"), mark("l1", "4 equal sides")),
    B("So 4 equal sides add up to 52. How do we find one side?",
      ask=choose(["52 ÷ 2", "52 − 4", "52 ÷ 4"], 2,
                 "The 52 centimetres is shared equally among 4 sides. Sharing equally means dividing, and there are 4 sides.")),
    B("52 divided by 4. Half of 52 is 26, and half of 26 is 13.",
      W("l2", "52 ÷ 2 = 26"), W("l3", "26 ÷ 2 = 13")),
    B("So each side of the rhombus is 13 centimetres.", A("a", "Each side = 13 cm", label=True), ring("a", "13")),
    B("Check by walking round: 13, 13, 13 and 13 make 52. It fits.", W("c", "13 + 13 + 13 + 13 = 52")),
    B("Remember: a side is always shorter than the whole perimeter. For 4 equal sides, divide the perimeter by 4."),
])

LESSONS["G4A_QUADS_004"] = lesson([
    B("A square handkerchief has sides of 25 centimetres. Lace goes all around its edge, and costs 3 rupees for every centimetre. What does the lace cost?",
      G("Square, side 25 cm. Lace all round, ₹3 per cm. Cost = ?"), F("G4A_QUADS_004")),
    B("First, how much lace? The lace goes all around the edge. So do we need the area or the perimeter?",
      ask=choose(["the area", "the perimeter"], 1,
                 "Lace is stitched along the edge, not spread over the cloth. The distance round the edge is the perimeter.")),
    B("A square has 4 equal sides. 4 times 25 is 100. So we need 100 centimetres of lace.",
      W("l1", "4 × 25 = 100"), note("l1", "100", "cm of lace", "below")),
    B("Each centimetre costs 3 rupees. So 100 centimetres cost 100 times 3, which is 300.",
      W("l2", "100 × 3 = 300")),
    B("The lace costs 300 rupees.", A("a", "Cost = ₹300", label=True), ring("a", "₹300")),
    B("The trap is to stop at one side. 25 times 3 is 75, but that only pays for one edge of the handkerchief.",
      W("l3", "25 × 3 = 75"), note("l3", "75", "one side only", "below")),
    B("So: all around means perimeter. Find the length first, then multiply by the price."),
])

LESSONS["G4A_QUADS_005"] = lesson([
    B("A wire is bent into a square of side 18 centimetres. Then the same wire makes a rectangle whose length is twice its breadth. What is the rectangle's area?",
      G("Wire: square of side 18 cm, then a rectangle"), GQ("q2", "Length = 2 × breadth. Area = ?"), F("G4A_QUADS_005")),
    B("The wire's length is the square's perimeter. 4 times 18 is 72 centimetres.",
      W("l1", "4 × 18 = 72"), note("l1", "72", "the wire", "below")),
    B("Now the rectangle. Its length is twice its breadth. So one length is the same as 2 breadths.",
      L("l2", "1 length = 2 breadths")),
    B("Walk round the rectangle: length, breadth, length, breadth. Counting in breadths, how many is that altogether?",
      ask=choose(["3 breadths", "4 breadths", "6 breadths"], 2,
                 "Each length counts as 2 breadths. So round the rectangle we have 2, then 1, then 2, then 1. Add those up.")),
    B("2 plus 1 plus 2 plus 1 is 6. So 6 breadths use up the whole 72 centimetres of wire.",
      W("l3", "2 + 1 + 2 + 1 = 6")),
    B("72 divided by 6 is 12. The breadth is 12 centimetres, and the length is twice that: 24.",
      W("l4", "72 ÷ 6 = 12"), W("l5", "2 × 12 = 24")),
    B("Area is length times breadth: 24 times 12. 24 times 10 is 240, and 24 times 2 is 48.",
      W("l6", "24 × 10 = 240"), W("l7", "24 × 2 = 48")),
    B("240 plus 48 makes 288. The area of the rectangle is 288 square centimetres.",
      W("l8", "240 + 48 = 288"), A("a", "Area = 288 cm²", label=True), ring("a", "288")),
    B("Notice the trap. The square's area is 18 times 18, a different number. Same wire means same perimeter, not same area."),
    B("Check the wire: 24 plus 12 is 36, and double 36 is 72. It fits, so 288 it is.",
      W("c1", "24 + 12 = 36"), W("c2", "2 × 36 = 72")),
])

LESSONS["G4A_QUADS_006"] = lesson([
    B("A garden is 20 metres long and 14 metres wide. A path 2 metres wide runs all around it, on the outside. What is the area of the path?",
      G("Garden 20 m by 14 m. Path 2 m wide all round."), GQ("q2", "Area of the path = ?"), F("G4A_QUADS_006")),
    B("The path is like a frame round the garden. Here's a neat trick: find the big rectangle with the path, then take away the garden.",
      L("l1", "Path = big rectangle − garden")),
    B("The path is 2 metres wide at the left end and at the right end. So how long is the big rectangle?",
      ask=choose(["20 m", "20 + 2 = 22 m", "20 + 4 = 24 m"], 2,
                 "The path is at both ends of the garden. So the length grows by 2 metres at one end and 2 metres at the other.")),
    B("That's the trap: the path is on both sides, so each measurement grows by 2 and 2. The length is 24 metres and the width is 18 metres.",
      W("l2", "20 + 2 + 2 = 24"), W("l3", "14 + 2 + 2 = 18"), F("G4A_QUADS_006", 0)),
    B("Big rectangle: 24 times 18. 24 times 10 is 240, and 24 times 8 is 192. Together that is 432.",
      W("l4", "24 × 10 = 240"), W("l5", "24 × 8 = 192"), W("l6", "240 + 192 = 432")),
    B("The garden alone is 20 times 14, which is 280.", W("l7", "20 × 14 = 280")),
    B("Take the garden away from the big rectangle. 432 minus 280 is 152.", W("l8", "432 − 280 = 152")),
    B("So the area of the path is 152 square metres.", A("a", "Area of path = 152 m²", label=True), ring("a", "152")),
    B("For a path all round: add the path's width twice to each side, find the big area, and subtract the inside."),
])

LESSONS["G4A_QUADS_007"] = lesson([
    B("A floor is 6 metres long and 4 metres wide. It is covered with square tiles of side 50 centimetres. How many tiles are needed?",
      G("Floor 6 m by 4 m. Square tiles of side 50 cm."), GQ("q2", "How many tiles?"), F("G4A_QUADS_007")),
    B("Watch the units! The floor is in metres but the tile is in centimetres. How many tiles of 50 centimetres fit along 1 metre?",
      L("l1", "1 m = 100 cm = 50 cm + 50 cm"),
      ask=choose(["5", "50", "2"], 2,
                 "1 metre is 100 centimetres. 50 and 50 make 100, so two tiles fit along each metre.")),
    B("Two tiles for every metre. Along the 6 metre side we fit 6 times 2, which is 12 tiles.", W("l2", "6 × 2 = 12")),
    B("Along the 4 metre side we fit 4 times 2, which is 8 tiles. So the floor has 8 rows of 12 tiles.", W("l3", "4 × 2 = 8")),
    B("8 rows of 12. 12 times 8 is 96.", W("l4", "12 × 8 = 96")),
    B("The floor needs 96 tiles.", A("a", "96 tiles", label=True), ring("a", "96")),
    B("The trap is 6 times 4, which is 24. That counts big squares of 1 metre, and each of those holds 4 tiles. 24 times 4 is 96 again.",
      W("c1", "6 × 4 = 24"), W("c2", "24 × 4 = 96")),
    B("So: put everything in the same unit, count the tiles each way, then multiply."),
])

LESSONS["G4A_QUADS_008"] = lesson([
    B("A square sheet of paper has sides of 12 centimetres. One straight cut makes two equal rectangles. What is the perimeter of each rectangle?",
      G("Square of side 12 cm, cut into 2 equal rectangles."), GQ("q2", "Perimeter of each rectangle = ?"),
      F("G4A_QUADS_008")),
    B("The cut goes through the middle. One side of each piece is still 12 centimetres. What is the other side?",
      ask=choose(["12 cm", "6 cm", "24 cm"], 1,
                 "The cut goes through the middle of a 12 centimetre side. So that side is shared into two equal halves.")),
    B("Half of 12 is 6. So each piece is 12 centimetres long and 6 centimetres wide.", W("l1", "12 ÷ 2 = 6")),
    B("Now walk round one piece: 12, 6, 12, 6. That adds up to 36.", W("l2", "12 + 6 + 12 + 6 = 36")),
    B("The perimeter of each rectangle is 36 centimetres.",
      A("a", "Perimeter of each = 36 cm", label=True), ring("a", "36")),
    B("Here's a surprise. The square's perimeter is 4 times 12, which is 48, and half of that is 24. But the answer isn't 24!",
      W("l3", "4 × 12 = 48"), W("l4", "48 ÷ 2 = 24")),
    B("Why not? The cut makes a new edge of 12 centimetres on each piece. 24 plus that new 12 gives 36.",
      W("l5", "24 + 12 = 36"), note("l5", "12", "the new edge", "below")),
    B("When you cut a shape, new edges appear. So find the sides of the new piece and add them up."),
])

LESSONS["G4A_QUADS_009"] = lesson([
    B("Think about four shapes: square, rectangle, rhombus and parallelogram. How many of them always have four right angles?",
      G("Square, rectangle, rhombus, parallelogram"), GQ("q2", "How many ALWAYS have 4 right angles?"),
      F("G4A_QUADS_009")),
    B("The important word is always. Let's test the shapes one at a time. Square first: four right angles, every time. Yes.",
      box("q2", "ALWAYS"), L("l1", "Square: yes")),
    B("Rectangle: four right angles is what makes it a rectangle. Yes, always.", L("l2", "Rectangle: yes")),
    B("Now the rhombus. It has four equal sides. But does it always have right angles?",
      ask=choose(["Yes, always", "No, it can lean over"], 1,
                 "Picture the diamond on a playing card. Its four sides are equal, but its corners are not square corners.")),
    B("A rhombus can lean over, like a diamond. So, not always.", L("l3", "Rhombus: not always")),
    B("A parallelogram can lean over too. Not always.", L("l4", "Parallelogram: not always")),
    B("Count the yeses: the square and the rectangle. That makes 2.",
      A("a", "2 shapes: square and rectangle", label=True), ring("a", "2")),
    B("When you see the word always, hunt for a shape that breaks the rule. One leaning rhombus is enough to say no."),
])

LESSONS["G4A_QUADS_010"] = lesson([
    B("A rectangle is 20 centimetres long and 15 centimetres wide. The length is made 5 centimetres longer, and the width 5 centimetres shorter. What happens to the area?",
      G("Rectangle 20 cm by 15 cm."), GQ("q2", "Length + 5 cm, width − 5 cm. The area?"), F("G4A_QUADS_010")),
    B("Area at the start: 20 times 15, which is 300.", W("l1", "20 × 15 = 300")),
    B("Now change the sides. The length grows to 20 plus 5, which is 25. The width shrinks to 15 minus 5, which is 10.",
      W("l2", "20 + 5 = 25"), W("l3", "15 − 5 = 10")),
    B("We added 5 to one side and took 5 from the other. Do you think the area stays the same? Have a guess.", ask=THINK),
    B("Let's find out. The new area is 25 times 10, which is 250.", W("l4", "25 × 10 = 250")),
    B("It changed! 300 has become 250. So what happened to the area?",
      ask=choose(["It got bigger by 50", "It got smaller by 50", "It stayed the same"], 1,
                 "Compare 300 at the start with 250 now. The new number is the smaller one.")),
    B("300 minus 250 is 50. The area decreases by 50 square centimetres.",
      W("l5", "300 − 250 = 50"), A("a", "It decreases by 50 cm²", label=True), ring("a", "decreases by 50")),
    B("Here's the trap. Plus 5 and minus 5 keeps the perimeter the same, but not the area. For area, work out both and compare."),
])

LESSONS["G4A_QUADS_011"] = lesson([
    B("A hall is 12 metres long and 9 metres wide. Carpet costs 150 rupees for each square metre. A wooden strip along the walls costs 40 rupees for each metre. What is the total cost?",
      G("Hall 12 m by 9 m."), GQ("q2", "Carpet ₹150 per sq m. Strip ₹40 per m. Total = ?"), F("G4A_QUADS_011")),
    B("Two things to buy, and each uses a different measure. The carpet covers the whole floor. Which measure is that?",
      ask=choose(["perimeter", "area"], 1,
                 "Carpet covers the space inside the room, and space inside is area. The strip along the walls is the one that uses perimeter.")),
    B("Carpet uses area: 12 times 9 is 108 square metres.", W("l1", "12 × 9 = 108"), note("l1", "108", "area", "below")),
    B("Each square metre costs 150 rupees. 100 times 150 is 15,000, and 8 times 150 is 1,200. Together that is 16,200 rupees.",
      W("l2", "100 × 150 = 15000"), W("l3", "8 × 150 = 1200"), W("l4", "15000 + 1200 = 16200")),
    B("The strip runs along all four walls. That is the perimeter. 12 plus 9 is 21, and double is 42 metres.",
      W("l5", "12 + 9 = 21"), W("l6", "2 × 21 = 42"), note("l6", "42", "perimeter", "below")),
    B("Each metre of strip costs 40 rupees. 42 times 4 is 168, so 42 times 40 is 1,680 rupees.",
      W("l7", "42 × 4 = 168"), W("l8", "42 × 40 = 1680")),
    B("Add the two costs. 16,200 plus 1,680 makes 17,880.", W("l9", "16200 + 1680 = 17880")),
    B("So the total cost is 17,880 rupees.", A("a", "Total cost = ₹17,880", label=True), ring("a", "₹17,880")),
    B("The trap is using one measure for both. Covering a floor uses area. Going along the edge uses perimeter."),
])

LESSONS["G4A_QUADS_012"] = lesson([
    B("A field is 30 metres long and 20 metres wide. Fence posts go all around it, 5 metres apart, with one at each corner. How many posts are needed?",
      G("Field 30 m by 20 m. Posts every 5 m, all round."), GQ("q2", "How many posts?"), F("G4A_QUADS_012")),
    B("Posts go all the way round, so first we need the distance round. 30 plus 20 is 50, and double is 100 metres.",
      W("l1", "30 + 20 = 50"), W("l2", "2 × 50 = 100")),
    B("The posts are 5 metres apart. 100 divided by 5 is 20. So there are 20 gaps between posts.",
      W("l3", "100 ÷ 5 = 20"), note("l3", "20", "gaps", "below")),
    B("Now the tricky bit. In a straight line of posts you need one extra post at the end. But is this fence a straight line?",
      ask=choose(["Yes, so add one more post", "No, it is a closed loop"], 1,
                 "The fence goes round the field and comes back to where it began. So the last gap ends at the very first post.")),
    B("Round a loop, the last gap ends at the first post. So no extra post is needed. Posts and gaps are equal in number.",
      L("l4", "Round a loop: posts = gaps")),
    B("The field needs 20 posts.", A("a", "20 posts", label=True), ring("a", "20")),
    B("Think of a tiny square with a post at each corner. 4 gaps, 4 posts. It is the same idea here."),
    B("So: find the distance round, divide by the gap, and for a closed loop that is your number of posts."),
])

LESSONS["G4A_QUADS_013"] = lesson([
    B("A wire 40 centimetres long is bent into a rectangle with whole number sides, and the length is greater than the breadth. Find the largest area minus the smallest area.",
      G("Wire 40 cm, bent into a rectangle. Length > breadth."), GQ("q2", "Largest area − smallest area = ?"),
      F("G4A_QUADS_013")),
    B("The wire is the perimeter, 40 centimetres. So length plus breadth is half of that: 20.",
      W("l1", "40 ÷ 2 = 20"), note("l1", "20", "length + breadth", "below")),
    B("Lots of pairs add up to 20. 19 and 1. 18 and 2. 17 and 3. All the way to 11 and 9.",
      L("l2", "19 + 1, 18 + 2, 17 + 3, ... 11 + 9")),
    B("Which pair gives the smallest area? Try the long thin one. 19 times 1 is only 19.", W("l3", "19 × 1 = 19")),
    B("As the sides get closer together, the area grows. 18 times 2 is already 36. So which pair gives the largest area?",
      W("l4", "18 × 2 = 36"),
      ask=choose(["19 and 1", "10 and 10", "11 and 9"], 2,
                 "10 and 10 would be a square, but the question says the length is greater than the breadth. The closest pair we are allowed is 11 and 9.")),
    B("That's the trap! 10 and 10 is not allowed, because the length must be greater. So the largest is 11 times 9, which is 99.",
      W("l5", "11 × 9 = 99")),
    B("Now the difference. 99 minus 19 is 80.", W("l6", "99 − 19 = 80")),
    B("So the difference is 80 square centimetres.", A("a", "Difference = 80 sq cm", label=True), ring("a", "80")),
    B("Same wire, very different areas. Thin rectangles hold little, and nearly square ones hold the most."),
])
