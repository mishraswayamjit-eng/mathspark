"""Lessons by rule for the generated families of gr4_ratio (see g4_gr4_ratio.py)."""
import re

from g4_gr4_ratio_lib import (A, AM, C, F, G, Lb, N, U, W, bar, bars, beat, choose, lesson, pick, seg, segs)

AGES = re.compile(r"^The ages of (\w+) and (\w+) are in the ratio (\d+):(\d+)\. If (\w+) is (\d+) years old, how old is (\w+)\?$")
DIVIDE = re.compile(r"^Divide (\d+) in the ratio (\d+):(\d+)\. What is the (smaller|larger) share\?$")
GROUPS = re.compile(r"^(\w+) has (\d+) (\w+) and divides them in the ratio (\d+):(\d+)\. How many \w+ are in the (smaller|larger) group\?$")
EQUAL = re.compile(r"^If (\d+) : (\d+) = (\d+) : x, find x\.$")


def parts(n):
    return "1 part" if n == 1 else "%d parts" % n


def nth_at(line, text, pos):
    assert line[pos:pos + len(text)] == text, (line, text, pos)
    return line[:pos].count(text) + 1


def ages(q, m):
    qid = q["id"]
    first, second, a, b, known, n, asked = m.groups()
    a, b, n = int(a), int(b), int(n)
    assert known == second and asked == first and n % b == 0 and a != b
    p = n // b
    r = a * p
    q1 = "%s : %s = %s : %s" % (first, second, a, b)
    fig = bars(bar(first, segs(a, "a")), bar(second, segs(b, "b"), brace="%d years" % n))
    beats = [
        beat(pick(qid, "open", [
            "The ages of %s and %s are in the ratio %d to %d. %s is %d years old, and we want %s's age." % (first, second, a, b, second, n, first),
            "Here are two ages in the ratio %d to %d. We know %s is %d. Let us find how old %s is." % (a, b, second, n, first),
            "%s and %s have ages in the ratio %d to %d. %s is %d years old. How old is %s? Let us see." % (first, second, a, b, second, n, first),
        ]), G("q1", q1), G("q2", "%s is %d years old. %s = ?" % (second, n, first))),
        beat("A ratio keeps its order. %s is named first and %s second. So which number of the ratio belongs to %s?" % (first, second, second),
             ask=choose(qid, "order", str(b), [str(a)],
                        "Match the names with the numbers, in order. %s comes second, so %s gets the second number, %d." % (second, second, b))),
        beat("So %s's age is %d equal parts, and %s's age is %d of the same parts. Look at the two bars." % (first, a, second, b),
             U("q1", str(a), nth_at(q1, str(a), len("%s : %s = " % (first, second)))),
             F(fig)),
        beat("%s's %d parts make %d years. How do we find the size of one part?" % (second, b, n),
             ask=choose(qid, "part", "%d ÷ %d" % (n, b), ["%d ÷ %d" % (n, a), "%d − %d" % (n, b)],
                        "The %d years are %s's, and %s has %d parts. So we share %d into %d equal parts." % (n, second, second, b, n, b))),
        beat(pick(qid, "part-say", [
            "%d divided by %d is %d. So one part is %d years." % (n, b, p, p),
            "Share %d into %d equal parts and each part is %d. One part is %d years." % (n, b, p, p),
        ]), W("w1", "%d ÷ %d = %d" % (n, b, p)), N("w1", str(p), "one part", "below", ("%d ÷ %d = %d" % (n, b, p)).count(str(p)))),
        beat("%s has %d parts, so we take %d lots of %d. %d times %d is %d. So %s is %d years old." % (first, a, a, p, a, p, r, first, r),
             W("w2", "%d × %d = %d" % (a, p, r)),
             A("ans", "%s is %d years old" % (first, r)), C("ans", str(r))),
    ]
    if p > 1:
        beats.append(beat("Let us check. Divide both ages by %d. %d gives %d, and %d gives %d. That is our ratio, %d to %d." % (p, r, a, n, b, a, b),
                          W("c1", "%d ÷ %d = %d" % (r, p, a)), W("c2", "%d ÷ %d = %d" % (n, p, b))))
    else:
        beats.append(beat("Let us check. The ages are %d and %d, which is exactly %d to %d. It fits." % (r, n, a, b),
                          Lb("c1", "%d : %d" % (r, n))))
    beats.append(beat(pick(qid, "sum", [
        "So the plan is: use the age you know to find one part, then multiply by the parts you need.",
        "Remember the two moves. Divide to find one part. Then multiply to get the age you want.",
        "One part first, then the parts you need. That works for every ratio like this one.",
    ])))
    return lesson(*beats, origin="rule")


def share(q, total, a, b, want, owner=None, things=None):
    qid = q["id"]
    s = a + b
    assert total % s == 0 and a != b
    one = total // s
    k = (min if want == "smaller" else max)(a, b)
    other = a + b - k
    res = k * one
    rest = other * one
    what = "group" if things else "share"
    unit = (" " + things) if things else ""
    if things:
        g1 = G("q1", "%s shares %d %s in the ratio %d : %d" % (owner, total, things, a, b))
        g2 = G("q2", "The %s group = ?" % want)
        opening = pick(qid, "open", [
            "%s has %d %s and splits them into two groups, in the ratio %d to %d. We want the %s group." % (owner, total, things, a, b, want),
            "%d %s, two groups, in the ratio %d to %d. Let us find how many are in the %s group." % (total, things, a, b, want),
        ])
    else:
        g1 = G("q1", "Divide %d in the ratio %d : %d" % (total, a, b))
        g2 = G("q2", "The %s share = ?" % want)
        opening = pick(qid, "open", [
            "We have to divide %d in the ratio %d to %d, and find the %s share." % (total, a, b, want),
            "%d is cut into two shares, in the ratio %d to %d. We want the %s one." % (total, a, b, want),
        ])
    brace = "%d%s" % (total, unit)
    if s <= 12:
        fig = bars(bar(None, segs(a, "a") + segs(b, "b"), brace=brace))
    else:
        fig = bars(bar(None, [seg(parts(a), a, "a"), seg(parts(b), b, "b")], brace=brace))
    third = "%d − %d = %d" % (max(a, b), min(a, b), abs(a - b))
    l1 = "%d + %d = %d" % (a, b, s)
    l2 = "%d ÷ %d = %d" % (total, s, one)
    l3 = "%d × %d = %d" % (k, one, res)
    beats = [
        beat(opening, g1, g2),
        beat("A ratio of %d to %d means the whole lot is cut into equal parts. One %s gets %s and the other gets %d." % (a, b, what, parts(a), b),
             F(fig)),
        beat("So first, how many equal parts are there altogether?",
             ask=choose(qid, "parts", l1, ["%d × %d = %d" % (a, b, a * b), third],
                        "One %s has %s and the other has %d. Put them together, so add: %d plus %d." % (what, parts(a), b, a, b))),
        beat("%d plus %d is %d. There are %d equal parts." % (a, b, s, s), W("w1", l1), N("w1", str(s), "parts in all", "below", l1.count(str(s)))),
        beat(pick(qid, "one", [
            "Now share %d into %d equal parts. %d divided by %d is %d. So one part is %d." % (total, s, total, s, one, one),
            "Next, the size of one part. %d divided by %d is %d. Each part is %d." % (total, s, one, one),
        ]), W("w2", l2), N("w2", str(one), "one part", "below", l2.count(str(one)))),
        beat("Careful now, this is where slips happen. We want the %s %s. How many parts does it have?" % (want, what),
             ask=choose(qid, "which", parts(k), [parts(other), parts(s)],
                        "The %s %s goes with the %s number of the ratio. Of %d and %d, that is %d." % (want, what, want, a, b, k))),
        beat(("%s of %d each. %d times %d is %d. So the %s %s is %d%s." % (parts(k), one, k, one, res, want, what, res, unit)) if k > 1 else
             ("Just 1 part, and one part is %d. So the %s %s is %d%s." % (one, want, what, res, unit)),
             W("w3", l3), A("ans", "The %s %s = %d%s" % (want, what, res, unit)), C("ans", str(res))),
        beat("Let us check. The other %s is %s, which is %d. And %d plus %d is %d. Nothing is lost." % (what, parts(other), rest, min(res, rest), max(res, rest), total),
             W("c1", "%d × %d = %d" % (other, one, rest)), W("c2", "%d + %d = %d" % (min(res, rest), max(res, rest), total))),
        beat(pick(qid, "sum", [
            "So for sharing in a ratio: add to count the parts, divide to find one part, then multiply for the %s you want." % what,
            "Three small steps every time. Count the parts. Find one part. Multiply by the parts you need.",
        ])),
    ]
    return lesson(*beats, origin="rule")


def equal(q, m):
    qid = q["id"]
    a, b, c = (int(v) for v in m.groups())
    assert c % a == 0 and c // a > 1
    k = c // a
    x = b * k
    q1 = "%d : %d = %d : x" % (a, b, c)
    pos_b = len("%d : " % a)
    pos_c = len("%d : %d = " % (a, b))
    l1 = "%d × %d = %d" % (a, k, c)
    l2 = "%d × %d = %d" % (b, k, x)
    beats = [
        beat(pick(qid, "open", [
            "Two ratios are equal here. %d to %d is the same as %d to x. Our job is to find x." % (a, b, c),
            "Here %d to %d equals %d to x. One number is hiding behind the x. Let us find it." % (a, b, c),
        ]), G("q1", q1)),
        beat("Equal ratios are made by multiplying both numbers by the same number. So look at the two first numbers, %d and %d." % (a, c),
             U("q1", str(a), nth_at(q1, str(a), 0)), U("q1", str(c), nth_at(q1, str(c), pos_c))),
        beat("What was %d multiplied by to become %d?" % (a, c),
             ask=choose(qid, "mult", "× %d" % k, ["+ %d" % (c - a), "× %d" % (k + 1)],
                        "Say the %d times table until you reach %d. %d times %d is %d." % (a, c, a, k, c))),
        beat("%d times %d is %d. So the multiplier is %d." % (a, k, c, k), W("w1", l1), C("w1", "× %d" % k)),
        beat("Careful here. We do not add anything. The second number, %d, must be multiplied by the very same %d." % (b, k),
             N("q1", str(b), "× %d" % k, "below", nth_at(q1, str(b), pos_b))),
        beat("%d times %d is %d. So x is %d." % (b, k, x, x),
             W("w2", l2), AM("ans", "x = %d" % x), C("ans", "x = %d" % x)),
        beat("Let us check. %d to %d became %d to %d. Both numbers were multiplied by %d, so the two ratios are equal." % (a, b, c, x, k),
             Lb("c1", "%d : %d = %d : %d" % (a, b, c, x))),
        beat(pick(qid, "sum", [
            "So with equal ratios, find the multiplier from the pair you know, then use it on the other pair.",
            "Remember: whatever one number is multiplied by, its partner is multiplied by the same.",
        ])),
    ]
    return lesson(*beats, origin="rule", check={"variable": "x", "value": str(x)})


def by_rule(q):
    """The lesson for a generated question, or None if its wording is not one of the families."""
    text = q["questionText"].strip()
    m = AGES.match(text)
    if m:
        return ages(q, m)
    m = DIVIDE.match(text)
    if m:
        return share(q, int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4))
    m = GROUPS.match(text)
    if m:
        return share(q, int(m.group(2)), int(m.group(4)), int(m.group(5)), m.group(6), owner=m.group(1), things=m.group(3))
    m = EQUAL.match(text)
    if m:
        return equal(q, m)
    return None
