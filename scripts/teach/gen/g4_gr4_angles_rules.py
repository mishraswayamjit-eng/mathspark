"""Rule-made Grade 4 angles lessons: one function per question wording.

RULES is a list of (regular expression, function). The function gets the question and the
match and returns a lesson. Every number on the board is computed here, never typed.
"""
import re

from g4_gr4_angles_lib import (A, B, G, L, W, angles, ask, box, hpick, lesson, mark, ring)

RULES = []


def rule(pattern):
    def register(fn):
        RULES.append((re.compile(pattern), fn))
        return fn
    return register


def take_away_beats(whole, n, result_id):
    """Beats that work out whole − n, in two easy hops when n is not a round number.
    The last line written is `whole − n = answer`, with id `result_id`."""
    ans = whole - n
    tens, ones = n - n % 10, n % 10
    final = W(result_id, "%d − %d = %d" % (whole, n, ans))
    if ones == 0 or tens == 0:
        return [B("%d take away %d leaves %d." % (whole, n, ans), final, mark(result_id, "= %d" % ans))]
    step = whole - tens
    return [
        B("Let's take %d away in two easy hops. First the %d: %d take away %d leaves %d." % (n, tens, whole, tens, step),
          W(result_id + "a", "%d − %d = %d" % (whole, tens, step))),
        B("Now the %d that is left: %d take away %d leaves %d. So %d minus %d is %d." % (ones, step, ones, ans, whole, n, ans),
          W(result_id + "b", "%d − %d = %d" % (step, ones, ans)), final),
    ]


# ── Supplementary and complementary angles ───────────────────────────────────

def angle_pair(q, n, kind, given_text):
    """The partner of n degrees on a straight line (kind 'supp') or in a right angle ('comp')."""
    qid = q["id"]
    supp = kind == "supp"
    whole = 180 if supp else 90
    other = 90 if supp else 180
    ans = whole - n
    layout = "onLine" if supp else "inRightAngle"
    name = "supplement" if supp else "complement"
    start = angles("f1", layout, [("%d°" % n, n), ("?",)])
    done = angles("f2", layout, [("%d°" % n, n), ("%d°" % ans, ans)], highlight=["p1"])

    if supp:
        opening = hpick(qid, "open", [
            "We want the supplement of %d degrees. Supplementary angles are two angles that sit side by side on a straight line. Here is the picture.",
            "Our angle is %d degrees, and we want its supplementary partner. The two angles lie together along a straight line, like this.",
            "Here is %d degrees, drawn on a straight line. Its supplement is the other piece of that line, the one with the question mark.",
        ]) % n
        why = hpick(qid, "why", [
            "Stand at the point and turn from one end of the line to the other. That is a half turn.",
            "Picture yourself standing where the two angles meet. You face along the line, then turn to face the other way. That is a half turn.",
        ])
        why_line = L("l2", "Straight line = half turn = 180°")
        told = "A straight line is a half turn, and a half turn is 180 degrees."
        if_not = "Look at the drawing. The two angles lie along a straight line, and a straight line is a half turn. That makes 180 degrees. 90 is for a square corner."
        trap = "To remember which is which: S for supplementary, S for straight line. C for complementary, C for corner."
    else:
        opening = hpick(qid, "open", [
            "We want the complement of %d degrees. Complementary angles are two angles that fit together to make a right angle, like the corner of a page. Here is the picture.",
            "Our angle is %d degrees, and we want its complementary partner. The two angles fit snugly into one square corner, like this.",
            "Here is %d degrees, drawn inside a right angle. Its complement is the other piece of that corner, the one with the question mark.",
        ]) % n
        why = hpick(qid, "why", [
            "A right angle is a square corner, like the corner of a book or a door. Turning through it is a quarter turn.",
            "Picture the corner of your notebook. That square corner is a right angle, a quarter of a full turn.",
        ])
        why_line = L("l2", "Right angle = quarter turn = 90°")
        told = "A right angle is a quarter turn, and a quarter turn is 90 degrees."
        if_not = "Look at the drawing. The two angles fit inside a square corner, and a square corner is a quarter turn. That makes 90 degrees. 180 is for a straight line."
        trap = "To remember which is which: C for complementary, C for corner. S for supplementary, S for straight line."

    how = hpick(qid, "how", [
        "We know the whole, %d, and one part, %d. How do we find the other part?",
        "The whole is %d and one piece is %d. Which sum finds the missing piece?",
    ]) % (whole, n)
    if supp:
        slips = ["%d + %d" % (whole, n), ("%d − %d" % (other, n)) if n < other else ("%d − %d" % (n, other))]
    else:
        slips = ["%d + %d" % (whole, n), "%d − %d" % (other, n)]
    closing = hpick(qid, "close", [
        "So to find a %s, take the angle away from %d." % (name, whole),
        "So the two partners make %d. Take the angle you have away from %d." % (whole, whole),
    ])

    beats = [
        B(opening, G("l1", given_text), start),
        B(why + " So how much do our two angles make together?",
          ask=ask(qid + "a1", "%d°" % whole, ["%d°" % other, "360°"], if_not)),
        B(told + " So %d, plus our missing angle, makes %d." % (n, whole),
          why_line, box("l2", "%d°" % whole),
          W("l3", "%d + ? = %d" % (n, whole)), ring("l3", "?")),
        B(how, ask=ask(qid + "a2", "%d − %d" % (whole, n), slips,
                       "When we know the whole and one part, we take the part away from the whole. So it is %d take away %d." % (whole, n))),
    ]
    beats += take_away_beats(whole, n, "l5")
    beats += [
        B("So the %s is %d degrees. Watch it go into the drawing." % (name, ans),
          A("l6", "%s = %d°" % (name.capitalize(), ans)), ring("l6", "%d°" % ans), done),
        B("Let's check by adding them back. %d plus %d makes %d. It fits exactly." % (n, ans, whole),
          W("l7", "%d + %d = %d" % (n, ans, whole))),
        B(closing + " " + trap),
    ]
    return lesson(beats, "rule")


@rule(r"^What is the (complement|supplement) of an angle of (\d+)°\?$")
def what_is_partner(q, m):
    n = int(m.group(2))
    kind = "supp" if m.group(1) == "supplement" else "comp"
    return angle_pair(q, n, kind, "%s of %d° = ?" % (m.group(1).capitalize(), n))


@rule(r"^Find the (supplementary|complementary) angle of (\d+)°\.$")
def find_partner(q, m):
    n = int(m.group(2))
    kind = "supp" if m.group(1) == "supplementary" else "comp"
    return angle_pair(q, n, kind, "%s angle of %d° = ?" % (m.group(1).capitalize(), n))


@rule(r"^Two angles are supplementary\. If one angle is (\d+)°, find the other\.$")
def supplementary_other(q, m):
    n = int(m.group(1))
    return angle_pair(q, n, "supp", "Supplementary angles: %d° and ?" % n)


# ── Two angles on a straight line: x and n ───────────────────────────────────

@rule(r"^Two angles on a straight line are x° and (\d+)°\. Find x\.$")
def straight_line_x(q, m):
    qid = q["id"]
    n = int(m.group(1))
    x = 180 - n
    f1 = angles("f1", "onLine", [("x°",), ("%d°" % n, n)])
    f2 = angles("f2", "onLine", [("%d°" % x, x), ("%d°" % n, n)], highlight=["p0"])
    opening = hpick(qid, "open", [
        "Here is a straight line with two angles sitting on it. One is %d degrees. The other is called x, and we want its size.",
        "Two angles share a straight line. One is %d degrees and the other is a mystery, called x. Let's find x.",
        "Look at the picture. A straight line, and two angles on it: %d degrees, and x. What is x?",
    ]) % n
    beats = [
        B(opening, G("l1", "On a straight line: x° and %d°. x = ?" % n), f1),
        B("Stand where the two angles meet. You face along the line, then turn to face the other way. That is a half turn. So how much do the two angles make together?",
          ask=ask(qid + "a1", "180°", ["90°", "360°"],
                  "The two angles lie along a straight line, and a straight line is a half turn. That makes 180 degrees. 90 is for a square corner.")),
        B("A half turn is 180 degrees. So x, plus %d, equals 180." % n,
          L("l2", "Straight line = half turn = 180°"), box("l2", "180°"),
          W("l3", "x + %d = 180" % n), ring("l3", "x")),
        B("180 is the whole, and %d is one part of it. x is the other part. How do we find x?" % n,
          ask=ask(qid + "a2", "180 − %d" % n, ["180 + %d" % n, ("90 − %d" % n) if n < 90 else ("%d − 90" % n)],
                  "When we know the whole and one part, we take the part away from the whole. So x is 180 take away %d." % n)),
    ]
    beats += take_away_beats(180, n, "l5")
    beats += [
        B("So x equals %d. The other angle is %d degrees." % (x, x),
          W("l6", "x = %d" % x, tone="answer"), ring("l6", "x = %d" % x), f2),
        B("Check: %d plus %d makes 180, one whole straight line. It fits." % (x, n),
          W("l7", "%d + %d = 180" % (x, n))),
        B(hpick(qid, "close", [
            "So angles on a straight line always make 180 degrees. Take the one you know away from 180, and you have the other.",
            "Remember: a straight line is 180 degrees. Know one angle on it, and 180 minus that angle gives you the other.",
        ])),
    ]
    return lesson(beats, "rule", check=("x", x))


# ── Vertically opposite angles ───────────────────────────────────────────────

@rule(r"^Two straight lines cross\. One angle formed is (\d+)°\. Find the vertically opposite angle\.$")
def vertically_opposite(q, m):
    qid = q["id"]
    n = int(m.group(1))
    side = 180 - n
    f1 = angles("f1", "crossing", [("%d°" % n, n), ("p",), ("?",), ("q",)])
    f2 = angles("f2", "crossing", [("%d°" % n, n), ("%d°" % side,), ("?",), ("q",)], highlight=["p0", "p1"])
    f3 = angles("f3", "crossing", [("%d°" % n, n), ("%d°" % side,), ("%d°" % n,), ("%d°" % side,)], highlight=["p0", "p2"])
    opening = hpick(qid, "open", [
        "Two straight lines cross and make 4 angles. One of them is %d degrees. We want the angle vertically opposite: the one straight across the crossing point.",
        "Here are two straight lines, crossing like a letter X. One angle is %d degrees. We want the angle right across from it.",
    ]) % n
    beats = [
        B(opening, G("l1", "Lines cross: one angle is %d°. Opposite angle = ?" % n), f1),
        B("I have called the two angles next door p and q. Now, a straight line is a half turn, and a half turn is 180 degrees.",
          L("l2", "Angles on a straight line = 180°"), box("l2", "180°")),
        B("Look at %d degrees and its neighbour, p. They sit side by side on one straight line. So p is what is left of 180." % n),
    ]
    beats += take_away_beats(180, n, "l3")
    beats += [
        B("So p is %d degrees. Now look at p and our mystery angle. They sit side by side on the other straight line. So what is the mystery angle?" % side,
          f2,
          ask=ask(qid + "a1", "180 − %d" % side, ["%d, the same as p" % side, "180 + %d" % side],
                  "p and the mystery angle share a straight line, so together they make 180 degrees. We take p, which is %d, away from 180." % side)),
    ]
    beats += take_away_beats(180, side, "l4")
    beats += [
        B("%d degrees. Exactly the angle we started with! That always happens: angles straight across from each other are equal." % n,
          L("l5", "Vertically opposite angles are equal"),
          A("l6", "Opposite angle = %d°" % n), ring("l6", "%d°" % n), f3),
        B("So next time you can say it straight away: the vertically opposite angle is equal, %d degrees. The slip to watch for is giving %d, which is the neighbour on the line." % (n, side)),
    ]
    return lesson(beats, "rule")
