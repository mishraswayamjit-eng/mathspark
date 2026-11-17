"""Count child-facing text in the Grade 5 bank that still breaks a writing rule.

    python -X utf8 scripts/fixes/scan_text.py            # counts
    python -X utf8 scripts/fixes/scan_text.py --list     # with question ids

Looks at the question, hints and worked steps of every Grade 5 question for: words the
app never says to a child, thinking aloud, markdown asterisks, and emoji. Reads only.
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

RULES = [
    ("banned word", re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)),
    ("thinks aloud", re.compile(r"\b(wait|hmm+|oops|nope|let'?s pick a (?:cleaner|better|different)|doesn'?t work)\b", re.I)),
    ("markdown asterisks", re.compile(r"\*\*[^*]+\*\*")),
    ("emoji", re.compile(u"[\U0001F300-\U0001FAFF☀-➿⃣]")),
]


def main():
    counts = collections.Counter()
    ids = collections.defaultdict(list)
    for q in bank.load_bank(5):
        steps = [(s.get("text") if isinstance(s, dict) else s) or "" for s in (q.get("stepByStep") or [])]
        fields = [("question", [q.get("questionText") or ""]), ("hints", q.get("hints") or []), ("steps", steps)]
        for field, texts in fields:
            for rule, rx in RULES:
                if any(rx.search(t) for t in texts):
                    counts[(field, rule, q.get("source"))] += 1
                    ids[(field, rule)].append(q["id"])
    for (field, rule, source), n in sorted(counts.items()):
        print("  %-9s %-20s %-20s %4d" % (field, rule, source, n))
    if "--list" in sys.argv:
        for (field, rule), found in sorted(ids.items()):
            print("\n%s / %s" % (field, rule))
            for qid in found:
                print("   " + qid)


if __name__ == "__main__":
    main()
