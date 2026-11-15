"""Small helpers shared by the money-percent lesson scripts (rules and hand-written lessons).

A lesson is built from beats; a beat is what the teacher says plus what the board does.
Nothing here knows any maths answers: the rules compute them, the checker verifies them.
"""
import hashlib
from fractions import Fraction


# ── Numbers, written and spoken ──────────────────────────────────────────────

def F(x):
    return x if isinstance(x, Fraction) else Fraction(str(x))


def num(x):
    """A number as it is written on the board: 25, 12.5, 0.25."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = ("%.4f" % float(x)).rstrip("0")
    return s


def rs(x):
    """Rupees on the board: Rs.250, Rs.12.50."""
    x = F(x)
    if x.denominator == 1:
        return "Rs.%d" % x.numerator
    return "Rs.%.2f" % float(x)


def sp(x):
    """A number as the teacher says it: 25, 12.5 (the voice reads 'twelve point five'), 0.25."""
    return num(x)


def rupees(x):
    """'250 rupees', '1 rupee', '12 and a half rupees'."""
    x = F(x)
    return "1 rupee" if x == 1 else "%s rupees" % sp(x)


# ── Stable variety ───────────────────────────────────────────────────────────

def pick(qid, salt, options):
    """One of `options`, always the same one for the same question and salt."""
    h = int(hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def GIVEN(id, text):
    """The question as printed: a line of words in dark ink."""
    return W(id, text, tone="given", label=True)


def ANSWER(id, text, label=True):
    return W(id, text, tone="answer", label=label)


def _target(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def MARK(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def RING(line, text, nth=None):
    return MARK(line, text, "circle", nth)


def BOX(line, text, nth=None):
    return MARK(line, text, "box", nth)


def NOTE(line, text, note, place=None, nth=None):
    op = {"op": "note", "line": line, "target": _target(text, nth), "text": note}
    if place:
        op["place"] = place
    return op


def STRIKE(line, text, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _target(text, nth)}
    if note:
        op["note"] = note
    return op


def GROUP(line, texts, label=None):
    op = {"op": "group", "line": line, "targets": [_target(t) for t in texts]}
    if label:
        op["label"] = label
    return op


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _target(frm), "to": [_target(t) for t in to]}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


# ── Figures ──────────────────────────────────────────────────────────────────

def seg(units, label=None, tone=None):
    s = {"units": units}
    if label:
        s["label"] = label
    if tone:
        s["tone"] = tone
    return s


def bar(segments, label=None, brace=None):
    b = {"segments": segments}
    if label:
        b["label"] = label
    if brace:
        b["brace"] = brace
    return b


def bars(*the_bars, **extra):
    spec = {"kind": "barModel", "bars": list(the_bars)}
    spec.update(extra)
    return spec


def table(headers, rows, **extra):
    spec = {"kind": "table", "rows": rows}
    if headers:
        spec["headers"] = headers
    spec.update(extra)
    return spec


def two_bars(cp_label, sp_label, gap_label, percent, profit=True, note=None, hl=False):
    """Cost price over selling price, with the gap between them named."""
    gap = max(1.2, percent / 10.0)
    if profit:
        top = bar([seg(10, cp_label, "a")], "Cost price")
        bottom = bar([seg(10, None, "a"), seg(gap, gap_label, "b")], "Selling price", sp_label)
        key = "b1s1"
    else:
        top = bar([seg(10 - gap, None, "a"), seg(gap, gap_label, "b")], "Cost price", cp_label)
        bottom = bar([seg(10 - gap, sp_label, "a")], "Selling price")
        key = "b0s1"
    extra = {"note": note} if note else {}
    if hl:
        extra["highlight"] = [key]
    return bars(top, bottom, **extra)


# ── Beats ────────────────────────────────────────────────────────────────────

def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


THINK = {"kind": "think"}


def choose(qid, salt, right, others, if_not):
    """A choose-ask with the right choice placed by a stable hash, so it is not always first."""
    n = len(others) + 1
    at = pick(qid, "at" + salt, list(range(n)))
    choices = list(others)
    choices.insert(at, right)
    return {"kind": "choose", "choices": choices, "answer": at, "ifNot": if_not}


def ASK(qid, salt, say, right, others, if_not, *ops):
    return B(say, *ops, ask=choose(qid, salt, right, others, if_not))


def lesson(beats, origin):
    return {"origin": origin, "beats": beats}


# ── Mental arithmetic, one true line at a time ───────────────────────────────

def percent_steps(qid, p, base, ids, what="", unit=""):
    """p% of base, worked the way a child does it in their head.

    Returns (value, steps, last_id). Each step is (say, [ops]); every op is a true maths line.
    `ids` is a prefix for line ids. `unit` is a spoken unit ('rupees', 'marks') or ''.
    """
    base = F(base)
    u = (" " + unit) if unit else ""
    steps = []
    tenth = base / 10

    def line(i, text):
        return W("%s%d" % (ids, i), text)

    if p == 50:
        v = base / 2
        steps.append((
            pick(qid, "p50", [
                "50 per cent is 50 out of every 100, and that is exactly one half. Half of %s is %s." % (sp(base), sp(v)),
                "50 out of every 100 is one half. So we just halve it: half of %s is %s." % (sp(base), sp(v)),
            ]),
            [line(1, "50%% of %s = %s ÷ 2 = %s" % (num(base), num(base), num(v)))]))
        return v, steps, ids + "1"
    if p in (25, 75):
        half = base / 2
        q = base / 4
        steps.append((
            pick(qid, "p25a", [
                "25 per cent is one quarter, because 4 lots of 25 make 100. To find a quarter, halve it, then halve it again. Half of %s is %s." % (sp(base), sp(half)),
                "4 lots of 25 make 100, so 25 per cent is one quarter. A quarter is half of a half. First, half of %s is %s." % (sp(base), sp(half)),
            ]),
            [line(1, "4 × 25 = 100"), line(2, "50%% of %s = %s" % (num(base), num(half)))]))
        steps.append((
            "And half of %s is %s. So 25 per cent of %s is %s%s." % (sp(half), sp(q), sp(base), sp(q), u),
            [line(3, "25%% of %s = %s ÷ 2 = %s" % (num(base), num(half), num(q)))]))
        if p == 25:
            return q, steps, ids + "3"
        v = 3 * q
        steps.append((
            "75 per cent is 3 quarters, so we need 3 lots of %s. 3 times %s is %s." % (sp(q), sp(q), sp(v)),
            [line(4, "75%% of %s = 3 × %s = %s" % (num(base), num(q), num(v)))]))
        return v, steps, ids + "4"

    # Everything else goes through 10%.
    if p == 10:
        steps.append((
            pick(qid, "p10only", [
                "10 per cent is a friendly one: it is one tenth. So we divide by 10. %s divided by 10 is %s." % (sp(base), sp(tenth)),
                "10 out of every 100 is one tenth. To find a tenth, divide by 10. %s divided by 10 is %s." % (sp(base), sp(tenth)),
            ]),
            [line(1, "10%% of %s = %s ÷ 10 = %s" % (num(base), num(base), num(tenth)))]))
        return tenth, steps, ids + "1"
    steps.append((
        pick(qid, "p10", [
            "Start with the friendly one, 10 per cent. 10 per cent is one tenth, so we divide by 10. %s divided by 10 is %s." % (sp(base), sp(tenth)),
            "10 per cent is the easy one: it is one tenth. %s divided by 10 is %s." % (sp(base), sp(tenth)),
            "First find 10 per cent. That is one tenth, so divide by 10. %s divided by 10 gives %s." % (sp(base), sp(tenth)),
        ]),
        [line(1, "10%% of %s = %s ÷ 10 = %s" % (num(base), num(base), num(tenth)))]))
    if p == 10:
        return tenth, steps, ids + "1"
    if p == 5:
        v = tenth / 2
        steps.append((
            "5 per cent is half of 10 per cent. Half of %s is %s." % (sp(tenth), sp(v)),
            [line(2, "5%% of %s = %s ÷ 2 = %s" % (num(base), num(tenth), num(v)))]))
        return v, steps, ids + "2"
    if p == 15:
        h = tenth / 2
        v = tenth + h
        steps.append((
            "5 per cent is half of 10 per cent. Half of %s is %s." % (sp(tenth), sp(h)),
            [line(2, "5%% of %s = %s ÷ 2 = %s" % (num(base), num(tenth), num(h)))]))
        steps.append((
            "15 per cent is 10 per cent and 5 per cent together. %s plus %s makes %s." % (sp(tenth), sp(h), sp(v)),
            [line(3, "15%% of %s = %s + %s = %s" % (num(base), num(tenth), num(h), num(v)))]))
        return v, steps, ids + "3"
    if p % 10 == 0:
        k = p // 10
        v = k * tenth
        steps.append((
            pick(qid, "pk", [
                "%d per cent is %d lots of 10 per cent. %d times %s is %s." % (p, k, k, sp(tenth), sp(v)),
                "Now, %d per cent is just 10 per cent, %d times over. %d times %s makes %s." % (p, k, k, sp(tenth), sp(v)),
            ]),
            [line(2, "%d%% of %s = %d × %s = %s" % (p, num(base), k, num(tenth), num(v)))]))
        return v, steps, ids + "2"
    # Any other per cent: find 1% and multiply.
    one = base / 100
    v = p * one
    steps = [(
        "1 per cent is one hundredth, so we divide by 100. %s divided by 100 is %s." % (sp(base), sp(one)),
        [line(1, "1%% of %s = %s ÷ 100 = %s" % (num(base), num(base), num(one)))]), (
        "%d per cent is %d lots of that. %d times %s is %s." % (p, p, p, sp(one), sp(v)),
        [line(2, "%d%% of %s = %d × %s = %s" % (p, num(base), p, num(one), num(v)))])]
    return v, steps, ids + "2"


def times_steps(a, b, ids):
    """a × b for small shop sums. Returns (steps, last_id); each step is (say, [ops])."""
    prod = a * b

    def line(i, text):
        return W("%s%d" % (ids, i), text)

    small, big = min(a, b), max(a, b)
    if big <= 10 or small == 10 or big == 10:
        if 10 in (a, b) and not (a <= 10 and b <= 10):
            other = a if b == 10 else b
            say = "%d times 10 is easy: %d tens are %d." % (other, other, prod)
        else:
            say = "%d times %d is %d." % (a, b, prod)
        return [(say, [line(1, "%d × %d = %d" % (a, b, prod))])], ids + "1"
    if big == 20:
        dbl = small * 2
        return [
            ("20 is 2 tens. So first double the %d: that is %d." % (small, dbl), [line(1, "%d × 2 = %d" % (small, dbl))]),
            ("Then 10 times %d is %d. So %d times %d is %d." % (dbl, prod, a, b, prod),
             [line(2, "%d × 10 = %d" % (dbl, prod)), line(3, "%d × %d = %d" % (a, b, prod))]),
        ], ids + "3"
    # Split the bigger number into 10 and the rest.
    rest = big - 10
    p1, p2 = 10 * small, rest * small
    if rest == 1:
        return [
            ("11 is 10 and 1 more. So start with 10 lots: 10 times %d is %d." % (small, p1), [line(1, "10 × %d = %d" % (small, p1))]),
            ("Then add the one extra lot of %d. %d plus %d makes %d. So %d times %d is %d." % (small, p1, small, prod, a, b, prod),
             [line(2, "%d + %d = %d" % (p1, small, prod)), line(3, "%d × %d = %d" % (a, b, prod))]),
        ], ids + "3"
    return [
        ("%d is 10 and %d. So we do it in two easy bites. 10 times %d is %d." % (big, rest, small, p1),
         [line(1, "10 × %d = %d" % (small, p1))]),
        ("And %d times %d is %d." % (rest, small, p2), [line(2, "%d × %d = %d" % (rest, small, p2))]),
        ("Put the two bites together. %d plus %d makes %d. So %d times %d is %d." % (p1, p2, prod, a, b, prod),
         [line(3, "%d + %d = %d" % (p1, p2, prod)), line(4, "%d × %d = %d" % (a, b, prod))]),
    ], ids + "4"
