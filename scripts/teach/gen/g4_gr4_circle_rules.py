"""Rule-made lessons for the generated family in Grade 4 circles.

One wording, two cases: "A circle has a radius of R cm. What is its area / circumference?
(Use π = 22/7)". Every line on the board is computed from the radius.
"""
import re

from g4_gr4_quads_lib import A, B, FIG, G, L, W, ask, figures, hpick, lesson, mark, note, ring, strike

FIGS = figures("gr4_circle")
FAMILY = re.compile(r"^A circle has a radius of (\d+) cm\. What is its (area|circumference)\? \(Use π = 22/7\)$")


def fig_ops(qid, step=None):
    entry = FIGS.get(qid) or {}
    if step is None:
        spec = entry.get("figure")
    else:
        steps = entry.get("stepFigures") or []
        spec = steps[step] if step < len(steps) else None
    return [FIG("f", spec)] if spec else []


def circumference(q, r):
    qid = q["id"]
    k = r // 7
    c = 44 * k
    d = 2 * r
    line = "2 × 22/7 × %d" % r
    beats = [
        B(hpick(qid, "open", [
            "Here is a circle with a radius of %d centimetres. We want its circumference, using 22 over 7 for pi.",
            "This circle has a radius of %d centimetres. Our job is to find its circumference. For pi we use 22 over 7.",
        ]) % r, G("Circle: radius %d cm. Circumference = ? (π = 22/7)" % r), *fig_ops(qid)),
        B(hpick(qid, "what", [
            "The circumference is the distance all the way round the circle. It is like a perimeter, but for a round shape.",
            "Circumference means the distance right round the edge of the circle. Think of an ant walking once round the rim.",
        ]), L("f0", "Circumference = 2 × π × radius"), mark("f0", "2", "circle")),
        B("The rule is 2 times pi times the radius. Which sum is that for our circle?",
          ask=ask(qid + "how", line, ["22/7 × %d" % r, "22/7 × %d × %d" % (r, r)],
                  "For going round the circle we need the 2 as well. Circumference is 2 times pi times the radius, and the radius goes in just once.")),
        B(("Here's a trick to keep the numbers small. The 7 underneath and the radius 7 cancel each other. 7 divided by 7 is 1." if r == 7 else
           hpick(qid, "trick", [
               "Here's a trick to keep the numbers small. Divide the %d by the 7 first. %d divided by 7 is %d.",
               "Before we multiply, let's make it easy. The 7 underneath divides into %d. %d divided by 7 is %d.",
           ]) % (r, r, k)), W("l1", line), strike("l1", "7"), note("l1", str(r), str(k), "below", line.count(str(r)) if line.count(str(r)) > 1 else None),
            W("l2", "%d ÷ 7 = %d" % (r, k))),
    ]
    if k == 1:
        beats.append(B("Now it is just 2 times 22 times 1. 2 times 22 is 44, and 44 times 1 is still 44.",
                       W("l3", "2 × 22 × 1 = 44")))
    else:
        beats.append(B("Now it is just 2 times 22 times %d. First, 2 times 22 is 44." % k, W("l3", "2 × 22 = 44")))
        beats.append(B("Then 44 times %d is %d." % (k, c), W("l4", "44 × %d = %d" % (k, c))))
    beats += [
        B(hpick(qid, "ans", [
            "So the circumference is %d centimetres.",
            "There it is: the circumference is %d centimetres.",
        ]) % c, A("a", "Circumference = %d cm" % c, label=True), ring("a", str(c)), *fig_ops(qid, 3)),
        B("Does that look sensible? The circle is %d centimetres across. Going round is a bit more than 3 times that. 3 times %d is %d, so %d fits." % (d, d, 3 * d, c),
          W("c1", "2 × %d = %d" % (r, d)), W("c2", "3 × %d = %d" % (d, 3 * d))),
        B(hpick(qid, "sum", [
            "So for a circumference: 2 times pi times the radius. And divide by the 7 first to keep the sum small.",
            "Remember the plan: 2 times pi times the radius. Don't leave out the 2, and let the 7 divide first.",
        ])),
    ]
    return lesson(beats, "rule")


def area(q, r):
    qid = q["id"]
    k = r // 7
    x = 22 * k
    total = x * r
    line = "22/7 × %d × %d" % (r, r)
    if r < 10:
        # 22 × 7: split the 22.
        p1, p2 = "20 × %d" % r, "2 × %d" % r
        v1, v2 = 20 * r, 2 * r
        split_line = "%d × %d = %s + %s" % (x, r, p1, p2)
        split_say = "Now %d times %d. Split %d into 20 and 2." % (x, r, x)
        w1, w2 = "20 times %d" % r, "2 times %d" % r
    else:
        tens, ones = r - r % 10, r % 10
        p1, p2 = "%d × %d" % (x, tens), "%d × %d" % (x, ones)
        v1, v2 = x * tens, x * ones
        split_line = "%d × %d = %s + %s" % (x, r, p1, p2)
        split_say = "Now %d times %d. Split %d into %d and %d." % (x, r, r, tens, ones)
        w1, w2 = "%d times %d" % (x, tens), "%d times %d" % (x, ones)
    slips = [str(total + 10), str(total - 100)]
    sq = r * r
    beats = [
        B(hpick(qid, "open", [
            "Here is a circle with a radius of %d centimetres. We want its area, using 22 over 7 for pi.",
            "This circle has a radius of %d centimetres. Our job is to find its area. For pi we use 22 over 7.",
        ]) % r, G("Circle: radius %d cm. Area = ? (π = 22/7)" % r), *fig_ops(qid)),
        B("The area is the space inside the circle. The rule is pi times the radius times the radius.",
          L("f0", "Area = π × radius × radius")),
        B("Which sum is that for our circle?",
          ask=ask(qid + "how", line, ["2 × 22/7 × %d" % r, "22/7 × %d" % r],
                  "The 2 belongs to the circumference, the distance round. For the space inside, the radius is used twice: pi times %d times %d." % (r, r))),
        B("Careful: the radius goes in twice, and there is no 2 in this rule. Now let the 7 divide first. %d divided by 7 is %d." % (r, k),
          W("l1", line), strike("l1", "7"), W("l2", "%d ÷ 7 = %d" % (r, k))),
        B(("So we have 22 times %d times %d. 22 times %d is %d." % (k, r, k, x)) if k > 1 else
          ("So we have 22 times 1 times %d. 22 times 1 is just 22." % r),
          W("l3", "22 × %d = %d" % (k, x))),
        B(split_say, W("m1", split_line)),
        B("%s is %d. %s is %d. What do the two parts make together?" % (w1, v1, w2, v2),
          W("m2", "%s = %d" % (p1, v1)), W("m3", "%s = %d" % (p2, v2)),
          ask=ask(qid + "add", str(total), slips, "Take it slowly, one place at a time. Let's write it down together.")),
        B("%d plus %d makes %d." % (v1, v2, total), W("m4", "%d + %d = %d" % (v1, v2, total))),
        B(hpick(qid, "ans", [
            "So the area is %d square centimetres. Square centimetres, because area measures the space inside.",
            "There it is: the area is %d square centimetres. We say square centimetres because it is an area.",
        ]) % total, A("a", "Area = %d cm²" % total, label=True), ring("a", str(total)), *fig_ops(qid, 3)),
        B("Does that look sensible? %d times %d is %d. A circle's area is a bit more than 3 times that. 3 times %d is %d, so %d fits." % (r, r, sq, sq, 3 * sq, total),
          W("c1", "%d × %d = %d" % (r, r, sq)), W("c2", "3 × %d = %d" % (sq, 3 * sq))),
        B(hpick(qid, "sum", [
            "So for the area of a circle: pi times radius times radius. No 2 in it, and the answer is in square units.",
            "Remember: area is pi times radius times radius. The rule with the 2 in it is for the circumference.",
        ])),
    ]
    return lesson(beats, "rule")


def family(q):
    m = FAMILY.match(q["questionText"].strip())
    if not m:
        return None
    r = int(m.group(1))
    if r % 7:
        return None
    return area(q, r) if m.group(2) == "area" else circumference(q, r)


RULES = [family]
