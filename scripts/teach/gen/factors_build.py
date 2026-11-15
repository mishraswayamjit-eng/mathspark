"""Build data/teach/parts/factors.json: a lesson for every Grade 5 question in the factors topic.

    python -X utf8 scripts/teach/gen/factors_build.py

Generated families are written by rule (factors_rules*.py). One-off questions are written
by hand (factors_authored_*.py). Then check with:

    python -X utf8 scripts/teach/validate.py --part factors
"""
import collections
import glob
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402
from factors_rules import hcf_lesson  # noqa: E402
from factors_rules_lcm import lcm_lesson  # noqa: E402
from factors_rules_div import divisible_lesson, equation_lesson  # noqa: E402

OUT = os.path.join(ROOT, "data", "teach", "parts", "factors.json")
GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def option_numbers(q):
    return [int(o.get("text", "") if isinstance(o, dict) else o) for o in q.get("options", [])]


def by_rule(q):
    """(wording, lesson) for a generated question, or (None, None)."""
    text = q["questionText"].strip()
    m = re.fullmatch(r"Find the HCF of (\d+) and (\d+)\.", text)
    if m:
        return "Find the HCF of a and b", hcf_lesson(q["id"], int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"Find the LCM of (\d+) and (\d+)\.", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        lesson = lcm_lesson(q["id"], a, b)
        big = max(a, b)
        low = a * b // __import__("math").gcd(a, b)
        how = "one divides the other" if low == big else ("count up both tables" if max(low // a, low // b) <= 6 and big <= 20 else "prime factors")
        return "Find the LCM of a and b (%s)" % how, lesson
    m = re.fullmatch(r"Which of the following numbers is divisible by (\d+)\?", text)
    if m:
        key = "ABCD".index(q["correctAnswer"])
        return "Which number is divisible by d", divisible_lesson(q["id"], int(m.group(1)), option_numbers(q), key)
    m = re.fullmatch(r"Solve: (\d+)x ([+−-]) (\d+) = (\d+)", text)
    if m:
        sign = "+" if m.group(2) == "+" else "−"
        return "Solve: ax ± b = c", equation_lesson(q["id"], int(m.group(1)), sign, int(m.group(3)), int(m.group(4)))
    return None, None


def lint(qid, script):
    """Things the checker does not look at, but a reader would trip on."""
    notes = []
    lines = {}
    for i, beat in enumerate(script["beats"]):
        for op in beat.get("board", []):
            if op["op"] == "write":
                lines[op["id"]] = op["text"]
            if op["op"] == "clear":
                lines = {}
            targets = []
            if op["op"] in ("mark", "strike", "note"):
                targets = [op["target"]]
            elif op["op"] == "arc":
                targets = [op["from"]] + op["to"]
            elif op["op"] == "group":
                targets = op["targets"]
            text = lines.get(op.get("line"), "")
            for t in targets:
                # A mark on a number must land on the whole number, not on digits inside a longer one,
                # unless the line is a bare number (digits are marked on purpose there).
                if not re.fullmatch(r"\d+", t["text"]) or re.fullmatch(r"[\d,]+", text):
                    continue
                pos, start = -1, 0
                for _ in range(t.get("nth", 1)):
                    pos = text.find(t["text"], start)
                    start = pos + 1
                    if pos == -1:
                        break
                if pos == -1:
                    continue
                before = text[pos - 1] if pos > 0 else " "
                after = text[pos + len(t["text"])] if pos + len(t["text"]) < len(text) else " "
                if before.isdigit() or after.isdigit():
                    notes.append("%s beat %d: the mark on %r lands inside a longer number on \"%s\"" % (qid, i + 1, t["text"], text))
    return notes


def main():
    questions = [q for q in load_grade5() if topic_of(q) == "factors"]
    lessons = collections.OrderedDict()
    wordings = collections.Counter()
    authored = {}
    for path in sorted(glob.glob(os.path.join(HERE, "factors_authored_*.py"))):
        module = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        for qid, script in module.LESSONS.items():
            if qid in authored:
                sys.exit("two hand-written lessons for %s" % qid)
            authored[qid] = script

    missing = []
    for q in questions:
        qid = q["id"]
        if qid in authored:
            lessons[qid] = authored[qid]
            wordings["written by hand"] += 1
            continue
        if qid.startswith(GENERATED):
            wording, lesson = by_rule(q)
            if lesson:
                lessons[qid] = lesson
                wordings[wording] += 1
                continue
        missing.append(qid)
    stray = sorted(set(authored) - {q["id"] for q in questions})
    if stray:
        sys.exit("hand-written lessons for questions not in this topic: %s" % ", ".join(stray))

    notes = []
    for qid, script in lessons.items():
        notes += lint(qid, script)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("%d questions in the topic, %d lessons written to %s" % (len(questions), len(lessons), os.path.relpath(OUT, ROOT)))
    for wording, n in sorted(wordings.items()):
        print("  %4d  %s" % (n, wording))
    if missing:
        print("%d without a lesson:" % len(missing))
        for qid in missing:
            print("  " + qid)
    for n in notes:
        print("NOTE  " + n)


if __name__ == "__main__":
    main()
