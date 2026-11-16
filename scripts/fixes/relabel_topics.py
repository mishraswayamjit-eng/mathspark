"""Give Grade 5 questions a sub-topic label that says which topic they belong to.

    python -X utf8 scripts/fixes/relabel_topics.py            # show what would change
    python -X utf8 scripts/fixes/relabel_topics.py --write    # write the seed file

Topic practice, "try one like it" and the topic ladder all find a topic's questions
through the sub-topic label (src/data/topicTree.ts keys, matched by matchesSubTopicKey).
Three groups of Grade 5 questions carried a label that reaches the wrong topic or none
(see `python -X utf8 scripts/audit/topic_classification.py 5`):

  1. 444 generated variants labelled only "Auto-generated variant". Their family is in
     the id (VAR_G5_vary_<family>_V<n>); the audit confirmed the text agrees for all.
  2. 45 questions labelled "LCM", which the HCF & LCM topic key ("hcf") does not match.
  3. 15 generated variants that are plain equations ("Solve: 3x - 5 = 16") filed under
     the label of the question they were varied from.

Only the `subTopic` field changes. Question text, options, answers, hints and steps are
not touched. The database takes the new labels at the next re-seed.
"""
import argparse
import collections
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")

FAMILY_LABEL = {
    "bodmas": "Grade 5 — BODMAS",
    "angles": "Grade 5 — Angles",
    "percentage": "Grade 5 — Percentage (money)",
    "equation": "Grade 5 — Equations",
    "perimeter_area": "Grade 5 — Area and perimeter",
    "hcf_lcm": "Grade 5 — HCF and LCM",
    "simple_interest": "Grade 5 — Simple interest",
    "fraction_arithmetic": "Grade 5 — Fractions",
}
VARIANT_ID = re.compile(r"^VAR_G5_vary_(.+)_V\d+$")
PLAIN_EQUATION = re.compile(r"^Solve:\s*\d*x\s*[+−-]\s*\d+\s*=\s*\d+\s*$")
EQUATION_LABEL = "Grade 5 — Equations"
LCM_LABEL = "Grade 5 — LCM (HCF and LCM)"


def new_label(q):
    """The label this question should carry, or None to leave it alone."""
    sub = q.get("subTopic") or ""
    m = VARIANT_ID.match(q.get("id", ""))
    if m and sub == "Auto-generated variant":
        return FAMILY_LABEL.get(m.group(1))
    if sub == "Grade 5 — LCM":
        return LCM_LABEL
    if q.get("id", "").startswith("VAR_EXT_G5_") and PLAIN_EQUATION.match((q.get("questionText") or "").strip()):
        if "equation" not in sub.lower():
            return EQUATION_LABEL
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    with io.open(SEED, encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    same_format = json.dumps(data, ensure_ascii=True, separators=(",", ":")) == raw.rstrip("\n")

    changes = collections.Counter()
    unknown_family = collections.Counter()
    for q in data["questions"]:
        if q.get("topicId") != "grade5":
            continue
        m = VARIANT_ID.match(q.get("id", ""))
        if m and q.get("subTopic") == "Auto-generated variant" and m.group(1) not in FAMILY_LABEL:
            unknown_family[m.group(1)] += 1
        label = new_label(q)
        if label and label != q.get("subTopic"):
            changes[(q.get("subTopic"), label)] += 1
            q["subTopic"] = label

    for (old, new), n in sorted(changes.items(), key=lambda kv: -kv[1]):
        print("%4d  %-36s -> %s" % (n, old, new))
    print("%d questions relabelled" % sum(changes.values()))
    for fam, n in unknown_family.items():
        print("LEFT ALONE: %d variants of family '%s' have no label mapped" % (n, fam))

    if not args.write:
        print("nothing written (use --write)")
        return
    if not same_format:
        raise SystemExit("The seed file is not in the compact one-line form this tool writes; stopping.")
    with io.open(SEED, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(data, ensure_ascii=True, separators=(",", ":")))
        if raw.endswith("\n"):
            f.write("\n")
    print("wrote %s" % os.path.relpath(SEED, ROOT))


if __name__ == "__main__":
    main()
