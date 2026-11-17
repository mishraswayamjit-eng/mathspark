"""Helpers for the imported-10 lessons: board ops, beats, stable picks, and a few computed moves."""
import hashlib
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-10.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-10.json")

with io.open(BATCH, encoding="utf-8") as _f:
    QUESTIONS = json.load(_f)

LESSONS = {}


def full(short):
    """The whole question id for the first eight characters of its code."""
    hits = [q["id"] for q in QUESTIONS if q["id"].startswith("AIGEN_grade5_" + short)]
    if len(hits) != 1:
        raise ValueError("%s matches %d questions" % (short, len(hits)))
    return hits[0]


def add(short, *beats):
    qid = full(short)
    if qid in LESSONS:
        raise ValueError("two lessons for %s" % short)
    LESSONS[qid] = {"origin": "authored", "beats": [b for b in beats if b is not None]}


# ── Numbers as written on the board ──────────────────────────────────────────

def f(n):
    """A whole number with Indian commas (1,250 and 6,40,550). Strings pass through."""
    if isinstance(n, str):
        return n
    s = str(n)
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


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


def L(id, text):
    return W(id, text, None, True)


def GIVEN(id, text, label=True):
    return W(id, text, "given", label)


def ANS(id, text, label=False):
    return W(id, text, "answer", label)


def M(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": _t(text, nth), "shape": shape}


def RING(line, text, nth=None):
    return M(line, text, "circle", nth)


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def table(headers, rows):
    return {"kind": "table", "headers": headers, "rows": rows}


def bar(segments, brace=None, label=None):
    """segments: (units, label, tone)."""
    b = {"segments": [{"units": u, "label": lab, "tone": tone} for u, lab, tone in segments]}
    if brace:
        b["brace"] = brace
    if label:
        b["label"] = label
    return b


def bars(*bs):
    return {"kind": "barModel", "bars": list(bs)}


# ── Beats ────────────────────────────────────────────────────────────────────

def B(say, *board):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
    if ops:
        beat["board"] = ops
    return beat


def h(key, salt=""):
    return int(hashlib.md5((key + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(key, salt, options):
    """One of `options`, the same every run for this question and salt."""
    return options[h(key, salt) % len(options)]


def ASK(key, salt, say, right, others, if_not, *board):
    """A beat that stops for the child. The right choice sits in a stable but varied place."""
    others = list(others)
    pos = h(key, salt) % (len(others) + 1)
    beat = B(say, *board)
    beat["ask"] = {"kind": "choose", "choices": others[:pos] + [right] + others[pos:], "answer": pos, "ifNot": if_not}
    return beat


# ── Computed moves ───────────────────────────────────────────────────────────

def _no_borrow(a, b):
    sa = str(a)
    sb = str(b).rjust(len(sa), "0")
    return all(x >= y for x, y in zip(sa, sb))


def take(key, a, b, lid, lead="", tone=None, mark=None, extra=()):
    """The beats for a − b, done in a way that suits the numbers.

    lead: a sentence said first. mark: (line, text) to underline while the sum is set up.
    extra: ops added after the finished line."""
    d = a - b
    main = W(lid, "%s − %s = %s" % (f(a), f(b), f(d)), tone)
    extra = list(extra)
    pre = (lead + " ") if lead else ""
    setup_ops = [M(mark[0], mark[1])] if mark else []
    if _no_borrow(a, b):
        return [B("%s%d minus %d is %d." % (pre, a, b, d), main, *extra)]
    if a % 100 == 0 and _no_borrow(a - 1, b - 1):
        sum_words = "" if str(a) in lead else (("That is " if lead else "") + "%d minus %d. " % (a, b))
        setup = pre + sum_words + pick(key, lid + "setup", [
            "Careful: borrowing across those zeros is where slips happen.",
            "Careful: the zeros in %d make the borrowing fiddly." % a,
        ])
        trick = pick(key, lid + "trick", [
            "So here is a trick: take 1 off both numbers, and the gap between them stays the same. %d minus %d needs no borrowing, and it is %d.",
            "A neat way round it: slide both numbers down by 1. The gap does not change, and %d minus %d needs no borrowing at all. It is %d.",
        ]) % (a - 1, b - 1, d)
        return [B(setup, *setup_ops),
                B(trick, W(lid + "t", "%s − %s = %s" % (f(a - 1), f(b - 1), f(d))), main, *extra)]
    up = (100 - b % 100) % 100
    if 0 < up <= 5 and a - b - up > 0:
        r = b + up
        return [B(pre + ("That is " if lead else "") + "%d minus %d." % (a, b), *setup_ops),
                B("%d is just %d short of %d. So take away %d, which leaves %d, and then give the %d back: %d."
                  % (b, up, r, r, a - r, up, d),
                  W(lid + "r", "%s − %s = %s" % (f(a), f(r), f(a - r))),
                  W(lid + "g", "%s + %s = %s" % (f(a - r), f(up), f(d))), main, *extra)]
    words = pick(key, lid + "plain", [
        "Mind the borrowing here: %d minus %d is %d.",
        "Go column by column, borrowing where you need to: %d minus %d is %d.",
    ]) % (a, b, d)
    return [B(pre + words, main, *extra)]


def total(nums, lid, note=None):
    """(words, ops, sum) for adding two, three or four numbers, one step at a time."""
    run = nums[0]
    ops = []
    said = []
    for i, n in enumerate(nums[1:]):
        nxt = run + n
        ops.append(W("%s%d" % (lid, i + 1), "%s + %s = %s" % (f(run), f(n), f(nxt))))
        if i == 0:
            said.append("%d plus %d is %d" % (run, n, nxt))
        elif i == len(nums) - 2:
            said.append("and %d more makes %d" % (n, nxt))
        else:
            said.append("%d more makes %d" % (n, nxt))
        run = nxt
    last = "%s%d" % (lid, len(nums) - 1)
    if note:
        ops.append(N(last, "= " + f(run), note))
    return ", ".join(said) + ".", ops, run, last


def hundreds(p, r, lid, whose=""):
    """Two beats: how many hundreds are in the deposit, and what they earn in one year."""
    hs = p // 100
    y = hs * r
    b1 = B("%d per cent a year means every 100 rupees earns %d rupees in a year. So how many hundreds are in %s%d? %d divided by 100 is %d."
           % (r, r, whose, p, p, hs),
           W(lid + "h", "%s ÷ 100 = %s" % (f(p), f(hs))), N(lid + "h", "= " + f(hs), "hundreds"))
    b2 = B("Each of those %d hundreds earns %d rupees. %d times %d is %d. So 1 year brings %d rupees of interest."
           % (hs, r, hs, r, y, y),
           W(lid + "y", "%s × %s = %s" % (f(hs), f(r), f(y))), N(lid + "y", "= " + f(y), "interest for 1 year"))
    return b1, b2
