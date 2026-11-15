"""Small helpers for writing ratio-word-problems lessons (see ratio_word_problems.py)."""
import hashlib


def beat(say, *ops, ask=None):
    b = {"say": say}
    if ops:
        b["board"] = list(ops)
    if ask:
        b["ask"] = ask
    return b


def ask(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


THINK = {"kind": "think"}


def lesson(*beats, origin="authored", check=None):
    out = {"origin": origin, "beats": list(beats)}
    if check:
        out["check"] = check
    return out


# ── Lines ────────────────────────────────────────────────────────────────────

def G(i, text):
    """The question as printed (words, so a label)."""
    return {"op": "write", "id": i, "text": text, "tone": "given", "label": True}


def W(i, text):
    """A line of working: checked maths."""
    return {"op": "write", "id": i, "text": text}


def Lb(i, text):
    """A line of working in words."""
    return {"op": "write", "id": i, "text": text, "label": True}


def A(i, text):
    """The final answer, in words with its unit."""
    return {"op": "write", "id": i, "text": text, "tone": "answer", "label": True}


def AM(i, text):
    """The final answer as a checked line of maths."""
    return {"op": "write", "id": i, "text": text, "tone": "answer"}


# ── Marks ────────────────────────────────────────────────────────────────────

def T(text, nth=1):
    return {"text": text} if nth == 1 else {"text": text, "nth": nth}


def U(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "underline"}


def C(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "circle"}


def Bx(line, text, nth=1):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": "box"}


def N(line, text, note, place="above", nth=1):
    return {"op": "note", "line": line, "target": T(text, nth), "text": note, "place": place}


def X(line, text, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": T(text, nth)}
    if note:
        op["note"] = note
    return op


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": frm, "to": to}


def nth_at(line, text, pos):
    """Which occurrence of `text` starts at character `pos` of `line`."""
    assert line[pos:pos + len(text)] == text, (line, text, pos)
    return line[:pos].count(text) + 1


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


def bars(*the_bars, note=None, highlight=None):
    spec = {"kind": "barModel", "bars": list(the_bars)}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return spec


def table(headers, rows, note=None, highlight=None):
    spec = {"kind": "table", "headers": headers, "rows": rows}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return spec


def venn(left_title, right_title, left, both, right, note=None, highlight=None):
    spec = {"kind": "venn", "leftTitle": left_title, "rightTitle": right_title,
            "left": left, "both": both, "right": right}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return spec


# ── Stable variety ───────────────────────────────────────────────────────────

def pick(qid, salt, options):
    """One of `options`, chosen by a stable hash of the question id."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def choose(qid, salt, right, others, if_not):
    """A 'choose' ask with the right choice at a stable, varying position."""
    seen = [right]
    for o in others:
        if o not in seen:
            seen.append(o)
    rest = seen[1:3]
    where = pick(qid, salt, list(range(len(rest) + 1)))
    choices = rest[:where] + [right] + rest[where:]
    return ask(choices, where, if_not)
