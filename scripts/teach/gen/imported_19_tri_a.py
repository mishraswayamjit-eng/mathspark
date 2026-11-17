"""Triangles: the angle sum (a missing angle, naming by angles, angles given in terms of one another)."""
from imported_19_lib import ANS, ANSR, B, BOTH, DIV, FIG, G, L, M, N, S, TRI, W, GIVEN, choose, lesson, pick

LESSONS = {}
A = "AIGEN_grade5_"

RULE = "Angles of a triangle add up to 180°"
KINDS = [("k1", "Acute: all three angles less than 90°"),
         ("k2", "Right: one angle is exactly 90°"),
         ("k3", "Obtuse: one angle is more than 90°")]
KINDS_SAY = "If all three angles are less than 90 degrees, it is acute. If one is exactly 90, it is right. If one is more than 90, it is obtuse."


def rule_ops():
    return [L("r", RULE), M("r", "180°", "box")]


def kind_ops():
    return [L(i, t) for i, t in KINDS]


# ── A missing angle ──────────────────────────────────────────────────────────

def third_angle(qid, a, b, intro, given, fig, found, trap):
    s = a + b
    t = 180 - s
    return lesson(
        B(intro, GIVEN("q", given), FIG("f1", fig)),
        B("Every triangle keeps one rule about its angles. What do the three angles of any triangle add up to?",
          ask=choose(["90°", "180°", "360°"], 1,
                     "90 degrees is one square corner, and 360 is a full turn. The three angles of a triangle together make a half turn.")),
        B("180 degrees. Always, for every triangle.", rule_ops()),
        B("We know two of the angles, so add them. %d plus %d is %d." % (a, b, s),
          W("w1", "%d + %d = %d" % (a, b, s))),
        B("So %d of the 180 degrees are used up. How do we find the third angle?" % s,
          ask=choose(["180 + %d" % s, "180 − %d" % s, "%d − 90" % s], 1,
                     "The three angles share 180 degrees between them. Two of them have used %d, so the third is whatever is left." % s)),
        B("180 minus %d is %d. %s" % (s, t, found),
          ANSR("a", "180 − %d = %d" % (s, t), str(t))),
        B("Check by adding all three: %d plus %d plus %d is 180. A full set." % (a, b, t),
          W("c", "%d + %d + %d = 180" % (a, b, t))),
        trap,
        B("So for a missing angle in a triangle: add the two you know, and take the total away from 180."),
    )


LESSONS[A + "7e937a6a-c649-499a-9a5e-b4c6e9efa2c2"] = third_angle(
    A + "7e93", 52, 74,
    "Two tent poles lean together and stand on the ground, making a triangle. The angle at the top is 52 degrees, and the left pole meets the ground at 74 degrees. What is the angle on the right?",
    "Top 52°, left 74°. Right angle = ?",
    TRI("scalene", ["52°", "74°", "?"]),
    "So the right pole meets the ground at 54 degrees.",
    B("Subtract with care here. The choices are all close together, so one small slip lands on one of them. That is why we add all three to check."))

LESSONS[A + "9207ef7a-1aa5-492d-8002-900c48f3f55c"] = third_angle(
    A + "9207", 65, 48,
    "Two sticks stand on a plank and lean in until they meet, making a triangle. The left stick makes 65 degrees with the plank, and the right stick makes 48 degrees. What is the angle at the top?",
    "Left 65°, right 48°. Top angle = ?",
    TRI("scalene", ["?", "65°", "48°"]),
    "So the two sticks meet at 67 degrees.",
    B("The trap is to stop at 113. That is the two angles we were given, added together. The question wants the angle that is left."))


# ── A missing angle, then the kind of triangle ───────────────────────────────

def third_and_kind(qid, a, b, intro, given, answer, ring, trap):
    s = a + b
    t = 180 - s
    return lesson(
        B(intro, GIVEN("q", given), FIG("f1", TRI("scalene", ["?", "%d°" % a, "%d°" % b]))),
        B(pick(qid, "rule", [
            "We cannot name the triangle until we know all three angles. So first, the rule: the three angles of a triangle add up to 180 degrees.",
            "Two angles are not enough to name a triangle. We need the third. Here is the rule that finds it: the three angles add up to 180 degrees."]),
          rule_ops()),
        B("Add the two we know. %d plus %d is %d." % (a, b, s),
          W("w1", "%d + %d = %d" % (a, b, s))),
        B("Now, which sum gives the third angle?",
          ask=choose(["%d − 90" % s, "180 + %d" % s, "180 − %d" % s], 2,
                     "The three angles share 180 degrees. Two of them use up %d, so the third is what is left over." % s)),
        B("180 minus %d is %d. So the third angle is %d degrees." % (s, t, t),
          W("w2", "180 − %d = %d" % (s, t)), N("w2", str(t), "third angle")),
        B("Now we can name the triangle by its angles. " + KINDS_SAY, kind_ops()),
        B("Our angles are %d, %d and %d. Is any of them 90 degrees or more?" % (a, b, t),
          L("an", "Angles: %d°, %d°, %d°" % (a, b, t)),
          ask=choose(["Yes, one of them", "No, all are less than 90°"], 1,
                     "Compare each angle with 90, one at a time: %d, then %d, then %d. Is any of them as big as 90?" % (a, b, t))),
        B("None of them. All three angles are less than 90 degrees, so this is an acute triangle.",
          M("k1", "Acute", "box"), ANSR("a", answer, ring, True)),
        B("Check the angles: %d plus %d plus %d is 180." % (a, b, t),
          W("c", "%d + %d + %d = 180" % (a, b, t))),
        trap,
        B("So: find the third angle from 180, then compare all three angles with 90."),
    )


LESSONS[A + "1f04f2bb-4e87-42ce-9fd7-e8c15ddf73ea"] = third_and_kind(
    A + "1f04", 55, 70,
    "Riya has a triangle shaped tile. Two of its angles are 55 degrees and 70 degrees. We want the third angle, and the kind of triangle it is.",
    "Angles 55° and 70°. Third angle? Kind of triangle?",
    "Third angle 55°: an acute triangle", "acute triangle",
    B("Notice that the third angle came out as 55, the same as one we were given. That is fine. And one angle over 90 would have been enough to make it obtuse, so always look at all three."))

LESSONS[A + "2d8106ce-086a-4ba1-a8ae-c35ec1451036"] = third_and_kind(
    A + "2d81", 45, 65,
    "Vikram's flag is a triangle with angles of 45 degrees and 65 degrees. His friend Sanya says it has an obtuse angle, so it is an obtuse triangle. Is she right? Let's find out.",
    "Angles 45° and 65°. Kind of triangle?",
    "Acute triangle", "Acute triangle",
    B("So Sanya was a little too quick. Obtuse means more than 90 degrees, and our biggest angle is only 70. Always work out the third angle before you decide."))

LESSONS[A + "9460cd3a-01c7-4798-9beb-066c669f03c8"] = third_and_kind(
    A + "9460", 55, 75,
    "Farhan draws a triangle. Two of its angles are 55 degrees and 75 degrees. His teacher asks for the third angle, and the kind of triangle it is.",
    "Angles 55° and 75°. Third angle? Kind of triangle?",
    "Third angle 50°: an acute triangle", "acute triangle",
    B("The trap is to stop at 130. That is the two given angles added together, not the third angle. And 130 would have made the triangle look obtuse."))

LESSONS[A + "9b4803d2-885c-4ff2-a575-f8e11a861684"] = third_and_kind(
    A + "9b48", 60, 70,
    "Ravi has a paper triangle. He measures two of its angles: 60 degrees and 70 degrees. What kind of triangle is it, going by its angles?",
    "Angles 60° and 70°. Kind of triangle?",
    "Acute-angled triangle", "Acute-angled triangle",
    B("With only two angles you cannot be sure. The hidden third angle might have been the big one! That is why we found it first."))

# ── Farhan's stand: all three angles given ───────────────────────────────────

LESSONS[A + "4e7b0c83-7daa-4e72-8385-1128b745b155"] = lesson(
    B("Farhan's triangle has angles of 50, 60 and 70 degrees. We want to name it by its angles.",
      GIVEN("q", "Angles 50°, 60°, 70°. Kind of triangle?"), FIG("f1", TRI("scalene", ["60°", "50°", "70°"]))),
    B("First, a quick check that these really make a triangle. The three angles must add up to 180 degrees. 50 plus 60 plus 70 is 180. Good.",
      rule_ops(), W("w1", "50 + 60 + 70 = 180")),
    B("To name a triangle by its angles, we compare each angle with 90 degrees. " + KINDS_SAY, kind_ops()),
    B("So look at 50, 60 and 70. Is any of them 90 degrees or more?",
      ask=choose(["Yes, one of them", "No, all are less than 90°"], 1,
                 "Compare each angle with 90, one at a time: 50, then 60, then 70. Is any of them as big as 90?")),
    B("None. 50 is less than 90. 60 is less than 90. 70 is less than 90.",
      W("w2", "50 < 90"), W("w3", "60 < 90"), W("w4", "70 < 90")),
    B("All three angles are acute, so this is an acute angled triangle.",
      M("k1", "Acute", "box"), ANSR("a", "Acute-angled triangle", "Acute-angled triangle", True)),
    B("One choice says equilateral. An equilateral triangle has three equal angles, sharing 180 degrees. How big would each one be?",
      ask=choose(["90°", "60°", "45°"], 1,
                 "Three equal angles share 180 degrees. So split 180 into 3 equal parts.")),
    B("60 degrees each. Our angles are 50, 60 and 70. Only one of them is 60, so the triangle is not equilateral.",
      W("w5", "180 ÷ 3 = 60")),
    B("So to name a triangle by its angles, hold every angle up against 90. All three must be smaller for it to be acute."),
)

# ── Pooja's rangoli: 50°, twice that, and the third ──────────────────────────

LESSONS[A + "5c40eab7-a96f-4251-ba88-7228edeee2ee"] = lesson(
    B("Pooja's triangle has one angle of 50 degrees. Another angle is exactly twice that. We want the third angle, and the kind of triangle.",
      GIVEN("q", "Angles: 50°, twice 50°, and ?")),
    B("Start with the second angle. Twice means 2 times. 2 times 50 is 100.",
      W("w1", "2 × 50 = 100"), N("w1", "100", "second angle")),
    B("Now the rule for every triangle: the three angles add up to 180 degrees.", rule_ops()),
    B("Which sum gives the third angle?",
      ask=choose(["180 − 50", "180 − 50 − 100", "180 − 100"], 1,
                 "Both of the angles we know have to come off the 180: the 50, and the 100 as well.")),
    B("50 plus 100 is 150. And 180 minus 150 is 30. So the third angle is 30 degrees.",
      W("w2", "50 + 100 = 150"), W("w3", "180 − 150 = 30"), FIG("f1", TRI("scalene", ["100°", "50°", "30°"]))),
    B("The angles are 50, 100 and 30. Here are the three kinds of triangle. Look at our biggest angle. Which kind is this?",
      L("an", "Angles: 50°, 100°, 30°"), M("an", "100°"), kind_ops(),
      ask=choose(["acute", "right", "obtuse"], 2,
                 "Acute needs all three angles to be less than 90. Right needs one of exactly 90. Here one angle is 100, which is more than 90.")),
    B("Obtuse. One angle of more than 90 degrees is all it takes.",
      M("k3", "Obtuse", "box"), ANSR("a", "Obtuse triangle; third angle 30°", "30°", True)),
    B("Check: 50 plus 100 plus 30 is 180.",
      W("c", "50 + 100 + 30 = 180")),
    B("The trap is to forget the doubling. Taking 50 and 50 from 180 leaves 80, and that is one of the choices, waiting.",
      W("t", "180 − 50 − 50 = 80"), S("t", "180 − 50 − 50 = 80", "forgot to double")),
    B("So: work out every angle the story describes, find the last one from 180, then compare the biggest with 90."),
)

# ── Ananya's mosaic: acute and scalene ───────────────────────────────────────

LESSONS[A + "5e6fe38d-c05d-4e47-a529-38d1a76c14a3"] = lesson(
    B("Ananya's triangle has three sides of different lengths. Two of its angles are 48 degrees and 67 degrees. We must name it two ways: by its angles and by its sides.",
      GIVEN("q", "Angles 48° and 67°. All three sides different."), FIG("f1", TRI("scalene", ["?", "48°", "67°"]))),
    B("Angles first. We need all three, and the three angles of a triangle add up to 180 degrees. 48 plus 67 is 115.",
      rule_ops(), W("w1", "48 + 67 = 115")),
    B("Which sum gives the third angle?",
      ask=choose(["180 − 115", "115 − 90", "180 + 115"], 0,
                 "The three angles share 180 degrees. Two of them use up 115, so the third is what is left over.")),
    B("180 minus 115 is 65. So the angles are 48, 67 and 65.",
      W("w2", "180 − 115 = 65"), L("an", "Angles: 48°, 67°, 65°")),
    B("Compare each with 90 degrees. All three are less than 90. So by its angles, the triangle is acute angled.",
      L("k1", "All angles less than 90°: acute-angled")),
    B("Now the sides. All three are different lengths. What do we call a triangle like that?",
      ask=choose(["isosceles", "equilateral", "scalene"], 2,
                 "Equilateral means all three sides are equal, and isosceles means two are equal. When no two sides match, there is a third name.")),
    B("Scalene. No two sides are the same.",
      L("k2", "No two sides equal: scalene")),
    B("Put the two names together: an acute angled scalene triangle.",
      ANSR("a", "Acute-angled scalene triangle", "Acute-angled scalene triangle", True)),
    B("Check the angles: 48 plus 67 plus 65 is 180. And see how all three angles are different too. That always goes with three different sides.",
      W("c", "48 + 67 + 65 = 180")),
    B("Two names need two tests. Angles are tested against 90 degrees. Sides are tested against each other."),
)

# ── Sanjay's frame: obtuse and scalene ───────────────────────────────────────

LESSONS[A + "5293d35a-c128-4d52-9663-bf562ad3b78f"] = lesson(
    B("Sanjay's triangle has sides of 8, 15 and 10 centimetres. Its largest angle is 108 degrees and its smallest is 27 degrees. We want the third angle, and the full name of the triangle.",
      GIVEN("q", "Sides 8 cm, 15 cm, 10 cm. Angles 108°, 27°, ?")),
    B("Start with the missing angle. The three angles of a triangle add up to 180 degrees. 108 plus 27 is 135.",
      L("r", RULE), M("r", "180°", "box"), W("w1", "108 + 27 = 135")),
    B("So the third angle is 180 minus 135. What is that?",
      ask=choose(["55", "45", "35"], 1,
                 "Count on from 135 up to 180. First go up to the next ten, then count the tens.")),
    B("45. The third angle is 45 degrees.",
      W("w2", "180 − 135 = 45"), L("an", "Angles: 108°, 27°, 45°")),
    B("Now name it by its angles. Here are the three kinds. Look at our biggest angle, 108. Which kind is this?",
      M("an", "108°"), kind_ops(),
      ask=choose(["acute-angled", "right-angled", "obtuse-angled"], 2,
                 "Acute needs all three angles under 90, and right needs one of exactly 90. Here 108 is more than 90, and one such angle is enough.")),
    B("Obtuse angled, because 108 is more than 90.",
      M("k3", "Obtuse", "box")),
    B("Now the sides: 8, 15 and 10. No two are the same, so the triangle is scalene. Isosceles would need two equal sides.",
      M("q", "8 cm, 15 cm, 10 cm"), L("s1", "No two sides equal: scalene")),
    B("So it is an obtuse angled scalene triangle, and the third angle is 45 degrees.",
      ANSR("a", "Obtuse-angled scalene; third angle 45°", "45°", True)),
    B("Check: 108 plus 27 plus 45 is 180.",
      W("c", "108 + 27 + 45 = 180")),
    B("Three things to get right here, so take them one at a time: the missing angle from 180, the angles against 90, and the sides against each other."),
)

# ── Sanya's flag: 60°, 60° and the third ─────────────────────────────────────

LESSONS[A + "625e57c9-413c-4a89-a07c-74a9225bda2d"] = lesson(
    B("Sanya's triangle has two angles of 60 degrees each. We want the third angle, and the name of the triangle.",
      GIVEN("q", "Angles 60° and 60°. Third angle? Kind of triangle?"), FIG("f1", TRI("equilateral", ["?", "60°", "60°"]))),
    B("The rule for every triangle: its three angles add up to 180 degrees.", rule_ops()),
    B("Add the two we know. 60 plus 60 is 120.",
      W("w1", "60 + 60 = 120")),
    B("So what is the third angle?",
      ask=choose(["120°", "80°", "60°"], 2,
                 "120 is the two known angles added together. The third angle is what is left when we take 120 away from 180.")),
    B("180 minus 120 is 60. The third angle is 60 degrees as well.",
      W("w2", "180 − 120 = 60")),
    B("Look at that. All three angles are 60 degrees. And when all three angles are equal, all three sides are equal too.",
      L("an", "Angles: 60°, 60°, 60°")),
    B("What do we call a triangle with all three sides equal?",
      ask=choose(["isosceles", "equilateral", "scalene"], 1,
                 "Isosceles means just two equal sides. Here all three match. The name we want begins with equi, which means equal.")),
    B("Equilateral. So the third angle is 60 degrees, and the triangle is equilateral.",
      ANSR("a", "Third angle 60°: equilateral triangle", "equilateral triangle", True)),
    B("Check: 60 plus 60 plus 60 is 180.",
      W("c", "60 + 60 + 60 = 180")),
    B("One choice says isosceles. Two equal angles would make it isosceles, but here the third one matches as well. So find the third angle before you choose a name."),
)

# ── Priya's patch: two equal sides and the angle between them ────────────────

LESSONS[A + "7597470a-e967-4738-98ee-69f2f4eedead"] = lesson(
    B("Priya's triangle has two sides of 5 centimetres each, and the angle between those two sides is 80 degrees. We want the other two angles.",
      GIVEN("q", "Two sides 5 cm and 5 cm. Angle between them 80°."),
      FIG("f1", TRI("isosceles", {"a": "80°", "b": "?", "c": "?"}, {"ab": "5 cm", "ca": "5 cm"}))),
    B("Two equal sides make this an isosceles triangle. And an isosceles triangle has a secret: the two angles facing the equal sides are equal too.",
      L("r1", "Isosceles: two equal sides, two equal angles")),
    B("Next, the rule for every triangle: the three angles add up to 180 degrees.",
      L("r", RULE), M("r", "180°", "box")),
    B("The angle at the top uses 80 of those degrees. How many are left for the other two angles together?",
      ask=choose(["80", "100", "260"], 1,
                 "The three angles share 180 degrees. Take away the 80 at the top to see what is left.")),
    B("180 minus 80 is 100. The other two angles share 100 degrees.",
      W("w1", "180 − 80 = 100")),
    B("And those two angles are equal. So how big is each one?",
      ask=choose(["40°", "100°", "50°"], 2,
                 "Two equal angles make 100 degrees together. So split 100 into 2 equal parts.")),
    B("100 divided by 2 is 50. Each of the other angles is 50 degrees.",
      W("w2", "100 ÷ 2 = 50"), ANSR("a", "50° and 50°", "50° and 50°", True)),
    B("Check: 80 plus 50 plus 50 is 180.",
      W("c", "80 + 50 + 50 = 180")),
    B("The trap is to halve the 80 and say 40 and 40. It is the leftover 100 that gets shared, not the angle we were given."),
    B("So for an isosceles triangle: take the angle you know from 180, then share what is left equally."),
)

# ── Priya's garden bed: 5 m, 7 m, 5 m and 84° ────────────────────────────────

LESSONS[A + "28e0cae9-e12e-4b24-9d39-8b2cac17a1ee"] = lesson(
    B("Priya's garden bed is a triangle with sides of 5, 7 and 5 metres. The angle between the two equal sides is 84 degrees. We want the kind of triangle, and the other two angles.",
      GIVEN("q", "Sides 5 m, 7 m, 5 m. Angle between equal sides 84°."),
      FIG("f1", TRI("isosceles", {"a": "84°", "b": "?", "c": "?"}, {"ab": "5 m", "ca": "5 m", "bc": "7 m"}))),
    B("Start with the sides: 5, 7 and 5. What kind of triangle is it?",
      ask=choose(["scalene", "isosceles", "equilateral"], 1,
                 "Scalene means no two sides match, and equilateral means all three match. Here exactly two sides are 5 metres.")),
    B("Isosceles: exactly two equal sides. And here is its secret. The two angles facing the equal sides are equal too.",
      L("r1", "Isosceles: two equal sides, two equal angles")),
    B("Now the angles. All three add up to 180 degrees, and the top one is 84. So 180 minus 84, which is 96, is left for the other two.",
      L("r", RULE), W("w1", "180 − 84 = 96")),
    B("Those two angles are equal. So how big is each one?",
      ask=choose(["42°", "96°", "48°"], 2,
                 "It is the leftover 96 that the two angles share, not the 84. Split 96 into 2 equal parts.")),
    B("96 divided by 2 is 48. Each of the other two angles is 48 degrees.",
      W("w2", "96 ÷ 2 = 48")),
    B("So it is an isosceles triangle, and each of the other two angles is 48 degrees.",
      ANSR("a", "Isosceles; the other two angles 48° each", "48°", True)),
    B("Check: 84 plus 48 plus 48 is 180.",
      W("c", "84 + 48 + 48 = 180")),
    B("The trap is to halve the 84 and get 42. Halve what is left over, not what you were given."),
)


# ── Angles described in terms of one another ─────────────────────────────────

def in_terms_of_x(qid, name, intro, given, use_check, ending):
    """Angles x, 3x and x + 20. name: what x stands for ('second' or 'smallest')."""
    def EQ(id, text):
        return W(id, text, None, not use_check)
    beats = [
        B(intro, GIVEN("q", given)),
        B("Every angle here is described using the %s angle. So let's give that one a name: x." % name,
          L("d1", "%s angle = x" % name), L("d2", "3 times it = 3x"), L("d3", "20° more than it = x + 20")),
        B("We have three angles, all written with x. What do we know about the three angles of any triangle?",
          ask=choose(["they are all equal", "they add up to 180°", "they add up to 360°"], 1,
                     "360 degrees is a full turn. The three angles of a triangle make a half turn between them.")),
        B("They add up to 180 degrees. So we add our three angles and set the total equal to 180.",
          EQ("e1", "x + 3x + x + 20 = 180"), G("e1", ["x", "3x", ("x", 3)], "5x")),
        B("Gather the x terms. x and 3 x and x make 5 x. So 5 x, plus 20, equals 180.",
          EQ("e2", "5x + 20 = 180")),
        B("To undo plus 20, we take 20 away. And to keep the balance level, we take it from both sides. 180 minus 20 is 160.",
          S("e2", "+ 20", "− 20"), BOTH("e2", "− 20"), EQ("e3", "5x = 160")),
        B("5 x means 5 times x. How do we undo times 5?",
          ask=choose(["subtract 5", "multiply by 5", "divide by 5"], 2,
                     "Times and divide are partners. Whatever times does, divide undoes.")),
        B("Divide both sides by 5. 160 divided by 5 is 32. So x is 32.",
          DIV("e3", "5"), W("w1", "160 ÷ 5 = 32"), EQ("e4", "x = 32")),
        B("Now build the three angles. The %s is 32. 3 times 32 is 96. And 32 plus 20 is 52." % name,
          W("w2", "3 × 32 = 96"), W("w3", "32 + 20 = 52")),
        B("Check that they make a triangle: 32 plus 96 plus 52 is 180. They do.",
          W("c", "32 + 96 + 52 = 180"), FIG("f1", TRI("scalene", ["96°", "32°", "52°"]))),
    ] + ending
    if use_check:
        return lesson(*beats, check=("x", 32))
    return lesson(*beats)


LESSONS[A + "09382572-179c-40c1-a137-3308a7a1d8d4"] = in_terms_of_x(
    A + "0938", "second",
    "Rahul cuts out a triangle. The first angle is 3 times the second. The third is 20 degrees more than the second. We must name the triangle by its angles, so first we need the angles.",
    "First = 3 × second. Third = second + 20°. Kind?",
    True,
    [B("Now name it. The biggest angle is 96 degrees, and that is more than 90. One angle over 90 makes the triangle obtuse angled.",
       ANSR("a", "96° is more than 90°: obtuse-angled triangle", "obtuse-angled triangle", True)),
     B("The trap is to stop at x equals 32, see a small angle, and say acute. Find all three angles before you name the triangle."),
     B("So: call one angle x, write the others with x, make them add up to 180, and solve.")])

LESSONS[A + "3a216919-51a0-4f8b-a087-88b3a93ee342"] = in_terms_of_x(
    A + "3a21", "smallest",
    "A triangular frame. One angle is 3 times the smallest angle. The third is 20 degrees more than the smallest. We want the largest angle.",
    "Angles: smallest, 3 × smallest, smallest + 20°",
    False,
    [B("The question asks for the largest angle. The three are 32, 96 and 52, so the largest is 96 degrees.",
       ANSR("a", "Largest angle = 96°", "96°", True)),
     B("The trap is to stop at x. 32 is the smallest angle, and 52 is the middle one. Read the question again before you pick."),
     B("So: call one angle x, write the others with x, make them add up to 180, and solve.")])
