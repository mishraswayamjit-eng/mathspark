"""Rule lessons for the generated Grade 4 equations families.

    solve   "Solve: 7x − 8 = 34", "Find the value of x: 3x + 13 = 73", "5x + 10 = 85. x = ?"
    root    "If √x + 1 = 6, find x."

rule_for(q) returns a lesson, or None if the wording is not one of these.
"""
import re

from g4_gr4_equations_lib import (B, W, answer, balance, both, choose, divide, given, lesson, mark, note, pick,
                                  shuffled, strike)

MINUS = "−"


def _opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def _divide_words(d, a, v):
    """(extra board lines, words) for d ÷ a = v, said the way a 9-year-old can follow."""
    if v <= 10:
        return [], "%d times %d is %d, so %d divided by %d is %d." % (a, v, d, d, a, v)
    if v % 10 == 0 and d % 10 == 0:
        return [], "%d divided by %d is %d, so %d divided by %d is %d." % (d // 10, a, v // 10, d, a, v)
    r = v - 10
    if r == 1:
        return ([W("l4a", "%d = %d + %d" % (d, a * 10, a))],
                "%d times 10 is %d, and one more %d makes %d. So %d divided by %d is %d."
                % (a, a * 10, a, d, d, a, v))
    return ([W("l4a", "%d = %d + %d" % (d, a * 10, a * r))],
            "%d times 10 is %d. That leaves %d, and %d times %d is %d. So %d divided by %d is 10 and %d more, "
            "which is %d." % (a, a * 10, a * r, a, r, a * r, d, a, r, v))


# ── ax + b = c  /  ax − b = c ────────────────────────────────────────────────

_SOLVE = [
    re.compile(r"^(?:Solve|Find the value of x): (\d+)x ([+−-]) (\d+) = (\d+)$"),
    re.compile(r"^(\d+)x ([+−-]) (\d+) = (\d+)\. x = \?$"),
]


def solve(q):
    m = None
    for pat in _SOLVE:
        m = m or pat.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b, c = int(m.group(1)), int(m.group(3)), int(m.group(4))
    plus = m.group(2) == "+"
    d = c - b if plus else c + b
    if d % a or d <= 0 or a < 2:
        return None
    v = d // a

    sg = "+" if plus else MINUS            # the sign in the question
    un = MINUS if plus else "+"            # the sign that undoes it
    opw = "plus" if plus else "minus"
    unw = "minus" if plus else "plus"
    did = ("added %d" if plus else "took away %d") % b
    doing = "adding" if plus else "taking away"
    term = "%s %d" % (sg, b)
    undo = "%s %d" % (un, b)
    l1 = "%dx %s %d = %d" % (a, sg, b, c)
    said = "%d x, %s %d, equals %d" % (a, opw, b, c)

    beats = []

    # 1. The equation goes up.
    beats.append(B(pick(qid, "intro", [
        "Here is our equation. %s. The x is a hidden number, and we are going to find it." % said,
        "Let's put it on the board. %s. A number is hiding behind the x. Let's go and find it." % said,
        "Look at this one. %s. Our job is to find the number that x stands for." % said,
    ]), given("l1", l1)))

    # 2. What the equation says.
    beats.append(B(pick(qid, "story", [
        "%d x means %d times x. So someone took a secret number, multiplied it by %d, then %s, and got %d."
        % (a, a, a, did, c),
        "When a number sits next to x, it means times. So x was multiplied by %d, then someone %s, and the "
        "answer was %d." % (a, did, c),
    ]), note("l1", "%dx" % a, "%d × x" % a, "below")))

    # 3. First turn.
    form = pick(qid, "ask1", ["last", "undo", "first"])
    scale = balance("f1", "%dx %s %d" % (a, sg, b), str(c))
    if form == "last":
        choices, right = shuffled(qid, "c1", ["%s %d" % (doing, b), "multiplying by %d" % a])
        beats.append(B(
            "Both sides are worth the same, like a level balance. To find x we work backwards, and undo the last "
            "thing first. Which was done last?",
            scale,
            ask=choose(choices, right,
                       "Read it from left to right. First x was multiplied by %d. After that came the %s %d. "
                       "So the %s %d was last, and we undo it first." % (a, opw, b, opw, b))))
        do_lines = [
            "We undo %s by %s. So I %s both sides, and the balance stays level."
            % (doing, "taking away" if plus else "adding", ("take %d from" if plus else "add %d to") % b),
        ]
    elif form == "undo":
        good = ("take away %d" if plus else "add %d") % b
        slip = ("add %d" if plus else "take away %d") % b
        choices, right = shuffled(qid, "c1", [good, slip, "divide by %d" % b if b > 1 else "multiply by %d" % a])
        beats.append(B(
            "Think of a balance. Both sides are worth the same. To get x alone, we first undo the %s %d. "
            "How do we undo it?" % (opw, b),
            scale,
            ask=choose(choices, right,
                       "Adding and taking away are partners. Each one undoes the other. "
                       "So to undo %s %d, we %s %d." % (opw, b, "take away" if plus else "add", b))))
        do_lines = [
            "So %d %s. But if we did that on one side only, the balance would tip. So we do it to both sides."
            % (b, "comes off" if plus else "goes on"),
            "And the rule of the balance is: what we do to one side, we do to the other. So I write %s %d under both."
            % (unw, b),
        ]
    else:
        good = ("take %d from both sides" if plus else "add %d to both sides") % b
        slip = ("add %d to both sides" if plus else "take %d from both sides") % b
        choices, right = shuffled(qid, "c1", [good, slip, "divide both sides by %d" % a])
        beats.append(B(
            "Both sides are worth the same, like a level balance, and every move must keep it level. "
            "What should our first move be?",
            scale,
            ask=choose(choices, right,
                       "We undo the last thing first, and that is the %s %d. Its opposite is %s %d. "
                       "The dividing comes after that." % (opw, b, "taking away" if plus else "adding", b))))
        do_lines = [
            "To undo %s %d, we %s %d. And to keep the balance level, we do it to both sides."
            % (opw, b, "take away" if plus else "add", b),
            "The opposite of %s %d is %s %d. What we do to one side, we do to the other, so I write it under both."
            % (opw, b, unw, b),
        ]

    # 4. Do it to both sides.
    beats.append(B(pick(qid, "do", do_lines), strike("l1", term, undo), both("l1", undo)))

    # 5. What is left.
    beats.append(B(pick(qid, "left", [
        "On the left, only %d x is left. On the right, %d %s %d is %d. So %d x equals %d."
        % (a, c, unw, b, d, a, d),
        "Now the left side is just %d x. And %d %s %d makes %d. So %d times x is %d."
        % (a, c, unw, b, d, a, d),
    ]), W("l2", "%dx = %d %s %d" % (a, c, un, b)), W("l3", "%dx = %d" % (a, d))))

    # 6. Second turn: undo the times.
    choices, right = shuffled(qid, "c2", ["divide by %d" % a, "take away %d" % a, "multiply by %d" % a])
    if str(d) in _opts(q):
        ask2 = pick(qid, "trap2", [
            "Careful: %d is one of the choices, but %d is %d x, not x. So, what undoes times %d?" % (d, d, a, a),
            "Don't stop here! %d is in the list of answers, but it is what %d x is worth, not x. "
            "What undoes times %d?" % (d, a, a),
        ])
    else:
        ask2 = pick(qid, "ask2", [
            "Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
            "We are not done yet: %d is %d times x, not x. What undoes times %d?" % (d, a, a),
        ])
    beats.append(B(ask2, ask=choose(choices, right,
                                    "Times and divide are partners. What times does, divide undoes. "
                                    "So to undo times %d, we divide by %d." % (a, a))))

    # 7. Divide both sides.
    extra, words = _divide_words(d, a, v)
    beats.append(B("So we divide both sides by %d. %s" % (a, words),
                   divide("l3", a), *(extra + [W("l4", "%d ÷ %d = %d" % (d, a, v))])))

    # 8. The answer.
    beats.append(B(pick(qid, "found", [
        "So x equals %d. There is our hidden number!" % v,
        "That means x is %d. We found the number that was hiding." % v,
        "So x equals %d. The mystery is solved." % v,
    ]), answer("l5", "x = %d" % v), mark("l5", "x = %d" % v, "circle")))

    # 9. Check.
    beats.append(B(pick(qid, "check", [
        "Let's check. Put %d in place of x. %d times %d is %d, and %d %s %d is %d. It works!"
        % (v, a, v, d, d, opw, b, c),
        "Good mathematicians always check. %d times %d is %d, and %d %s %d is %d. Both sides match."
        % (a, v, d, d, opw, b, c),
    ]), W("l6", "%d × %d %s %d = %d" % (a, v, sg, b, c))))

    # 10. The method in one line.
    beats.append(B(pick(qid, "sum", [
        "So the plan is to work backwards. First undo the adding or taking away. Then undo the times.",
        "Remember the order. Clear the plus or minus first, then divide. And do the same to both sides each time.",
        "Every equation like this works the same way. Undo the last thing first, and keep both sides level.",
    ])))

    return lesson(beats, "x", v, origin="rule")


# ── √x + b = c ───────────────────────────────────────────────────────────────

_ROOT = re.compile(r"^If √x \+ (\d+) = (\d+), find x\.$")


def root(q):
    m = _ROOT.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    b, c = int(m.group(1)), int(m.group(2))
    r = c - b
    if r < 2:
        return None
    v = r * r
    opts = _opts(q)

    beats = []
    beats.append(B(pick(qid, "intro", [
        "Here is our puzzle. The square root of x, plus %d, equals %d. We want to find x." % (b, c),
        "Let's put it on the board. The square root of x, plus %d, equals %d. The x is a hidden number." % (b, c),
    ]), given("l1", "√x + %d = %d" % (b, c))))

    beats.append(B(
        "This sign is a square root. The square root of x is the number that, times itself, makes x. "
        "Let's find the root first.",
        mark("l1", "√x", "box"), note("l1", "√x", "the root", "below")))

    good, slip = "take away %d" % b, "add %d" % b
    choices, right = shuffled(qid, "c1", [good, slip, "multiply %d by itself" % c])
    trap = ""
    if str(c * c) in opts:
        trap = " We must not square the %d yet. The %d still has the extra %d in it." % (c, c, b)
    beats.append(B(
        "The root, plus %d, makes %d. So to get the root alone, how do we undo plus %d?" % (b, c, b),
        ask=choose(choices, right,
                   "Adding and taking away are partners. To undo plus %d, we take away %d.%s" % (b, b, trap))))

    beats.append(B(pick(qid, "do", [
        "We take %d from both sides, so the two sides stay equal. %d minus %d is %d." % (b, c, b, r),
        "So %d comes off both sides, to keep things level. And %d minus %d is %d." % (b, c, b, r),
    ]), strike("l1", "+ %d" % b, "%s %d" % (MINUS, b)), both("l1", "%s %d" % (MINUS, b)),
        W("l2", "√x = %d %s %d" % (c, MINUS, b)), W("l3", "√x = %d" % r)))

    wrongs = [w for w in (str(r), str(2 * r), str(c * c), str(v + b)) if w in opts and w != str(v)]
    picks = [str(v)] + (wrongs[:2] if len(wrongs) >= 2 else [str(r), str(2 * r)])
    choices, right = shuffled(qid, "c2", picks)
    beats.append(B(
        "So the square root of x is %d. Careful: %d is the root, not x. Which number has %d as its square root?"
        % (r, r, r),
        ask=choose(choices, right,
                   "The root times itself gives x. So we need %d times %d, not %d on its own." % (r, r, r))))

    if r <= 10:
        beats.append(B("To go back from the root to x, we multiply the root by itself. %d times %d is %d."
                       % (r, r, v), W("l4", "%d × %d = %d" % (r, r, v))))
    else:
        t = r - 10
        beats.append(B(
            "We multiply the root by itself. %d times 10 is %d, and %d times %d is %d. Together that makes %d."
            % (r, r * 10, r, t, r * t, v),
            W("l4", "%d × %d = %d + %d" % (r, r, r * 10, r * t)), W("l4b", "%d × %d = %d" % (r, r, v))))

    beats.append(B(pick(qid, "found", [
        "So x equals %d. There is our hidden number!" % v,
        "That means x is %d. We found it." % v,
    ]), answer("l5", "x = %d" % v), mark("l5", "x = %d" % v, "circle")))

    beats.append(B(
        "Let's check. The square root of %d is %d, because %d times %d is %d. And %d plus %d is %d. It works!"
        % (v, r, r, r, v, r, b, c),
        W("l6", "√%d + %d = %d" % (v, b, c))))

    beats.append(B("So the plan is: first get the square root alone. Then multiply it by itself to find x."))
    return lesson(beats, "x", v, origin="rule")


def rule_for(q):
    for rule in (solve, root):
        script = rule(q)
        if script is not None:
            return script
    return None
