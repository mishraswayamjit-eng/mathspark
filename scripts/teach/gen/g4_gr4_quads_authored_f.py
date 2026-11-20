"""Lessons written one by one: Grade 4 quadrilaterals, Q_CH20_013 to 025."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_quads")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["Q_CH20_013"] = lesson([
    B("Four shapes: a square, an equilateral triangle, a rectangle and a rhombus. Which one has the least perimeter?",
      G("Which has the LEAST perimeter?"), F("Q_CH20_013")),
    B("We can't tell by looking, so we work out all four. The square has 4 sides of 5.5 centimetres. 4 times 5.5 is 22.",
      L("s1", "Square, side 5.5 cm"), W("l1", "4 × 5.5 = 22")),
    B("The equilateral triangle has 3 sides of 6 centimetres. 3 times 6 is 18.",
      L("s2", "Equilateral triangle, side 6 cm"), W("l2", "3 × 6 = 18")),
    B("The rectangle is 5 centimetres by 3 centimetres. 5 plus 3 is 8, and double is 16.",
      L("s3", "Rectangle, 5 cm by 3 cm"), W("l3", "2 × (5 + 3) = 16")),
    B("Last, the rhombus, with a side of 5 centimetres. How many equal sides does a rhombus have?",
      L("s4", "Rhombus, side 5 cm"),
      ask=choose(["2", "3", "4"], 2, "A rhombus is like a square that has been pushed over. All 4 of its sides are equal.")),
    B("4 equal sides. 4 times 5 is 20.", W("l4", "4 × 5 = 20")),
    B("Now compare: 22, 18, 16 and 20. The smallest is 16.", ring("l3", "16")),
    B("So the least perimeter belongs to the rectangle, 5 centimetres by 3 centimetres.",
      A("a", "Least: the rectangle, 5 cm by 3 cm", label=True), ring("a", "the rectangle")),
    B("The triangle has the fewest sides, but that didn't make it the smallest. Work each one out before you compare."),
])

LESSONS["Q_CH20_014"] = lesson([
    B("An equilateral triangle has the same perimeter as a square of side 6 centimetres. What is the side of the triangle?",
      G("Triangle's perimeter = perimeter of a square of side 6 cm"), GQ("q2", "Side of the triangle = ?"),
      F("Q_CH20_014")),
    B("Start with the shape we know. The square has 4 sides of 6 centimetres. 4 times 6 is 24.",
      W("l1", "4 × 6 = 24"), note("l1", "24", "perimeter", "below")),
    B("The triangle has the same perimeter, 24 centimetres. An equilateral triangle has 3 equal sides. So how do we find one side?",
      ask=choose(["24 ÷ 3", "24 ÷ 4", "3 × 6"], 0,
                 "The triangle shares its 24 centimetres equally among 3 sides. So we divide 24 by 3.")),
    B("24 divided by 3 is 8.", W("l2", "24 ÷ 3 = 8")),
    B("Each side of the triangle is 8 centimetres.", A("a", "Side of triangle = 8 cm", label=True), ring("a", "8")),
    B("Notice that 8 is more than 6. The triangle has fewer sides to share the same perimeter, so each side is longer."),
    B("Check: 3 sides of 8 make 24, the same as the square.", W("c", "3 × 8 = 24")),
])

LESSONS["Q_CH20_015"] = lesson([
    B("A square has the same area as a rectangle 16 centimetres long and 4 centimetres broad. We want the perimeter of the square.",
      G("Area of square = area of a rectangle 16 cm by 4 cm"), GQ("q2", "Perimeter of the square = ?"),
      F("Q_CH20_015")),
    B("Three steps here: the rectangle's area, then the square's side, then the square's perimeter. First, 16 times 4 is 64.",
      W("l1", "16 × 4 = 64"), note("l1", "64", "area", "below")),
    B("The square's area is also 64. Area is side times side. Which number times itself makes 64?",
      ask=choose(["16", "8", "32"], 1, "Try the times tables. 8 times 8 is 64. Halving 64 or dividing it by 4 does not give the side.")),
    B("8 times 8 is 64. So the side of the square is 8 centimetres.", W("l2", "8 × 8 = 64")),
    B("Don't stop here! 8 is the side, but the question asks for the perimeter.", box("q2", "Perimeter")),
    B("A square has 4 equal sides. 4 times 8 is 32.", W("l3", "4 × 8 = 32")),
    B("The perimeter of the square is 32 centimetres.", A("a", "Perimeter of square = 32 cm", label=True), ring("a", "32")),
    B("Same area links the two shapes. From the area we find the side, and from the side we find the perimeter."),
])

LESSONS["Q_CH20_016"] = lesson([
    B("A square has the same perimeter as a rectangle 16 centimetres long and 4 centimetres broad. We want the area of the square.",
      G("Perimeter of square = perimeter of a rectangle 16 cm by 4 cm"), GQ("q2", "Area of the square = ?"),
      F("Q_CH20_016")),
    B("First the rectangle's perimeter. 16 plus 4 is 20. That is halfway round, so double it: 40.",
      W("l1", "16 + 4 = 20"), W("l2", "2 × 20 = 40")),
    B("The square's perimeter is also 40 centimetres. How long is each side of the square?",
      ask=choose(["20 cm", "16 cm", "10 cm"], 2,
                 "A square has 4 equal sides. Share the 40 centimetres among all 4 of them.")),
    B("40 divided by 4 is 10. The side of the square is 10 centimetres.", W("l3", "40 ÷ 4 = 10")),
    B("Now the area: side times side. 10 times 10 is 100.", W("l4", "10 × 10 = 100")),
    B("The area of the square is 100 square centimetres.", A("a", "Area of square = 100 sq. cm", label=True), ring("a", "100")),
    B("Here's something neat. The rectangle's area is 16 times 4, only 64. Same perimeter, but the square holds more.",
      W("l5", "16 × 4 = 64")),
    B("Same perimeter links the two shapes. From the perimeter we find the side, then side times side gives 100."),
])

LESSONS["Q_CH20_017"] = lesson([
    B("In a parallelogram, what is true about the opposite sides?",
      G("In a parallelogram, opposite sides are: ?"), F("Q_CH20_017")),
    B("Listen to the name: parallelogram. Which word can you hear hiding inside it?",
      ask=choose(["parallel", "pentagon", "perimeter"], 0, "Say it slowly: parallel, o, gram. The name begins with the word parallel.")),
    B("Parallel! Opposite sides run in the same direction, like railway tracks, and never meet.",
      L("l1", "opposite sides: parallel"), mark("l1", "parallel")),
    B("Now look at their lengths. In the picture, compare the top side with the bottom side, and the left side with the right side.",
      F("Q_CH20_017", 1)),
    B("Each side is exactly as long as the side facing it. So opposite sides are equal as well.",
      L("l2", "opposite sides: equal"), mark("l2", "equal")),
    B("So in a parallelogram, opposite sides are parallel and equal.",
      A("a", "parallel and equal", label=True), ring("a", "parallel and equal")),
    B("Two facts, and both are true. Don't settle for a choice that gets only one of them right."),
])

LESSONS["Q_CH20_018"] = lesson([
    B("A rhombus has axes of symmetry. Which lines are they?",
      G("In a rhombus, the axes of symmetry are: ?"), F("Q_CH20_018")),
    B("An axis of symmetry is a fold line. Fold along it, and one half lands exactly on the other.",
      L("l1", "Axis of symmetry = a fold line that matches")),
    B("So an axis has to be a line we can fold along. Could an angle be an axis of symmetry?",
      ask=choose(["Yes", "No, an angle is not a line"], 1, "An angle is a corner, the turn between two sides. We can only fold along a line.")),
    B("Right, angles are out. Now try folding along a side. Nothing lands on anything, so the sides are out too.",
      L("l2", "angles: no.  sides: no.")),
    B("Now fold the rhombus corner to corner, along a diagonal. All four sides are equal, so the two halves match exactly.",
      L("l3", "fold along a diagonal: yes"), F("Q_CH20_018", 0)),
    B("The other diagonal works in the same way. So a rhombus has 2 axes of symmetry, and they are its diagonals.",
      A("a", "The axes are the diagonals", label=True), ring("a", "the diagonals"), F("Q_CH20_018", 1)),
    B("Remember the paper test: if you can fold along the line and the halves match, it is an axis of symmetry."),
])

LESSONS["Q_CH20_019"] = lesson([
    B("Four statements about shapes. Only one is true. Let's test each one.",
      G("Which statement is TRUE?"), F("Q_CH20_019")),
    B("Every rhombus is a square? A rhombus has four equal sides, but it can lean over like a diamond. Then it has no right angles. Not true.",
      L("s1", "Every rhombus is a square?"), strike("s1", "square", "it can lean")),
    B("Every parallelogram is a rectangle? A parallelogram can lean over too. A rectangle needs four right angles. Not true.",
      L("s2", "Every parallelogram is a rectangle?"), strike("s2", "rectangle", "it can lean")),
    B("Every rectangle is a square? Think of a door. It is a rectangle, but are its four sides equal?",
      L("s3", "Every rectangle is a square?"),
      ask=choose(["Yes, all equal", "No, it is longer than it is wide"], 1,
                 "A door is much taller than it is wide. A square needs all four sides to be the same length.")),
    B("A long rectangle is not a square. So that one is not true either.", strike("s3", "square", "a door!")),
    B("Every square is a rectangle? A rectangle only needs four right angles. Does every square have four right angles? Yes, always!",
      L("s4", "Every square is a rectangle?")),
    B("So the true statement is: every square is a rectangle. A square is a special rectangle, one with equal sides.",
      A("a", "Every square is a rectangle: TRUE", label=True), ring("a", "TRUE")),
    B("The trick with the word every: hunt for one shape that breaks the rule. If you find one, the statement is not true."),
])

LESSONS["Q_CH20_020"] = lesson([
    B("A quadrilateral has exactly one pair of parallel sides. What is it called?",
      G("Exactly one pair of parallel sides. It is called a: ?"), F("Q_CH20_020")),
    B("Parallel sides run in the same direction and never meet, like railway tracks. Let's count the parallel pairs in each shape.",
      box("q", "one pair")),
    B("A parallelogram has two pairs: top with bottom, and left with right. A rhombus has two pairs as well.",
      L("l1", "parallelogram: 2 pairs"), L("l2", "rhombus: 2 pairs")),
    B("What about a kite? Its equal sides sit next to each other. Does a kite usually have any parallel sides?",
      ask=choose(["No, none", "Yes, one pair", "Yes, two pairs"], 0,
                 "Picture a kite in the sky. Its sides all slant in different directions, so none of them are parallel.")),
    B("A kite usually has no parallel sides at all.", L("l3", "kite: 0 pairs")),
    B("That leaves the trapezium. Its top and bottom are parallel, but its other two sides are not. Exactly one pair!",
      L("l4", "trapezium: 1 pair"), ring("l4", "1 pair")),
    B("So the shape is a trapezium.", A("a", "A trapezium", label=True), ring("a", "trapezium")),
    B("The word exactly matters. Two pairs is too many. We want one pair and no more."),
])

LESSONS["Q_CH20_021"] = lesson([
    B("Here is a kite. How many axes of symmetry does it have?",
      G("A kite has how many axes of symmetry?"), F("Q_CH20_021")),
    B("A kite has two short sides that meet at one end, and two long sides that meet at the other end.",
      F("Q_CH20_021", 0)),
    B("An axis of symmetry is a fold line where the two halves match. Fold the kite along its length, from one end corner to the other.",
      L("l1", "fold end to end"), F("Q_CH20_021", 1)),
    B("One half lands exactly on the other. Short side on short side, long side on long side. That is 1 axis.",
      note("l1", "end to end", "matches", "below")),
    B("Now fold it the other way, across the middle, joining the two side corners. Do the halves match?",
      ask=choose(["Yes", "No, short lands on long"], 1,
                 "One part has the two short sides and the other part has the two long sides. When you fold, a short side lands on a long side.")),
    B("A short side would land on a long side. So that fold does not match.",
      L("l2", "fold across the middle"), strike("l2", "across the middle", "no match"), F("Q_CH20_021", 2)),
    B("A kite has just 1 axis of symmetry.", A("a", "1 axis of symmetry", label=True), ring("a", "1"), F("Q_CH20_021", 3)),
    B("A rhombus has 2 and a square has 4. The kite, with its two different pairs of sides, has only the one."),
])

LESSONS["Q_CH20_022"] = lesson([
    B("Three angles of a quadrilateral are 90 degrees, 85 degrees and 110 degrees. What is the fourth angle?",
      G("Quadrilateral: angles 90°, 85°, 110° and ?"), F("Q_CH20_022")),
    B("The key fact: the four angles of a quadrilateral always add up to 360 degrees.",
      L("l1", "4 angles add up to 360°"), box("l1", "360°")),
    B("Add the three we know. 90 plus 85 is 175. Then 175 plus 110 is 285.",
      W("l2", "90 + 85 = 175"), W("l3", "175 + 110 = 285")),
    B("Three angles use up 285 of the 360 degrees. What do we do to find the fourth?",
      ask=choose(["360 − 285", "285 − 110", "360 + 285"], 0,
                 "The fourth angle is whatever is left of the 360 after the other three. To find what is left, we subtract.")),
    B("360 minus 285. From 285 up to 300 is 15, and from 300 up to 360 is 60. 15 and 60 make 75.",
      W("l4", "285 + 15 = 300"), W("l5", "300 + 60 = 360"), W("l6", "360 − 285 = 75")),
    B("The fourth angle is 75 degrees.", A("a", "Fourth angle = 75°", label=True), ring("a", "75°")),
    B("Check: 90, 85, 110 and 75 add up to 360.", W("c", "90 + 85 + 110 + 75 = 360")),
    B("Add the three you know, then take the total from 360. And add carefully: most slips happen in the adding."),
])

LESSONS["Q_CH20_023"] = lesson([
    B("The area of a square is 144 square centimetres. What is its side?",
      G("Square: area = 144 cm². Side = ?"), F("Q_CH20_023")),
    B("Area of a square is side times side. So we need a number that, multiplied by itself, gives 144.",
      L("l1", "side × side = 144")),
    B("Careful: this is not 144 divided by 4. Dividing by 4 is for a perimeter. Here we hunt for a number times itself.",
      box("l1", "side × side")),
    B("Start with an easy one. 10 times 10 is 100. Is the side bigger or smaller than 10?",
      W("l2", "10 × 10 = 100"),
      ask=choose(["bigger than 10", "smaller than 10"], 0, "100 is less than 144. We need more area, so we need a longer side.")),
    B("Bigger. Try 11: 11 times 11 is 121. Still too small.", W("l3", "11 × 11 = 121")),
    B("Try 12: 12 times 12 is 144. That's it!", W("l4", "12 × 12 = 144"), ring("l4", "144")),
    B("The side of the square is 12 centimetres.", A("a", "Side = 12 cm", label=True), ring("a", "12")),
    B("To go from area back to the side, ask: which number times itself gives the area? Try, check, and adjust."),
])

LESSONS["Q_CH20_024"] = lesson([
    B("A rectangle has an area of 96 square centimetres and a length of 12 centimetres. What is its breadth?",
      G("Rectangle: area = 96 cm², length = 12 cm. Breadth = ?"), F("Q_CH20_024")),
    B("Length times breadth gives the area. So 12 times the breadth is 96.", W("l1", "12 × ? = 96")),
    B("We know the answer to a multiplication and one of its numbers. How do we find the missing number?",
      ask=choose(["96 − 12", "96 × 12", "96 ÷ 12"], 2,
                 "Multiplying made the 96. To go backwards from a multiplication, we divide.")),
    B("Divide the area by the length: 96 divided by 12. Think: 12 times 8 is 96.", W("l2", "96 ÷ 12 = 8")),
    B("The breadth is 8 centimetres.", A("a", "Breadth = 8 cm", label=True), ring("a", "8")),
    B("Check: 12 times 8 is 96. That is the area we were given.", W("c", "12 × 8 = 96")),
    B("A breadth of 8 makes sense: it must be a small number, because 12 lots of it make only 96."),
])

LESSONS["Q_CH20_025"] = lesson([
    B("What is true about the two diagonals of a square?",
      G("The diagonals of a square: ?"), F("Q_CH20_025")),
    B("A diagonal joins opposite corners. A square has two of them, and they cross in the middle. We'll check three things.",
      L("l0", "Equal?  Cut in half?  Right angles?")),
    B("First: are they the same length? A square looks the same when you turn it. So one diagonal can't be longer than the other.",
      L("l1", "equal: yes"), F("Q_CH20_025", 0)),
    B("Second: bisect means cut exactly in half. The diagonals cross at the centre of the square. Does each one cut the other in half?",
      ask=choose(["Yes, at the centre", "No, off to one side"], 0,
                 "The crossing point is the very middle of the square. So it is the middle of each diagonal too.")),
    B("Yes. Each diagonal cuts the other exactly in half. They bisect each other.", L("l2", "bisect each other: yes")),
    B("Third: look at the corner where they cross. It is a square corner, a right angle.",
      L("l3", "cross at right angles: yes"), F("Q_CH20_025", 1)),
    B("So the diagonals of a square are equal, and they bisect each other at right angles.",
      A("a", "Equal, and bisect at right angles", label=True), ring("a", "Equal")),
    B("A square gets the best of both: equal diagonals like a rectangle, and a right angle crossing like a rhombus."),
])
