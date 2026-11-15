"""Rules for the generated families of ratio-word-problems (one rule per wording).

Each rule takes a question, reads its numbers from the wording, computes every
line, and returns a lesson, or None if the wording is not its own.
"""
import re

from ratio_word_problems_lib import (A, AM, Bx, C, F, G, N, U, W, arc, bar, bars, beat,
                                     choose, lesson, nth_at, pick, seg)


def keyed(q):
    idx = "ABCD".find(q.get("correctAnswer", ""))
    o = q["options"][idx]
    return (o.get("text", "") if isinstance(o, dict) else str(o)).strip()


# ── Sharing a total in a ratio ───────────────────────────────────────────────

SHARE = re.compile(r"^(\w+) has (\d+) (\w+) and divides them in the ratio (\d+):(\d+)\. "
                   r"How many \w+ are in the larger group\?$")
DIVIDE = re.compile(r"^Divide (\d+) in the ratio (\d+):(\d+)\. What is the smaller share\?$")


def share(q):
    qid, text = q["id"], q["questionText"].strip()
    m = SHARE.match(text)
    if m:
        name, items = m.group(1), m.group(3)
        total, a, b = int(m.group(2)), int(m.group(4)), int(m.group(5))
        want_larger = True
    else:
        m = DIVIDE.match(text)
        if not m:
            return None
        name, items = None, None
        total, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        want_larger = False
    assert a < b and total % (a + b) == 0, qid
    parts = a + b
    one = total // parts
    small, large = a * one, b * one
    answer = large if want_larger else small
    assert keyed(q) == str(answer), qid

    things = (" " + items) if items else ""
    if want_larger:
        given = "%d %s in the ratio %d : %d. Larger group = ?" % (total, items, a, b)
        names = ("smaller group", "larger group")
        wanted, wanted_parts = "larger group", b
        opening = pick(qid, "open", [
            "%s has %d %s and shares them into two groups, in the ratio %d is to %d. We want to know how many are in the larger group." % (name, total, items, a, b),
            "Here is our story. %d %s, split into two groups in the ratio %d is to %d. How many %s land in the larger group?" % (total, items, a, b, items),
            "%s is sharing out %d %s in the ratio %d is to %d. Our job is to find the larger group." % (name, total, items, a, b),
        ])
    else:
        given = "Divide %d in the ratio %d : %d. Smaller share = ?" % (total, a, b)
        names = ("smaller share", "larger share")
        wanted, wanted_parts = "smaller share", a
        opening = pick(qid, "open", [
            "We have to divide %d in the ratio %d is to %d, and find the smaller share." % (total, a, b),
            "Here is the number %d. It is to be split into two shares, in the ratio %d is to %d, and we want the smaller one." % (total, a, b),
            "%d is being shared out in the ratio %d is to %d. We are after the smaller share." % (total, a, b),
        ])
    assert len(given) <= 60, qid

    def picture(labelled):
        lab = str(one) if labelled else None
        return bars(bar(names[0], [seg(lab, 1, "a") for _ in range(a)]),
                    bar(names[1], [seg(lab, 1, "b") for _ in range(b)]),
                    note=("Each piece is worth %d" % one) if labelled else "Every piece is the same size")

    a_parts = "1 equal part" if a == 1 else "%d equal parts" % a
    beats = [
        beat(opening, G("q", given)),
        beat(pick(qid, "know", [
            "Before any sum, let's be sure what we know. The total is %d. The ratio is %d is to %d. And we want the %s only." % (total, a, b, wanted),
            "First, what are we given? A total of %d, and a ratio, %d is to %d. And what are we asked for? Just the %s." % (total, a, b, wanted),
            "Let's read it like detectives. There is %d to share. The ratio is %d is to %d. And the question only wants the %s." % (total, a, b, wanted),
        ]), U("q", str(total)), Bx("q", "%d : %d" % (a, b))),
        beat(pick(qid, "bars", [
            "A ratio of %d is to %d means this. One side gets %s, and the other gets %d parts of the very same size. Here they are as two bars." % (a, b, a_parts, b),
            "Let's draw the ratio. %d is to %d: one bar with %s, and one bar with %d. Every piece is the same size." % (a, b, a_parts, b),
        ]), F(picture(False))),
        beat("Count the pieces in both bars. How many equal parts are there altogether?",
             ask=choose(qid, "parts", "%d parts" % parts,
                        ["%d parts" % b, "%d parts" % (a * b), "%d parts" % (parts + 1), "%d parts" % (2 * parts)],
                        "Count every piece, in both bars. %d and %d together make %d parts." % (a, b, parts))),
        beat(pick(qid, "cut", [
            "%d plus %d is %d. So the whole %d is cut into %d equal parts." % (a, b, parts, total, parts),
            "%d and %d make %d. That means the %d is spread over %d equal parts." % (a, b, parts, total, parts),
        ]), W("w1", "%d + %d = %d" % (a, b, parts))),
        beat(pick(qid, "slip", [
            "Now for the step where slips happen. How do we find what one part is worth?",
            "Careful with this next step, it is the one that trips people up. What is one part worth?",
            "Here comes the turning point. Which sum tells us what a single part is worth?",
        ]),
             ask=choose(qid, "one", "%d ÷ %d" % (total, parts),
                        ["%d ÷ %d" % (total, b), ("%d ÷ %d" % (total, a)) if a > 1 else "%d × %d" % (total, parts)],
                        "The %d fills all %d parts, not just the %d parts of one bar. So we divide %d by %d." % (total, parts, b, total, parts))),
        beat(pick(qid, "worth", [
            "%d divided by %d is %d. So every single part is worth %d%s." % (total, parts, one, one, things),
            "%d divided by %d is %d. Now we can write %d on every piece of both bars." % (total, parts, one, one),
        ]), W("w2", "%d ÷ %d = %d" % (total, parts, one)), F(picture(True))),
        beat(pick(qid, "take", [
            "The %s has %d of these parts. %d times %d is %d." % (wanted, wanted_parts, wanted_parts, one, answer),
            "We want the %s, and that is %d parts. %d times %d makes %d." % (wanted, wanted_parts, wanted_parts, one, answer),
        ]), W("w3", "%d × %d = %d" % (wanted_parts, one, answer))),
    ]
    if want_larger:
        final = "Larger group = %d %s" % (answer, items)
        beats.append(beat(pick(qid, "done", [
            "So the larger group has %d %s. There it is!" % (answer, items),
            "So %d %s are in the larger group." % (answer, items),
        ]), A("ans", final), C("ans", "%d %s" % (answer, items))))
        if a == 1:
            beats.append(beat("Let's check. The smaller group is just 1 part, which is %d. And %d plus %d is %d, the number we started with." % (one, small, large, total),
                              W("c1", "%d + %d = %d" % (small, large, total))))
        else:
            beats.append(beat("Let's check. The smaller group is %d times %d, which is %d. And %d plus %d is %d, just what we started with." % (a, one, small, small, large, total),
                              W("c1", "%d × %d = %d" % (a, one, small)), W("c2", "%d + %d = %d" % (small, large, total))))
    else:
        final = "Smaller share = %d" % answer
        beats.append(beat(pick(qid, "done", [
            "So the smaller share is %d. There it is!" % answer,
            "So %d is the smaller share." % answer,
        ]), A("ans", final), C("ans", str(answer))))
        beats.append(beat("Let's check. The larger share is %d times %d, which is %d. And %d plus %d is %d, just what we started with." % (b, one, large, small, large, total),
                          W("c1", "%d × %d = %d" % (b, one, large)), W("c2", "%d + %d = %d" % (small, large, total))))
    beats.append(beat(pick(qid, "sum", [
        "So, to share in a ratio: count the parts, find what one part is worth, then take as many parts as you need.",
        "Remember the three moves. Add the parts, divide to find one part, then multiply for the share you want.",
        "That is the whole method. Total parts first, then one part, then the share the question asks for.",
    ])))
    return lesson(*beats, origin="rule")


# ── A proportion with one term missing ───────────────────────────────────────

PROPORTION = re.compile(r"^If (\d+) : (\d+) = (\d+) : x, find x\.$")


def proportion(q):
    qid = q["id"]
    m = PROPORTION.match(q["questionText"].strip())
    if not m:
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
    assert c % a == 0 and c > a, qid
    k = c // a
    x = b * k
    assert keyed(q) == str(x), qid
    line = "%d : %d = %d : x" % (a, b, c)
    pos_b = len("%d : " % a)
    pos_c = len("%d : %d = " % (a, b))
    ta = {"text": str(a)}
    tb = {"text": str(b)}
    tc = {"text": str(c)}
    for t, pos in ((tb, pos_b), (tc, pos_c)):
        n = nth_at(line, t["text"], pos)
        if n > 1:
            t["nth"] = n
    times = "× %d" % k
    added = c - a

    beats = [
        beat(pick(qid, "open", [
            "Here is a proportion. %d is to %d, equals %d is to x. Two ratios that are equal, with one number, x, in hiding." % (a, b, c),
            "Read it with me: %d is to %d, equals %d is to x. It says the two ratios are the same, and it hides one number behind x." % (a, b, c),
            "This says %d is to %d, equals %d is to x. So the second ratio is the first one in disguise, and x is its missing number." % (a, b, c),
        ]), G("q", line)),
        beat(pick(qid, "have", [
            "What do we have? A complete ratio, %d is to %d. The second ratio shows only its first number, %d. We must find its partner." % (a, b, c),
            "Before any sum, look at what is given. The first ratio is whole: %d is to %d. The second has its first number, %d, and a gap where x sits." % (a, b, c),
        ]), U("q", "%d : %d" % (a, b)), Bx("q", "x")),
        beat("Compare the two first numbers, %d and %d. What happened to %d to turn it into %d?" % (a, c, a, c),
             ask=choose(qid, "k", "it was multiplied by %d" % k,
                        ["%d was added to it" % added, "it was multiplied by %d" % c],
                        "Ratios grow by multiplying, not by adding. %d times %d gives %d, so it was multiplied by %d." % (a, k, c, k))),
        beat("%d divided by %d is %d. So the first number was multiplied by %d." % (c, a, k, k),
             W("w1", "%d ÷ %d = %d" % (c, a, k)), arc("q", ta, [tc]),
             {"op": "note", "line": "q", "target": ta, "text": times, "place": "above"}),
        beat("For the two ratios to stay equal, what must we do to the second number, %d?" % b,
             ask=choose(qid, "same", "multiply it by %d" % k,
                        ["add %d to it" % added, "divide it by %d" % k],
                        "Whatever was done to the first number must be done to the second. %d was multiplied by %d, so %d is multiplied by %d as well." % (a, k, b, k))),
        beat(pick(qid, "do", [
            "%d times %d is %d. Careful: we multiply here. Adding would break the ratio." % (b, k, x),
            "So %d times %d, which is %d. Notice we multiply, we never add, to keep a ratio the same." % (b, k, x),
        ]), W("w2", "%d × %d = %d" % (b, k, x)), arc("q", tb, [{"text": "x"}]),
            {"op": "note", "line": "q", "target": tb, "text": times, "place": "below"}),
        beat(pick(qid, "done", [
            "So x is %d. There is our missing number!" % x,
            "That makes x equal to %d." % x,
        ]), AM("ans", "x = %d" % x), C("ans", "x = %d" % x)),
        beat(pick(qid, "check", [
            "Let's check. Divide %d and %d by %d, and we get %d and %d again. The two ratios match." % (c, x, k, a, b),
            "Now check it. Shrink %d is to %d by dividing both by %d. Out comes %d is to %d, the ratio we began with." % (c, x, k, a, b),
        ]), W("c1", "%d ÷ %d = %d" % (c, k, a)), W("c2", "%d ÷ %d = %d" % (x, k, b))),
        beat(pick(qid, "sum", [
            "So in a proportion, find what the first number was multiplied by, then do the very same to the second.",
            "That is the trick for any proportion. Spot the multiplier between the first numbers, and use it on the second numbers.",
        ])),
    ]
    return lesson(*beats, origin="rule", check={"variable": "x", "value": str(x)})


# ── Two ages in a ratio, one age known ───────────────────────────────────────

AGE_RATIO = re.compile(r"^The ages of (\w+) and (\w+) are in the ratio (\d+):(\d+)\. "
                       r"If (\w+) is (\d+) years old, how old is (\w+)\?$")


def age_ratio(q):
    qid = q["id"]
    m = AGE_RATIO.match(q["questionText"].strip())
    if not m:
        return None
    n1, n2 = m.group(1), m.group(2)
    a, b, known = int(m.group(3)), int(m.group(4)), int(m.group(6))
    assert m.group(5) == n2 and m.group(7) == n1 and known % b == 0 and a != b, qid
    one = known // b
    age = a * one
    assert keyed(q) == str(age), qid
    q1 = "%s : %s = %d : %d" % (n1, n2, a, b)
    q2 = "%s is %d years old. %s = ?" % (n2, known, n1)
    assert len(q1) <= 60 and len(q2) <= 60, qid
    pos_a = len("%s : %s = " % (n1, n2))
    pos_b = pos_a + len("%d : " % a)
    na, nb = nth_at(q1, str(a), pos_a), nth_at(q1, str(b), pos_b)

    def picture(labelled):
        lab = str(one) if labelled else None
        return bars(bar(n1, [seg(lab, 1, "a") for _ in range(a)], brace="?"),
                    bar(n2, [seg(lab, 1, "b") for _ in range(b)], brace="%d years" % known),
                    note=("Each piece is %d years" % one) if labelled else "Every piece is the same size")

    a_parts = "1 equal part" if a == 1 else "%d equal parts" % a
    beats = [
        beat("The ages of %s and %s are in the ratio %d is to %d. %s is %d years old, and we want %s's age." % (n1, n2, a, b, n2, known, n1),
             G("q1", q1), G("q2", q2)),
        beat("Look at the order carefully. %s is named first, so %s goes with the %d. %s is second, and goes with the %d." % (n1, n1, a, n2, b),
             N("q1", str(a), n1, "below", na), N("q1", str(b), n2, "below", nb)),
        beat("As bars: %s's age is %s, and %s's is %d parts of the same size. We know %s's whole bar is %d years." % (n1, a_parts, n2, b, n2, known),
             F(picture(False))),
        beat("So how do we find what one part is worth?",
             ask=choose(qid, "one", "%d ÷ %d" % (known, b),
                        ["%d ÷ %d" % (known, a + b), ("%d ÷ %d" % (known, a)) if a > 1 else "%d × %d" % (known, b)],
                        "The %d years belong to %s alone, and %s's bar has %d parts. So we divide %d by %d." % (known, n2, n2, b, known, b))),
        beat("%d divided by %d is %d, so each part is %d years. Notice we did not add %d and %d this time, because %d is not the total of both ages." % (known, b, one, one, a, b, known),
             W("w1", "%d ÷ %d = %d" % (known, b, one)), F(picture(True))),
        beat(pick(qid, "take", [
            "%s has %d of these parts. %d times %d is %d." % (n1, a, a, one, age),
            "Now for %s, who has %d of these parts. %d times %d makes %d." % (n1, a, a, one, age),
        ]), W("w2", "%d × %d = %d" % (a, one, age))),
        beat("So %s is %d years old." % (n1, age),
             A("ans", "%s is %d years old" % (n1, age)), C("ans", "%d years" % age)),
        beat("Check. Take %d is to %d, and divide both by %d. We get %d is to %d, the ratio in the question." % (age, known, one, a, b),
             W("c1", "%d ÷ %d = %d" % (age, one, a)), W("c2", "%d ÷ %d = %d" % (known, one, b))),
        beat(pick(qid, "sum", [
            "So when you are told one person's share, divide it by that person's parts to find one part. Then multiply for the other person.",
            "Here is the plan to keep. Find one part from the age you know, then take as many parts as the other person has.",
        ])),
    ]
    return lesson(*beats, origin="rule")


# ── The sum of two ages after some years ─────────────────────────────────────

AGE_SUM = re.compile(r"^(\w+) is (\d+) years old and (\w+) is (\d+) years old\. "
                     r"What will be the sum of their ages after (\d+) years\?$")


def age_sum(q):
    qid = q["id"]
    m = AGE_SUM.match(q["questionText"].strip())
    if not m:
        return None
    n1, a1, n2, a2, n = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    f1, f2 = a1 + n, a2 + n
    total = f1 + f2
    now = a1 + a2
    assert keyed(q) == str(total), qid
    given = "%s is %d, %s is %d. Sum after %d years = ?" % (n1, a1, n2, a2, n)
    assert len(given) <= 60, qid
    grow = "+ %d" % n
    picture = bars(bar(n1, [seg(str(a1), a1 / 5.0, "a"), seg(grow, max(n / 5.0, 0.8), "c")]),
                   bar(n2, [seg(str(a2), a2 / 5.0, "b"), seg(grow, max(n / 5.0, 0.8), "c")]),
                   note="Both bars grow by the same piece")
    beats = [
        beat(pick(qid, "open", [
            "%s is %d years old and %s is %d. We want the sum of their ages after %d years." % (n1, a1, n2, a2, n),
            "Two people here: %s, who is %d, and %s, who is %d. The question asks what their ages will add up to after %d years." % (n1, a1, n2, a2, n),
        ]), G("q", given)),
        beat("Read the last part again: after %d years. So we don't add the ages they have today. We add the ages they will have then." % n,
             U("q", "after %d years" % n)),
        beat("Here is a bar for each of them. In %d years, each bar grows by a piece of %d." % (n, n), F(picture)),
        beat("Who gets older in those %d years?" % n,
             ask=choose(qid, "who", "both of them", ["only %s" % n1, "only %s" % n2],
                        "Time passes for everybody. %s gets %d years older, and so does %s." % (n1, n, n2))),
        beat("%s will be %d plus %d, which is %d. %s will be %d plus %d, which is %d." % (n1, a1, n, f1, n2, a2, n, f2),
             W("w1", "%d + %d = %d" % (a1, n, f1)), W("w2", "%d + %d = %d" % (a2, n, f2))),
        beat("Now add the two new ages. %d plus %d is %d." % (f1, f2, total),
             W("w3", "%d + %d = %d" % (f1, f2, total))),
        beat("So after %d years, their ages add up to %d." % (n, total),
             A("ans", "Sum after %d years = %d years" % (n, total)), C("ans", "= %d years" % total)),
        beat("Here is a quick check. Today they add up to %d. Two people each gain %d years, so the sum gains %d. And %d plus %d is %d." % (now, n, 2 * n, now, 2 * n, total),
             W("c1", "%d + %d = %d" % (a1, a2, now)), W("c2", "2 × %d = %d" % (n, 2 * n)), W("c3", "%d + %d = %d" % (now, 2 * n, total))),
        beat(pick(qid, "sum", [
            "So remember: when years pass, they pass for everyone. Add the %d years once for each person." % n,
            "The slip to avoid is adding the %d only once. Two people means the years are added two times." % n,
        ])),
    ]
    return lesson(*beats, origin="rule")


# ── The difference of two ages some years ago ────────────────────────────────

AGE_GAP = re.compile(r"^(\w+) is (\d+) years old and (\w+) is (\d+) years old\. "
                     r"What was the difference in their ages (\d+) years ago\?$")


def age_gap(q):
    qid = q["id"]
    m = AGE_GAP.match(q["questionText"].strip())
    if not m:
        return None
    n1, a1, n2, a2, n = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    assert a1 > a2 > n, qid
    gap = a1 - a2
    p1, p2 = a1 - n, a2 - n
    assert keyed(q) == str(gap), qid
    given = "%s is %d, %s is %d. Difference %d years ago = ?" % (n1, a1, n2, a2, n)
    assert len(given) <= 60, qid
    picture = bars(bar(n1, [seg(str(a2), 3, "a"), seg("gap ?", 1.5, "unknown")], brace="%d years" % a1),
                   bar(n2, [seg(str(a2), 3, "a")]),
                   note="The extra piece is the gap between them")
    beats = [
        beat(pick(qid, "open", [
            "%s is %d years old and %s is %d. The question asks for the difference in their ages %d years ago." % (n1, a1, n2, a2, n),
            "We have %s, who is %d, and %s, who is %d. We are asked about the difference in their ages, but %d years ago." % (n1, a1, n2, a2, n),
        ]), G("q", given)),
        beat("Difference means the gap between the two ages: how much older one of them is than the other.",
             U("q", "Difference")),
        beat("Think about this before any sum. %d years ago, was the gap between them bigger, smaller, or the same as today?" % n,
             ask=choose(qid, "gap", "the same as today", ["smaller than today", "bigger than today"],
                        "Both of them were %d years younger then. They step back together, so the gap between them does not move." % n)),
        beat("Here is a fact worth keeping: the gap between two ages never changes. Every year, both people get exactly one year older.",
             F(picture)),
        beat("So we only need the gap today. %s's bar is %s's bar plus an extra piece. %d minus %d is %d." % (n1, n2, a1, a2, gap),
             W("w1", "%d − %d = %d" % (a1, a2, gap))),
        beat("Don't just take my word for it. Go back %d years: %s was %d minus %d, that is %d. %s was %d minus %d, that is %d." % (n, n1, a1, n, p1, n2, a2, n, p2),
             W("w2", "%d − %d = %d" % (a1, n, p1)), W("w3", "%d − %d = %d" % (a2, n, p2))),
        beat("And %d minus %d is %d. The very same gap!" % (p1, p2, gap),
             W("w4", "%d − %d = %d" % (p1, p2, gap))),
        beat("So %d years ago, the difference in their ages was %d years." % (n, gap),
             A("ans", "Difference = %d years" % gap), C("ans", "%d years" % gap)),
        beat(pick(qid, "sum", [
            "The %d years was only there to tempt us into extra sums. For a difference in ages, past or future, just subtract the ages you are given." % n,
            "So whenever a question asks for the difference in two ages, in any year at all, subtract the ages you know. The gap never changes.",
        ])),
    ]
    return lesson(*beats, origin="rule")


RULES = [share, proportion, age_ratio, age_sum, age_gap]


def by_rule(q):
    for rule in RULES:
        made = rule(q)
        if made:
            return made
    return None
