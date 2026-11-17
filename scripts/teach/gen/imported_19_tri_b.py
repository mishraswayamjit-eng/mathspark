"""Triangles: naming by sides and angles, whether three lengths make a triangle, and mixed questions.

Left out on purpose: AIGEN_grade5_73792540-78bd-487a-bb05-2b0a029cf253 (its story contradicts itself).
"""
from imported_19_lib import ANS, ANSR, B, BOTH, DIV, FIG, G, L, M, N, S, TRI, W, GIVEN, choose, lesson

LESSONS = {}
A = "AIGEN_grade5_"

RULE = "Angles of a triangle add up to 180°"
SIDE_RULE = "Rule: two shorter sides together > longest side"
BY_SIDES = "By sides: equilateral, isosceles or scalene"
BY_ANGLES = "By angles: acute, right or obtuse"
SQUARE_TEST = "Right angle test: short² + short² = long²"

# ── Riya's napkin: 6, 8, 10 with a right angle ───────────────────────────────

LESSONS[A + "60493d60-649c-475b-b092-ef43922e580c"] = lesson(
    B("Riya's napkin is a triangle with sides of 6, 8 and 10 centimetres, and one of its angles is exactly 90 degrees. We must name it by its sides and by its angles.",
      GIVEN("q", "Sides 6 cm, 8 cm, 10 cm. One angle is 90°."),
      FIG("f1", TRI("right", None, {"ab": "6 cm", "bc": "8 cm", "ca": "10 cm"}))),
    B("A triangle can carry two names. One comes from comparing its sides. The other comes from looking at its angles. So we do two separate tests.",
      L("t1", BY_SIDES), L("t2", BY_ANGLES)),
    B("Sides first: 6, 8 and 10. How many of them are equal?",
      ask=choose(["all three", "two", "none"], 2,
                 "Compare them in pairs: 6 with 8, 8 with 10, and 6 with 10. Do any two match?")),
    B("None. When no two sides are equal, the triangle is scalene.",
      L("s1", "6, 8, 10: no two equal → scalene"), M("s1", "scalene", "box")),
    B("Now the angles. One angle is exactly 90 degrees. What do we call a triangle with a 90 degree angle?",
      ask=choose(["acute-angled", "right-angled", "obtuse-angled"], 1,
                 "Acute is for a triangle with every angle under 90, and obtuse needs one over 90. Exactly 90, a square corner, has its own name.")),
    B("Right angled. A 90 degree angle is a right angle.",
      L("s2", "One angle of 90°: right-angled"), M("s2", "right-angled", "box")),
    B("Put the two names together: scalene and right angled.",
      ANSR("a", "Scalene and right-angled", "Scalene and right-angled", True)),
    B("Could the other two angles change the name? No. All three add up to 180, so the other two share just 90 between them. Each one is smaller than 90.",
      W("c", "180 − 90 = 90")),
    B("One choice says equilateral and right angled. That can never happen: the angles of an equilateral triangle are all 60 degrees.",
      W("c2", "180 ÷ 3 = 60")),
    B("So: compare the sides with each other for one name, and the angles with 90 degrees for the other."),
)

# ── Meera's cut-out: 5, 5, 8 with a 110° angle ───────────────────────────────

LESSONS[A + "7f275cb5-83e1-4b41-94ae-298adaf3098e"] = lesson(
    B("Meera's triangle has sides of 5, 5 and 8 centimetres, and one of its angles is 110 degrees. We must name it by its sides and by its angles.",
      GIVEN("q", "Sides 5 cm, 5 cm, 8 cm. One angle is 110°."),
      FIG("f1", TRI("isosceles", {"a": "110°"}, {"ab": "5 cm", "ca": "5 cm", "bc": "8 cm"}))),
    B("Two names, so two separate tests. One for the sides, and one for the angles.",
      L("t1", BY_SIDES), L("t2", BY_ANGLES)),
    B("Sides first: 5, 5 and 8. How many of them are equal?",
      ask=choose(["none", "exactly two", "all three"], 1,
                 "Look at the three lengths: 5, 5 and 8. Two of them match, and the third does not.")),
    B("Exactly two. That makes it isosceles. Equilateral would need all three sides equal, and the 8 spoils that.",
      L("s1", "5, 5, 8: two equal → isosceles"), M("s1", "isosceles", "box")),
    B("Now the angle of 110 degrees. A right angle is 90 degrees. What do we call an angle that is bigger than a right angle?",
      L("s0", "Right angle = 90°"),
      ask=choose(["acute", "obtuse", "right"], 1,
                 "Acute angles are smaller than 90 degrees. 110 is bigger than 90, so it needs the other name.")),
    B("Obtuse. And one obtuse angle makes the whole triangle an obtuse triangle.",
      W("w1", "110 > 90"), L("s2", "One angle more than 90°: obtuse"), M("s2", "obtuse", "box")),
    B("Put the two names together: isosceles and obtuse.",
      ANSR("a", "Isosceles and Obtuse", "Isosceles and Obtuse", True)),
    B("We only know one angle. Does that matter? No. The three angles add up to 180, so once 110 is used, the other two share only 70. Neither can be big.",
      L("r", RULE), W("c", "180 − 110 = 70")),
    B("So: compare the sides with each other for one name, and the biggest angle with 90 degrees for the other."),
)

# ── Ankit's garden bed: 6, 6, 10 ─────────────────────────────────────────────

LESSONS[A + "8b6664e9-c712-46b8-9b03-162ddfa6dd61"] = lesson(
    B("A garden bed is to be a triangle with sides of 6, 6 and 10 metres. Two questions: what kind of triangle is it, and can it really be built?",
      GIVEN("q", "Sides 6 m, 6 m, 10 m. What kind? Can it exist?")),
    B("The kind first. Look at the sides: 6, 6 and 10. What do we call this triangle?",
      ask=choose(["equilateral", "scalene", "isosceles"], 2,
                 "Equilateral needs all three sides equal, and scalene means no two match. Here exactly two sides are 6 metres.")),
    B("Isosceles: exactly two equal sides.",
      L("s1", "6, 6, 10: two equal → isosceles"), M("s1", "isosceles", "box")),
    B("Now, can it exist? Not every set of three lengths makes a triangle. Picture the 10 metre side on the ground, with a 6 metre side hinged at each end. They must be long enough to meet.",
      L("r", SIDE_RULE)),
    B("So we add the two shorter sides. 6 plus 6 is 12. Is that more than the longest side, 10?",
      W("w1", "6 + 6 = 12"),
      ask=choose(["No, 12 is too short", "Yes, 12 is more than 10"], 1,
                 "Compare 12 with the longest side, which is 10. The two shorter sides need to add up to more than it.")),
    B("Yes. 12 is more than 10, so the two sides meet with room to spare. The triangle can exist.",
      W("w2", "12 > 10")),
    B("The other pairs are safe too: 6 plus 10 is 16, far more than 6. Any pair that includes the longest side always passes. That is why we only test the two shorter ones.",
      W("w3", "6 + 10 = 16")),
    B("So it is an isosceles triangle, and it can exist.",
      ANSR("a", "Isosceles, and it CAN exist", "CAN exist", True)),
    B("Two jobs: count the equal sides for the name. Then add the two shorter sides and compare with the longest."),
)

# ── Deepa's rangoli: 8, 15, 6 will not close ─────────────────────────────────

LESSONS[A + "6cb0fd51-b9ec-4af4-ae61-e10d51f80241"] = lesson(
    B("Deepa wants a triangle with sides of 8, 15 and 6 centimetres. Her brother says it will not work. We need to say why he is right.",
      GIVEN("q", "Sides 8 cm, 15 cm, 6 cm. Why is this not a triangle?")),
    B("Picture it. Lay the longest side, 15, flat. Hinge the 8 at one end and the 6 at the other, and swing them towards each other. Will their tips meet?"),
    B("Here is the rule. The two shorter sides, added together, must be longer than the longest side. If not, they cannot reach each other.",
      L("r", SIDE_RULE)),
    B("So which sum do we test, and against which side?",
      ask=choose(["8 + 15 against 6", "8 + 6 against 15", "15 + 6 against 8"], 1,
                 "Any pair that includes the longest side will always beat the small side left over. The pair that might fall short is the two shortest sides.")),
    B("The two shorter sides are 8 and 6. 8 plus 6 is 14.",
      M("q", "8 cm"), M("q", "6 cm"), W("w1", "8 + 6 = 14")),
    B("Now compare. Is 14 more than 15?",
      ask=choose(["Yes, it is more", "No, it is less"], 1,
                 "Put 14 and 15 side by side. Which of them is the bigger number?")),
    B("No. 14 is less than 15. Even laid end to end, the two short sides cannot stretch across the long one. The shape will not close.",
      W("w2", "14 < 15")),
    B("So the reason is: 8 plus 6 is 14, which is less than 15, so these sides cannot form a triangle.",
      ANSR("a", "8 + 6 = 14, less than 15: no triangle", "no triangle", True)),
    B("Watch the other choices. One tests 8 plus 15, which is 23, against 6. That pair always passes, so it proves nothing.",
      W("t", "8 + 15 = 23"), N("t", "23", "always passes")),
    B("And three different side lengths are no problem at all. That is just a scalene triangle. The trouble here is the two short sides."),
    B("So to test three lengths: add the two shortest, and make sure the total beats the longest."),
)

# ── Arjun's sticks: 9, 12, 15 and three questions ────────────────────────────

LESSONS[A + "7f314a77-bc15-46f9-81aa-6aa186eb0fd5"] = lesson(
    B("Arjun makes a triangle from sticks of 9, 12 and 15 centimetres. There are three questions here, so we take them one at a time.",
      GIVEN("q", "Sticks 9 cm, 12 cm, 15 cm."), L("q2", "1) Kind by angles  2) Perimeter  3) New triangle?")),
    B("Question 1. There is a test for a right angle. Square the two shorter sides and add them. If that equals the square of the longest side, the triangle is right angled.",
      L("r1", SQUARE_TEST)),
    B("9 times 9 is 81. 12 times 12 is 144. Together they make 225.",
      W("w1", "9² = 81"), W("w2", "12² = 144"), W("w3", "81 + 144 = 225")),
    B("Now the longest side. 15 times 10 is 150, and 15 times 5 is 75. So what is 15 squared?",
      W("w4", "15 × 15 = 150 + 75"),
      ask=choose(["215", "225", "175"], 1,
                 "Add the two parts on the board: 150, and then 75 more.")),
    B("225. The two totals match! So the triangle is right angled.",
      W("w5", "15² = 225"), N("w5", "225", "a match")),
    B("Question 2. The perimeter is the distance all the way round, so add the three sides. 9 plus 12 plus 15 is 36 centimetres.",
      W("w6", "9 + 12 + 15 = 36")),
    B("Question 3. Arjun cuts the 15 stick into two equal pieces. 15 divided by 2 is 7.5. So the new sticks are 7.5, 7.5 and 9.",
      W("w7", "15 ÷ 2 = 7.5"), L("n", "New sticks: 7.5 cm, 7.5 cm, 9 cm")),
    B("Three sticks make a triangle only if the two shorter ones together are longer than the longest. The longest is now 9. Which sum do we test?",
      L("r2", SIDE_RULE),
      ask=choose(["7.5 + 9", "7.5 + 7.5", "9 + 9"], 1,
                 "The longest stick is the 9. The pair that has to reach across it is the two shorter sticks.")),
    B("7.5 plus 7.5 is 15, and 15 is more than 9. So yes, the new triangle can be made.",
      W("w8", "7.5 + 7.5 = 15"), W("w9", "15 > 9")),
    B("So the three answers are: right angled, 36 centimetres, and yes.",
      ANSR("a", "Right-angled; 36 cm; Yes", "36 cm", True)),
    B("Notice something neat. The two pieces together are just the old 15 stick. It was longer than 9 before the cut, so it still is."),
    B("Three questions, three tools: the squares test, adding the sides, and the two shorter sides against the longest."),
)

# ── Rahul's kite: isosceles, perimeter 56 ────────────────────────────────────

LESSONS[A + "87ad8698-a1e0-45de-a77f-0ba953734090"] = lesson(
    B("Rahul's kite frame is an isosceles triangle with a perimeter of 56 centimetres. The unequal side is 8 centimetres longer than each equal side. We want the sides, and where the largest angle is.",
      GIVEN("q", "Isosceles, perimeter 56 cm. Third side = equal side + 8")),
    B("We do not know the equal sides yet, so give them a name: s. Then the unequal side is s plus 8.",
      L("d1", "equal sides: s and s"), L("d2", "unequal side: s + 8")),
    B("The perimeter is all the sides added together, and it is 56. Which equation says that?",
      ask=choose(["s + 8 = 56", "s + s + 8 = 56", "s + s + s + 8 = 56"], 2,
                 "A triangle has three sides: s, then s again, and then the longer one, which is s plus 8. All three go into the perimeter.")),
    B("s plus s plus s plus 8 equals 56. Three lots of s, so 3 s plus 8 equals 56.",
      W("e1", "s + s + s + 8 = 56"), G("e1", ["s", ("s", 2), ("s", 3)], "3s"), W("e2", "3s + 8 = 56")),
    B("To undo plus 8, we take 8 away, from both sides to keep the balance. 56 minus 8 is 48.",
      S("e2", "+ 8", "− 8"), BOTH("e2", "− 8"), W("e3", "3s = 48")),
    B("3 s means 3 times s, so divide both sides by 3. 48 divided by 3 is 16. Each equal side is 16 centimetres.",
      DIV("e3", "3"), W("e4", "s = 16")),
    B("And the unequal side is 8 more: 16 plus 8 is 24 centimetres.",
      W("w1", "16 + 8 = 24"),
      FIG("f1", TRI("isosceles", None, {"ab": "16 cm", "ca": "16 cm", "bc": "24 cm"}))),
    B("Check the perimeter: 16 plus 16 plus 24 is 56. And 16 plus 16 is 32, which is more than 24, so the sides really do close up.",
      W("c1", "16 + 16 + 24 = 56"), W("c2", "16 + 16 = 32")),
    B("Now the largest angle. Think of opening a pair of scissors: the wider the angle, the further apart the tips. So where is the largest angle of a triangle?",
      ask=choose(["opposite a 16 cm side", "opposite the 24 cm side"], 1,
                 "The widest angle pushes its two arms furthest apart. So it faces the longest side of the triangle.")),
    B("Opposite the longest side, which is the 24 centimetre side.",
      L("r", "Largest angle is opposite the longest side")),
    B("So each equal side is 16 centimetres, and the largest angle is opposite the 24 centimetre side.",
      ANSR("a", "Equal sides 16 cm; largest angle faces 24 cm", "24 cm", True)),
    B("The trap is to mix up s and s plus 8, and call 24 the equal side. Always go back and read what your letter stood for."),
    B("So: name the unknown side, add up the perimeter, solve, and then answer every part of the question."),
    check=("s", 16),
)

# ── Ananya's rangoli: joining the midpoints ──────────────────────────────────

LESSONS[A + "8b35f7a2-1834-4508-a1e2-d5e13234deb9"] = lesson(
    B("Ananya draws a big triangle with a perimeter of 84 centimetres and angles of 50, 60 and 70 degrees. She joins the midpoints of its sides to make a smaller triangle inside. We want its perimeter and its angles.",
      GIVEN("q", "Big triangle: perimeter 84 cm, angles 50°, 60°, 70°"), L("q2", "Join the midpoints of the sides. Inner triangle?"),
      FIG("f1", TRI("scalene", ["60°", "50°", "70°"]))),
    B("A midpoint is the halfway point of a side. Joining the three midpoints cuts the big triangle into 4 small triangles, and all 4 are exactly alike.",
      L("f", "4 small triangles, all the same")),
    B("Each small one is a half size copy of the big triangle: the same shape, with every side half as long.",
      L("h", "Each inner side = half of a big side")),
    B("So every side of the inner triangle is half of a big side. What happens to the perimeter?",
      ask=choose(["it stays 84 cm", "it is halved too", "it becomes a quarter"], 1,
                 "The perimeter is the three sides added together. If each of the three is cut in half, their total is cut in half as well.")),
    B("It is halved too. 84 divided by 2 is 42 centimetres.",
      W("w1", "84 ÷ 2 = 42")),
    B("Let's see it with numbers. Suppose the big sides were 24, 28 and 32, which add up to 84. Their halves are 12, 14 and 16, and those add up to 42.",
      W("w2", "24 + 28 + 32 = 84"), W("w3", "12 + 14 + 16 = 42")),
    B("Now the angles. The inner triangle is the same shape as the big one, only smaller. So what happens to its angles?",
      ask=choose(["they are halved", "they stay the same", "they double"], 1,
                 "An angle measures how wide a corner opens, not how long its arms are. Shrinking a shape does not change its corners.")),
    B("They stay the same: 50, 60 and 70 degrees.",
      L("s", "Same shape → same angles: 50°, 60°, 70°")),
    B("Here is the proof that halving the angles cannot be right. 25, 30 and 35 add up to only 90, and a triangle's angles must add up to 180.",
      W("c1", "25 + 30 + 35 = 90"), W("c2", "50 + 60 + 70 = 180")),
    B("So the inner triangle has a perimeter of 42 centimetres, and angles of 50, 60 and 70 degrees.",
      ANSR("a", "Perimeter 42 cm; angles 50°, 60°, 70°", "42 cm", True)),
    B("Remember this: shrink a shape and its lengths shrink, but its angles do not."),
)

# ── Priya's garden and tile: 12, 16, 20 and a half-size copy ─────────────────

LESSONS[A + "0cefe8e7-7fc1-4460-b97e-d0a2d511127e"] = lesson(
    B("Priya's garden is a triangle with sides of 12, 16 and 20 centimetres. A tile inside it is a triangle with every side half as long. We must add the largest angle of each.",
      GIVEN("q", "Garden: 12 cm, 16 cm, 20 cm. Tile: each side half."), L("q2", "Largest angle of garden + largest angle of tile = ?")),
    B("The story hints that one angle is special. There is a test for a right angle: square the two shorter sides and add. If that equals the square of the longest side, there is a right angle.",
      L("r1", SQUARE_TEST)),
    B("12 times 12 is 144. 16 times 16 is 256. Together they make 400.",
      W("w1", "12² = 144"), W("w2", "16² = 256"), W("w3", "144 + 256 = 400")),
    B("Now the longest side. What is 20 squared?",
      ask=choose(["40", "400", "200"], 1,
                 "20 squared is 20 times 20, not 20 times 2. Work out 2 times 2, and then put the two zeros back.")),
    B("400. The totals match, so the garden has a right angle. And in a right angled triangle, 90 degrees is the largest angle, because the other two share the other 90.",
      W("w4", "20² = 400"), L("g", "Garden: largest angle 90°"),
      FIG("f1", TRI("right", None, {"ab": "12 cm", "bc": "16 cm", "ca": "20 cm"}))),
    B("Now the tile. Halve each side: 6, 8 and 10 centimetres.",
      W("w5", "12 ÷ 2 = 6"), W("w6", "16 ÷ 2 = 8"), W("w7", "20 ÷ 2 = 10")),
    B("The tile is the same shape as the garden, only smaller. So what is its largest angle?",
      ask=choose(["45°", "90°", "180°"], 1,
                 "Shrinking a shape makes its sides shorter, but its corners open just as wide as before. Angles do not shrink.")),
    B("90 degrees again. We can test it: 6 squared is 36, 8 squared is 64, and together they make 100. And 10 squared is 100. A match.",
      W("w8", "6² + 8² = 36 + 64"), W("w9", "36 + 64 = 100"), W("w10", "10² = 100"), L("t", "Tile: largest angle 90°")),
    B("Now add the two largest angles. 90 plus 90 is 180 degrees.",
      ANSR("a", "90 + 90 = 180", "180")),
    B("The trap is to think a smaller triangle must have smaller angles. Halve the sides, and the angles stay exactly as they were."),
    B("So: use the squares test to spot the right angle, and remember that a smaller copy keeps the same angles."),
)
