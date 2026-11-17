"""Helpers for the imported-08 lessons: board ops, beats, stable picks, prime factors."""
import hashlib


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


def GIVEN(id, text, label=False):
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
    """targets: list of (text, nth)."""
    op = {"op": "group", "line": line, "targets": [_t(t, n) for t, n in targets]}
    if label:
        op["label"] = label
    return op


def DIV(line, by):
    return {"op": "divide", "line": line, "by": by}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


# ── Beats and lessons ────────────────────────────────────────────────────────

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
    return {"origin": "authored", "beats": [b for b in beats if b is not None]}


# ── Stable variety ───────────────────────────────────────────────────────────

def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    return options[h(qid, salt) % len(options)]


def placed(qid, salt, right, others):
    """Choices with the right one in a stable but varied position. Returns (choices, index)."""
    others = list(others)
    pos = h(qid, salt) % (len(others) + 1)
    return others[:pos] + [right] + others[pos:], pos


# ── Numbers ──────────────────────────────────────────────────────────────────

def primes_of(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def hcf(nums):
    from math import gcd
    g = nums[0]
    for n in nums[1:]:
        g = gcd(g, n)
    return g


def times_words(factors):
    return " times ".join(str(f) for f in factors)


def and_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def how_often(k):
    return {1: "once", 2: "twice"}.get(k, "%d times" % k)


def nth_at(line, sub, at):
    """Which occurrence (1-based) of `sub` on `line` starts at index `at`."""
    assert line[at:at + len(sub)] == sub, (line, sub, at)
    n, i = 0, 0
    while True:
        j = line.find(sub, i)
        if j < 0 or j > at:
            raise ValueError("%r is not cleanly found at %d on %r" % (sub, at, line))
        n += 1
        if j == at:
            return n
        i = j + 1


def factor_line(n):
    """('84 = 2 × 2 × 3 × 7', [char index of each factor])."""
    text = "%d = " % n
    places = []
    for i, p in enumerate(primes_of(n)):
        if i:
            text += " × "
        places.append(len(text))
        text += str(p)
    return text, places


def shared_runs(n, shared):
    """Where the shared primes sit on n's factor line, as runs: [(text, nth)].

    `shared` is the HCF's prime list. For each prime the first copies on the line are taken;
    neighbours are joined into one run ('2 × 2 × 3')."""
    text, places = factor_line(n)
    factors = primes_of(n)
    want = list(shared)
    taken = []
    for i, p in enumerate(factors):
        if p in want:
            want.remove(p)
            taken.append(i)
    assert not want, (n, shared)
    runs, start, prev = [], None, None
    for i in taken:
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            runs.append((start, prev))
            start = prev = i
    runs.append((start, prev))
    out = []
    for a, b in runs:
        sub = " × ".join(str(f) for f in factors[a:b + 1])
        out.append((sub, nth_at(text, sub, places[a])))
    return out
