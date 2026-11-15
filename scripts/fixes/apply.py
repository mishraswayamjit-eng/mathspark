"""Apply checked fixes to the question bank, and build the file the app serves them from.

    python -X utf8 scripts/fixes/apply.py            # check everything, show what would change
    python -X utf8 scripts/fixes/apply.py --write    # write the seed file and the served fixes

Two things are written, from the same part files:
  1. data/mathspark_complete_seed.json: the source of truth, used by every other
     offline check (figures, narration) and by the next re-seed of the database.
  2. src/data/questionFixes/fixes.json: the corrected fields for each fixed
     question. The app lays these over what the database returns, so the fixes
     reach children as soon as the app is deployed, without waiting for a re-seed.

Nothing is written unless every part passes scripts/fixes/check.py. Answer-key
letters are never changed here: a fix that tried to would stop the run, because
grading reads the key from the database.
"""
import argparse
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import PARTS, ROOT, SEED, check_entry  # noqa: E402

OUT = os.path.join(ROOT, "src", "data", "questionFixes", "fixes.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    with io.open(SEED, encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    # The seed file is one compact line; make sure we can write it back the same way.
    same_format = json.dumps(data, ensure_ascii=True, separators=(",", ":")) == raw.rstrip("\n")
    by_id = {q["id"]: q for q in data["questions"]}

    fixes = {}
    problems = []
    for path in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
        name = os.path.splitext(os.path.basename(path))[0]
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        for qid, fix in part.items():
            q = by_id.get(qid)
            if q is None or q.get("topicId") != "grade5":
                problems.append("%s: %s is not a Grade 5 question" % (name, qid))
                continue
            if qid in fixes:
                problems.append("%s: %s is fixed in two parts" % (name, qid))
                continue
            problems += check_entry(qid, fix, q, name)
            if "correctAnswer" in fix and fix["correctAnswer"] != q.get("correctAnswer"):
                problems.append("%s: changes the answer-key letter, which this tool does not do" % qid)
            fixes[qid] = fix

    if problems:
        print("%d PROBLEMS, nothing written" % len(problems))
        for p in problems[:80]:
            print("  " + p)
        sys.exit(1)

    served = {}
    counts = {"hints": 0, "steps": 0, "options": 0, "questionText": 0}
    for qid in sorted(fixes):
        fix = fixes[qid]
        q = by_id[qid]
        out = {}
        if "questionText" in fix:
            q["questionText"] = fix["questionText"]
            out["questionText"] = fix["questionText"]
            counts["questionText"] += 1
        if "options" in fix:
            for i, text in enumerate(fix["options"]):
                if isinstance(q["options"][i], dict):
                    q["options"][i]["text"] = text
                else:
                    q["options"][i] = text
            out["options"] = fix["options"]
            counts["options"] += 1
        if "hints" in fix:
            q["hints"] = list(fix["hints"])
            out["hints"] = fix["hints"]
            counts["hints"] += 1
        if "steps" in fix:
            q["stepByStep"] = [{"step": i + 1, "text": s["text"], "latex": s.get("latex", "")} for i, s in enumerate(fix["steps"])]
            out["steps"] = q["stepByStep"]
            counts["steps"] += 1
        served[qid] = out

    print("%d questions fixed: %s" % (len(served), ", ".join("%d %s" % (n, k) for k, n in counts.items())))
    if not same_format:
        print("NOTE: the seed file is not in the compact one-line form this tool writes; the diff will be large.")
    if not args.write:
        print("dry run: nothing written (use --write)")
        return

    with io.open(SEED, "w", encoding="utf-8", newline="") as f:
        # The seed file is ASCII-only JSON on one line: keep it so, and the diff shows only real changes.
        f.write(json.dumps(data, ensure_ascii=True, separators=(",", ":")))
        if raw.endswith("\n"):
            f.write("\n")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(served, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print("wrote %s and %s" % (os.path.relpath(SEED, ROOT), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()
