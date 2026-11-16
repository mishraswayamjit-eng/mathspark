"""Move narration entries to the part file of the topic their question now belongs to.

    python -X utf8 scripts/speech/rehome.py            # show what would move
    python -X utf8 scripts/speech/rehome.py --write

A question's topic comes from its sub-topic label (common.topic_of). When a label is
corrected in the bank (data/bank/), the question's narration is still right but sits in the old
topic's part file, which validate.py reports. This moves the entry, unchanged.
"""
import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PARTS, TOPICS, load_grade5, topic_of  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    questions = {q["id"]: q for q in load_grade5()}
    parts, was_sorted = {}, {}
    for slug in TOPICS:
        with io.open(os.path.join(PARTS, slug + ".json"), encoding="utf-8") as f:
            parts[slug] = json.load(f)
        keys = list(parts[slug])
        was_sorted[slug] = keys == sorted(keys)

    moved = []
    for slug in TOPICS:
        for qid in list(parts[slug]):
            q = questions.get(qid)
            if q is None:
                continue
            home = topic_of(q)
            if home != slug:
                if qid in parts[home]:
                    raise SystemExit("%s is already in %s as well as %s; stopping." % (qid, home, slug))
                parts[home][qid] = parts[slug].pop(qid)
                moved.append((qid, slug, home))

    for qid, old, new in moved:
        print("%-34s %s -> %s" % (qid, old, new))
    print("%d entries to move" % len(moved))
    if not args.write or not moved:
        if not args.write:
            print("nothing written (use --write)")
        return
    touched = set(old for _, old, _ in moved) | set(new for _, _, new in moved)
    for slug in sorted(touched):
        part = parts[slug]
        if was_sorted[slug]:
            part = {k: part[k] for k in sorted(part)}
        with io.open(os.path.join(PARTS, slug + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("wrote %s.json" % slug)


if __name__ == "__main__":
    main()
