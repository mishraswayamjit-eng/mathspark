"""Figures for the Grade 4 Angles questions (node gr4_angles).

    python -X utf8 scripts/figures/authoring/g4_gr4_angles.py                 # write the part file, print the summary
    python -X utf8 scripts/figures/authoring/g4_gr4_angles.py review [a] [b]  # also print questions beside their figures
    python -X utf8 scripts/figures/authoring/g4_gr4_angles.py review <id part>
    python -X utf8 scripts/figures/authoring/g4_gr4_angles.py skips

Writes data/question-figures/parts/g4-gr4_angles.json.

Where two lines cross, the parts run clockwise from the top. A part the question
says nothing about still needs a label in the contract, so it is called p or q
(as the Grade 5 figures do).
"""
import re
import sys

from g4_gr4_angles_kit import (Book, deg, line, corner, cross, around, single, unknown, CLOCK, COMPASS, BM,
                               tri_angles, CW, ACW)

book = Book("gr4_angles")
add = book.add
skip = book.skip

STRAIGHT = "Angles on a straight line add up to 180°"
FACING = "Angles facing each other across a crossing are equal"


# ══ Rules: families that differ only in their numbers ════════════════════════

def pair_rule(qid, a, total, short):
    """One angle given; find the angle that makes 180° (on a line) or 90° (in a right angle) with it."""
    b = total - a
    if book.answer_number(qid) != b:
        raise SystemExit("%s: the key is not %s" % (qid, b))
    make = line if total == 180 else corner
    word = "Supplementary" if total == 180 else "Complementary"
    given = (deg(a), a)
    before = make([given, unknown(b)])
    rule = make([given, unknown(b)], note="%s angles add up to %s" % (word, deg(total)))
    calc = make([given, unknown(b)], hl=["p1"], note="? = %s − %s" % (deg(total), deg(a)))
    if short:
        steps = {0: rule, 1: make([given, (deg(b), b)], hl=["p1"], note="%s − %s = %s" % (deg(total), deg(a), deg(b)))}
    else:
        steps = {0: rule, 1: calc, 2: make([given, (deg(b), b)], hl=["p1"], note="%s + %s = %s" % (deg(a), deg(b), deg(total)))}
    add(qid, figure=before, steps=steps, origin="rule")


def x_on_line_rule(qid, a):
    """Two angles on a straight line are x° and a°."""
    b = 180 - a
    if book.answer_number(qid) != b:
        raise SystemExit("%s: the key is not %s" % (qid, b))
    add(qid, origin="rule",
        figure=line([unknown(b, "x°"), (deg(a), a)]),
        steps={0: line([unknown(b, "x°"), (deg(a), a)], note=STRAIGHT),
               1: line([(deg(b), b), (deg(a), a)], hl=["p0"], note="x = 180° − %s = %s" % (deg(a), deg(b)))})


def opposite_rule(qid, a):
    """Two straight lines cross; one angle is a°; find the one facing it."""
    if book.answer_number(qid) != a:
        raise SystemExit("%s: the key is not %s" % (qid, a))
    parts = [(deg(a), a), ("p",), ("?",), ("q",)]
    add(qid, origin="rule",
        figure=cross(parts),
        steps={0: cross(parts, hl=["p0", "p2"], note=FACING),
               1: cross([(deg(a), a), ("p",), (deg(a),), ("q",)], hl=["p2"], note="The opposite angle is also %s" % deg(a))})


RULES = [
    (re.compile(r"^What is the (supplement|complement) of an angle of (\d+)°\?$"),
     lambda qid, m: pair_rule(qid, int(m.group(2)), 180 if m.group(1) == "supplement" else 90, False)),
    (re.compile(r"^Find the (supplementary|complementary) angle of (\d+)°\.$"),
     lambda qid, m: pair_rule(qid, int(m.group(2)), 180 if m.group(1) == "supplementary" else 90, False)),
    (re.compile(r"^Two angles are supplementary\. If one angle is (\d+)°, find the other\.$"),
     lambda qid, m: pair_rule(qid, int(m.group(1)), 180, True)),
    (re.compile(r"^Two angles on a straight line are x° and (\d+)°\. Find x\.$"),
     lambda qid, m: x_on_line_rule(qid, int(m.group(1)))),
    (re.compile(r"^Two straight lines cross\. One angle formed is (\d+)°\. Find the vertically opposite angle\.$"),
     lambda qid, m: opposite_rule(qid, int(m.group(1)))),
]

GENERATED = re.compile(r"^(Q_CH\d+_\d+_V\d+|VAR_G4_.*|PH3_.*)$")
for _qid in sorted(book.questions):
    if not GENERATED.match(_qid):
        continue
    _q = book.q(_qid)
    _steps = len(_q.get("stepByStep") or [])
    for _pattern, _build in RULES:
        _m = _pattern.match(_q["questionText"].strip())
        if _m:
            _expected = 2 if _qid.startswith("PH3_") else 3
            if _steps != _expected:
                raise SystemExit("%s: expected %d steps, has %d" % (_qid, _expected, _steps))
            _build(_qid, _m)
            break


# ══ Individually drawn: one given angle, find its partner ════════════════════

def comp_supp_sum(qid, a, s_comp, s_supp):
    """Add the complement and the supplement of a°. (The two answers are never stated
    in the step texts, so the step figures keep them as ?.)"""
    add(qid,
        figure=single(deg(a), a, note="Find its complement and its supplement, then add them"),
        steps={s_comp: corner([(deg(a), a), ("?",)], hl=["p1"], note="Complement: ? = 90° − %s" % deg(a)),
               s_supp: line([(deg(a), a), ("?",)], hl=["p1"], note="Supplement: ? = 180° − %s" % deg(a))})


comp_supp_sum("EXT_G4_FP_2021_016", 35, 0, 1)
comp_supp_sum("EXT_G4_FP_2023_008", 48, 0, 1)
comp_supp_sum("EXT_G4_FP_2024_003", 48, 0, 1)
comp_supp_sum("PYQ_2018_Q29", 35, 0, 1)

add("PYQ_2016_Q34",
    figure=line([("57¼°", 57.25), ("?",)]),
    steps={0: line([("57¼°", 57.25), ("?",)], note="Supplementary angles add up to 180°"),
           1: line([("57¼°", 57.25), ("?",)], hl=["p1"], note="First the whole number: 180° − 57° = 123°"),
           2: line([("57¼°", 57.25), ("?",)], hl=["p1"], note="One quarter less than 123° is 122¾°"),
           3: line([("57¼°", 57.25), ("122¾°", 122.75)], hl=["p1"], note="57¼° + 122¾° = 180°")})

add("Q_CH18_004",
    figure=corner([("67½°", 67.5), ("?",)]),
    steps={0: corner([("67½°", 67.5), ("?",)], note="Complementary angles add up to 90°"),
           1: corner([("67½°", 67.5), ("?",)], hl=["p1"], note="First the whole degrees: 90° − 67° = 23°"),
           2: corner([("67½°", 67.5), ("?",)], hl=["p1"], note="Half a degree less than 23° is 22½°"),
           3: corner([("67½°", 67.5), ("22½°", 22.5)], hl=["p1"], note="67½° + 22½° = 90°")})

add("Q_CH18_005",
    figure=line([("55°", 55), ("?",)]),
    steps={0: line([("55°", 55), ("?",)], note="Supplementary angles add up to 180°, like angles on a line"),
           1: line([("55°", 55), ("?",)], hl=["p1"], note="? = 180° − 55°"),
           2: line([("55°", 55), ("125°", 125)], hl=["p1"], note="180° − 55° = 125°")})

add("Q_CH18_010",
    figure=line([("65°", 65), ("?",)]),
    steps={0: line([("65°", 65), ("?",)], note="A linear pair sits on a straight line: 180° together"),
           1: line([("65°", 65), ("?",)], hl=["p1"], note="? = 180° − 65°"),
           2: line([("65°", 65), ("115°", 115)], hl=["p1"], note="180° − 65° = 115°")})

add("Q_CH18_006",
    figure=corner([("x",), ("35°", 35)], note="x + 35° = 90°. Find the supplement of x."),
    steps={0: corner([("x = 55°", 55), ("35°", 35)], hl=["p0"], note="x = 90° − 35° = 55°"),
           1: line([("55°", 55), ("?",)], note="The supplement of x makes 180° with it"),
           2: line([("55°", 55), ("125°", 125)], hl=["p1"], note="180° − 55° = 125°")})

add("Q_CH18_007",
    figure=line([("angle",), ("125°", 125)], note="The angle's supplement is 125°. Find its complement."),
    steps={0: line([("55°", 55), ("125°", 125)], hl=["p0"], note="The angle is 180° − 125° = 55°"),
           1: corner([("55°", 55), ("?",)], hl=["p1"], note="Its complement: ? = 90° − 55°"),
           2: corner([("55°", 55), ("35°", 35)], hl=["p1"], note="90° − 55° = 35°")})

add("G4A_ANGLES_001",
    figure=line([("48°", 48), ("67°", 67), ("?",)]),
    steps={0: line([("48°", 48), ("67°", 67), ("?",)], note=STRAIGHT),
           1: line([("48°", 48), ("67°", 67), ("?",)], hl=["p0", "p1"], note="48° + 67° = 115°"),
           2: line([("48°", 48), ("67°", 67), ("?",)], hl=["p2"], note="? = 180° − 115°"),
           3: line([("48°", 48), ("67°", 67), ("65°", 65)], hl=["p2"], note="180° − 115° = 65°")})

add("Q_CH18_022",
    figure=around([("110°", 110), ("85°", 85), ("x°",)]),
    steps={0: around([("110°", 110), ("85°", 85), ("x°",)], note="All the way round a point is 360°"),
           1: around([("110°", 110), ("85°", 85), ("x°",)], hl=["p0", "p1"], note="Add the two angles you know: 110° and 85°"),
           2: around([("110°", 110), ("85°", 85), ("x°",)], hl=["p2"], note="x = 360° − 110° − 85°"),
           3: around([("110°", 110), ("85°", 85), ("165°", 165)], hl=["p2"], note="x = 165°")})

add("G4A_ANGLES_010",
    figure=around([("80°", 80), ("?",), ("?",), ("?",), ("?",)], note="The four angles marked ? are equal"),
    steps={0: around([("80°", 80), ("?",), ("?",), ("?",), ("?",)], hl=["p1", "p2", "p3", "p4"], note="360° − 80° = 280° for the four equal angles"),
           1: around([("80°", 80), ("?",), ("?",), ("?",), ("?",)], hl=["p1", "p2", "p3", "p4"], note="280° shared equally among the four angles"),
           2: around([("80°", 80), ("70°", 70), ("70°", 70), ("70°", 70), ("70°", 70)], hl=["p1", "p2", "p3", "p4"], note="Each equal angle is 70°")})

add("Q_CH18_023",
    figure=line([("x°", 30), ("2x°", 60), ("3x°", 90)]),
    steps={0: line([("x°", 30), ("2x°", 60), ("3x°", 90)], note=STRAIGHT),
           1: line([("x°", 30), ("2x°", 60), ("3x°", 90)], note="x + 2x + 3x = 6 lots of x"),
           2: line([("x°", 30), ("2x°", 60), ("3x°", 90)], note="6 lots of x make 180°, so x = 180° ÷ 6"),
           3: line([("30°", 30), ("60°", 60), ("90°", 90)], note="30° + 60° + 90° = 180°")})

add("Q_CH18_020",
    figure=corner([("2 parts", 36), ("3 parts", 54)], note="Two complementary angles in the ratio 2:3"),
    steps={0: corner([("2 parts", 36), ("3 parts", 54)], note="2 + 3 = 5 equal parts make 90°"),
           1: corner([("2 parts", 36), ("3 parts", 54)], note="Share 90° into 5 equal parts to find one part"),
           2: corner([("2 parts", 36), ("3 parts", 54)], hl=["p0"], note="The smaller angle has 2 of these parts: 36°"),
           3: corner([("36°", 36), ("54°", 54)], hl=["p0"], note="36° + 54° = 90°")})

add("EXT_G4_FP_2021_029",
    figure=BM([("Angle", [(1, "?", "unknown")]), ("Supplement", [(1, None, "a")] * 5)],
              note="The angle is one fifth of its supplement. Together they make 180°."),
    steps={0: BM([("Angle", [(1, "1 part", "b")]), ("Supplement", [(1, None, "a")] * 5)], note="Angle: 1 part. Supplement: 5 parts."),
           1: BM([("Angle", [(1, "1 part", "b")]), ("Supplement", [(1, None, "a")] * 5)], note="Together: 6 parts make 180°"),
           2: BM([("Angle", [(1, "30°", "b")]), ("Supplement", [(1, "30°", "a")] * 5)], hl=["b0"], note="One part = 180° ÷ 6 = 30°"),
           3: line([("30°", 30), ("150°", 150)], hl=["p0"], note="30° + 150° = 180°, and one fifth of 150° is 30°")})

add("G4A_ANGLES_008",
    figure=BM([("Complement", [(1, "?", "unknown")]), ("Supplement", [(1, "?", "unknown")] * 3)],
              note="The supplement is 3 times the complement"),
    steps={0: BM([("Complement", [(1, "c", "a")]), ("Supplement", [(1, "c", "a"), (2, "90° more", "b")])],
                 note="The supplement is 90° more than the complement"),
           1: BM([("Complement", [(1, "c", "a")]), ("Supplement", [(1, "c", "a"), (1, "c", "b"), (1, "c", "b")])], hl=["b1s1", "b1s2"],
                 note="The extra 90° is 2 times the complement"),
           2: corner([("angle",), ("45°", 45)], hl=["p0"], note="The complement is 45°, so the angle is 90° − 45°"),
           3: line([("45°", 45), ("135°", 135)], note="The angle is 45°. Its supplement, 135°, is 3 × 45°.")})

add("G4A_ANGLES_020",
    figure=BM([("Angle", [(1, "?", "unknown"), (1, "30°", "b")]), ("Complement", [(1, "?", "unknown")])],
              note="The angle is 30° more than its complement. Together: 90°."),
    steps={0: BM([("Angle", [(1, "30°", "a"), (1, "30°", "b")]), ("Complement", [(1, "30°", "a")])],
                 note="90° − 30° = 60°, and half of 60° is 30°"),
           1: corner([("60°", 60), ("30°", 30)], hl=["p0"], note="Complement 30°, so the angle is 30° + 30° = 60°"),
           2: line([("60°", 60), ("?",)], hl=["p1"], note="Supplement: ? = 180° − 60°"),
           3: line([("60°", 60), ("120°", 120)], hl=["p1"], note="180° − 60° = 120°")})

add("Q_CH18_021",
    figure=BM([("Larger", [(7, "?", "unknown"), (4, "40°", "b")]), ("Smaller", [(7, "?", "unknown")])],
              note="Two supplementary angles: together they make 180°"),
    steps={0: BM([("Larger", [(7, "smaller", "a"), (4, "40°", "b")]), ("Smaller", [(7, "smaller", "a")])],
                 note="The larger angle is the smaller angle and 40° extra"),
           1: BM([("Larger", [(7, "smaller", "a"), (4, "40°", "b")]), ("Smaller", [(7, "smaller", "a")])], hl=["b0s0", "b1s0"],
                 note="Take away the extra 40°: two copies of the smaller are left"),
           2: BM([("Larger", [(7, "smaller", "a"), (4, "40°", "b")]), ("Smaller", [(7, "smaller", "a")])], hl=["b1s0"],
                 note="Halve 140° to find the smaller angle"),
           3: line([("110°", 110), ("70°", 70)], hl=["p0"], note="70° + 40° = 110°, and 110° + 70° = 180°")})


# ══ Two lines crossing ═══════════════════════════════════════════════════════

add("Q_CH18_009",
    figure=cross([("70°", 70), ("p",), ("?",), ("q",)]),
    steps={0: cross([("70°", 70), ("p",), ("?",), ("q",)], note="Two crossing lines make two pairs of angles that face each other"),
           1: cross([("70°", 70), ("p",), ("?",), ("q",)], hl=["p0", "p2"], note="Vertically opposite angles are always equal"),
           2: cross([("70°", 70), ("p",), ("70°",), ("q",)], hl=["p2"], note="The opposite angle is also 70°")})

add("Q_CH18_008",
    figure=cross([("a",), ("b",), ("c",), ("d",)], note="Two lines cross. How many pairs face each other?"),
    steps={0: cross([("a",), ("b",), ("c",), ("d",)], note="Two crossing lines make 4 angles around the point"),
           1: cross([("a",), ("b",), ("c",), ("d",)], hl=["p0", "p2"], note="a faces c: one pair. b faces d: another pair."),
           2: cross([("a",), ("b",), ("c",), ("d",)], note="Every angle is in a pair: 2 pairs")})

# Before answering no part has a stated size, so the renderer draws its stock crossing.
add("G4A_ANGLES_009",
    figure=cross([("small",), ("4 × small",), ("p",), ("q",)], note="One angle is 4 times the angle beside it"),
    steps={0: line([("small", 36), ("4 × small",)], note=STRAIGHT),
           1: line([("1 part", 36), ("4 parts",)], note="1 part + 4 parts = 5 parts in all"),
           2: line([("36°", 36), ("144°",)], hl=["p1"], note="The larger angle is 4 parts: 144°"),
           3: cross([("36°", 36), ("144°",), ("36°",), ("144°",)], hl=["p1", "p3"], note="The largest angle formed is 144°")})

add("G4A_ANGLES_019",
    figure=cross([("a",), ("b",), ("c",), ("?",)], note="a + b + c = 250°. Find the smallest of the four angles."),
    steps={0: cross([("a",), ("b",), ("c",), ("110°", 110)], hl=["p3"], note="A whole turn is 360°: 360° − 250° = 110°"),
           1: line([("110°", 110), ("?",)], hl=["p1"], note="The angle beside it: 180° − 110° = 70°"),
           2: cross([("70°", 70), ("110°",), ("70°",), ("110°",)], note=FACING),
           3: cross([("70°", 70), ("110°",), ("70°",), ("110°",)], hl=["p0", "p1", "p2"], note="Check: 70° + 110° + 70° = 250°"),
           4: cross([("70°", 70), ("110°",), ("70°",), ("110°",)], hl=["p0", "p2"], note="The smallest angle is 70°")})


# ══ Naming angles and pairs ══════════════════════════════════════════════════

add("EXT_G4_WS2_CH18_004",
    figure=single("less than 90°", 50, note="What is an angle like this called?"),
    steps={0: single("90°", 90, note="A right angle is exactly 90°"),
           1: single("less than 90°", 50, note="Smaller than a right angle"),
           2: single("acute", 50, note="An angle less than 90° is an acute angle")})

add("EXT_G4_WS2_CH18_005",
    figure=corner([("?",)], note="A right angle, like the corner of a square"),
    steps={0: around([("?",), ("?",), ("?",), ("?",)], hl=["p0"], note="A full turn is 360°. A right angle is a quarter turn."),
           1: around([("?",), ("?",), ("?",), ("?",)], hl=["p0"], note="Share 360° into 4 equal parts"),
           2: corner([("90°",)], hl=["p0"], note="A right angle measures 90°")})

add("EXT_G4_WS2_CH18_006",
    figure=single("180°", 180, note="What is an angle of 180° called?"),
    steps={0: around([("180°", 180), ("180°", 180)], hl=["p0"], note="180° is half of a full turn"),
           1: single("180°", 180, note="The two arms point opposite ways and make a straight line"),
           2: single("straight angle", 180)})

add("EXT_G4_WS2_CH18_007",
    figure=single("135°", 135, note="What type of angle is this?"),
    steps={0: single("135°", 135, note="135° is more than 90°: wider than a right angle"),
           1: single("135°", 135, note="135° is less than 180°: not yet a straight line"),
           2: single("obtuse", 135, note="Between 90° and 180°: an obtuse angle")})

add("EXT_G4_WS2_CH18_008",
    figure=corner([("angle 1", 55), ("angle 2",)], note="Angle 1 + angle 2 = 90°"),
    steps={0: corner([("angle 1", 55), ("angle 2",)], note="Together they make a right angle"),
           1: corner([("30°", 30), ("60°", 60)], note="For example, 30° + 60° = 90°"),
           2: corner([("angle 1", 55), ("angle 2",)], note="Such a pair of angles is called complementary")})

add("EXT_G4_FP_2022_008",
    figure=line([("obtuse", 125), ("?",)], note="What kind of angle is the one marked ?"),
    steps={0: single("obtuse", 125, note="Obtuse: more than 90° and less than 180°"),
           1: line([("obtuse", 125), ("?",)], hl=["p1"], note="180° take away more than 90° leaves less than 90°"),
           2: line([("110°", 110), ("70°",)], hl=["p1"], note="For example, 180° − 110° = 70°"),
           3: line([("obtuse", 125), ("acute",)], hl=["p1"], note="Less than 90°: always an acute angle")})

add("Q_CH18_001",
    figure=single("?", 130, note="Bigger than 90° but smaller than 180°. What is it called?"),
    steps={0: single("90°", 90, note="Exactly 90° is a right angle. Smaller than that is acute."),
           1: single("reflex", 250, note="Bigger than 180°: a reflex angle"),
           2: single("obtuse", 130, note="In between, from 90° to 180°: an obtuse angle")})

add("Q_CH18_002",
    figure=single("250°", 250, note="What kind of angle is this?"),
    steps={0: single("180°", 180, note="A straight angle is exactly 180°. A complete angle is 360°."),
           1: single("250°", 250, note="250° is more than 180° but less than 360°"),
           2: single("reflex angle", 250, note="Between 180° and 360°: a reflex angle")})

add("G4A_ANGLES_021",
    figure=corner([("P",), ("Q",)], note="P + Q = 90°, and Q + R = 180°"),
    steps={0: corner([("P = 20°", 20), ("Q = 70°", 70)], note="Try P = 20°: then Q = 70° and R = 110°"),
           1: corner([("P = 40°", 40), ("Q = 50°", 50)], note="Try P = 40°: then Q = 50° and R = 130°")})

add("G4A_ANGLES_022",
    figure=single("70°", 70, note="This is angle AOB. A ray OC makes 30° with OB."),
    steps={0: single("70°", 70, note="OC makes 30° with OB, on either side of OB"),
           1: single("100°", 100, note="OC on the side away from OA: 70° + 30° = 100°"),
           2: single("40°", 40, note="OC between OA and OB: 70° − 30° = 40°")})

# The three angles drawn to size would show the answer (a straight angle), so the
# before-answering figure is a bar in the same proportions instead.
add("G4A_ANGLES_018",
    figure=BM([("Angles", [(1, "first", "a"), (2, "second", "b"), (3, "third", "c")], "360°")],
              note="The second is twice the first. The third is three times the first."),
    steps={1: around([("1 part", 60), ("2 parts", 120), ("3 parts", 180)], note="1 + 2 + 3 = 6 parts fill the whole turn of 360°"),
           2: around([("1 part", 60), ("2 parts", 120), ("3 parts", 180)], hl=["p2"], note="The largest angle is 3 parts: 180°"),
           3: single("180°", 180, note="An angle of 180° makes a straight line")})


# ══ Turns that are part of a full turn ═══════════════════════════════════════

add("G4A_ANGLES_002",
    figure={"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 8, "shaded": 3}],
            "note": "8 equal slices. The 3 shaded slices are eaten."},
    steps={0: {"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 8, "shaded": 1}], "highlight": ["b0"],
               "note": "One slice: 360° ÷ 8 = 45°"},
           1: {"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 8, "shaded": 3}],
               "note": "8 − 3 slices are left: the unshaded ones"},
           2: {"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 8, "shaded": 3}],
               "note": "Slices left × 45° = 225°"},
           3: {"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 8, "shaded": 3}],
               "note": "The unshaded slices make 225° at the centre"}})

# Bar widths 3 and 5 stand for 15 seconds and the other 25 of the 40.
_TIME = ("Time", [(3, "15 s", "a"), (5, None, "c")], "40 s")
_TURN = ("Turn", [(3, "?", "unknown"), (5, None, "c")], "360°")
add("G4A_ANGLES_007",
    figure=BM([_TIME, _TURN], note="One full turn takes 40 seconds"),
    steps={0: BM([_TIME, _TURN], note="Turn in one second: 360° ÷ 40"),
           1: BM([_TIME, _TURN], hl=["b1s0"], note="Multiply the turn in one second by 15"),
           2: BM([_TIME, ("Turn", [(3, "135°", "a"), (5, None, "c")], "360°")], hl=["b1s0"], note="In 15 seconds the lamp turns 135°")})


# ══ Clocks ═══════════════════════════════════════════════════════════════════

ASK = "Angle between the hands = ?"

add("EXT_G4_FP_2024_017",
    figure=CLOCK(7, 20, True, note=ASK),
    steps={0: CLOCK(7, 20, note="Each gap between two numbers is 30°"),
           1: CLOCK(7, 20, hl=["minute"], note="The minute hand is on 4. From 4 to 7 is 3 gaps."),
           2: CLOCK(7, 20, hl=["hour"], note="The hour hand is one third of a gap past 7"),
           3: CLOCK(7, 20, True, note="3 gaps and a third of a gap: 90° + 10° = 100°"),
           4: CLOCK(7, 20, True, hl=["angle"], note="The angle between the hands is 100°")})

add("EXT_G4_FP_2025_013",
    figure=CLOCK(5, 18, True, note=ASK),
    steps={0: CLOCK(5, 18, hl=["minute"], note="Minute hand: 18 minutes of 6° each, 108° from the 12"),
           1: CLOCK(5, 0, hl=["hour"], note="At 5 o'clock the hour hand is 150° from the 12"),
           2: CLOCK(5, 18, hl=["hour"], note="In 18 minutes the hour hand moves 9° more"),
           3: CLOCK(5, 18, True, note="150° + 9° − 108° = 51°"),
           4: CLOCK(5, 18, True, hl=["angle"], note="The angle is 51°")})

add("G4A_ANGLES_011",
    figure=CLOCK(2, 40, True, note="The smaller angle between the hands = ?"),
    steps={0: CLOCK(2, 40, hl=["minute"], note="The minute hand is on the 8. Each number is 30° from the next."),
           1: CLOCK(2, 40, hl=["hour"], note="In 40 minutes the hour hand moves 20°"),
           2: CLOCK(2, 40, hl=["hour"], note="So the hour hand is 20° past the 2"),
           3: CLOCK(2, 40, True, note="Subtract the hour hand's place from the minute hand's"),
           4: CLOCK(2, 40, True, hl=["angle"], note="The smaller angle is 160°")})

add("G4A_ANGLES_003",
    figure=CLOCK(3, 0, hl=["hour"], note="The hour hand at 3 p.m. How far has it turned by 7:30 p.m.?"),
    steps={0: CLOCK(3, 0, hl=["hour"], note="The hour hand turns 30° every hour"),
           1: CLOCK(7, 30, hl=["hour"], note="From 3 p.m. to 7:30 p.m. is 4 and a half hours"),
           2: CLOCK(7, 30, hl=["hour"], note="4 hours give 120°. Half an hour gives 15°."),
           3: CLOCK(7, 30, hl=["hour"], note="120° + 15° = 135°")})

add("G4A_ANGLES_006",
    figure=CLOCK(6, 30, True, note="At 6:00 the angle was 180°. How much smaller is it at 6:30?"),
    steps={0: CLOCK(6, 30, hl=["minute"], note="At 6:30 the minute hand points exactly at 6"),
           1: CLOCK(6, 30, hl=["hour"], note="The hour hand is halfway from 6 to 7: half of 30° is 15°"),
           2: CLOCK(6, 30, True, hl=["angle"], note="At 6:30 the angle between the hands is 15°"),
           3: CLOCK(6, 0, True, hl=["angle"], note="At 6:00 the angle was 180°"),
           4: CLOCK(6, 30, True, note="180° − 15° = 165° smaller")})

add("G4A_ANGLES_012",
    figure=CLOCK(2, 10, note="From 2:10 to 2:50, how much more does the minute hand turn?"),
    steps={0: CLOCK(2, 50, note="The clock at 2:50. Find the time that has passed."),
           1: CLOCK(2, 50, hl=["minute"], note="The minute hand turns 6° each minute"),
           2: CLOCK(2, 50, hl=["hour"], note="The hour hand turns 1° every 2 minutes")})

add("G4A_ANGLES_013",
    figure=CLOCK(12, 0, hl=["hour"], note="The hour hand turns 75° from here. What time is it then?"),
    steps={0: CLOCK(1, 0, hl=["hour"], note="In one hour the hour hand turns 30°"),
           1: CLOCK(2, 0, hl=["hour"], note="Two hours take 60° of the 75°"),
           2: CLOCK(2, 30, hl=["hour"], note="15° is half of 30°: half an hour more"),
           3: CLOCK(2, 30, note="2 hours and 30 minutes have passed since noon"),
           4: CLOCK(2, 30, note="The time is 2:30 pm")})

add("G4A_ANGLES_014",
    figure=CLOCK(12, 20, True, note="Sana says the angle between the hands is 120°"),
    steps={0: CLOCK(12, 20, hl=["minute"], note="The minute hand is on the 4: 120° from the 12"),
           1: CLOCK(12, 20, hl=["hour"], note="The hour hand has moved one third of 30° past the 12"),
           2: CLOCK(12, 20, True, hl=["angle"], note="So the true angle is smaller: 120° − 10° = 110°"),
           3: CLOCK(12, 20, True, note="Sana's 120° − the true 110° = 10°")})

add("PYQ_2017_Q20",
    steps={1: CLOCK(12, 0, hl=["minute"], note="Once round, 360°, in 60 minutes: 6° each minute"),
           2: CLOCK(12, 5, hl=["minute"], note="In 5 minutes: 5 times 6° = 30°")})

add("PYQ_2019_Q40",
    steps={2: CLOCK(8, 30, hl=["hour"], note="At half past, the hour hand is halfway between two numbers"),
           3: CLOCK(7, 30, True, hl=["angle"], note="At 7:30: 1 and a half gaps of 30° make 45°"),
           4: CLOCK(2, 30, True, note="At 2:30 there are 3 and a half gaps: too wide")})

add("Q_CH18_011",
    figure=CLOCK(3, 0, True, note=ASK),
    steps={0: CLOCK(3, 0, note="12 equal gaps share the full turn of 360°: each gap is 30°"),
           1: CLOCK(3, 0, hl=["hour", "minute"], note="Minute hand on 12, hour hand on 3: 3 gaps between them"),
           2: CLOCK(3, 0, True, hl=["angle"], note="3 gaps of 30° make 90°")})

add("Q_CH18_012",
    figure=CLOCK(9, 30, True, note=ASK),
    steps={0: CLOCK(9, 30, hl=["hour"], note="The hour hand has moved halfway from 9 to 10"),
           1: CLOCK(9, 30, hl=["minute"], note="From 6 to 9 is 3 gaps of 30°: 90°"),
           2: CLOCK(9, 30, hl=["hour"], note="The hour hand is half a gap past 9: half of 30° is 15°"),
           3: CLOCK(9, 30, True, hl=["angle"], note="90° + 15° = 105°")})

add("Q_CH18_024",
    figure=CLOCK(4, 30, True, note=ASK),
    steps={0: CLOCK(4, 30, hl=["hour"], note="The hour hand has moved halfway from 4 to 5"),
           1: CLOCK(4, 30, hl=["minute"], note="From 5 to 6 is 1 full gap: 30°"),
           2: CLOCK(4, 30, hl=["hour"], note="From the hour hand to 5 is half a gap: 15°"),
           3: CLOCK(4, 30, True, hl=["angle"], note="30° + 15° = 45°")})

# The answer is one of the times in the choices, so no clock before answering.
add("Q_CH18_013",
    steps={1: CLOCK(10, 0, True, note="10:00: 2 gaps apart, 60°. Less than 90°, so acute."),
           2: CLOCK(6, 0, True, note="6:00: 6 gaps apart, 180°. A straight angle."),
           3: CLOCK(3, 30, True, note="3:30: 2 and a half gaps, 75°. Acute."),
           4: CLOCK(4, 0, True, hl=["angle"], note="4:00: 4 gaps apart, 120°. Obtuse.")})

add("Q_CH18_014",
    steps={0: CLOCK(6, 0, True, hl=["angle"], note="6:00: 6 gaps of 30° make 180°"),
           1: CLOCK(3, 45, True, hl=["hour"], note="3:45: the hour hand is most of the way from 3 to 4"),
           2: CLOCK(9, 15, True, hl=["hour"], note="9:15: the hour hand is a little past 9"),
           3: CLOCK(6, 0, True, hl=["angle"], note="Only at 6:00 are the hands exactly opposite")})

add("Q_CH18_015",
    steps={1: CLOCK(9, 0, True, note="9:00: the hands are 3 gaps apart"),
           2: CLOCK(4, 30, True, note="4:30: 1 and a half gaps"),
           3: CLOCK(12, 15, True, note="12:15: 2 and three-quarter gaps"),
           4: CLOCK(6, 15, True, note="6:15: 3 and a quarter gaps"),
           5: CLOCK(6, 15, True, hl=["angle"], note="The greatest angle is 97.5°, at 6:15")})

add("Q_CH18_016",
    figure=CLOCK(1, 0, True, note="At 1 o'clock the angle between the hands is 30°"),
    steps={0: corner([("30°", 30), ("60°", 60)], hl=["p1"], note="Complementary angles make 90°: 90° − 30° = 60°"),
           1: CLOCK(1, 0, True, hl=["angle"], note="At 1 o'clock the hands are one gap apart: each gap is 30°"),
           2: CLOCK(2, 0, True, note="60° is two gaps, because 60 ÷ 30 = 2"),
           3: CLOCK(2, 0, True, hl=["angle"], note="The hands are two gaps apart at 2 o'clock")})

add("Q_CH18_018",
    figure=CLOCK(1, 0, True, note="From 12 to 1 is one hour for the hour hand"),
    steps={0: CLOCK(12, 0, hl=["hour"], note="The hour hand goes once round, 360°, in 12 hours"),
           1: CLOCK(1, 0, True, note="Share 360° equally among the 12 hours"),
           2: CLOCK(1, 0, True, hl=["angle"], note="360° ÷ 12 = 30° in one hour")})

add("Q_CH18_019",
    figure=CLOCK(12, 1, hl=["minute"], note="The minute hand, 1 minute after 12 o'clock"),
    steps={0: CLOCK(12, 0, hl=["minute"], note="The minute hand goes once round, 360°, in 60 minutes"),
           1: CLOCK(12, 1, hl=["minute"], note="Share 360° equally among the 60 minutes"),
           2: CLOCK(12, 1, hl=["minute"], note="360° ÷ 60 = 6° in 1 minute")})


# ══ Compass directions and turns ═════════════════════════════════════════════

add("EXT_G4_FP_2020_025",
    figure=COMPASS("N", [(135, ACW), (225, CW)], note="135° to the left, then 225° to the right"),
    steps={0: COMPASS("N", [(135, ACW), (225, CW)], hl=["t1"], note="Left and right cancel. The right turn is bigger."),
           1: COMPASS("N", [(90, CW)], hl=["t0"], note="225° − 135° = 90° to the right, from north"),
           2: COMPASS("N", [(90, CW)], end=True, hl=["end"], note="A quarter turn right from north: East")})

add("EXT_G4_FP_2024_038",
    figure=COMPASS("SW", note="He turns clockwise until he faces North"),
    steps={0: COMPASS("SW", note="The eight directions are 45° apart"),
           1: COMPASS("SW", [(45, CW), (45, CW), (45, CW)], end=True, note="SW → W → NW → N: 3 steps"),
           2: COMPASS("SW", [(45, CW), (45, CW), (45, CW)], end=True, note="Each of the 3 steps is 45°"),
           3: COMPASS("SW", [(135, CW)], end=True, hl=["t0"], note="3 steps of 45° make 135°: not in the list")})

add("PYQ_2016_Q14",
    figure=COMPASS("S", note="He starts facing South. Later he faces North-East."),
    steps={0: COMPASS("S", note="8 directions share 360°: each step is 45°"),
           1: COMPASS("S", [(45, ACW), (45, ACW), (45, ACW)], end=True, note="Anticlockwise: S → SE → E → NE is 3 steps"),
           2: COMPASS("S", [(135, ACW)], end=True, hl=["t0"], note="Three steps of 45° make 135°"),
           3: COMPASS("S", [(225, CW)], end=True, note="Clockwise it is 5 steps, 225°: no choice says that"),
           4: COMPASS("S", [(135, ACW)], end=True, hl=["t0"], note="He turned 135° anticlockwise")})

add("Q_CH18_017",
    figure=COMPASS("NE", note="Angle between North-East and South = ?"),
    steps={0: COMPASS("NE", note="N, E, S and W are 90° apart. NE is halfway from N to E."),
           1: COMPASS("NE", [(45, CW)], hl=["t0"], note="North-East to East: half of 90°, which is 45°"),
           2: COMPASS("NE", [(45, CW), (90, CW)], hl=["t1"], note="East to South: a quarter turn, 90°"),
           3: COMPASS("NE", [(135, CW)], end=True, hl=["t0"], note="45° + 90° = 135°")})

add("Q_CH18_025",
    figure=COMPASS("N", [(225, CW)], note="He turns clockwise through 225°"),
    steps={0: COMPASS("N", [(90, CW), (90, CW), (90, CW)], note="Each quarter turn clockwise is 90°: East, South, then West"),
           1: COMPASS("N", [(90, CW), (90, CW)], end=True, note="Two quarter turns: 90° + 90° = 180°, round to South"),
           2: COMPASS("N", [(180, CW), (45, CW)], hl=["t1"], note="He still has 225° − 180° = 45° to turn"),
           3: COMPASS("N", [(225, CW)], end=True, hl=["end"], note="Halfway between South and West: South-West")})

add("G4A_ANGLES_004",
    figure=COMPASS("E", note="A three-quarter turn anticlockwise"),
    steps={0: COMPASS("E", note="Anticlockwise: East, North, West, South"),
           1: COMPASS("E", [(90, ACW), (90, ACW)], end=True, note="Two quarter turns: East → North → West"),
           2: COMPASS("E", [(90, ACW), (90, ACW), (90, ACW)], end=True, hl=["t2"], note="Third quarter turn: West → South"),
           3: COMPASS("E", [(90, ACW), (90, ACW), (90, ACW)], end=True, hl=["end"], note="Arjun is now facing South")})

add("G4A_ANGLES_015",
    figure=COMPASS("NE", [(90, CW), (225, ACW), (135, CW)], note="90° clockwise, 225° anticlockwise, then 135° clockwise"),
    steps={0: COMPASS("NE", [(90, CW)], end=True, hl=["t0"], note="90° clockwise is two steps of 45°: South-East"),
           2: COMPASS("SE", [(225, ACW)], end=True, hl=["t0"], note="From South-East, 225° anticlockwise: West"),
           4: COMPASS("W", [(135, CW)], end=True, hl=["t0"], note="From West, 135° clockwise: North-East"),
           5: COMPASS("NE", [(90, CW), (225, ACW), (135, CW)], end=True, hl=["end"], note="Back where he started: North-East")})

add("G4A_ANGLES_016",
    figure=COMPASS("S", note="After both turns Ravi faces South. Where did he start?"),
    steps={0: COMPASS("S", hl=["start"], note="Start from where Ravi ends: South"),
           1: COMPASS("S", [(90, CW)], end=True, hl=["t0"], note="Undo the last turn: 90° clockwise from South is West"),
           2: COMPASS("W", [(135, ACW)], end=True, hl=["t0"], note="Undo the first turn: 135° anticlockwise from West"),
           3: COMPASS("SE", [(135, CW), (90, ACW)], end=True, note="Check forwards from South-East: he ends facing South"),
           4: COMPASS("SE", hl=["start"], note="Ravi was facing South-East")})

add("G4A_ANGLES_017",
    figure=COMPASS("N", [(45, CW)], note="Each press turns the robot 45° clockwise. 13 presses."),
    steps={0: COMPASS("N", [(360, CW)], note="How many turns of 45° make a full turn of 360°?"),
           1: COMPASS("N", [(360, CW)], end=True, note="After 8 presses the robot faces North again"),
           2: COMPASS("N", [(360, CW)], end=True, note="13 − 8 presses are still to come"),
           3: COMPASS("N", [(180, CW), (45, CW)], end=True, note="Five more: NE, E, SE, S, SW"),
           4: COMPASS("N", [(180, CW), (45, CW)], end=True, hl=["end"], note="The robot is facing South-West")})

# A ladder against a wall: the wall on the left, the ground along the bottom.
_LADDER = {"ab": "wall", "bc": "ground", "ca": "ladder"}
add("G4A_ANGLES_005",
    figure=tri_angles(32, 90, 58, "?", None, "58°", sides=_LADDER),
    steps={0: tri_angles(32, 90, 58, "?", None, "58°", sides=_LADDER, note="The wall and the ground meet at 90°"),
           1: tri_angles(32, 90, 58, "?", None, "58°", sides=_LADDER, note="So ? + 58° = 90°"),
           2: tri_angles(32, 90, 58, "?", None, "58°", sides=_LADDER, note="? = 90° − 58°"),
           3: tri_angles(32, 90, 58, "32°", None, "58°", sides=_LADDER, hl=["ca", "ab"], note="90° − 58° = 32° between the ladder and the wall")})


# ══ Left without a picture ═══════════════════════════════════════════════════

skip("EXT_G4_FP_2025_031", "adding up the pairs in the answer choices: arithmetic, and a drawn pair would point at the answer")
skip("PYQ_2017_Q40", "adding up the pairs in the answer choices: arithmetic, and a drawn pair would point at the answer")
skip("PYQ_2019_Q25", "adding up the pairs in the answer choices: arithmetic, and a drawn pair would point at the answer")
skip("EXT_G4_WS2_CH18_001", "a line segment and its end points: no figure kind draws a bare segment")
skip("EXT_G4_WS2_CH18_002", "a line through two points: no figure kind draws points and a line")
skip("EXT_G4_WS2_CH18_003", "points on a line: no figure kind draws points and a line")
skip("Q_CH18_003", "which instrument measures an angle: vocabulary, and no figure kind draws a protractor")

book.finish(sys.argv)
