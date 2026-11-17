"""Helpers for the imported-09 lessons (integers on a number line, simple interest)."""


# ── Board ops ────────────────────────────────────────────────────────────────

def _t(text, nth=None):
    t = {"text": text}
    if nth and nth > 1:
        t["nth"] = nth
    return t


def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def GIVEN(id, text, label=True):
    return W(id, text, "given", label)


def ANS(id, text, label=False):
    return W(id, text, "answer", label)


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_t(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats):
    flat = []
    for b in beats:
        if b is None:
            continue
        if isinstance(b, list):
            flat.extend(x for x in b if x is not None)
        else:
            flat.append(b)
    return {"origin": "authored", "beats": flat}


# ── Saying and writing numbers ───────────────────────────────────────────────

def sp(n):
    """A number as the teacher says it: minus 12, 5."""
    return ("minus %d" % -n) if n < 0 else str(n)


def bd(n):
    """A number as it is written on the board: −12, 5."""
    return ("−%d" % -n) if n < 0 else str(n)


def cap(s):
    return s[0].upper() + s[1:]


def listed(nums):
    nums = [str(n) for n in nums]
    if len(nums) == 1:
        return nums[0]
    return ", ".join(nums[:-1]) + " and " + nums[-1]


def circle_last(line_id, line, text):
    """Ring the last place `text` appears on the line."""
    return M(line_id, text, "circle", line.count(text))


# ── A walk along the number line, one move at a time ─────────────────────────

class Walk:
    """Keeps the position, writes one line per move and says why the sign comes out as it does.

    Each kind of move (crossing 0 going up, staying below, going further down ...) is
    explained in full the first time it happens in a lesson, and just stated after that.
    """

    def __init__(self, start, horizontal=False, prefix="s"):
        self.pos = start
        self.h = horizontal
        self.prefix = prefix
        self.n = 0
        self.seen = set()
        self.last_id = None
        self.last_line = None

    def _why(self, a, d):
        b = a + d
        h = self.h
        if d > 0 and a < 0:
            if b > 0:
                return "upcross", ("%d of those steps bring us back to 0, and then %d more to the right of it." if h
                                   else "%d of those steps bring us up to 0, and then %d more above it.") % (-a, b)
            if b == 0:
                return "upexact", "That is exactly enough to get back to 0."
            return "upshort", ("We move towards 0 but do not reach it, so we are still on the minus side, at minus %d." if h
                               else "We climb towards 0 but do not reach it, so we are still below, at minus %d.") % -b
        if d < 0 and a < 0:
            return "downneg", ("We were already on the minus side and we go further left, so %d and %d join up to make minus %d." if h
                               else "We were already below 0 and we go further down, so %d and %d join up to make minus %d.") % (-a, -d, -b)
        if d < 0 and a == 0:
            return "zero", ("Going left from 0 puts us straight into the minus numbers." if h
                            else "Going down from 0 puts us straight into the minus numbers.")
        if d < 0 and a > 0 and b < 0:
            return "downcross", ("%d of those steps take us back to 0, and then %d more to the left of it." if h
                                 else "%d of those steps take us down to 0, and then %d more below it.") % (a, -b)
        return None, ""

    def mv(self, d, lead="", why=True, tail="", before=(), after=()):
        a, b = self.pos, self.pos + d
        self.n += 1
        lid = "%s%d" % (self.prefix, self.n)
        line = "%s %s %d = %s" % (bd(a), "+" if d > 0 else "−", abs(d), bd(b))
        say = (lead + " " if lead else "") + cap("%s %s %d is %s." % (sp(a), "plus" if d > 0 else "minus", abs(d), sp(b)))
        case, text = self._why(a, d)
        if why and case and case not in self.seen:
            say += " " + text
        if case:
            self.seen.add(case)
        if tail:
            say += " " + tail
        self.pos = b
        self.last_id, self.last_line = lid, line
        ops = list(before) + [W(lid, line), M(lid, bd(b), "underline", line.count(bd(b)))] + list(after)
        return B(say, *ops)


# ── Simple interest pieces ───────────────────────────────────────────────────

FORMULA = "Interest = P × R × T ÷ 100"


def hundreds(p):
    assert p % 100 == 0, p
    return p // 100


def per_year(p, r):
    return hundreds(p) * r


def pct_ask(r, lead="First, what does %d percent a year mean?"):
    return B(lead % r,
             ask=choose(["₹%d on every ₹100, each year" % r, "₹%d each year" % r, "₹%d on every ₹100, only once" % r], 0,
                        "Percent means out of 100. So the bank pays %d rupees for every 100 rupees kept there, and it pays that again every year." % r))


def yearly(p, r, lid, lead="Start with 1 year."):
    """One beat: p is so many hundreds, each earning r rupees a year."""
    h = hundreds(p)
    say = "%s %d is %d hundreds, and each hundred earns %d rupees a year. %d times %d is %d." % (lead, p, h, r, h, r, h * r)
    return B(say, W(lid + "a", "%d ÷ 100 = %d" % (p, h)), W(lid + "b", "%d × %d = %d" % (h, r, h * r)))


def rate_beats(p, t, amount, lid="r", first="First the interest."):
    """Two beats that find the rate from a deposit, the time and the amount paid back."""
    i = amount - p
    assert i % t == 0
    y = i // t
    h = hundreds(p)
    assert y % h == 0
    r = y // h
    b1 = B("%s %d minus %d is %d. That built up over %d years, the same each year, so 1 year is %d." % (first, amount, p, i, t, y),
           W(lid + "1", "%d − %d = %d" % (amount, p, i)), W(lid + "2", "%d ÷ %d = %d" % (i, t, y)))
    b2 = B("%d is %d hundreds. Share %d among %d hundreds and each hundred earns %d rupees a year. So the rate is %d percent." % (p, h, y, h, r, r),
           W(lid + "3", "%d ÷ 100 = %d" % (p, h)), W(lid + "4", "%d ÷ %d = %d" % (y, h, r)),
           W(lid + "5", "Rate = %d%% a year" % r, label=True), M(lid + "5", "%d%%" % r, "box"))
    return [b1, b2], r
