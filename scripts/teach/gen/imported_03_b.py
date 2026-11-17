"""Lessons for textbook chapter 19 (perimeter): builders for the shared shapes, and three one-offs."""
from imported_03_lib import (ANS, ANSR, B, D, DIV, FIG, GIVEN, M, N, W, WN, choose, lesson, n, pick, placed)

LESSONS = {}
P = "IPMTB_grade5_ch19_"

SHAPES = {
    "tri": dict(title="Equilateral triangle", a="an equilateral triangle", sides=3, choices=["2", "3", "4"], right=1,
                why="Equilateral means all the sides are equal, and a triangle has 3 sides."),
    "sq": dict(title="Square", a="a square", sides=4, choices=["3", "4", "6"], right=1,
               why="A square has 4 sides, and all 4 are the same length."),
    "hex": dict(title="Regular hexagon", a="a regular hexagon", sides=6, choices=["5", "6", "8"], right=1,
                why="Hex means 6. A hexagon has 6 sides, and regular means they are all the same length."),
}


def shape_figure(shape, label):
    if shape == "tri":
        return FIG("f1", {"kind": "triangle", "shape": "equilateral", "sides": {"ab": label, "bc": label, "ca": label}})
    if shape == "sq":
        return FIG("f1", {"kind": "rectangle", "square": True, "length": label, "breadth": label})
    return None


# ── Side known, perimeter wanted (the side is a decimal) ─────────────────────

def regular_perimeter(qid, shape, side, trap):
    sh = SHAPES[shape]
    k = sh["sides"]
    side = D(side)
    whole = int(side)
    tenth = side - whole
    a, b = k * whole, k * tenth
    total = k * side
    s = n(side)
    add_line = " + ".join([s] * k) + " = %d × %s" % (k, s)
    return lesson(
        B(pick(qid, "open", [
            "Here is %s, and each side is %s centimetres. We want the perimeter, the distance all the way round.",
            "This is %s with every side %s centimetres long. The perimeter is how far it is all the way round."]) % (sh["a"], s),
          GIVEN("q1", "%s, each side %s cm. Perimeter = ?" % (sh["title"], s)), shape_figure(shape, s + " cm")),
        B("How many equal sides does it have?",
          ask=choose(sh["choices"], sh["right"], sh["why"])),
        B("So going round, we walk %s centimetres, %d times over. A quicker way to write that is %d times %s." % (s, k, k, s),
          W("a", add_line), M("a", "%d × %s" % (k, s), "box")),
        B("To multiply, split %s into %d and %s. %d times %d is %s, and %d times %s is %s."
          % (s, whole, n(tenth), k, whole, n(D(a)), k, n(tenth), n(b)),
          W("b", "%d × %d = %s" % (k, whole, n(D(a)))), W("c", "%d × %s = %s" % (k, n(tenth), n(b)))),
        B("Put the two pieces together. %s plus %s is %s, so the perimeter is %s centimetres." % (n(D(a)), n(b), n(total), n(total)),
          W("d", "%s + %s = %s" % (n(D(a)), n(b), n(total))),
          ANSR("e", "%d × %s = %s" % (k, s, n(total)), n(total))),
        B(trap),
        B(pick(qid, "check", [
            "Check by sharing it back out. %s divided by %d is %s, the side we started with.",
            "Let's check. Share %s equally among the %d sides, and each one gets %s. That is our side."]) % (n(total), k, s),
          W("g", "%s ÷ %d = %s" % (n(total), k, s))),
        B(pick(qid, "sum", [
            "So for any shape with equal sides, the perimeter is the number of sides times one side.",
            "The rule to keep: when every side is equal, count the sides and multiply by the length of one."])),
    )


LESSONS[P + "q001"] = regular_perimeter(
    P + "q001", "tri", "5.3",
    "Careful not to lose the decimal part. 3 times 5 alone gives 15, but those 3 lots of 0.3 count too.")
LESSONS[P + "q012"] = regular_perimeter(
    P + "q012", "sq", "4.6",
    "Now look at the units. A perimeter is a length, so it stays in centimetres. Square centimetres are for area, and nothing here was changed to millimetres.")
LESSONS[P + "q013"] = regular_perimeter(
    P + "q013", "tri", "5.4",
    "Two things to watch. A triangle has 3 sides, not 4. And a perimeter is a length, so it is in centimetres, not square centimetres.")
LESSONS[P + "q023"] = regular_perimeter(
    P + "q023", "hex", "6.1",
    "Don't drop the little 0.1. It is on all 6 sides, so together it adds 0.6. The answer is 36.6, not just 36.")


# ── Perimeter known, one side wanted ─────────────────────────────────────────

def regular_side(qid, shape, perimeter, trap, split=None, trap_board=None):
    sh = SHAPES[shape]
    k = sh["sides"]
    per = D(perimeter)
    side = per / k
    p, s = n(per), n(side)
    opening = B(
        pick(qid, "open", [
            "%s has a perimeter of %s centimetres. We want the length of one side.",
            "The distance all the way round %s is %s centimetres. How long is each side?"])
        % ((sh["a"][0].upper() + sh["a"][1:]) if pick(qid, "open", [0, 1]) == 0 else sh["a"], p),
        GIVEN("q1", "%s, perimeter %s cm. Each side = ?" % (sh["title"], p)), shape_figure(shape, "?"))
    beats = [
        opening,
        B("The perimeter is all the sides added together. How many equal sides share this %s?" % p,
          ask=choose(sh["choices"], sh["right"], sh["why"])),
        B("So %d equal sides, put end to end, make %s centimetres." % (k, p),
          W("r", "%d × side = %s" % (k, p), label=True)),
        B("How do we get back to just one side?",
          ask=choose(["%s × %d" % (p, k), "%s ÷ %d" % (p, k), "%s − %d" % (p, k)], 1,
                     "The %d equal sides together make %s. To get back to one side, we share %s equally among %d, and sharing is dividing."
                     % (k, p, p, k))),
    ]
    final = "%s ÷ %d = %s" % (p, k, s)
    if split is None:
        beats.append(B("%s divided by %d. Well, %d times %s is %s, so each side is %s centimetres." % (p, k, k, s, p, s),
                       DIV("r", str(k)), ANSR("a", final, s)))
    else:
        x, y = D(split[0]), D(split[1])
        qx, qy = x / k, y / k
        beats.append(B("To divide %s by %d, split it into %s and %s. %s divided by %d is %s, and %s divided by %d is %s."
                       % (p, k, n(x), n(y), n(x), k, n(qx), n(y), k, n(qy)),
                       DIV("r", str(k)), W("a", "%s = %s + %s" % (p, n(x), n(y))),
                       W("b", "%s ÷ %d = %s" % (n(x), k, n(qx))), W("c", "%s ÷ %d = %s" % (n(y), k, n(qy)))))
        beats.append(B("%s plus %s is %s. Each side is %s centimetres." % (n(qx), n(qy), s, s),
                       W("d", "%s + %s = %s" % (n(qx), n(qy), s)), ANSR("e", final, s)))
    beats.append(B(trap, trap_board))
    beats.append(B(pick(qid, "check", [
        "Check: %d sides of %s make %s. That is the perimeter we were given.",
        "Let's check by going back round. %d times %s is %s, the perimeter. It works."]) % (k, s, p),
        W("g", "%d × %s = %s" % (k, s, p))))
    beats.append(B(pick(qid, "sum", [
        "So when all the sides are equal, one side is the perimeter divided by the number of sides.",
        "The rule to keep: count the equal sides, then divide the perimeter by that number."])))
    return lesson(*beats)


LESSONS[P + "q002"] = regular_side(
    P + "q002", "sq", "16",
    "Careful not to just halve it. Half of 16 is 8, but a square has 4 sides, not 2.")
LESSONS[P + "q004"] = regular_side(
    P + "q004", "hex", "54",
    "A trap here is to answer 6, the number of sides. The 6 is what we divide by. The side is what comes out, 9.")
LESSONS[P + "q010"] = regular_side(
    P + "q010", "tri", "23.1",
    "Don't drop the decimal part. A side of just 7 would give a perimeter of only 21, and ours is 23.1.",
    split=("21", "2.1"))
LESSONS[P + "q014"] = regular_side(
    P + "q014", "sq", "24.4",
    "Now the units. The perimeter was in centimetres, so the side is in centimetres too. Not millimetres, and not square units, which are for area.",
    split=("24", "0.4"))
LESSONS[P + "q016"] = regular_side(
    P + "q016", "hex", "72",
    "Careful with the 6 times table. 6 times 10 is 60, and 2 more sixes take us up to 72. So each side is 12.",
    trap_board=W("t", "6 × 10 = 60"))
LESSONS[P + "q021"] = regular_side(
    P + "q021", "tri", "29.1",
    "Careful with the whole part. 3 times 9 is 27, so the side starts with 9, not with 8 or 7.",
    split=("27", "2.1"))


# ── Rectangle: perimeter and length known, breadth wanted ────────────────────

def rect_breadth(qid, per, length, extra=""):
    half = per // 2
    breadth = half - length
    both = per - 2 * length
    return lesson(
        B("A rectangle with a perimeter of %d centimetres and a length of %d centimetres. We need its breadth." % (per, length),
          GIVEN("q1", "Rectangle: perimeter %d cm, length %d cm. Breadth = ?" % (per, length)),
          FIG("f1", {"kind": "rectangle", "length": "%d cm" % length, "breadth": "?"})),
        B("Walk round a rectangle and you pass a length, a breadth, another length and another breadth. So the perimeter is 2 lengths and 2 breadths.",
          W("r", "Perimeter = 2 × (length + breadth)", label=True)),
        B("So what does half of the perimeter give us?",
          ask=choose(["one length", "one length + one breadth", "two breadths"], 1,
                     "Half of the walk round takes you along one length and one breadth. So half the perimeter is length plus breadth.")),
        B("Half of %d is %d. So the length and the breadth together make %d." % (per, half, half),
          WN("a", "%d ÷ 2 = %d" % (per, half), str(half), "length + breadth")),
        B("The length is %d. So the breadth is %d minus %d, which is %d centimetres." % (length, half, length, breadth),
          ANSR("b", "%d − %d = %d" % (half, length, breadth), str(breadth))),
        B("Here is the trap. Take both lengths off the %d and you get %d. But that is two breadths, so it still has to be halved.%s"
          % (per, both, extra),
          W("c", "%d − %d − %d = %d" % (per, length, length, both)), W("d", "%d ÷ 2 = %d" % (both, breadth))),
        B("Check: %d plus %d is %d, and twice %d is %d. It matches the perimeter." % (length, breadth, half, half, per),
          W("e", "2 × (%d + %d) = %d" % (length, breadth, per))),
        B(pick(qid, "sum", [
            "So to find a missing side of a rectangle, halve the perimeter, then take away the side you know.",
            "The plan to keep: half the perimeter is length plus breadth. Take away the one you know to get the other."])),
    )


LESSONS[P + "q003"] = rect_breadth(P + "q003", 40, 12)
LESSONS[P + "q015"] = rect_breadth(P + "q015", 48, 14, " And keep the unit: centimetres, like the question.")


# ── Rectangle: length is so many times the breadth, perimeter known ──────────

def rect_times(qid, per, k, both, opening, trap):
    parts = 2 * (k + 1)
    unit = per // parts
    length = k * unit
    together = length + unit
    beats = [
        B(opening,
          GIVEN("q1", "Rectangle: length = %d × breadth, perimeter %d cm" % (k, per)),
          GIVEN("q2", "Length = ?  Breadth = ?" if both else "Breadth = ?")),
        B("Call the breadth 1 part. Then the length is %d parts, because it is %d times as long." % (k, k),
          FIG("f1", {"kind": "rectangle", "length": "%d parts" % k, "breadth": "1 part", "proportion": k})),
        B("Going all the way round the rectangle, how many parts do we pass?",
          ask=choose(["%d parts" % (k + 1), "%d parts" % parts, "%d parts" % (2 * k)], 1,
                     "One length and one breadth make %d parts. But the walk round passes two lengths and two breadths, so it is %d parts, twice over."
                     % (k + 1, k + 1))),
        B("%d plus 1 plus %d plus 1 is %d parts. And those %d parts together are the whole perimeter, %d centimetres." % (k, k, parts, parts, per),
          W("a", "%d + 1 + %d + 1 = %d" % (k, k, parts)), W("b", "%d parts = %d cm" % (parts, per), label=True)),
    ]
    if both:
        beats.append(B("So one part is %d divided by %d, which is %d. That is the breadth: %d centimetres." % (per, parts, unit, unit),
                       DIV("b", str(parts)), WN("c", "%d ÷ %d = %d" % (per, parts, unit), str(unit), "breadth")))
        beats.append(B("The length is %d parts. %d times %d is %d centimetres." % (k, k, unit, length),
                       WN("d", "%d × %d = %d" % (k, unit, length), str(length), "length"),
                       ANSR("e", "Length %d cm, breadth %d cm" % (length, unit), "%d cm, breadth %d cm" % (length, unit), True)))
    else:
        beats.append(B("So one part is %d divided by %d, which is %d. And one part is the breadth: %d centimetres." % (per, parts, unit, unit),
                       DIV("b", str(parts)), ANSR("c", "%d ÷ %d = %d" % (per, parts, unit), str(unit))))
        beats.append(B("The length is %d parts, so %d times %d is %d centimetres. We were not asked for it, but it helps us check." % (k, k, unit, length),
                       WN("d", "%d × %d = %d" % (k, unit, length), str(length), "length")))
    beats.append(B(trap))
    beats.append(B("Check: %d plus %d is %d, and twice %d is %d. That is the perimeter, so it all fits." % (length, unit, together, together, per),
                   W("g", "%d + %d = %d" % (length, unit, together)), W("h", "2 × %d = %d" % (together, per))))
    beats.append(B(pick(qid, "sum", [
        "So when one side is so many times the other, count the parts all the way round, find one part, and build the sides from it.",
        "The plan to keep: turn the sides into parts, count the parts round the whole edge, and divide the perimeter by that."])))
    return lesson(*beats)


LESSONS[P + "q005"] = rect_times(
    P + "q005", 42, 2, True,
    "This rectangle is twice as long as it is wide, and its perimeter is 42 centimetres. We want both the length and the breadth.",
    "The trap is to share 42 among 3 parts only. That forgets we pass every side twice on the way round.")
LESSONS[P + "q020"] = rect_times(
    P + "q020", 78, 2, True,
    "The length of this rectangle is twice its breadth, and the perimeter is 78 centimetres. We need the length and the breadth.",
    "The trap is to share 78 among 3 parts only. That makes both sides twice too big, because we pass every side twice on the way round.")
LESSONS[P + "q025"] = rect_times(
    P + "q025", 64, 3, False,
    "Thrice means 3 times. So this rectangle is 3 times as long as it is wide, and its perimeter is 64 centimetres. We want the breadth.",
    "Two traps here. Sharing 64 among 4 parts forgets we pass every side twice. And the question wants the breadth, not the length.")


# ── Square: perimeter known, area wanted (also used for chapter 20) ──────────

def square_area_from_perimeter(qid, per, unit, short, trap):
    side = per // 4
    area = side * side
    choices, right = placed(qid, "first", "%d ÷ 4" % per, ["%d ÷ 2" % per, "%d × 4" % per])
    beats = [
        B("A square with a perimeter of %d %s. We want its area." % (per, unit),
          GIVEN("q1", "Square, perimeter %d %s. Area = ?" % (per, short))),
        B("Area needs the side, and all we have is the perimeter. So this takes two steps: first the side, then the area.",
          W("r", "perimeter, then side, then area", label=True)),
        B("A square has 4 equal sides. How do we get one side from the perimeter?",
          ask=choose(choices, right,
                     "The 4 equal sides add up to the perimeter. So one side is the perimeter shared among 4.")),
        B("%d divided by 4 is %d. Each side is %d %s." % (per, side, side, unit),
          WN("a", "%d ÷ 4 = %d" % (per, side), str(side), "side")),
        B("Now for the area of the square. Which sum is it?",
          ask=choose(["%d + %d" % (side, side), "%d × %d" % (side, side), "4 × %d" % side], 1,
                     "Area counts the little squares inside: %d rows, with %d in each row. That is side times side. 4 times the side only takes us back to the perimeter."
                     % (side, side))),
    ]
    final = "%d × %d = %d" % (side, side, area)
    if side <= 10:
        beats.append(B("%d times %d is %d. The area is %d square %s." % (side, side, area, area, unit),
                       ANSR("b", final, str(area))))
    else:
        tens, ones = 10, side - 10
        beats.append(B("%d times %d. Take it in two bites: %d times 10 is %d, and %d times %d is %d."
                       % (side, side, side, side * tens, side, ones, side * ones),
                       W("b", "%d × 10 = %d" % (side, side * tens)), W("c", "%d × %d = %d" % (side, ones, side * ones))))
        beats.append(B("%d plus %d is %d. The area is %d square %s." % (side * tens, side * ones, area, area, unit),
                       W("d", "%d + %d = %d" % (side * tens, side * ones, area)), ANSR("e", final, str(area))))
    beats.append(B(trap))
    beats.append(B("Check the first step: 4 sides of %d make %d, the perimeter we were given." % (side, per),
                   W("g", "4 × %d = %d" % (side, per))))
    beats.append(B(pick(qid, "sum", [
        "So from perimeter to area in a square: divide by 4 for the side, then multiply the side by itself.",
        "Two steps to keep: perimeter divided by 4 gives the side, and side times side gives the area."])))
    return lesson(*beats)


LESSONS[P + "q006"] = square_area_from_perimeter(
    P + "q006", 20, "centimetres", "cm",
    "Don't stop at 5, that is only the side. And notice that the perimeter, 20, and the area, 25, are different numbers, measuring different things.")
LESSONS[P + "q017"] = square_area_from_perimeter(
    P + "q017", 36, "centimetres", "cm",
    "Careful not to do something quick with the 36, like doubling it. The area always comes from the side, and 9 times 9 is exactly 81.")


# ── Rectangle: perimeter known, length a few centimetres more than breadth ───

def rect_longer(qid, per, d, trap):
    half = per // 2
    two_b = half - d
    b = two_b // 2
    length = b + d
    area = length * b
    return lesson(
        B("A rectangle with a perimeter of %d centimetres, and its length is %d centimetres more than its breadth. We want the area, so first we need both sides."
          % (per, d),
          GIVEN("q1", "Rectangle: perimeter %d cm, length = breadth + %d cm" % (per, d)), GIVEN("q2", "Area = ?")),
        B("Half of the perimeter is one length plus one breadth. Half of %d is %d." % (per, half),
          WN("a", "%d ÷ 2 = %d" % (per, half), str(half), "length + breadth")),
        B("The length is a breadth with %d extra. If we take that extra %d away from the %d, what is left?" % (d, d, half),
          ask=choose(["two breadths", "one breadth", "two lengths"], 0,
                     "Without its extra %d, the length is exactly as long as the breadth. So what is left is one breadth, and another breadth." % d)),
        B("%d minus %d is %d, and that is two breadths." % (half, d, two_b),
          WN("b", "%d − %d = %d" % (half, d, two_b), str(two_b), "2 breadths")),
        B("So one breadth is half of %d, which is %d. And the length is %d plus %d, which is %d." % (two_b, b, b, d, length),
          WN("c", "%d ÷ 2 = %d" % (two_b, b), str(b), "breadth"), WN("d", "%d + %d = %d" % (b, d, length), str(length), "length")),
        B("Now the area, which is length times breadth. %d times %d is %d square centimetres." % (length, b, area),
          ANSR("e", "%d × %d = %d" % (length, b, area), str(area))),
        B(trap),
        B("Check: %d plus %d is %d, and twice %d is %d. And %d is %d more than %d. Both clues fit."
          % (length, b, half, half, per, length, d, b),
          W("g", "2 × (%d + %d) = %d" % (length, b, per))),
        B("So: halve the perimeter, take off the extra, and halve again for the shorter side. Then it is length times breadth."),
    )


LESSONS[P + "q007"] = rect_longer(
    P + "q007", 50, 5,
    "Two traps to dodge. Don't stop at the sides, because the question asks for the area. And don't halve the 25 straight away: the extra 5 has to come off first.")
LESSONS[P + "q018"] = rect_longer(
    P + "q018", 40, 8,
    "Careful not to multiply the numbers in the question. 40 is a perimeter and 8 is a difference, so 40 times 8 means nothing here. We need the two sides first.")


# ── Square: area known, perimeter wanted (also used for chapter 20) ──────────

def square_perimeter_from_area(qid, area, near, clue, trap):
    side = int(round(area ** 0.5))
    assert side * side == area
    per = 4 * side
    return lesson(
        B("A square with an area of %d square centimetres. We want its perimeter." % area,
          GIVEN("q1", "Square, area %d sq cm. Perimeter = ?" % area)),
        B("The perimeter needs the side. And the area of a square is side times side. So we want a number that, multiplied by itself, makes %d." % area,
          W("r", "side × side = %d" % area, label=True)),
        B("Let's get close first. %d times %d is %d. So what can we say about the side?" % (near, near, near * near),
          W("a", "%d × %d = %d" % (near, near, near * near)),
          ask=choose(["it is less than %d" % near, "it is more than %d" % near, "it is exactly %d" % near], 1,
                     "%d is smaller than %d. So the side has to be a bit bigger than %d." % (near * near, area, near))),
        B(clue + " %d times %d is %d, so the side is %d centimetres." % (side, side, area, side),
          W("b", "%d × %d = %d" % (side, side, area)), N("b", "%d × %d" % (side, side), "side = %d cm" % side, "below")),
        B("Now the perimeter. A square has 4 equal sides, so which sum do we want?",
          ask=choose(["%d × %d" % (side, side), "4 × %d" % side, "2 × %d" % side], 1,
                     "The perimeter is the walk round all 4 sides. Each side is %d, so it is 4 times %d." % (side, side))),
        B("4 times %d is %d. The perimeter is %d centimetres." % (side, per, per),
          ANSR("c", "4 × %d = %d" % (side, per), str(per))),
        B(trap),
        B("Check by going backwards. %d divided by 4 is %d, and %d times %d is %d, the area we were given." % (per, side, side, side, area),
          W("d", "%d ÷ 4 = %d" % (per, side))),
        B(pick(qid, "sum", [
            "So from area to perimeter in a square: find the number that multiplies by itself to make the area, then multiply it by 4.",
            "Two steps to keep: the area tells you the side, and 4 times the side is the perimeter."])),
    )


LESSONS[P + "q008"] = square_perimeter_from_area(
    P + "q008", 441, 20, "441 ends in 1, and 1 times 1 is 1. So let's try 21.",
    "Two things to watch. 21 is only the side, so don't stop there. And a perimeter is a length, so it is 84 centimetres, not square centimetres.")
LESSONS[P + "q019"] = square_perimeter_from_area(
    P + "q019", 676, 25, "676 ends in 6, and 6 times 6 ends in 6. So let's try 26.",
    "Mind the units. Area is in square centimetres, but a perimeter is a length. So the answer is 104 centimetres, plain centimetres.")


# ── Isosceles triangle: perimeter and the equal sides known ──────────────────

def isosceles(qid, per, s, trap, trap_board=None):
    two = 2 * s
    third = per - two
    return lesson(
        B("An isosceles triangle with a perimeter of %d centimetres. Each of its two equal sides is %d centimetres, and we want the third side." % (per, s),
          GIVEN("q1", "Isosceles triangle: perimeter %d cm" % per), GIVEN("q2", "Equal sides %d cm each. Third side = ?" % s),
          FIG("f1", {"kind": "triangle", "shape": "isosceles", "sides": {"ab": "%d cm" % s, "ca": "%d cm" % s, "bc": "?"}})),
        B("Isosceles means two sides are equal, and congruent is just another word for equal. So the sides are %d, %d, and one we do not know yet." % (s, s),
          W("a", "%d + %d + ? = %d" % (s, s, per))),
        B("What should we work out first?",
          ask=choose(["%d − %d" % (per, s), "%d + %d" % (s, s), "%d + %d" % (per, s)], 1,
                     "There are two equal sides, and both are part of the perimeter. So first find how much the two of them make together.")),
        B("%d plus %d is %d. That is how much of the perimeter the two equal sides use up." % (s, s, two),
          WN("b", "%d + %d = %d" % (s, s, two), str(two), "two equal sides")),
        B("The rest belongs to the third side. %d minus %d is %d centimetres." % (per, two, third),
          ANSR("c", "%d − %d = %d" % (per, two, third), str(third))),
        B(trap, trap_board),
        B("Check by adding all three sides. %d plus %d plus %d is %d. It matches the perimeter." % (s, s, third, per),
          W("d", "%d + %d + %d = %d" % (s, s, third, per))),
        B(pick(qid, "sum", [
            "So for a missing side, add up the sides you know and take that away from the perimeter.",
            "The plan to keep: perimeter, minus all the sides you already know, leaves the side you want."])),
    )


LESSONS[P + "q011"] = isosceles(
    P + "q011", 26, 8,
    "The trap is taking away only one 8. That gives 18, but there are two equal sides to take off, not one.",
    W("t", "26 − 8 = 18"))
LESSONS[P + "q026"] = isosceles(
    P + "q026", 32, 9,
    "Don't stop at 18. That is the two equal sides together, not the third side. The third side is what is left of the perimeter.")


# ── One-offs ─────────────────────────────────────────────────────────────────

# Area 98, length double the breadth: find the perimeter.
LESSONS[P + "q009"] = lesson(
    B("A rectangle with an area of 98 square centimetres, and its length is double its breadth. We want the perimeter, so we need the sides.",
      GIVEN("q1", "Rectangle: area 98 sq cm, length = 2 × breadth"), GIVEN("q2", "Perimeter = ?")),
    B("Here is a picture that helps. If the length is double the breadth, the rectangle is really two equal squares, side by side.",
      FIG("f1", {"kind": "rectangle", "length": "2 × breadth", "breadth": "breadth", "proportion": 2, "grid": {"cols": 2, "rows": 1}}),
      W("r", "Rectangle = 2 equal squares", label=True)),
    B("The two squares together have an area of 98. So what is the area of one square?",
      ask=choose(["196", "49", "98"], 1,
                 "Two equal squares share the 98 between them. So each one is half of 98.")),
    B("Half of 98 is 49. So each square has an area of 49.",
      WN("a", "98 ÷ 2 = 49", "49", "one square")),
    B("Which number, multiplied by itself, makes 49? 7 times 7. So the breadth is 7 centimetres, and the length is double that, 14.",
      WN("b", "7 × 7 = 49", "7", "breadth"), WN("c", "2 × 7 = 14", "14", "length")),
    B("Now the perimeter, 2 lengths and 2 breadths. 14 plus 7 is 21, and twice 21 is 42 centimetres.",
      W("d", "14 + 7 = 21"), ANSR("e", "2 × (14 + 7) = 42", "42")),
    B("Don't stop at 7, or 14, or 21. Those are steps on the way. The question asks for the whole walk round, and that is 42."),
    B("Check the area clue: 14 times 7 is 98. It fits.",
      W("g", "14 × 7 = 98")),
    B("So when you are given an area, find the sides first. Once you have the sides, the perimeter is easy."),
)

# Regular hexagon, perimeter 42: the sum of 5 of its sides.
LESSONS[P + "q022"] = lesson(
    B("A regular hexagon has a perimeter of 42 centimetres. We want the total of just 5 of its sides.",
      GIVEN("q1", "Regular hexagon, perimeter 42 cm. Sum of 5 sides = ?")),
    B("First, how many equal sides does a regular hexagon have?",
      ask=choose(["5", "6", "8"], 1, SHAPES["hex"]["why"])),
    B("So 6 equal sides make 42. One side is 42 divided by 6, which is 7 centimetres.",
      WN("a", "42 ÷ 6 = 7", "7", "one side")),
    B("We want 5 of the sides, not all 6. What is the quickest way to get that?",
      ask=choose(["42 − 7", "42 + 7", "42 ÷ 5"], 0,
                 "5 sides is all 6 sides with one side left out. So we can take one side, 7, away from the whole perimeter.")),
    B("42 minus 7 is 35. The 5 sides add up to 35 centimetres.",
      ANSR("b", "42 − 7 = 35", "35")),
    B("We can also multiply. 5 sides of 7 centimetres is 35. Two ways, one answer.",
      W("c", "5 × 7 = 35")),
    B("The trap is dividing 42 by 5. The 42 belongs to all 6 sides, so we must find one side first."),
    B("So with a regular shape, always find one side first. After that you can build any number of sides you like."),
)

# Triangle with sides 3.2, 4.6 and 5.3: perimeter.
LESSONS[P + "q024"] = lesson(
    B("A triangle with sides 3.2, 4.6 and 5.3 centimetres. The perimeter is the walk all the way round, so we add the three sides.",
      GIVEN("q1", "Triangle: sides 3.2 cm, 4.6 cm, 5.3 cm. Perimeter = ?"),
      FIG("f1", {"kind": "triangle", "shape": "scalene", "sides": {"ab": "3.2 cm", "bc": "5.3 cm", "ca": "4.6 cm"}}),
      W("a", "3.2 + 4.6 + 5.3")),
    B("Add the whole numbers first. 3 plus 4 plus 5 is 12.",
      W("b", "3 + 4 + 5 = 12")),
    B("Now the tenths: 2 tenths, 6 tenths and 3 tenths. How many tenths is that altogether?",
      ask=choose(["11 tenths", "10 tenths", "1 tenth"], 0,
                 "Add them like ordinary numbers. 2 plus 6 is 8, and 3 more makes 11. So there are 11 tenths.")),
    B("11 tenths is more than one whole. It is 1 whole and 1 tenth, which we write as 1.1. This is the step that often gets dropped.",
      W("c", "0.2 + 0.6 + 0.3 = 1.1")),
    B("12 plus 1.1 is 13.1. The perimeter is 13.1 centimetres.",
      W("d", "12 + 1.1 = 13.1"), ANSR("e", "3.2 + 4.6 + 5.3 = 13.1", "13.1")),
    B("Check by adding in order. 3.2 plus 4.6 is 7.8, and 7.8 plus 5.3 is 13.1 again.",
      W("g", "3.2 + 4.6 = 7.8"), W("h", "7.8 + 5.3 = 13.1")),
    B("So with decimals, add the wholes, add the tenths, and when the tenths go past 10, carry a whole across."),
)
