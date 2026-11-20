"""Small authoring kit for Grade 4 "Explain it to me" lessons (gr4_numbers, gr4_squares).

A lesson is a list of beats made with b(say, *things). A thing is a board op (G, W, A, U, C,
BX, N, X, ARC, GRP, FIG, CLR) or an ask (Q, THINK). Lines get ids by themselves; a mark points
at the last line written unless on="name" names another (give a line a name with name="...").
A line that is not plain maths is marked as a label automatically.
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

_spec = importlib.util.spec_from_file_location("teach_validate", os.path.join(ROOT, "scripts", "teach", "validate.py"))
tv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tv)


def h(qid, salt=""):
    return int(hashlib.md5((qid + "|" + str(salt)).encode("utf-8")).hexdigest(), 16)


def pick(qid, salt, options):
    return options[h(qid, salt) % len(options)]


# ── Board ops ────────────────────────────────────────────────────────────────

def _w(text, tone, name, lab):
    return {"_k": "write", "text": text, "tone": tone, "name": name, "lab": lab}


def G(text, name=None, lab=None):
    """The question, as given."""
    return _w(text, "given", name, lab)


def W(text, name=None, lab=None):
    """A line of working."""
    return _w(text, "work", name, lab)


def A(text, name=None, lab=None):
    """The final answer: written large and ringed."""
    return _w(text, "answer", name, lab)


def _t(t):
    if isinstance(t, tuple):
        return {"text": t[0], "nth": t[1]}
    return {"text": t}


def U(t, on=None):
    return {"_k": "mark", "target": _t(t), "shape": "underline", "on": on}


def C(t, on=None):
    return {"_k": "mark", "target": _t(t), "shape": "circle", "on": on}


def BX(t, on=None):
    return {"_k": "mark", "target": _t(t), "shape": "box", "on": on}


def N(t, text, on=None, below=False):
    return {"_k": "note", "target": _t(t), "text": text, "on": on, "below": below}


def X(t, note=None, on=None):
    return {"_k": "strike", "target": _t(t), "note": note, "on": on}


def ARC(frm, to, on=None):
    return {"_k": "arc", "from": _t(frm), "to": [_t(x) for x in to], "on": on}


def GRP(targets, label=None, on=None):
    return {"_k": "group", "targets": [_t(x) for x in targets], "label": label, "on": on}


def FIG(spec):
    return {"_k": "figure", "spec": spec}


def CLR():
    return {"_k": "clear"}


def Q(choices, ifnot, answer=0, keep=False):
    """Ask the child to choose. Write the right choice first; the order is turned by a stable hash."""
    return {"_k": "ask", "choices": list(choices), "answer": answer, "ifNot": ifnot, "keep": keep}


THINK = {"_k": "think"}


def b(say, *things):
    return (say, things)


# ── Figures ──────────────────────────────────────────────────────────────────

def chart(number, marked=(), note=None):
    """A place-value chart. `marked` are digit positions counted from the left, 0 first."""
    spec = {"kind": "placeChart", "number": str(number)}
    if note:
        spec["note"] = note
    if marked:
        spec["highlight"] = ["d%d" % i for i in marked]
    return spec


def table(headers, rows, note=None, highlight=None):
    spec = {"kind": "table", "headers": [str(x) for x in headers], "rows": [[str(c) for c in r] for r in rows]}
    if note:
        spec["note"] = note
    if highlight:
        spec["highlight"] = highlight
    return spec


def nline(lo, hi, step, points, hops=(), note=None):
    """A number line. points: (at, label or None). hops: (from, to, label or None)."""
    spec = {"kind": "numberLine", "min": lo, "max": hi, "step": step, "tickLabels": "none", "points": []}
    for at, label in points:
        p = {"at": at}
        if label:
            p["label"] = label
        spec["points"].append(p)
    if hops:
        spec["hops"] = []
        for f, t, label in hops:
            hop = {"from": f, "to": t}
            if label:
                hop["label"] = label
            spec["hops"].append(hop)
    if note:
        spec["note"] = note
    return spec


def dots(rows, cols, note=None):
    """A grid of dots: rows by cols."""
    spec = {"kind": "grid", "rows": rows, "cols": cols, "dots": True}
    if note:
        spec["note"] = note
    return spec


def square(side, inside=None, note=None):
    spec = {"kind": "rectangle", "square": True, "length": str(side), "breadth": str(side)}
    if inside:
        spec["inside"] = inside
    if note:
        spec["note"] = note
    return spec


# ── Building ─────────────────────────────────────────────────────────────────

def build(qid, beats, origin="authored", check=None):
    variable, at = None, None
    if check:
        variable, at = check["variable"], tv.value_of(check["value"])
    out = []
    n_line, n_fig = 0, 0
    names = {}
    last = None
    for bi, (say, things) in enumerate(beats):
        beat = {"say": say}
        ops = []
        for t in things:
            k = t["_k"]
            if k == "ask":
                choices, ans = t["choices"], t["answer"]
                if not t["keep"]:
                    r = h(qid, "ask%d" % bi) % len(choices)
                    choices = choices[r:] + choices[:r]
                    ans = (ans - r) % len(choices)
                beat["ask"] = {"kind": "choose", "choices": choices, "answer": ans, "ifNot": t["ifNot"]}
            elif k == "think":
                beat["ask"] = {"kind": "think"}
            elif k == "write":
                n_line += 1
                lid = "l%d" % n_line
                if t["name"]:
                    names[t["name"]] = lid
                last = lid
                op = {"op": "write", "id": lid, "text": t["text"]}
                if t["tone"] != "work":
                    op["tone"] = t["tone"]
                lab = t["lab"]
                if lab is None:
                    # Words make a line a label, even when a "?" would let it pass unchecked as maths.
                    matter = tv.check_line(t["text"], variable, at)
                    lab = bool(matter and matter.startswith("is not plain maths")) or bool(re.search(r"[A-Za-z]{3,}", t["text"]))
                if lab:
                    op["label"] = True
                ops.append(op)
                if t["tone"] == "answer":
                    ops.append({"op": "mark", "line": lid, "target": {"text": t["text"]}, "shape": "circle"})
            elif k == "figure":
                n_fig += 1
                ops.append({"op": "figure", "id": "f%d" % n_fig, "spec": t["spec"]})
            elif k == "clear":
                ops.append({"op": "clear"})
            else:
                line = names[t["on"]] if t.get("on") else last
                if k == "mark":
                    ops.append({"op": "mark", "line": line, "target": t["target"], "shape": t["shape"]})
                elif k == "note":
                    op = {"op": "note", "line": line, "target": t["target"], "text": t["text"]}
                    if t["below"]:
                        op["place"] = "below"
                    ops.append(op)
                elif k == "strike":
                    op = {"op": "strike", "line": line, "target": t["target"]}
                    if t["note"]:
                        op["note"] = t["note"]
                    ops.append(op)
                elif k == "arc":
                    ops.append({"op": "arc", "line": line, "from": t["from"], "to": t["to"]})
                elif k == "group":
                    op = {"op": "group", "line": line, "targets": t["targets"]}
                    if t["label"]:
                        op["label"] = t["label"]
                    ops.append(op)
        if ops:
            beat["board"] = ops
        out.append(beat)
    script = {"origin": origin}
    if check:
        script["check"] = check
    script["beats"] = out
    return script


def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def write_part(topic, lessons):
    """Check every lesson; write the ones that pass (in bank order); say what is missing."""
    qs = questions(topic)
    good = {}
    bad = 0
    for q in qs:
        script = lessons.get(q["id"])
        if script is None:
            continue
        problems = tv.check_script(q["id"], script, q)
        if problems:
            bad += 1
            for p in problems[:6]:
                print("  " + p)
        else:
            good[q["id"]] = script
    extra = sorted(set(lessons) - {q["id"] for q in qs})
    if extra:
        print("  NOT IN TOPIC: %s" % ", ".join(extra))
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(good, f, ensure_ascii=False, indent=1)
        f.write("\n")
    kinds = {}
    for s in good.values():
        kinds[s["origin"]] = kinds.get(s["origin"], 0) + 1
    missing = [q["id"] for q in qs if q["id"] not in lessons]
    print("%s: wrote %d of %d (%s); %d with problems; %d not written yet" % (
        topic, len(good), len(qs), ", ".join("%d %s" % (v, k) for k, v in sorted(kinds.items())), bad, len(missing)))
    if missing and len(missing) <= 40:
        print("  missing: " + " ".join(missing))
