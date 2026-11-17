"""Angles: complementary and supplementary pairs from the textbook (five questions)."""
from imported_01_lib import ANS, B, FIG, GIVEN, M, TB, W, choose, lesson, placed

LESSONS = {}

WORDS = {
    90: ("complementary", "inRightAngle",
         "Complementary angles fit together to make a square corner, and a square corner is 90 degrees. The pair that makes 180 has a different name: supplementary."),
    180: ("supplementary", "onLine",
          "Supplementary angles sit side by side on a straight line, and a straight line is 180 degrees. The pair that makes 90 is called complementary."),
}


# ── An angle with a half degree ──────────────────────────────────────────────

def with_a_half(qid, total, a, last_trap):
    """The partner of (a and a half) degrees in a pair that makes `total`."""
    word, layout, miss = WORDS[total]
    r = total - a          # after the whole degrees
    ans = r - 1            # the whole part of the answer
    choices, right = placed(qid, "total", "%d°" % total, ["%d°" % t for t in (90, 180, 360) if t != total])
    halves, half_right = placed(qid, "half", "%d½" % ans, ["%d½" % r, "%d" % ans])
    return lesson(
        B("We want the %s angle of %d and a half degrees. So first, what does %s mean?" % (word, a, word),
          GIVEN("l1", "%s angle of %d½° = ?" % (word.capitalize(), a))),
        B("Two angles are %s when they add up to how much?" % word, ask=choose(choices, right, miss)),
        B("So %d and a half, plus our missing angle, makes %d." % (a, total),
          W("l2", "%d½ + ? = %d" % (a, total)),
          FIG("f1", kind="angles", layout=layout, parts=[{"label": "%d½°" % a, "size": a + 0.5}, {"label": "?"}])),
        B("Let's subtract in two easy steps. First the whole degrees: %d minus %d is %d." % (total, a, r),
          W("l3", "%d − %d = %d" % (total, a, r))),
        B("But we still have to take away the extra half. What is %d minus a half?" % r,
          ask=choose(halves, half_right,
                     "Taking a half away makes the number smaller, so we drop below %d. Break one whole into two halves: that is %d and two halves. Take one half away and %d and a half is left." % (r, ans, ans))),
        B("Careful: this is where it slips. Stopping at %d forgets the half. One whole is two halves, so %d minus a half is %d and a half." % (r, r, ans),
          W("l4", "%d + 1/2 + 1/2 = %d" % (ans, r)), W("l5", "%d − ½ = %d½" % (r, ans), label=True)),
        B("So the %s angle is %d and a half degrees." % (word, ans),
          ANS("ans", "%s angle = %d½°" % (word.capitalize(), ans), True), M("ans", "%d½°" % ans, "circle")),
        B("Check by adding. The two halves make 1 whole. %d and %d make %d, and 1 more is %d." % (a, ans, a + ans, total),
          W("c1", "%d + %d = %d" % (a, ans, a + ans)), W("c2", "%d + 1 = %d" % (a + ans, total))),
        B(last_trap),
        B("%s means the two angles make %d degrees. Subtract the whole degrees first, then deal with the half." % (word.capitalize(), total)),
    )


LESSONS[TB + "ch18_q002"] = with_a_half(
    TB + "ch18_q002", 90, 45,
    "And don't mix up the two words. Taking the angle from 180 would give its supplementary angle, which is a different question.")

LESSONS[TB + "ch18_q003"] = with_a_half(
    TB + "ch18_q003", 180, 100,
    "Notice the word had to be supplementary here. 100 and a half is already bigger than a square corner, so it can have no complementary angle at all.")


# ── Two equal angles ─────────────────────────────────────────────────────────

def equal_pair(qid, total, picture, trap):
    word, layout, miss = WORDS[total]
    half = total // 2
    choices, right = placed(qid, "total", "%d°" % total, ["%d°" % t for t in (90, 180, 360) if t != total])
    sums, sum_right = placed(qid, "sum", "%d ÷ 2" % total, ["%d × 2" % total, "%d − 2" % total])
    return lesson(
        B("Two angles are equal, and they are also %s. We want the size of each one." % word,
          GIVEN("l1", "Two equal angles, %s. Each = ?" % word)),
        B("Start with the long word. %s angles add up to how much?" % word.capitalize(), ask=choose(choices, right, miss)),
        B("So the two angles together make %d degrees. And they are equal, so it is the same angle twice." % total,
          W("l2", "angle + angle = %d" % total, label=True),
          FIG("f1", kind="angles", layout=layout, parts=[{"label": "?"}, {"label": "?"}])),
        B("Two equal angles share %d degrees. How do we find each one?" % total,
          ask=choose(sums, sum_right,
                     "Sharing equally between two means halving. So we divide the %d degrees by 2." % total)),
        B("Half of %d is %d. So each angle is %d degrees." % (total, half, half),
          W("l3", "%d ÷ 2 = %d" % (total, half)),
          ANS("ans", "Each angle = %d°" % half, True), M("ans", "%d°" % half, "circle")),
        B(trap),
        B(picture + " Check: %d plus %d is %d." % (half, half, total), W("chk", "%d + %d = %d" % (half, half, total)),
          FIG("f2", kind="angles", layout=layout, parts=[{"label": "%d°" % half, "size": half}, {"label": "%d°" % half, "size": half}])),
        B("Turn the word into its number, %d for %s. Then two equal angles each get half." % (total, word)),
    )


LESSONS[TB + "ch18_q004"] = equal_pair(
    TB + "ch18_q004", 90,
    "Picture a square corner cut exactly down the middle.",
    "Careful not to answer 90. That is what the two angles make together, not the size of each one.")

LESSONS[TB + "ch18_q005"] = equal_pair(
    TB + "ch18_q005", 180,
    "Picture a pole standing straight up on flat ground, with a square corner on each side.",
    "Careful not to halve 90 here. That would be for complementary angles. Supplementary angles share 180.")


# ── A linear pair with a right angle ─────────────────────────────────────────

LESSONS[TB + "ch18_q006"] = lesson(
    B("Two angles form a linear pair, and one of them is 90 degrees. We want to know what kind of angle the other one is.",
      GIVEN("l1", "Linear pair: one angle = 90°. The other is what kind?"),
      FIG("f1", kind="angles", layout="onLine", parts=[{"label": "90°", "size": 90}, {"label": "?"}])),
    B("First the words. A linear pair is two angles side by side on a straight line. What do they add up to?",
      ask=choose(["90°", "360°", "180°"], 2,
                 "A straight line is a half turn. A full turn is 360 degrees, so the two angles of a linear pair share 180 degrees.")),
    B("So 90, plus the other angle, makes 180.", W("l2", "90 + ? = 180")),
    B("180 minus 90 is 90. The other angle is 90 degrees too.", W("l3", "180 − 90 = 90")),
    B("And what do we call an angle of exactly 90 degrees?",
      ask=choose(["Acute angle", "Right angle", "Obtuse angle"], 1,
                 "Acute angles are smaller than 90 degrees, and obtuse angles are bigger than 90. Exactly 90 degrees, a square corner, is a right angle.")),
    B("Here are the three names together. Less than 90 is acute. Exactly 90 is right. More than 90, up to 180, is obtuse.",
      W("n1", "Acute: less than 90°", label=True), W("n2", "Right: exactly 90°", label=True),
      W("n3", "Obtuse: more than 90°", label=True), M("n2", "Right", "box")),
    B("So the other angle is a right angle.",
      ANS("ans", "The other angle is a right angle (90°)", True), M("ans", "right angle", "circle")),
    B("It can feel as if the partner must be a different kind. Usually it is: a small acute angle has a wide obtuse partner. But 90 is exactly half of 180, so here both are the same."),
    B("Picture a pole standing straight up on flat ground: a square corner on each side. And 90 plus 90 is 180.",
      W("chk", "90 + 90 = 180"),
      FIG("f2", kind="angles", layout="onLine", parts=[{"label": "90°", "size": 90}, {"label": "90°", "size": 90}])),
    B("For a linear pair, take the angle you know from 180. Then name what you get: acute, right or obtuse."),
)
