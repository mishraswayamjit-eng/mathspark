"""Figures for the imported Grade 5 Angles & Lines questions (node gr5_angles).
Run through imported_geometry.py.

Where two lines cross, the parts run clockwise from the top. A part the question
says nothing about still needs a label in the contract, so it is called p or q
(as the templated figures do)."""
from imported_geometry_lib import add, skip, n, A, CLOCK, COMPASS, tri_angles


def deg(x):
    return "%s°" % n(x)


def cross(parts, note=None, hl=None):
    return A("crossing", parts, note, hl)


def line(parts, note=None, hl=None):
    return A("onLine", parts, note, hl)


def corner(parts, note=None, hl=None):
    return A("inRightAngle", parts, note, hl)


STRAIGHT = "Angles on a straight line add up to 180°"
FACING = "Angles facing each other across a crossing are equal"


# ── One angle given where two lines cross (or on a straight line): the one next to it ──

def adjacent(key, a, before, s_line, s_calc=None, s_ans=None, s_pair=None):
    b = 180 - a
    crossing = cross([(deg(a), a), ("?",), ("p",), ("q",)])
    pair = line([(deg(a), a), ("?",)])
    steps = {s_line: line([(deg(a), a), ("?",)], note=STRAIGHT)}
    if s_pair is not None:
        steps[s_pair] = cross([(deg(a), a), ("?",), ("p",), ("q",)], hl=["p0", "p1"], note="These two angles sit side by side on one straight line")
    if s_calc is not None:
        steps[s_calc] = line([(deg(a), a), ("?",)], hl=["p1"], note="? = 180° − %s" % deg(a))
    if s_ans is not None:
        steps[s_ans] = line([(deg(a), a), (deg(b), b)], hl=["p1"], note="180° − %s = %s" % (deg(a), deg(b)))
    add(key, figure=crossing if before == "cross" else pair, steps=steps)


adjacent("40e395f6", 65, "cross", s_line=0, s_calc=1, s_ans=2)
adjacent("62647a3d", 65, "cross", s_pair=0, s_line=1, s_calc=2, s_ans=3)
adjacent("9994fe74", 65, "cross", s_pair=0, s_line=1, s_ans=2)
adjacent("edcfe902", 65, "cross", s_line=0, s_calc=1, s_ans=2)
adjacent("51c32ebb", 65, "line", s_line=0, s_calc=1, s_ans=2)
adjacent("8920f4d6", 53, "line", s_line=0, s_calc=1, s_ans=2)


# ── A third line from the crossing point cuts an angle into two equal parts ──

def halve_adjacent(key, a, s_line, s_next, s_ans, s_half=None):
    """The angle next to `a` is halved. Drawn on the straight line: a, then the two halves."""
    b = 180 - a
    h = b / 2.0
    steps = {s_line: line([(deg(a), a), ("?",)], note=STRAIGHT),
             s_next: line([(deg(a), a), (deg(b), b)], hl=["p1"], note="180° − %s = %s" % (deg(a), deg(b))),
             s_ans: line([(deg(a), a), (deg(h), h), (deg(h), h)], hl=["p1", "p2"], note="%s ÷ 2 = %s" % (deg(b), deg(h)))}
    if s_half is not None:
        steps[s_half] = line([(deg(a), a), ("?",), ("?",)], hl=["p1", "p2"], note="The third line cuts the %s angle in half" % deg(b))
    add(key, figure=line([(deg(a), a), ("?",), ("?",)], note="A third line cuts the angle next to %s into two equal parts" % deg(a)), steps=steps)


halve_adjacent("00efe1c8", 72, s_line=0, s_next=1, s_half=2, s_ans=3)
halve_adjacent("8f3d128d", 65, s_line=0, s_next=1, s_ans=2)


def halve_opposite(key, a, s_facing, s_half, s_ans, s_calc=None):
    """The angle facing `a` is halved. Two crossing lines and the third line as a ray."""
    b = 180 - a
    h = a / 2.0

    def fig(l1, l2, **extra):
        # No size for an unknown part: the two share what is left, which is exactly half each.
        halves = [(l,) if l == "?" else (l, h) for l in (l1, l2)]
        return A("aroundPoint", [(deg(a), a), ("p", b)] + halves + [("q", b)], **extra)

    steps = {s_facing: cross([(deg(a), a), ("p",), (deg(a),), ("q",)], hl=["p0", "p2"], note=FACING),
             s_half: fig("?", "?", hl=["p2", "p3"], note="The third line cuts this %s angle in half" % deg(a)),
             s_ans: fig(deg(h), deg(h), hl=["p2", "p3"], note="%s ÷ 2 = %s" % (deg(a), deg(h)))}
    if s_calc is not None:
        steps[s_calc] = fig("?", "?", hl=["p2", "p3"], note="? = %s ÷ 2" % deg(a))
    add(key, figure=fig("?", "?", note="A third line cuts the angle opposite %s into two equal parts" % deg(a)), steps=steps)


halve_opposite("0bcee95c", 72, s_facing=0, s_half=1, s_calc=2, s_ans=3)
halve_opposite("d9ae9510", 65, s_facing=0, s_half=1, s_calc=2, s_ans=3)


# ── One angle is 3 times the angle next to it ────────────────────────────────
# Before answering, no part is given a size (the contract: only a part whose size the
# question states), so the renderer draws its stock crossing. The step figures, which
# are the solution, are drawn at the true 45° and 135°.

WORDS = line([("small", 45), ("3 × small",)], note=STRAIGHT)
X_PAIR = line([("x°", 45), ("3x°",)], note="x + 3x = 180°")
FOUR_X = line([("x°", 45), ("3x°",)], note="4x = 180°")
ALL_FOUR = cross([("45°", 45), ("135°",), ("45°",), ("135°",)], note=FACING)


def answer_pair(hl, note="45° + 135° = 180°"):
    return line([("45°", 45), ("135°",)], hl=hl, note=note)


SMALL_ASKED = cross([("?",), ("3 × ?",), ("p",), ("q",)], note="One angle is 3 times the angle next to it")
LARGE_ASKED = cross([("small",), ("?",), ("p",), ("q",)], note="The angle marked ? is 3 times the small angle")

add("2def0f90", figure=LARGE_ASKED, steps={0: WORDS, 1: X_PAIR, 4: line([("x°", 45), ("3x°",)], hl=["p1"], note="The larger angle is 3x°"), 5: ALL_FOUR})
add("33b0f63c", figure=SMALL_ASKED, steps={0: WORDS, 1: X_PAIR, 3: FOUR_X, 4: answer_pair(["p0"])})
add("46a665e2", figure=SMALL_ASKED, steps={0: WORDS, 1: X_PAIR, 3: FOUR_X, 4: answer_pair(["p0"])})
add("52dd3f2c", figure=SMALL_ASKED, steps={0: WORDS, 1: X_PAIR, 4: answer_pair(["p0"])})
add("cbcf98a0", figure=SMALL_ASKED, steps={0: WORDS, 1: X_PAIR, 3: answer_pair(["p0"])})
add("19d857d5",
    figure=cross([("?",), ("?",), ("?",), ("?",)], note="One angle is 3 times the angle next to it. Find all four."),
    steps={0: line([("x°", 45), ("3x°",)], note="Call one angle x°: the one next to it is 3x°"), 1: X_PAIR, 3: ALL_FOUR})

# ... and then a third line through the point halves the large angle (so it halves both large angles).
SIX = "The large angle is 3 times the small one. A third line halves it."


def six(l, note=None, hl=None, before=False):
    """Three lines through a point: small, half, half, small, half, half."""
    if before:                                   # nothing is stated yet: no sizes
        return A("aroundPoint", [("small",), ("?",), ("?",), ("small",), ("?",), ("?",)], note, hl)
    small = ("45°", 45)
    half = (l,) if l == "?" else (l, 67.5)       # unknown parts share what is left: 67.5° each
    return A("aroundPoint", [small, half, half, small, half, half], note, hl)


add("1984a5bf", figure=six("?", SIX, before=True),
    steps={0: line([("x°", 45), ("3x°",)], note="Call the small angle x°: the large one is 3x°"), 1: X_PAIR,
           3: answer_pair(["p1"], "3 × 45° = 135°"),
           4: six("?", "The third line cuts each 135° angle in half", ["p1", "p2"]),
           5: six("67.5°", "135° ÷ 2 = 67.5°", ["p1", "p2"])})
add("e2b4be33", figure=six("?", SIX, before=True),
    steps={0: line([("x°", 45), ("3x°",)], note="Call the small angle x°: the large one is 3x°"), 1: X_PAIR,
           2: ALL_FOUR,
           3: six("?", "The third line cuts each 135° angle in half", ["p1", "p2"]),
           4: six("67.5°", "135° ÷ 2 = 67.5°", ["p1", "p2"])})

# ... and then a triangle that uses the small angle.
add("d68deb3e", origin="authored",
    figure=cross([("small",), ("3 × small",), ("p",), ("q",)], note="A triangle has angles: small, 50° and ?"),
    steps={0: WORDS, 1: X_PAIR, 2: ALL_FOUR,
           3: tri_angles(85, 45, 50, "?", "45°", "50°", note="The triangle: 45°, 50° and ?"),
           4: tri_angles(85, 45, 50, "85°", "45°", "50°", hl=["a"], note="180° − 45° − 50° = 85°")})


# ── One-offs: lines and crossings ────────────────────────────────────────────

add("0666aacf", origin="authored",
    figure=line([("58°", 58), ("?",), ("75°", 75)]),
    steps={0: line([("58°", 58), ("?",), ("75°", 75)], note="The three angles together make a straight line: 180°"),
           1: line([("58°", 58), ("?",), ("75°", 75)], hl=["p0", "p2"], note="58° + 75° = 133°"),
           2: line([("58°", 58), ("?",), ("75°", 75)], hl=["p1"], note="? = 180° − 133°"),
           3: line([("58°", 58), ("47°", 47), ("75°", 75)], hl=["p1"], note="180° − 133° = 47°")})

add("7d808fa7", origin="authored",
    figure=line([("?",), ("?",)], note="Three ribbons from one point. The two gaps between them are equal."),
    steps={0: line([("?",), ("?",)], note="The two outer ribbons make a straight line: 180°"),
           1: line([("?",), ("?",)], hl=["p0", "p1"], note="3 ribbons make 2 gaps"),
           2: line([("90°", 90), ("90°", 90)], note="180° ÷ 2 = 90°")})

SIX_AT_O = [("35°", 35), ("85°", 85), ("?",), ("p", 35), ("q", 85), ("r",)]
add("8a008d60", origin="authored",
    figure=A("aroundPoint", SIX_AT_O, note="Three straight lines through O. Going clockwise: 35°, 85°, then ?"),
    steps={0: A("aroundPoint", SIX_AT_O, note="The six angles at O make a full turn: 360°"),
           1: line([("35°", 35), ("85°", 85), ("?",)], note="These three sit on one side of a straight line: 180°"),
           2: line([("35°", 35), ("85°", 85), ("60°", 60)], hl=["p2"], note="180° − 35° − 85° = 60°"),
           3: A("aroundPoint", [("35°", 35), ("85°", 85), ("60°", 60), ("35°", 35), ("85°", 85), ("60°", 60)],
                note="Angles facing each other are equal: 35°, 85°, 60°, twice")})

# Four lines make eight angles, more than the contract can draw: only the two lines that make the 70° angle are shown.
add("91eb5306", origin="authored",
    figure=cross([("70°", 70), ("p",), ("?",), ("q",)], note="Only the two lines that make the 70° angle are drawn"),
    steps={1: cross([("70°", 70), ("p",), ("?",), ("q",)], hl=["p0", "p2"], note=FACING),
           2: cross([("70°", 70), ("p",), ("?",), ("q",)], hl=["p0", "p2"], note="The same two lines make both angles"),
           3: cross([("70°", 70), ("p",), ("70°",), ("q",)], hl=["p2"], note="The opposite angle is also 70°")})

add("b2292806", origin="authored",
    figure=cross([("3x",), ("5x − 20°",), ("p",), ("q",)], note="Find x, and the smallest angle at the crossing"),
    steps={0: line([("3x", 75), ("5x − 20°",)], note="3x + (5x − 20°) = 180°"),
           3: line([("3x", 75), ("5x − 20°",)], note=["8x = 200°, so x = 25°", "x = 25°"]),
           4: line([("75°", 75), ("105°",)], note="3 × 25° = 75° and 5 × 25° − 20° = 105°"),
           5: cross([("75°", 75), ("105°",), ("75°",), ("105°",)], hl=["p0", "p2"], note="The smallest angle is 75°")})

add("bd76f893", origin="authored",
    figure=cross([("65°", 65), ("?",), ("?",), ("?",)], note="Add up the three angles marked ?"),
    steps={0: cross([("65°", 65), ("?",), ("?",), ("?",)], note="All four angles make a full turn: 360°"),
           1: cross([("65°", 65), ("?",), ("?",), ("?",)], hl=["p1", "p2", "p3"], note="360° − 65° = 295°"),
           2: cross([("65°", 65), ("115°",), ("65°",), ("115°",)], note="Check: 115° + 65° + 115° = 295°")})

add("e5c10ca9", origin="authored",
    figure=cross([("small",), ("2 × small",), ("?",), ("p",)], note="The angle marked ? faces the small angle"),
    steps={0: line([("x°", 60), ("2x°",)], note="x + 2x = 180°"),
           2: line([("60°", 60), ("120°",)], note="2 × 60° = 120°"),
           3: cross([("60°", 60), ("120°",), ("60°",), ("120°",)], hl=["p0", "p2"], note=FACING)})


# ── Inside a right angle ─────────────────────────────────────────────────────

def with_upright(key, a, s_right, s_calc, s_ans):
    """A string between flat ground and an upright line: a with the ground, ? with the upright."""
    b = 90 - a
    add(key, origin="authored",
        figure=corner([("?",), (deg(a), a)], note="An upright line, flat ground, and the kite string between them"),
        steps={s_right: corner([("?",), (deg(a), a)], note="Upright and flat meet at 90°"),
               s_calc: corner([("?",), (deg(a), a)], hl=["p0"], note="? = 90° − %s" % deg(a)),
               s_ans: corner([(deg(b), b), (deg(a), a)], hl=["p0"], note="90° − %s = %s" % (deg(a), deg(b)))})


with_upright("4783ddb3", 53, 0, 1, 2)
with_upright("e3b7c930", 55, 0, 1, 2)


def complement(key, label, size, answer, answer_size, s_rule, s_calc, s_ans):
    add(key, origin="authored",
        figure=corner([(label, size), ("?",)]),
        steps={s_rule: corner([(label, size), ("?",)], note="Complementary angles add up to 90°"),
               s_calc: corner([(label, size), ("?",)], hl=["p1"], note="? = 90° − %s" % label),
               s_ans: corner([(label, size), (answer, answer_size)], hl=["p1"], note="90° − %s = %s" % (label, answer))})


def supplement(key, label, size, answer, answer_size, s_rule, s_calc, s_ans):
    add(key, origin="authored",
        figure=line([(label, size), ("?",)]),
        steps={s_rule: line([(label, size), ("?",)], note="Supplementary angles add up to 180°"),
               s_calc: line([(label, size), ("?",)], hl=["p1"], note="? = 180° − %s" % label),
               s_ans: line([(label, size), (answer, answer_size)], hl=["p1"], note="180° − %s = %s" % (label, answer))})


complement("ch18_q002", "45½°", 45.5, "44½°", 44.5, 0, 1, 3)
complement("ch18_q019", "37½°", 37.5, "52½°", 52.5, 0, 2, 4)
supplement("ch18_q003", "100½°", 100.5, "79½°", 79.5, 0, 2, 4)
supplement("ch18_q020", "98¼°", 98.25, "81¾°", 81.75, 0, 1, 3)

add("ch18_q004", origin="authored",
    figure=corner([("?",), ("?",)], note="The two angles are equal"),
    steps={0: corner([("?",), ("?",)], note="Complementary angles add up to 90°"),
           1: corner([("x",), ("x",)], note="Call each angle x"),
           5: corner([("45°", 45), ("45°", 45)], note="90° ÷ 2 = 45°")})
for _key in ("ch18_q005", "ch18_q024"):
    add(_key, origin="authored",
        figure=line([("?",), ("?",)], note="The two angles are equal"),
        steps={0: line([("?",), ("?",)], note="Supplementary angles add up to 180°"),
               1: line([("x",), ("x",)], note="Call each angle x"),
               4: line([("90°", 90), ("90°", 90)], note="180° ÷ 2 = 90°")})
add("ch18_q026", origin="authored",
    figure=corner([("x°",), ("(x + x)°",)], note="The two angles are complementary (not drawn to size)"),
    steps={1: corner([("x°", 30), ("2x°",)], note="x + x is 2x"),
           3: corner([("x°", 30), ("2x°",)], note="x + 2x = 3x = 90°"),
           5: corner([("30°", 30), ("60°", 60)], note="30° + 60° = 90°")})


# ── Linear pairs: what kind of angle is the other one? ───────────────────────

KIND = "What kind of angle is the one marked ?"
PAIR = "A linear pair adds up to 180°"
for _key in ("ch18_q006", "ch18_q031"):
    add(_key, origin="authored",
        figure=line([("90°", 90), ("?",)], note=KIND),
        steps={0: line([("90°", 90), ("?",)], note=PAIR),
               2: line([("90°", 90), ("?",)], hl=["p1"], note="? = 180° − 90°"),
               3: line([("90°", 90), ("90°", 90)], hl=["p1"], note="Exactly 90°: a right angle")})
add("ch18_q007", origin="authored",
    figure=line([("acute", 50), ("?",)], note=KIND),
    steps={0: line([("acute", 50), ("?",)], note=PAIR),
           3: line([("acute", 50), ("?",)], hl=["p1"], note="180° take away less than 90° leaves more than 90°"),
           5: line([("35°", 35), ("145°",)], hl=["p1"], note="For example, 180° − 35° = 145°: an obtuse angle")})
add("ch18_q029", origin="authored",
    figure=line([("obtuse", 125), ("?",)], note=KIND),
    steps={0: line([("obtuse", 125), ("?",)], note=PAIR),
           3: line([("110°", 110), ("70°",)], hl=["p1"], note="For example, 180° − 110° = 70°"),
           4: line([("obtuse", 125), ("?",)], hl=["p1"], note="Less than 90°: an acute angle")})

# Names of angle pairs, and of one angle.
add("ch18_q015", origin="authored",
    figure=line([("angle 1", 110), ("angle 2",)], note="Angle 1 + angle 2 = 180°"),
    steps={2: line([("angle 1", 110), ("angle 2",)], note="Together they make a straight line")})
add("ch18_q016", origin="authored",
    figure=corner([("angle 1", 55), ("angle 2",)], note="Angle 1 + angle 2 = 90°"),
    steps={1: corner([("angle 1", 55), ("angle 2",)], note="Together they fill a right angle")})
add("ch18_q036", origin="authored",
    figure=A("single", [("?", 130)], note="Bigger than 90° but smaller than 180°. What is it called?"),
    steps={1: A("single", [("90°", 90)], note="A right angle is exactly 90°"),
           2: A("single", [("?", 130)], note="Wider than a right angle, but not yet a straight line")})

# Steps only: the question is sums until the last two steps.
add("ch18_q037", origin="authored",
    steps={2: line([("55°", 55), ("?",)], note="Supplementary angles add up to 180°"),
           3: line([("55°", 55), ("125°",)], hl=["p1"], note="180° − 55° = 125°")})


# ── Clocks and compasses ─────────────────────────────────────────────────────

add("7f9964f6", origin="authored",
    figure=CLOCK(4, 0, True, note="x is the shaded angle; y is the angle the other way round. y − x = ?"),
    steps={1: CLOCK(4, 0, True, hl=["angle"], note=["x = 4 gaps of 30° = 120°", "x is 4 gaps wide: 120°"]),
           2: CLOCK(4, 0, hl=["hour", "minute"], note="y is the rest of the full turn: 360° − 120° = 240°"),
           3: CLOCK(4, 0, True, note="y − x = 240° − 120° = 120°")})
HANDS_9 = CLOCK(9, 0, hl=["hour", "minute"], note="The minute hand is on 12, the hour hand on 9")
add("ch18_q001", origin="authored",
    figure=CLOCK(9, 0, True, note="Angle between the hands = ?"),
    steps={1: HANDS_9,
           2: CLOCK(9, 0, True, hl=["angle"], note="From 9 to 12 there are 3 gaps"),
           3: CLOCK(9, 0, True, hl=["angle"], note=["3 × 30° = 90°", "3 gaps make 90°"])})
add("ch18_q021", origin="authored",
    figure=CLOCK(9, 0, True, note="Angle between the hands = ?"),
    steps={0: HANDS_9,
           1: CLOCK(9, 0, True, hl=["angle"], note="From 9 to 12 there are 3 gaps"),
           3: CLOCK(9, 0, True, hl=["angle"], note=["3 × 30° = 90°", "3 gaps make 90°"])})
add("ch18_q022", origin="authored",
    figure=CLOCK(4, 0, True, note="Angle between the hands = ?"),
    steps={1: CLOCK(4, 0, hl=["hour", "minute"], note="The minute hand is on 12, the hour hand on 4"),
           2: CLOCK(4, 0, True, hl=["angle"], note="From 12 to 4 there are 4 gaps"),
           3: CLOCK(4, 0, True, hl=["angle"], note=["4 × 30° = 120°", "4 gaps make 120°"])})

add("ch18_q017", origin="authored",
    figure=COMPASS("E", note="Angle between East and South = ?"),
    steps={1: COMPASS("E", note="4 main directions share the full turn of 360°"),
           3: COMPASS("E", [(90, "clockwise")], end=True, hl=["t0"], note="East to South is a quarter turn: 90°")})
add("ch18_q035", origin="authored",
    figure=COMPASS("N", note="Angle between North and West = ?"),
    steps={1: COMPASS("N", note="4 main directions share the full turn of 360°"),
           3: COMPASS("N", [(90, "anticlockwise")], end=True, hl=["t0"], note="North to West is a quarter turn: 90°")})
add("ch18_q018", origin="authored",
    figure=COMPASS("W", note="Angle between West and North-East = ?"),
    steps={1: COMPASS("W", [(45, "clockwise")], hl=["t0"], note="Each step to the next direction is 45°"),
           2: COMPASS("W", [(45, "clockwise"), (45, "clockwise"), (45, "clockwise")], end=True, note="W → NW → N → NE: 3 steps of 45°"),
           4: COMPASS("W", [(135, "clockwise")], end=True, hl=["t0"], note="The shorter way round: 135°")})


# ── Left without a figure ────────────────────────────────────────────────────

skip("b22920c0", "contradiction",
     "rectangular tiles meet in right angles, yet the story measures 65° where they meet (the sum itself, 180° − 65°, is sound)")
skip("ch18_q010", "no-picture", "adding up the pairs in the answer choices: arithmetic, and a picture of a pair would point at the answer")
skip("ch18_q011", "no-picture", "adding up the pairs in the answer choices: arithmetic, and a picture of a pair would point at the answer")
skip("ch18_q027", "no-picture", "adding up the pairs in the answer choices: arithmetic, and a picture of a pair would point at the answer")
