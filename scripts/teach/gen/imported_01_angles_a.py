"""Angles on a straight line: the angle next door (seven questions, one builder)."""
from imported_01_lib import AI, ANS, B, FIG, GIVEN, M, W, choose, count_up_lines, lesson, placed, take_away_lines

LESSONS = {}

ASK_LINE = [
    ("These two angles sit side by side on one straight line. Together, how much do they always make?",
     "A straight line is a half turn. A full turn is 360 degrees, and half of that is 180 degrees."),
    ("Look at the picture. The two angles share the straight line between them. How many degrees is a straight line?",
     "Think of turning to face the opposite way. That is half of a full turn of 360 degrees, so a straight line is 180 degrees."),
    ("Here is the fact we need. Two angles next to each other on a straight line add up to how many degrees?",
     "A square corner is 90 degrees. Put two square corners side by side and they make a straight line. So a straight line is 180 degrees."),
]

ASK_SUM = [
    "How do we get the missing angle from that?",
    "Which sum finds the missing angle?",
    "So what do we do with the 180 and the %d?",
]

SUMMARY = [
    "Two angles side by side on a straight line always make 180 degrees. Know one, subtract, and you have the other.",
    "So the plan is short. Spot the straight line, remember 180 degrees, and take away the angle you know.",
    "Next-door angles on a straight line are partners that make 180 degrees. Find one by taking the other from 180.",
]


def split_lines(prefix, a):
    """180 − a by splitting 180 into 100 and 80 (for a below 80)."""
    rest = 80 - a
    ops = [W(prefix + "a", "180 = 100 + 80"), W(prefix + "b", "80 − %d = %d" % (a, rest)),
           W(prefix + "c", "100 + %d = %d" % (rest, 100 + rest))]
    words = "Split 180 into 100 and 80. 80 minus %d is %d. Put the 100 back, and we have %d." % (a, rest, 100 + rest)
    return ops, words


def next_door(qid, a, opening, given, answer_label, trap, method, mix):
    """The angle next to `a` on a straight line.

    `method` is the way of subtracting; `mix` picks the wording of (first ask, second ask, check, summary),
    so that the six lessons about 65 degrees do not sound alike.
    """
    b = 180 - a
    ask_say, ask_miss = ASK_LINE[mix[0]]
    choices, right = placed(qid, "line", "180°", ["90°", "360°"])
    sums, sum_right = placed(qid, "sum", "180 − %d" % a, ["180 + %d" % a, "90 − %d" % a])
    if method == 0:
        ops, words = take_away_lines("s", 180, a)
        words = "180 minus %d. %s" % (a, words)
    elif method == 1:
        ops, words = count_up_lines("s", 180, a)
        words = "180 minus %d is the gap from %d up to 180. %s" % (a, a, words)
    else:
        ops, words = split_lines("s", a)
        words = "180 minus %d. %s" % (a, words)
    sum_say = ASK_SUM[mix[1]]
    if "%d" in sum_say:
        sum_say = sum_say % a
    check = [
        "Check by adding. %d plus %d makes 180. A straight line, just as it should be." % (a, b),
        "Does it fit? %d plus %d is 180, so together they lie flat along the line." % (a, b),
        "Let's check. %d and %d together make 180, which is exactly a straight line." % (a, b),
    ][mix[2]]
    return lesson(
        B(opening, GIVEN("l1", given),
          FIG("f1", kind="angles", layout="onLine", parts=[{"label": "%d°" % a, "size": a}, {"label": "?"}])),
        B(ask_say, ask=choose(choices, right, ask_miss)),
        B("So %d degrees and the missing angle add up to 180 degrees." % a,
          W("l2", "%d + ? = 180" % a), M("l2", "180")),
        B(sum_say, ask=choose(sums, sum_right,
                              "The two angles share 180 degrees between them. Take away the part we know, and what is left is the part we want.")),
        B(words, ops),
        B("So the angle we want is %d degrees." % b,
          ANS("ans", "%s = %d°" % (answer_label, b), True), M("ans", "%d°" % b, "circle")),
        B(trap),
        B(check, W("chk", "%d + %d = 180" % (a, b)),
          FIG("f2", kind="angles", layout="onLine",
              parts=[{"label": "%d°" % a, "size": a}, {"label": "%d°" % b, "size": b}])),
        B(SUMMARY[mix[3]]),
    )


TRAP_CROSS = [
    "Careful with the other choices. %d degrees again is the angle straight across the crossing, not the one next door.",
    "One trap: the angle straight across the crossing is %d degrees again. But we were asked for the one next to it.",
    "Watch out. Angles opposite each other at a crossing are equal, so %d degrees is the one across. Next door is a different angle.",
]
TRAP_CORNER = "Careful: taking %d from 90 is for a square corner. Here the two angles share a straight line, so we take it from 180."

LESSONS[AI + "40e395f6-79e5-4f96-9b0b-75485dbea0bb"] = next_door(
    AI + "40e395f6-79e5-4f96-9b0b-75485dbea0bb", 65,
    "Meera's two kite sticks cross, and one angle at the crossing is 65 degrees. We want the angle right next to it. Let me draw one stick as a straight line, with the two angles sitting on it.",
    "Two sticks cross. One angle = 65°. Next to it = ?", "Angle next to it", TRAP_CROSS[0] % 65, 0, (0, 0, 0, 0))

LESSONS[AI + "51c32ebb-0d7c-4c91-8fa1-e830b3f84462"] = next_door(
    AI + "51c32ebb-0d7c-4c91-8fa1-e830b3f84462", 65,
    "Rohan's crease meets the straight edge of his paper. On one side of the crease the angle is 65 degrees. We want the angle on the other side.",
    "Crease on a straight edge. One side = 65°. Other = ?", "Other side of the crease", TRAP_CORNER % 65, 1, (1, 1, 1, 1))

LESSONS[AI + "62647a3d-5e4d-4910-a575-a336a0e2bc10"] = next_door(
    AI + "62647a3d-5e4d-4910-a575-a336a0e2bc10", 65,
    "Riya's rangoli has two straight lines that cross. One angle is 65 degrees, and we want its next-door neighbour. Here is one of her lines, with both angles sitting on it.",
    "Two lines cross. One angle = 65°. Adjacent angle = ?", "Adjacent angle", TRAP_CROSS[1] % 65, 2, (2, 2, 2, 2))

LESSONS[AI + "8920f4d6-32d0-4d7f-925e-f791c893ab59"] = next_door(
    AI + "8920f4d6-32d0-4d7f-925e-f791c893ab59", 53,
    "Arjun's rope lies in a straight line along the ground, and a pole leans against it. On one side of the pole the angle is 53 degrees. What is the angle on the other side?",
    "Pole on a straight rope. One side = 53°. Other = ?", "Other side of the pole",
    "Careful with the taking away. It is easy to slip by 10 in the tens and still feel sure. That is why we check by adding.", 0, (1, 2, 2, 1))

LESSONS[AI + "9994fe74-ae30-42d7-ae90-f772c6f33893"] = next_door(
    AI + "9994fe74-ae30-42d7-ae90-f772c6f33893", 65,
    "Riya lays two straight sticks so that they cross. One of the angles is 65 degrees. Which angle sits right beside it? Let's look along one stick.",
    "Two sticks cross. One angle = 65°. Adjacent angle = ?", "Adjacent angle", TRAP_CROSS[2] % 65, 1, (2, 0, 0, 2))

LESSONS[AI + "b22920c0-5356-4556-a726-365e88c4f35e"] = next_door(
    AI + "b22920c0-5356-4556-a726-365e88c4f35e", 65,
    "Vikram finds an angle of 65 degrees where two tiles meet. We want the angle right next to it along the same straight edge. So let me draw that straight edge.",
    "On a straight edge: one angle = 65°. Next to it = ?", "Angle next to it", TRAP_CORNER % 65, 2, (0, 1, 2, 1))

LESSONS[AI + "edcfe902-58ed-4108-be24-f52764e67984"] = next_door(
    AI + "edcfe902-58ed-4108-be24-f52764e67984", 65,
    "Ravi crosses two sticks and gets 4 angles. One of them is 65 degrees, and we are after the angle right next to it. Follow one stick: it is a straight line with two angles on it.",
    "Two sticks cross: 4 angles. One = 65°. Next to it = ?", "Angle next to it",
    "Careful: the 4 angles here come in two sizes. The one straight across is 65 degrees again. The one next door is the other size.",
    0, (2, 1, 1, 0))
