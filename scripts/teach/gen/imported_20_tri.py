"""Builder for triangle lessons where every angle is described using one unknown angle x.

xsum() writes the angles with x, makes them add up to 180, and solves, computing every
number. The caller supplies the story, and what the question asks once x is known.
"""
from imported_20_lib import (B, LESSON, G, W, Lb, A, C, X, DIV, GROUP, T, F, bar, bars, seg, nth_at,
                             ask_180, FACT)


def tx(k, c):
    s = "x" if k == 1 else "%dx" % k
    return s + (" + %d" % c if c else "")


def tsay(k, c):
    s = "x" if k == 1 else "%d x" % k
    return s + (" plus %d" % c if c else "")


def xsum(qid, intro, givens, terms, name_say, after, answer, answer_say, summary, checked=False):
    """terms: [(k, c, name)] in the order they are written, each angle being kx + c."""
    K = sum(k for k, c, nm in terms)
    Cc = sum(c for k, c, nm in terms)
    R = 180 - Cc
    assert R % K == 0
    x = R // K
    vals = [k * x + c for k, c, nm in terms]
    assert sum(vals) == 180
    line = W if checked else Lb

    # The equation, remembering where each x-term sits.
    e1 = ""
    targets = []
    for i, (k, c, nm) in enumerate(terms):
        if i:
            e1 += " + "
        xt = tx(k, 0)
        targets.append(T(xt, nth_at(e1 + xt, xt, len(e1))))
        e1 += tx(k, c)
    e1 += " = 180"
    for t in targets:  # nth must be counted on the finished line
        assert e1.count(t["text"]) >= t.get("nth", 1)

    fig = F(bars(*[bar(nm, [seg("x") for _ in range(k)] + ([seg("%d°" % c, 0.7, "c")] if c else [])) for k, c, nm in terms],
                 note="The three angles together make the whole triangle"))
    beats = [
        B(intro, *[G("g%d" % (i + 1), g) for i, g in enumerate(givens)]),
        B(name_say, Lb("n", "Angles: " + ", ".join(tx(k, c) for k, c, nm in terms)), fig),
        ask_180(qid),
        B("So our three angles together make 180: %s." % ", plus ".join(tsay(k, c) for k, c, nm in terms), FACT(), line("e1", e1)),
    ]
    e2 = "%dx + %d = 180" % (K, Cc) if Cc else "%dx = 180" % K
    count = " and ".join(str(k) for k, c, nm in terms)
    beats.append(B("Count the x's: %s make %d x. So %d x%s equals 180." % (count, K, K, " plus %d" % Cc if Cc else ""),
                   GROUP("e1", targets, "%dx" % K), line("e2", e2)))
    last = "e2"
    if Cc:
        e3 = "%dx = %d" % (K, R)
        beats.append(B("To undo plus %d, we take %d from both sides. 180 minus %d is %d, so %d x is %d." % (Cc, Cc, Cc, R, K, R),
                       X("e2", "+ %d" % Cc, "− %d" % Cc), W("w1", "180 − %d = %d" % (Cc, R)), line("e3", e3)))
        last = "e3"
    beats.append(B("%d x means %d times x, so we divide both sides by %d. %d divided by %d is %d, so x is %d degrees." % (K, K, K, R, K, x, x),
                   DIV(last, K), W("w2", "%d ÷ %d = %d" % (R, K, x))))
    beats += list(after)
    text, mark = answer
    beats.append(B(answer_say, A("ans", text), C("ans", mark)))
    beats.append(B("Check: %s is 180. The three angles fit a triangle." % " plus ".join(str(v) for v in vals),
                   W("csum", "%s = 180" % " + ".join(str(v) for v in vals))))
    beats.append(B(summary))
    return LESSON(beats, {"variable": "x", "value": str(x)} if checked else None)
