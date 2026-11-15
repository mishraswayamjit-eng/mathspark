"""Rule lessons for the generated algebra families.

    solve       "Solve: 7x + 18 = 95", "Solve: 5x − 3 = 47", "Find the value of x: 2x + 14 = 40"
    simplify    "Simplify: 6x + 9 + 8x − 5"
    sub2        "If x = 5 and y = 1, find the value of 5x + 1y."
    think       "Think of a number 8. Multiply it by 2 and add 9. What do you get?"
    sub1        "If x = 6, find the value of 3x + 13 − 5."

rule_for(q) returns a lesson, or None if the wording is not one of these.
"""
import re

from algebra_lib import (B, T, W, answer, both, choose, divide, given, group, lesson, mark, note, nth_at, pick,
                         shuffled, strike)

MINUS = "−"


def _opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


# ── Solve: ax + b = c  /  ax − b = c ─────────────────────────────────────────

_SOLVE = re.compile(r"^(?:Solve|Find the value of x): (\d+)x ([+−-]) (\d+) = (\d+)$")


def solve(q):
    m = _SOLVE.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b, c = int(m.group(1)), int(m.group(3)), int(m.group(4))
    plus = m.group(2) == "+"
    d = c - b if plus else c + b
    if d % a or d <= 0:
        return None
    v = d // a

    sg = "+" if plus else MINUS            # the sign in the question
    un = MINUS if plus else "+"            # the sign that undoes it
    opw = "plus" if plus else "minus"
    unw = "minus" if plus else "plus"
    term = "%s %d" % (sg, b)
    undo = "%s %d" % (un, b)
    l1 = "%dx %s %d = %d" % (a, sg, b, c)
    said = "%d x, %s %d, equals %d" % (a, opw, b, c)

    beats = []

    # 1. The equation goes up.
    story = "multiplied it by %d, then %s %d, and got %d" % (a, "added" if plus else "took away", b, c)
    beats.append(B(pick(qid, "intro", [
        "Here is our equation. %s. Somewhere behind that x a number is hiding, and we are going to find it." % said,
        "Let's write it on the board. %s. The x is a mystery number, and our job is to work out what it is." % said,
        "%s. Someone took a secret number, %s. Let's work backwards and find that number." % (said, story),
        "Look at this one. %s. We want x standing all on its own, so we can see what it is worth." % said,
    ]), given("l1", l1)))

    # 2. First turn: what has to go first?
    form = pick(qid, "ask1", ["way", "first", "undo"])
    if form == "way":
        choices, right = shuffled(qid, "c1", ["the %s" % term, "the %d on the right" % c, "the %d in front of x" % a])
        beats.append(B(
            "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. "
            "So, what is in the way of the %d x?" % a,
            ask=choose(choices, right,
                       "Look at the left side once more. The %d x has a %s %d hanging on to it. "
                       "That is the first thing to clear away." % (a, opw, b))))
    elif form == "first":
        good = ("take %d from both sides" if plus else "add %d to both sides") % b
        slip = ("add %d to both sides" if plus else "take %d from both sides") % b
        choices, right = shuffled(qid, "c1", [good, "divide both sides by %d" % a, slip])
        beats.append(B(pick(qid, "first", [
            "An equation is like a balance: both sides weigh the same, and we must keep it that way. "
            "What should we do first?",
            "Both sides of an equation weigh the same, like a balance, and every move has to keep it level. "
            "So what is our first move?",
        ]),
            ask=choose(choices, right,
                       "If we divided first, the %d would have to be divided as well, and that gets messy. "
                       "It is easier to clear the %s %d first, by doing the opposite." % (b, opw, b))))
    else:
        good = ("subtract %d" if plus else "add %d") % b
        slip = ("add %d" if plus else "subtract %d") % b
        choices, right = shuffled(qid, "c1", [good, slip, "divide by %d" % a])
        beats.append(B(
            "The two sides are worth the same, like a level see-saw. To get x alone we undo things, last one first. "
            "The %s %d was done last. How do we undo it?" % (opw, b),
            ask=choose(choices, right,
                       "Adding and taking away are partners: each one undoes the other. "
                       "So to undo %s %d, we %s %d." % (opw, b, "take away" if plus else "add", b))))

    # 3. Do it to both sides. The words follow on from the question that was just asked.
    off = "comes off" if plus else "goes on to"
    take = ("take %d from" if plus else "add %d to") % b
    if form == "undo":
        lines3 = [
            "So %d %s. But if we only did that on the left, the balance would tip. So we %s both sides."
            % (b, "comes off" if plus else "goes on", take),
            "And here is the rule of the balance: whatever we do to one side, we do to the other. "
            "So %d %s both sides." % (b, off),
        ]
    elif form == "first":
        lines3 = [
            "%s is what undoes %s %d. So I cross out the %s %d, and write %s %d under both sides."
            % ("Taking away" if plus else "Adding", opw, b, opw, b, unw, b),
            "We %s both sides. %s is the opposite of %s, so that clears the %s %d away."
            % (take, "Minus" if plus else "Plus", opw, opw, b),
        ]
    elif plus:
        lines3 = [
            "To undo plus %d, we take away %d. And to keep the balance level, we take it from both sides." % (b, b),
            "We clear it by doing the opposite: we take away %d. But if we only did that on the left, "
            "the balance would tip. So %d comes off both sides." % (b, b),
            "The opposite of plus %d is minus %d. Whatever we do to one side we do to the other, "
            "so I write it under both." % (b, b),
        ]
    else:
        lines3 = [
            "To undo minus %d, we add %d. And to keep the balance level, we add it to both sides." % (b, b),
            "We clear it by doing the opposite: we add %d. But if we only did that on the left, "
            "the balance would tip. So %d goes on to both sides." % (b, b),
            "The opposite of minus %d is plus %d. Whatever we do to one side we do to the other, "
            "so I write it under both." % (b, b),
        ]
    beats.append(B(pick(qid, "do", lines3), strike("l1", term, undo), both("l1", undo)))

    # 4. What is left.
    left = [
        "On the left, %s %d and %s %d cancel each other out. On the right, %d %s %d makes %d."
        % (opw, b, unw, b, c, unw, b, d),
        "On the left the %s %d has gone, and only %d x is there. On the right, %d %s %d is %d. So %d x equals %d."
        % (opw, b, a, c, unw, b, d, a, d),
    ]
    beats.append(B(pick(qid, "left", left), W("l2", "%dx = %d %s %d" % (a, c, un, b)), W("l3", "%dx = %d" % (a, d))))

    # 5. Second turn: undo the times.
    choices, right = shuffled(qid, "c2", ["divide by %d" % a, "subtract %d" % a, "multiply by %d" % a])
    if str(d) in _opts(q):
        ask2 = pick(qid, "ask2", [
            ("Careful, we are not finished. %d is what %d x is worth, not x. "
             "How do we get from %d lots of x down to one x?" % (d, a, a),
             "%d x is %d equal lots of x. To find one lot, we share %d into %d equal parts. "
             "That is dividing by %d." % (a, a, d, a, a)),
            ("It is tempting to stop here and say %d. But that is %d x, and we want just x. "
             "%d x means %d times x. What undoes times %d?" % (d, a, a, a, a),
             "Times and divide are partners. Whatever times does, divide undoes. "
             "So to undo times %d, we divide by %d." % (a, a)),
        ])
    else:
        ask2 = pick(qid, "ask2", [
            ("Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
             "Times and divide are partners. Whatever times does, divide undoes. "
             "So to undo times %d, we divide by %d." % (a, a)),
            ("Now only the %d is stuck to the x. %d x means %d lots of x. How do we find just one x?" % (a, a, a),
             "%d x is %d equal lots of x. To find one lot, we share %d into %d equal parts. "
             "That is dividing by %d." % (a, a, d, a, a)),
        ])
    beats.append(B(ask2[0], ask=choose(choices, right, ask2[1])))

    # 6. Divide both sides.
    beats.append(B(pick(qid, "div", [
        "So we divide both sides by %d." % a,
        "We divide the left by %d and, to keep it fair, the right by %d too." % (a, a),
        "So a bar goes under each side, and we divide both by %d." % a,
    ]), divide("l3", a)))

    # 7. The answer.
    beats.append(B(pick(qid, "ans", [
        "%d divided by %d is %d. So x equals %d. There is our hidden number!" % (d, a, v, v),
        "%d x divided by %d is just x. And %d divided by %d is %d. So x equals %d." % (a, a, d, a, v, v),
        "%d divided by %d is %d. So x equals %d. Found it!" % (d, a, v, v),
    ]), answer("l4", "x = %d" % v), mark("l4", "x = %d" % v)))

    # 8. Check in the equation we started with.
    beats.append(B(pick(qid, "check", [
        "Good mathematicians always check. Put %d back in place of x. %d times %d is %d, and %d %s %d is %d. It works."
        % (v, a, v, d, d, opw, b, c),
        "Let's test it in the equation we started with. %d times %d is %d. Then %d %s %d gives %d, just as it should."
        % (a, v, d, d, opw, b, c),
        "Does it really work? Swap the x for %d. %d times %d is %d, and %d %s %d is %d. Both sides match."
        % (v, a, v, d, d, opw, b, c),
    ]), W("l5", "%d × %d %s %d = %d" % (a, v, sg, b, c))))

    # 9. The method in one line.
    beats.append(B(pick(qid, "sum", [
        "So here is the plan for any equation like this. First clear away what is %s. Then undo the times. "
        "Your turn next!" % ("added" if plus else "taken off"),
        "Remember the order: undo the %s %d first, then undo the times %d. And every move is made on both sides."
        % (opw, b, a),
        "We undid things in reverse: first the %s, then the times. Keep the balance level, "
        "and the hidden number always comes out." % opw,
    ])))
    return lesson(beats, "x", v, "rule")


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
        "%s. That is quite a mouthful. Let's tidy it up, so it says the same thing in fewer pieces." % said,
        "Look at this. %s. Four pieces, and some of them can be joined together. Let's see which." % said,
    ]), given("l1", l1)))

    if pick(qid, "ask1", [0, 1]) == 0:
        choices, right = shuffled(qid, "c1", ["%dx and %dx" % (a, c), "%dx and %d" % (a, b), "%d and %dx" % (b, c)])
        beats.append(B(
            "Some of these pieces belong together. The ones with an x are one family, "
            "and the plain numbers are another. Which two are like terms?",
            ask=choose(choices, right,
                       "Like terms have the same letter part. %d x and %d x both have an x, so they are family. "
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
        "So gather the x terms. %d x and %d x together make %d x." % (a, c, xs),
        "First the x family. %d lots of x and %d more lots of x make %d lots of x." % (a, c, xs),
    ]), group("l1", [t_a, t_c], "%dx" % xs), W("l2", "%dx + %dx = %dx" % (a, c, xs))))

    if plus:
        say_n = "Now the plain numbers. %d plus %d makes %d." % (b, d, n)
    else:
        say_n = ("Now the plain numbers. Careful: the sign in front of a number belongs to that number. "
                 "So this is %d minus %d, which is %d." % (b, d, n))
    beats.append(B(say_n, group("l1", [t_b, t_d], str(n)), W("l3", "%d %s %d = %d" % (b, sg, d, n))))

    choices, right = shuffled(qid, "c2", ["No, they are not like terms", "Yes, it makes %dx" % (xs + n)])
    beats.append(B(
        "So we have %d x and %d. Here is where people slip. Can we squash those two into one term?" % (xs, n),
        ask=choose(choices, right,
                   "%d x means %d lots of a hidden number. %d is a plain number. "
                   "They are different families, so they stay side by side." % (xs, xs, n))))

    final = "%dx + %d" % (xs, n)
    beats.append(B(pick(qid, "ans", [
        "So the short form is %d x plus %d. Same value, far fewer pieces." % (xs, n),
        "That leaves %d x plus %d. It cannot get any shorter than that." % (xs, n),
    ]), answer("l4", final), mark("l4", final)))

    if pick(qid, "check", [0, 1]) == 0:
        t = xs + n
        beats.append(B(
            "Let's test it with a number. Say x is 1. The long one is %d plus %d plus %d %s %d, which is %d. "
            "The short one is %d plus %d, also %d. They match." % (a, b, c, opw, d, t, xs, n, t),
            W("l5", "%d + %d + %d %s %d = %d" % (a, b, c, sg, d, t)), W("l6", "%d + %d = %d" % (xs, n, t))))
    else:
        t = 2 * xs + n
        beats.append(B(
            "Let's test it with a number. Say x is 2. The long one comes to %d. "
            "The short one, %d times 2 plus %d, comes to %d as well. They match." % (t, xs, n, t),
            W("l5", "%d × 2 + %d + %d × 2 %s %d = %d" % (a, b, c, sg, d, t)),
            W("l6", "%d × 2 + %d = %d" % (xs, n, t))))

    beats.append(B(pick(qid, "sum", [
        "So to simplify: gather the x terms, gather the plain numbers, and keep the two families apart.",
        "The plan every time: x terms with x terms, numbers with numbers, and each sign stays with its own term.",
    ])))
    return lesson(beats, "x", n, "rule")


# ── If x = .. and y = .., find px + qy ───────────────────────────────────────

_SUB2 = re.compile(r"^If x = (\d+) and y = (\d+), find the value of (\d+)x \+ (\d+)y\.$")


def _meaning_ask(qid, p, x):
    """The turn every substitution lesson starts with: what does 5x mean?"""
    choices, right = shuffled(qid, "c1", ["%d × %d" % (p, x), "%d + %d" % (p, x), "the number %d%d" % (p, x)])
    say = pick(qid, "ask1", [
        "First, what does %d x turn into when x is %d?" % (p, x),
        "Before we swap anything: when x is %d, what is %d x?" % (x, p),
    ])
    if_not = ("When a number sits right next to a letter, there is a hidden times sign between them. "
              "So %d x means %d times x, and here that is %d times %d." % (p, p, p, x))
    return say, choose(choices, right, if_not)


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
        "We are told that x is %d and y is %d. And we want to know what %d x plus %d y is worth." % (x, y, p, k),
        "Two letters this time. x is %d and y is %d. Our job is to find the value of %d x plus %d y." % (x, y, p, k),
    ]), given("l1", "x = %d, y = %d" % (x, y), label=True), given("l2", "%dx + %dy" % (p, k), label=True)))

    say, ask = _meaning_ask(qid, p, x)
    beats.append(B(say, ask=ask))

    beats.append(B(
        "So we swap each letter for its number. %d x becomes %d times %d, and %d y becomes %d times %d."
        % (p, p, x, k, k, y),
        note("l2", "x", str(x)), note("l2", "y", str(y)), W("l3", "%d × %d + %d × %d" % (p, x, k, y))))

    choices, right = shuffled(qid, "c2", ["the two multiplications", "the addition in the middle"])
    beats.append(B(
        "Now we have two multiplications and one addition. Which do we do first?",
        ask=choose(choices, right,
                   "Multiplying comes before adding. So we work out each times first, "
                   "and only then add the two answers.")))

    if k == 1:
        second = "And 1 y is just one single y, so that is %d." % y
    else:
        second = "And %d times %d is %d." % (k, y, ky)
    beats.append(B("%d times %d is %d. %s" % (p, x, px, second),
                   W("l4", "%d × %d = %d" % (p, x, px)), W("l5", "%d × %d = %d" % (k, y, ky))))

    last = "%d + %d = %d" % (px, ky, tot)
    beats.append(B(
        "Now add them. %d plus %d is %d. So %d x plus %d y is worth %d." % (px, ky, tot, p, k, tot),
        answer("l6", last), mark("l6", T(str(tot), nth_at(last, str(tot), last.index("= ") + 2)))))

    beats.append(B(pick(qid, "sum", [
        "So for any question like this: swap each letter for its number, do the times first, then add. "
        "And %d x is %d times x, never the two digits side by side." % (p, p),
        "The plan: put the numbers in place of the letters, multiply, then add. "
        "A number next to a letter always means times.",
    ])))
    return lesson(beats, None, None, "rule")


# ── Think of a number ────────────────────────────────────────────────────────

_THINK = re.compile(r"^Think of a number (\d+)\. Multiply it by (\d+) and add (\d+)\. What do you get\?$")


def think(q):
    m = _THINK.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    n, t, k = (int(g) for g in m.groups())
    prod = n * t
    tot = prod + k

    beats = []
    beats.append(B(pick(qid, "intro", [
        "This one is a recipe. Start with %d, multiply it by %d, then add %d. "
        "We just have to follow it in the right order." % (n, t, k),
        "A number game! Our number is %d. We multiply it by %d, and then we add %d. "
        "Let's take it one step at a time." % (n, t, k),
    ]), given("l1", "start with %d:  × %d,  then + %d" % (n, t, k), label=True)))

    choices, right = shuffled(qid, "c1", ["%d × %d" % (n, t), "%d + %d" % (n, k), "%d + %d" % (t, k)])
    beats.append(B(
        pick(qid, "ask1", ["What do we work out first?", "Which step comes first?"]),
        ask=choose(choices, right,
                   "Read the recipe again: multiply it by %d comes before add %d. "
                   "So first we work out %d times %d." % (t, k, n, t))))

    beats.append(B(pick(qid, "mul", [
        "%d times %d is %d." % (n, t, prod),
        "So we multiply. %d times %d makes %d." % (n, t, prod),
    ]), W("l2", "%d × %d = %d" % (n, t, prod))))

    raw = ["to the %d" % prod, "to the %d we started with" % n, "to the %d" % t]
    if n == t:
        raw = raw[:2]
    choices, right = shuffled(qid, "c2", raw)
    beats.append(B(
        "Next the recipe says add %d. What do we add it to?" % k,
        ask=choose(choices, right,
                   "We add it to the number we are holding now, not the one we started with. "
                   "Right now we are holding %d." % prod)))

    last = "%d + %d = %d" % (prod, k, tot)
    beats.append(B(
        "%d plus %d is %d. That is what we get." % (prod, k, tot),
        answer("l3", last), mark("l3", T(str(tot), nth_at(last, str(tot), last.index("= ") + 2)))))

    beats.append(B(
        "Here is the clever bit. If we call the starting number n, the whole recipe is %d n plus %d. "
        "That is all algebra is: a recipe, with a letter standing for the number." % (t, k),
        W("l4", "for any number n:  %dn + %d" % (t, k), label=True)))

    beats.append(B(
        "Put %d in for n. %d times %d, plus %d, is %d. The same answer. "
        "Just never add the %d and the %d first, because that changes the recipe." % (n, t, n, k, tot, t, k),
        W("l5", "%d × %d + %d = %d" % (t, n, k, tot))))

    beats.append(B(pick(qid, "sum", [
        "So: follow the steps in the order they are given, one at a time, "
        "and always carry on from the number you have reached.",
        "The plan for any number recipe: do the first step, keep the result, then do the next step to that result.",
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
        "This time the hidden number is not hidden at all: x is %d. "
        "So we can work out what %d x, plus %d, minus %d is worth." % (x, p, b, c),
    ]), given("l1", "x = %d" % x, label=True), given("l2", "%dx + %d − %d" % (p, b, c), label=True)))

    say, ask = _meaning_ask(qid, p, x)
    beats.append(B(say, ask=ask))

    beats.append(B(
        "So we rub out the x and write %d in its place, with a times sign. %d times %d, plus %d, minus %d."
        % (x, p, x, b, c),
        note("l2", "x", str(x)), W("l3", "%d × %d + %d − %d" % (p, x, b, c))))

    choices, right = shuffled(qid, "c2", ["%d × %d" % (p, x), "%d + %d" % (x, b), "any order is fine"])
    beats.append(B(
        "Three jobs here: a times, a plus and a minus. Which one goes first?",
        ask=choose(choices, right,
                   "Multiplying always goes before adding and taking away. So %d times %d comes first." % (p, x))))

    beats.append(B(
        "%d times %d is %d. So now we have %d, plus %d, minus %d." % (p, x, px, px, b, c),
        mark("l3", "%d × %d" % (p, x), "underline"), W("l4", "%d + %d − %d" % (px, b, c))))

    if b == c:
        last = "%d + %d − %d = %d" % (px, b, c, tot)
        beats.append(B(
            "Look closely: plus %d, and then minus %d. Those two undo each other. So we are left with %d."
            % (b, c, tot),
            answer("l5", last), mark("l5", T(str(tot), nth_at(last, str(tot), last.index("= ") + 2)))))
    else:
        last = "%d − %d = %d" % (s, c, tot)
        beats.append(B(
            "Now we go left to right. %d plus %d is %d. Then %d minus %d is %d." % (px, b, s, s, c, tot),
            W("l5", "%d + %d = %d" % (px, b, s)), answer("l6", last),
            mark("l6", T(str(tot), nth_at(last, str(tot), last.index("= ") + 2)))))

    beats.append(B(pick(qid, "sum", [
        "So when x is %d, the whole thing is worth %d. The plan: swap the letter for its number, "
        "multiply first, then work left to right." % (x, tot),
        "That gives %d. Remember the order: number in for the letter, then the times, "
        "then the plus and minus from left to right." % tot,
    ])))
    return lesson(beats, None, None, "rule")


RULES = [solve, simplify, sub2, think, sub1]


def rule_for(q):
    for rule in RULES:
        out = rule(q)
        if out is not None:
            return out
    return None
