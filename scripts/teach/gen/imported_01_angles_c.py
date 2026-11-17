"""Angles: one angle is so many times the angle next to it (ten questions, two methods)."""
from imported_01_lib import AI, ANS, B, DIV, FIG, G, GIVEN, M, W, choose, half_lines, lesson, num, placed

LESSONS = {}

ASK_180 = [
    ("The two angles are next to each other on a straight line. So together, what do they make?",
     "Follow one of the lines through the crossing. The two angles sit on it side by side, and a straight line is 180 degrees."),
    ("Start with what we know for sure. Two angles side by side on a straight line add up to how much?",
     "A straight line is half of a full turn. A full turn is 360 degrees, so the two angles share 180 degrees."),
    ("Before any sums, one fact. What do next-door angles on a straight line add up to?",
     "Two square corners of 90 degrees fit side by side on a straight line. So next-door angles on a line make 180 degrees."),
]

TRAP_PARTS = [
    "That is the trap in this question. It says %(k)d times, so it is tempting to divide by %(k)d. But the small angle needs a part of its own too.",
    "Notice it is not %(k)d parts. The big angle takes %(k)d of them, and the small angle takes 1 more.",
]


def parts_core(qid, k, v):
    """The shared middle: straight line, equal parts, one part, the big angle. Returns (beats, small, big)."""
    n = k + 1
    small = 180 // n
    big = k * small
    ask_say, ask_miss = ASK_180[v % 3]
    line_choices, line_right = placed(qid, "line", "180°", ["90°", "360°"])
    part_choices, part_right = placed(qid, "parts", "%d parts" % n, ["%d parts" % k, "%d parts" % (n + 1)])
    bar = [{"units": 1, "label": "small", "tone": "a"}] + [{"units": 1, "label": "big", "tone": "b"} for _ in range(k)]
    if k == 3:
        share_say = ["So 4 equal parts share 180 degrees. Dividing by 4 is halving twice: half of 180 is 90, and half of 90 is 45.",
                     "So 180 degrees is shared among 4 equal parts. Halve 180 to get 90, then halve again to get 45. That is one part."][v % 2]
        share_ops = [W("p1", "1 + 3 = 4"), W("p2", "180 ÷ 2 = 90"), W("p3", "90 ÷ 2 = 45"), W("p4", "180 ÷ 4 = 45"), M("p4", "45")]
    else:
        share_say = "So 3 equal parts share 180 degrees. 18 divided by 3 is 6, so 180 divided by 3 is 60."
        share_ops = [W("p1", "1 + 2 = 3"), W("p2", "18 ÷ 3 = 6"), W("p4", "180 ÷ 3 = 60"), M("p4", "60")]
    beats = [
        B(ask_say, ask=choose(line_choices, line_right, ask_miss)),
        B(["We don't know either angle yet. But one is %d times the other. So picture equal parts: the small angle is 1 part, and the big angle is %d parts." % (k, k),
           "Neither angle is given, only how they compare. So let's use equal parts. Call the small angle 1 part. Then the big angle is %d parts." % k][v % 2],
          W("parts", "small angle = 1 part,  big angle = %d parts" % k, label=True),
          FIG("bar", kind="barModel", bars=[{"segments": bar, "brace": "180°"}])),
        B("Look at the bar. How many equal parts fill the whole 180 degrees?",
          ask=choose(part_choices, part_right,
                     "Count both angles. The small one is 1 part and the big one is %d parts. 1 plus %d makes %d parts." % (k, k, n))),
        B(TRAP_PARTS[(v // 2) % 2] % {"k": k}),
        B(share_say, share_ops),
        B("One part is %d degrees, so that is the small angle. The big angle is %d parts: %d times %d is %d." % (small, k, k, small, big),
          W("big", "%d × %d = %d" % (k, small, big)),
          FIG("f2", kind="angles", layout="onLine",
              parts=[{"label": "%d°" % small, "size": small}, {"label": "%d°" % big, "size": big}])),
    ]
    return beats, small, big


def opening(say, given, k):
    return B(say, GIVEN("l1", given),
             FIG("f1", kind="angles", layout="onLine", parts=[{"label": "small"}, {"label": "%d times as big" % k}]))


CHECK = [
    "Check. %(s)d plus %(b)d is 180, a straight line. And %(b)d really is %(k)d times %(s)d.",
    "Does it fit the story? %(s)d and %(b)d make 180 together, and the big one is %(k)d lots of the small one.",
]
SUMMARY = [
    "When one angle is so many times another, count the equal parts, share out the 180 degrees, and then build the angle you were asked for.",
    "So: straight line means 180. Count the parts, find one part, and read the question again to see which angle it wants.",
]


def check_beat(v, small, big, k):
    return B(CHECK[v % 2] % {"s": small, "b": big, "k": k}, W("chk", "%d + %d = 180" % (small, big)))


def smaller(qid, say, given, v):
    core, small, big = parts_core(qid, 3, v)
    return lesson(
        opening(say, given, 3), core,
        B("The question asks for the smaller angle, and that is the single part: %d degrees." % small,
          ANS("ans", "Smaller angle = %d°" % small, True), M("ans", "%d°" % small, "circle")),
        B(["Don't be tempted by %d. It is a real angle at this crossing, but it is the larger one." % big,
           "You will see %d among the choices. It is the big angle, and we were asked for the small one." % big][v % 2]),
        check_beat(v, small, big, 3),
        B(SUMMARY[v % 2]),
    )


LESSONS[AI + "33b0f63c-6058-4389-b8f7-7e5634b6278b"] = smaller(
    AI + "33b0f63c-6058-4389-b8f7-7e5634b6278b",
    "Two straight roads cross near the stadium. One angle at the crossing is 3 times the angle next to it on the same straight line. We want the smaller angle.",
    "One angle = 3 × the angle next to it. Smaller = ?", 0)

LESSONS[AI + "52dd3f2c-80e8-4374-ae63-f9ea8b27d64b"] = smaller(
    AI + "52dd3f2c-80e8-4374-ae63-f9ea8b27d64b",
    "Ankit's two tent poles cross at P. One of the angles is 3 times the angle next to it, and we want the smaller one.",
    "Poles cross at P. One angle = 3 × the next. Smaller = ?", 3)

_core, _s, _b = parts_core(AI + "2def0f90-4ce7-434e-aab2-37232943d8ba", 3, 1)
LESSONS[AI + "2def0f90-4ce7-434e-aab2-37232943d8ba"] = lesson(
    opening("Ravi's two rangoli lines cross. One angle is 3 times as large as the angle next to it, and this time we want the larger one.",
            "One angle = 3 × the angle next to it. Larger = ?", 3),
    _core,
    B("We were asked for the larger angle, so the answer is the 3 parts: 135 degrees.",
      ANS("ans", "Larger angle = 135°", True), M("ans", "135°", "circle")),
    B("Stopping at 45 is the easy slip here. That is one part, the smaller angle. Read the last line of the question before you choose."),
    check_beat(1, _s, _b, 3),
    B(SUMMARY[0]),
)

_core, _s, _b = parts_core(AI + "19d857d5-076b-4db9-8cf1-e1f9fb2d4502", 3, 2)
LESSONS[AI + "19d857d5-076b-4db9-8cf1-e1f9fb2d4502"] = lesson(
    opening("Two kite strings cross in the air. At the crossing, one angle is 3 times the angle next to it. We want all four angles.",
            "Two strings cross. One angle = 3 × the next. All 4 = ?", 3),
    _core,
    B("Now the other two. Angles straight across a crossing are equal. So across from the 45 is another 45, and across from the 135 is another 135.",
      FIG("f3", kind="angles", layout="crossing",
          parts=[{"label": "45°", "size": 45}, {"label": "135°", "size": 135}, {"label": "45°", "size": 45}, {"label": "135°", "size": 135}])),
    B("So going round the crossing, the four angles are 45, 135, 45 and 135 degrees.",
      ANS("ans", "45°, 135°, 45°, 135°", True), M("ans", "45°, 135°, 45°, 135°", "circle")),
    B("Careful: in every choice the pairs add up to 180, so that test alone is not enough. The big angle must also be 3 times the small one."),
    B("Check with a full turn. All four angles together should make 360 degrees, and they do.",
      W("chk", "45 + 135 + 45 + 135 = 360")),
    B("At any crossing: next-door angles make 180, and opposite angles are equal. Find two angles and you have all four."),
)


def halve_larger(qid, say, given, v):
    core, small, big = parts_core(qid, 3, v)
    ops, words, half = half_lines("h", big)
    hs = num(half)
    return lesson(
        opening(say, given, 3), core,
        B(["Now the third line. It cuts the larger angle, the %d, into two equal halves. So we halve %d." % (big, big),
           "We are not finished. The third line splits the largest angle, %d degrees, into two equal parts. So we need half of %d." % (big, big)][v % 2]),
        B(words, ops),
        B("Each part is %s degrees." % hs, ANS("ans", "Each part = %s°" % hs, True), M("ans", "%s°" % hs, "circle")),
        B("There are two tempting places to stop on the way: %d and %d. Both are real angles here, but the question wants half of the larger one." % (small, big)),
        B("Check. %s plus %s is %d, and %d plus %d is 180." % (hs, hs, big, small, big),
          W("c1", "%s + %s = %d" % (hs, hs, big)), W("c2", "%d + %d = 180" % (small, big))),
        B("Three steps, in order: share out the 180 degrees in parts, build the larger angle, then cut it in half."),
    )


LESSONS[AI + "1984a5bf-7467-488c-bc74-9691aa369e86"] = halve_larger(
    AI + "1984a5bf-7467-488c-bc74-9691aa369e86",
    "Riya's two lines cross, and one angle is 3 times the angle next to it. Then a third line cuts the larger angle exactly in half. We want one of those halves.",
    "One angle = 3 × the angle next to it. Half of larger = ?", 0)

LESSONS[AI + "e2b4be33-589a-4848-ad94-d70b34a2725e"] = halve_larger(
    AI + "e2b4be33-589a-4848-ad94-d70b34a2725e",
    "Two lines cross at P, and one angle is 3 times the angle next to it. A third line then splits the largest angle into two equal parts. How big is each part?",
    "Lines cross at P. One angle = 3 × the next. Half of largest?", 3)

_core, _s, _b = parts_core(AI + "d68deb3e-35d9-4203-83cd-271944ff33c9", 3, 1)
LESSONS[AI + "d68deb3e-35d9-4203-83cd-271944ff33c9"] = lesson(
    opening("This one has two parts. First, a crossing where one angle is 3 times the angle next to it. Then a triangle that borrows the smaller of those angles, and has another angle of 50 degrees.",
            "Crossing: one angle = 3 × the next. Triangle: small, 50°, ?", 3),
    _core,
    B("Now the triangle. One of its angles equals the smaller crossing angle, 45 degrees. Another is 50 degrees. We want the third.",
      W("t1", "Triangle: 45°, 50°, ?", label=True),
      FIG("f3", kind="triangle", shape="scalene", angles={"a": "?", "b": "45°", "c": "50°"})),
    B("The three angles of any triangle add up to 180 degrees. 45 plus 50 is 95, and 180 minus 95 is 85.",
      W("t2", "45 + 50 = 95"), W("t3", "180 − 95 = 85")),
    B("So the third angle of the triangle is 85 degrees.", ANS("ans", "Third angle = 85°", True), M("ans", "85°", "circle")),
    B("Careful to use the smaller angle, 45. With 135 the triangle could not even close: 135 and 50 together are already more than 180."),
    B("Check the triangle: 45 plus 50 plus 85 makes 180.", W("chk", "45 + 50 + 85 = 180")),
    B("Two facts did all the work, and both are about 180. Angles on a straight line make 180, and so do the angles of a triangle."),
)

_core, _s, _b = parts_core(AI + "e5c10ca9-1d56-4647-8cb7-43622e0856fb", 2, 0)
LESSONS[AI + "e5c10ca9-1d56-4647-8cb7-43622e0856fb"] = lesson(
    opening("Kavya's paper strip is a straight line with two angles on one side. The first angle is twice the second. We want the angle vertically opposite the smaller one.",
            "On a line: first angle = 2 × second. Opposite smaller = ?", 2),
    _core,
    B("Now look across the crossing from the small angle. Angles straight across from each other are called vertically opposite, and they are always equal.",
      FIG("f3", kind="angles", layout="crossing", highlight=["p2"],
          parts=[{"label": "60°", "size": 60}, {"label": "120°", "size": 120}, {"label": "?"}, {"label": "120°", "size": 120}])),
    B("So the angle vertically opposite the 60 is also 60 degrees.",
      ANS("ans", "Vertically opposite angle = 60°", True), M("ans", "60°", "circle")),
    B("Careful not to pick 120. That is the angle next door to the small one, not the one across from it."),
    check_beat(0, _s, _b, 2),
    B("Share the 180 degrees in equal parts to find the angles on the line. Then remember: opposite angles at a crossing are equal."),
)


# ── The same question solved with a letter ───────────────────────────────────

def smaller_with_x(qid, say, given, v):
    ask_say, ask_miss = ASK_180[(v + 1) % 3]
    line_choices, line_right = placed(qid, "line", "180°", ["90°", "360°"])
    x_choices, x_right = placed(qid, "xs", "4x", ["3x", "5x"])
    return lesson(
        B(say, GIVEN("l1", given),
          FIG("f1", kind="angles", layout="onLine", parts=[{"label": "x"}, {"label": "3x"}])),
        B(["We don't know the small angle, so let's give it a name: x. The angle next to it is 3 times as big, so it is 3 x.",
           "Let's call the smaller angle x. Then the one next to it, 3 times as large, is 3 x."][v % 2],
          W("names", "small angle = x,  big angle = 3x", label=True)),
        B(ask_say, ask=choose(line_choices, line_right, ask_miss)),
        B("So x plus 3 x equals 180. That is our equation.", W("eq", "x + 3x = 180")),
        B("Now gather the x's. x plus 3 x: how many x is that altogether?",
          ask=choose(x_choices, x_right, "An x on its own counts as 1 x. So 1 x and 3 x together make 4 x.")),
        B("Careful: that lonely x is easy to forget. Counting it, we have 4 x, and 4 x equals 180.",
          G("eq", ["x", "3x"], "4x"), W("e2", "4x = 180")),
        B("4 x means 4 times x. To undo times 4, we divide both sides by 4. Half of 180 is 90, and half of 90 is 45.",
          DIV("e2", "4"), W("d1", "180 ÷ 2 = 90"), W("d2", "90 ÷ 2 = 45")),
        B("So x is 45. The smaller angle is 45 degrees.",
          ANS("ans", "Smaller angle: x = 45°", True), M("ans", "45°", "circle")),
        B("The bigger angle is 3 times 45, which is 135. You will see it among the choices, but it is not the one we were asked for.",
          W("big", "3 × 45 = 135")),
        B("Check: 45 plus 135 is 180. The two angles lie along a straight line, just as they should.",
          W("chk", "45 + 135 = 180"),
          FIG("f2", kind="angles", layout="onLine", parts=[{"label": "45°", "size": 45}, {"label": "135°", "size": 135}])),
        B(["Give the unknown angle a letter, write down what the straight line tells you, and solve. Then answer the question that was asked.",
           "A letter for the small angle, 180 for the straight line, and one short equation. That is all this question needs."][v % 2]),
        check=("x", 45),
    )


LESSONS[AI + "46a665e2-2630-4980-8206-30d789cc97fd"] = smaller_with_x(
    AI + "46a665e2-2630-4980-8206-30d789cc97fd",
    "Meera's two lines cross at O. One angle is 3 times as large as the angle next to it. We are after the smaller angle.",
    "Lines cross at O. One angle = 3 × the next. Smaller = ?", 0)

LESSONS[AI + "cbcf98a0-0b99-4673-a484-5c0205dabff3"] = smaller_with_x(
    AI + "cbcf98a0-0b99-4673-a484-5c0205dabff3",
    "Arjun's kite sticks cross and make 4 angles. The first angle is 3 times the second, and the two sit next to each other on a straight line. We want the smaller angle.",
    "First angle = 3 × second, on a straight line. Smaller = ?", 1)
