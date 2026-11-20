"""Helpers for writing Grade 4 lessons (used by g4_gr4_ratio.py and g4_gr4_ages.py)."""
import hashlib
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


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
    """A line of working in words (not checked: keep it true)."""
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


def N(line, text, note, place="below", nth=1):
    return {"op": "note", "line": line, "target": T(text, nth), "text": note, "place": place}


def X(line, text, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": T(text, nth)}
    if note:
        op["note"] = note
    return op


def grp(line, targets, label=None):
    op = {"op": "group", "line": line, "targets": [T(t) if isinstance(t, str) else T(*t) for t in targets]}
    if label:
        op["label"] = label
    return op


def last(line_text, text):
    """nth of the LAST occurrence of `text` on a line (the result of a sum, usually)."""
    return line_text.count(text)


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


def segs(n, tone=None, label=None):
    """n equal pieces."""
    return [seg(label, 1, tone) for _ in range(n)]


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


def table(headers, rows, note=None):
    spec = {"kind": "table", "headers": headers, "rows": rows}
    if note:
        spec["note"] = note
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


# ── Building a part ──────────────────────────────────────────────────────────

def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def _checker():
    path = os.path.join(ROOT, "scripts", "teach", "validate.py")
    spec = importlib.util.spec_from_file_location("teach_validate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(topic, lessons):
    """Check every lesson; write the ones that pass to data/teach/parts/g4-<topic>.json."""
    checker = _checker()
    qs = {q["id"]: q for q in questions(topic)}
    good = {}
    bad = 0
    for qid in qs:
        if qid not in lessons:
            continue
        found = checker.check_script(qid, lessons[qid], qs[qid])
        if found:
            bad += 1
            for p in found[:8]:
                print("PROBLEM  " + p)
        else:
            good[qid] = lessons[qid]
    for qid in lessons:
        if qid not in qs:
            print("PROBLEM  %s is not a question of %s" % (qid, topic))
    out = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(good, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in qs if qid not in lessons]
    print("%s: wrote %d lessons of %d questions; %d did not pass; %d not written yet" % (
        topic, len(good), len(qs), bad, len(missing)))
    if missing:
        print("  no lesson yet: " + ", ".join(missing[:12]) + (" ..." if len(missing) > 12 else ""))
