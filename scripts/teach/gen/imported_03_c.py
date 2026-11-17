"""Lessons for textbook chapter 20 (area): unit changes, costs, triangles, walls, tiles."""
from imported_03_b import square_area_from_perimeter, square_perimeter_from_area
from imported_03_lib import ANS, ANSR, B, FIG, G, GIVEN, M, N, S, W, WN, choose, lesson

LESSONS = {}
P = "IPMTB_grade5_ch20_"

# ── Length in metres, breadth in centimetres ─────────────────────────────────
LESSONS[P + "q001"] = lesson(
    B("A rectangle with a length of 1.2 metres and a breadth of 50 centimetres. We want its area.",
      GIVEN("q1", "Rectangle: length 1.2 m, breadth 50 cm. Area = ?")),
    B("Before we multiply anything, look at the units. What do you notice?",
      ask=choose(["both are in metres", "one is metres, one is centimetres", "both are in centimetres"], 1,
                 "Read the two measurements again. The length is in metres, but the breadth is in centimetres. They do not match yet.")),
    B("The answer is wanted in square centimetres, so let's turn the length into centimetres. 1 metre is 100 centimetres.",
      W("r", "1 m = 100 cm", label=True)),
    B("So 1.2 metres is 1.2 times 100, which is 120 centimetres.",
      W("a", "1.2 × 100 = 120"), S("q1", "1.2 m", "120 cm")),
    B("Now both sides are in centimetres, and area is length times breadth. 12 times 5 is 60, and the two zeros go on the end: 6000 square centimetres.",
      W("b", "12 × 5 = 60"), ANSR("c", "120 × 50 = 6000", "6000")),
    B("Here is the trap. Multiply 1.2 by 50 straight away and you get 60. But that mixes metres with centimetres, so it means nothing.",
      W("d", "1.2 × 50 = 60"), N("d", "1.2 × 50", "m × cm: mixed units", "below")),
    B("So before any area sum, make the units match. Then it is just length times breadth."),
)

# ── Square whose area and perimeter are the same number ──────────────────────
LESSONS[P + "q006"] = lesson(
    B("A square whose area and perimeter are the very same number. We have to find its side.",
      GIVEN("q1", "Square: area = perimeter. Side = ?")),
    B("Write the two rules side by side. Area is side times side. Perimeter is 4 times the side.",
      W("r1", "Area = side × side", label=True), W("r2", "Perimeter = 4 × side", label=True)),
    B("Let's try a small square and watch. With side 2, the area is 2 times 2, which is 4. The perimeter is 4 times 2, which is 8. Not equal.",
      W("a", "2 × 2 = 4"), W("b", "4 × 2 = 8")),
    B("Look at the two rules again. Both multiply the side by something. When will they give the same answer?",
      M("r1", "side", "underline"), M("r2", "4", "underline"),
      ask=choose(["when the side is 4", "when the side is 1", "when the side is 0"], 0,
                 "One rule multiplies the side by the side, the other multiplies it by 4. They agree when those two are the same, so the side must be 4.")),
    B("Try 4. The area is 4 times 4, which is 16. The perimeter is 4 times 4, which is 16. Equal!",
      W("c", "4 × 4 = 16"), ANSR("d", "Side = 4 units", "4", True)),
    B("What about 0? The numbers do match, but a square with side 0 is no square at all. So we leave that one out."),
    B("And bigger squares? With side 5, the area is 25 but the perimeter is only 20. From here on the area runs ahead, so 4 is the only answer.",
      W("e", "5 × 5 = 25"), W("g", "4 × 5 = 20")),
    B("So when a question gives a rule but no numbers, write the formulas side by side and test small numbers."),
)

# ── Perimeter 50, length 3/2 times the breadth ───────────────────────────────
LESSONS[P + "q007"] = lesson(
    B("A rectangle with a perimeter of 50 centimetres. Its length is 3 over 2 times its breadth, and we want the area.",
      GIVEN("q1", "Rectangle: perimeter 50 cm, length = 3/2 × breadth"), GIVEN("q2", "Area = ?")),
    B("3 over 2 times sounds hard, so let's make it easy. Cut the breadth into 2 equal parts. Then the length is 3 of those same parts.",
      FIG("f1", {"kind": "barModel", "bars": [
          {"label": "length", "segments": [{"units": 1, "tone": "a"}, {"units": 1, "tone": "a"}, {"units": 1, "tone": "a"}]},
          {"label": "breadth", "segments": [{"units": 1, "tone": "b"}, {"units": 1, "tone": "b"}]}]}),
      W("r", "breadth = 2 parts, length = 3 parts", label=True)),
    B("Half of the perimeter is one length plus one breadth. Half of 50 is 25.",
      WN("a", "50 ÷ 2 = 25", "25", "length + breadth")),
    B("One length and one breadth together: how many parts is that?",
      ask=choose(["5 parts", "6 parts", "3 parts"], 0,
                 "The length is 3 parts and the breadth is 2 parts. Together that is 3 plus 2.")),
    B("3 plus 2 is 5 parts, and they make 25. So one part is 25 divided by 5, which is 5 centimetres.",
      W("b", "3 + 2 = 5"), WN("c", "25 ÷ 5 = 5", "5", "one part")),
    B("The breadth is 2 parts: 2 times 5 is 10. The length is 3 parts: 3 times 5 is 15.",
      WN("d", "2 × 5 = 10", "10", "breadth"), WN("e", "3 × 5 = 15", "15", "length")),
    B("Area is length times breadth. 15 times 10 is 150 square centimetres.",
      ANSR("g", "15 × 10 = 150", "150")),
    B("Check both clues. Twice 15 plus 10 is 50, the perimeter. And 15 is one and a half times 10. Everything fits.",
      W("h", "2 × (15 + 10) = 50")),
    B("So when one side is a fraction of the other, turn the sides into equal parts. Find one part, and the rest follows."),
)

# ── Which playground is bigger ───────────────────────────────────────────────
LESSONS[P + "q008"] = lesson(
    B("Two playgrounds. One is a rectangle, 25 metres by 20 metres. The other is a square with sides of 22 metres. Which one is bigger?",
      GIVEN("q1", "Rectangle: 25 m by 20 m"), GIVEN("q2", "Square: each side 22 m")),
    B("A bigger playground means more room to play. Which measurement tells us that?",
      ask=choose(["the perimeter", "the area", "the longest side"], 1,
                 "Room to run about is the flat space inside the edges. That is the area.")),
    B("The rectangle first. 25 times 20 is 500 square metres.",
      WN("a", "25 × 20 = 500", "500", "rectangle")),
    B("Now the square, 22 times 22. Take it in two bites: 22 times 20 is 440, and 22 times 2 is 44.",
      W("b", "22 × 20 = 440"), W("c", "22 × 2 = 44")),
    B("440 plus 44 is 484 square metres.",
      W("d", "440 + 44 = 484"), WN("e", "22 × 22 = 484", "484", "square")),
    B("500 is more than 484. So the rectangular playground is the bigger one.",
      W("g", "500 > 484"),
      ANS("h", "Bigger: the rectangular playground", True), M("h", "rectangular", "circle")),
    B("Don't judge by the side lengths. 22 looks big next to 20, but the rectangle has that long 25. Only working out both areas settles it."),
    B("So to compare two shapes for size, find the area of each one, then compare the two numbers."),
)

# ── Cost of a plot at 1000 rupees a square metre ─────────────────────────────
LESSONS[P + "q009"] = lesson(
    B("A plot of land is 16 metres long and 10 metres wide. Each square metre costs 1000 rupees. What does the whole plot cost?",
      GIVEN("q1", "Plot 16 m × 10 m. 1 sq m costs Rs. 1000. Cost = ?")),
    B("The price is for each square metre. So what must we find first?",
      ask=choose(["the perimeter", "the area", "the length only"], 1,
                 "Square metres measure the flat surface of the plot, and that is its area.")),
    B("Area is length times breadth. 16 times 10 is 160 square metres.",
      WN("a", "16 × 10 = 160", "160", "sq m")),
    B("Picture 160 squares, each one metre by one metre, and every one of them costs 1000 rupees. So the cost is 160 times 1000.",
      W("b", "160 × 1000")),
    B("To multiply by 1000, write 160 and put three zeros after it. That makes 1,60,000 rupees.",
      ANSR("c", "160 × 1000 = 160000", "160000")),
    B("Careful with the trap. 16 times 1000 is only 16000. That leaves out the breadth altogether.",
      W("d", "16 × 1000 = 16000")),
    B("Check by dividing back. 1,60,000 divided by 1000 is 160, the area we found.",
      W("e", "160000 ÷ 1000 = 160")),
    B("So for a cost on land or floors, find the area first, then multiply by the price of one square metre."),
)

# ── Cost of levelling a ground ───────────────────────────────────────────────
LESSONS[P + "q010"] = lesson(
    B("A ground 30 metres long and 20 metres wide has to be levelled. The charge is 5 rupees for every square metre.",
      GIVEN("q1", "Ground 30 m × 20 m. Levelling: Rs. 5 per sq m. Cost = ?")),
    B("We pay for every square metre of ground. So which sum comes first?",
      ask=choose(["30 + 20", "30 × 20", "30 × 5"], 1,
                 "The number of square metres is the area of the ground. For a rectangle, that is length times breadth.")),
    B("30 times 20. 3 times 2 is 6, and the two zeros go on the end: 600 square metres.",
      WN("a", "30 × 20 = 600", "600", "sq m")),
    B("Careful: 600 is the area, not the cost. Each of those 600 square metres costs 5 rupees.",
      W("b", "600 × 5")),
    B("6 times 5 is 30, so 600 times 5 is 3000. The levelling costs 3000 rupees.",
      W("c", "6 × 5 = 30"), ANSR("d", "600 × 5 = 3000", "3000")),
    B("Check by sharing the money back out. 3000 rupees divided by 5 rupees is 600 square metres, the area we found.",
      W("e", "3000 ÷ 5 = 600")),
    B("So it is always two steps: the area first, then area times the rate."),
)

LESSONS[P + "q011"] = square_perimeter_from_area(
    P + "q011", 144, 10, "144 ends in 4, and 2 times 2 is 4. So let's try 12.",
    "Careful not to divide 144 by 4, and don't stop at 12. The side comes first, then all 4 sides. And the answer is a length, in centimetres.")

# ── Triangle: area and height known, base wanted ─────────────────────────────
LESSONS[P + "q012"] = lesson(
    B("A triangle with an area of 5 square centimetres and a height of 2 centimetres. We want its base. It is isosceles, but that does not change the area rule.",
      GIVEN("q1", "Triangle: area 5 sq cm, height 2 cm. Base = ?")),
    B("The area of a triangle is half of base times height.",
      W("r", "Area = ½ × base × height", label=True)),
    B("Put in what we know. 5 equals half, times the base, times 2.",
      W("a", "5 = ½ × base × 2", label=True)),
    B("Look at the half and the 2 on that line. What is half of 2?",
      ask=choose(["1", "4", "2"], 0,
                 "Half of 2 means 2 split into two equal parts. Each part is 1.")),
    B("So the half and the 2 together make just 1. And 1 times the base is simply the base.",
      G("a", ["½", "2"], "= 1"), W("b", "½ × 2 = 1")),
    B("That leaves 5 equals the base. The base is 5 centimetres.",
      ANSR("c", "Base = 5 cm", "5", True)),
    B("Check it in the rule. Half of 5 times 2 is half of 10, which is 5. That is our area.",
      W("d", "½ × 5 × 2 = 5")),
    B("The trap is to forget the half and say 5 divided by 2. The steady way is: double the area, then divide by the height.",
      W("e", "2 × 5 ÷ 2 = 5")),
    B("So for a missing base, double the area and divide by the height."),
)

# ── Height of a room from the area of its four walls ─────────────────────────
LESSONS[P + "q013"] = lesson(
    B("A room has a floor 5 metres long and 4 metres wide. Its four walls have a total area of 108 square metres. How high is the room?",
      GIVEN("q1", "Floor 5 m × 4 m. Four walls: 108 sq m. Height = ?")),
    B("Imagine unfolding the four walls and laying them flat in a row. They make one long rectangle, exactly as tall as the room.",
      W("r", "4 walls = one long strip", label=True)),
    B("How long is that strip of walls?",
      ask=choose(["the area of the floor", "the perimeter of the floor", "the length of the room"], 1,
                 "The walls stand on the edges of the floor, all the way round. So the strip is as long as the walk round the floor, its perimeter.")),
    B("The floor's perimeter is 2 lengths and 2 breadths. 5 plus 4 is 9, and twice 9 is 18 metres.",
      WN("a", "2 × (5 + 4) = 18", "18", "strip length")),
    B("So the strip is 18 metres long, and its area is 108. Length times height gives area.",
      W("b", "18 × height = 108", label=True)),
    B("The height is 108 divided by 18. Now 18 times 6 is 108, so the room is 6 metres high.",
      ANSR("c", "108 ÷ 18 = 6", "6")),
    B("Check wall by wall. Two walls are 5 by 6, which is 30 each. Two are 4 by 6, which is 24 each. And 30, 30, 24 and 24 make 108.",
      W("d", "5 × 6 = 30"), W("e", "4 × 6 = 24"), W("g", "30 + 30 + 24 + 24 = 108")),
    B("The trap is dividing 108 by the floor area, 20. The walls stand on the floor's edges, so it is the perimeter we need.",
      W("h", "5 × 4 = 20"), N("h", "20", "floor area: not needed", "below")),
    B("So the area of four walls is the perimeter of the floor times the height. Divide to get the height back."),
)

# ── One side up 50 percent, the other down 50 percent ────────────────────────
LESSONS[P + "q014"] = lesson(
    B("One side of a square grows by 50 percent, and the other shrinks by 50 percent. It becomes a rectangle. Is its area bigger, smaller, or the same?",
      GIVEN("q1", "Square: one side + 50%, the other side − 50%"), GIVEN("q2", "New area: bigger, smaller or the same?")),
    B("No numbers are given, so let's choose an easy square. Say each side is 10. Its area is 10 times 10, which is 100.",
      WN("a", "10 × 10 = 100", "100", "square")),
    B("50 percent means half. So what is 50 percent of 10?",
      ask=choose(["5", "50", "2"], 0,
                 "50 percent is the same as half. And half of 10 is 5.")),
    B("One side grows by 5: 10 plus 5 is 15. The other shrinks by 5: 10 minus 5 is 5.",
      W("b", "10 + 5 = 15"), W("c", "10 − 5 = 5")),
    B("One side went up by 5 and the other came down by 5. What do you think happens to the area?",
      ask=choose(["it stays the same", "it gets smaller", "it gets bigger"], 1,
                 "It feels as if up 5 and down 5 should cancel out. But area multiplies the sides, so let's work it out and see.")),
    B("The new rectangle is 15 times 5, which is 75. And 75 is less than 100.",
      WN("d", "15 × 5 = 75", "75", "rectangle"), W("e", "75 < 100")),
    B("So the rectangle's area is smaller than the square's.",
      ANS("g", "The new area is smaller than the square", True), M("g", "smaller", "circle")),
    B("That is the trap: the same percent up and down does not cancel. One side became one and a half times as long, but the other became only half. Together that makes just three quarters of the square.",
      W("h", "3/2 × 1/2 = 3/4"), N("h", "3/4", "of the square", "below")),
    B("So when a question gives no numbers, pick easy ones and try it. The sums will show you what really happens."),
)

# ── Tiles of side 25 cm on a 5 m by 4 m floor ────────────────────────────────
LESSONS[P + "q017"] = lesson(
    B("A hall is 5 metres long and 4 metres wide. It is covered with square tiles of side 25 centimetres. How many tiles are needed?",
      GIVEN("q1", "Hall 5 m × 4 m, square tiles of side 25 cm. Tiles = ?")),
    B("Metres and centimetres are mixed, so first we make them match. 1 metre is 100 centimetres, so the hall is 500 centimetres by 400 centimetres.",
      W("r", "1 m = 100 cm", label=True), W("a", "5 × 100 = 500"), W("b", "4 × 100 = 400")),
    B("How many 25 centimetre tiles fit in one row along the 500 centimetre length?",
      ask=choose(["20", "25", "50"], 0,
                 "Four 25s make 100. There are 5 hundreds in 500, so that is 4 times 5, which is 20 tiles.")),
    B("500 divided by 25 is 20 tiles in a row. And across the breadth, 400 divided by 25 is 16 rows.",
      WN("c", "500 ÷ 25 = 20", "20", "tiles in a row"), WN("d", "400 ÷ 25 = 16", "16", "rows")),
    B("So the floor is a grid of tiles: 16 rows, with 20 tiles in each row. 20 times 16 is 320 tiles.",
      ANSR("e", "20 × 16 = 320", "320")),
    B("Check it with areas. The floor is 500 times 400, which is 200000 square centimetres. One tile is 25 times 25, which is 625.",
      W("g", "500 × 400 = 200000"), W("h", "25 × 25 = 625")),
    B("And 200000 divided by 625 is 320. The same answer both ways.",
      W("i", "200000 ÷ 625 = 320")),
    B("The trap is using 5 and 4 with 25 without changing units. Metres and centimetres must never be mixed in one sum."),
    B("So for tiles: same units first, count how many fit along each side, then multiply."),
)

# ── A 100 cm wire: square, then a rectangle 5 longer and 5 narrower ──────────
LESSONS[P + "q018"] = lesson(
    B("A wire 100 centimetres long is bent into a square. Then the same wire makes a rectangle, 5 centimetres longer and 5 centimetres narrower than the square.",
      GIVEN("q1", "Wire 100 cm, bent into a square"),
      GIVEN("q2", "Rectangle: length = side + 5 cm, breadth = side − 5 cm"),
      GIVEN("q3", "Difference between the two areas = ?")),
    B("The wire goes all the way round the square, so 100 centimetres is its perimeter. One side is 100 divided by 4, which is 25.",
      WN("a", "100 ÷ 4 = 25", "25", "side of square")),
    B("The area of the square is 25 times 25, which is 625 square centimetres.",
      WN("b", "25 × 25 = 625", "625", "square")),
    B("Now the rectangle. Its length is 5 more than 25, and its breadth is 5 less than 25. What are they?",
      ask=choose(["30 and 20", "30 and 25", "25 and 20"], 0,
                 "Both sides change. 25 plus 5 is 30 for the length, and 25 minus 5 is 20 for the breadth.")),
    B("So the rectangle is 30 by 20, and 30 times 20 is 600 square centimetres.",
      W("c", "25 + 5 = 30"), W("d", "25 − 5 = 20"), WN("e", "30 × 20 = 600", "600", "rectangle")),
    B("The difference is 625 minus 600, which is 25 square centimetres.",
      ANSR("g", "625 − 600 = 25", "25")),
    B("Don't answer 625 or 600. Those are the two areas, and the question wants the gap between them."),
    B("Notice something. Both shapes use the same wire: twice 30 plus 20 is 100 too. Yet the square holds more, by exactly 5 times 5.",
      W("h", "2 × (30 + 20) = 100"), W("i", "5 × 5 = 25")),
    B("So: the perimeter gives the side, the side gives each area, and then we subtract."),
)

# ── Triangle with base 5.2 and height 2.9 ────────────────────────────────────
LESSONS[P + "q021"] = lesson(
    B("A triangle with a base of 5.2 centimetres and a height of 2.9 centimetres. We want its area.",
      GIVEN("q1", "Triangle: base 5.2 cm, height 2.9 cm. Area = ?"),
      FIG("f1", {"kind": "triangle", "shape": "scalene", "sides": {"bc": "5.2 cm"}, "height": "2.9 cm"})),
    B("The area of a triangle is half of base times height.",
      W("r", "Area = ½ × base × height", label=True)),
    B("A smart move is to halve one of the numbers first. Which one halves more easily?",
      ask=choose(["5.2", "2.9", "neither"], 0,
                 "5.2 ends in an even digit, so it halves neatly. 2.9 ends in an odd digit, so its half would be messier.")),
    B("Half of 5.2 is 2.6. So the area is 2.6 times 2.9.",
      W("a", "5.2 ÷ 2 = 2.6"), W("b", "½ × 5.2 × 2.9 = 2.6 × 2.9")),
    B("Leave the decimal points out for a moment: 26 times 29. Now 26 times 30 is 780, and taking away one 26 leaves 754.",
      W("c", "26 × 30 = 780"), W("d", "780 − 26 = 754"), W("e", "26 × 29 = 754")),
    B("Time to put the point back. 2.6 and 2.9 have one decimal place each. So how many decimal places does the answer have?",
      ask=choose(["1", "2", "3"], 1,
                 "Count the decimal places in both numbers: one, and one more. Together that makes 2 decimal places in the answer.")),
    B("So 754 becomes 7.54. The area is 7.54 square centimetres.",
      ANSR("g", "2.6 × 2.9 = 7.54", "7.54")),
    B("Does that look right? Half of 5 times 3 is 7 and a half, so 7.54 is sensible. And area is in square centimetres, not plain centimetres."),
    B("So for a triangle: halve the easy number, multiply, then count the decimal places."),
)

# ── Area of a square of side 6.1 ─────────────────────────────────────────────
LESSONS[P + "q022"] = lesson(
    B("A square with each side 6.1 centimetres. We want its area.",
      GIVEN("q1", "Square, each side 6.1 cm. Area = ?"),
      FIG("f1", {"kind": "rectangle", "square": True, "length": "6.1 cm", "breadth": "6.1 cm", "inside": "Area = ?"})),
    B("Which sum gives the area of a square?",
      ask=choose(["4 × 6.1", "6.1 × 6.1", "6.1 + 6.1"], 1,
                 "4 times the side is the walk round the edge, which is the perimeter. Area is the space inside: side times side.")),
    B("That is the trap in this question. 4 times 6.1 is 24.4, but that is the perimeter, a length.",
      W("a", "4 × 6.1 = 24.4"), N("a", "24.4", "perimeter, not area", "below")),
    B("So we need 6.1 times 6.1. Leave the points out for now: 61 times 61. Well, 61 times 60 is 3660, and one more 61 makes 3721.",
      W("b", "61 × 60 = 3660"), W("c", "3660 + 61 = 3721")),
    B("Each 6.1 has one decimal place. So where does the point go in 3721?",
      ask=choose(["372.1", "37.21", "3.721"], 1,
                 "One decimal place and one more make two. So count two digits from the right, and put the point there.")),
    B("That gives 37.21. The area is 37.21 square centimetres.",
      ANSR("d", "6.1 × 6.1 = 37.21", "37.21")),
    B("A quick sense check: 6 times 6 is 36, and 6.1 is a little more than 6. So a little more than 36 is just right.",
      W("e", "6 × 6 = 36")),
    B("So for the area of a square, multiply the side by itself, then count the decimal places in the answer."),
)

# ── Area of a rectangle 1.1 cm by 30 cm ──────────────────────────────────────
LESSONS[P + "q023"] = lesson(
    B("A rectangle with a length of 1.1 centimetres and a breadth of 30 centimetres. We want its area.",
      GIVEN("q1", "Rectangle: length 1.1 cm, breadth 30 cm. Area = ?")),
    B("Both sides are already in centimetres, so we can multiply straight away. Area is length times breadth.",
      W("r", "Area = length × breadth", label=True), W("a", "1.1 × 30")),
    B("1.1 is 1 whole and 1 tenth. What is 1 tenth of 30?",
      ask=choose(["3", "0.3", "30"], 0,
                 "A tenth means divide by 10. And 30 divided by 10 is 3.")),
    B("So split the sum in two. 1 times 30 is 30, and 0.1 times 30 is 3.",
      W("b", "1 × 30 = 30"), W("c", "0.1 × 30 = 3")),
    B("30 plus 3 is 33. The area is 33 square centimetres.",
      W("d", "30 + 3 = 33"), ANSR("e", "1.1 × 30 = 33", "33")),
    B("Here is another way to see it. 11 times 30 is 330, and one decimal place brings that back to 33.",
      W("g", "11 × 30 = 330"), W("h", "330 ÷ 10 = 33")),
    B("Watch the decimal point: it is 33, not 330. And we multiplied centimetres by centimetres, so the answer is in square centimetres."),
    B("So for an area with a decimal, split the decimal into its whole and its tenths, multiply each, and add."),
)

# ── Triangle: area 120, base 40, height in millimetres ───────────────────────
LESSONS[P + "q025"] = lesson(
    B("A triangle with an area of 120 square centimetres and a base of 40 centimetres. We want its height.",
      GIVEN("q1", "Triangle: area 120 sq cm, base 40 cm. Height = ?")),
    B("The area of a triangle is half of base times height.",
      W("r", "Area = ½ × base × height", label=True)),
    B("Put in what we know. Half of the base is half of 40, which is 20. So 20 times the height is 120.",
      W("a", "½ × 40 = 20"), W("b", "20 × height = 120", label=True)),
    B("20 times the height is 120. So how do we find the height?",
      ask=choose(["120 ÷ 20", "120 × 20", "120 − 20"], 0,
                 "20 times something gives 120. To undo the times, we divide 120 by 20.")),
    B("120 divided by 20 is 6. The height is 6 centimetres.",
      WN("c", "120 ÷ 20 = 6", "6", "cm")),
    B("Now look at the choices: none of them says 6 centimetres. A height is a length, so which unit could be right?",
      ask=choose(["sq cm", "mm", "sq mm"], 1,
                 "Square units are for area. A height is a length, so it needs a plain length unit, like millimetres.")),
    B("1 centimetre is 10 millimetres. So 6 centimetres is 6 times 10, which is 60 millimetres.",
      W("d", "1 cm = 10 mm", label=True), W("e", "6 × 10 = 60"), ANSR("g", "Height = 6 cm = 60 mm", "60 mm", True)),
    B("Check it in the rule. Half of 40 is 20, and 20 times 6 is 120. And mind the trap: 120 divided by 40 gives 3, which forgets the half.",
      W("h", "½ × 40 × 6 = 120")),
    B("So for a missing height: halve the base, divide the area by that, and then check which unit the answer is wanted in."),
)

LESSONS[P + "q027"] = square_area_from_perimeter(
    P + "q027", 52, "millimetres", "mm",
    "Look at the units. The side is in millimetres, so the area is in square millimetres. Not square centimetres, and not plain millimetres.")
