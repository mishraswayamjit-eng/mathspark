"""Write real hints, by rule, for the auto-generated Grade 5 questions.

    python -X utf8 scripts/fixes/gen/generated_hints.py

Reads the question bank (data/bank/, through scripts/bank/bank.py) and writes data/question-fixes/parts/generated-hints.json.
Every question with source "auto_generated_v2" is matched against one rule per wording (re.fullmatch on
the question text). A rule pulls out the numbers, works out the answer itself, and writes:
  hint 1  the idea for this kind of question;
  hint 2  the first move with this question's own numbers, stopping before the answer;
  hint 3  a worked example of the same method with different, easy numbers, chosen from a fixed list
          (its arithmetic is computed here, never typed in).
Nothing is random: the same question always gets the same hints.
A question is skipped (and counted) when it is reserved in answers_ids.txt, when no rule matches its
wording, when the rule's answer disagrees with the answer key, or when the hints would not pass check.py.
"""
import collections
import io
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from check import PARTS, bank, answer_numbers, check_entry, correct_text, numbers_in, option_texts  # noqa: E402
from generated_hints_common import Skip, pick  # noqa: E402
from generated_hints_rules_a import RULES_A  # noqa: E402
from generated_hints_rules_b import RULES_B  # noqa: E402

PART = "generated-hints"
RULES = RULES_A + RULES_B
WHY = "All three hints were the same generic lines given to every generated question; they said nothing about this one."
ID = re.compile(r"VAR_G5_vary_(.+)_V(\d+)")
VALUE = re.compile(r"(?:Rs\.)?(\d+(?:\.\d+)?(?:/\d+)?)(?:°| cm| sq\. cm)?")


def reserved_ids():
    with io.open(os.path.join(HERE, "..", "answers_ids.txt"), encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def load_questions():
    qs = [q for q in bank.load_pool("grade5")
          if q.get("source") == "auto_generated_v2" and ID.fullmatch(q["id"])]
    return sorted(qs, key=lambda q: (ID.fullmatch(q["id"]).group(1), int(ID.fullmatch(q["id"]).group(2))))


def key_value(q):
    m = VALUE.fullmatch(correct_text(q).strip())
    return Fraction(m.group(1)) if m else None


def make(q):
    """(rule name, variant, tier, fix) for one question, or raise Skip."""
    family = ID.fullmatch(q["id"]).group(1)
    text = q["questionText"].strip()
    for fam, name, pattern, rule in RULES:
        m = re.fullmatch(pattern, text)
        if fam == family and m:
            break
    else:
        raise Skip("no rule for this wording")
    out = rule(*m.groups())
    if key_value(q) != out["answer"]:
        raise Skip("answer key %r disagrees with the computed answer %s" % (correct_text(q), out["answer"]))
    options = set().union(*[numbers_in(o) for o in option_texts(q)])
    # A rule that compares its examples with the answer itself (fractions) passes its own, empty, set.
    answer = out.get("answer_nums", numbers_in(correct_text(q)) - out["qnums"])
    example, tier = pick(out["cands"], out["qnums"], options, answer, answer_numbers(q))
    if example is None:
        raise Skip("no worked example with numbers different from the question's")
    fix = {"hints": [out["h1"], out["h2"], example.text], "why": WHY}
    problems = check_entry(q["id"], fix, q, PART)
    if problems:
        raise Skip("checker: " + "; ".join(problems))
    return name, out.get("variant", ""), tier, fix


def build():
    """Every generated question with what was made of it: a list of dicts."""
    reserved = reserved_ids()
    rows = []
    for q in load_questions():
        row = {"q": q, "family": ID.fullmatch(q["id"]).group(1), "rule": "", "variant": "", "tier": 0, "fix": None, "skip": ""}
        if q["id"] in reserved:
            row["skip"] = "reserved for the answers workstream"
        else:
            try:
                row["rule"], row["variant"], row["tier"], row["fix"] = make(q)
            except Skip as e:
                row["skip"] = str(e)
        rows.append(row)
    return rows


def main():
    rows = build()
    part = collections.OrderedDict((r["q"]["id"], r["fix"]) for r in rows if r["fix"])
    os.makedirs(PARTS, exist_ok=True)
    with io.open(os.path.join(PARTS, PART + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("%d generated questions, %d given hints, %d skipped" % (len(rows), len(part), len(rows) - len(part)))
    total = collections.Counter(r["family"] for r in rows)
    done = collections.Counter(r["family"] for r in rows if r["fix"])
    for fam in sorted(total):
        print("  %-22s %3d of %3d" % (fam, done[fam], total[fam]))
    print("by wording:")
    for (fam, rule, variant), n in sorted(collections.Counter((r["family"], r["rule"], r["variant"]) for r in rows if r["fix"]).items()):
        print("  %-22s %-26s %-32s %3d" % (fam, rule, variant, n))
    print("worked example tier (1 = shares no number with question or choices):",
          dict(sorted(collections.Counter(r["tier"] for r in rows if r["fix"]).items())))
    skipped = [r for r in rows if not r["fix"]]
    if skipped:
        print("skipped:")
        for r in skipped:
            print("  %-36s %s | %s" % (r["q"]["id"], r["skip"], r["q"]["questionText"]))
    # Not a failure, but worth a look: a hint 1 or 2 holding a number from the correct choice that is not in the question.
    for r in rows:
        if r["fix"]:
            q = r["q"]
            answer = numbers_in(correct_text(q)) - numbers_in(q["questionText"])
            for i in (0, 1):
                hit = numbers_in(r["fix"]["hints"][i]) & answer
                if hit:
                    print("LOOK %s hint %d has %s from the answer %r: %s" % (
                        q["id"], i + 1, sorted(map(str, hit)), correct_text(q), r["fix"]["hints"][i]))


if __name__ == "__main__":
    main()
