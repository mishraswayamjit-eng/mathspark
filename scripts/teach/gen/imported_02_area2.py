"""Area and perimeter, part 2: covering and tiling, borders and paths, triangles, longer one-offs."""
from imported_02_lib import ANS, B, FIG, GIVEN, L, M, N, W, choose, lesson, num
from imported_02_area import rect, side_ask

LESSONS = {}
P = "AIGEN_grade5_"


# ── How many sheets or packets cover a rectangle ─────────────────────────────

LESSONS[P + "03e12fba-287f-4f66-86b3-1d5612e0ffb9"] = lesson(
    B("Riya wants to cover a wall, 8 metres long and 5 metres wide, with rangoli paper. Each sheet covers exactly 4 square metres. How many sheets?",
      GIVEN("q", "Wall 8 m × 5 m, 1 sheet covers 4 sq. m"), L("q2", "Sheets = ?"),
      FIG("f1", rect("8 m", "5 m", "Area = ?"))),
    B("Each sheet covers an area. So what do we need to know about the wall first?",
      ask=choose(["its perimeter", "its area", "its length"], 1,
                 "Paper covers a surface: the flat space inside the edges. That space is the wall's area.")),
    B("Area is length times breadth. 8 times 5 is 40 square metres.",
      W("w", "8 × 5 = 40"), N("w", "40", "wall")),
    B("Each sheet covers 4 of those 40 square metres. How do we find the number of sheets?",
      ask=choose(["40 × 4", "40 − 4", "40 ÷ 4"], 2,
                 "We are asking how many 4s fit into 40. That is a division.")),
    B("40 divided by 4 is 10. Riya needs 10 sheets.",
      ANS("a", "40 ÷ 4 = 10"), M("a", "10", "circle")),
    B("Check: 10 sheets of 4 square metres each. 10 times 4 is 40. The whole wall is covered.",
      W("c", "10 × 4 = 40")),
    B("The slip is to stop at 40. That is the wall's area in square metres, not the number of sheets. And 13 is just 8 plus 5, which is not an area at all.",
      W("t", "8 + 5 = 13")),
    B("Covering questions go like this: area of the whole thing, divided by the area 1 piece covers."),
)

LESSONS[P + "d157d455-f536-4b7d-ae81-d99bd91141f2"] = lesson(
    B("Priya's rangoli is a rectangle, 9 metres long and 5 metres wide. Each packet of coloured powder covers 3 square metres. How many packets fill the whole rangoli?",
      GIVEN("q", "Rangoli 9 m × 5 m, 1 packet covers 3 sq. m"), L("q2", "Packets = ?"),
      FIG("f1", rect("9 m", "5 m", "Area = ?"))),
    B("Powder fills the space inside the rangoli. Which sum measures that space?",
      ask=choose(["9 + 5 = 14", "9 × 5 = 45", "2 × (9 + 5) = 28"], 1,
                 "Adding the sides only measures along the edges. The space inside is the area: 5 rows of 9 square metres.")),
    B("9 times 5 is 45. The rangoli covers 45 square metres.",
      W("w", "9 × 5 = 45"), N("w", "45", "rangoli")),
    B("Each packet covers 3 of those square metres. So we need to know how many 3s there are in 45. That is a division.",
      W("d", "45 ÷ 3 = ?")),
    B("30 divided by 3 is 10, and the 15 left over, divided by 3, is 5. So 45 divided by 3 is 15 packets.",
      W("d1", "30 ÷ 3 = 10"), W("d2", "15 ÷ 3 = 5"), ANS("a", "45 ÷ 3 = 15"), M("a", "15", "circle")),
    B("Check: 15 packets, 3 square metres each. 15 times 3 is 45. The whole rangoli is filled, with nothing left over.",
      W("c", "15 × 3 = 45")),
    B("Don't stop at 45. That is how many square metres there are, not how many packets. And 14 comes from adding 9 and 5, which is not an area."),
    B("So: find the area, then divide by what 1 packet covers."),
)


# ── Square tiles on a floor ──────────────────────────────────────────────────

def tiles(intro, given, fig, floor_say, floor_line, A, s, unit, tail):
    T = s * s
    return lesson(*([
        B(intro, GIVEN("q", given[0]), L("q2", given[1]), FIG("f1", fig)),
        B(floor_say, W("w", floor_line), N("w", num(A), "floor")),
        side_ask(s, "tile", unit.split(" ")[1]),
        B("%d times %d is %d. So each tile covers %d %s." % (s, s, T, T, unit),
          W("p", "%d × %d = %d" % (s, s, T)), N("p", str(T), "1 tile", nth=("%d × %d = %d" % (s, s, T)).count(str(T)))),
        B("The floor is %s %s and each tile covers %d. How do we find the number of tiles?" % (num(A), unit, T),
          ask=choose(["%s ÷ %d" % (num(A), s), "%s × %d" % (num(A), T), "%s ÷ %d" % (num(A), T)], 2,
                     "We want to know how many tile areas fit into the floor area. So we divide area by area: %s by %d, not by the side of the tile."
                     % (num(A), T))),
    ] + tail))


LESSONS[P + "bfa55199-50a5-4865-a627-c17c7f7f6ad6"] = tiles(
    "Arjun is tiling a kitchen floor, 12 metres long and 8 metres wide. Each square tile has a side of 2 metres. How many tiles cover the whole floor?",
    ["Floor 12 m × 8 m, square tiles of side 2 m", "Tiles = ?"],
    rect("12 m", "8 m", "tile: side 2 m"),
    "Tiles cover a surface, so this is about area. The floor is 12 times 8, which is 96 square metres.",
    "12 × 8 = 96", 96, 2, "square metres",
    [
        B("96 divided by 4. Half of 96 is 48, and half of 48 is 24. Arjun needs 24 tiles.",
          W("d1", "96 ÷ 2 = 48"), W("d2", "48 ÷ 2 = 24"), ANS("a", "96 ÷ 4 = 24"), M("a", "24", "circle")),
        B("Check by picturing the tiles. 6 fit along the length, and 4 rows fit down the breadth. 6 times 4 is 24.",
          W("c1", "12 ÷ 2 = 6"), W("c2", "8 ÷ 2 = 4"), W("c3", "6 × 4 = 24"),
          FIG("f2", {"kind": "grid", "rows": 4, "cols": 6})),
        B("Did you notice 48 on the way? It is one of the choices. It comes from dividing by 2, the side of the tile, when we should divide by its area."),
        B("For tiling: floor area, divided by the area of 1 tile."),
    ])

LESSONS[P + "2ccc6511-7533-486b-b0a8-599a82d1fa8e"] = tiles(
    "Aarav is tiling a kitchen floor that is 12 metres long and 9 metres wide. Each square tile has a side of 3 metres. How many tiles does he need?",
    ["Floor 12 m × 9 m, square tiles of side 3 m", "Tiles = ?"],
    rect("12 m", "9 m", "tile: side 3 m"),
    "To cover a floor we need its area. Length times breadth: 12 times 9 is 108 square metres.",
    "12 × 9 = 108", 108, 3, "square metres",
    [
        B("108 divided by 9. We know that 9 times 12 is 108, so the answer is 12. Aarav needs 12 tiles.",
          W("d1", "9 × 12 = 108"), ANS("a", "108 ÷ 9 = 12"), M("a", "12", "circle")),
        B("Check by picturing the tiles. 4 fit along the length, and 3 rows fit down the breadth. 4 times 3 is 12.",
          W("c1", "12 ÷ 3 = 4"), W("c2", "9 ÷ 3 = 3"), W("c3", "4 × 3 = 12"),
          FIG("f2", {"kind": "grid", "rows": 3, "cols": 4})),
        B("The trap is to divide 108 by 3, the side of the tile. That gives 36, three times too many. A tile covers an area, so divide by its area.",
          W("t", "108 ÷ 3 = 36")),
        B("For tiling: floor area, divided by the area of 1 tile."),
    ])

LESSONS[P + "91e7ed21-b09a-45ff-8263-ac4de3fe45c5"] = tiles(
    "Rohan's bathroom floor is a square with a side of 50 centimetres. He covers it with small square tiles of side 5 centimetres. How many tiles?",
    ["Square floor of side 50 cm, square tiles of side 5 cm", "Tiles = ?"],
    rect("50 cm", "50 cm", "tile: side 5 cm", square=True),
    "Tiles cover a surface, so we need areas. The floor is a square, so its area is side times side: 50 times 50 is 2,500 square centimetres.",
    "50 × 50 = 2,500", 2500, 5, "square centimetres",
    [
        B("25 times 100 is 2,500. So 2,500 divided by 25 is 100. Rohan needs 100 tiles.",
          W("d1", "25 × 100 = 2,500"), ANS("a", "2,500 ÷ 25 = 100"), M("a", "100", "circle")),
        B("Check by picturing the tiles. 50 divided by 5 is 10, so 10 tiles fit in a row. And there are 10 rows. 10 times 10 is 100.",
          W("c1", "50 ÷ 5 = 10"), W("c2", "10 × 10 = 100"),
          FIG("f2", {"kind": "grid", "rows": 10, "cols": 10})),
        B("That shows the trap. 10 is only the number of tiles along 1 edge. The floor needs row after row of them."),
        B("For tiling: floor area, divided by the area of 1 tile."),
    ])

LESSONS[P + "55700548-8de3-454e-9cda-14843e62777a"] = lesson(
    B("Ankit's kitchen floor is 9 metres long and 5 metres wide. Each square tile has a side of 1 metre and costs 45 rupees. What will all the tiles cost?",
      GIVEN("q", "Floor 9 m × 5 m, tiles of side 1 m, ₹45 each"), L("q2", "Cost = ?"),
      FIG("f1", {"kind": "rectangle", "length": "9 m", "breadth": "5 m", "grid": {"cols": 9, "rows": 5}})),
    B("Each tile is 1 metre by 1 metre, so it covers exactly 1 square metre. That means the number of tiles is the same as the floor's area. Which sum gives that?",
      ask=choose(["9 + 5 = 14", "9 × 5 = 45", "2 × (9 + 5) = 28"], 1,
                 "Adding the sides only counts along the edges. Tiles fill the whole floor, row after row: 5 rows of 9.")),
    B("9 times 5 is 45. The floor is 45 square metres, so it takes 45 tiles.",
      W("w", "9 × 5 = 45"), N("w", "45", "tiles")),
    B("Now the cost. 45 tiles, at 45 rupees each. Careful: the two 45s are different things. One counts tiles, the other counts rupees.",
      L("l2", "45 tiles, ₹45 each")),
    B("How do we find the total cost?",
      ask=choose(["45 + 45", "45 × 45", "45 ÷ 45"], 1,
                 "Every one of the 45 tiles costs 45 rupees. 45 lots of 45 is a multiplication.")),
    B("Split one 45 into 40 and 5. 45 times 40 is 1,800, and 45 times 5 is 225. Together, 2,025 rupees.",
      W("m1", "45 × 40 = 1,800"), W("m2", "45 × 5 = 225"),
      ANS("m", "45 × 45 = 1,800 + 225 = 2,025"), M("m", "2,025", "circle")),
    B("Does that feel right? 45 is a little less than 50, and 45 times 50 would be 2,250. A little less than 2,250 is sensible.",
      W("c", "45 × 50 = 2,250")),
    B("The choices 630 and 1,260 come from adding the sides, or going round the edge, to count the tiles. Tiles cover the inside of the floor, so we need the area.",
      W("t1", "14 × 45 = 630"), W("t2", "28 × 45 = 1,260")),
    B("So: area gives the number of tiles, and tiles times price gives the cost."),
)


# ── Borders and paths ────────────────────────────────────────────────────────

LESSONS[P + "08bfdcbd-9431-4ec2-878b-b57a81e96794"] = lesson(
    B("Ravi's garden is 18 metres long and 12 metres wide. A path 2 metres wide runs all the way round, just inside the edge. The vegetable patch is what is left in the middle.",
      GIVEN("q", "Garden 18 m × 12 m, path 2 m wide inside"), L("q2", "Area of the vegetable patch = ?"),
      FIG("f1", {"kind": "rectangle", "length": "18 m", "breadth": "12 m", "inside": "patch = ?", "highlight": ["border"]})),
    B("The patch is a smaller rectangle. The path is 2 metres wide. So how much shorter than the garden is the patch?",
      ask=choose(["2 m shorter", "4 m shorter", "8 m shorter"], 1,
                 "The path runs along both ends of the garden. It takes 2 metres off one end and 2 metres off the other end. That is 4 metres altogether.")),
    B("So the length of the patch is 18, take away 2, take away 2 again. That is 14 metres.",
      W("l", "18 − 2 − 2 = 14"), N("l", "14", "patch length")),
    B("The width loses 2 metres on each side as well. 12, take away 2, take away 2, is 8 metres.",
      W("b", "12 − 2 − 2 = 8"), N("b", "8", "patch width")),
    B("Now the patch is a rectangle, 14 by 8, and area is length times breadth. 10 times 8 is 80, and 4 times 8 is 32. Together, 112 square metres.",
      W("a1", "10 × 8 = 80"), W("a2", "4 × 8 = 32"), ANS("a", "14 × 8 = 80 + 32 = 112"), M("a", "112", "circle")),
    B("Check against the whole garden. 18 times 12 is 216 square metres. The patch takes 112, leaving 104 for the path. A patch smaller than the garden: sensible.",
      W("c1", "18 × 12 = 216"), W("c2", "216 − 112 = 104")),
    B("The classic slip is to take the path off only once. That gives 16 by 10, which is 160: much too big. A path all the way round comes off twice.",
      W("t", "16 × 10 = 160")),
    B("For a border inside a rectangle: take twice its width off the length, and twice off the breadth, then multiply."),
)

LESSONS[P + "37f1c808-f5f1-42e6-9b01-858f41d54856"] = lesson(
    B("Priya's courtyard is 12 metres long and 8 metres wide. A rangoli border 1 metre wide runs all round the inside edge. We want the area of just the border.",
      GIVEN("q", "Courtyard 12 m × 8 m, border 1 m wide inside"), L("q2", "Area of the border = ?"),
      FIG("f1", {"kind": "rectangle", "length": "12 m", "breadth": "8 m", "inside": "inner part", "highlight": ["border"]})),
    B("A border is a frame shape, awkward to measure directly. So here is the trick: find the whole courtyard, find the empty middle, and subtract.",
      L("plan", "Border = whole courtyard − inner rectangle")),
    B("The whole courtyard first. 12 times 8 is 96 square metres.",
      W("w", "12 × 8 = 96"), N("w", "96", "whole")),
    B("Now the inner rectangle. The border is 1 metre wide. How long is the inner rectangle?",
      ask=choose(["11 m", "10 m", "12 m"], 1,
                 "The border runs along both ends. It takes 1 metre off one end and 1 metre off the other, so the length loses 2 metres.")),
    B("12, take away 1, take away 1, is 10. In the same way the width is 8, take away 1, take away 1, which is 6.",
      W("l", "12 − 1 − 1 = 10"), W("b", "8 − 1 − 1 = 6")),
    B("So the inner rectangle is 10 by 6. Its area is 60 square metres.",
      W("i", "10 × 6 = 60"), N("i", "60", "inner")),
    B("The border is the difference. 96 minus 60 is 36 square metres.",
      ANS("a", "96 − 60 = 36"), M("a", "36", "circle")),
    B("Careful: 60 is one of the choices, but that is the middle, not the border. The question asks for the frame around it."),
    B("Another tempting shortcut is distance round times width: 40 times 1 is 40. But that counts each of the 4 corner squares twice. Take 4 off, and we get 36 again.",
      W("t1", "2 × (12 + 8) = 40"), W("t2", "40 − 4 = 36")),
    B("For the area of a border: outer rectangle, minus inner rectangle."),
)

LESSONS[P + "0866e5c1-1917-43cc-bc33-21d705a824bd"] = lesson(
    B("Vikram's courtyard is a square with an area of 625 square metres. A path 2 metres wide goes all round the outside. We want the area of the path alone.",
      GIVEN("q", "Square courtyard, area 625 sq. m"), L("q2", "Path 2 m wide all round, outside. Path area = ?"),
      FIG("f1", {"kind": "rectangle", "square": True, "length": "?", "breadth": "?", "inside": "625 sq. m"})),
    B("We need the side of the courtyard first. A square's area is side times side, and 20 times 20 is only 400. So which number, times itself, makes 625?",
      W("h", "20 × 20 = 400"),
      ask=choose(["312.5", "156.25", "25"], 2,
                 "Halving 625, or sharing it by 4, does not undo side times side. We need a number times itself, a bit bigger than 20.")),
    B("It is 25. Let's make sure: 25 times 20 is 500, and 25 times 5 is 125. Together, 625. So the courtyard is 25 metres on each side.",
      W("s1", "25 × 20 = 500"), W("s2", "25 × 5 = 125"), W("s", "25 × 25 = 500 + 125 = 625")),
    B("Now add the path, 2 metres wide, all the way round. How long is one side of the big outer square?",
      ask=choose(["27 m", "29 m", "33 m"], 1,
                 "The path sticks out 2 metres on one side, and 2 metres on the opposite side as well. So the side grows by 4 metres.")),
    B("25 plus 2 plus 2 is 29. The outer square, courtyard and path together, is 29 metres on each side.",
      W("o", "25 + 2 + 2 = 29")),
    B("Its area is 29 times 29. A quick way: 29 times 30 is 870, then take away one 29. That leaves 841 square metres.",
      W("o1", "29 × 30 = 870"), W("o2", "870 − 29 = 841"), W("o3", "29 × 29 = 841")),
    B("The path is the outer square with the courtyard taken out. 841 minus 625 is 216 square metres.",
      ANS("a", "841 − 625 = 216"), M("a", "216", "circle")),
    B("A tempting shortcut gives 200: the distance round the courtyard, 100 metres, times 2. But that misses the 4 corner squares of the path, each 2 by 2. They add 16, which makes 216.",
      W("t1", "4 × 25 = 100"), W("t2", "100 × 2 = 200"), W("t3", "4 × 2 × 2 = 16"), W("t4", "200 + 16 = 216")),
    B("For a path round the outside: outer area minus inner area. And the side grows by twice the width of the path."),
)

LESSONS[P + "75be410e-7a69-4662-b276-e87aeedcebac"] = lesson(
    B("Priya's courtyard is a square of side 20 metres. She leaves a border 2 metres wide all round, and fills the inside with coloured powder that costs 15 rupees for each square metre.",
      GIVEN("q", "Square courtyard of side 20 m, border 2 m wide"), L("q2", "Powder: ₹15 per sq. m. Cost = ?"),
      FIG("f1", {"kind": "rectangle", "square": True, "length": "20 m", "breadth": "20 m", "inside": "rangoli", "highlight": ["border"]})),
    B("The rangoli fills the inner square. The border is 2 metres wide. How long is one side of that inner square?",
      ask=choose(["18 m", "16 m", "12 m"], 1,
                 "The border runs down both edges. It takes 2 metres off one side and 2 metres off the opposite side, so 4 metres go.")),
    B("20, take away 2, take away 2, is 16. The inner square is 16 metres on each side.",
      W("l", "20 − 2 − 2 = 16")),
    B("Its area is side times side. 16 times 10 is 160, and 16 times 6 is 96. Together, 256 square metres.",
      W("a1", "16 × 10 = 160"), W("a2", "16 × 6 = 96"), W("a", "16 × 16 = 160 + 96 = 256")),
    B("Each square metre of powder costs 15 rupees. How do we find the cost of 256 square metres?",
      ask=choose(["256 + 15", "256 ÷ 15", "256 × 15"], 2,
                 "Every one of the 256 square metres costs 15 rupees. 256 lots of 15 is a multiplication.")),
    B("15 is 10 and 5. 256 times 10 is 2,560. 256 times 5 is half of that, 1,280. Together, 3,840 rupees.",
      W("m1", "256 × 10 = 2,560"), W("m2", "256 × 5 = 1,280"),
      ANS("m", "256 × 15 = 2,560 + 1,280 = 3,840"), M("m", "3,840", "circle")),
    B("Two traps. Pricing the whole courtyard, 400 square metres, gives 6,000. And taking the border off only one way gives 20 times 16, which is 320, and a cost of 4,800.",
      W("t1", "20 × 20 = 400"), W("t2", "400 × 15 = 6,000"), W("t3", "20 × 16 = 320"), W("t4", "320 × 15 = 4,800")),
    B("A border all round comes off twice from each side. Then find the area, then the cost."),
)


# ── Triangles ────────────────────────────────────────────────────────────────

def tri(shape, ab=None, bc=None, ca=None, **more):
    sides = {}
    if ab:
        sides["ab"] = ab
    if bc:
        sides["bc"] = bc
    if ca:
        sides["ca"] = ca
    spec = {"kind": "triangle", "shape": shape, "sides": sides}
    spec.update(more)
    return spec


HALF_RULE = "Area of triangle = 1/2 × base × height"
RIGHT_TEST = "Right angle test: short² + short² = longest²"

LESSONS[P + "dc9f4799-da0b-40fb-bf71-8fa122e085a4"] = lesson(
    B("Amit's bracket is an isosceles triangle. The two equal sides are 13 centimetres each, and the base is 10 centimetres. We want its perimeter.",
      GIVEN("q", "Isosceles triangle: equal sides 13 cm, base 10 cm"), L("q2", "Perimeter = ?"),
      FIG("f1", tri("isosceles", ab="13 cm", bc="10 cm", ca="?"))),
    B("First, what is a perimeter? It is the distance all the way round a shape. Imagine an ant walking along every side until it is back where it started.",
      L("r", "Perimeter = distance all the way round")),
    B("Isosceles means two of the sides are equal. So what are the three sides of this triangle?",
      ask=choose(["13, 10 and 10", "13, 13 and 10", "13 and 10 only"], 1,
                 "The question says the two equal sides are each 13 centimetres. So 13 appears twice, and the base, 10, appears once.")),
    B("13, 13 and 10. A triangle has 3 sides, so we add 3 numbers, even though the question only printed 2 different ones.",
      L("s", "Sides: 13 cm, 13 cm, 10 cm"), FIG("f2", tri("isosceles", ab="13 cm", bc="10 cm", ca="13 cm"))),
    B("13 plus 13 is 26. Then 26 plus 10 is 36.",
      W("a1", "13 + 13 = 26"), ANS("a", "13 + 13 + 10 = 36"), M("a", "36", "circle")),
    B("So the perimeter is 36 centimetres. That is the length of metal strip Amit needs."),
    B("Two slips to avoid. Stopping at 26 leaves out the base. And 13 plus 10 is only 23, which forgets that there are two sides of 13.",
      W("t", "13 + 10 = 23")),
    B("For any perimeter: list every side, count them, then add them all."),
)

LESSONS[P + "d3681d12-6a3c-4748-995f-cff90f89236e"] = lesson(
    B("Sanjay's kite is a triangle with sides of 15, 20 and 25 centimetres, and his friend says one angle is 90 degrees. Cloth costs 2 rupees for each square centimetre. What does the cloth cost?",
      GIVEN("q", "Triangle: sides 15 cm, 20 cm, 25 cm"), L("q2", "Cloth: ₹2 per sq. cm. Cost = ?"),
      FIG("f1", tri("right", ab="15 cm", bc="20 cm", ca="25 cm"))),
    B("Let's test what the friend said. In a right-angled triangle, the squares of the two shorter sides add up to the square of the longest side.",
      L("r", RIGHT_TEST)),
    B("15 times 15 is 225. 20 times 20 is 400. Add them: 625. And 25 times 25 is 625 as well. It matches, so the triangle really is right-angled.",
      W("s1", "15 × 15 = 225"), W("s2", "20 × 20 = 400"), W("s3", "225 + 400 = 625"), W("s4", "25 × 25 = 625")),
    B("The right angle sits between two of the sides. Those two are the base and the height. Which two are they?",
      ask=choose(["15 and 25", "20 and 25", "15 and 20"], 2,
                 "The longest side, 25, always lies opposite the right angle, on a slant. The two shorter sides, 15 and 20, are the ones that meet at the square corner.")),
    B("15 and 20. Now, a right-angled triangle is exactly half of a rectangle. So its area is half of base times height.",
      L("f", HALF_RULE), FIG("f2", tri("right", ab="15 cm", bc="20 cm", enclose=True))),
    B("15 times 20 is 300. Half of 300 is 150. So the kite needs 150 square centimetres of cloth.",
      W("a1", "15 × 20 = 300"), W("a2", "1/2 × 15 × 20 = 150"), N("a2", "150", "area")),
    B("Each square centimetre costs 2 rupees. 150 times 2 is 300 rupees.",
      ANS("a", "150 × 2 = 300"), M("a", "300", "circle")),
    B("Notice that 300 turned up twice: first as the area of the whole rectangle, then as the cost. The slips here are forgetting to halve, and using the slanted side, 25, as a height."),
    B("Right-angled triangle: half of the two short sides multiplied together. Then area times price."),
)

LESSONS[P + "a7c1fcb5-6bac-4ec8-9f7d-4924e5614bcd"] = lesson(
    B("Arjun's triangle has sides of 9, 12 and 15 centimetres. Meena doubles every side. By how much does the area go up?",
      GIVEN("q", "Triangle: sides 9 cm, 12 cm, 15 cm"), L("q2", "Every side doubled. Increase in area = ?"),
      FIG("f1", tri("right", ab="9 cm", bc="12 cm", ca="15 cm"))),
    B("First, what kind of triangle is it? Test for a right angle. 9 times 9 is 81, 12 times 12 is 144, and together they make 225. And 15 times 15 is 225 too.",
      W("s1", "9 × 9 = 81"), W("s2", "12 × 12 = 144"), W("s3", "81 + 144 = 225"), W("s4", "15 × 15 = 225")),
    B("They match, so it is a right-angled triangle. The two shorter sides, 9 and 12, meet at the right angle. They are the base and the height.",
      L("k", "Right-angled: base 9 cm, height 12 cm")),
    B("The area is half of base times height. 9 times 12 is 108, and half of 108 is 54 square centimetres.",
      L("f", HALF_RULE), W("a1", "9 × 12 = 108"), W("a2", "1/2 × 9 × 12 = 54"), N("a2", "54", "old area")),
    B("Now double every side. The new triangle is 18, 24 and 30. Its base is 18 and its height is 24.",
      L("d", "Doubled: 18 cm, 24 cm, 30 cm")),
    B("Before we work it out, have a guess. When every side is doubled, what happens to the area?",
      ask=choose(["it doubles", "it becomes 4 times as big", "it stays the same"], 1,
                 "It is natural to say it doubles. But the base doubles and the height doubles too, so the area is doubled twice. Let's work it out and see.")),
    B("18 times 20 is 360, and 18 times 4 is 72, so 18 times 24 is 432. Half of 432 is 216 square centimetres.",
      W("b1", "18 × 20 = 360"), W("b2", "18 × 4 = 72"), W("b3", "18 × 24 = 360 + 72 = 432"),
      W("b4", "1/2 × 18 × 24 = 216"), N("b4", "216", "new area")),
    B("216 is 4 times 54. But the question asks for the increase: 216 minus 54 is 162 square centimetres.",
      W("c", "4 × 54 = 216"), ANS("a", "216 − 54 = 162"), M("a", "162", "circle")),
    B("Three traps in the choices. 54 is the old area, 216 is the new area, and 108 comes from thinking the area only doubles. The increase is the gap between new and old."),
    B("Double every side and the area becomes 4 times as big. So the increase is 3 times the old area: 3 times 54 is 162.",
      W("e", "3 × 54 = 162")),
)

LESSONS[P + "9bea442a-3f4c-4461-bed6-7e37658a29ed"] = lesson(
    B("Ananya's garden is a triangle. The distance round it is 72 metres, and its sides are in the ratio 3 to 4 to 5. We want its area.",
      GIVEN("q", "Triangle: perimeter 72 m, sides in ratio 3 : 4 : 5"), L("q2", "Area = ?"),
      FIG("f1", {"kind": "barModel", "bars": [{"segments": [
          {"units": 3, "label": "3 parts", "tone": "a"}, {"units": 4, "label": "4 parts", "tone": "b"},
          {"units": 5, "label": "5 parts", "tone": "c"}], "brace": "72 m"}]})),
    B("A ratio is about equal parts. The sides are 3 parts, 4 parts and 5 parts. How many parts make up the whole 72 metres?",
      ask=choose(["5", "12", "60"], 1,
                 "The 72 metres is all three sides put together. So we add the parts: 3 and 4 and 5.")),
    B("3 plus 4 plus 5 is 12 parts. So 1 part is 72 divided by 12, which is 6 metres.",
      W("p1", "3 + 4 + 5 = 12"), W("p2", "72 ÷ 12 = 6")),
    B("Now the sides. 3 parts is 18 metres, 4 parts is 24 metres, and 5 parts is 30 metres.",
      W("s1", "3 × 6 = 18"), W("s2", "4 × 6 = 24"), W("s3", "5 × 6 = 30")),
    B("The question hints that this triangle is special. Test it: 18 times 18 is 324, and 24 times 24 is 576. Together, 900. And 30 times 30 is 900 as well.",
      W("t1", "18 × 18 = 324"), W("t2", "24 × 24 = 576"), W("t3", "324 + 576 = 900"), W("t4", "30 × 30 = 900")),
    B("When the squares of the two shorter sides add up to the square of the longest side, the triangle has a right angle. So 18 and 24 meet at a square corner: they are the base and the height.",
      FIG("f2", tri("right", ab="18 m", bc="24 m", ca="30 m"))),
    B("So which sum gives the area of this right-angled triangle?",
      ask=choose(["18 × 24", "1/2 × 18 × 24", "1/2 × 24 × 30"], 1,
                 "A right-angled triangle is half of a rectangle, so we must halve. And we use the two sides that meet at the right angle, 18 and 24, not the slanted side.")),
    B("18 times 20 is 360, and 18 times 4 is 72, so 18 times 24 is 432. Half of 432 is 216 square metres.",
      W("a1", "18 × 20 = 360"), W("a2", "18 × 4 = 72"), W("a3", "18 × 24 = 360 + 72 = 432"),
      ANS("a", "1/2 × 18 × 24 = 216"), M("a", "216", "circle")),
    B("A quick check on the sides: 18 plus 24 plus 30 is 72, the perimeter we were given.",
      W("c", "18 + 24 + 30 = 72")),
    B("So: share the perimeter by the ratio to get the sides, spot the right angle, then take half of base times height. The answer is 216 square metres."),
)

LESSONS[P + "de0dda2b-c85c-4299-b764-ecbb5250cc4e"] = lesson(
    B("Ananya's courtyard is a square of side 20 metres. Inside it she paints a triangle: its base is one whole side of the square, and its tip touches the opposite side.",
      GIVEN("q", "Square of side 20 m, triangle inside (base 20 m)"), L("q2", "Gold paint for the rest: ₹12 per sq. m. Cost = ?"),
      FIG("f1", tri("isosceles", bc="20 m", enclose=True))),
    B("The rest of the square is painted gold, at 12 rupees for each square metre. So we need the gold area. Start with the square: 20 times 20 is 400 square metres.",
      W("w", "20 × 20 = 400"), N("w", "400", "square")),
    B("Now the triangle. Its base is 20 metres, and its tip touches the opposite side of the square. So how tall is it?",
      ask=choose(["10 m", "20 m", "40 m"], 1,
                 "The triangle reaches from one side of the square right across to the opposite side. That distance is the side of the square.")),
    B("Base 20, height 20. A triangle's area is half of base times height. Half of 400 is 200 square metres.",
      L("f", HALF_RULE), W("t", "1/2 × 20 × 20 = 200"), N("t", "200", "triangle")),
    B("Look at the picture. The triangle takes up exactly half of the square. So the gold part is the other half: 400 minus 200 is 200 square metres.",
      W("g", "400 − 200 = 200"), N("g", "200", "gold", nth=2)),
    B("Gold paint costs 12 rupees for each square metre. 2 times 12 is 24, so 200 times 12 is 2,400 rupees.",
      W("m1", "2 × 12 = 24"), ANS("m", "200 × 12 = 2,400"), M("m", "2,400", "circle")),
    B("The trap: 4,800 is the price of painting the whole square gold. The triangle is not gold, so only half of that is needed.",
      W("x", "400 × 12 = 4,800")),
    B("A triangle with its base on one side of a rectangle and its tip on the opposite side is always half of the rectangle."),
)

LESSONS[P + "8d2c4e7b-464a-42a0-8cc2-4e0777b7436e"] = lesson(
    B("Ananya's courtyard is 18 metres long and 12 metres wide. A diagonal cuts it into two equal triangles, and she paints one. Then a square flower bed of side 4 metres goes inside the painted triangle.",
      GIVEN("q", "Courtyard 18 m × 12 m, cut by a diagonal"), L("q2", "One triangle painted, with a square bed of side 4 m"),
      L("q3", "Painted area not covered = ?"),
      FIG("f1", {"kind": "polygon", "points": [[0, 0], [12, 0], [12, 8], [0, 8]],
                 "edges": ["18 m", "12 m", None, None], "dashed": [{"from": 0, "to": 2}]})),
    B("Start with the whole courtyard. Length times breadth: 18 times 10 is 180, and 18 times 2 is 36. Together, 216 square metres.",
      W("w1", "18 × 10 = 180"), W("w2", "18 × 2 = 36"), W("w", "18 × 12 = 180 + 36 = 216")),
    B("The diagonal cuts the rectangle into two equal triangles. So how do we find the area of one triangle?",
      ask=choose(["216 × 2", "216 ÷ 2", "it is still 216"], 1,
                 "Two equal triangles share the rectangle between them. So each one gets half of the 216.")),
    B("Half of 216 is 108. The painted triangle is 108 square metres.",
      W("h", "216 ÷ 2 = 108"), N("h", "108", "painted triangle")),
    B("Now the flower bed. It is a square of side 4, so its area is 4 times 4, which is 16 square metres.",
      W("p", "4 × 4 = 16"), N("p", "16", "flower bed")),
    B("The bed covers up 16 of the painted square metres. Take it away: 108 minus 16 is 92 square metres.",
      ANS("a", "108 − 16 = 92"), M("a", "92", "circle")),
    B("Check by adding back. 92 plus 16 is 108, the whole painted triangle.",
      W("c", "92 + 16 = 108")),
    B("Two slips. 108 is the triangle before the flower bed goes in. And 200 comes from taking the bed away from the whole courtyard, forgetting that only half was painted.",
      W("t", "216 − 16 = 200")),
    B("Go in the order of the story: the whole rectangle, half of it, then take away the piece on top."),
)


# ── Longer one-offs ──────────────────────────────────────────────────────────

LESSONS[P + "56d7bc6f-d4dc-404a-8a5e-69af0e71f3f7"] = lesson(
    B("Arjun has 120 metres of rope to go round a rectangular cover. The length is twice the breadth. Then a square hole of side 5 metres is cut in the middle. We want the area that is left.",
      GIVEN("q", "Rectangle: perimeter 120 m, length = 2 × breadth"), L("q2", "Square hole of side 5 m. Area left = ?")),
    B("We don't know the sides yet, so think in parts. Call the breadth 1 part. Then the length, which is twice as long, is 2 parts.",
      L("k", "breadth = 1 part, length = 2 parts"),
      FIG("f1", {"kind": "barModel", "bars": [
          {"label": "breadth", "segments": [{"units": 1, "label": "1 part", "tone": "a"}]},
          {"label": "length", "segments": [{"units": 1, "label": "1 part", "tone": "a"}, {"units": 1, "label": "1 part", "tone": "a"}]}]})),
    B("The rope goes all the way round: a length, a breadth, another length, another breadth. How many parts is that altogether?",
      ask=choose(["3 parts", "4 parts", "6 parts"], 2,
                 "Going round a rectangle, we pass 2 lengths and 2 breadths. That is 2 parts, and 1, and 2, and 1.")),
    B("2 plus 1 plus 2 plus 1 is 6 parts. Those 6 parts use all 120 metres of rope, so 1 part is 120 divided by 6, which is 20 metres.",
      W("p1", "2 + 1 + 2 + 1 = 6"), W("p2", "120 ÷ 6 = 20")),
    B("So the breadth is 20 metres, and the length is twice that, 40 metres. Check the rope: 40 plus 20 plus 40 plus 20 is 120.",
      W("s1", "2 × 20 = 40"), W("s2", "40 + 20 + 40 + 20 = 120"), FIG("f2", rect("40 m", "20 m", "hole: side 5 m"))),
    B("Now the area of the whole cover. 40 times 20 is 800 square metres.",
      W("w", "40 × 20 = 800"), N("w", "800", "cover")),
    side_ask(5, "hole", "metres"),
    B("5 times 5 is 25. Take the hole out of the cover: 800 minus 25 is 775 square metres.",
      W("h", "5 × 5 = 25"), ANS("a", "800 − 25 = 775"), M("a", "775", "circle")),
    B("The big trap is sharing the 120 metres by 3, as if the rope were just 1 length and 1 breadth. That gives a breadth of 40, and a cover far too big. A perimeter has 2 of each.",
      W("t", "120 ÷ 3 = 40")),
    B("So: use the perimeter to find the sides, then the area, then take away the hole."),
)

LESSONS[P + "bec57c6e-45cf-48f7-aa15-399cd29d76bf"] = lesson(
    B("Vikram is painting a wall, 10 metres long and 4 metres high. It has two square windows, each of side 1.5 metres, and a door 2 metres wide and 3 metres tall. He paints only the wall itself.",
      GIVEN("q", "Wall 10 m × 4 m"), L("q2", "2 square windows of side 1.5 m, door 2 m × 3 m"), L("q3", "Area to paint = ?"),
      FIG("f1", rect("10 m", "4 m", "2 windows, 1 door"))),
    B("The plan: find the whole wall, then take away every opening that gets no paint. How many openings are there?",
      ask=choose(["1", "2", "3"], 2,
                 "Count them: a window, another window, and a door. Each one is a piece of wall that gets no paint.")),
    B("The whole wall first. 10 times 4 is 40 square metres.",
      W("w", "10 × 4 = 40"), N("w", "40", "wall")),
    B("One window is a square of side 1.5. 1 times 1.5 is 1.5, and half of 1.5 is 0.75. Together, 2.25 square metres.",
      W("p1", "1 × 1.5 = 1.5"), W("p2", "0.5 × 1.5 = 0.75"), W("p", "1.5 × 1.5 = 1.5 + 0.75 = 2.25")),
    B("That was 1 window, and there are 2 of them. What area do the two windows cover together?",
      ask=choose(["2.25", "3", "4.5"], 2,
                 "Each window covers 2.25 square metres, and there are 2 of them. So we need 2 lots of 2.25.")),
    B("2 times 2.25 is 4.5 square metres. Now the door: 2 times 3 is 6 square metres.",
      W("v", "2 × 2.25 = 4.5"), N("v", "4.5", "both windows"), W("d", "2 × 3 = 6"), N("d", "6", "door")),
    B("Altogether, the openings take 4.5 plus 6, which is 10.5 square metres.",
      W("o", "4.5 + 6 = 10.5")),
    B("So the paint goes on 40 minus 10.5. 40 minus 10 is 30, and another 0.5 off leaves 29.5 square metres.",
      W("r1", "40 − 10 = 30"), W("r2", "30 − 0.5 = 29.5"), ANS("a", "40 − 10.5 = 29.5"), M("a", "29.5", "circle")),
    B("The easy slip is to take away only 1 window, when the question says two. Another is to forget the door, which leaves 35.5.",
      W("t", "40 − 4.5 = 35.5")),
    B("List every opening, find each area, add them up, and take the total from the wall."),
)
