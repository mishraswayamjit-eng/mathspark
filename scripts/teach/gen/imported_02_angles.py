"""Angles and lines: linear pairs, complementary and supplementary, compass and clock angles."""
from imported_02_lib import ANS, B, DIV, FIG, G, GIVEN, L, M, N, S, W, choose, lesson

LESSONS = {}
P = "IPMTB_grade5_ch18_q"

LINE_180 = "Linear pair: the two angles add up to 180°"


def on_line(*parts):
    return {"kind": "angles", "layout": "onLine", "parts": list(parts)}


def in_corner(*parts):
    return {"kind": "angles", "layout": "inRightAngle", "parts": list(parts)}


# ── Linear pairs ─────────────────────────────────────────────────────────────

LESSONS[P + "007"] = lesson(
    B("Two angles sit side by side on a straight line. That is a linear pair. One of them is acute, and we want to know what kind the other must be.",
      GIVEN("q", "Linear pair: one angle is acute. The other?"),
      FIG("f1", on_line({"label": "acute", "size": 50}, {"label": "?"}))),
    B("First, the key fact. A straight line is a half turn, so the two angles of a linear pair always add up to 180 degrees.",
      L("r1", LINE_180), M("r1", "180°", "box")),
    B("Acute means small: less than 90 degrees. Let's try one. Say the acute angle is 50 degrees. How do we find its partner?",
      L("r2", "Acute: less than 90°"),
      ask=choose(["180 − 50", "90 − 50", "180 + 50"], 0,
                 "The two angles share 180 degrees between them. So the partner is whatever is left when we take 50 away from 180.")),
    B("180 minus 50 is 130. That is more than 90 degrees, so the partner is an obtuse angle.",
      W("w1", "180 − 50 = 130"), N("w1", "130", "more than 90")),
    B("Was that just luck? Try an acute angle close to 90, say 80 degrees. Its partner is 180 minus 80, which is 100. Still more than 90.",
      W("w2", "180 − 80 = 100"), N("w2", "100", "more than 90")),
    B("Here is why it always works. 90 and 90 make 180. If one angle takes less than its 90, the other has to take more than 90 to make up the total.",
      W("w3", "90 + 90 = 180")),
    B("So the other angle is always obtuse.",
      ANS("a", "The other angle is obtuse", True), M("a", "obtuse", "circle")),
    B("The trap is to say acute, because the two angles are a pair. But two acute angles together are less than 180, so they could never fill a straight line."),
    B("Remember it this way: on a straight line, a small angle always has a big partner."),
)

LESSONS[P + "029"] = lesson(
    B("Two angles side by side on a straight line make a linear pair. This time one of them is obtuse. What kind is the other?",
      GIVEN("q", "Linear pair: one angle is obtuse. The other?"),
      FIG("f1", on_line({"label": "obtuse", "size": 120}, {"label": "?"}))),
    B("The key fact first. A straight line is a half turn, so the two angles of a linear pair always add up to 180 degrees.",
      L("r1", LINE_180), M("r1", "180°", "box")),
    B("Obtuse means wide: more than 90 degrees, but less than 180. Let's try one. Say the obtuse angle is 120 degrees. How do we find its partner?",
      L("r2", "Obtuse: between 90° and 180°"),
      ask=choose(["120 − 90", "180 − 120", "180 + 120"], 1,
                 "Together the two angles make 180 degrees. So the partner is what is left when 120 is taken away from 180.")),
    B("180 minus 120 is 60. That is less than 90 degrees, so the partner is an acute angle.",
      W("w1", "180 − 120 = 60"), N("w1", "60", "less than 90")),
    B("Try another, to be sure. An obtuse angle of 100 degrees leaves 180 minus 100, which is 80. Less than 90 again.",
      W("w2", "180 − 100 = 80"), N("w2", "80", "less than 90")),
    B("Here is why. 90 and 90 make 180. If one angle takes more than its 90, there is less than 90 left for the other.",
      W("w3", "90 + 90 = 180")),
    B("So the other angle is always acute.",
      ANS("a", "The other angle is acute", True), M("a", "acute", "circle")),
    B("Don't be tempted by obtuse. Two obtuse angles would add up to more than 180, and that is too much for a straight line."),
    B("On a straight line, a big angle always has a small partner."),
)

LESSONS[P + "031"] = lesson(
    B("Two angles side by side on a straight line make a linear pair. One of them is 90 degrees. What kind of angle is the other?",
      GIVEN("q", "Linear pair: one angle is 90°. The other?"),
      FIG("f1", on_line({"label": "90°", "size": 90}, {"label": "?"}))),
    B("A straight line is a half turn. So the two angles of a linear pair always add up to 180 degrees.",
      L("r1", LINE_180), M("r1", "180°", "box")),
    B("One angle is 90. Which sum gives us the other one?",
      ask=choose(["90 − 90", "180 + 90", "180 − 90"], 2,
                 "The two angles share 180 degrees. Take away the 90 we know, and what is left is the other angle.")),
    B("180 minus 90 is 90. So the other angle is 90 degrees as well.",
      W("w1", "180 − 90 = 90"), M("w1", "90", "underline", 2)),
    B("Now, what do we call an angle of exactly 90 degrees?",
      ask=choose(["an acute angle", "a right angle", "an obtuse angle"], 1,
                 "Acute is less than 90 degrees and obtuse is more than 90. Exactly 90 degrees, like the corner of your notebook, has its own name.")),
    B("A right angle. So the other angle is a right angle too.",
      ANS("a", "The other angle is a right angle", True), M("a", "right angle", "circle")),
    B("Check: 90 plus 90 is 180, a whole straight line. Picture a pole standing straight up on flat ground: a square corner on each side.",
      W("c", "90 + 90 = 180")),
    B("So for any linear pair, take the angle you know away from 180, then name what is left."),
)

# ── Which pair? ──────────────────────────────────────────────────────────────

SUPP_RULE = "Supplementary: the two angles add up to 180°"
COMP_RULE = "Complementary: the two angles add up to 90°"

LESSONS[P + "010"] = lesson(
    B("We have three pairs of angles, and we are hunting for a supplementary pair. There may not be one at all.",
      GIVEN("q", "Which pair is supplementary?"),
      L("p", "A: 70°, 20°   B: 50°, 50°   C: 100°, 180°")),
    B("First, what does supplementary mean? What must the two angles add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "90 degrees is for complementary angles. Supplementary angles fill a straight line, and a straight line is 180 degrees.")),
    B("So our test is simple. Add the pair. If the total is exactly 180, it is supplementary.",
      L("r", SUPP_RULE), M("r", "180°", "box")),
    B("Pair A. 70 plus 20 is 90. That is a right angle, not a straight line. So A is out.",
      W("a1", "70 + 20 = 90"), S("p", "A: 70°, 20°")),
    B("Pair B. 50 plus 50 is 100. Not 180 either.",
      W("b1", "50 + 50 = 100"), S("p", "B: 50°, 50°")),
    B("Pair C looks tempting, because it has 180 in it. But we need the total to be 180. What is 100 plus 180?",
      ask=choose(["180", "280", "80"], 1,
                 "Add the two angles together: 100, and 180 more. That goes well past 180.")),
    B("280. Far too big. So C is out as well.",
      W("c1", "100 + 180 = 280"), S("p", "C: 100°, 180°")),
    B("None of the three pairs adds up to 180. So the answer is: none of these.",
      ANS("ans", "None of these", True), M("ans", "None of these", "circle")),
    B("It can feel odd to pick none of these. But we tested every pair, so we can be sure."),
    B("The method: for supplementary, add the pair and look for 180. Check every choice before you decide."),
)

LESSONS[P + "011"] = lesson(
    B("Three pairs of angles. One of them is a complementary pair, and we are going to find it.",
      GIVEN("q", "Which pair is complementary?"),
      L("p", "A: 80°, 20°   B: 70°, 110°   C: 50°, 40°")),
    B("What do complementary angles add up to?",
      ask=choose(["90°", "180°", "100°"], 0,
                 "180 degrees is for supplementary angles. Complementary angles fit together into one right angle, and a right angle is 90 degrees.")),
    B("So we add each pair and look for exactly 90.",
      L("r", COMP_RULE), M("r", "90°", "box")),
    B("Pair A. 80 plus 20 is 100. Close, but 100 is not 90. A is out.",
      W("a1", "80 + 20 = 100"), S("p", "A: 80°, 20°")),
    B("Pair B. 70 plus 110 is 180. That pair is supplementary, which is the other word. Easy to mix up! B is out.",
      W("b1", "70 + 110 = 180"), S("p", "B: 70°, 110°")),
    B("Pair C. 50 plus 40. What do we get?",
      ask=choose(["80", "90", "100"], 1,
                 "Add the tens: 5 tens and 4 tens make 9 tens.")),
    B("90, exactly. So 50 degrees and 40 degrees are complementary.",
      ANS("ans", "50 + 40 = 90"), M("p", "C: 50°, 40°", "circle")),
    B("A way to remember: C for complementary, C for corner. A corner is a right angle, 90 degrees."),
    B("So: add the pair. 90 means complementary, 180 means supplementary."),
)

LESSONS[P + "027"] = lesson(
    B("Four pairs of angles. Three of them are supplementary, and one is not. We want the odd one out.",
      GIVEN("q", "Which pair is NOT supplementary?"),
      L("p1", "A: 70°, 20°     B: 40°, 140°"), L("p2", "C: 70°, 110°    D: 120°, 60°")),
    B("What do supplementary angles add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "90 degrees is for complementary angles. Supplementary angles fill a straight line, and a straight line is 180 degrees.")),
    B("So we add each pair, and look for the one that does not make 180.",
      L("r", SUPP_RULE), M("r", "180°", "box")),
    B("Pair A. 70 plus 20 is 90. That is not 180. It looks like our odd one out, but let's check the others to be sure.",
      W("a1", "70 + 20 = 90"), M("p1", "A: 70°, 20°", "circle")),
    B("Pair B. 40 plus 140 is 180. Supplementary.",
      W("b1", "40 + 140 = 180")),
    B("Pair C. 70 plus 110. What is the total?",
      ask=choose(["170", "180", "190"], 1,
                 "Add the two angles carefully: start at 110, and count on 70 more.")),
    B("180 again. And pair D: 120 plus 60 is 180 as well.",
      W("c1", "70 + 110 = 180"), W("d1", "120 + 60 = 180")),
    B("So only pair A does not make 180. 70 degrees and 20 degrees are not supplementary.",
      ANS("ans", "70 + 20 = 90, not 180", True), M("ans", "not 180", "circle")),
    B("Notice the word not in the question. Three pairs pass the test here, and we want the one that does not."),
    B("70 and 20 make 90, so they are complementary instead. Add the pair: 90 is complementary, 180 is supplementary."),
)


# ── The name for a total ─────────────────────────────────────────────────────

def pair_name(total):
    supp = total == 180
    name, other = ("supplementary", "complementary") if supp else ("complementary", "supplementary")
    if supp:
        example = B("Here is a pair like that: 120 degrees and 60 degrees. Side by side they make a straight line, and a straight line is 180 degrees.",
                    FIG("f1", on_line({"label": "120°", "size": 120}, {"label": "60°", "size": 60})), W("e", "120 + 60 = 180"))
        ask = B("Two names get mixed up all the time: complementary and supplementary. One goes with 90 degrees, the other with 180. Which is the name for 180?",
                L("t", "Two names: complementary, supplementary"), L("u", "Two totals: 90°, 180°"),
                ask=choose(["complementary", "supplementary"], 1,
                           "Complementary goes with a corner, 90 degrees. The other word, supplementary, goes with a straight line, 180 degrees."))
        trick = B("Supplementary. Here is the trick: S for supplementary, S for straight line. And C for complementary, C for corner, which is 90 degrees.",
                  L("r1", "180°: supplementary (S for straight line)"), L("r2", "90°: complementary (C for corner)"))
        last = "Whenever you see a total of 180, think straight line, think supplementary."
    else:
        example = B("Here is a pair like that: 60 degrees and 30 degrees. Together they fill a square corner, and a square corner is a right angle, 90 degrees.",
                    FIG("f1", in_corner({"label": "60°", "size": 60}, {"label": "30°", "size": 30})), W("e", "60 + 30 = 90"))
        ask = B("Two names get mixed up all the time: complementary and supplementary. One goes with 90 degrees, the other with 180. Which one goes with 90?",
                L("t", "Two names: complementary, supplementary"), L("u", "Two totals: 90°, 180°"),
                ask=choose(["supplementary", "complementary"], 1,
                           "Supplementary goes with a straight line, 180 degrees. The other word, complementary, goes with a corner, 90 degrees."))
        trick = B("Complementary. Here is the trick: C for complementary, C for corner. And S for supplementary, S for straight line, which is 180 degrees.",
                  L("r1", "90°: complementary (C for corner)"), L("r2", "180°: supplementary (S for straight line)"))
        last = "Whenever you see a total of 90, think corner, think complementary."
    return lesson(
        B("Two angles add up to %d degrees. There is a special name for a pair like that." % total,
          GIVEN("q", "Two angles add up to %d°. They are called ...?" % total)),
        example,
        ask,
        trick,
        B("What about the other two choices? Adjacent just means the angles are neighbours, sharing an arm. Their total can be anything.",
          L("r3", "Adjacent: next to each other, any total")),
        B("And vertically opposite angles face each other where two lines cross. They are equal, but they need not add up to %d." % total,
          L("r4", "Vertically opposite: across a crossing, equal")),
        B("So two angles with a sum of %d degrees are called %s angles." % (total, name),
          ANS("a", "Sum %d°: %s angles" % (total, name), True), M("a", "%s angles" % name, "circle")),
        B(last),
    )


LESSONS[P + "015"] = pair_name(180)
LESSONS[P + "016"] = pair_name(90)


# ── Compass directions ───────────────────────────────────────────────────────

def compass(facing, turn=None, direction="clockwise"):
    spec = {"kind": "compass", "facing": facing}
    if turn:
        spec["turns"] = [{"degrees": turn, "direction": direction}]
        spec["showEnd"] = True
    return spec


def main_directions(a, b, a_code, direction, between, b_first_miss):
    """The angle between two neighbouring main directions (always a quarter turn)."""
    return lesson(
        B("Picture a compass. We want the angle between %s and %s." % (a, b),
          GIVEN("q", "Angle between %s and %s = ?" % (a, b)), FIG("f1", compass(a_code))),
        B("A compass is a full circle. How many degrees are there in a full turn?",
          ask=choose(["180°", "360°", "100°"], 1,
                     "180 degrees is only a half turn, a straight line. All the way round, back to where you started, is twice that.")),
        B("360 degrees. And the 4 main directions, North, East, South and West, cut that circle into 4 equal parts.",
          L("l1", "Full turn = 360°"), L("l2", "N, E, S, W: 4 equal parts")),
        B("So each part is 360 divided by 4. That is 90 degrees, a quarter turn.",
          W("l3", "360 ÷ 4 = 90")),
        B("Now, %s and %s. Are they next-door neighbours on the compass, or is there another main direction between them?" % (a, b),
          ask=choose(["one main direction in between", "next-door neighbours"], 1, b_first_miss)),
        B("They are neighbours. So turning from %s to %s is exactly 1 quarter turn." % (a, b),
          FIG("f2", compass(a_code, 90, direction))),
        B("The angle between %s and %s is 90 degrees. A right angle." % (a, b),
          ANS("a", "%s to %s = 90°" % (a, b), True), M("a", "90°", "circle")),
        B("Check with the half-way direction, %s. From %s to %s is 45 degrees, and from %s to %s is another 45. Together, 90."
          % (between, a, between, between, b),
          W("c", "45 + 45 = 90")),
        B("So for the main compass directions, neighbours are always a quarter turn apart: 90 degrees."),
    )


LESSONS[P + "017"] = main_directions(
    "East", "South", "E", "clockwise", "South-East",
    "Go round the compass in order: North, East, South, West. East and South come one straight after the other.")
LESSONS[P + "035"] = main_directions(
    "North", "West", "N", "anticlockwise", "North-West",
    "Go round the compass in order: North, East, South, West, and back to North. West and North come one straight after the other.")

LESSONS[P + "018"] = lesson(
    B("Picture a compass. We want the angle between West and North-East.",
      GIVEN("q", "Angle between West and North-East = ?"), FIG("f1", compass("W"))),
    B("North-East is one of the half-way directions. With those included, how many directions are there around the compass?",
      ask=choose(["4", "6", "8"], 2,
                 "There are 4 main directions, and one half-way direction sits between each pair of them. That makes 4 more.")),
    B("8 directions, equally spaced around a full turn of 360 degrees.",
      L("l1", "N, NE, E, SE, S, SW, W, NW: 8 directions"), L("l2", "Full turn = 360°")),
    B("So each step from one direction to the next is 360 divided by 8, which is 45 degrees.",
      W("l3", "360 ÷ 8 = 45")),
    B("Now count the steps from West to North-East, the short way, over the top. West to North-West, then to North, then to North-East. How many steps?",
      L("l4", "W → NW → N → NE"),
      ask=choose(["2", "3", "4"], 1,
                 "Count the arrows, not the names. West to North-West is 1, North-West to North is 2, North to North-East is 3.")),
    B("3 steps of 45 degrees. 3 times 45 is 135. The angle is 135 degrees.",
      ANS("a", "3 × 45 = 135"), M("a", "135", "circle"), FIG("f2", compass("W", 135, "clockwise"))),
    B("Why the short way? Going round the other way is 5 steps, and 5 times 45 is 225. The angle between two directions is the smaller one.",
      W("o", "5 × 45 = 225")),
    B("And a check: 135 plus 225 makes 360, the full turn. The two ways round fit together.",
      W("c", "135 + 225 = 360")),
    B("The trap is to say 90, by treating North-East as if it were North. West to North is 90, and then there are 45 more.",
      W("t", "90 + 45 = 135")),
    B("So: 45 degrees for every step on the compass. Count the steps, then multiply."),
)

# ── Finding the partner angle ────────────────────────────────────────────────

LESSONS[P + "019"] = lesson(
    B("We need the complementary angle of 37 and a half degrees.",
      GIVEN("q", "Complementary angle of 37 1/2° = ?")),
    B("Complementary angles are partners. What do the two partners add up to?",
      ask=choose(["90°", "180°", "100°"], 0,
                 "180 degrees is for supplementary angles. Complementary angles fit into one right angle, a square corner, and that is 90 degrees.")),
    B("So our angle and its partner make 90 degrees together. To find the partner, we take 37 and a half away from 90.",
      L("l1", "37 1/2° + ? = 90°"), L("l2", "? = 90° − 37 1/2°"),
      FIG("f1", in_corner({"label": "37 1/2°", "size": 37.5}, {"label": "?"}))),
    B("Let's do it in two small steps. First the whole part: 90 minus 37 is 53.",
      W("l3", "90 − 37 = 53")),
    B("Now there is still a half to take away. What is 53 minus a half?",
      ask=choose(["53 1/2", "52 1/2", "52"], 1,
                 "Taking away a half makes the number smaller than 53, but not a whole 1 smaller. So it lands between 52 and 53.")),
    B("52 and a half. So the complementary angle is 52 and a half degrees.",
      ANS("a", "90° − 37 1/2° = 52 1/2°", True), M("a", "52 1/2°", "circle")),
    B("Check by adding the partners. 37 and 52 make 89. The two halves make 1 more. And 89 plus 1 is 90.",
      W("c1", "37 + 52 = 89"), W("c2", "1/2 + 1/2 = 1"), W("c3", "89 + 1 = 90")),
    B("Watch out: if you take it away from 180 instead, you are finding the supplementary angle, which is a different partner."),
    B("So: complementary means the pair makes 90. Take the angle away from 90, whole part first, then the fraction."),
)

LESSONS[P + "020"] = lesson(
    B("We need the supplementary angle of 98 and a quarter degrees.",
      GIVEN("q", "Supplementary angle of 98 1/4° = ?")),
    B("Supplementary angles are partners. What do the two partners add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "90 degrees is for complementary angles. Supplementary angles fill a straight line, and a straight line is 180 degrees.")),
    B("So the partner is 180 take away 98 and a quarter.",
      L("l1", "98 1/4° + ? = 180°"), L("l2", "? = 180° − 98 1/4°"),
      FIG("f1", on_line({"label": "98 1/4°", "size": 98}, {"label": "?"}))),
    B("Whole part first. From 98 up to 100 is 2, and from 100 up to 180 is 80. So 180 minus 98 is 82.",
      L("l3", "98 → 100 → 180"), W("l4", "2 + 80 = 82"), W("l5", "180 − 98 = 82")),
    B("Now take a quarter from 82. Break 1 whole off the 82: that leaves 81 and 4 quarters. Take 1 quarter away from the 4 quarters. What is left?",
      W("l6", "82 = 81 + 4/4"),
      ask=choose(["81 1/4", "82 3/4", "81 3/4"], 2,
                 "We had 81 and 4 quarters. One quarter goes, so 3 quarters stay, and the 81 does not change.")),
    B("81 and three quarters. So the supplementary angle is 81 and three quarters degrees.",
      W("l7", "4/4 − 1/4 = 3/4"),
      ANS("a", "180° − 98 1/4° = 81 3/4°", True), M("a", "81 3/4°", "circle")),
    B("Check by adding. 98 and 81 make 179. A quarter and three quarters make 1 whole. And 179 plus 1 is 180.",
      W("c1", "98 + 81 = 179"), W("c2", "1/4 + 3/4 = 1"), W("c3", "179 + 1 = 180")),
    B("The slip to watch is 81 and a quarter. The quarter is being taken away, so it cannot just be copied into the answer."),
    B("So: supplementary means the pair makes 180. Take away the whole part first, then the fraction."),
)

LESSONS[P + "037"] = lesson(
    B("Two angles add up to 140 degrees, and one of them is 85 degrees. We want the supplementary angle of the smaller one. That is two jobs.",
      GIVEN("q", "Two angles: sum 140°, one is 85°"), L("q2", "Supplementary angle of the smaller one = ?")),
    B("First job: find the other angle. Which sum does that?",
      ask=choose(["140 + 85", "140 − 85", "180 − 85"], 1,
                 "The two angles together make 140. We know one is 85, so the other is what is left of the 140.")),
    B("140 minus 85. Take away 80 to get 60, then 5 more to get 55. The other angle is 55 degrees.",
      W("l0", "140 − 80 = 60"), W("l1", "60 − 5 = 55"), W("l1b", "140 − 85 = 55")),
    B("So the two angles are 85 degrees and 55 degrees. The smaller one is 55.",
      L("l2", "Angles: 85° and 55°"), M("l2", "55°", "circle")),
    B("Second job: the supplementary angle of 55. What must 55 and its partner add up to?",
      ask=choose(["90", "140", "180"], 2,
                 "140 was the total of the first two angles, and that job is done. Supplementary partners always make a straight line, 180 degrees.")),
    B("So the partner is 180 minus 55. 180 minus 50 is 130, and 5 more off is 125.",
      W("l3", "180 − 50 = 130"), W("l4", "130 − 5 = 125"), ANS("a", "180 − 55 = 125"), M("a", "125", "circle")),
    B("Check: 55 plus 125 is 180. Yes, a straight line.",
      W("c", "55 + 125 = 180")),
    B("Two traps here. One is to stop at 55, which is only the first job. The other is to use the 85: that gives 95, the partner of the bigger angle.",
      W("t", "180 − 85 = 95")),
    B("For a two-job question, underline what is really being asked, and do the jobs one at a time."),
)


# ── Clock hands at an exact hour ─────────────────────────────────────────────

def clock_lesson(hour, path, gaps, count_miss, gap_choices, closing):
    """`path` is the list of clock numbers passed going the short way between the hands."""
    angle = gaps * 30
    walk = ", ".join("%d to %d" % (path[i], path[i + 1]) for i in range(len(path) - 1))
    beats = [
        B("It is exactly %d o'clock. We want the angle between the hour hand and the minute hand." % hour,
          GIVEN("q", "Angle between the hands at %d o'clock = ?" % hour),
          FIG("f1", {"kind": "clock", "hour": hour, "minute": 0})),
        B("First, where are the two hands pointing at %d o'clock?" % hour,
          ask=choose(["both at %d" % hour, "hour hand at 12, minute hand at %d" % hour,
                      "hour hand at %d, minute hand at 12" % hour], 2,
                     "At an exact hour, the long minute hand points straight up at 12. The short hour hand points at the hour, which is %d." % hour)),
        B("Now the clock face. It is a full circle, 360 degrees, and the 12 numbers cut it into 12 equal gaps.",
          L("l1", "Full turn = 360°"), L("l2", "12 numbers: 12 equal gaps")),
        B("So each gap, from one number to the next, is 360 divided by 12. That is 30 degrees.",
          W("l3", "360 ÷ 12 = 30")),
        B("Now count the gaps between the hands, the short way round. From %s. How many gaps?" % walk,
          L("l4", " → ".join(str(n) for n in path)),
          ask=choose(gap_choices, gap_choices.index(str(gaps)), count_miss)),
        B("%d gaps of 30 degrees each. %d times 30 is %d. The angle is %d degrees." % (gaps, gaps, angle, angle),
          ANS("a", "%d × 30 = %d" % (gaps, angle)), M("a", str(angle), "circle"),
          FIG("f2", {"kind": "clock", "hour": hour, "minute": 0, "showAngle": True})),
    ]
    return lesson(*(beats + closing))


LESSONS[P + "021"] = clock_lesson(
    9, [9, 10, 11, 12], 3,
    "Count the jumps, not the numbers. 9 to 10 is 1, 10 to 11 is 2, 11 to 12 is 3.",
    ["4", "3", "9"],
    [
        B("Check it another way. 3 gaps out of 12 is a quarter of the clock, and a quarter of 360 is 90. The hands make a perfect square corner.",
          W("c", "360 ÷ 4 = 90")),
        B("Don't go the long way round, from 12 all the way down to 9. That is 9 gaps. The angle between the hands is the smaller one."),
        B("So for any exact hour: count the gaps between the hands, and multiply by 30 degrees."),
    ])

LESSONS[P + "022"] = clock_lesson(
    4, [12, 1, 2, 3, 4], 4,
    "Count the jumps, not the numbers. 12 to 1 is 1, 1 to 2 is 2, 2 to 3 is 3, 3 to 4 is 4.",
    ["3", "5", "4"],
    [
        B("Does that look right? At 3 o'clock the hands make a square corner, 90 degrees. At 4 o'clock they are 1 gap wider, and 90 plus 30 is 120.",
          W("c", "90 + 30 = 120")),
        B("The slip here is to count the numbers 12, 1, 2, 3, 4 and get 5. We count the gaps between them, and there are 4."),
        B("So for any exact hour: count the gaps between the hands, and multiply by 30 degrees."),
    ])

# ── Equations from angle facts ───────────────────────────────────────────────

LESSONS[P + "024"] = lesson(
    B("Two angles are equal, and they are supplementary. We want the size of each one.",
      GIVEN("q", "Two equal angles, supplementary. Each = ?")),
    B("Supplementary tells us the total. What do supplementary angles add up to?",
      ask=choose(["90°", "180°", "360°"], 1,
                 "90 degrees is the total for complementary angles. Supplementary angles fill a straight line, which is 180 degrees.")),
    B("So the two angles add up to 180. They are equal, so let's call each one x.",
      W("l1", "x + x = 180"), FIG("f1", on_line({"label": "x"}, {"label": "x"}))),
    B("x plus x is 2 lots of x. So 2 x equals 180.",
      G("l1", ["x", ("x", 2)], "2x"), W("l2", "2x = 180")),
    B("2 times x is 180. How do we get x on its own?",
      ask=choose(["subtract 2", "divide by 2", "multiply by 2"], 1,
                 "Times and divide are partners. To undo times 2, we divide by 2, and we do it to both sides.")),
    B("Divide both sides by 2. Half of 180 is 90. So x is 90.",
      DIV("l2", "2"), ANS("l3", "x = 90"), M("l3", "x = 90", "circle")),
    B("Each angle is 90 degrees, a right angle. Check: 90 plus 90 is 180. Equal, and supplementary.",
      W("c", "90 + 90 = 180")),
    B("The trap is to share out 90 instead, which gives 45. But 90 is the total for complementary angles. Supplementary means 180.",
      W("t", "90 ÷ 2 = 45")),
    B("So when two equal angles make a total, just halve the total."),
    check=("x", 90),
)

LESSONS[P + "026"] = lesson(
    B("Two complementary angles. One is x degrees and the other is x plus x degrees. We need to find x.",
      GIVEN("q", "Complementary angles: x° and (x + x)°")),
    B("What do complementary angles add up to?",
      ask=choose(["180°", "90°", "360°"], 1,
                 "180 degrees is for supplementary angles. Complementary angles fit into a right angle, which is 90 degrees.")),
    B("So the first angle plus the second angle makes 90. Let's write that down.",
      W("l1", "x + (x + x) = 90"), FIG("f1", in_corner({"label": "x"}, {"label": "x + x"}))),
    B("Now count the x's on the left. How many are there altogether?",
      ask=choose(["2", "3", "1"], 1,
                 "Count every x you can see: one outside the bracket, and two inside it.")),
    B("3 of them. So 3 x equals 90.",
      G("l1", ["x", ("x", 2), ("x", 3)], "3x"), W("l2", "3x = 90")),
    B("3 times x is 90, so we divide both sides by 3. 90 divided by 3 is 30.",
      DIV("l2", "3"), ANS("l3", "x = 30"), M("l3", "x = 30", "circle")),
    B("Check. The first angle is 30. The second is 30 plus 30, which is 60. And 30 plus 60 is 90. Complementary!",
      W("c1", "30 + 30 = 60"), W("c2", "30 + 60 = 90")),
    B("The trap is to forget the first x and write 2 x equals 90. That gives 45, and then the angles would be 45 and 90. Far too much.",
      W("t", "90 ÷ 2 = 45")),
    B("So: write the total as an equation, gather the x's, and divide."),
    check=("x", 30),
)

# ── Naming an angle by its size ──────────────────────────────────────────────

LESSONS[P + "036"] = lesson(
    B("An angle is bigger than 90 degrees but smaller than 180 degrees. What is it called?",
      GIVEN("q", "An angle between 90° and 180° is called ...?")),
    B("Let's line up the angle names by size. The smallest kind is sharp and pointy, less than 90 degrees. That is an acute angle.",
      L("l1", "Less than 90°: acute"),
      FIG("f1", {"kind": "angles", "layout": "single", "parts": [{"label": "acute", "size": 40}]})),
    B("Exactly 90 degrees is the square corner, like the corner of your notebook. What is that one called?",
      ask=choose(["a straight angle", "a right angle", "an obtuse angle"], 1,
                 "A straight angle is a flat line, 180 degrees. The square corner, exactly 90 degrees, is the right angle.")),
    B("A right angle. And exactly 180 degrees is a flat, straight line, called a straight angle.",
      L("l2", "Exactly 90°: right angle"), L("l4", "Exactly 180°: straight angle")),
    B("Our angle sits between those two. Wider than a square corner, but not yet flat. Like a book opened wide, or a hand fan.",
      L("l3", "Between 90° and 180°: ?"),
      FIG("f2", {"kind": "angles", "layout": "single", "parts": [{"label": "?", "size": 130}]})),
    B("Which name fills that gap?",
      ask=choose(["acute", "right", "obtuse"], 2,
                 "Acute is the small, sharp one, under 90 degrees. Right is exactly 90. The wide one, between 90 and 180, has a different name.")),
    B("Obtuse. An angle between 90 degrees and 180 degrees is an obtuse angle.",
      ANS("a", "Between 90° and 180°: obtuse angle", True), M("a", "obtuse angle", "circle")),
    B("A way to remember: acute is a cute little angle. Obtuse is the big, wide one."),
    B("So learn the two fence posts, 90 and 180. Below 90 is acute, and between them is obtuse."),
)
