"""Helpers for the imported-11 lessons (addition and subtraction, multiplication
and division stories). Board ops are plain dicts in the shape of
src/lib/teach/types.ts.
"""

MINUS = "−"

PLACES = ["ones", "tens", "hundreds", "thousands", "ten-thousands", "lakhs", "ten-lakhs", "crores", "ten-crores"]


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    return op


def LB(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text, "label": True}
    if tone:
        op["tone"] = tone
    return op


def GIVEN(id, text):
    """The question, in words and numbers."""
    return LB(id, text, "given")


def GIVENM(id, text):
    """The question, when it is a line of maths."""
    return W(id, text, "given")


def ANS(id, text):
    return W(id, text, "answer")


def ANSL(id, text):
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


def NOTE(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": _target(target, nth), "text": str(text), "place": place}


def STRIKE(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note:
        op["note"] = note
    return op


def ARC(line, frm, to, frm_nth=1):
    return {"op": "arc", "line": line, "from": _target(frm, frm_nth),
            "to": [_target(*t) if isinstance(t, tuple) else _target(t) for t in to]}


def GROUP(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_target(*t) if isinstance(t, tuple) else _target(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def TRI(shape, ab, bc, ca):
    return {"kind": "triangle", "shape": shape, "sides": {"ab": ab, "bc": bc, "ca": ca}}


def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats):
    assert 6 <= len(beats) <= 16, len(beats)
    return {"origin": "authored", "beats": list(beats)}


def last_nth(text, sub):
    """Which occurrence of `sub` is the last one in `text`."""
    return text.count(sub)


# ── Column working, computed ─────────────────────────────────────────────────

def col_sub(a, b):
    """Column subtraction a − b from the ones up. One dict per place:
    place, top (digit as printed), lent (it gave 1 to the place on its right),
    eff (what the top is worth in this column after lending and borrowing),
    bot, borrow (it had to borrow), res.
    """
    assert a >= b >= 0
    da = [int(c) for c in str(a)][::-1]
    db = [int(c) for c in str(b)][::-1] + [0] * len(str(a))
    out = []
    lent = 0
    for i, top in enumerate(da):
        eff = top - lent
        borrow = eff < db[i]
        if borrow:
            eff += 10
        out.append({"place": PLACES[i], "top": top, "lent": bool(lent), "eff": eff,
                    "bot": db[i], "borrow": borrow, "res": eff - db[i], "has_bot": i < len(str(b))})
        lent = 1 if borrow else 0
    assert lent == 0
    got = int("".join(str(c["res"]) for c in out)[::-1])
    assert got == a - b, (a, b, got)
    return out


def col_add(nums):
    """Column addition from the ones up. One dict per place: place, digits,
    carry_in, total, write, carry_out."""
    width = max(len(str(n)) for n in nums)
    out = []
    carry = 0
    for i in range(width):
        digits = [(n // 10 ** i) % 10 for n in nums if n >= 10 ** i or i == 0]
        total = sum(digits) + carry
        out.append({"place": PLACES[i], "digits": digits, "carry_in": carry, "total": total,
                    "write": total % 10 if i < width - 1 else total, "carry_out": total // 10 if i < width - 1 else 0})
        carry = total // 10
    return out
