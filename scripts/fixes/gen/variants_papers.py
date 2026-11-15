"""Build data/question-fixes/parts/variants-papers.json.

    python -X utf8 scripts/fixes/gen/variants_papers.py                    # build and write the part file
    python -X utf8 scripts/fixes/gen/variants_papers.py --sample <rule> 3  # print some of one rule's output, write nothing
    python -X utf8 scripts/fixes/gen/variants_papers.py --sample <rule> 3 7  # ... starting at the 7th match

Job 1: generated variants (source variant_generator_phase*), fixed by the rules in variants_papers_rules*.py.
        One rule per wording, matched with re.fullmatch; a question matching no rule is left alone.
Job 2: past papers (EXT_G5_FP_*), fixed by hand in variants_papers_hand_*.py (each has a dict HAND).
Ids in scripts/fixes/answers_ids.txt, and every id in data/question-fixes/parts/answers.json (read at
build time), belong to the answers workstream and are never touched. Every fix is run through check.check_entry before
it is written; one that does not pass is left out and reported.
"""
import collections
import glob
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
from check import PARTS, check_entry, load_seed  # noqa: E402
from variants_papers_util import Skip  # noqa: E402

PART = "variants-papers"
RESERVED = set(io.open(os.path.join(HERE, "..", "answers_ids.txt"), encoding="utf-8").read().split())
# The "answers" workstream owns every id in its part file as well: leave those out too.
ANSWERS_PART = os.path.join(PARTS, "answers.json")
OWNED_BY_ANSWERS = set()
if os.path.exists(ANSWERS_PART):
    with io.open(ANSWERS_PART, encoding="utf-8") as _f:
        OWNED_BY_ANSWERS = set(json.load(_f))
RESERVED |= OWNED_BY_ANSWERS


def all_rules():
    rules = []
    for name in ("variants_papers_rules", "variants_papers_rules2", "variants_papers_rules3"):
        rules += importlib.import_module(name).RULES
    return rules


def hand_fixes():
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, "variants_papers_hand_*.py"))):
        module = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        for qid, fix in module.HAND.items():
            if qid in out:
                sys.exit("hand fix given twice: %s" % qid)
            out[qid] = fix
    return out


def show(q, fix):
    print("=== %s  key=%s" % (q["id"], q.get("correctAnswer")))
    print("Q: " + q["questionText"])
    print("   " + " | ".join("%s) %s" % (l, o.get("text", "") if isinstance(o, dict) else o) for l, o in zip("ABCD", q.get("options", []))))
    for i, h in enumerate(q.get("hints") or []):
        print("  old H%d: %s" % (i + 1, h))
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  old S%d: %s" % (i + 1, s.get("text", "")))
    for i, h in enumerate(fix.get("hints", [])):
        print("  NEW H%d: %s" % (i + 1, h))
    for i, s in enumerate(fix.get("steps", [])):
        print("  NEW S%d: %s%s" % (i + 1, s["text"], ("  [latex: %s]" % s["latex"]) if s.get("latex") else ""))


def main():
    questions = load_seed()
    sample = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--sample" else None
    sample_n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    sample_from = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    rules = all_rules()
    part, counts, skipped, rejected, shown = {}, collections.Counter(), [], [], 0

    for qid in sorted(questions):
        q = questions[qid]
        if not (q.get("source") or "").startswith("variant_generator_phase"):
            continue
        for name, rule in rules:
            try:
                fix = rule(q)
            except Skip as why:
                if qid not in RESERVED:
                    skipped.append("%s [%s]: %s" % (qid, name, why))
                break
            if fix is None:
                continue
            if qid in RESERVED:
                counts["(reserved, not touched)"] += 1
                break
            problems = check_entry(qid, fix, q, PART)
            if problems:
                rejected.append("%s [%s]: %s" % (qid, name, "; ".join(problems)))
                break
            part[qid] = fix
            counts[name] += 1
            if sample == name:
                if counts[name] > sample_from and shown < sample_n:
                    show(q, fix)
                    shown += 1
            break

    hand = hand_fixes()
    for qid, fix in hand.items():
        if qid in RESERVED:
            counts["(hand fix left out: id belongs to the answers workstream)"] += 1
            skipped.append("%s [hand]: belongs to the answers workstream" % qid)
            continue
        if qid in part:
            sys.exit("hand fix for a question a rule already fixes: %s" % qid)
        if qid not in questions:
            sys.exit("hand fix for an unknown id: %s" % qid)
        problems = check_entry(qid, fix, questions[qid], PART)
        if problems:
            rejected.append("%s [hand]: %s" % (qid, "; ".join(problems)))
            continue
        part[qid] = fix
        counts["hand (past papers)"] += 1

    print("fixes by rule:")
    for name, n in sorted(counts.items()):
        print("  %-34s %d" % (name, n))
    print("  %-34s %d" % ("TOTAL written", len(part)))
    if skipped:
        print("\n%d matched a rule but were left alone:" % len(skipped))
        for s in skipped:
            print("  " + s)
    if rejected:
        print("\n%d did not pass the checker and were left out:" % len(rejected))
        for r in rejected:
            print("  " + r)
    if sample:
        print("\n(sample only: nothing written)")
        return
    path = os.path.join(PARTS, PART + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(part.items())), f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("\nwrote %s" % path)


if __name__ == "__main__":
    main()
