"""Builders for number-series lessons that share a structure. Every board line is computed.

    ap    a steady step (add or take away the same number), with gaps anywhere
    odd   a steady step with one number that does not fit
    geo   multiply or divide by the same number each time
    grow  the jump itself grows or shrinks by a steady amount
"""
from imported_17_lib import (B, CHOOSE, CIRC, LB, LESSON, MINUS, Series, UL, W, pick, say_list)

GAP = "__"


def _place(qid, salt, right, others):
    at = pick(qid, salt, list(range(len(others) + 1)))
    choices = list(others)
    choices.insert(at, right)
    return choices, at


def ap(qid, shown, full, intro, wrong_rules, summary, ask2=None, closing=None, answer_text=None, extra=None):
    """shown: the series as printed, GAP for each blank. full: the whole series."""
    n = len(full)
    d = full[1] - full[0]
    assert all(full[i + 1] - full[i] == d for i in range(n - 1)), qid
    assert len(shown) == n and all(s == GAP or int(s) == full[i] for i, s in enumerate(shown)), qid
    up = d > 0
    D = abs(d)
    rule = ("add %d" if up else "take away %d") % D
    step_word = "plus" if up else "minus"
    back_word = "minus" if up else "plus"
    sgn, inv = ("+", MINUS) if up else (MINUS, "+")
    blanks = [i for i, s in enumerate(shown) if s == GAP]
    known = [i for i in range(n - 1) if shown[i] != GAP and shown[i + 1] != GAP]
    p0 = known[0]
    p1 = known[1] if len(known) > 1 else None
    a, b = full[p0], full[p0 + 1]
    s = Series("s", shown)

    def diff_line(id, lo, hi):
        big, small = (hi, lo) if up else (lo, hi)
        return W(id, "%d %s %d = %d" % (big, MINUS, small, D)), "%d minus %d is %d" % (big, small, D)

    beats = [B(intro, s.given())]
    choices, at = _place(qid, "rule", rule, wrong_rules)
    if up:
        if_not = "Look at %d and %d again. %d is bigger than %d by %d, so the step is %s." % (a, b, b, a, D, rule)
    else:
        if_not = "Look at %d and %d again. %d is smaller than %d by %d, so the step is %s." % (a, b, b, a, D, rule)
    beats.append(B(pick(qid, "askrule", [
        "Pick two neighbours we can see, %d and %d. How do we get from %d to %d?" % (a, b, a, b),
        "Start with %d and %d, sitting side by side. What takes us from %d to %d?" % (a, b, a, b),
        "Look at %d and then %d. What has been done to %d to make %d?" % (a, b, a, b),
    ]), ask=CHOOSE(choices, at, if_not)))

    l1, s1 = diff_line("d1", a, b)
    hop = "%s%d" % (sgn, D)
    if p1 is None:
        end = full[-1]
        beats.append(B("%s, so the rule looks like %s. We only have one pair to go on, so we will test the rule "
                       "when we reach %d at the far end." % (s1, rule, end), l1, s.note(p0 + 1, hop)))
    else:
        l2, s2 = diff_line("d2", full[p1], full[p1 + 1])
        beats.append(B(pick(qid, "rule", [
            "%s. One pair is never enough, so try another: %s as well. The rule is %s, every time.",
            "%s. Let's not trust a single pair: %s too. So the rule is %s, all the way along.",
        ]) % (s1, s2, rule), l1, l2, s.note(p0 + 1, hop), s.note(p1 + 1, hop)))

    values = {}
    for j, i in enumerate(blanks):
        if ask2 and ask2["before"] == j:
            beats.append(B(ask2["say"], ask=CHOOSE(ask2["choices"], ask2["answer"], ask2["ifNot"])))
        v = full[i]
        ops = []
        which = "" if len(blanks) == 1 else ["first ", "second "][j]
        if i > 0:
            prev = full[i - 1]
            ops.append(W("f%d" % j, "%d %s %d = %d" % (prev, sgn, D, v)))
            if ask2 and ask2["before"] == j and i - 1 not in blanks:
                say = "%d %s %d is %d." % (prev, step_word, D, v)
            elif i - 1 in blanks:
                say = "We have just found %d, and the %sgap comes straight after it. %d %s %d is %d." % (
                    prev, which, prev, step_word, D, v)
            elif len(blanks) == 1 and i == n - 1:
                say = "The last number we can see is %d. %d %s %d is %d." % (prev, prev, step_word, D, v)
            else:
                say = "The number just before the %sgap is %d. %d %s %d is %d." % (which, prev, prev, step_word, D, v)
        else:
            nxt = full[1]
            ops.append(W("f%d" % j, "%d %s %d = %d" % (nxt, inv, D, v)))
            say = "The %sgap is at the very front, so we walk backwards and undo the step. %d %s %d is %d." % (
                which, nxt, back_word, D, v)
        if i > 0 and i + 1 < n and shown[i + 1] != GAP:
            nxt = full[i + 1]
            ops.append(W("c%d" % j, "%d %s %d = %d" % (v, sgn, D, nxt)))
            say += " And %d %s %d is %d, the number that follows, so it fits." % (v, step_word, D, nxt)
        values[i] = v
        beats.append(B(say, *ops))

    last = blanks[-1]
    if last == n - 1 and last > 0:
        v, prev = full[last], full[last - 1]
        beats.append(B(pick(qid, "back", [
            "Check by walking backwards: %d %s %d is %d, right where we came from.",
            "A quick check by undoing the step: %d %s %d is %d. It fits.",
        ]) % (v, back_word, D, prev), W("k1", "%d %s %d = %d" % (v, inv, D, prev))))

    done = Series("a", full if answer_text is None else [answer_text.get(i, t) for i, t in enumerate(full)])
    found = [done.terms[i] for i in blanks]
    if closing is None:
        closing = ("So the missing number is %s." if len(found) == 1 else "So the missing numbers are %s.") % say_list(found)
    beats.append(B(closing, done.label("answer"), *[done.mark(i) for i in blanks]))
    for e in extra or []:
        beats.append(e)
    beats.append(B(summary))
    return LESSON(*beats)


def odd(qid, terms, bad, intro, wrong_rules, culprits, summary, rule_say=None):
    n = len(terms)
    d = terms[1] - terms[0]
    right = terms[bad - 1] + d
    fixed = list(terms)
    fixed[bad] = right
    assert bad >= 3 and all(fixed[i + 1] - fixed[i] == d for i in range(n - 1)) and terms[bad] != right, qid
    s = Series("s", terms)
    beats = [B(intro, s.given())]
    a, b, c = terms[0], terms[1], terms[2]
    choices, at = _place(qid, "rule", "add %d" % d, wrong_rules)
    beats.append(B("Start at the front, with %d and %d. How do we get from %d to %d?" % (a, b, a, b),
                   ask=CHOOSE(choices, at, "Look at %d and %d again. %d is %d more than %d, so the step is add %d." % (a, b, b, d, a, d))))
    beats.append(B(rule_say or ("%d minus %d is %d, and %d minus %d is %d. So this series wants to go up by %d each time. "
                                "Now we test every jump." % (b, a, d, c, b, d, d)),
                   W("d1", "%d %s %d = %d" % (b, MINUS, a, d)), W("d2", "%d %s %d = %d" % (c, MINUS, b, d)),
                   s.note(1, "+%d" % d), s.note(2, "+%d" % d)))
    ops = []
    bits = []
    for i in range(2, n - 1):
        diff = terms[i + 1] - terms[i]
        lid = "d%d" % (i + 1)
        line = "%d %s %d = %d" % (terms[i + 1], MINUS, terms[i], diff)
        ops.append(W(lid, line))
        if diff != d:
            ops.append(UL(lid, "= %d" % diff))
        bits.append(("%d minus %d is %d" if diff == d else "%d minus %d is %d, not %d") % (
            (terms[i + 1], terms[i], diff) if diff == d else (terms[i + 1], terms[i], diff, d)))
    if bad == n - 1:
        tail = "Every jump is %d until the very last one." % d
    else:
        tail = "Two jumps, side by side, do not fit."
    beats.append(B("Carry on along the line. %s. %s" % ("; ".join(bits).capitalize(), tail), *ops))
    cs, at2 = _place(qid, "culprit", str(terms[bad]), [str(x) for x in culprits])
    if bad == n - 1:
        if_not = "Every number up to %d follows the rule. The first jump that breaks it lands on %d, so %d is the one to look at." % (
            terms[bad - 1], terms[bad], terms[bad])
    else:
        if_not = "Both of the jumps that do not fit touch %d. %d and %d get on perfectly well with their other neighbours." % (
            terms[bad], terms[bad - 1], terms[bad + 1])
    beats.append(B("So which number is spoiling the pattern?", ask=CHOOSE(cs, at2, if_not)))
    ops = [W("r1", "%d + %d = %d" % (terms[bad - 1], d, right))]
    say = "What should stand there? %d plus %d is %d." % (terms[bad - 1], d, right)
    if bad < n - 1:
        ops.append(W("r2", "%d + %d = %d" % (right, d, terms[bad + 1])))
        say += " And %d plus %d is %d, exactly the number that follows. So %d belongs there." % (right, d, terms[bad + 1], right)
    else:
        say += " The series should end on %d." % right
    ops.append(s.strike(bad, str(right)))
    beats.append(B(say, *ops))
    ans = "Odd one out: %d" % terms[bad]
    beats.append(B("So the odd one out, the number that does not belong, is %d." % terms[bad],
                   LB("a", ans, "answer"), CIRC("a", str(terms[bad]))))
    beats.append(B(summary))
    return LESSON(*beats)


def geo(qid, terms, op, r, intro, wrong_rules, next_wrong, next_if_not, summary):
    n = len(terms)
    times = op == "×"
    for i in range(n - 1):
        assert (terms[i] * r == terms[i + 1]) if times else (terms[i + 1] * r == terms[i]), qid
    nxt = terms[-1] * r if times else terms[-1] // r
    s = Series("s", list(terms) + [GAP])
    a, b, c = terms[0], terms[1], terms[2]
    opw = "times" if times else "divided by"
    rule = ("multiply by %d" if times else "divide by %d") % r
    beats = [B(intro, s.given())]
    hi = lambda x, y: (max(x, y), min(x, y))
    j1 = abs(b - a)
    j2 = abs(c - b)
    beats.append(B("First the usual test: how big is the jump between neighbours? %d minus %d is %d, but %d minus %d is %d. "
                   "The jumps are not equal, so this series does not %s the same number each time." % (
                       hi(a, b) + (j1,) + hi(b, c) + (j2, "add" if times else "take away")),
                   W("j1", "%d %s %d = %d" % (hi(a, b)[0], MINUS, hi(a, b)[1], j1)),
                   W("j2", "%d %s %d = %d" % (hi(b, c)[0], MINUS, hi(b, c)[1], j2))))
    choices, at = _place(qid, "rule", rule, wrong_rules)
    beats.append(B("So try another idea. What turns %d into %d, and then %d into %d?" % (a, b, b, c),
                   ask=CHOOSE(choices, at, "Try it out: %d %s %d is %d, and %d %s %d is %d. The same move works both times: %s." % (
                       a, opw, r, b, b, opw, r, c, rule))))
    ops = []
    bits = []
    for i in range(min(3, n - 1)):
        ops.append(W("m%d" % (i + 1), "%d %s %d = %d" % (terms[i], op, r, terms[i + 1])))
        bits.append("%d %s %d is %d" % (terms[i], opw, r, terms[i + 1]))
    ops.append(s.note(1, "%s%d" % (op, r)))
    ops.append(s.note(2, "%s%d" % (op, r)))
    beats.append(B("%s, and %s. Each number is the one before it, %s %d." % (", ".join(bits[:-1]), bits[-1], opw, r), *ops))
    cs, at2 = _place(qid, "next", str(nxt), [str(x) for x in next_wrong])
    beats.append(B("The last number we can see is %d. What comes after it?" % terms[-1],
                   ask=CHOOSE(cs, at2, next_if_not)))
    line = "%d %s %d = %d" % (terms[-1], op, r, nxt)
    beats.append(B("%d %s %d is %d. So the next number in the series is %d." % (terms[-1], opw, r, nxt, nxt),
                   W("a", line, "answer"), CIRC("a", "= %d" % nxt)))
    inv, invw = ("÷", "divided by") if times else ("×", "times")
    beats.append(B("Check by undoing the move: %d %s %d is %d, back where we were." % (nxt, invw, r, terms[-1]),
                   W("k", "%d %s %d = %d" % (nxt, inv, r, terms[-1]))))
    beats.append(B(summary))
    return LESSON(*beats)


def grow(qid, terms, count, intro, jump_wrong, summary, trap=None):
    """The jumps themselves change by a steady amount. `count` new numbers are wanted."""
    n = len(terms)
    jumps = [terms[i + 1] - terms[i] for i in range(n - 1)]
    dd = jumps[1] - jumps[0]
    assert all(jumps[i + 1] - jumps[i] == dd for i in range(len(jumps) - 1)) and dd != 0, qid
    s = Series("s", list(terms) + [GAP] * count)
    beats = [B(intro, s.given())]

    def jl(i):
        return W("j%d" % (i + 1), "%d %s %d = %d" % (terms[i + 1], MINUS, terms[i], jumps[i])), \
            "%d minus %d is %d" % (terms[i + 1], terms[i], jumps[i])

    first = [jl(i) for i in range(2)]
    beats.append(B("Measure the jump between neighbours. %s, but %s. The jumps are not equal, so there is no single number to add." % (
        first[0][1].capitalize(), first[1][1]), first[0][0], first[1][0]))
    rest = [jl(i) for i in range(2, n - 1)]
    jl_text = "Jumps: " + ", ".join(str(j) for j in jumps)
    beats.append(B("Don't stop there. Measure the rest: %s. Now look at the jumps on their own: %s." % (
        ", ".join(r[1] for r in rest[:-1]) + ", and " + rest[-1][1], say_list(jumps)), *([r[0] for r in rest] + [LB("jj", jl_text)])))
    nj = jumps[-1] + dd
    more = "%d more" % dd if dd > 0 else "%d less" % (-dd)
    cs, at = _place(qid, "jump", str(nj), [str(x) for x in jump_wrong])
    beats.append(B("The jumps have a pattern of their own. What will the next jump be?",
                   ask=CHOOSE(cs, at, "Read the jumps in order: %s. Each jump is %s than the one before, so after %d comes %d." % (
                       say_list(jumps), more, jumps[-1], nj))))
    new = []
    cur = terms[-1]
    for k in range(count):
        j = jumps[-1] + dd * (k + 1)
        v = cur + j
        if k == 0:
            say = "Each jump is %s than the last, so the next jump is %d. %d plus %d is %d." % (more, j, cur, j, v)
        else:
            say = (trap or "Careful: the jump does not stay at %d. It changes again, to %d.") % (j - dd, j) + " %d plus %d is %d." % (cur, j, v)
        beats.append(B(say, W("n%d" % (k + 1), "%d + %d = %d" % (cur, j, v))))
        new.append(v)
        cur = v
    done = Series("a", list(terms) + new)
    all_jumps = jumps + [jumps[-1] + dd * (k + 1) for k in range(count)]
    closing = ("So the next number is %s." if count == 1 else "So the next two numbers are %s.") % say_list(new)
    beats.append(B(closing + " And the jumps run %s, with no break in their pattern." % say_list(all_jumps),
                   done.label("answer"), *([done.mark(n + k) for k in range(count)] +
                                           [LB("jk", "Jumps: " + ", ".join(str(j) for j in all_jumps))])))
    beats.append(B(summary))
    return LESSON(*beats)
