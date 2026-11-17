"""Write the review inputs for classifying the Grade 4 bank by reading it.

    python -X utf8 scripts/fixes/g4_classify_inputs.py [parts]

Grade 4 has about a thousand ORIGINAL questions (past papers, worksheets, hand-written).
Everything else is derived: variants carry their parent's id inside their own, and the
generated sets follow a small number of templates. So reviewers read
  data/bank-import/g4/originals-in-NN.json   every original question, in full
  data/bank-import/g4/templates-in.json      one entry per generator template, with examples
and the derived questions later take the verdict of their parent or template.
Reads the bank; changes nothing in it.
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

OUT = os.path.join(ROOT, "data", "bank-import", "g4")
PARENT = re.compile(r"EXT_G4_(?:FP_\d+_\d+|WS\d+_CH\d+_\d+)")
ORIGINAL_SOURCES = ("hand_crafted", "g4_ipm_worksheets_2")


def is_original(q):
    s = q.get("source") or ""
    return s in ORIGINAL_SOURCES or s.startswith("g4_mse_final") or s.startswith("previous_year")


def family(q):
    """('original', id) | ('variant', parent id) | ('template', key)."""
    if is_original(q):
        return ("original", q["id"])
    m = PARENT.search(q["id"])
    if m:
        return ("variant", m.group(0))
    if q.get("source") == "auto_generated":
        return ("template", "%s | %s" % (q.get("topicId"), re.sub(r"\d+(?:\.\d+)?", "N", q.get("questionText") or "")))
    m = re.match(r"^VAR_G4_(vary_[a-z_]+?)_V\d+", q["id"])
    return ("template", "v2 | %s" % (m.group(1) if m else q["id"]))


def dump(name, data):
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def brief(q, names):
    return {
        "id": q["id"], "source": q.get("source"), "filedUnder": names.get(q.get("node")) or "(nothing)",
        "label": q.get("subTopic"), "difficulty": q.get("difficulty"),
        "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
        "answer": q.get("correctAnswer"),
        "steps": [(s.get("text") if isinstance(s, dict) else s) for s in (q.get("stepByStep") or [])][:6],
    }


def main():
    parts = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    rows = bank.load_bank(4)
    ids = {q["id"] for q in rows}
    kinds = collections.Counter()
    templates = collections.defaultdict(list)
    orphans = 0
    for q in rows:
        kind, key = family(q)
        kinds[kind] += 1
        if kind == "template":
            templates[key].append(q)
        if kind == "variant" and key not in ids:
            orphans += 1
    print("%d questions: %s; %d variants whose parent is not in the bank" % (len(rows), dict(kinds), orphans))

    originals = sorted([q for q in rows if is_original(q)], key=lambda q: (q.get("source") or "", q["id"]))
    size = (len(originals) + parts - 1) // parts
    for i in range(parts):
        chunk = originals[i * size:(i + 1) * size]
        dump("originals-in-%02d.json" % (i + 1), [brief(q, names) for q in chunk])
        print("originals-in-%02d.json  %d questions (%s .. %s)" % (i + 1, len(chunk), chunk[0]["id"], chunk[-1]["id"]))

    out = []
    for key, qs in sorted(templates.items(), key=lambda kv: -len(kv[1])):
        out.append({
            "template": key, "count": len(qs), "filedUnder": names.get(qs[0].get("node")) or "(nothing)",
            "examples": [{
                "id": q["id"], "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
                "answer": q.get("correctAnswer"), "difficulty": q.get("difficulty"),
            } for q in qs[:4]],
        })
    dump("templates-in.json", out)
    print("templates-in.json  %d templates covering %d questions" % (len(out), sum(t["count"] for t in out)))


if __name__ == "__main__":
    main()
