"""List every distinct wording among the auto-generated Grade 5 questions.

    python -X utf8 scripts/fixes/gen/generated_hints_wordings.py            # wordings with counts
    python -X utf8 scripts/fixes/gen/generated_hints_wordings.py --full     # every question in full
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")


def load():
    with io.open(SEED, encoding="utf-8") as f:
        return [q for q in json.load(f)["questions"] if q.get("source") == "auto_generated_v2" and q.get("topicId") == "grade5"]


def family(qid):
    return re.fullmatch(r"VAR_G5_vary_(.+)_V\d+", qid).group(1)


def main():
    qs = load()
    print("total", len(qs))
    if "--full" in sys.argv:
        for q in sorted(qs, key=lambda q: (family(q["id"]), q["questionText"])):
            opts = [o.get("text") if isinstance(o, dict) else o for o in q["options"]]
            print("%s | %r | %s | %s | sub=%s | steps=%d" % (q["id"], q["questionText"], opts, q["correctAnswer"],
                                                         q.get("subTopic"), len(q.get("stepByStep") or [])))
        return
    groups = collections.defaultdict(list)
    for q in qs:
        shape = re.sub(r"\d+(?:\.\d+)?", "#", q["questionText"])
        groups[(family(q["id"]), shape)].append(q)
    fams = collections.Counter(family(q["id"]) for q in qs)
    for fam in sorted(fams):
        print("\n== %s (%d)" % (fam, fams[fam]))
        for (f, shape), items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            if f != fam:
                continue
            q = items[0]
            opts = [o.get("text") if isinstance(o, dict) else o for o in q["options"]]
            print("%4d  %r" % (len(items), shape))
            print("        e.g. %s %r %s %s" % (q["id"], q["questionText"], opts, q["correctAnswer"]))


if __name__ == "__main__":
    main()
