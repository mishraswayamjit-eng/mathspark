"""Angles: a line that cuts an angle in half (four questions), and angles in a square corner (two)."""
from imported_01_lib import (AI, ANS, B, FIG, GIVEN, M, W, choose, count_up_lines, half_lines, lesson, num, placed,
                             take_away_lines)

LESSONS = {}


# ── Find the angle next door, then halve it ──────────────────────────────────

def halve_next_door(qid, a, opening, v):
    b = 180 - a
    line_choices, line_right = placed(qid, "line", "180°", ["90°", "360°"])
    if v == 0:
        sub_ops, sub_words = take_away_lines("s", 180, a)
        sub_words = "So the angle next door is 180 minus %d. %s" % (a, sub_words)
    else:
        sub_ops, sub_words = count_up_lines("s", 180, a)
        sub_words = "So the angle next door is whatever takes %d up to 180. %s" % (a, sub_words)
    half_ops, half_words, half = half_lines("h", b)
    hs = num(half)
    cut_choices, cut_right = placed(qid, "cut", "%d ÷ 2" % b, ["%d ÷ 2" % a, "%d × 2" % b])
    return lesson(
        B(opening, GIVEN("l1", "One angle = %d°. The angle next to it is cut in half." % a),
          FIG("f1", kind="angles", layout="onLine", parts=[{"label": "%d°" % a, "size": a}, {"label": "cut in half"}])),
        B(["There are two jobs here. First find the angle next to the %d degrees. Then cut it in half." % a,
           "Notice that the third line does not touch the %d degrees. So first we need the angle next to it, and then we halve that." % a][v],
          W("plan", "1. Find the angle next door.  2. Halve it.", label=True)),
        B("Job one. The %d degrees and the angle next to it sit together on a straight line. What do they add up to?" % a,
          ask=choose(line_choices, line_right,
                     "A straight line is a half turn, and a half turn is 180 degrees. So the two angles next to each other share 180 degrees.")),
        B(sub_words, sub_ops),
        B("Job two. The third line cuts this %d degree angle into two equal parts. Which sum gives each part?" % b,
          ask=choose(cut_choices, cut_right,
                     "The line cuts the angle next door, the %d degrees, not the %d degrees we started with. And two equal parts means dividing by 2." % (b, a))),
        B(half_words, half_ops),
        B("So each part is %s degrees." % hs, ANS("ans", "Each part = %s°" % hs, True), M("ans", "%s°" % hs, "circle")),
        B(["Two traps here. Stopping at %d gives the angle before it was cut. And halving the %d halves the angle we were given, not the one next to it." % (b, a),
           "Watch for two slips. One is to halve the %d we were given. The other is to stop at %d and forget the cutting." % (a, b)][v]),
        B("Check. %s plus %s is %d, and %d plus %d is 180. Everything fits on the straight line." % (hs, hs, b, b, a),
          W("c1", "%s + %s = %d" % (hs, hs, b)), W("c2", "%d + %d = 180" % (b, a)),
          FIG("f2", kind="angles", layout="onLine",
              parts=[{"label": "%d°" % a, "size": a}, {"label": "%s°" % hs, "size": half}, {"label": "%s°" % hs, "size": half}])),
        B(["When a question has two jobs, do them in order: find the angle, then cut it. And always read which angle is being cut.",
           "So: straight line first, to get the angle next door. Then halve it. Two small steps, in the right order."][v]),
    )


LESSONS[AI + "00efe1c8-40bf-4888-99b3-39621734633c"] = halve_next_door(
    AI + "00efe1c8-40bf-4888-99b3-39621734633c", 72,
    "Riya's two rangoli lines cross, and one angle is 72 degrees. A third line then splits the angle next to it into two equal parts. How big is each part?", 0)

LESSONS[AI + "8f3d128d-d012-4a02-9f8e-2662491e28dc"] = halve_next_door(
    AI + "8f3d128d-d012-4a02-9f8e-2662491e28dc", 65,
    "Two lines cross in Riya's rangoli, and one angle is 65 degrees. Then a third line splits the angle next to the 65 into two equal parts. We want the size of each part.", 1)


# ── The opposite angle, then halve it ────────────────────────────────────────

def halve_opposite(qid, a, opening, v):
    b = 180 - a
    half_ops, half_words, half = half_lines("h", a)
    hs = num(half)
    same_choices, same_right = placed(qid, "same", "It is also %d°" % a, ["It is 180° − %d°" % a, "It is 90° − %d°" % a])
    cut_choices, cut_right = placed(qid, "cut", "%d ÷ 2" % a, ["%d ÷ 2" % b, "%d × 2" % a])
    return lesson(
        B(opening, GIVEN("l1", "One angle = %d°. The opposite angle is cut in half." % a),
          FIG("f1", kind="angles", layout="crossing", highlight=["p2"],
              parts=[{"label": "%d°" % a, "size": a}, {"label": "next door"}, {"label": "opposite"}, {"label": "next door"}])),
        B(["Look at the angle straight across from the %d degrees. How does it compare?" % a,
           "Before any cutting, we need the size of the opposite angle. What is it?"][v],
          ask=choose(same_choices, same_right,
                     "Taking away from 180 gives the angle next door. The angle straight across is made by the same two lines, opened by the same amount. So it is equal.")),
        B("Here is why. The angle next door is 180 minus %d, which is %d. The opposite angle sits next to that %d on the other line, so it is 180 minus %d. Back to %d." % (a, b, b, b, a),
          W("w1", "180 − %d = %d" % (a, b)), W("w2", "180 − %d = %d" % (b, a))),
        B("Angles straight across a crossing are called vertically opposite angles, and they are always equal. So the opposite angle is %d degrees." % a,
          W("rule", "Vertically opposite angles are equal", label=True), M("rule", "equal", "box")),
        B("Now the third line cuts that %d degree angle into two equal parts. Which sum do we need?" % a,
          ask=choose(cut_choices, cut_right,
                     "The line cuts the opposite angle, which is %d degrees, not the %d next door. Two equal parts means dividing by 2." % (a, b))),
        B(half_words, half_ops),
        B("So each part is %s degrees." % hs, ANS("ans", "Each part = %s°" % hs, True), M("ans", "%s°" % hs, "circle")),
        B(["The slip to watch for is halving the %d, the angle next door. Always read which angle the new line cuts." % b,
           "Careful: the word opposite matters. Had the line cut the angle next door, we would be halving %d instead." % b][v]),
        B("Check: %s plus %s gives back %d." % (hs, hs, a), W("c1", "%s + %s = %d" % (hs, hs, a))),
        B(["Opposite angles at a crossing are equal. Next-door angles make 180. Pick the right fact first, then do the cutting.",
           "So ask yourself: across, or next door? Across means equal. Next door means the two make 180. Then halve."][v]),
    )


LESSONS[AI + "0bcee95c-177d-4b67-afaf-eb909069f2a6"] = halve_opposite(
    AI + "0bcee95c-177d-4b67-afaf-eb909069f2a6", 72,
    "Riya's two lines cross, and one angle is 72 degrees. This time the third line splits the angle opposite the 72 into two equal parts. What is each part?", 0)

LESSONS[AI + "d9ae9510-6956-426d-a701-2e0d19be1cf5"] = halve_opposite(
    AI + "d9ae9510-6956-426d-a701-2e0d19be1cf5", 65,
    "Priya's two lines cross at the centre, and one of the 4 angles is 65 degrees. A third line splits the angle directly opposite into two equal parts. We want each part.", 1)


# ── Angles that share a square corner ────────────────────────────────────────

_ops, _words = take_away_lines("s", 90, 53)
LESSONS[AI + "4783ddb3-7bc8-47dd-b969-3d922cac0d13"] = lesson(
    B("Arjun's kite string climbs from the ground at 53 degrees. A pole stands straight up beside it. We want the angle between the string and the pole.",
      GIVEN("l1", "String and ground = 53°. String and pole = ?")),
    B("First, forget the string. The ground is flat and the pole stands straight up. What angle do the ground and the pole make?",
      ask=choose(["180°", "90°", "45°"], 1,
                 "A pole standing straight up makes a square corner with flat ground, like the corner of a page. A square corner is 90 degrees.")),
    B("Now put the string back. It rises inside that square corner and splits it into two parts: 53 degrees below the string, and our missing angle above it.",
      FIG("f1", kind="angles", layout="inRightAngle", parts=[{"label": "53°", "size": 53}, {"label": "?"}]),
      W("l2", "53 + ? = 90")),
    B("So which sum gives the missing part?",
      ask=choose(["180 − 53", "90 + 53", "90 − 53"], 2,
                 "The two parts fill the square corner between the ground and the pole. That corner is 90 degrees, not a straight line. So we take 53 away from 90.")),
    B("90 minus 53. " + _words, _ops),
    B("So the string and the pole are 37 degrees apart.", ANS("ans", "String and pole = 37°", True), M("ans", "37°", "circle")),
    B("Careful with that last step. Taking 3 from 40 drops us below 40, into the thirties."),
    B("Check by adding the two parts. 53 plus 37 is 90, a perfect square corner.", W("chk", "53 + 37 = 90")),
    B("Two angles that fill a square corner add up to 90 degrees. Find the corner first, then subtract."),
)

_ops, _words = take_away_lines("s", 90, 55)
LESSONS[AI + "e3b7c930-6f05-43c4-9e7c-fe1cc7980313"] = lesson(
    B("Arjun's kite string makes 55 degrees with the ground. Priya says the angle with the upright line is complementary to 55. Arjun says supplementary. Let's find out who is right.",
      GIVEN("l1", "String and ground = 55°. String and upright line = ?")),
    B("Two words to sort out first. Complementary angles add up to 90 degrees. Supplementary angles add up to 180 degrees.",
      W("d1", "Complementary: add up to 90°", label=True), W("d2", "Supplementary: add up to 180°", label=True)),
    B("Now the picture. The ground is flat, and the line goes straight up. What angle is there between them?",
      ask=choose(["90°", "180°", "55°"], 0,
                 "Straight up from flat ground makes a square corner, like the corner of a book. And a square corner is 90 degrees.")),
    B("The string sits inside that square corner. So its angle with the ground and its angle with the upright line fill 90 degrees between them.",
      FIG("f1", kind="angles", layout="inRightAngle", parts=[{"label": "55°", "size": 55}, {"label": "?"}]),
      W("l2", "55 + ? = 90")),
    B("So whose word fits?",
      ask=choose(["Arjun: supplementary", "Priya: complementary"], 1,
                 "Supplementary is for two angles that make a straight line. These two share a square corner, 90 degrees. That is what complementary means.")),
    B("Priya's word fits, so we take 55 from 90. " + _words, _ops, M("d1", "Complementary", "box")),
    B("The string is 35 degrees away from the upright line.",
      ANS("ans", "String and upright line = 35°", True), M("ans", "35°", "circle")),
    B("Arjun's way takes 55 from 180 and gives a very wide angle. But the string leans between the ground and the upright line, so the angle has to be smaller than 90."),
    B("Check: 55 plus 35 is 90. The two angles fill the square corner exactly.", W("chk", "55 + 35 = 90")),
    B("A square corner means the two angles make 90. A straight line means they make 180. Decide which picture you have before you subtract."),
)
