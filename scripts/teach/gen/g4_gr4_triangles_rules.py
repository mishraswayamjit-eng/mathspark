"""Grade 4 triangle lessons made by rule: one function per wording of a generated family.

RULES is a list of (pattern, function). The function reads the numbers from the question,
works out every line, and picks its phrasing by a stable hash of the question id.
"""
import json
import re

from g4_gr4_triangles_lib import (ANS, B, G, QF, W, ask, has_figure, hpick, lesson, mark, tri)


def _with_answer(figop, value):
    """The same figure with its '?' corner filled in."""
    spec = json.loads(json.dumps(figop["spec"]))
    if "corners" in spec:
        spec["corners"] = [value if c == "?" else c for c in spec["corners"]]
    if "angles" in spec:
        spec["angles"] = {k: (value if v == "?" else v) for k, v in spec["angles"].items()}
    return {"op": "figure", "id": "", "spec": spec}


# ── Two angles are given; find the third ─────────────────────────────────────

def third_angle(q, m):
    qid = q["id"]
    a, b = int(m.group(1)), int(m.group(2))
    s = a + b
    t = 180 - s
    fig = QF(qid) if has_figure(qid) else tri(a="?", b="%d°" % a, c="%d°" % b)

    beats = []
    beats.append(B(
        hpick(qid, "open", [
            "Here is a triangle. 2 of its angles are %d degrees and %d degrees. We need to find the third one." % (a, b),
            "A triangle has 3 angles. We are told 2 of them: %d degrees and %d degrees. Let's hunt for the third." % (a, b),
            "This triangle is keeping a secret. We know 2 angles, %d degrees and %d degrees, and the third is hidden." % (a, b),
        ]),
        G("l1", "Two angles: %d° and %d°. Third angle = ?" % (a, b)), fig))
    beats.append(B(
        hpick(qid, "fact", [
            "Here is the fact that unlocks every triangle. Its 3 angles always add up to 180 degrees.",
            "Every triangle, big or small, keeps one rule. Its 3 angles together make exactly 180 degrees.",
            "Start with the one thing we know about every triangle. The 3 angles add up to 180 degrees, every time.",
        ]),
        W("l2", "3 angles of a triangle = 180°"), mark("l2", "180°", "box")))
    beats.append(B(
        hpick(qid, "ask1", [
            "We know 2 of the 3 angles. What should we do with them first?",
            "So 2 angles are known and 1 is missing. What is our first move?",
        ]),
        ask=ask(qid + "a1", "add them: %d + %d" % (a, b),
                ["add them to 180", "take the small one from the big one"],
                "We want to know how much of the 180 degrees is used up already. So first we add the 2 angles we know.")))

    # Adding, in two small steps when that helps.
    big, small = (a, b) if b % 10 else (b, a)
    if small % 10 == 0 or small < 10:
        beats.append(B(
            "Add the 2 angles we know. %d plus %d makes %d." % (big, small, s),
            W("l3", "%d + %d = %d" % (a, b, s)), mark("l3", "= %d" % s, "underline")))
    else:
        tens, ones = small - small % 10, small % 10
        mid = big + tens
        beats.append(B(
            hpick(qid, "add", [
                "Let's add in 2 small steps. %d plus %d is %d. Then %d more makes %d." % (big, tens, mid, ones, s),
                "Add the tens first. %d plus %d is %d. Now the %d that is left: that makes %d." % (big, tens, mid, ones, s),
            ]),
            W("l3a", "%d + %d = %d" % (big, tens, mid)), W("l3b", "%d + %d = %d" % (mid, ones, s)),
            W("l3", "%d + %d = %d" % (a, b, s)), mark("l3", "= %d" % s, "underline")))

    beats.append(B(
        hpick(qid, "ask2", [
            "So %d degrees are used up by the 2 angles we know. How do we find the third angle?" % s,
            "The 2 known angles take %d degrees out of the 180. What is left for the third angle?" % s,
        ]),
        ask=ask(qid + "a2", "180 − %d" % s, ["180 + %d" % s, "it is %d" % s],
                "The 3 angles share 180 degrees between them. So the third angle is what is left when we take %d away from 180." % s)))

    if s % 10 == 0:
        beats.append(B(
            "Take %d away from 180. That leaves %d. So the third angle is %d degrees." % (s, t, t),
            W("l4", "180 − %d = %d" % (s, t)), ANS("l5", "Third angle = %d°" % t, "%d°" % t)))
    else:
        tens, ones = s - s % 10, s % 10
        mid = 180 - tens
        beats.append(B(
            hpick(qid, "sub", [
                "Take %d away from 180 in 2 small steps. First take away %d: that leaves %d. Then take away %d more: %d." % (s, tens, mid, ones, t),
                "180 minus %d. Take off %d first, which leaves %d. Then take off the last %d, and we land on %d." % (s, tens, mid, ones, t),
            ]),
            W("l4a", "180 − %d = %d" % (tens, mid)), W("l4b", "%d − %d = %d" % (mid, ones, t)),
            W("l4", "180 − %d = %d" % (s, t))))
        beats.append(B(
            hpick(qid, "found", [
                "So the third angle is %d degrees. There it is!" % t,
                "The hidden angle is %d degrees." % t,
                "So the third angle is %d degrees. Found it!" % t,
            ]),
            ANS("l5", "Third angle = %d°" % t, "%d°" % t)))

    if t > 90:
        extra = " And notice: %d degrees is a wide angle, an obtuse one. A triangle can have just 1 of those." % t
    elif t == 90:
        extra = " And notice: the third angle is a right angle, a square corner."
    else:
        extra = ""
    beats.append(B(
        "Good mathematicians check. Add all 3 angles: %d, %d and %d. They make 180, just as they should.%s" % (a, b, t, extra),
        W("l6", "%d + %d + %d = 180" % (a, b, t)), _with_answer(fig, "%d°" % t)))
    beats.append(B(
        hpick(qid, "close", [
            "So for a missing angle in a triangle: add the 2 angles you know, then take the total away from 180.",
            "Remember the plan: add the 2 angles you have, and take that from 180. What is left is the third angle.",
            "That is the whole method. Add what you know, then find how far it is from 180.",
        ])))
    return lesson(beats, "rule")


# ── Angles in a ratio; find the largest ──────────────────────────────────────

def _parts(n):
    return "1 part" if n == 1 else "%d parts" % n


def ratio_largest(q, m):
    qid = q["id"]
    r = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
    total = sum(r)
    one = 180 // total
    if one * total != 180:
        raise ValueError("%s: 180 is not shared exactly" % qid)
    big = max(r)
    largest = big * one
    angles = [x * one for x in r]
    twice = r.count(big) > 1
    ratio = "%d : %d : %d" % tuple(r)
    fig = QF(qid) if has_figure(qid) else tri(a=_parts(r[0]), b=_parts(r[1]), c=_parts(r[2]))

    beats = []
    beats.append(B(
        "The angles of this triangle are in the ratio %d to %d to %d. We want the largest angle." % tuple(r),
        G("l1", "Angles in the ratio %s. Largest angle = ?" % ratio), fig))
    beats.append(B(
        hpick(qid, "parts", [
            "A ratio is a way of sharing. Think of equal parts: the first angle gets %s, the second gets %s, and the third gets %s." % (_parts(r[0]), _parts(r[1]), _parts(r[2])),
            "Read the ratio as equal parts. One angle is %s, the next is %s, and the last is %s. Every part is the same size." % (_parts(r[0]), _parts(r[1]), _parts(r[2])),
        ]),
        W("l2", "%s, %s, %s" % (_parts(r[0]), _parts(r[1]), _parts(r[2])))))
    beats.append(B(
        "How many equal parts are there altogether?",
        ask=ask(qid + "a1", "%d parts" % total, ["3 parts, one for each angle", "%d parts" % (total + big)],
                "Count every part of every angle. Add the 3 ratio numbers: %d, %d and %d." % tuple(r))))
    beats.append(B(
        "%d plus %d plus %d makes %d. So there are %d equal parts in all." % (r[0], r[1], r[2], total, total),
        W("l3", "%d + %d + %d = %d" % (r[0], r[1], r[2], total))))
    beats.append(B(
        hpick(qid, "fact", [
            "Now the fact about every triangle: its 3 angles add up to 180 degrees. So these %d parts share 180 degrees." % total,
            "The 3 angles of any triangle make 180 degrees together. So all %d parts together are 180 degrees." % total,
        ]),
        W("l4", "All %d parts together = 180°" % total)))
    beats.append(B(
        "So how big is 1 part?",
        ask=ask(qid + "a2", "180 ÷ %d" % total, ["180 × %d" % total, "180 − %d" % total],
                "Sharing equally means dividing. 180 degrees shared among %d equal parts is 180 divided by %d." % (total, total))))
    beats.append(B(
        "180 divided by %d is %d. Multiply back to be sure: %d times %d is 180. So 1 part is %d degrees." % (total, one, total, one, one),
        W("l5", "180 ÷ %d = %d" % (total, one)), W("l6", "%d × %d = 180" % (total, one))))
    if twice:
        say = ("Careful: %d degrees is only 1 part, not the answer. The most parts any angle has is %d, and 2 angles have that many. "
               "%d times %d is %d.") % (one, big, big, one, largest)
    else:
        say = ("Careful: %d degrees is only 1 part, not the answer. The largest angle has the most parts, %d of them. "
               "%d times %d is %d.") % (one, big, big, one, largest)
    beats.append(B(say, mark("l1", str(big), "circle"), W("l7", "%d × %d = %d" % (big, one, largest))))
    beats.append(B(
        "So the largest angle is %d degrees." % largest,
        ANS("l8", "Largest angle = %d°" % largest, "%d°" % largest)))
    spec = json.loads(json.dumps(fig["spec"]))
    if "corners" in spec:
        spec["corners"] = ["%d°" % x for x in angles]
    else:
        spec["angles"] = {"a": "%d°" % angles[0], "b": "%d°" % angles[1], "c": "%d°" % angles[2]}
    beats.append(B(
        "Let's check with all 3 angles: %d, %d and %d. Together they make 180. It works." % tuple(angles),
        W("l9", "%d + %d + %d = 180" % tuple(angles)), {"op": "figure", "id": "", "spec": spec}))
    beats.append(B(
        "So with a ratio: add the parts, divide 180 by that to get 1 part, then multiply by the parts you need."))
    return lesson(beats, "rule")


# ── Area of a triangle from base and height ──────────────────────────────────

def area_base_height(q, m):
    qid = q["id"]
    b, h = int(m.group(1)), int(m.group(2))
    rect = b * h
    if rect % 2:
        raise ValueError("%s: half is not whole" % qid)
    area = rect // 2
    beats = [
        B("Here is a triangle. Its base is %d centimetres and its height is %d centimetres. We want its area, the space inside it." % (b, h),
          G("l1", "Triangle: base %d cm, height %d cm. Area = ?" % (b, h)),
          tri(bc="%d cm" % b, height="%d cm" % h)),
        B("Picture a rectangle drawn round the triangle, with the same base and the same height. The triangle fills exactly half of that rectangle.",
          tri(bc="%d cm" % b, height="%d cm" % h, enclose=True, note="The triangle is half of the rectangle")),
        B("So let's find the rectangle first. Which sum gives the area of the whole rectangle?",
          ask=ask(qid + "a1", "%d × %d" % (b, h), ["%d + %d" % (b, h), "%d − %d" % (max(b, h), min(b, h))],
                  "The area of a rectangle is its length times its breadth. Adding the 2 numbers does not give the space inside.")),
        B("%d times %d is %d. That is the whole rectangle." % (b, h, rect),
          W("l2", "%d × %d = %d" % (b, h, rect))),
        B("Here comes the step that is easy to forget. The triangle is only half of the rectangle. So what do we do with %d?" % rect,
          ask=ask(qid + "a2", "halve it: %d ÷ 2" % rect, ["double it: %d × 2" % rect, "keep it as %d" % rect],
                  "The triangle covers half of the rectangle, so its area is half of %d. We divide by 2." % rect)),
        B("Half of %d is %d." % (rect, area),
          W("l3", "%d ÷ 2 = %d" % (rect, area))),
        B("So the area of the triangle is %d square centimetres." % area,
          ANS("l4", "Area = %d square cm" % area, "%d" % area)),
        B("So for the area of a triangle: multiply the base by the height, then take half. Stopping at %d is the classic slip." % rect),
    ]
    return lesson(beats, "rule")


RULES = [
    (re.compile(r"^Two angles of a triangle are (\d+)° and (\d+)°\. What is the third angle\?$"), third_angle),
    (re.compile(r"^In a triangle, two angles are (\d+)° and (\d+)°\. Find the third angle\.$"), third_angle),
    (re.compile(r"^Angles of a triangle are in the ratio (\d+):(\d+):(\d+)\. Find the largest angle\.$"), ratio_largest),
    (re.compile(r"^Find the area of a triangle with base (\d+) cm and height (\d+) cm\.$"), area_base_height),
]
