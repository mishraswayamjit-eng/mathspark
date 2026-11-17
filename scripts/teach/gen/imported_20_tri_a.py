"""Triangle lessons of imported-20: angle sum, isosceles and equilateral, naming by angles."""
from imported_20_lib import (P, B, LESSON, G, W, Lb, A, U, C, X, BOTH, DIV, F, bar, bars, seg, tri,
                             choose_at, ask_180, FACT)
from imported_20_tri import xsum

LESSONS = {}

X_METHOD = ("So the method: call the unknown angle x, write every angle using x, make them add up to 180, and solve. "
            "Then read the question again to see what it really wants.")


def third_ask(q, total, right, others, if_not):
    return B("The three angles must make 180, and the ones we know use up %d. How do we find the third?" % total,
             ask=choose_at(q, "third", right, others, if_not))


LEFT_OVER = "The third angle is whatever is left of the 180 once the other two are taken out. Finding what is left is a take away."

# ── 3x, x, x + 20: largest angle and type ──
q = P + "a125fe02-aab3-4711-85cf-23c25b9a8b74"
LESSONS[q] = xsum(
    q, "Tara's triangle has three angles, and two of them are described using the second angle. We want the largest angle, and the type of triangle.",
    ["First angle = 3 × second angle", "Third angle = second angle + 20°"],
    [(3, 0, "First"), (1, 0, "Second"), (1, 20, "Third")],
    "We don't know the second angle yet, so let's call it x. Then the first angle is 3 x, and the third angle is x plus 20.",
    [
        B("Careful, x is not the answer yet. With x as 32, which angle is the largest?",
          ask=choose_at(q, "largest", "the first, 3x", ["the third, x + 20", "the second, x"],
                        "Put 32 in place of x. 3 times 32 is much more than 32 plus 20, so the first angle is the largest.")),
        B("3 times 32 is 96, so the first angle is 96 degrees. The third is 32 plus 20, which is 52 degrees.",
          W("a1", "3 × 32 = 96"), W("a2", "32 + 20 = 52")),
        B("Now for the type: a right angle is 90 degrees, and 96 is more than that. A triangle with one angle bigger than a right angle is called obtuse.",
          W("a3", "96 > 90")),
    ],
    ("Largest angle = 96°, an obtuse triangle", "96°"),
    "So the largest angle is 96 degrees, and Tara's patch is an obtuse triangle.",
    X_METHOD)

# ── x, x + 20, 3x: type only ──
q = P + "c139ad61-0429-4946-8845-bc90c0187368"
LESSONS[q] = xsum(
    q, "In Lakshmi's triangle the largest angle is three times the smallest, and the middle angle is 20 degrees more than the smallest. We want the type of triangle.",
    ["Largest angle = 3 × smallest angle", "Middle angle = smallest angle + 20°"],
    [(1, 0, "Smallest"), (1, 20, "Middle"), (3, 0, "Largest")],
    "Everything is described using the smallest angle, so let's call that one x. Then the middle angle is x plus 20, and the largest is 3 x.",
    [
        B("The type of a triangle is decided by its largest angle, and that is 3 x. 3 times 32 is 96 degrees.", W("a1", "3 × 32 = 96")),
        B("The largest angle is 96 degrees, and a right angle is 90 degrees. So what kind of triangle is this?", W("a2", "96 > 90"),
          ask=choose_at(q, "type", "obtuse-angled", ["acute-angled", "right-angled"],
                        "Compare 96 with 90. It is more than a right angle, and a triangle with an angle bigger than a right angle is called obtuse-angled.")),
        B("One angle bigger than 90 degrees makes the whole triangle obtuse-angled. For the record, the middle angle is 32 plus 20, which is 52 degrees.",
          W("a3", "32 + 20 = 52")),
    ],
    ("Largest angle 96°: obtuse-angled triangle", "obtuse-angled"),
    "So Lakshmi has drawn an obtuse-angled triangle.",
    "So the method: call the smallest angle x, write every angle using x, make them add up to 180, and solve. Then let the largest angle name the triangle.",
    checked=True)

# ── x, 2x, 3x: the largest angle ──
q = P + "df22c72e-9551-4e67-8cbe-f45b10e49205"
LESSONS[q] = xsum(
    q, "In Deepa's tile, one angle is twice the smallest angle, and the largest is three times the smallest. We want the largest angle.",
    ["One angle = 2 × smallest angle", "Largest angle = 3 × smallest angle"],
    [(1, 0, "Smallest"), (2, 0, "Second"), (3, 0, "Largest")],
    "Everything is measured against the smallest angle, so let's call that one x. Then the other two angles are 2 x and 3 x.",
    [
        B("Careful, x is the smallest angle, and the question wants the largest. Which sum gives the largest angle?",
          ask=choose_at(q, "largest", "3 × 30", ["2 × 30", "30 + 3"],
                        "The largest angle is three times the smallest, and the smallest is 30. So we want 3 times 30.")),
        B("3 times 30 is 90. And the angle in the middle is 2 times 30, which is 60.", W("a1", "3 × 30 = 90"), W("a2", "2 × 30 = 60")),
    ],
    ("Largest angle = 90°", "90°"),
    "So the largest angle is 90 degrees, a right angle. Deepa's tile is a right-angled triangle.",
    X_METHOD)

# ── x + 15, x, x + 25: type only, and x is not a whole number ──
q = P + "cd2d25aa-ed71-40c4-b2b9-8168cc15950b"
LESSONS[q] = LESSON([
    B("In Meera's banner, the first angle is 15 degrees more than the second, and the third is 25 degrees more than the second. We want the type of triangle.",
      G("g1", "First angle = second angle + 15°"), G("g2", "Third angle = second angle + 25°")),
    B("Both clues lean on the second angle, so let's call it x. Then the first angle is x plus 15, and the third is x plus 25.",
      Lb("n", "Angles: x + 15, x, x + 25"),
      F(bars(bar("First", [seg("x"), seg("15°", 0.5, "c")]), bar("Second", [seg("x")]), bar("Third", [seg("x"), seg("25°", 0.8, "c")]),
             note="The three angles together make the whole triangle"))),
    ask_180(q),
    B("So our three angles together make 180: x plus 15, plus x, plus x plus 25.", FACT(), W("e1", "x + 15 + x + x + 25 = 180")),
    B("There are 3 x's, and 15 plus 25 is 40. So 3 x plus 40 equals 180. Take 40 from both sides, and 3 x equals 140.",
      W("e2", "3x + 40 = 180"), X("e2", "+ 40", "− 40"), W("e3", "3x = 140")),
    B("Now, 140 does not divide by 3 exactly. 3 times 46 is 138 and 3 times 47 is 141, so x is somewhere between 46 and 47 degrees.",
      W("w1", "3 × 46 = 138"), W("w2", "3 × 47 = 141")),
    B("That is fine, because we only need the type of triangle. Which angle decides the type?",
      ask=choose_at(q, "which", "the largest, x + 25", ["the smallest, x", "the middle, x + 15"],
                    "If the largest angle is under a right angle, the other two must be as well. So the largest one, x plus 25, decides the type.")),
    B("x is less than 47, so the largest angle is less than 47 plus 25, which is 72.", W("w3", "47 + 25 = 72")),
    B("72 is well under 90, the size of a right angle. So all three angles are smaller than a right angle.", W("w4", "72 < 90")),
    B("A triangle whose angles are all less than 90 degrees is an acute-angled triangle. That is Meera's banner.",
      A("ans", "All angles less than 90°: acute-angled"), C("ans", "acute-angled")),
    B("Check another way. If the largest angle were 90, the second would be 65 and the first 80. Those add up to 235, far more than 180, so the real angles must be smaller.",
      W("c1", "90 − 25 = 65"), W("c2", "65 + 15 = 80"), W("c3", "65 + 80 + 90 = 235"), W("c4", "235 > 180")),
    B("So the method: write every angle using x and make them add up to 180. And when you only need the type, you just need to know which side of 90 the largest angle falls."),
], {"variable": "x", "value": "140/3"})

# ── Isosceles, 40° between the equal sides ──
q = P + "a41aeda1-2994-45eb-bd4f-e1569ca5e01d"
LESSONS[q] = LESSON([
    B("Sanya's flag is a triangle with exactly two equal sides, and the angle between those two sides is 40 degrees. We want each of the other two angles.",
      G("g1", "Two equal sides, angle between them = 40°"), F(tri("isosceles", a="40°", b="?", c="?"))),
    B("A triangle with two equal sides is called isosceles. Its special trick: the two angles opposite the equal sides are equal to each other.",
      Lb("w0", "The other two angles are equal")),
    ask_180(q),
    B("So the 40 and the two equal angles make 180. Take the 40 away: 180 minus 40 is 140.", FACT(), W("w1", "180 − 40 = 140")),
    B("That 140 is for both of the equal angles together. So how big is each one?",
      ask=choose_at(q, "each", "140 ÷ 2", ["140", "140 − 40"],
                    "The 140 is shared by two angles of the same size. Sharing equally between 2 means dividing by 2.")),
    B("140 divided by 2 is 70. Careful: this is where many people stop at 140, but that is two angles, not one.", W("w2", "140 ÷ 2 = 70")),
    B("So each of the other two angles is 70 degrees.", A("ans", "Each of the other angles = 70°"), C("ans", "70°")),
    B("Check: 40 plus 70 plus 70 is 180. It fits.", W("c1", "40 + 70 + 70 = 180")),
    B("So for a triangle with two equal sides: take the angle between them from 180, then halve what is left."),
])

# ── 60° and 60°: third angle and type ──
q = P + "af918b14-ab07-445c-8e1a-e3e95633593d"
LESSONS[q] = LESSON([
    B("Sunita's piece of cloth is a triangle with two angles of 60 degrees each. We want the third angle, and the type of triangle.",
      G("g1", "Two angles: 60° and 60°"), F(tri("isosceles", a="?", b="60°", c="60°"))),
    ask_180(q),
    B("So the two angles we know and the third one make 180. First add the two we know: 60 plus 60 is 120.", FACT(), W("w1", "60 + 60 = 120")),
    B("Take that from 180 to see what is left for the third angle. 180 minus 120 is 60.", W("w2", "180 − 120 = 60")),
    B("So the angles are 60, 60 and 60. All three are equal. What do we call a triangle like that?", Lb("w3", "Angles: 60°, 60°, 60°"),
      ask=choose_at(q, "name", "equilateral", ["isosceles", "obtuse"],
                    "Isosceles is the name we use when just two angles are equal. Here all three are equal, and that has its own special name: equilateral.")),
    B("When all three angles are equal, all three sides are equal too. That is an equilateral triangle, and its angles are always 60 degrees each."),
    B("So the third angle is 60 degrees, and it is an equilateral triangle.", A("ans", "Third angle = 60°, equilateral triangle"), C("ans", "60°")),
    B("Check: 60 plus 60 plus 60 is 180. It fits.", W("c1", "60 + 60 + 60 = 180")),
    B("So to find a missing angle, add the two you know and take the total from 180. Then look at all three angles to name the triangle."),
])

# ── Angles in the ratio 3 : 5 : 7 ──
q = P + "b0d31ddd-4a6f-4633-b304-8cb390ddc1b4"
LESSONS[q] = LESSON([
    B("The three angles of Farhan's garden are in the ratio 3 to 5 to 7. We must find the largest angle and name the triangle. The 12 metre side is extra: only the angles matter here.",
      G("g1", "Angles in the ratio 3 : 5 : 7")),
    ask_180(q),
    B("So 180 degrees is shared between the three angles in the ratio 3 to 5 to 7. Count the parts: 3 plus 5 plus 7 is 15.",
      FACT(), W("w1", "3 + 5 + 7 = 15"),
      F(bars(bar("Smallest", [seg(tone="a") for _ in range(3)]), bar("Middle", [seg(tone="b") for _ in range(5)]),
             bar("Largest", [seg(tone="c") for _ in range(7)]), note="All the boxes together: 180°"))),
    B("15 equal parts make 180 degrees. So one part is 180 divided by 15, which is 12 degrees.", W("w2", "180 ÷ 15 = 12")),
    B("Now each angle. 3 times 12 is 36, 5 times 12 is 60, and 7 times 12 is 84.",
      W("w3", "3 × 12 = 36"), W("w4", "5 × 12 = 60"), W("w5", "7 × 12 = 84")),
    B("To name the triangle, compare the largest angle, 84 degrees, with a right angle, 90 degrees. What kind of triangle is it?", W("w6", "84 < 90"),
      ask=choose_at(q, "type", "acute-angled", ["obtuse-angled", "right-angled"],
                    "84 is less than 90, so even the largest angle is smaller than a right angle. A triangle like that is acute-angled.")),
    B("Don't be fooled because 84 is close to 90. It is still less, so all three angles are acute, and the triangle is acute-angled."),
    B("So it is an acute-angled triangle, and its largest angle is 84 degrees.", A("ans", "Acute-angled, largest angle = 84°"), C("ans", "84°")),
    B("Check: 36 plus 60 plus 84 is 180. The three angles fit a triangle.", W("c1", "36 + 60 + 84 = 180")),
    B("So for angles in a ratio: share 180 degrees into the parts, find each angle, then let the largest angle name the triangle."),
])

# ── The kite: 52° and 34° ──
q = P + "b2c0c32e-ebf3-4701-abe4-09f931109c0d"
LESSONS[q] = LESSON([
    B("The kite string and the ground make a triangle. One angle on the ground is 52 degrees and the angle up at the kite is 34 degrees. We want the third angle, where the string on Arjun's side meets the ground.",
      G("g1", "Angle on the ground = 52°, angle at the kite = 34°"),
      F(tri("scalene", a="34°", b="52°", c="?", note="The kite is at the top. Arjun's angle is the ?"))),
    ask_180(q),
    B("Add the two angles we know. 52 plus 34 is 86.", FACT(), W("w1", "52 + 34 = 86")),
    third_ask(q, 86, "180 − 86", ["180 + 86", "86 − 52"], LEFT_OVER + " So it is 180 minus 86."),
    B("Do it in two hops: 180 minus 80 is 100, and 100 minus 6 is 94. Go carefully here, this is where small slips creep in.",
      W("w2", "180 − 80 = 100"), W("w3", "100 − 6 = 94"), W("w4", "180 − 86 = 94")),
    B("So the string on Arjun's side makes an angle of 94 degrees with the ground.", A("ans", "Angle on Arjun's side = 94°"), C("ans", "94°")),
    B("Check: 52 plus 34 plus 94 is 180. It fits.", W("c1", "52 + 34 + 94 = 180")),
    B("So to find the third angle of any triangle: add the two you know, and take the total from 180."),
])

# ── Two isosceles triangles: 40° and then 100° between the equal sides ──
q = P + "c16897be-8e91-47cf-99d3-4f234b1fd14d"
LESSONS[q] = LESSON([
    B("Tanvi's flag is an isosceles triangle with 40 degrees between its two equal sides. Then she changes that angle to 100 degrees. We want the difference between the base angles, new and old.",
      G("g1", "Isosceles: angle between equal sides = 40°"), G("g2", "New triangle: that angle = 100°")),
    B("In an isosceles triangle, the two base angles, the ones opposite the equal sides, are equal to each other.",
      F(tri("isosceles", a="40°", b="?", c="?")), Lb("w0", "The two base angles are equal")),
    ask_180(q),
    B("Start with the first triangle. Take the 40 away from 180, and 140 is left for the two base angles together.", FACT(), W("w1", "180 − 40 = 140")),
    B("Those two base angles are equal. So how big is each one?",
      ask=choose_at(q, "each", "140 ÷ 2", ["140", "140 − 40"],
                    "The 140 is shared by two angles of the same size. Sharing equally between 2 means dividing by 2.")),
    B("140 divided by 2 is 70. So each base angle of the first triangle is 70 degrees.", W("w2", "140 ÷ 2 = 70")),
    B("Now the new triangle, done the very same way. 180 minus 100 is 80, and 80 divided by 2 is 40. Each base angle is now 40 degrees.",
      U("g2", "100°"), W("w3", "180 − 100 = 80"), W("w4", "80 ÷ 2 = 40")),
    B("The question asks for the difference, so compare one base angle from each triangle. 70 minus 40 is 30.", W("w5", "70 − 40 = 30")),
    B("So each base angle is 30 degrees smaller in the new triangle.", A("ans", "Difference between the base angles = 30°"), C("ans", "30°")),
    B("Check both triangles. 40 plus 70 plus 70 is 180, and 100 plus 40 plus 40 is 180. Both fit.",
      W("c1", "40 + 70 + 70 = 180"), W("c2", "100 + 40 + 40 = 180")),
    B("So for any isosceles triangle: take the angle between the equal sides from 180, then halve what is left to get each base angle."),
])

# ── Isosceles flag: perimeter 84 cm, and 40° between the equal sides ──
q = P + "c29423a2-fba4-4974-a8de-7e81fe91a8af"
LESSONS[q] = LESSON([
    B("Sunita's flag is an isosceles triangle with a perimeter of 84 centimetres. The unequal side is 12 centimetres shorter than each equal side, and the angle between the equal sides is 40 degrees.",
      G("g1", "Perimeter = 84 cm, angle between equal sides = 40°"), G("g2", "Unequal side = equal side − 12 cm")),
    B("We want each equal side and each of the other two angles. That is two jobs, so take the sides first. Call each equal side a. Then the unequal side is a minus 12.",
      F(tri("isosceles", a="40°", sides={"ab": "a", "ca": "a", "bc": "a − 12"}))),
    B("The perimeter is all three sides added together. So a, plus a, plus a minus 12, equals 84.", W("e1", "a + a + (a − 12) = 84")),
    B("Three a's make 3 a, so 3 a minus 12 equals 84. What should we do to both sides to clear away the minus 12?", W("e2", "3a − 12 = 84"),
      ask=choose_at(q, "undo", "add 12", ["subtract 12", "divide by 3"],
                    "To undo a minus 12 we do the opposite, which is to add 12. And we do it to both sides to keep them equal.")),
    B("84 plus 12 is 96. So 3 a equals 96.", X("e2", "− 12", "+ 12"), BOTH("e2", "+ 12"), W("e3", "3a = 96")),
    B("Now divide both sides by 3. 96 divided by 3 is 32, so each equal side is 32 centimetres.", DIV("e3", 3), W("e4", "a = 32")),
    B("Check the sides before moving on. The unequal side is 32 minus 12, which is 20, and 32 plus 32 plus 20 is 84.",
      W("c1", "32 − 12 = 20"), W("c2", "32 + 32 + 20 = 84")),
    B("Now the angles. What do the three angles of any triangle add up to?",
      ask=choose_at(q, "a180", "180°", ["90°", "360°"],
                    "Tear the three corners off a paper triangle and put them side by side. They always make a straight line, and a straight line is 180 degrees.")),
    B("The angle between the equal sides is 40 degrees. 180 minus 40 leaves 140 for the other two angles together.", FACT(), W("w1", "180 − 40 = 140")),
    B("Those two angles are opposite the equal sides, so they are equal. 140 divided by 2 is 70. Careful not to stop at 140: that is two angles, not one.",
      W("w2", "140 ÷ 2 = 70")),
    B("So each of the equal angles is 70 degrees, and each equal side is 32 centimetres.",
      A("ans", "Each equal angle = 70°, each equal side = 32 cm"), C("ans", "70°"), C("ans", "32 cm")),
    B("Check the angles too: 40 plus 70 plus 70 is 180.", W("c3", "40 + 70 + 70 = 180")),
    B("So when a question mixes sides and angles, split it in two. The perimeter gives the sides, and the 180 degree rule gives the angles."),
], {"variable": "a", "value": "32"})

# ── 90° and 35° ──
q = P + "cad77791-6999-46e9-b829-6524c68a8048"
LESSONS[q] = LESSON([
    B("Arjun's bamboo triangle has one angle of 90 degrees and another of 35 degrees. We want the third angle.",
      G("g1", "Two angles: 90° and 35°"), F(tri("right", a="35°", b="90°", c="?"))),
    ask_180(q),
    B("Add the two angles we know. 90 plus 35 is 125.", FACT(), W("w1", "90 + 35 = 125")),
    third_ask(q, 125, "180 − 125", ["180 + 125", "125 − 90"], LEFT_OVER + " So it is 180 minus 125."),
    B("180 minus 125 is 55. Careful not to stop at 125: that is the two angles we already had, not the missing one.", W("w2", "180 − 125 = 55")),
    B("So the third angle of Arjun's triangle is 55 degrees.", A("ans", "Third angle = 55°"), C("ans", "55°")),
    B("Check: 90 plus 35 plus 55 is 180. And here is a bonus: in a right-angled triangle the other two angles always make 90, and 35 plus 55 is 90.",
      W("c1", "90 + 35 + 55 = 180"), W("c2", "35 + 55 = 90")),
    B("So to find the third angle of any triangle: add the two you know, and take the total from 180."),
])

# ── Sticks 8, 15, 8: equal angles of 28° ──
q = P + "d316dfa5-a728-45f3-8596-e1e99bb9f2c1"
LESSONS[q] = LESSON([
    B("Vikram's triangle has two sticks of 8 centimetres, so two of its sides are equal. Each of the two equal angles is 28 degrees. We want the angle between the two equal sides.",
      G("g1", "Sides: 8 cm, 15 cm, 8 cm"), G("g2", "The two equal angles are 28° each"),
      F(tri("isosceles", a="?", b="28°", c="28°", sides={"ab": "8 cm", "ca": "8 cm", "bc": "15 cm"}))),
    B("The equal angles sit at the two ends of the long stick, opposite the equal sides. The angle we want is the third one, at the top, where the two short sticks meet.",
      U("g1", "8 cm"), U("g1", "8 cm", 2)),
    ask_180(q),
    B("Add the two angles we know. 28 plus 28 is 56.", FACT(), W("w1", "28 + 28 = 56")),
    third_ask(q, 56, "180 − 56", ["180 − 28", "56 ÷ 2"],
              "Both of the 28 degree angles are inside the triangle, so both must come out of the 180. Together they are 56, so it is 180 minus 56."),
    B("180 minus 56 is 124. Notice we never used the stick lengths in the sum: they only told us which sides are equal.", W("w2", "180 − 56 = 124")),
    B("So the angle between the two equal sides is 124 degrees.", A("ans", "Angle between the equal sides = 124°"), C("ans", "124°")),
    B("Check: 28 plus 28 plus 124 is 180. It fits.", W("c1", "28 + 28 + 124 = 180")),
    B("So when you know the two equal angles of an isosceles triangle: add them, and take the total from 180 to get the angle between the equal sides."),
])

# ── 70° and 70°: is it acute and isosceles? ──
q = P + "d510200e-62ae-4d85-b72a-391c89b1e09a"
LESSONS[q] = LESSON([
    B("Neha's bookmark has two angles of 70 degrees each. She says it is both an acute triangle and an isosceles triangle. We must find the third angle and decide if she is right.",
      G("g1", "Two angles: 70° and 70°"), G("g2", "Neha says: acute and isosceles"), F(tri("isosceles", a="?", b="70°", c="70°"))),
    ask_180(q),
    B("70 plus 70 is 140, and 180 minus 140 leaves 40. So the third angle is 40 degrees.", FACT(), W("w1", "70 + 70 = 140"), W("w2", "180 − 140 = 40")),
    B("Now test Neha's word isosceles. A triangle is isosceles when two of its angles are equal. Here two angles are both 70, so yes.",
      Lb("t1", "Angles: 70°, 70°, 40°"), U("t1", "70°"), U("t1", "70°", 2), U("g2", "isosceles")),
    B("Now her other word, acute. What must be true for a triangle to be acute?", U("g2", "acute"),
      ask=choose_at(q, "acute", "all 3 angles less than 90°", ["one angle less than 90°", "two angles equal"],
                    "Every triangle has some angles under 90 degrees, so one is not enough. A triangle is acute only when all three of its angles are less than 90 degrees.")),
    B("Look at each one: 70, 70 and 40 are all less than 90. So it is acute as well.", W("w3", "70 < 90"), W("w4", "40 < 90")),
    B("So Neha is correct on both counts, and the third angle is 40 degrees.", A("ans", "Neha is right, third angle = 40°"), C("ans", "40°")),
    B("Check: 70 plus 70 plus 40 is 180. It fits.", W("c1", "70 + 70 + 40 = 180")),
    B("So find the missing angle from 180 first. Then test each name on its own: equal angles for isosceles, all angles under 90 for acute."),
])

# ── 60° between two equal sides of 7 cm ──
q = P + "df55bd02-ab7a-4017-9598-03a9e3a01d31"
LESSONS[q] = LESSON([
    B("Kavya's triangle has an angle of 60 degrees, and the two sides that form it are both 7 centimetres. We want each of the other two angles.",
      G("g1", "One angle = 60°, between two sides of 7 cm"),
      F(tri("isosceles", a="60°", b="?", c="?", sides={"ab": "7 cm", "ca": "7 cm"}))),
    B("Two equal sides make this an isosceles triangle. So the two angles opposite those sides, the ones we want, are equal to each other.",
      Lb("w0", "The other two angles are equal")),
    ask_180(q),
    B("Take the 60 away from 180. That leaves 120 for the other two angles together.", FACT(), W("w1", "180 − 60 = 120")),
    B("That 120 is for both angles together, and they are equal. So how big is each one?",
      ask=choose_at(q, "each", "120 ÷ 2", ["120", "120 − 60"],
                    "The 120 is shared by two angles of the same size. Sharing equally between 2 means dividing by 2.")),
    B("120 divided by 2 is 60. Careful not to stop at 120: that is both angles together.", W("w2", "120 ÷ 2 = 60")),
    B("So each of the other two angles is 60 degrees.", A("ans", "Each of the other angles = 60°"), C("ans", "60°")),
    B("Look what happened: all three angles are 60 degrees, and 60 plus 60 plus 60 is 180. So this triangle is equilateral, and its third side is 7 centimetres too.",
      W("c1", "60 + 60 + 60 = 180")),
    B("So for a triangle with two equal sides: take the angle between them from 180, then halve what is left."),
])

# ── Sides 6, 8, 10 ──
q = P + "f2300d21-5b20-4b8d-abc8-27ec390378c7"
LESSONS[q] = LESSON([
    B("Rohan's window frame has sides of 6, 8 and 10 centimetres. He notices that the longest side squared equals the squares of the other two sides added together. We want the type of triangle.",
      G("g1", "Sides: 6 cm, 8 cm, 10 cm")),
    B("Let's test what Rohan noticed for ourselves. First, what does 6 squared mean?",
      ask=choose_at(q, "sq", "6 × 6", ["6 × 2", "6 + 6"],
                    "Squared means a number times itself. So 6 squared is 6 times 6, not 6 times 2.")),
    B("6 squared is 6 times 6, which is 36. And 8 squared is 8 times 8, which is 64.",
      U("g1", "6 cm"), U("g1", "8 cm"), W("w1", "6² = 36"), W("w2", "8² = 64")),
    B("Add those two squares: 36 plus 64 is 100.", W("w3", "36 + 64 = 100")),
    B("Now the longest side. 10 squared is 10 times 10, and that is 100 as well. The two results match, so Rohan is right.",
      U("g1", "10 cm"), W("w4", "10² = 100"), C("w3", "100"), C("w4", "100")),
    B("Only one kind of triangle has sides that do this. Which kind?",
      ask=choose_at(q, "type", "right-angled", ["equilateral", "acute-angled"],
                    "This is the special rule of right-angled triangles, named after Pythagoras. When the squares match like this, the angle opposite the longest side is a right angle.")),
    B("It is the rule of Pythagoras. The squares match exactly only when the triangle has a right angle, and that angle sits opposite the longest side.",
      W("w5", "6² + 8² = 10²")),
    B("So the window frame is a right-angled triangle.", A("ans", "Right-angled triangle"), C("ans", "Right-angled")),
    B("Check the other names. It cannot be equilateral, because its three sides are all different. And the matching squares rule out acute and obtuse."),
    B("So to test for a right angle using only the sides: square the two shorter sides, add them, and see whether you get the longest side squared."),
])
