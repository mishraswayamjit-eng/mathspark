"""Rule-made geometry lessons: one function per question wording.

RULES is a list of (regular expression, function). The function gets the question and the
match and returns a lesson. Every number on the board is computed here, never typed.
"""
import re

from geometry_lib import (B, FIG, LV, T, W, arc, ask, both, divide, fmt, hpick, lesson, mark, strike)

RULES = []


def rule(pattern):
    def register(fn):
        RULES.append((re.compile(pattern), fn))
        return fn
    return register


# ── "Solve: ax ± b = c" (filed under this topic, taught as an equation) ──────

@rule(r"^Solve: (\d+)x ([+−-]) (\d+) = (\d+)$")
def solve_linear(q, m):
    qid = q["id"]
    a, sign, b, c = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    plus = sign == "+"
    sign = "+" if plus else "−"
    undo = "−" if plus else "+"
    mid = c - b if plus else c + b
    x = mid // a
    assert a * x == mid
    word = "plus" if plus else "minus"
    undo_word = "subtract" if plus else "add"
    undo_say = "take away" if plus else "add"

    l1 = "%dx %s %d = %d" % (a, sign, b, c)
    opening = hpick(qid, "open", [
        "Here is our equation. %d x, %s %d, equals %d. A number is hiding behind that x, and we are going to find it.",
        "Look at this equation. %d x, %s %d, equals %d. Our job is to find the number that x stands for.",
        "Let's solve this one together. %d x, %s %d, equals %d. Somewhere behind the x there is a hidden number.",
    ]) % (a, word, b, c)
    balance = hpick(qid, "bal", [
        "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what is in the way of the %d x?",
        "The two sides are level, like a see-saw. We want the %d x on its own. What is in its way?",
    ]) % a
    if plus:
        why = "To undo plus %d, we take away %d. And to keep the balance level, we take it from both sides." % (b, b)
        after = "On the left, plus %d and minus %d cancel each other out. On the right, %d minus %d makes %d." % (b, b, c, b, mid)
    else:
        why = "To undo minus %d, we add %d. And to keep the balance level, we add it to both sides." % (b, b)
        after = "On the left, minus %d and plus %d cancel each other out. On the right, %d plus %d makes %d." % (b, b, c, b, mid)
    times = hpick(qid, "times", [
        "Nearly there. %d x means %d times x. What undoes times %d?",
        "Now only the %d is stuck to x. %d x means %d times x. So how do we undo times %d?",
    ])
    times = times % ((a, a, a) if times.count("%d") == 3 else (a, a, a, a))
    found = hpick(qid, "found", [
        "%d divided by %d is %d. So x equals %d. There is our hidden number!",
        "%d divided by %d is %d. So x equals %d. We found it.",
        "%d shared into %d equal parts gives %d each. So x equals %d.",
    ]) % (mid, a, x, x)
    check_open = hpick(qid, "chk", [
        "Good mathematicians always check. Put %d back in place of x.",
        "Now the check. Swap the x for %d and see if the two sides agree.",
        "Let's make sure. Put %d where the x was.",
    ]) % x
    check_say = "%s %d times %d is %d, and %d %s %d is %d. It works." % (check_open, a, x, mid, mid, word, b, c)
    plan = hpick(qid, "plan", [
        "So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times. Your turn next!",
        "Remember the order. First undo the plus or minus, on both sides. Then divide, on both sides. That is the whole method.",
        "Two undo steps, in order: first the number that is added or taken away, then the number that multiplies x. And always the same on both sides.",
    ])

    beats = [
        B(opening, W("l1", l1, tone="given")),
        B(balance, ask=ask(qid + "a1", "the %s %d" % (sign, b), ["the %d on the right" % c, "the %d in front of x" % a],
                           "Look at the left side once more. The %d x has a %s %d hanging on to it. That is the first thing to clear away." % (a, word, b))),
        B(why, strike("l1", "%s %d" % (sign, b), "%s %d" % (undo, b)), both("l1", "%s %d" % (undo, b))),
        B(after, W("l2", "%dx = %d %s %d" % (a, c, undo, b)), W("l3", "%dx = %d" % (a, mid))),
        B(times, ask=ask(qid + "a2", "divide by %d" % a, ["%s %d" % (undo_word, a), "multiply by %d" % a],
                         "Times and divide are partners. Whatever times does, divide undoes. So to undo times %d, we divide by %d." % (a, a))),
        B(hpick(qid, "div", [
            "So we divide both sides by %d. Careful: both sides, or the balance tips.",
            "So we divide by %d. And we do it to both sides, to keep the balance level.",
            "Divide by %d, then. The left side and the right side, both of them.",
        ]) % a, divide("l3", str(a))),
        B(found, W("l4", "x = %d" % x, tone="answer"), mark("l4", "x = %d" % x, "circle")),
        B(check_say, W("l5", "%d × %d %s %d = %d" % (a, x, sign, b, c))),
        B(plan),
    ]
    del undo_say
    return lesson(beats, "rule", check=("x", x))


# ── Supplementary and complementary angles ───────────────────────────────────

def take_away_beats(whole, n, result_id):
    """Beats that work out whole − n, in two easy hops when n is not a round number.
    The last line written is `whole − n = answer`, with id `result_id`."""
    ans = whole - n
    tens, ones = n - n % 10, n % 10
    final = W(result_id, "%d − %d = %d" % (whole, n, ans))
    if ones == 0 or tens == 0:
        return [B("%d take away %d leaves %d." % (whole, n, ans), final)]
    step = whole - tens
    return [
        B("Let's take %d away in two easy hops. First the %d: %d take away %d leaves %d." % (n, tens, whole, tens, step),
          W(result_id + "a", "%d − %d = %d" % (whole, tens, step))),
        B("Now the %d that is left: %d take away %d leaves %d. So %d minus %d is %d." % (ones, step, ones, ans, whole, n, ans),
          W(result_id + "b", "%d − %d = %d" % (step, ones, ans)), final),
    ]


def angle_pair(q, n, kind, given_text):
    """The partner of n degrees on a straight line (kind 'supp') or in a right angle ('comp')."""
    qid = q["id"]
    supp = kind == "supp"
    whole = 180 if supp else 90
    other = 90 if supp else 180
    ans = whole - n
    layout = "onLine" if supp else "inRightAngle"
    name = "supplementary" if supp else "complementary"
    start = FIG("f1", kind="angles", layout=layout, parts=[{"label": "%d°" % n, "size": n}, {"label": "?"}])
    done = FIG("f2", kind="angles", layout=layout, highlight=["p1"],
               parts=[{"label": "%d°" % n, "size": n}, {"label": "%d°" % ans, "size": ans}])

    if supp:
        opening = hpick(qid, "open", [
            "We need the supplementary angle of %d degrees. Supplementary angles are two angles that sit side by side on a straight line. Here is the picture.",
            "Our angle is %d degrees, and we want its supplementary partner. That means the two angles lie together along a straight line, like this.",
            "Here is %d degrees, drawn on a straight line. Its supplementary angle is the other piece of that line, the one marked with a question mark.",
        ]) % n
        why = hpick(qid, "why", [
            "Stand at the point and turn from one end of the line to the other. That is a half turn.",
            "Picture yourself standing where the two angles meet. Facing along the line one way, then turning to face the other way, is a half turn.",
        ])
        why_line = W("l2", "Straight line = half turn = 180°", label=True)
        question = "So how much do our two angles make together?"
        told = "A straight line is a half turn, and a half turn is 180 degrees."
        if_not = "Look at the drawing. The two angles lie along a straight line, and a straight line is a half turn. That makes 180 degrees. 90 is for a corner, a right angle."
        trap = "Here is a way to remember. S for supplementary, S for straight line: 180. C for complementary, C for corner: 90."
    else:
        opening = hpick(qid, "open", [
            "We need the complementary angle of %d degrees. Complementary angles are two angles that fit together to make a right angle, like the corner of a page. Here is the picture.",
            "Our angle is %d degrees, and we want its complementary partner. That means the two angles fit snugly into one square corner, like this.",
            "Here is %d degrees, drawn inside a right angle. Its complementary angle is the other piece of that corner, the one marked with a question mark.",
        ]) % n
        why = hpick(qid, "why", [
            "A right angle is a square corner, like the corner of a book or a door. Turning through it is a quarter turn.",
            "Picture the corner of your notebook. That square corner is a right angle, a quarter of a full turn.",
        ])
        why_line = W("l2", "Right angle = quarter turn = 90°", label=True)
        question = "So how much do our two angles make together?"
        told = "A right angle is a quarter turn, and a quarter turn is 90 degrees."
        if_not = "Look at the drawing. The two angles fit inside a square corner, and a square corner is a quarter turn. That makes 90 degrees. 180 is for a straight line."
        trap = "Here is a way to remember. C for complementary, C for corner: 90. S for supplementary, S for straight line: 180."

    how = hpick(qid, "how", [
        "We know the whole, %d, and one part, %d. How do we find the other part?",
        "The whole is %d and one piece is %d. What sum finds the missing piece?",
    ]) % (whole, n)
    slips = ["%d + %d" % (whole, n), "%d − %d" % (other, n)] if n < other else ["%d + %d" % (whole, n), "%d − %d" % (n, 90)]
    closing = hpick(qid, "close", [
        "So for a %s angle, take the angle away from %d." % (name, whole),
        "So %s partners make %d: subtract the angle you have from %d." % (name, whole, whole),
    ])
    if supp:
        trap = "To remember which is which: S for supplementary, S for straight line. C for complementary, C for corner."
    else:
        trap = "To remember which is which: C for complementary, C for corner. S for supplementary, S for straight line."

    beats = [
        B(opening, W("l1", given_text, tone="given", label=True), start),
        B(why + " " + question,
          ask=ask(qid + "a1", "%d°" % whole, ["%d°" % other, "360°"], if_not)),
        B(told + " So %d degrees, plus our missing angle, makes %d degrees." % (n, whole),
          why_line, mark("l2", "%d°" % whole, "box"),
          W("l3", "angle + partner = %d°" % whole, label=True), W("l4", "%d + ? = %d" % (n, whole)),
          mark("l4", "?", "circle")),
        B(how, ask=ask(qid + "a2", "%d − %d" % (whole, n), slips,
                       "When we know the whole and one part, we take the part away from the whole. So it is %d take away %d." % (whole, n))),
    ]
    beats += take_away_beats(whole, n, "l5")
    beats += [
        B("So the %s angle is %d degrees. Watch it go into the drawing." % (name, ans),
          W("l6", "%s angle = %d°" % (name.capitalize(), ans), tone="answer", label=True),
          mark("l6", "%d°" % ans, "circle"), done),
        B("Let's check by adding them back. %d plus %d makes %d. It fits exactly." % (n, ans, whole),
          W("l7", "%d + %d = %d" % (n, ans, whole))),
        B(closing + " " + trap),
    ]
    return lesson(beats, "rule")


@rule(r"^Find the supplementary angle of (\d+)°\.$")
def supplementary(q, m):
    n = int(m.group(1))
    return angle_pair(q, n, "supp", "Supplementary angle of %d° = ?" % n)


@rule(r"^Find the complementary angle of (\d+)°\.$")
def complementary(q, m):
    n = int(m.group(1))
    return angle_pair(q, n, "comp", "Complementary angle of %d° = ?" % n)


@rule(r"^Two angles are supplementary\. If one angle is (\d+)°, find the other\.$")
def supplementary_other(q, m):
    n = int(m.group(1))
    return angle_pair(q, n, "supp", "Supplementary angles: %d° and ?" % n)


@rule(r"^(?=.*complementary).*\((\d+|[a-z]) − (\d+|[a-z])\)°")
def complement_of_expression(q, m):
    """The complement of (38 − x)° or of (x − 35)°: 90 minus a whole bracket."""
    qid = q["id"]
    first, second = m.group(1), m.group(2)
    letter_last = first.isdigit()
    c = int(first if letter_last else second)
    v = second if letter_last else first
    angle = "(%s − %s)" % (first, second)
    if letter_last:
        total = 90 - c
        answer = "%d + %s" % (total, v)
        opened = "90 − %d + %s" % (c, v)
        sum_line = W("l5", "90 − %d = %d" % (c, total))
        sign_q = "Taking the bracket away takes away the %d. But what happens to the minus %s inside?" % (c, v)
        right, slips = "it becomes + %s" % v, ["it stays − %s" % v, "it disappears"]
        if_not = "The angle is %d with %s already taken off, so it is smaller than %d. Take a smaller angle from 90 and more is left over. So the %s comes back as plus %s." % (c, v, c, v, v)
        open_say = "Careful here: the minus in front of the bracket reaches both things inside. The %d becomes minus %d, and the minus %s becomes plus %s." % (c, c, v, v)
        arc_to = [str(c), "− %s" % v]
        tidy = "Now tidy up. 90 take away %d is %d. So we have %d plus %s." % (c, total, total, v)
        check_say = "Check by adding the two angles. The minus %s and the plus %s cancel, and %d plus %d is 90. A perfect right angle." % (v, v, c, total)
        check_num = W("l8", "%d + %d = 90" % (c, total))
        trap = "The slip to watch for is leaving the sign alone and writing %d minus %s. Taking away a bracket flips the signs inside it." % (total, v)
    else:
        total = 90 + c
        answer = "%d − %s" % (total, v)
        opened = "90 − %s + %d" % (v, c)
        sum_line = W("l5", "90 + %d = %d" % (c, total))
        sign_q = "Taking the bracket away takes away the %s. But what happens to the minus %d inside?" % (v, c)
        right, slips = "it becomes + %d" % c, ["it stays − %d" % c, "it disappears"]
        if_not = "The angle is %s with %d already taken off. Taking away an angle that is %d smaller leaves %d more. So the %d comes back as plus %d." % (v, c, c, c, c, c)
        open_say = "Careful here: the minus in front of the bracket reaches both things inside. The %s becomes minus %s, and the minus %d becomes plus %d." % (v, v, c, c)
        arc_to = [v, "− %d" % c]
        tidy = "Now tidy up. 90 plus %d is %d. So we have %d minus %s." % (c, total, total, v)
        check_say = "Check by adding the two angles. The %s and the minus %s cancel, and %d take away %d is 90. A perfect right angle." % (v, v, total, c)
        check_num = W("l8", "%d − %d = 90" % (total, c))
        trap = "The slip to watch for is leaving the sign alone. Taking away a bracket flips the signs inside it, so minus %d turns into plus %d." % (c, c)

    tests = ({v: 3}, {v: 12})
    opening = hpick(qid, "open", [
        "Our angle is not a plain number this time. It is %s minus %s degrees, all in one bracket. We want its complementary angle.",
        "Here the angle is written with a letter: %s minus %s degrees. We need the angle that is complementary to it.",
    ]) % (first, second)
    l4 = "90 − %s = %s" % (angle, opened)
    beats = [
        B(opening, W("l1", "Angle = %s°. Complementary angle = ?" % angle, tone="given", label=True),
          FIG("f1", kind="angles", layout="inRightAngle", parts=[{"label": "%s°" % angle}, {"label": "?"}])),
        B("Complementary angles fit together in a square corner, a right angle. So what do the two of them add up to?",
          ask=ask(qid + "a1", "90°", ["180°", "360°"],
                  "A right angle is a quarter turn, and a quarter turn is 90 degrees. 180 is for a straight line.")),
        B("A right angle is 90 degrees. So the partner is 90 take away our angle. And our angle is the whole bracket, so the whole bracket is taken away.",
          W("l2", "complement = 90° − angle", label=True), W("l3", "90 − %s" % angle, label=True), mark("l3", angle, "box")),
        B(sign_q, ask=ask(qid + "a2", right, slips, if_not)),
        B(open_say, LV("l4", l4, *tests), arc("l4", T("−", 1), arc_to)),
        B(tidy, sum_line, LV("l6", "%s = %s" % (opened, answer), *tests)),
        B("So the complementary angle is %s degrees, written in a bracket." % answer.replace("+", "plus").replace("−", "minus"),
          W("l7", "Complementary angle = (%s)°" % answer, tone="answer", label=True), mark("l7", "(%s)°" % answer, "circle"),
          FIG("f2", kind="angles", layout="inRightAngle", highlight=["p1"],
              parts=[{"label": "%s°" % angle}, {"label": "(%s)°" % answer}])),
        B(check_say, check_num, LV("l9", "%s + (%s) = 90" % (angle, answer), *tests)),
        B(trap),
    ]
    return lesson(beats, "rule")


@rule(r"^In a triangle, two angles are (\d+)° and (\d+)°\. Find the third angle\.$")
def triangle_third_angle(q, m):
    qid = q["id"]
    p, r = int(m.group(1)), int(m.group(2))
    used = p + r
    ans = 180 - used
    f1 = FIG("f1", kind="triangle", shape="scalene", angles={"b": "%d°" % p, "c": "%d°" % r, "a": "?"})
    f2 = FIG("f2", kind="triangle", shape="scalene", angles={"b": "%d°" % p, "c": "%d°" % r, "a": "%d°" % ans},
             highlight=["a"])
    beats = [
        B("Here is our triangle. Two of its angles are %d degrees and %d degrees. The third one, at the top, is our mystery." % (p, r),
          W("l1", "Triangle: angles %d°, %d° and ?" % (p, r), tone="given", label=True), f1),
        B("Here is something you can try with paper. Tear the 3 corners off any triangle and put them side by side. They always make a straight line. So how much do the 3 angles make together?",
          ask=ask(qid + "a1", "180°", ["90°", "360°"],
                  "A straight line is a half turn, and a half turn is 180 degrees. So the 3 angles of a triangle always make 180 degrees.")),
        B("A straight line is a half turn, 180 degrees. So the 3 angles of any triangle add up to 180 degrees.",
          W("l2", "Angles of a triangle add up to 180°", label=True), mark("l2", "180°", "box"),
          W("l3", "%d + %d + ? = 180" % (p, r)), mark("l3", "?", "circle")),
        B("First, how much have the two angles we know used up? %d plus %d is %d." % (p, r, used),
          W("l4", "%d + %d = %d" % (p, r, used))),
        B("So %d of the 180 degrees is gone. What sum finds the third angle?" % used,
          ask=ask(qid + "a2", "180 − %d" % used, ["180 + %d" % used, "180 − %d" % p],
                  "Both known angles have to come off the 180, not just one of them. Together they are %d, so it is 180 take away %d." % (used, used))),
    ]
    beats += take_away_beats(180, used, "l5")
    beats += [
        B("So the third angle is %d degrees. Into the drawing it goes." % ans,
          W("l6", "Third angle = %d°" % ans, tone="answer", label=True), mark("l6", "%d°" % ans, "circle"), f2),
        B("Check: %d plus %d plus %d makes 180. All three together make the straight line." % (p, r, ans),
          W("l7", "%d + %d + %d = 180" % (p, r, ans))),
        B("So for any triangle: add the two angles you know, then take the total away from 180. The slip to watch for is taking away only one of them."),
    ]
    return lesson(beats, "rule")


@rule(r"^Two angles on a straight line are x° and (\d+)°\. Find x\.$")
def straight_line_x(q, m):
    qid = q["id"]
    n = int(m.group(1))
    x = 180 - n
    f1 = FIG("f1", kind="angles", layout="onLine", parts=[{"label": "x°"}, {"label": "%d°" % n, "size": n}])
    f2 = FIG("f2", kind="angles", layout="onLine", highlight=["p0"],
             parts=[{"label": "%d°" % x, "size": x}, {"label": "%d°" % n, "size": n}])
    hops = take_away_beats(180, n, "l5")
    beats = [
        B("Here is a straight line with two angles sitting on it. One is %d degrees. The other is called x, and we want to know its size." % n,
          W("l1", "On a straight line: x° and %d°. x = ?" % n, tone="given", label=True), f1),
        B("Stand where the two angles meet. Facing along the line one way, then turning to face the other way, is a half turn. So how much do the two angles make together?",
          ask=ask(qid + "a1", "180°", ["90°", "360°"],
                  "The two angles lie along a straight line, and a straight line is a half turn. That makes 180 degrees. 90 is for a square corner.")),
        B("A half turn is 180 degrees. So x, plus %d, equals 180. Now it is an equation." % n,
          W("l2", "Straight line = half turn = 180°", label=True), mark("l2", "180°", "box"),
          W("l3", "x + %d = 180" % n)),
        B("We want x on its own. What do we do about the plus %d?" % n,
          ask=ask(qid + "a2", "take %d from both sides" % n, ["add %d to both sides" % n, "take %d from 90" % n],
                  "To undo plus %d, we take away %d. And to keep the two sides level, we take it from both sides." % (n, n))),
        B("To undo plus %d, we take %d away, from both sides." % (n, n),
          strike("l3", "+ %d" % n, "− %d" % n), both("l3", "− %d" % n), W("l4", "x = 180 − %d" % n)),
    ]
    beats += hops
    beats += [
        B("So x equals %d. The other angle is %d degrees." % (x, x),
          W("l6", "x = %d" % x, tone="answer"), mark("l6", "x = %d" % x, "circle"), f2),
        B("Check: %d plus %d makes 180, a full straight line. It fits." % (x, n),
          W("l7", "%d + %d = 180" % (x, n))),
        B("So angles on a straight line always make 180 degrees. Take the one you know away from 180, and you have the other."),
    ]
    return lesson(beats, "rule", check=("x", x))


@rule(r"^Two straight lines cross\. One angle formed is (\d+)°\. Find the vertically opposite angle\.$")
def vertically_opposite(q, m):
    qid = q["id"]
    n = int(m.group(1))
    side = 180 - n
    f1 = FIG("f1", kind="angles", layout="crossing",
             parts=[{"label": "%d°" % n, "size": n}, {"label": "p"}, {"label": "?"}, {"label": "q"}])
    f2 = FIG("f2", kind="angles", layout="crossing", highlight=["p0", "p1"],
             parts=[{"label": "%d°" % n, "size": n}, {"label": "%d°" % side}, {"label": "?"}, {"label": "q"}])
    f3 = FIG("f3", kind="angles", layout="crossing", highlight=["p0", "p2"],
             parts=[{"label": "%d°" % n, "size": n}, {"label": "%d°" % side}, {"label": "%d°" % n}, {"label": "%d°" % side}])
    first = take_away_beats(180, n, "l3")
    first[0]["say"] = "Look at %d degrees and its neighbour, p. They sit side by side on one straight line. " % n + first[0]["say"]
    second = take_away_beats(180, side, "l4")
    beats = [
        B("Two straight lines cross and make 4 angles. One of them is %d degrees. We want the angle vertically opposite: the one straight across the crossing point." % n,
          W("l1", "Lines cross: one angle is %d°. Opposite angle = ?" % n, tone="given", label=True), f1),
        B("I have called the two angles next door p and q. Now, here is what we know about a straight line: it is a half turn, and a half turn is 180 degrees.",
          W("l2", "Angles on a straight line = 180°", label=True), mark("l2", "180°", "box")),
    ]
    beats += first
    beats += [
        B("So p is %d degrees. Now look at p and our mystery angle. They sit side by side on the other straight line. So what is the mystery angle?" % side,
          f2,
          ask=ask(qid + "a1", "180 − %d" % side, ["%d, the same as p" % side, "180 + %d" % side],
                  "p and the mystery angle share a straight line, so together they make 180 degrees. We take p, which is %d, away from 180." % side)),
    ]
    beats += second
    beats += [
        B("%d degrees. Exactly the angle we started with! That always happens: angles straight across from each other are equal." % n,
          W("l5", "Vertically opposite angles are equal", label=True),
          W("l6", "Opposite angle = %d°" % n, tone="answer", label=True), mark("l6", "%d°" % n, "circle"), f3),
        B("So next time you can say it straight away: the vertically opposite angle is equal, %d degrees. The slip to watch for is giving %d, which is the neighbour on the line." % (n, side)),
    ]
    return lesson(beats, "rule")


# ── Perimeter and area ───────────────────────────────────────────────────────

@rule(r"^Find the circumference of a circle with radius (\d+) cm\. \(Use π = 22/7\)$")
def circumference(q, m):
    qid = q["id"]
    r = int(m.group(1))
    d = 2 * r
    assert d % 7 == 0
    k = d // 7
    c = 22 * k
    rough = 3 * d
    beats = [
        B("Here is our circle. Its radius, from the centre out to the edge, is %d centimetres. We want the circumference, and we are told to use 22 over 7 for pi." % r,
          W("l1", "Circle: radius %d cm, π = 22/7. Circumference = ?" % r, tone="given", label=True),
          FIG("f1", kind="circle", radius="%d cm" % r, note="Circumference = ?")),
        B("Circumference is the walk all the way round the circle. And here is a lovely fact: for every circle, that walk is a little more than 3 times the distance straight across. That number is pi.",
          W("l2", "Circumference = π × diameter", label=True)),
        B("We were given the radius, %d. So what is the distance straight across, the diameter?" % r,
          ask=ask(qid + "a1", "2 × %d" % r, ["%d, the same" % r, "%d ÷ 2" % r],
                  "The radius only goes from the centre to the edge. The diameter goes right across, through the centre. That is 2 radii, so 2 times %d." % r)),
        B("The diameter is 2 radii: 2 times %d is %d centimetres. That is why the rule is often written as 2 times pi times the radius." % (r, d),
          W("l3", "2 × %d = %d" % (r, d)), FIG("f2", kind="circle", diameter="%d cm" % d, highlight=["diameter"]),
          W("l4", "Circumference = 2 × π × radius", label=True)),
        B("Now we need 22 over 7, times %d. Divide by the 7 first, because %d is in the 7 times table: %d divided by 7 is %d." % (d, d, d, k),
          W("l5", "%d ÷ 7 = %d" % (d, k))),
        B("Then multiply by the 22. 22 times %d is %d." % (k, c),
          W("l6", "22 × %d = %d" % (k, c)), W("l7", "2 × 22/7 × %d = %d" % (r, c))),
        B("So the circumference is %d centimetres. Plain centimetres, because it is a length, a walk round the edge." % c,
          W("l8", "Circumference = %d cm" % c, tone="answer", label=True), mark("l8", "%d cm" % c, "circle"),
          FIG("f3", kind="circle", radius="%d cm" % r, highlight=["edge"], note="Circumference = %d cm" % c)),
        B("Does that make sense? 3 times %d is %d, and our answer, %d, is a little more than that. Just as pi promised." % (d, rough, c),
          W("l9", "3 × %d = %d" % (d, rough))),
        B("So: circumference is 2 times pi times the radius. The slip to watch for is forgetting to double the radius, which gives only half the walk."),
    ]
    return lesson(beats, "rule")


def times_beats(a, b, result_id, lead=""):
    """Beats that work out a × b, splitting a two-digit number into tens and ones when
    the product is not one a child knows. The last line written is `a × b = product`."""
    product = a * b
    final = W(result_id, "%d × %d = %d" % (a, b, product))
    easy = (a <= 10 and b <= 10) or a % 10 == 0 or b % 10 == 0 or a == 1 or b == 1
    # 30 × 15: do 3 × 15 first, then make it 10 times bigger.
    for round_one, other in ((a, b), (b, a)):
        if round_one % 10 == 0 and 20 <= round_one < 100 and other > 10 and other % 10 != 0:
            small = round_one // 10
            return [B("%s%d times %d. Do %d times %d first: that is %d. Then make it 10 times bigger, and we have %d." % (
                lead, a, b, small, other, small * other, product),
                W(result_id + "a", "%d × %d = %d" % (small, other, small * other)), final)]
    if easy:
        return [B("%s%d times %d is %d." % (lead, a, b, product), final)]
    # Split the number that leaves the easier sums: a two-digit number with the smaller ones digit.
    if b > 10 and (a <= 10 or b % 10 <= a % 10):
        keep, split = a, b
    else:
        keep, split = b, a
    tens, ones = split - split % 10, split % 10
    p1, p2 = keep * tens, keep * ones
    return [
        B("%s%d times %d is easier in two pieces. Split the %d into %d and %d. First, %d times %d is %d." % (
            lead, a, b, split, tens, ones, keep, tens, p1),
          W(result_id + "a", "%d × %d = %d" % (keep, tens, p1))),
        B("And %d times %d is %d. Put the two pieces together: %d plus %d makes %d." % (keep, ones, p2, p1, p2, product),
          W(result_id + "b", "%d × %d = %d" % (keep, ones, p2)),
          W(result_id + "c", "%d + %d = %d" % (p1, p2, product)), final),
    ]


def UNIT_ASK(qid, area):
    """The unit slip: an area is in square centimetres, not centimetres."""
    return B("We have our number, %d. But %d what? Which unit goes with an area?" % (area, area),
             ask=ask(qid + "au", "square centimetres", ["centimetres"],
                     "Centimetres measure a length, like an edge. Area counts the little squares inside, so it is measured in square centimetres."))


@rule(r"^Find the area of a triangle with base (\d+) cm and height (\d+) cm\.$")
def triangle_area(q, m):
    qid = q["id"]
    b, h = int(m.group(1)), int(m.group(2))
    rect = b * h
    area = fmt(rect / 2.0)
    f1 = FIG("f1", kind="triangle", shape="scalene", sides={"bc": "%d cm" % b}, height="%d cm" % h, note="Area = ?")
    f2 = FIG("f2", kind="triangle", shape="scalene", sides={"bc": "%d cm" % b}, height="%d cm" % h, enclose=True)
    f3 = FIG("f3", kind="triangle", shape="scalene", sides={"bc": "%d cm" % b}, height="%d cm" % h, enclose=True,
             highlight=["fill"], note="Area = %s sq. cm" % area)
    opening = hpick(qid, "open", [
        "Here is our triangle. Its base is %d centimetres and its height is %d centimetres. We want its area, the flat space inside.",
        "Look at this triangle. The base, along the bottom, is %d centimetres. The height, straight up, is %d centimetres. How much space is inside?",
        "We need the area of this triangle. The base is %d centimetres and the height is %d centimetres. Area means the space inside the shape.",
    ]) % (b, h)
    box = hpick(qid, "box", [
        "A triangle is tricky to fill with squares. So here is a trick: I draw a rectangle snugly around it, as wide as the base and as tall as the height.",
        "Counting squares inside a triangle is awkward. So let me box it in: a rectangle around the triangle, with the same base and the same height.",
    ])
    half_q = hpick(qid, "half", [
        "Now look closely. The two corner pieces outside the triangle fit together to make another triangle, just the same size. So what do we do with %d?",
        "Look at the drawing. The triangle fills exactly half of the rectangle, and the leftover corners make the other half. So what do we do with %d?",
    ]) % rect
    if rect % 2 == 0:
        halve = "Half of %d is %s. And see how it is written: a half, times %d, times %d." % (rect, area, b, h)
    else:
        halve = "%d is odd, so its half has a point 5 on the end: %s. And see how it is written: a half, times %d, times %d." % (rect, area, b, h)
    closing = hpick(qid, "close", [
        "So for any triangle: multiply base by height to get the rectangle, then halve it. The slip to watch for is forgetting the half.",
        "The method in one line: half of base times height. If you stop at base times height, you have found the whole rectangle, not the triangle.",
    ])

    beats = [
        B(opening, W("l1", "Triangle: base %d cm, height %d cm. Area = ?" % (b, h), tone="given", label=True), f1),
        B(box + " How do we find the area of that rectangle?", f2,
          ask=ask(qid + "a0", "%d × %d" % (b, h), ["%d + %d" % (b, h), "2 × (%d + %d)" % (b, h)],
                  "Adding the sides is for the walk round the edge. The space inside a rectangle is its length times its breadth.")),
        B("The area of a rectangle is its length times its breadth. Here that means base times height.",
          W("l2", "Rectangle area = base × height", label=True)),
    ]
    beats += times_beats(b, h, "l3")
    beats += [
        B(half_q, mark("l3", str(rect), "underline"),
          ask=ask(qid + "a1", "halve it: %d ÷ 2" % rect, ["keep it as %d" % rect, "double it: %d × 2" % rect],
                  "Look at the drawing once more. The triangle covers only half of the dashed rectangle. So we need half of %d." % rect)),
        B("So the rule for a triangle is: half of base times height.",
          W("l4", "Triangle area = ½ × base × height", label=True), mark("l4", "½", "circle")),
        B(halve, W("l5", "½ × %d × %d = %s" % (b, h, area))),
        B("So the area of the triangle is %s square centimetres. Square centimetres, because area counts little squares." % area,
          W("l6", "Area = %s sq. cm" % area, tone="answer", label=True), mark("l6", "%s sq. cm" % area, "circle"), f3),
        B("A quick check: two triangles of %s make %d, the whole rectangle. It fits." % (area, rect),
          W("l7", "%s + %s = %d" % (area, area, rect))),
        B(closing),
    ]
    return lesson(beats, "rule")


@rule(r"^Find the area of a rectangle with length (\d+) cm and breadth (\d+) cm\.$")
def rectangle_area(q, m):
    qid = q["id"]
    l, b = int(m.group(1)), int(m.group(2))
    area = l * b
    prop = max(1.0, min(3.0, round(l / float(b), 2)))
    f1 = FIG("f1", kind="rectangle", length="%d cm" % l, breadth="%d cm" % b, inside="Area = ?", proportion=prop)
    small = l <= 12 and b <= 12
    if small:
        f2 = FIG("f2", kind="rectangle", length="%d cm" % l, breadth="%d cm" % b, proportion=prop, grid={"cols": l, "rows": b})
        tiles = "Area is the flat space inside. Let's tile the rectangle with little squares, each 1 centimetre wide. Each row has %d squares, and there are %d rows." % (l, b)
    else:
        f2 = FIG("f2", kind="rectangle", length="%d cm" % l, breadth="%d cm" % b, proportion=prop, highlight=["fill"])
        tiles = "Area is the flat space inside. Imagine tiling the rectangle with little squares, each 1 centimetre wide. Each row would have %d squares, and there would be %d rows." % (l, b)
    f3 = FIG("f3", kind="rectangle", length="%d cm" % l, breadth="%d cm" % b, proportion=prop,
             inside="%d sq. cm" % area, highlight=["fill"])
    opening = hpick(qid, "open", [
        "Here is our rectangle. It is %d centimetres long and %d centimetres wide. We want its area.",
        "Look at this rectangle. The length is %d centimetres and the breadth is %d centimetres. How much space does it cover?",
        "We need the area of this rectangle. Its length is %d centimetres and its breadth is %d centimetres.",
    ]) % (l, b)
    closing = hpick(qid, "close", [
        "So for any rectangle, area is length times breadth. Adding the sides is for the walk round the edge, the perimeter.",
        "The method in one line: area of a rectangle is length times breadth, and the answer is in square units.",
    ])
    beats = [
        B(opening, W("l1", "Rectangle: length %d cm, breadth %d cm. Area = ?" % (l, b), tone="given", label=True), f1),
        B(tiles, f2),
        B("How do we count all those squares quickly?",
          ask=ask(qid + "a1", "%d × %d" % (l, b), ["%d + %d" % (l, b), "2 × (%d + %d)" % (l, b)],
                  "Adding the sides tells us about the edge, not the inside. To count squares in equal rows, we multiply: the squares in one row, times the number of rows.")),
        B("Equal rows mean multiplying. So the rule is: area equals length times breadth.",
          W("l2", "Area = length × breadth", label=True)),
    ]
    beats += times_beats(l, b, "l3")
    beats += [
        UNIT_ASK(qid, area),
        B("So the area is %d square centimetres. We say square centimetres because we counted squares." % area,
          W("l4", "Area = %d sq. cm" % area, tone="answer", label=True), mark("l4", "%d sq. cm" % area, "circle"), f3),
        B("Let's check by dividing back. %d divided by %d is %d, our length. It fits." % (area, b, l),
          W("l5", "%d ÷ %d = %d" % (area, b, l))),
        B(closing),
    ]
    return lesson(beats, "rule")


@rule(r"^Find the area of a square with side (\d+) cm\.$")
def square_area(q, m):
    qid = q["id"]
    s = int(m.group(1))
    area = s * s
    f1 = FIG("f1", kind="rectangle", square=True, length="%d cm" % s, inside="Area = ?")
    if s <= 12:
        f2 = FIG("f2", kind="rectangle", square=True, length="%d cm" % s, breadth="%d cm" % s, grid={"cols": s, "rows": s})
        tiles = "A square has all its sides equal, so it is %d centimetres across and %d centimetres down. Let's tile it with little squares, each 1 centimetre wide: %d rows of %d." % (s, s, s, s)
    else:
        f2 = FIG("f2", kind="rectangle", square=True, length="%d cm" % s, breadth="%d cm" % s, highlight=["fill"])
        tiles = "A square has all its sides equal, so it is %d centimetres across and %d centimetres down. Imagine it tiled with little squares, each 1 centimetre wide: %d rows of %d." % (s, s, s, s)
    f3 = FIG("f3", kind="rectangle", square=True, length="%d cm" % s, breadth="%d cm" % s,
             inside="%d sq. cm" % area, highlight=["fill"])
    opening = hpick(qid, "open", [
        "Here is our square. Each side is %d centimetres. We want its area, the flat space inside.",
        "Look at this square, with a side of %d centimetres. How much space does it cover?",
    ]) % s
    beats = [
        B(opening, W("l1", "Square: side %d cm. Area = ?" % s, tone="given", label=True), f1),
        B(tiles, f2),
        B("Which sum counts all the little squares?",
          ask=ask(qid + "a1", "%d × %d" % (s, s), ["%d × 4" % s, "%d + %d" % (s, s)],
                  "%d times 4 is the walk round the 4 sides, the perimeter. For the squares inside, we need rows times squares in a row: %d times %d." % (s, s, s))),
        B("So the rule is: area of a square equals side times side.",
          W("l2", "Area of square = side × side", label=True)),
    ]
    beats += times_beats(s, s, "l3")
    beats += [
        UNIT_ASK(qid, area),
        B("So the area is %d square centimetres. Square centimetres, because we counted squares." % area,
          W("l4", "Area = %d sq. cm" % area, tone="answer", label=True), mark("l4", "%d sq. cm" % area, "circle"), f3),
        B("Let's check by dividing back. %d divided by %d is %d, the side we started with." % (area, s, s),
          W("l5", "%d ÷ %d = %d" % (area, s, s))),
        B(hpick(qid, "close", [
            "So for a square, area is side times side. Side times 4 is a different thing: that is the perimeter.",
            "Remember: side times side for the space inside, side times 4 for the walk round the outside.",
        ])),
    ]
    return lesson(beats, "rule")


@rule(r"^Find the perimeter of a square with side (\d+) cm\.$")
def square_perimeter(q, m):
    qid = q["id"]
    s = int(m.group(1))
    half, p = 2 * s, 4 * s
    side = "%d cm" % s
    f1 = FIG("f1", kind="rectangle", square=True, length=side, note="Perimeter = ?")
    f2 = FIG("f2", kind="polygon", points=[[3, 2], [9, 2], [9, 8], [3, 8]], edges=[side, side, side, side],
             rightAngles=[0, 1, 2, 3], highlight=["e0", "e1", "e2", "e3"])
    f3 = FIG("f3", kind="polygon", points=[[3, 2], [9, 2], [9, 8], [3, 8]], edges=[side, side, side, side],
             rightAngles=[0, 1, 2, 3], highlight=["e0", "e1", "e2", "e3"], note="Perimeter = %d cm" % p)
    opening = hpick(qid, "open", [
        "Here is our square, with a side of %d centimetres. We want its perimeter.",
        "Look at this square. One side is %d centimetres. How far is it all the way round?",
    ]) % s
    walk = hpick(qid, "walk", [
        "Perimeter is a walk all the way round the edge, back to where you started. A square has 4 equal sides, so every side is %d centimetres. Let me label them all.",
        "Think of an ant walking round the edge of the square until it is back at the start. That walk is the perimeter. All 4 sides are equal, so each one is %d centimetres.",
    ]) % s
    beats = [
        B(opening, W("l1", "Square: side %d cm. Perimeter = ?" % s, tone="given", label=True), f1),
        B(walk, f2),
        B("Which sum takes us all the way round?",
          ask=ask(qid + "a1", "%d + %d + %d + %d" % (s, s, s, s), ["%d + %d" % (s, s), "%d × %d" % (s, s)],
                  "The walk goes along every side, and a square has 4 of them. So we add %d four times. %d times %d would be the space inside, the area." % (s, s, s))),
        B("Let's walk it. The first two sides: %d plus %d is %d. That is halfway round." % (s, s, half),
          W("l2", "%d + %d = %d" % (s, s, half))),
        B("The other two sides are the same again: %d plus %d is %d." % (half, half, p),
          W("l3", "%d + %d = %d" % (half, half, p))),
        B("Adding the same number 4 times is multiplying by 4. So the rule is: perimeter of a square equals 4 times the side.",
          W("l4", "Perimeter of square = 4 × side", label=True), W("l5", "4 × %d = %d" % (s, p))),
        B("So the perimeter is %d centimetres. Plain centimetres, not square ones, because a perimeter is a length." % p,
          W("l6", "Perimeter = %d cm" % p, tone="answer", label=True), mark("l6", "%d cm" % p, "circle"), f3),
        B("Check with the whole walk: %d plus %d plus %d plus %d makes %d." % (s, s, s, s, p),
          W("l7", "%d + %d + %d + %d = %d" % (s, s, s, s, p))),
        B(hpick(qid, "close", [
            "So for a square, the perimeter is 4 times the side. Side times side is a different thing: that is the area.",
            "Remember: perimeter is the walk round, so add every side. For a square that is 4 times the side.",
        ])),
    ]
    return lesson(beats, "rule")


@rule(r"^Find the perimeter of a rectangle with length (\d+) cm and breadth (\d+) cm\.$")
def rectangle_perimeter(q, m):
    qid = q["id"]
    l, b = int(m.group(1)), int(m.group(2))
    half, p = l + b, 2 * (l + b)
    ll, bb = "%d cm" % l, "%d cm" % b
    prop = max(1.0, min(3.0, round(l / float(b), 2)))
    pts = [[1, 3], [11, 3], [11, 8], [1, 8]] if l >= b else [[3, 1], [8, 1], [8, 11], [3, 11]]
    f1 = FIG("f1", kind="rectangle", length=ll, breadth=bb, proportion=prop, note="Perimeter = ?")
    f2 = FIG("f2", kind="polygon", points=pts, edges=[ll, bb, ll, bb], rightAngles=[0, 1, 2, 3],
             highlight=["e0", "e1", "e2", "e3"])
    f3 = FIG("f3", kind="polygon", points=pts, edges=[ll, bb, ll, bb], rightAngles=[0, 1, 2, 3],
             highlight=["e0", "e1", "e2", "e3"], note="Perimeter = %d cm" % p)
    opening = hpick(qid, "open", [
        "Here is our rectangle. It is %d centimetres long and %d centimetres wide. We want its perimeter.",
        "Look at this rectangle. The length is %d centimetres and the breadth is %d centimetres. How far is it all the way round?",
        "We need the perimeter of this rectangle. Its length is %d centimetres and its breadth is %d centimetres.",
    ]) % (l, b)
    walk = hpick(qid, "walk", [
        "Perimeter is a walk all the way round the edge, back to where you started. Opposite sides of a rectangle are equal, so there are 2 lengths and 2 breadths. Let me label all 4 sides.",
        "Think of an ant walking round the edge until it is back at the start. That walk is the perimeter. It goes along 2 lengths and 2 breadths, because opposite sides are equal.",
    ])
    if l == b:
        slips = ["%d + %d" % (l, b), "%d × %d" % (l, b)]
    else:
        slips = ["%d + %d" % (l, b), "%d × %d" % (l, b)]
    beats = [
        B(opening, W("l1", "Rectangle: length %d cm, breadth %d cm. Perimeter = ?" % (l, b), tone="given", label=True), f1),
        B(walk, f2),
        B("Which sum takes us all the way round?",
          ask=ask(qid + "a1", "%d + %d + %d + %d" % (l, b, l, b), slips,
                  "%d plus %d only gets us halfway, along one length and one breadth. The walk goes along all 4 sides. And %d times %d would be the space inside, the area." % (l, b, l, b))),
        B("Let's walk it. One length and one breadth: %d plus %d is %d. That is halfway round." % (l, b, half),
          W("l2", "%d + %d = %d" % (l, b, half))),
        B("The other two sides are the same again, so we double it: %d plus %d is %d." % (half, half, p),
          W("l3", "%d + %d = %d" % (half, half, p))),
        B("That is where the rule comes from: add the length and the breadth, then double.",
          W("l4", "Perimeter = 2 × (length + breadth)", label=True), W("l5", "2 × (%d + %d) = %d" % (l, b, p)),
          mark("l5", "2", "circle")),
        B("So the perimeter is %d centimetres. Plain centimetres, because a perimeter is a length." % p,
          W("l6", "Perimeter = %d cm" % p, tone="answer", label=True), mark("l6", "%d cm" % p, "circle"), f3),
        B("Check with the whole walk: %d plus %d plus %d plus %d makes %d." % (l, b, l, b, p),
          W("l7", "%d + %d + %d + %d = %d" % (l, b, l, b, p))),
        B(hpick(qid, "close", [
            "So for a rectangle: add length and breadth, then double. The slip to watch for is stopping at halfway.",
            "The method in one line: perimeter is 2 times, length plus breadth. Do not stop after adding just two sides.",
        ])),
    ]
    return lesson(beats, "rule")
