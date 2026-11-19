"""Check narration written for newly added Grade 5 questions, and merge it into the topic parts.

    python -X utf8 scripts/speech/check_new.py <file>            # check only
    python -X utf8 scripts/speech/check_new.py <file> --merge    # check, then add to data/question-speech/parts/

<file> is { "<question id>": entry } in the same form as a part file. Every entry is checked
by the same rules as validate.py. With --merge, each entry is added to the part of the topic
its question belongs to (common.topic_of); an existing entry for the same id is replaced.
Nothing is written if any entry has a problem.
"""
import collections
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
import validate  # noqa: E402


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not files:
        raise SystemExit(__doc__)
    questions = {q["id"]: q for q in common.load_grade5()}
    new = {}
    problems = []
    for path in files:
        with io.open(path, encoding="utf-8") as f:
            data = json.load(f)
        for qid, entry in data.items():
            q = questions.get(qid)
            if q is None:
                problems.append("%s is not a Grade 5 question" % qid)
                continue
            found = validate.check_entry(qid, entry, q)
            problems += found
            if not found:
                new[qid] = entry
    wanted = [qid for qid in questions if qid.startswith("G5A_")]
    missing = [qid for qid in wanted if qid not in new]
    print("%d entries pass, %d problems; %d of %d new Grade 5 questions still without narration" % (
        len(new), len(problems), len(missing), len(wanted)))
    for p in problems[:60]:
        print("  " + p)
    if problems:
        sys.exit(1)
    if "--merge" not in sys.argv:
        return
    by_topic = collections.defaultdict(dict)
    for qid, entry in new.items():
        by_topic[common.topic_of(questions[qid])][qid] = entry
    for slug, entries in sorted(by_topic.items()):
        path = os.path.join(common.PARTS, slug + ".json")
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        part.update(entries)
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("  %-22s +%d" % (slug, len(entries)))


if __name__ == "__main__":
    main()
