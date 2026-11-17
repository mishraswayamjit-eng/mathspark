"""Figures for the imported Grade 5 questions outside area, angles and triangles.

    python -X utf8 scripts/figures/authoring/imported_other.py            # build the part
    python -X utf8 scripts/figures/authoring/imported_other.py show ID... # print the entries of these ids

Writes data/question-figures/parts/imported-other.json ({ "<question id>": QuestionVisual }).
The questions' numbers are written out family by family in the spec modules
imported_other_s*.py; the engines in imported_other_lib.py draw them, work out
the step-figure slots from each question's own steps, and check every entry with
the checker (scripts/figures/validate.py) before it is kept.

Then:  python -X utf8 scripts/figures/validate.py --part data/question-figures/parts/imported-other.json
"""
import collections
import glob
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import imported_other_lib as lib  # noqa: E402

OUT = os.path.join(lib.validate.ROOT, "data", "question-figures", "parts", "imported-other.json")


def brief(f):
    if f is None:
        return "-"
    k = f["kind"]
    if k == "barModel":
        body = " // ".join("%s{%s}[%s]" % (b.get("label", ""), b.get("brace", ""), "|".join(s.get("label", "_") for s in b["segments"])) for b in f["bars"])
    elif k == "journey":
        body = " ".join("%s --(%s; %s)--" % (p, l.get("top", ""), l.get("bottom", "")) for p, l in zip(f["places"], f["legs"])) + " " + f["places"][-1]
    elif k == "table":
        body = (" H:" + ",".join(f["headers"]) if "headers" in f else "") + " " + " / ".join(",".join(r) for r in f["rows"])
    else:
        body = json.dumps(dict((a, b) for a, b in f.items() if a not in ("kind", "note", "highlight")), ensure_ascii=False)
    return "%s %s  hl=%s  note=%s" % (k, body, ",".join(f.get("highlight", [])), f.get("note", ""))


def main():
    for path in sorted(glob.glob(os.path.join(HERE, "imported_other_s*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        before = len(lib.E)
        spec.loader.exec_module(mod)
        print("%-34s %4d entries" % (name, len(lib.E) - before))

    if len(sys.argv) > 2 and sys.argv[1] == "brief":
        # One line per figure, for reading many entries at once: brief ID... | brief <topic> | brief <module prefix>
        want = sys.argv[2:]
        for qid, e in lib.E.items():
            q = lib.POOL[qid]
            if not (q["node"] in want or qid in want or qid[-12:] in want):
                continue
            print("## %s  %s" % (qid[-12:] if qid.startswith("AIGEN") else qid, q["questionText"].replace("\n", " ")[:110]))
            print("   before: " + brief(e.get("figure")))
            steps = q.get("stepByStep") or []
            for i, f in enumerate(e.get("stepFigures") or []):
                print("   s%d %s\n        -> %s" % (i, (steps[i].get("text", "")[:60] + " | " + (steps[i].get("latex") or "")[:70]).replace("\n", " "), brief(f)))
        return

    if len(sys.argv) > 2 and sys.argv[1] == "show":
        for sid in sys.argv[2:]:
            q = lib.Q(sid)
            print("## " + q["id"])
            print(json.dumps(lib.E.get(q["id"]), ensure_ascii=False, indent=1))
        return

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(lib.E.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")

    by_topic, by_kind, with_steps = collections.Counter(), collections.Counter(), 0
    pool = collections.Counter(q["node"] for q in lib.POOL.values())
    for qid, e in lib.E.items():
        by_topic[lib.POOL[qid]["node"]] += 1
        fig = e.get("figure") or next(f for f in e["stepFigures"] if f)
        by_kind[fig["kind"]] += 1
        with_steps += 1 if e.get("stepFigures") else 0
    print("\nwrote %d entries (%d with step figures) of %d questions" % (len(lib.E), with_steps, len(lib.POOL)))
    for topic in sorted(pool):
        print("  %4d of %4d  %s" % (by_topic[topic], pool[topic], topic))
    print("by kind: " + ", ".join("%s %d" % kv for kv in by_kind.most_common()))
    if lib.PROBLEMS:
        print("\n%d LEFT OUT OR TRIMMED" % len(lib.PROBLEMS))
        for p in lib.PROBLEMS:
            print("  " + p)


if __name__ == "__main__":
    main()
