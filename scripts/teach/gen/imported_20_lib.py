"""Helpers for the imported-20 lessons (triangles, sharing in a ratio).

Board ops are plain dicts in the shape of src/lib/teach/types.ts.
"""
import hashlib

P = "AIGEN_grade5_"


# ── Beats and lessons ────────────────────────────────────────────────────────

def B(say, *ops, ask=None):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if ask:
        beat["ask"] = ask
    return beat


def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def choose_at(qid, salt, right, others, if_not):
    """A choose ask with the right choice put at a stable place among the others."""
    others = list(others)
    assert right not in others and len(set(others)) == len(others), (qid, right, others)
    at = pick(qid, salt, list(range(len(others) + 1)))
    choices = list(others)
    choices.insert(at, right)
    return CHOOSE(choices, at, if_not)


def LESSON(beats, check=None):
    beats = [b for b in beats if b]
    assert 6 <= len(beats) <= 16, "%d beats" % len(beats)
    out = {"origin": "authored", "beats": beats}
    if check:
        out["check"] = check
    return out


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


# ── Lines ────────────────────────────────────────────────────────────────────

def G(i, text):
    """The question as printed (words, so a label)."""
    return {"op": "write", "id": i, "text": text, "tone": "given", "label": True}


def W(i, text):
    """A line of working: checked maths."""
    return {"op": "write", "id": i, "text": text}


def Lb(i, text):
    """A line of working in words (not checked)."""
    return {"op": "write", "id": i, "text": text, "label": True}


def A(i, text):
    """The final answer, in words with its unit."""
    return {"op": "write", "id": i, "text": text, "tone": "answer", "label": True}


# ── Marks ────────────────────────────────────────────────────────────────────

def T(text, nth=1):
    return {"text": text} if nth == 1 else {"text": text, "nth": nth}


def U(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "underline"}


def C(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "circle"}


def BX(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "box"}


def N(line, text, note, place="below", nth=1):
    return {"op": "note", "line": line, "target": T(text, nth), "text": note, "place": place}


def X(line, text, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": T(text, nth)}
    if note:
        op["note"] = note
    return op


def BOTH(line, text):
    return {"op": "both", "line": line, "text": text}


def DIV(line, by):
    return {"op": "divide", "line": line, "by": str(by)}


def GROUP(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": targets}
    if label:
        op["label"] = label
    return op


def last(text, sub):
    """The nth of the last place `sub` appears in `text`."""
    pos = text.rfind(sub)
    assert pos >= 0, (text, sub)
    return text[:pos].count(sub) + 1


def nth_at(text, sub, pos):
    assert text[pos:pos + len(sub)] == sub, (text, sub, pos)
    return text[:pos].count(sub) + 1


# ── Figures ──────────────────────────────────────────────────────────────────

def F(spec, i="fig"):
    return {"op": "figure", "id": i, "spec": spec}


def seg(label=None, units=1, tone=None):
    s = {"units": units}
    if label is not None:
        s["label"] = label
    if tone:
        s["tone"] = tone
    return s


def bar(label, segments, brace=None):
    b = {"segments": segments}
    if label:
        b["label"] = label
    if brace:
        b["brace"] = brace
    return b


def bars(*the_bars, note=None):
    spec = {"kind": "barModel", "bars": list(the_bars)}
    if note:
        spec["note"] = note
    return spec


def tri(shape, a=None, b=None, c=None, sides=None, note=None, highlight=None):
    spec = {"kind": "triangle", "shape": shape}
    angles = {k: v for k, v in (("a", a), ("b", b), ("c", c)) if v}
    if angles:
        spec["angles"] = angles
    if sides:
        spec["sides"] = sides
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return spec


# ── Words ────────────────────────────────────────────────────────────────────

def fmt(n):
    """A number as it is written and said: 1,800 and 14.4."""
    if isinstance(n, float) and n != int(n):
        return ("%f" % n).rstrip("0").rstrip(".")
    n = int(n)
    return "{:,}".format(n)


def parts(n):
    return "1 part" if n == 1 else "%d parts" % n


def say_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


ASK_180_SAY = [
    "Before we go on: what do the three angles of any triangle add up to?",
    "Here is the fact we need. What do the three angles of a triangle always add up to?",
    "One fact unlocks this. What do the three angles of any triangle add up to?",
]
ASK_180_IFNOT = [
    "Tear the three corners off a paper triangle and put them side by side. They always make a straight line, and a straight line is 180 degrees.",
    "A square corner is 90 degrees and a full turn is 360. The three angles of a triangle always make a half turn, a straight line, which is 180 degrees.",
]


def ask_180(qid):
    """The beat that asks for the angle sum. The fact goes on the board in the next beat."""
    return B(pick(qid, "a180", ASK_180_SAY),
             ask=choose_at(qid, "a180c", "180°", ["90°", "360°"], pick(qid, "a180n", ASK_180_IFNOT)))


def FACT(i="fact"):
    return Lb(i, "Angles of a triangle add up to 180°")
