"""Helpers for the Grade 4 quadrilateral and circle lessons (teach mode).

Shared by g4_gr4_quads.py and g4_gr4_circle.py (both written by the same writer).
A lesson is built from beats: B("what the teacher says", op, op, ..., ask=...).
"""
import collections
import hashlib
import importlib.util
import io
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
teach_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(teach_check)
bank = teach_check.bank


def hpick(qid, salt, options):
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return options[int(h[:8], 16) % len(options)]


def hnum(qid, salt, n):
    h = hashlib.md5(("%s|%s" % (qid, salt)).encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def fmt(v):
    f = Fraction(str(v)).limit_denominator(1000)
    if f.denominator == 1:
        return str(f.numerator)
    return ("%.3f" % float(f)).rstrip("0").rstrip(".")


def W(id, text, tone=None, label=False):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    if label:
        op["label"] = True
    return op


def G(text, id="q"):
    """The question, written first, as words."""
    return W(id, text, tone="given", label=True)


def L(id, text):
    return W(id, text, label=True)


def A(id, text, label=False):
    return W(id, text, tone="answer", label=label)


def FIG(id, spec):
    return {"op": "figure", "id": id, "spec": spec}


def T(text, nth=None):
    t = {"text": text}
    if nth:
        t["nth"] = nth
    return t


def mark(line, text, shape="underline", nth=None):
    return {"op": "mark", "line": line, "target": T(text, nth), "shape": shape}


def ring(line, text, nth=None):
    return mark(line, text, "circle", nth)


def box(line, text, nth=None):
    return mark(line, text, "box", nth)


def note(line, target, text, place=None, nth=None):
    op = {"op": "note", "line": line, "target": T(target, nth), "text": text}
    if place:
        op["place"] = place
    return op


def strike(line, target, text=None, nth=None):
    op = {"op": "strike", "line": line, "target": T(target, nth)}
    if text:
        op["note"] = text
    return op


def group(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [t if isinstance(t, dict) else T(t) for t in targets]}
    if label:
        op["label"] = label
    return op


def arc(line, frm, to):
    return {"op": "arc", "line": line, "from": frm if isinstance(frm, dict) else T(frm),
            "to": [t if isinstance(t, dict) else T(t) for t in to]}


def divide(line, by):
    return {"op": "divide", "line": line, "by": by}


def B(say, *ops, **kw):
    beat = {"say": say}
    ops = [op for op in ops if op is not None]
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def choose(choices, answer, if_not):
    return {"kind": "choose", "choices": list(choices), "answer": answer, "ifNot": if_not}


def ask(key, right, slips, if_not):
    """A choose-ask with the right choice placed by a stable hash."""
    pos = hnum(key, "pos", len(slips) + 1)
    choices = list(slips)
    choices.insert(pos, right)
    return choose(choices, pos, if_not)


THINK = {"kind": "think"}


def lesson(beats, origin="authored", check=None):
    out = {"origin": origin, "beats": beats}
    if check:
        out["check"] = {"variable": check[0], "value": str(check[1])}
    return out


# ── Reading the bank and the figures ─────────────────────────────────────────

def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def figures(topic):
    path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def figure_getter(topic):
    """F(qid) is the question's own picture; F(qid, i) is the picture for step i (0-based).
    Drawn under one id, so a later picture replaces the earlier one in place."""
    figs = figures(topic)

    def F(qid, i=None, id="f"):
        entry = figs.get(qid) or {}
        if i is None:
            spec = entry.get("figure")
        else:
            steps = entry.get("stepFigures") or []
            spec = steps[i] if i < len(steps) else None
        # No picture there: the beat simply goes without one (B drops a None op).
        return FIG(id, spec) if spec else None
    return F


def opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def key_text(q):
    return opts(q)["ABCD".find(q["correctAnswer"])]


def dump(topic, argv):
    """Print questions in full. argv: [what] [start end]; what = all | missing | fig | an id prefix."""
    what = argv[0] if argv else "all"
    qs = questions(topic)
    figs = figures(topic)
    if what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
    elif what == "ids":
        c = collections.Counter()
        for q in qs:
            print(q["id"], "|", q.get("difficulty"), "|", "FIG" if q["id"] in figs else "", "|", q["questionText"][:110].replace("\n", " "))
        print(len(qs), "questions")
        return
    elif what == "fig":
        for qid in argv[1:]:
            print(qid, json.dumps(figs.get(qid), ensure_ascii=False))
        return
    elif what == "hand":
        import re
        qs = [q for q in qs if q["id"].startswith("Q_") and not re.search(r"_V\d+$", q["id"])]
    elif what != "all":
        qs = [q for q in qs if q["id"].startswith(what)]
    total = len(qs)
    if len(argv) > 2:
        qs = qs[int(argv[1]):int(argv[2])]
    for q in qs:
        print("=" * 70)
        print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"), "| FIG" if q["id"] in figs else "")
        print("Q:", q["questionText"])
        for i, o in enumerate(opts(q)):
            print("   ", "ABCD"[i], o)
        print("KEY:", q.get("correctAnswer"))
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            print("MIS %s: %s" % (k, v))
    print(len(qs), "of", total, "questions")


def read(topic, argv):
    """Print built lessons compactly, to read them through. argv: ids, or 'rule'/'authored' start end."""
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    with io.open(path, encoding="utf-8") as f:
        part = json.load(f)
    by_id = {q["id"]: q for q in questions(topic)}
    if argv and argv[0] in ("rule", "authored"):
        ids = [qid for qid in sorted(part) if part[qid]["origin"] == argv[0]]
        if len(argv) > 2:
            ids = ids[int(argv[1]):int(argv[2])]
    else:
        ids = argv
    for qid in ids:
        q = by_id[qid]
        print("=" * 60)
        print(qid, "|", q["questionText"][:150].replace("\n", " "), "| KEY", key_text(q))
        for i, beat in enumerate(part[qid]["beats"]):
            print("%2d  %s" % (i + 1, beat["say"]))
            shown = []
            for op in beat.get("board", []):
                if op["op"] == "write":
                    shown.append("[%s]" % op["text"])
                elif op["op"] == "figure":
                    shown.append("(fig: %s)" % (op["spec"].get("note") or op["spec"].get("kind")))
                else:
                    t = op.get("target") or {}
                    shown.append("%s:%s%s" % (op["op"], t.get("text", op.get("by", "")),
                                              ("/" + op.get("text", op.get("note", ""))) if op.get("text") or op.get("note") else ""))
            if shown:
                print("      " + "  ".join(shown))
            if beat.get("ask"):
                a = beat["ask"]
                if a["kind"] == "think":
                    print("      ASK think")
                else:
                    print("      ASK %s -> %s | %s" % (a["choices"], a["choices"][a["answer"]], a["ifNot"]))


def build(topic, rules, authored_prefix):
    """Write data/teach/parts/g4-<topic>.json from rule functions and authored lesson files."""
    authored = {}
    for filename in sorted(os.listdir(HERE)):
        if filename.startswith(authored_prefix) and filename.endswith(".py"):
            authored.update(__import__(filename[:-3]).LESSONS)
    out = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    qs = questions(topic)
    ids = {q["id"] for q in qs}
    for qid in authored:
        if qid not in ids:
            print("authored lesson for an id not in the topic: %s" % qid)
    part = {}
    counts = collections.Counter()
    missing = []
    problems = []
    for q in qs:
        qid = q["id"]
        script = None
        if qid in authored:
            script = authored[qid]
            if callable(script):
                script = script(q)
            counts["authored"] += 1
        else:
            for fn in rules:
                try:
                    script = fn(q)
                except Exception as e:  # a rule that cannot handle the question says so
                    problems.append("%s: rule %s raised %r" % (qid, fn.__name__, e))
                    script = None
                if script:
                    counts[fn.__name__] += 1
                    break
        if script is None:
            missing.append(qid)
            continue
        found = teach_check.check_script(qid, script, q)
        if found:
            problems += found
            continue
        part[qid] = script
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote %d lessons of %d questions" % (len(part), len(qs)))
    for name, n in sorted(counts.items()):
        print("  %-28s %d" % (name, n))
    if missing:
        print("%d with no lesson yet:" % len(missing))
        for qid in missing[:20]:
            print("  " + qid)
    if problems:
        print("%d PROBLEMS" % len(problems))
        for p in problems[:60]:
            print("  " + p)
