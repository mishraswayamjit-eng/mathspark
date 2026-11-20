"""Rule lessons for the generated Grade 4 algebra families.

    simplify    "Simplify: 11x + 10 + 8x − 3"
    sub2        "If x = 2 and y = 4, find the value of 2x + 4y."
    sub1        "If x = 6, find the value of 5x + 10 − 8."
    two_term    "If a=6,b=7: 3a-b=?"   "If a=9,b=2: a+4b=?"   "If a=10,b=3: 2a+b=?"
    square      "If a=3,b=9: a²=?"
    product     "If a = 9 and b = 9, what is the value of ab?"

rule_for(q) returns a lesson, or None if the wording is not one of these.
"""
import re

from g4_gr4_algebra_lib import (B, L, T, W, answer, choose, given, group, last_num, lesson, mark, note, nth_at, pick,
                                shuffled, under)

MINUS = "−"
GENERATED = re.compile(r"^(?:VAR2?_|BOOST_|PH3_)|_V\d+$")


def is_generated(qid):
    return bool(GENERATED.search(qid))


# ── Simplify: ax + b + cx ± d ────────────────────────────────────────────────

_SIMPLIFY = re.compile(r"^Simplify: (\d+)x \+ (\d+) \+ (\d+)x ([+−-]) (\d+)$")


def simplify(q):
    m = _SIMPLIFY.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b, c, d = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(5))
    plus = m.group(4) == "+"
    sg = "+" if plus else MINUS
    opw = "plus" if plus else "minus"
    xs = a + c
    n = b + d if plus else b - d
    if n <= 0:
        return None

    l1 = "%dx + %d + %dx %s %d" % (a, b, c, sg, d)
    at_b = len("%dx " % a)
    at_c = len("%dx + %d + " % (a, b))
    at_d = len("%dx + %d + %dx " % (a, b, c))
    t_a = T("%dx" % a, nth_at(l1, "%dx" % a, 0))
    t_b = T("+ %d" % b, nth_at(l1, "+ %d" % b, at_b))
    t_c = T("%dx" % c, nth_at(l1, "%dx" % c, at_c))
    t_d = T("%s %d" % (sg, d), nth_at(l1, "%s %d" % (sg, d), at_d))
    said = "%d x, plus %d, plus %d x, %s %d" % (a, b, c, opw, d)

    beats = []
    beats.append(B(pick(qid, "intro", [
        "Here is a long expression. %s. Simplify means write it shorter, without changing what it is worth." % said,
        "%s. That is a lot to say! Let's tidy it up, so it says the same thing in fewer pieces." % said,
        "Look at this. %s. Four pieces, and some of them can be joined together. Let's find out which." % said,
    ]), given("l1", l1)))

    if pick(qid, "ask1", [0, 1]) == 0:
        choices, right = shuffled(qid, "c1", ["%dx and %dx" % (a, c), "%dx and %d" % (a, b), "%d and %dx" % (b, c)])
        beats.append(B(
            "Some of these pieces belong together. The ones with an x are one family. "
            "The plain numbers are another family. Which two are from the same family?",
            ask=choose(choices, right,
                       "Look for the letter. %d x and %d x both have an x, so they are one family. "
                       "%d has no x at all." % (a, c, b))))
    else:
        choices, right = shuffled(qid, "c1", ["the boxes: %dx and %dx" % (a, c), "a box and some loose sweets",
                                              "everything, all at once"])
        beats.append(B(
            "Think of x as a box with a secret number of sweets inside. %d x is %d boxes, and %d x is %d more boxes. "
            "The plain numbers are loose sweets. What can we count together?" % (a, a, c, c),
            ask=choose(choices, right,
                       "Boxes go with boxes, and loose sweets go with loose sweets. We cannot add a box "
                       "to a loose sweet, because we do not know how many are inside the box.")))

    beats.append(B(pick(qid, "xs", [
        "So first gather the x terms. %d x and %d x together make %d x." % (a, c, xs),
        "First the x family. %d lots of x and %d more lots of x make %d lots of x." % (a, c, xs),
    ]), group("l1", [t_a, t_c], "%dx" % xs), W("l2", "%dx + %dx = %dx" % (a, c, xs))))

    if plus:
        say_n = pick(qid, "nums", [
            "Now the plain numbers. %d plus %d makes %d." % (b, d, n),
            "Next, the numbers with no letter. %d and %d together make %d." % (b, d, n),
        ])
    else:
        say_n = ("Now the plain numbers. Careful: the sign in front of a number belongs to that number. "
                 "So this is %d minus %d, which is %d." % (b, d, n))
    beats.append(B(say_n, group("l1", [t_b, t_d], str(n)), W("l3", "%d %s %d = %d" % (b, sg, d, n))))

    choices, right = shuffled(qid, "c2", ["No, keep them apart", "Yes, it makes %dx" % (xs + n)])
    beats.append(B(
        "So we have %d x and %d. Here is where many people slip. Can we join those two into one piece?" % (xs, n),
        ask=choose(choices, right,
                   "%d x means %d lots of a hidden number. %d is a plain number. "
                   "They are different families, so they stay side by side." % (xs, xs, n))))

    final = "%dx + %d" % (xs, n)
    beats.append(B(pick(qid, "ans", [
        "So the short form is %d x plus %d. Same value, fewer pieces." % (xs, n),
        "That leaves %d x plus %d. It cannot get any shorter than that." % (xs, n),
    ]), answer("l4", final), mark("l4", final)))

    t = xs + n
    beats.append(B(pick(qid, "check", [
        "Let's test it. Pretend x is 1. The long one is %d plus %d plus %d %s %d, which is %d. "
        "The short one is %d plus %d, also %d. They match." % (a, b, c, opw, d, t, xs, n, t),
        "Good mathematicians check. If x were 1, the long one would be %d plus %d plus %d %s %d. That is %d. "
        "The short one is %d plus %d, and that is %d too." % (a, b, c, opw, d, t, xs, n, t),
    ]), W("l5", "%d + %d + %d %s %d = %d" % (a, b, c, sg, d, t)), W("l6", "%d + %d = %d" % (xs, n, t))))

    beats.append(B(pick(qid, "sum", [
        "So to simplify: gather the x terms, gather the plain numbers, and keep the two families apart. "
        "Our answer is %d x plus %d." % (xs, n),
        "The plan every time: x terms with x terms, numbers with numbers, and each sign stays with its own number. "
        "That gave us %d x plus %d." % (xs, n),
    ])))
    return lesson(beats, "x", n, "rule")


# ── What does 5x mean? ───────────────────────────────────────────────────────

def _meaning_ask(qid, p, letter, x):
    """The turn most substitution lessons start with: what does 5x turn into?"""
    choices, right = shuffled(qid, "c1", ["%d × %d" % (p, x), "%d + %d" % (p, x), "the number %d%d" % (p, x)])
    say = pick(qid, "ask1", [
        "First, what does %d %s turn into when %s is %d?" % (p, letter, letter, x),
        "Before we swap anything: when %s is %d, what is %d %s?" % (letter, x, p, letter),
        "Look at %d %s. The %d and the %s are side by side. When %s is %d, what does that mean?"
        % (p, letter, p, letter, letter, x),
    ])
    if_not = ("When a number sits right next to a letter, there is a hidden times sign between them. "
              "So %d %s means %d times %s. Here that is %d times %d." % (p, letter, p, letter, p, x))
    return say, choose(choices, right, if_not)


# ── If x = .. and y = .., find px + qy ───────────────────────────────────────

_SUB2 = re.compile(r"^If x = (\d+) and y = (\d+), find the value of (\d+)x \+ (\d+)y\.$")


def sub2(q):
    m = _SUB2.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    x, y, p, k = (int(g) for g in m.groups())
    px, ky = p * x, k * y
    tot = px + ky

    beats = []
    beats.append(B(pick(qid, "intro", [
        "We are told that x is %d and y is %d. We want to know what %d x plus %d y is worth." % (x, y, p, k),
        "Two letters this time. x is %d and y is %d. Our job is to find the value of %d x plus %d y." % (x, y, p, k),
        "Here x stands for %d and y stands for %d. Let's find what %d x plus %d y comes to." % (x, y, p, k),
    ]), given("l1", "x = %d, y = %d" % (x, y), label=True), given("l2", "%dx + %dy" % (p, k), label=True)))

    say, ask = _meaning_ask(qid, p, "x", x)
    beats.append(B(say, ask=ask))

    beats.append(B(pick(qid, "swap", [
        "So we swap each letter for its own number. %d x becomes %d times %d. And %d y becomes %d times %d."
        % (p, p, x, k, k, y),
        "Each letter has its own number, so be careful not to mix them up. x is %d, so %d x is %d times %d. "
        "y is %d, so %d y is %d times %d." % (x, p, p, x, y, k, k, y),
    ]), note("l2", "x", str(x)), note("l2", "y", str(y)), W("l3", "%d × %d + %d × %d" % (p, x, k, y))))

    if k == 1:
        second = "And 1 y is just one y, so that is %d." % y
    else:
        second = "And %d times %d is %d." % (k, y, ky)
    beats.append(B("We do the times first. %d times %d is %d. %s" % (p, x, px, second),
                   W("l4", "%d × %d = %d" % (p, x, px)), W("l5", "%d × %d = %d" % (k, y, ky))))

    choices, right = shuffled(qid, "c2", ["add them", "multiply them"])
    if px == ky:
        have = "Now we have two parts, and each one is %d." % px
    else:
        have = "Now we have two parts: %d and %d." % (px, ky)
    beats.append(B(
        "%s What do we do with them?" % have,
        ask=choose(choices, right,
                   "Look at the sign between %d x and %d y. It is a plus. So the two parts are added." % (p, k))))

    last = "%d + %d = %d" % (px, ky, tot)
    beats.append(B(pick(qid, "ans", [
        "%d plus %d is %d. So %d x plus %d y is worth %d." % (px, ky, tot, p, k, tot),
        "Add them up. %d plus %d makes %d. That is our answer: %d." % (px, ky, tot, tot),
    ]), answer("l6", last), mark("l6", last_num(last, tot))))

    beats.append(B(pick(qid, "sum", [
        "So the plan is: swap each letter for its number, do the times first, then add. The answer is %d." % tot,
        "Remember: a number next to a letter always means times. Multiply each part, then add the parts. "
        "That gave us %d." % tot,
    ])))
    return lesson(beats, None, None, "rule")


# ── If x = .., find px + b − c ───────────────────────────────────────────────

_SUB1 = re.compile(r"^If x = (\d+), find the value of (\d+)x \+ (\d+) − (\d+)\.$")


def sub1(q):
    m = _SUB1.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    x, p, b, c = (int(g) for g in m.groups())
    px = p * x
    s = px + b
    tot = s - c

    beats = []
    beats.append(B(pick(qid, "intro", [
        "We know that x is %d. We want the value of %d x, plus %d, minus %d." % (x, p, b, c),
        "This time the letter is no mystery: x is %d. So we can find what %d x, plus %d, minus %d is worth."
        % (x, p, b, c),
    ]), given("l1", "x = %d" % x, label=True), given("l2", "%dx + %d − %d" % (p, b, c), label=True)))

    say, ask = _meaning_ask(qid, p, "x", x)
    beats.append(B(say, ask=ask))

    beats.append(B(pick(qid, "swap", [
        "So we rub out the x and write %d in its place, with a times sign. %d times %d, plus %d, minus %d."
        % (x, p, x, b, c),
        "So the x goes, and %d takes its place. Now it reads %d times %d, plus %d, minus %d." % (x, p, x, b, c),
    ]), note("l2", "x", str(x)), W("l3", "%d × %d + %d − %d" % (p, x, b, c))))

    choices, right = shuffled(qid, "c2", ["%d × %d" % (p, x), "%d + %d" % (x, b), "any order is fine"])
    beats.append(B(
        "Three jobs here: a times, a plus and a minus. Which one goes first?",
        ask=choose(choices, right,
                   "Multiplying always goes before adding and taking away. So %d times %d comes first. "
                   "The %d must not be added to the %d." % (p, x, b, x))))

    beats.append(B(
        "%d times %d is %d. So now we have %d, plus %d, minus %d." % (p, x, px, px, b, c),
        under("l3", "%d × %d" % (p, x)), W("l4", "%d + %d − %d" % (px, b, c))))

    if b == c:
        last = "%d + %d − %d = %d" % (px, b, c, tot)
        beats.append(B(
            "Look closely: plus %d, and then minus %d. Those two undo each other. So we are left with %d."
            % (b, c, tot),
            answer("l5", last), mark("l5", last_num(last, tot))))
    else:
        last = "%d − %d = %d" % (s, c, tot)
        beats.append(B(
            "Now we go left to right. %d plus %d is %d. The sign before the %d is a minus, so we take it away. "
            "%d minus %d is %d." % (px, b, s, c, s, c, tot),
            W("l5", "%d + %d = %d" % (px, b, s)), answer("l6", last), mark("l6", last_num(last, tot))))

    beats.append(B(pick(qid, "sum", [
        "So when x is %d, the whole thing is worth %d. The plan: swap the letter for its number, "
        "multiply first, then work left to right." % (x, tot),
        "That gives %d. Remember the order: number in for the letter, then the times, "
        "then the plus and minus from left to right." % tot,
    ])))
    return lesson(beats, None, None, "rule")


# ── If a=6,b=7: 3a-b=?   a+4b=?   2a+b=? ─────────────────────────────────────

_AB = re.compile(r"^If a=(\d+),b=(\d+): (\d*)a([+-])(\d*)b=\?$")


def two_term(q):
    m = _AB.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b = int(m.group(1)), int(m.group(2))
    p = int(m.group(3) or 1)
    k = int(m.group(5) or 1)
    plus = m.group(4) == "+"
    sg = "+" if plus else MINUS
    opw = "plus" if plus else "minus"
    if (p > 1) == (k > 1):
        return None
    expr = "%sa %s %sb" % (p if p > 1 else "", sg, k if k > 1 else "")
    said = "%s %s %s" % ("%d a" % p if p > 1 else "a", opw, "%d b" % k if k > 1 else "b")

    beats = []
    beats.append(B(pick(qid, "intro", [
        "We are told that a is %d and b is %d. We want to know what %s is worth." % (a, b, said),
        "Two letters here. a stands for %d and b stands for %d. Our job is to find the value of %s." % (a, b, said),
        "Here a is %d and b is %d. Let's find what %s comes to." % (a, b, said),
    ]), given("l1", "a = %d, b = %d" % (a, b), label=True), given("l2", expr, label=True)))

    if p > 1:
        # 3a − b, 2a + b: multiply into a first, then add or take away b.
        prod = p * a
        tot = prod + b if plus else prod - b
        if tot < 0:
            return None
        say, ask = _meaning_ask(qid, p, "a", a)
        beats.append(B(say, ask=ask))
        beats.append(B(pick(qid, "swap", [
            "So swap each letter for its number. %d a becomes %d times %d, and b becomes %d." % (p, p, a, b),
            "Now put the numbers in. %d a is %d times %d. And in place of b we write %d." % (p, p, a, b),
        ]), note("l2", "a", str(a)), note("l2", "b", str(b)), W("l3", "%d × %d %s %d" % (p, a, sg, b))))

        other = "the plus: %d + %d" % (a, b) if plus else "the take away"
        choices, right = shuffled(qid, "c2", ["the times: %d × %d" % (p, a), other])
        beats.append(B(
            "Two jobs here: a times and a %s. Which one goes first?" % ("plus" if plus else "take away"),
            ask=choose(choices, right,
                       "Multiplying goes before adding and taking away. So %d times %d comes first." % (p, a))))

        beats.append(B(pick(qid, "times", [
            "%d times %d is %d." % (p, a, prod),
            "%d lots of %d make %d." % (p, a, prod),
        ]), under("l3", "%d × %d" % (p, a)), W("l4", "%d × %d = %d" % (p, a, prod))))

        last = "%d %s %d = %d" % (prod, sg, b, tot)
        if plus:
            fin = pick(qid, "fin", [
                "Now add b, which is %d. %d plus %d is %d." % (b, prod, b, tot),
                "We are not done yet: b still has to be added. %d plus %d makes %d." % (prod, b, tot),
            ])
        else:
            fin = pick(qid, "fin", [
                "Now take away b, which is %d. We take it away just once. %d minus %d is %d." % (b, prod, b, tot),
                "The sign before b is a minus, so b comes off. %d minus %d leaves %d." % (prod, b, tot),
            ])
        beats.append(B(fin, answer("l5", last), mark("l5", last_num(last, tot))))
        beats.append(B(pick(qid, "sum", [
            "So %s is worth %d. The plan: swap the letters for their numbers, do the times first, then the %s."
            % (said, tot, "adding" if plus else "taking away"),
            "That gives %d. Remember: a number next to a letter means times, and the times is done first." % tot,
        ])))
        return lesson(beats, None, None, "rule")

    # a + 4b: the times is in the second term.
    if not plus:
        return None
    prod = k * b
    tot = a + prod
    say, ask = _meaning_ask(qid, k, "b", b)
    beats.append(B(say, ask=ask))
    beats.append(B(pick(qid, "swap", [
        "So swap each letter for its number. a becomes %d, and %d b becomes %d times %d." % (a, k, k, b),
        "Now put the numbers in. In place of a we write %d. And %d b is %d times %d." % (a, k, k, b),
    ]), note("l2", "a", str(a)), note("l2", "b", str(b)), W("l3", "%d + %d × %d" % (a, k, b))))

    choices, right = shuffled(qid, "c2", ["the times: %d × %d" % (k, b), "the plus: %d + %d" % (a, k)])
    beats.append(B(
        "Careful now. The plus comes first as we read, but that does not mean it is done first. "
        "Which job do we do first?",
        ask=choose(choices, right,
                   "Multiplying goes before adding, even when the plus is written first. "
                   "The %d belongs to b, so %d times %d comes first." % (k, k, b))))

    beats.append(B(pick(qid, "times", [
        "%d times %d is %d." % (k, b, prod),
        "%d lots of %d make %d." % (k, b, prod),
    ]), under("l3", "%d × %d" % (k, b)), W("l4", "%d × %d = %d" % (k, b, prod))))

    last = "%d + %d = %d" % (a, prod, tot)
    beats.append(B(pick(qid, "fin", [
        "Now add a, which is %d. We add it just once. %d plus %d is %d." % (a, a, prod, tot),
        "Now the plus. %d plus %d makes %d." % (a, prod, tot),
    ]), answer("l5", last), mark("l5", last_num(last, tot))))
    beats.append(B(pick(qid, "sum", [
        "So %s is worth %d. The plan: swap the letters for their numbers, do the times first, then add." % (said, tot),
        "That gives %d. Remember: a number next to a letter means times, and the times is done before the plus." % tot,
    ])))
    return lesson(beats, None, None, "rule")


# ── If a=3,b=9: a²=? ─────────────────────────────────────────────────────────

_SQ = re.compile(r"^If a=(\d+),b=(\d+): a²=\?$")


def square(q):
    m = _SQ.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b = int(m.group(1)), int(m.group(2))
    sq = a * a

    beats = []
    beats.append(B(pick(qid, "intro", [
        "We are told that a is %d and b is %d. We want the value of a squared. See the small 2 sitting up high?"
        % (a, b),
        "Here a is %d and b is %d. We need a squared. That is the a with a small 2 up above it." % (a, b),
    ]), given("l1", "a = %d, b = %d" % (a, b), label=True), given("l2", "a²", label=True)))

    choices, right = shuffled(qid, "c1", ["a × a", "a × 2", "a + 2"])
    beats.append(B(
        "That small 2 has a special job. What does a squared mean?",
        ask=choose(choices, right,
                   "The small 2 is not a number to add or to multiply by. It says: use a two times over, "
                   "multiplied together. So a squared is a times a.")))

    beats.append(B(pick(qid, "mean", [
        "So a squared means a times a. The letter is multiplied by itself.",
        "a squared is a times a. It is a short way to write a number times itself.",
    ]), L("l3", "a² = a × a")))

    choices, right = shuffled(qid, "c2", ["No, there is no b in a²", "Yes, add b", "Yes, take b away"])
    beats.append(B(
        "We were also told that b is %d. Do we need b here?" % b,
        ask=choose(choices, right,
                   "Look at what we are asked for: a squared. There is no b in it at all. "
                   "So b is extra, and we leave it alone.")))

    last = "%d × %d = %d" % (a, a, sq)
    beats.append(B(pick(qid, "put", [
        "So we only swap a for %d. a times a becomes %d times %d." % (a, a, a),
        "Only a matters. Put %d in place of each a, and we get %d times %d." % (a, a, a),
    ]), note("l3", T("a", 2), str(a)), note("l3", T("a", 3), str(a))))

    beats.append(B("%d times %d is %d. So a squared is %d." % (a, a, sq, sq),
                   answer("l4", last), mark("l4", last_num(last, sq))))

    if a == 2:
        end = ("With 2 it looks the same as doubling, but that is just luck. "
               "Squared always means the number times itself. The answer is %d." % sq)
    else:
        end = pick(qid, "sum", [
            "So squared means the number times itself, never times 2. And we only use the letters that are asked for. "
            "The answer is %d." % sq,
            "Remember: a squared is a times a. And a number we are given but do not need can be left alone. "
            "That gives %d." % sq,
        ])
    beats.append(B(end))
    return lesson(beats, None, None, "rule")


# ── If a = 9 and b = 9, what is the value of ab? ─────────────────────────────

_PROD = re.compile(r"^If a = (\d+) and b = (\d+), what is the value of ab\?$")


def product(q):
    m = _PROD.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b = int(m.group(1)), int(m.group(2))
    prod, total = a * b, a + b

    beats = []
    beats.append(B(pick(qid, "intro", [
        "We are told that a is %d and b is %d. We want the value of a b. Two letters, side by side." % (a, b),
        "Here a is %d and b is %d. We need to find a b: the a and the b written right next to each other." % (a, b),
    ]), given("l1", "a = %d, b = %d" % (a, b), label=True), given("l2", "ab", label=True)))

    choices, right = shuffled(qid, "c1", ["a × b", "a + b", "a two-digit number"])
    beats.append(B(
        "There is no sign between the a and the b. So what does a b mean?",
        ask=choose(choices, right,
                   "When two letters stand side by side, there is a hidden times sign between them. "
                   "So a b means a times b.")))

    beats.append(B("So a b is a times b. I'll write the hidden times sign in.", L("l3", "ab = a × b")))

    beats.append(B(pick(qid, "put", [
        "Now swap each letter for its number. a is %d and b is %d, so we get %d times %d." % (a, b, a, b),
        "Put the numbers in place of the letters. That makes it %d times %d." % (a, b),
    ]), note("l3", T("a", 2), str(a)), note("l3", T("b", 2), str(b)), W("l4", "%d × %d" % (a, b))))

    last = "%d × %d = %d" % (a, b, prod)
    beats.append(B("%d times %d is %d. So a b is worth %d." % (a, b, prod, prod),
                   answer("l5", last), mark("l5", last_num(last, prod))))

    if prod == total:
        beats.append(B(
            "A funny thing: %d plus %d is also %d. That is just luck with these numbers. "
            "Letters side by side always mean times." % (a, b, total),
            W("l6", "%d + %d = %d" % (a, b, total))))
    else:
        beats.append(B(
            "Watch out for the classic slip: adding. %d plus %d is %d, but that is a plus b, a different thing."
            % (a, b, total),
            W("l6", "%d + %d = %d" % (a, b, total)), note("l6", last_num("%d + %d = %d" % (a, b, total), total), "a + b")))

    beats.append(B(pick(qid, "sum", [
        "So remember: letters side by side mean times. a b is a times b, and here that is %d." % prod,
        "The plan: read a b as a times b, put the numbers in, and multiply. That gives %d." % prod,
    ])))
    return lesson(beats, None, None, "rule")


RULES = [simplify, sub2, sub1, two_term, square, product]


def rule_for(q):
    for rule in RULES:
        out = rule(q)
        if out is not None:
            return out
    return None
