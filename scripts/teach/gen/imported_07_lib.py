"""Helpers for the imported-07 lessons (equations): board ops, beats, a checked label line, the two-step ending."""
import hashlib
import importlib.util
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-07.json")
BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-07.json")

_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
_tv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tv)


def _t(t):
    if isinstance(t, tuple):
        out = {"text": t[0]}
        if t[1] > 1:
            out["nth"] = t[1]
        return out
    return {"text": t}


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


def E(id, text, var, val, tone=None):
    """A line with a letter in it that the checker cannot test (the letter is not the keyed answer,
    or is a capital). We test it here, then write it as a label."""
    matter = _tv.check_line(text, var, Fraction(val))
    if matter:
        raise ValueError('"%s" %s' % (text, matter))
    return W(id, text, tone, True)


def L(id, text, vv=None, tone=None):
    """A maths line: plain when the checker can test it, a tested label otherwise (vv = (letter, value))."""
    return E(id, text, vv[0], vv[1], tone) if vv else W(id, text, tone)


def M(line, text, shape="underline"):
    return {"op": "mark", "line": line, "target": _t(text), "shape": shape}


def N(line, target, text, place="below"):
    return {"op": "note", "line": line, "target": _t(target), "text": text, "place": place}


def S(line, target, note=None):
    op = {"op": "strike", "line": line, "target": _t(target)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_t(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _t(frm), "to": [_t(t) for t in to]}


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


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


def lesson(*beats, **kw):
    out = {"origin": "authored"}
    if kw.get("check"):
        out["check"] = {"variable": kw["check"][0], "value": str(kw["check"][1])}
    flat = []
    for b in beats:
        if isinstance(b, list):
            flat += b
        elif b is not None:
            flat.append(b)
    out["beats"] = flat
    return out


def pick(qid, salt, options):
    n = int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)
    return options[n % len(options)]


def placed(qid, salt, right, others):
    n = int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)
    pos = n % (len(others) + 1)
    return others[:pos] + [right] + others[pos:], pos


# ── The ending every two-step equation shares: clear the loose number, then undo the times ──

def tail(qid, v, a, b, c, eq, form="ax+b", vv=None, asks=("clear",), found=None, final=True, p="t"):
    """Beats that solve  a·v + b = c  (form "ax+b"),  b + a·v = c  ("b+ax")  or  a·v − b = c  ("ax-b").

    eq     id of the line already on the board that holds the equation
    vv     None when the checker can test lines with the letter, else (letter, value) for tested labels
    asks   which turning points stop for the child: "clear" (the loose number), "div" (undo the times)
    found  a sentence saying what the value means in the story, said when it is ringed
    final  True: the value is the lesson's answer (answer pen, ringed). False: it is a step on the way.
    """
    minus = form == "ax-b"
    r = c + b if minus else c - b
    assert r % a == 0, (qid, a, b, c)
    val = r // a
    av = "%d%s" % (a, v)
    sav = "%d %s" % (a, v)
    if minus:
        target, note, undo, anti = "− %d" % b, "+ %d" % b, "add %d to both sides" % b, "take %d from both sides" % b
        loose = "the %d that is taken off" % b
        why = "Taking off %d is undone by adding %d, and the balance only stays level if both sides get the same. The dividing comes later." % (b, b)
        rhs = "%d + %d" % (c, b)
        done = pick(qid, p + "done", [
            "So we add %d to both sides. That leaves %s on the left, and %d plus %d, which is %d, on the right." % (b, sav, c, b, r),
            "Add %d on the left, and %d on the right as well. That leaves %s equals %d plus %d, which is %d." % (b, b, sav, c, b, r),
        ])
    else:
        target = ("+ %d" % b) if form == "ax+b" else str(b)
        note, undo, anti = "− %d" % b, "take %d from both sides" % b, "add %d to both sides" % b
        loose = "the %d that is added on" % b
        why = "Adding %d is undone by taking %d away, and the balance only stays level if both sides lose the same. The dividing comes later." % (b, b)
        rhs = "%d − %d" % (c, b)
        done = pick(qid, p + "done", [
            "So we take %d from both sides. That leaves %s on the left, and %d minus %d, which is %d, on the right." % (b, sav, c, b, r),
            "Take away %d on the left, and %d on the right as well. That leaves %s equals %d minus %d, which is %d." % (b, b, sav, c, b, r),
        ])
    beats = []
    if "clear" not in asks:
        # Nobody was asked, so the teacher says why before doing it.
        if minus:
            done = "The %d is taken off, so to undo it we add %d to both sides. That leaves %s equals %d plus %d, which is %d." % (b, b, sav, c, b, r)
        else:
            done = "The %d is added on, so to undo it we take %d from both sides. That leaves %s equals %d minus %d, which is %d." % (b, b, sav, c, b, r)
    if "clear" in asks:
        choices, idx = placed(qid, p + "c", undo, [anti, "divide both sides by %d" % a])
        beats.append(B(pick(qid, p + "q", [
            "We want the %s by itself. So what should we do about %s?" % (sav, loose),
            "The %s is not alone yet. Which move clears away %s?" % (sav, loose),
            "Think of the equals sign as a balance. What gets rid of %s and keeps the balance level?" % loose,
        ]), ask=choose(choices, idx, why)))
    beats.append(B(done, S(eq, target, note), BOTH(eq, note),
                   L(p + "1", "%s = %s" % (av, rhs), vv), L(p + "2", "%s = %d" % (av, r), vv)))
    last = "%s = %d" % (v, val)
    ring = [L(p + "3", last, vv, "answer" if final else None), M(p + "3", last, "circle" if final else "box")]
    tell = found if found else "So %s equals %d." % (v, val)
    # A division outside the tables gets its times fact said with it.
    if a > 10 or val > 10:
        fact = "%d divided by %d is %d, because %d times %d is %d." % (r, a, val, a, val, r)
    else:
        fact = "%d divided by %d is %d." % (r, a, val)
    if "div" in asks:
        choices, idx = placed(qid, p + "d", "divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a])
        beats.append(B(pick(qid, p + "dq", [
            "Nearly there. %s means %d times %s. What undoes times %d?" % (sav, a, v, a),
            "Now %s means %d lots of %s. How do we get down to just one %s?" % (sav, a, v, v),
        ]), ask=choose(choices, idx, "Times and divide are partners. Whatever times does, divide undoes. So we divide both sides by %d." % a)))
        beats.append(B("So a bar goes under each side, and we divide by %d." % a, DIV(p + "2", a)))
    else:
        beats.append(B(pick(qid, p + "dv", [
            "%s means %d times %s. So to undo the times, we divide both sides by %d." % (sav, a, v, a),
            "Now %s is %d lots of %s. To find just one %s, we divide both sides by %d." % (sav, a, v, v, a),
        ]), DIV(p + "2", a)))
    beats.append(B("%s %s" % (fact, tell), *ring))
    return beats
