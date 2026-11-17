"""Helpers for the imported-14 lessons (place value, a little profit and loss).

Board ops are plain dicts in the shape of src/lib/teach/types.ts. In every ask
written with ch() the FIRST choice is the right one; finish() moves it to a
position picked by a stable hash of the question id.
"""
import hashlib

MINUS = "−"


def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    return options[h(qid, salt) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def _w(i, text, tone, lab):
    op = {"op": "write", "id": i, "text": text}
    if tone:
        op["tone"] = tone
    if lab:
        op["label"] = True
    return op


def w(i, text):
    return _w(i, text, None, False)


def wl(i, text):
    return _w(i, text, None, True)


def g(i, text):
    return _w(i, text, "given", False)


def gl(i, text):
    return _w(i, text, "given", True)


def a(i, text):
    return _w(i, text, "answer", False)


def al(i, text):
    return _w(i, text, "answer", True)


def _t(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


def ul(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "underline"}


def ring(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "circle"}


def box(line, text, nth=1):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": "box"}


def nt(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": str(text), "place": place}


def x(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def grp(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_t(v[0], v[1]) if isinstance(v, tuple) else _t(v) for v in targets]}
    if label:
        op["label"] = label
    return op


def fig(i, spec):
    return {"op": "figure", "id": i, "spec": spec}


def pchart(number, hi=None, note=None):
    spec = {"kind": "placeChart", "number": "".join(c for c in str(number) if c.isdigit())}
    if hi:
        spec["highlight"] = ["d%d" % k for k in hi]
    if note:
        spec["note"] = note
    return spec


# ── Beats and asks ───────────────────────────────────────────────────────────

def ch(choices, if_not):
    """A choose ask. The FIRST choice is the right one; finish() shuffles it."""
    return {"kind": "choose", "choices": [str(c) for c in choices], "answer": 0, "ifNot": if_not}


def b(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def finish(qid, beats):
    """Move the right choice of each ask to a stable, varied position."""
    out = []
    for i, beat in enumerate(beats):
        beat = dict(beat)
        ask = beat.get("ask")
        if ask and ask.get("kind") == "choose":
            choices = list(ask["choices"])
            right, rest = choices[0], choices[1:]
            if h(qid, "flip%d" % i) % 2:
                rest.reverse()
            pos = h(qid, "pos%d" % i) % len(choices)
            choices = rest[:pos] + [right] + rest[pos:]
            beat["ask"] = {"kind": "choose", "choices": choices, "answer": pos, "ifNot": ask["ifNot"]}
        out.append(beat)
    return {"origin": "authored", "beats": out}


# ── Numbers and places ───────────────────────────────────────────────────────

def indian(n):
    s = str(n)
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    parts.insert(0, head)
    return ",".join(parts) + "," + tail


def fmt(n, style="in"):
    """Four digits are written plain (6000); five or more get Indian commas (60,000; 5,00,000)."""
    if style == "plain" or n < 10000:
        return str(n)
    return indian(n)


# Index 0 is the units place.
PLACES = ["units", "tens", "hundreds", "thousands", "ten-thousands", "lakhs", "ten-lakhs"]


def place_name(k, unit="ones"):
    return unit if k == 0 else PLACES[k]


def digits_of(shown):
    return [c for c in shown if c.isdigit()]


def nth_digit(shown, i):
    """Which occurrence (1-based) of its own character the i-th digit of `shown` is."""
    seen = -1
    for pos, c in enumerate(shown):
        if c.isdigit():
            seen += 1
            if seen == i:
                return shown[:pos + 1].count(c)
    raise ValueError((shown, i))


def take_apart(a_, b_, style="in"):
    """Lines that take b away from a one place at a time: thousands, then hundreds, tens, ones.

    Returns [(text, left, part, result)].
    """
    out = []
    cur = a_
    s = str(b_)
    for i, c in enumerate(s):
        part = int(c) * 10 ** (len(s) - 1 - i)
        if part == 0:
            continue
        nxt = cur - part
        out.append(("%s − %s = %s" % (fmt(cur, style), fmt(part, style), fmt(nxt, style)), cur, part, nxt))
        cur = nxt
    assert cur == a_ - b_
    return out
