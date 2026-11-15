"""Small helpers shared by the factors lesson scripts (rules and hand-written lessons).

Board ops are plain dicts in the shape of src/lib/teach/types.ts. These helpers only
save typing and work out `nth` for marks so that a mark lands on the right digit.
"""
import hashlib

TIMES = " × "


# ── Numbers ──────────────────────────────────────────────────────────────────

def pf(n):
    """Prime factors of n, smallest first: 60 -> [2, 2, 3, 5]."""
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def product(nums):
    v = 1
    for n in nums:
        v *= n
    return v


def shared(a, b):
    """Primes a and b have in common, with repeats: 24, 36 -> [2, 2, 3]."""
    fb = pf(b)
    out = []
    for p in pf(a):
        if p in fb:
            fb.remove(p)
            out.append(p)
    return out


def only(a, b):
    """Primes of a left over once the shared ones are taken out."""
    fa = pf(a)
    for p in shared(a, b):
        fa.remove(p)
    return fa


def join_times(nums):
    return TIMES.join(str(n) for n in nums)


def say_times(nums):
    return " times ".join(str(n) for n in nums)


def say_plus(nums):
    return " plus ".join(str(n) for n in nums)


def say_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


COUNT_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def count_of(n, p):
    """'one 2', 'two 2s'."""
    return "%s %d%s" % (COUNT_WORDS[n], p, "" if n == 1 else "s")


def how_often(n):
    return {1: "once", 2: "twice", 3: "three times", 4: "four times", 5: "five times", 6: "six times"}[n]


# ── Picking a phrasing ───────────────────────────────────────────────────────

def pick(qid, salt, options):
    """A stable choice among a few phrasings, so a family does not sound the same every time."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None):
    """A line of maths (the checker verifies it)."""
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    return op


def LB(id, text, tone=None):
    """A line of words (not checked as maths)."""
    op = {"op": "write", "id": id, "text": text, "label": True}
    if tone:
        op["tone"] = tone
    return op


def GIVEN(id, text):
    """The question, in words."""
    return LB(id, text, "given")


def GIVENM(id, text):
    """The question, when it is plain maths."""
    return W(id, text, "given")


def ANS(id, text):
    """The answer in words, e.g. 'HCF = 6'."""
    return LB(id, text, "answer")


def _target(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


def MARK(line, text, shape="circle", nth=1):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def CIRC(line, text, nth=1):
    return MARK(line, text, "circle", nth)


def UL(line, text, nth=1):
    return MARK(line, text, "underline", nth)


def BOX(line, text, nth=1):
    return MARK(line, text, "box", nth)


def NOTE(line, target, text, place=None, nth=1):
    op = {"op": "note", "line": line, "target": _target(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def STRIKE(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note:
        op["note"] = note
    return op


def GROUP(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else _target(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def T(text, nth=1):
    return _target(text, nth)


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIVIDE(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def TREE(id, n, note=None):
    spec = {"kind": "factorTree", "number": n, "highlight": ["primes"]}
    if note:
        spec["note"] = note
    return FIG(id, spec)


def VENN(id, left_title, right_title, left, both, right, highlight=None, note=None):
    spec = {"kind": "venn", "leftTitle": left_title, "rightTitle": right_title,
            "left": left, "both": both, "right": right}
    if highlight:
        spec["highlight"] = highlight
    if note:
        spec["note"] = note
    return FIG(id, spec)


def TABLE(id, headers, rows, highlight=None, note=None):
    spec = {"kind": "table", "rows": rows}
    if headers:
        spec["headers"] = headers
    if highlight:
        spec["highlight"] = highlight
    if note:
        spec["note"] = note
    return FIG(id, spec)


# ── Beats and asks ───────────────────────────────────────────────────────────

def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def THINK():
    return {"kind": "think"}


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats, **kw):
    script = {"origin": kw.get("origin", "authored"), "beats": list(beats)}
    if kw.get("check"):
        script["check"] = {"variable": kw["check"][0], "value": str(kw["check"][1])}
    return script


def shuffled(qid, salt, right, others):
    """Put the right choice at a stable but varying position. Returns (choices, index)."""
    n = len(others) + 1
    at = pick(qid, salt, list(range(n)))
    choices = list(others)
    choices.insert(at, right)
    return choices, at


# ── Prime-factor lines ───────────────────────────────────────────────────────

def nth_at(text, sub, pos):
    """Which occurrence of `sub` in `text` starts at `pos` (1-based)."""
    count = 0
    i = text.find(sub)
    while i != -1:
        count += 1
        if i == pos:
            return count
        i = text.find(sub, i + 1)
    raise ValueError("%r is not at %d in %r" % (sub, pos, text))


def factor_line(n):
    """('60 = 2 × 2 × 3 × 5', [(2, pos), (2, pos), (3, pos), (5, pos)])."""
    primes = pf(n)
    if len(primes) == 1:
        text = "%d = %d (prime)" % (n, n)
        return text, [(n, len("%d = " % n))]
    text = "%d = " % n
    places = []
    for i, p in enumerate(primes):
        if i:
            text += TIMES
        places.append((p, len(text)))
        text += str(p)
    return text, places


def factor_write(id, n):
    text, _ = factor_line(n)
    if len(pf(n)) == 1:
        return LB(id, text)
    return W(id, text)


def factor_marks(id, n, primes, shape="circle"):
    """Marks on the factor line of n for the given primes (with repeats), leftmost first."""
    text, places = factor_line(n)
    want = list(primes)
    ops = []
    for p, pos in places:
        if p in want:
            want.remove(p)
            ops.append(MARK(id, str(p), shape, nth_at(text, str(p), pos)))
    if want:
        raise ValueError("%s are not all factors of %d" % (primes, n))
    return ops


def pulled_out(n):
    """How the primes come out of n, in words: '2, 2 again, then 3, and 5 is left'."""
    primes = pf(n)
    last = primes[-1]
    runs = []
    for p in primes[:-1]:
        if runs and runs[-1][0] == p:
            runs[-1][1] += 1
        else:
            runs.append([p, 1])
    parts = []
    for p, count in runs:
        piece = str(p) if count == 1 else "%d %s" % (p, how_often(count))
        parts.append(piece if not parts else "then " + piece)
    return ", ".join(parts) + ", and %d is left" % last


def first_divisor_words(n):
    """Trying the small divisors in turn, in words, up to the first one that fits."""
    p = pf(n)[0]
    if p == 2:
        return "%d is even, so 2 comes out first." % n
    if p == 3:
        return "%d is odd, so 2 will not go in. Try 3 next, and 3 does go in." % n
    if p == 5:
        return "%d is odd, and 3 will not go in. But it ends in %d, so 5 does." % (n, n % 10)
    if p == 7:
        return "2, 3 and 5 will not go into %d. Try 7 next, and 7 does go in." % n
    return "2, 3, 5 and 7 will not go into %d. Try %d next, and it does go in." % (n, p)
