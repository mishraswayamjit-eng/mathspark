"""Builders for the sharing-in-a-ratio lessons of imported-20.

split()  a total shared in a ratio: count the parts, find one part, multiply for
         the share(s) needed; the caller adds whatever the story asks after that.
chain()  two ratios joined by one person, with one real amount known.
Every number written or said is computed here from the question's numbers.
"""
from imported_20_lib import (B, LESSON, G, W, Lb, A, U, C, N, F, bar, bars, seg, pick, choose_at,
                             fmt, parts, say_list, nth_at)


def shares(total, ratio):
    s = sum(ratio)
    assert total % s == 0, (total, ratio)
    one = total // s
    return s, one, [r * one for r in ratio]


def ratio_line(names, ratio):
    return " : ".join(names) + " = " + " : ".join(str(r) for r in ratio)


def ratio_marks(line_id, text, ratio):
    """Underline each ratio number on the ratio line."""
    ops = []
    pos = text.index("=") + 2
    for r in ratio:
        s = str(r)
        ops.append(U(line_id, s, nth_at(text, s, pos)))
        pos += len(s) + 3
    return ops


SUMMARIES = [
    "So the plan for sharing in a ratio: add the ratio numbers to count the parts, divide the total to find one part, then multiply by the parts you need.",
    "So remember three moves: count the parts, find one part, multiply for the share. Then do whatever else the story asks.",
    "So every time: total parts first, then the size of one part, then the share. And read the last line of the story to see what is still left to do.",
]


def split(qid, intro, names, ratio, total, unit, need, answer, answer_say, givens=(), spoken=None, pre=None,
          own=None, got=None, both_say=None, ask_share=True, tail=(), check=None, summary=None, sym=""):
    spoken = spoken or names
    S, one, sh = shares(total, ratio)
    n = len(ratio)

    def amt(v):
        return "%s %s" % (fmt(v), unit)

    rline = ratio_line(names, ratio)
    assert len(rline) <= 60, rline
    beats = []

    # 1. The question.
    ops = [G("g%d" % (i + 1), g) for i, g in enumerate(givens)]
    if not pre:
        ops.append(G("r", rline))
    beats.append(B(intro, *ops))

    # A ratio that has to be made simpler first.
    if pre:
        x, y, g = pre["x"], pre["y"], pre["g"]
        assert (x // g, y // g) == tuple(ratio) and x % g == 0 and y % g == 0
        a, b = ratio
        beats.append(B(pre["lead"], Lb("r0", "%s : %s = %d : %d" % (names[0], names[1], x, y))))
        beats.append(B("Those numbers can be made simpler. What is the biggest number that divides both %d and %d exactly?" % (x, y),
                       ask=choose_at(qid, "g", str(g), pre["others"],
                                     ("%d is %d times %d, and %d is %d times %d. Nothing bigger goes into both." % (x, a, g, y, b, g)) if b != 1 else
                                     ("%d is %d times %d, and %d goes into itself once. Nothing bigger goes into both." % (x, a, g, y)))))
        beats.append(B("%d divided by %d is %d, and %d divided by %d is %d. So %d to %d is the same ratio as %d to %d, just in smaller numbers." % (
            x, g, a, y, g, b, x, y, a, b),
            W("d1", "%d ÷ %d = %d" % (x, g, a)), W("d2", "%d ÷ %d = %d" % (y, g, b)), Lb("r", rline)))

    # 2. The ratio as equal parts, with a picture.
    each = say_list(["%s for %s" % (parts(r), nm) for r, nm in zip(ratio, spoken)])
    to = " to ".join(str(r) for r in ratio)
    fig = F(bars(*[bar(nm, [seg(tone="abc"[i]) for _ in range(r)]) for i, (r, nm) in enumerate(zip(ratio, names))],
                 note="All the boxes together: %s%s%s" % (sym, fmt(total), "" if sym else " " + unit)))
    beats.append(B(pick(qid, "p2", [
        "A ratio of %s means equal parts: %s. Here they are as boxes." % (to, each),
        "Read the ratio as parts: %s, and every part is the same size. Look at the boxes." % each,
        "Think of the ratio as equal boxes: %s." % each,
    ]), fig, *ratio_marks("r", rline, ratio)))

    # 3. Ask: how many parts?
    wrong = []
    for cand in [max(ratio), n, ratio[0] * ratio[1], min(ratio), S + 1]:
        if cand != S and cand not in wrong:
            wrong.append(cand)
    plus_words = " and ".join(str(r) for r in ratio)
    beats.append(B(pick(qid, "p3", [
        "So how many equal parts are there altogether?",
        "First job: how many equal parts are there in all?",
        "Before sharing anything, count. How many equal parts altogether?",
    ]), ask=choose_at(qid, "p3c", parts(S), [parts(w) for w in wrong[:2]],
                      "Count the boxes in all the rows together: %s make %d parts." % (plus_words, S))))

    # 4. Total parts.
    plus_say = " plus ".join(str(r) for r in ratio)
    beats.append(B(pick(qid, "p4", [
        "%s is %d. So the %s are shared into %d equal parts." % (plus_say, S, amt(total), S),
        "Add the ratio numbers: %s makes %d. All %s sit in those %d equal parts." % (plus_say, S, amt(total), S),
    ]), W("p", "%s = %d" % (" + ".join(str(r) for r in ratio), S))))

    # 5. One part.
    oline = "%s ÷ %d = %s" % (fmt(total), S, fmt(one))
    beats.append(B("To find one part, we divide: %s divided by %d is %s, so each part is %s. %s" % (
        fmt(total), S, fmt(one), amt(one), pick(qid, "p5", [
            "Careful: we divide by all %d parts, not by one of the ratio numbers on its own." % S,
            "The classic slip is to divide by just one ratio number, but the total belongs to all %d parts." % S,
        ])), W("o", oline), N("o", fmt(one), "1 part", "below", nth_at(oline, fmt(one), oline.rindex(fmt(one))))))

    # 6. The share, or shares.
    if len(need) == 1:
        i = need[0]
        f, sf = ratio[i], sh[i]
        own_i = own or "%s has %s" % (spoken[i], parts(f))
        got_i = got or "%s gets %s" % (spoken[i], amt(sf))
        line = W("s%d" % i, "%d × %s = %s" % (f, fmt(one), fmt(sf)))
        if ask_share and not pre:
            o = max(r for k, r in enumerate(ratio) if k != i and r != f)
            beats.append(B("%s. Which sum gives that share?" % own_i,
                           ask=choose_at(qid, "p6", "%d × %s" % (f, fmt(one)), ["%s ÷ %d" % (fmt(total), f), "%d × %s" % (o, fmt(one))],
                                         "%s. One part is %s, so we want %d lots of %s." % (own_i, amt(one), f, fmt(one)))))
            beats.append(B("%d times %s is %s. So %s." % (f, fmt(one), fmt(sf), got_i), line))
        else:
            beats.append(B("%s, and each part is %s. %d times %s is %s, so %s." % (own_i, amt(one), f, fmt(one), fmt(sf), got_i), line))
    else:
        ops = [W("s%d" % i, "%d × %s = %s" % (ratio[i], fmt(one), fmt(sh[i]))) for i in need]
        beats.append(B(both_say or " ".join("%s has %s: %d times %s is %s." % (spoken[i], parts(ratio[i]), ratio[i], fmt(one), fmt(sh[i])) for i in need), *ops))

    # 7. Whatever else the story asks.
    beats += list(tail)

    # 8. The answer.
    text, mark = answer
    beats.append(B(answer_say, A("ans", text), C("ans", mark)))

    # 9. Check the sharing.
    if check:
        beats += list(check)
    else:
        rest = [k for k in range(n) if k not in need]
        sum_line = "%s = %s" % (" + ".join(fmt(v) for v in sh), fmt(total))
        sum_say = "%s is %s, the whole amount" % (" plus ".join(fmt(v) for v in sh), fmt(total))
        if rest:
            words = " and ".join("%s has %s, and %d times %s is %s" % (spoken[k], parts(ratio[k]), ratio[k], fmt(one), fmt(sh[k])) for k in rest)
            ops = [W("c%d" % k, "%d × %s = %s" % (ratio[k], fmt(one), fmt(sh[k]))) for k in rest] + [W("csum", sum_line)]
            beats.append(B("Check the sharing. %s. %s, so the shares are right." % (words[0].upper() + words[1:], sum_say), *ops))
        else:
            beats.append(B("Check the sharing: %s. The shares are right." % sum_say, W("csum", sum_line)))

    # 10. The method in one line.
    beats.append(B(summary or pick(qid, "sum", SUMMARIES)))
    return LESSON(beats)


def diff_tail(qid, question, sb, ss, ask=True):
    """Two beats (or one): the gap between two shares already on the board."""
    d = sb - ss
    line = W("t1", "%s − %s = %s" % (fmt(sb), fmt(ss), fmt(d)))
    if not ask:
        return [B("%s That is the gap between the two shares, so we take the smaller from the bigger: %s minus %s is %s." % (
            question, fmt(sb), fmt(ss), fmt(d)), line)]
    return [
        B("%s What do we do with %s and %s?" % (question, fmt(sb), fmt(ss)),
          ask=choose_at(qid, "diff", "%s − %s" % (fmt(sb), fmt(ss)), ["%s + %s" % (fmt(sb), fmt(ss)), "stop at %s" % fmt(sb)],
                        "How much more asks for the gap between the two shares. To find a gap, take the smaller from the bigger: %s minus %s." % (fmt(sb), fmt(ss)))),
        B("%s minus %s is %s. That gap is what the question wants." % (fmt(sb), fmt(ss), fmt(d)), line),
    ]


def diff_check(big, small, ra, rb, one, d):
    """Check a gap another way: the gap in parts times one part."""
    k = ra - rb
    if k == 1:
        return [B("Check it another way. %s has just 1 part more than %s, and 1 part is %s. The same answer, so we can trust it." % (big, small, fmt(one)),
                  W("c1", "%d − %d = 1" % (ra, rb)), W("c2", "1 × %s = %s" % (fmt(one), fmt(d))))]
    return [B("Check it another way. %s has %d parts more than %s, and %d times %s is %s. The same answer, so we can trust it." % (
        big, k, small, k, fmt(one), fmt(d)),
        W("c1", "%d − %d = %d" % (ra, rb, k)), W("c2", "%d × %s = %s" % (k, fmt(one), fmt(d))))]


def chain(qid, intro, names, r1, r2, known, value, unit, sym, answer_text, answer_say):
    """names = (A, B, C); r1 is A : B, r2 is B : C; known is 0 (A) or 2 (C)."""
    A_, B_, C_ = names
    a, b = r1
    c, d = r2
    l1 = ratio_line([A_, B_], r1)
    l2 = ratio_line([B_, C_], r2)

    def amt(v):
        return "%s %s" % (fmt(v), unit)

    if known == 0:
        first, f_id, f_text, kn, k_parts, b_parts = (A_, B_), "r1", l1, A_, a, b
        second, s_id, s_text, b_parts2, t_parts, target = (B_, C_), "r2", l2, c, d, C_
    else:
        first, f_id, f_text, kn, k_parts, b_parts = (B_, C_), "r2", l2, C_, d, c
        second, s_id, s_text, b_parts2, t_parts, target = (A_, B_), "r1", l1, b, a, A_
    assert value % k_parts == 0
    one1 = value // k_parts
    bv = b_parts * one1
    assert bv % b_parts2 == 0
    one2 = bv // b_parts2
    tv = t_parts * one2
    first_name = "%s : %s" % first
    second_name = "%s : %s" % second

    beats = [
        B(intro, G("r1", l1), G("r2", l2), G("k", "%s = %s%s%s" % (kn, sym, fmt(value), "" if sym else " " + unit))),
        B("Notice that %s is in both ratios, and that makes a bridge between %s and %s. But careful: the parts in one ratio are not the same size as the parts in the other." % (
            B_, A_, C_), U("r1", B_), U("r2", B_)),
        B("We know a real number for %s. So which ratio do we start with?" % kn,
          ask=choose_at(qid, "start", first_name, [second_name],
                        "Start where you know a real number. %s is in the ratio %s to %s, so we begin there." % (kn, first[0], first[1]))),
        B("In that ratio %s has %s, and those are worth %s. So one part is %s divided by %d, which is %s." % (
            kn, parts(k_parts), amt(value), fmt(value), k_parts, fmt(one1)),
          W("o1", "%s ÷ %d = %s" % (fmt(value), k_parts, fmt(one1)))),
        B("%s has %d of those parts. %d times %s is %s, so %s has %s." % (B_, b_parts, b_parts, fmt(one1), fmt(bv), B_, amt(bv)),
          W("b", "%d × %s = %s" % (b_parts, fmt(one1), fmt(bv)))),
        B("Now cross the bridge to the other ratio. There, %s has %s, and we know %s has %s. What is one part this time?" % (
            B_, parts(b_parts2), B_, fmt(bv)),
          ask=choose_at(qid, "one2", "%s ÷ %d" % (fmt(bv), b_parts2), ["%s ÷ %d" % (fmt(bv), t_parts), "%s ÷ %d" % (fmt(value), b_parts2)],
                        "In the ratio %s to %s, the %s belong to %s, who has %s. So one part is %s divided by %d." % (
                            second[0], second[1], fmt(bv), B_, parts(b_parts2), fmt(bv), b_parts2))),
        B("%s divided by %d is %s. See how these parts are a different size from the first ones? That is why we could not mix the two ratios." % (
            fmt(bv), b_parts2, fmt(one2)), W("o2", "%s ÷ %d = %s" % (fmt(bv), b_parts2, fmt(one2)))),
        B("%s has %s in this ratio. %d times %s is %s." % (target, parts(t_parts), t_parts, fmt(one2), fmt(tv)),
          W("t", "%d × %s = %s" % (t_parts, fmt(one2), fmt(tv)))),
        B(answer_say, A("ans", answer_text), C("ans", sym + fmt(tv))),
    ]
    va, vc = (value, tv) if known == 0 else (tv, value)
    g1, g2 = va // a, bv // c
    assert va == a * g1 and bv == b * g1 and bv == c * g2 and vc == d * g2
    beats.append(B("Check both ratios. %s to %s: divide both by %s and you get %d to %d. %s to %s: divide both by %s and you get %d to %d." % (
        fmt(va), fmt(bv), fmt(g1), a, b, fmt(bv), fmt(vc), fmt(g2), c, d),
        W("c1", "%s ÷ %s = %d" % (fmt(va), fmt(g1), a)), W("c2", "%s ÷ %s = %d" % (fmt(bv), fmt(g1), b)),
        W("c3", "%s ÷ %s = %d" % (fmt(bv), fmt(g2), c)), W("c4", "%s ÷ %s = %d" % (fmt(vc), fmt(g2), d))))
    beats.append(B("So when one person sits in two ratios, use them as a bridge: find their real number from the ratio you know, then carry it into the other ratio."))
    return LESSON(beats), tv
