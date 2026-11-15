"""Build data/teach/parts/place-value.json: a lesson for every place-value question.

    python -X utf8 scripts/teach/gen/place_value_build.py          # write the part file
    python -X utf8 scripts/teach/gen/place_value_build.py --stats  # also say which rule made what

Generated families are written by rule (place_value_rules_a.py, place_value_rules_b.py).
One-off questions are written by hand (place_value_authored_*.py).
Then check with: python -X utf8 scripts/teach/validate.py --part place-value
"""
import collections
import sys

from place_value_lib import finish, load_questions, write_part
import place_value_rules_a
import place_value_rules_b
import place_value_authored_a
import place_value_authored_b
import place_value_authored_c


def main():
    rules = place_value_rules_a.RULES + place_value_rules_b.RULES
    authored = {}
    for mod in (place_value_authored_a, place_value_authored_b, place_value_authored_c):
        for qid, beats in mod.LESSONS.items():
            assert qid not in authored, qid
            authored[qid] = beats

    lessons = {}
    made = collections.Counter()
    missing = []
    questions = load_questions()
    ids = {q["id"] for q in questions}
    for qid in authored:
        assert qid in ids, "authored lesson for an unknown question: %s" % qid
    for q in questions:
        qid = q["id"]
        if qid in authored:
            lessons[qid] = finish(qid, "authored", authored[qid])
            made["by hand"] += 1
            continue
        for rule in rules:
            beats = rule(q)
            if beats:
                lessons[qid] = finish(qid, "rule", beats)
                made[rule.__name__] += 1
                break
        else:
            missing.append(q)
    write_part(lessons)
    print("wrote %d lessons for %d questions" % (len(lessons), len(questions)))
    if "--stats" in sys.argv:
        for name, n in sorted(made.items()):
            print("  %-22s %d" % (name, n))
    for q in missing:
        print("  NO LESSON  %s  %s" % (q["id"], q["questionText"][:90]))


if __name__ == "__main__":
    main()
