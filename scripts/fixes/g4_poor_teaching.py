"""Find Grade 4 questions whose hints or worked steps are not fit for a child, and write
them out for rewriting.

    python -X utf8 scripts/fixes/g4_poor_teaching.py            # counts
    python -X utf8 scripts/fixes/g4_poor_teaching.py --write    # also write teach2-in-NN.json

A question is picked when a hint or step:
  - is past-paper filler ("This is from the 2016 IPM exam (Q3)", "Correct answer: Option 3");
  - thinks aloud ("Wait", "Hmm", "Let me recount");
  - is written as notes, not sentences (arrows, ticks and crosses, a line starting with "=");
  - names an option by letter or number (the options may not be in that order any more);
  - is a filler step ("Identify the ratio parts and total.", "Compute the answer: 40",
    "Follow BODMAS", "Find factors of ...") with no working in it;
or when the third hint states the question's own answer.
Reads the bank. With --write, the inputs go to data/bank-import/g4/ (not part of the bank).
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

RULES = [
    ("past-paper filler", re.compile(r"This is from the \d{4} IPM exam|Correct answer: Option|Try working backwards from the options|^Think (?:carefully|step by step)", re.I)),
    ("thinks aloud", re.compile(r"\b(wait|hmm+|oops|let me (?:recount|check|pick|try)|actually,)\b", re.I)),
    ("note style", re.compile(u"→|⇒|✓|✗|✔|✘|^\\s*=|\\bLHS\\b|\\bRHS\\b")),
    ("names an option", re.compile(r"\b[Oo]ption\s+\(?[A-D1-4]\)?(?![A-Za-z])|\([A-D]\)|\b[A-D]\s+is\s+(?:the\s+)?(?:correct|right|not)\b|^[A-D][:)]\s|\b[Aa]nswer(?:\s+is|:)\s*\(?[A-D]\)?\s*[.!]?$")),
    ("filler step", re.compile(r"^(?:Identify the |Compute the answer|Follow BODMAS|Find factors of|The answer is \S+\.?$|Answer: )", re.I)),
]
NUM = re.compile(r"\d+(?:\.\d+)?")


def texts(q):
    hints = [h or "" for h in (q.get("hints") or [])]
    steps = [(s.get("text") or "") if isinstance(s, dict) else str(s) for s in (q.get("stepByStep") or [])]
    return hints, steps


def reasons(q):
    hints, steps = texts(q)
    out = []
    for label, rx in RULES:
        if any(rx.search(t) for t in hints + steps):
            out.append(label)
    right = next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), "")
    mine = [n for n in NUM.findall(right.replace(",", "")) if n not in NUM.findall((q.get("questionText") or "").replace(",", ""))]
    if len(hints) >= 3 and mine and len(mine[0]) > 1 and all(n in NUM.findall(hints[2].replace(",", "")) for n in mine):
        out.append("hint 3 states the answer")
    return out


def main():
    names = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    rows = bank.load_bank(4)
    picked = []
    by_reason = collections.Counter()
    by_source = collections.Counter()
    for q in rows:
        why = reasons(q)
        if why:
            picked.append((q, why))
            by_source[q.get("source")] += 1
            for w in why:
                by_reason[w] += 1
    print("%d of %d Grade 4 questions have hints or steps that need rewriting" % (len(picked), len(rows)))
    for w, n in by_reason.most_common():
        print("   %-26s %4d" % (w, n))
    print("   by source: " + ", ".join("%s %d" % kv for kv in by_source.most_common()))
    if "--write" not in sys.argv:
        return
    picked.sort(key=lambda p: (p[0].get("node") or "", p[0]["id"]))
    parts = max(1, (len(picked) + 59) // 60)
    size = (len(picked) + parts - 1) // parts
    for i in range(parts):
        chunk = picked[i * size:(i + 1) * size]
        g4.dump("teach2-in-%02d.json" % (i + 1), [{
            "id": q["id"], "topic": names.get(q.get("node")), "difficulty": q.get("difficulty"), "source": q.get("source"),
            "flagged": why, "question": q.get("questionText"),
            "options": {o["id"]: o["text"] for o in q["options"]}, "answer": q.get("correctAnswer"),
            "hints": texts(q)[0], "steps": texts(q)[1],
        } for q, why in chunk])
        print("teach2-in-%02d.json  %d questions" % (i + 1, len(chunk)))


if __name__ == "__main__":
    main()
