"""More rule lessons: a × b ± c, a ÷ b + c × d, and Solve: ax ± b = c. See arithmetic_rules.py."""
from fractions import Fraction

from arithmetic_common import (ANS, B, BOTH, DIV, GIVEN, M, N, S, W, choose, lesson, nth_at, pick, placed)
from arithmetic_rules import SUMMARY, circle_answer


# ── a × b + c  and  a × b − c ────────────────────────────────────────────────

def times_then(qid, a, b, sign, c):
    p = a * b
    plus = sign == "+"
    r = p + c if plus else p - c
    word = "plus" if plus else "minus"
    l1 = "%d × %d %s %d" % (a, b, sign, c)
    pair = "%d × %d" % (a, b)
    tail = "%d %s %d" % (b, sign, c)
    l2 = "%s = %d %s %d" % (l1, p, sign, c)
    l3 = "%s = %d" % (l1, r)
    choices, right = placed(qid, "c1", pair, [tail, "either, it makes no difference"])
    beats = [
        B(pick(qid, "i", [
            "Here is our sum. %d times %d, %s %d. Two signs, a times and a %s." % (a, b, word, c, word),
            "Let's write this one up. %d times %d, %s %d. Before we work anything out, we decide where to start." % (a, b, word, c),
            "Look at this line. %d times %d, %s %d. Short, but it still has an order to follow." % (a, b, word, c),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "So, which part do we do first?",
            "Which pair of numbers goes first?",
            "Have a look at the two signs. Where do we start?",
        ]), ask=choose(choices, right, pick(qid, "n", [
            ("%d plus %d looks like the easier bit, so it is tempting. But times is stronger than plus, so %d times %d has to go first." % (b, c, a, b))
            if plus else
            ("The %d and the %d sit either side of the minus, so they look like a pair. But times is stronger than minus, so %d times %d has to go first." % (b, c, a, b)),
            "Look for the times sign. Times comes before %s, so %d times %d goes first." % (word, a, b),
        ]))),
    ]
    tens, ones = (a // 10) * 10, a % 10
    if a <= 10 and b <= 10:
        beats.append(B(pick(qid, "m", [
            "Times comes before %s, so this pair goes first. I'll underline it. %d times %d is %d." % (word, a, b, p),
            "I'll underline %d times %d, because times is done before %s. %d times %d makes %d." % (a, b, word, a, b, p),
        ]), M("l1", pair), N("l1", pair, str(p))))
    elif ones == 0:
        beats.append(B("Times comes before %s, so I'll underline this pair. %d is %d tens, and %d times %d is %d. So we have %d tens, which is %d."
                       % (word, a, a // 10, a // 10, b, (a // 10) * b, (a // 10) * b, p),
                       M("l1", pair), W("m1", "%d × %d = %d" % (a // 10, b, (a // 10) * b)),
                       W("m2", "%d × %d = %d" % (a, b, p)), N("l1", pair, str(p))))
    else:
        x, y = tens * b, ones * b
        beats.append(B(pick(qid, "m", [
            "Times comes before %s, so I'll underline this pair. %d times %d is easier in two bites, so let's split %d into %d and %d." % (word, a, b, a, tens, ones),
            "I'll underline %d times %d, because times goes before %s. To make it easier, we break %d into %d and %d." % (a, b, word, a, tens, ones),
        ]), M("l1", pair), W("m1", "%d × %d = %d × %d + %d × %d" % (a, b, tens, b, ones, b))))
        beats.append(B("%d times %d is %d, and %d times %d is %d. Put them together and we get %d." % (tens, b, x, ones, b, y, p),
                       W("m2", "%d × %d + %d × %d = %d + %d = %d" % (tens, b, ones, b, x, y, p)), N("l1", pair, str(p))))
    beats.append(B(pick(qid, "w", [
        "Now we write the line again, with %d sitting where %d times %d was. The %s %d comes down unchanged." % (p, a, b, word, c),
        "So %d times %d has turned into %d, and the %s %d is still waiting at the end." % (a, b, p, word, c),
    ]), W("l2", l2)))
    beats.append(B(pick(qid, "a", [
        "And %d %s %d is %d. That is our answer." % (p, word, c, r),
        "Now it is easy. %d %s %d %s %d." % (p, word, c, "makes" if plus else "leaves", r),
    ]), ANS("l3", l3), circle_answer("l3", l3, str(r))))
    t = a * (b + c) if plus else a * (b - c)
    if t > 0 and t != r:
        beats.append(B(pick(qid, "t", [
            "Here is why the order matters. Doing %d %s %d first is like putting a bracket round them, and that gives %d. A different sum, so a different answer." % (b, word, c, t),
            "See the trap? If the %d %s %d went first, as if it wore a bracket, the line would come to %d. That belongs to a different sum." % (b, word, c, t),
        ]), W("l4", "%d × (%d %s %d) = %d" % (a, b, sign, c, t))))
    beats.append(B(pick(qid, "s", SUMMARY)))
    return lesson(*beats, origin="rule")


# ── a ÷ b + c × d ────────────────────────────────────────────────────────────

def divide_plus_times(qid, a, b, c, d, answer_text):
    q, rem = divmod(a, b)
    p = c * d
    l1 = "%d ÷ %d + %d × %d" % (a, b, c, d)
    dpair = "%d ÷ %d" % (a, b)
    tpair = "%d × %d" % (c, d)
    t_at = l1.index("+")
    choices, right = placed(qid, "c1", "%s and %s" % (dpair, tpair),
                            ["%d + %d" % (b, c), "only %s, then carry on along" % dpair])
    beats = [
        B(pick(qid, "i", [
            "Here is our sum. %d divided by %d, plus %d times %d. A divide, a plus and a times, all in one line." % (a, b, c, d),
            "Let's write it up. %d divided by %d, plus %d times %d. Three signs, so we need to think about the order." % (a, b, c, d),
            "Look at this one. %d divided by %d, plus %d times %d. Before we work anything out, we decide what goes first." % (a, b, c, d),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "Which parts have to be done before the plus?",
            "The plus sits in the middle. What must we work out before we can use it?",
        ]), ask=choose(choices, right,
                       "Divide and times are both stronger than plus. So both of those pairs are worked out first, and the plus waits in the middle until they are done.")),
    ]
    if rem == 0:
        beats.append(B(pick(qid, "d", [
            "Divide and times both come before plus. Let's take them one at a time. %d divided by %d is %d." % (a, b, q),
            "Both of these beat the plus. First the divide: %d divided by %d is %d." % (a, b, q),
        ]), M("l1", dpair), N("l1", dpair, str(q))))
        left = str(q)
    else:
        beats.append(B("Divide and times both come before plus. Let's start with the divide. %d divided by %d does not come out evenly: %d goes into %d only %d times, with %d left over."
                       % (a, b, b, a, q, rem), M("l1", dpair), W("d1", "%d = %d × %d + %d" % (a, b, q, rem))))
        part = Fraction(rem, b)
        if part == Fraction(1, 2):
            left = "%d.5" % q
            beats.append(B("Share the %d left over among %d, and each gets a half. So %d divided by %d is %d and a half, which we write as %s." % (rem, b, a, b, q, left),
                           W("d2", "%s = %s" % (dpair, left)), N("l1", dpair, left)))
        else:
            assert part == Fraction(2, 3), qid
            left = "%d + 2/3" % q
            beats.append(B("Share the %d left over among %d, and each gets two thirds. So %d divided by %d is %d and two thirds." % (rem, b, a, b, q),
                           W("d2", "%s = %s" % (dpair, left)), N("l1", dpair, "%d 2/3" % q)))
    beats.append(B(pick(qid, "m", [
        "Now the times. %d times %d is %d." % (c, d, p),
        "And the other pair: %d times %d makes %d." % (c, d, p),
    ]), M("l1", tpair, "underline", nth_at(l1, tpair, t_at)), N("l1", tpair, str(p), "below", nth_at(l1, tpair, t_at))))
    l2 = "%s = %s + %d" % (l1, left, p)
    if rem == 0:
        r = q + p
        l3 = "%s = %d" % (l1, r)
        beats.append(B(pick(qid, "w", [
            "Now we write the line again with those two answers in place. It has shrunk to %d plus %d." % (q, p),
            "Put the two answers where the pairs were, and the line is much shorter: %d plus %d." % (q, p),
        ]), W("l2", l2)))
        beats.append(B(pick(qid, "a", [
            "At last the plus gets its turn. %d plus %d is %d. That is our answer." % (q, p, r),
            "Now the plus can go. %d plus %d makes %d." % (q, p, r),
        ]), ANS("l3", l3), circle_answer("l3", l3, str(r))))
        t = (q + c) * d
        if t != r:
            beats.append(B("Here is the trap. Working along from the left, one step at a time, is like wrapping a bracket round the first part. That gives %d, which belongs to a different sum." % t,
                           W("l4", "(%d ÷ %d + %d) × %d = %d" % (a, b, c, d, t))))
    elif left.endswith(".5"):
        l3 = "%s = %s" % (l1, answer_text)
        beats.append(B("Now we write the line again with those two answers in place. It has shrunk to %s plus %d." % (left, p), W("l2", l2)))
        beats.append(B("At last the plus gets its turn. %s plus %d is %s. That is our answer." % (left, p, answer_text),
                       ANS("l3", l3), circle_answer("l3", l3, answer_text)))
    else:
        whole = q + p
        beats.append(B("Now we write the line again with those two answers in place: %d and two thirds, plus %d." % (q, p), W("l2", l2)))
        beats.append(B("Add the whole numbers, %d plus %d is %d, and the two thirds comes along too. So the answer is %d and two thirds." % (q, p, whole, whole),
                       W("l3", "%d + %d + 2/3 = %d + 2/3" % (q, p, whole)), ANS("l4", "%s = %s" % (l1, answer_text), True),
                       M("l4", answer_text, "circle")))
    beats.append(B(pick(qid, "s", SUMMARY)))
    return lesson(*beats, origin="rule")


# ── Solve: ax + b = c  and  ax − b = c ───────────────────────────────────────

def equation(qid, a, sign, b, c):
    plus = sign == "+"
    s = c - b if plus else c + b
    x = s // a
    assert a * x == s, qid
    word = "plus" if plus else "minus"
    undo_word = "minus" if plus else "plus"
    undo_sign = "−" if plus else "+"
    undo_verb = "take away" if plus else "add"
    l1 = "%dx %s %d = %d" % (a, sign, b, c)
    term = "%s %d" % (sign, b)
    choices, right = placed(qid, "c1", "the %s" % term, ["the %d on the right" % c, "the %d in front of x" % a])
    c2, right2 = placed(qid, "c2", "divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a])
    beats = [
        B(pick(qid, "i", [
            "Here is our equation. %d x, %s %d, equals %d. Somewhere behind that x a number is hiding, and we are going to find it." % (a, word, b, c),
            "Let's write it up. %d x, %s %d, equals %d. The x is a number in disguise, and our job is to unmask it." % (a, word, b, c),
            "Look at this equation. %d x, %s %d, equals %d. We want the x all on its own, so we can see what it is." % (a, word, b, c),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what is in the way of the %d x?" % a,
            "The two sides balance, like a see-saw. We want the %d x alone on its side. What do we clear away first?" % a,
        ]), ask=choose(choices, right,
                       "Look at the left side once more. The %d x has a %s %d hanging on to it. That is the first thing to clear away." % (a, word, b))),
        B(pick(qid, "u", [
            "To undo %s %d, we %s %d. And to keep the balance level, we do it to both sides." % (word, b, undo_verb, b),
            "The opposite of %s %d is %s %d. So we %s %d, and we do it on both sides so the balance stays level." % (word, b, undo_word, b, undo_verb, b),
        ]), S("l1", term, "%s %d" % (undo_sign, b)), BOTH("l1", "%s %d" % (undo_sign, b))),
        B(pick(qid, "r", [
            "On the left, %s %d and %s %d cancel each other out. On the right, %d %s %d %s %d." % (word, b, undo_word, b, c, undo_word, b, "leaves" if plus else "makes", s),
            "The left side is now just %d x. The right side is %d %s %d, which is %d." % (a, c, undo_word, b, s),
        ]), W("l2", "%dx = %d %s %d" % (a, c, undo_sign, b)), W("l3", "%dx = %d" % (a, s))),
        B(pick(qid, "q2", [
            "Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
            "Now %d x is %d lots of x. How do we get from %d lots down to just one?" % (a, a, a),
        ]), ask=choose(c2, right2,
                       "Times and divide are partners. Whatever times does, divide undoes. So to undo times %d, we divide by %d." % (a, a))),
        B("So we divide both sides by %d." % a, DIV("l3", str(a))),
        B(pick(qid, "a", [
            "%d divided by %d is %d. So x equals %d. There is our hidden number!" % (s, a, x, x),
            "%d shared into %d equal parts gives %d each. So x equals %d. Found it!" % (s, a, x, x),
        ]), ANS("l4", "x = %d" % x), M("l4", "x = %d" % x, "circle")),
        B(pick(qid, "k", [
            "Good mathematicians always check. Put %d back in place of x. %d times %d is %d, and %d %s %d is %d. It works." % (x, a, x, s, s, word, b, c),
            "Let's check it. With %d in place of x, %d times %d is %d. Then %d %s %d gives %d, just as the equation says." % (x, a, x, s, s, word, b, c),
        ]), W("l5", "%d × %d %s %d = %d" % (a, x, sign, b, c))),
        B(pick(qid, "s", [
            "So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times. Your turn next!",
            "Two moves, every time. Undo the plus or minus first, then undo the times. And always do the same to both sides.",
        ])),
    ]
    return lesson(*beats, origin="rule", check=("x", x))
