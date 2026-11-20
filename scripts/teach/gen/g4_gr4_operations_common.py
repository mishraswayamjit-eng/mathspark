"""Small helpers shared by the Grade 4 operations lesson scripts (board ops, beats, stable picks)."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

TOPIC = "gr4_operations"
PART = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
FIGS = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)


def questions():
    return {q["id"]: q for q in bank.load_bank(4) if q.get("node") == TOPIC}


def opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def key_text(q):
    i = "ABCD".find(q.get("correctAnswer", ""))
    o = opts(q)
    return o[i] if 0 <= i < len(o) else ""


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


def RING(line, text, nth=None):
    return M(line, text, "circle", nth)


def N(line, target, text, place="below", nth=None):
    return {"op": "note", "line": line, "target": _t(target, nth), "text": text, "place": place}


def S(line, target, note=None, nth=None):
    op = {"op": "strike", "line": line, "target": _t(target, nth)}
    if note:
        op["note"] = note
    return op


def G(line, targets, label=None):
    op = {"op": "group", "line": line,
          "targets": [_t(*t) if isinstance(t, tuple) else _t(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def ARC(line, frm, to):
    return {"op": "arc", "line": line, "from": _t(frm),
            "to": [_t(*t) if isinstance(t, tuple) else _t(t) for t in to]}


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


# ── Beats and lessons ────────────────────────────────────────────────────────

def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


THINK = {"kind": "think"}


def B(say, *board, **kw):
    beat = {"say": say}
    ops = [op for op in board if op is not None]
    if ops:
        beat["board"] = ops
    if kw.get("ask") is not None:
        beat["ask"] = kw["ask"]
    return beat


def lesson(*beats, **kw):
    out = {"origin": kw.get("origin", "authored")}
    out["beats"] = [b for b in beats if b is not None]
    return out


# ── Stable variety ───────────────────────────────────────────────────────────

def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest()[:8], 16)


def pick(qid, salt, options):
    """One of `options`, the same every run for this question and salt."""
    return options[h(qid, salt) % len(options)]


def placed(qid, salt, right, others):
    """Choices with the right one in a stable but varied position. Returns (choices, index)."""
    others = [o for i, o in enumerate(others) if o != right and o not in others[:i]]
    pos = h(qid, salt) % (len(others) + 1)
    choices = others[:pos] + [right] + others[pos:]
    return choices, pos


def ask_of(qid, salt, right, others, if_not):
    choices, pos = placed(qid, salt, right, others)
    return choose(choices, pos, if_not)


def tw(n):
    return "1 ten" if n == 1 else "%d tens" % n


def ow(n):
    return "1 one" if n == 1 else "%d ones" % n


def ANSR(id, text, target):
    """The answer line, with a ring round the LAST place `target` appears on it."""
    return [ANS(id, text), RING(id, target, text.count(target))]


def has(q, value):
    return str(value) in [o.replace(",", "").replace("₹", "").strip() for o in opts(q)]


_FIGS = None


def figures():
    global _FIGS
    if _FIGS is None:
        import io
        import json
        _FIGS = {}
        if os.path.exists(FIGS):
            with io.open(FIGS, encoding="utf-8") as f:
                _FIGS = json.load(f)
    return _FIGS


def hop_figure(qid):
    """The question's number-line figure with the most hops drawn, as a board op (or None)."""
    entry = figures().get(qid) or {}
    best = None
    for spec in entry.get("stepFigures") or []:
        if spec and spec.get("kind") == "numberLine" and spec.get("hops"):
            if best is None or len(spec["hops"]) >= len(best["hops"]):
                best = spec
    return FIG("nl", best) if best else None


def step_figure(qid, kind, index=0):
    """The question's step figure number `index` if it is of this kind, as a board op (or None)."""
    steps = (figures().get(qid) or {}).get("stepFigures") or []
    if index < len(steps) and steps[index] and steps[index].get("kind") == kind:
        return FIG("fig", steps[index])
    return None


def times_work(m, n, name):
    """How to work out m × n in small steps: (what to say, board ops). The last line shows the product."""
    p = m * n
    if (m <= 10 and n <= 10) or n == 10 or m == 10:
        return "%d times %d is %d." % (m, n, p), [W(name, "%d × %d = %d" % (m, n, p))]
    if m > 10 and n <= 9:
        t, o = m - m % 10, m % 10
        if o == 0:
            d = t // 10
            return ("%d times %d is %d, so %d times %d is %d." % (d, n, d * n, m, n, p),
                    [W(name + "a", "%d × %d = %d" % (d, n, d * n)), W(name, "%d × %d = %d" % (m, n, p))])
        return ("%d times %d. %d times %d is %d, and %d times %d is %d. Together that makes %d." % (m, n, t, n, t * n, o, n, o * n, p),
                [W(name + "a", "%d × %d = %d" % (t, n, t * n)), W(name + "b", "%d × %d = %d" % (o, n, o * n)),
                 W(name, "%d × %d = %d + %d = %d" % (m, n, t * n, o * n, p))])
    if m <= 9 and n > 10:
        t, o = n - n % 10, n % 10
        if o == 0:
            d = t // 10
            return ("%d times %d is %d, so %d times %d is %d." % (m, d, m * d, m, n, p),
                    [W(name + "a", "%d × %d = %d" % (m, d, m * d)), W(name, "%d × %d = %d" % (m, n, p))])
        return ("%d times %d. %d times %d is %d, and %d times %d is %d. Together that makes %d." % (m, n, m, t, m * t, m, o, m * o, p),
                [W(name + "a", "%d × %d = %d" % (m, t, m * t)), W(name + "b", "%d × %d = %d" % (m, o, m * o)),
                 W(name, "%d × %d = %d + %d = %d" % (m, n, m * t, m * o, p))])
    # two bigger numbers: split the first into tens and ones
    t, o = m - m % 10, m % 10
    if o == 0:
        d = t // 10
        return ("%d times %d is %d, so %d times %d is %d." % (d, n, d * n, m, n, p),
                [W(name + "a", "%d × %d = %d" % (d, n, d * n)), W(name, "%d × %d = %d" % (m, n, p))])
    return ("%d times %d. %d times %d is %d, and %d times %d is %d. Together that makes %d." % (m, n, t, n, t * n, o, n, o * n, p),
            [W(name + "a", "%d × %d = %d" % (t, n, t * n)), W(name + "b", "%d × %d = %d" % (o, n, o * n)),
             W(name, "%d × %d = %d + %d = %d" % (m, n, t * n, o * n, p))])
