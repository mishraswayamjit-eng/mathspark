"""Helpers for the imported-06 lessons: board ops, beats, stable picks, and the two-step equation solver."""
import hashlib
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-06.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-06.json")


def batch():
    with io.open(BATCH, encoding="utf-8") as f:
        return json.load(f)


_IDS = None


def QID(short):
    """The full question id in this batch that contains `short` (must be unique)."""
    global _IDS
    if _IDS is None:
        _IDS = [q["id"] for q in batch()]
    hits = [i for i in _IDS if short in i]
    if len(hits) != 1:
        raise ValueError("%r matches %d ids" % (short, len(hits)))
    return hits[0]


# ── Board ops ────────────────────────────────────────────────────────────────

def _t(text, nth=None):
    t = {"text": text}
    if nth and nth > 1:
        t["nth"] = nth
    return t


def _tt(t):
    return _t(*t) if isinstance(t, tuple) else _t(t)


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


def C(line, text, nth=None):
    return M(line, text, "circle", nth)


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [_tt(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _tt(frm), "to": [_tt(t) for t in to]}


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


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


def lesson(*beats, **kw):
    out = {"origin": "authored"}
    if kw.get("check"):
        out["check"] = {"variable": kw["check"][0], "value": str(kw["check"][1])}
    flat = []
    for b in beats:
        if b is None:
            continue
        if isinstance(b, list):
            flat.extend(x for x in b if x is not None)
        else:
            flat.append(b)
    out["beats"] = flat
    return out


# ── Stable variety ───────────────────────────────────────────────────────────

def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    return options[h(qid, salt) % len(options)]


def placed(qid, salt, right, others):
    """Choices with the right one in a stable but varied position, as an ask."""
    others = list(others)
    pos = h(qid, salt) % (len(others) + 1)
    return others[:pos] + [right] + others[pos:], pos


def ask(qid, salt, right, others, if_not):
    choices, pos = placed(qid, salt, right, others)
    return choose(choices, pos, if_not)


# ── Solving  a·v + b = c  or  a·v − b = c  (or  b + a·v = c) ─────────────────

def eq_text(v, a, sign, b, c, const_first=False):
    if const_first:
        return "%d + %d%s = %d" % (b, a, v, c)
    return "%d%s %s %d = %d" % (a, v, "+" if sign == "+" else "−", b, c)


def solve(qid, v, a, sign, b, c, eq="e1", lab=False, const_first=False, asks="undo", final=True, tail=""):
    """The beats that take  a·v ± b = c  (already written on line `eq`) down to  v = x.

    asks: "undo" (ask how to clear the constant), "div" (ask what undoes the times),
    "both", or None. With lab=True the lines are labels (no `check` on the lesson).
    """
    plus = sign == "+"
    r = c - b if plus else c + b
    if r % a:
        raise ValueError("%s: %d is not a multiple of %d" % (qid, r, a))
    x = r // a
    f = {"t": "%d %s" % (a, v), "a": a, "b": b, "c": c, "r": r, "x": x, "v": v}
    undo_note = ("− %d" if plus else "+ %d") % b
    target = ("%d +" % b) if const_first else ("%s %d" % ("+" if plus else "−", b))
    beats = []

    if asks in ("undo", "both"):
        if const_first:
            q = pick(qid, "uq", [
                "We want the {t} on its own, but {b} is added to it. How do we clear the {b} away?",
                "First job: get the {t} alone. What do we do about the {b} that is added to it?"])
        elif plus:
            q = pick(qid, "uq", [
                "We want the {t} on its own, but it has a plus {b} with it. How do we clear that away?",
                "Think of the equals sign as a balance. How do we get rid of the plus {b} and keep it level?",
                "First job: get the {t} alone. What do we do about the plus {b}?"])
        else:
            q = pick(qid, "uq", [
                "We want the {t} on its own, but it has a minus {b} with it. How do we clear that away?",
                "Think of the equals sign as a balance. How do we get rid of the minus {b} and keep it level?",
                "First job: get the {t} alone. What do we do about the minus {b}?"])
        if plus:
            right = "take %d from both sides" % b
            wrongs = ["add %d to both sides" % b, "take %d from the left side only" % b]
            if_not = "Adding {b} is undone by taking {b} away. And the two sides only stay equal if we take it from both."
            do = pick(qid, "do", ["So we take {b} from both sides.", "So {b} comes off both sides."])
        else:
            right = "add %d to both sides" % b
            wrongs = ["take %d from both sides" % b, "add %d to the left side only" % b]
            if_not = "Taking away {b} is undone by adding {b}. And the two sides only stay equal if we add it to both."
            do = pick(qid, "do", ["So we add {b} to both sides.", "So {b} goes on to both sides."])
        beats.append(B(q.format(**f), ask=ask(qid, "undo", right, wrongs, if_not.format(**f))))
    elif const_first:
        do = "To clear the {b}, we take {b} away. And to keep the two sides equal, we take it from both."
    elif plus:
        do = "To undo the plus {b}, we take {b} away. And to keep the two sides equal, we take it from both."
    else:
        do = "To undo the minus {b}, we add {b}. And to keep the two sides equal, we add it to both."
    beats.append(B(do.format(**f), S(eq, target, undo_note), BOTH(eq, undo_note)))

    if plus:
        res = pick(qid, "res", [
            "On the left, only {t} is left. On the right, {c} minus {b} is {r}.",
            "The {b} is gone from the left, leaving {t}. And {c} take away {b} is {r}."])
    else:
        res = pick(qid, "res", [
            "On the left, only {t} is left. On the right, {c} plus {b} is {r}.",
            "The minus {b} is gone from the left, leaving {t}. And {c} plus {b} is {r}."])
    beats.append(B(res.format(**f),
                   W(eq + "a", "%d%s = %d %s %d" % (a, v, c, "−" if plus else "+", b), label=lab),
                   W(eq + "b", "%d%s = %d" % (a, v, r), label=lab)))

    if asks in ("div", "both"):
        beats.append(B("{t} means {a} times {v}. What undoes times {a}?".format(**f),
                       ask=ask(qid, "div", "divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a],
                               "Times and divide are partners. To undo times {a}, we divide by {a}, on both sides.".format(**f))))
        dv = "So we divide both sides by {a}. {r} divided by {a} is {x}."
    else:
        dv = pick(qid, "dv", [
            "{t} means {a} times {v}. So we divide both sides by {a}, and {r} divided by {a} is {x}.",
            "Now {a} lots of {v} make {r}. Divide both sides by {a}: {r} divided by {a} is {x}."])
    line = "%s = %d" % (v, x)
    if final:
        ops = [DIV(eq + "b", a), ANS("ans", line), C("ans", line)]
    else:
        ops = [DIV(eq + "b", a), W(eq + "x", line, label=lab), M(eq + "x", line)]
    beats.append(B(dv.format(**f) + tail, *ops))
    return beats


def plain(short, v, a, sign, b, c, given, intro, eq_q, wrongs, eq_if, build, tail, check, summ,
          asks="undo", const_first=False, trap=None, pre=None, marks=(), right=None, checklines=None, lead=()):
    """A whole lesson for a word problem that becomes  a·v ± b = c  with v the answer."""
    qid = QID(short)
    plus = sign == "+"
    r = c - b if plus else c + b
    x = r // a
    eq = eq_text(v, a, sign, b, c, const_first)
    if checklines is None:
        if const_first:
            checklines = ["%d + %d × %d = %d" % (b, a, x, c)]
        else:
            checklines = ["%d × %d %s %d = %d" % (a, x, "+" if plus else "−", b, c)]
    beats = [B(intro, GIVEN("g", given, True))]
    beats += list(pre or [])
    beats.append(B(eq_q, ask=ask(qid, "eq", right or eq, wrongs, eq_if)))
    beats.append(B(build, *(list(lead) + [W("e1", eq)] + list(marks))))
    beats += solve(qid, v, a, sign, b, c, const_first=const_first, asks=asks, tail=tail)
    if trap is not None:
        beats.append(trap)
    beats.append(B(check, *[W("c%d" % (i + 1), t) for i, t in enumerate(checklines)]))
    beats.append(B(summ))
    return qid, lesson(*beats, check=(v, x))
