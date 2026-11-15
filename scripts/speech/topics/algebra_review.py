"""Review helper for the algebra narration. Reads the part file; writes nothing.

    python -X utf8 scripts/speech/topics/algebra_review.py ext      # every past-paper and worksheet line, source then spoken
    python -X utf8 scripts/speech/topics/algebra_review.py flags    # lines worth a second look
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

SUSPECT = [
    (r"(?:equals|plus|minus|times|by|over|\d) a\b", "letter a read as a word?"),
    (r"\ba (?:equals|plus|minus|times|over|squared)\b", "letter a read as a word?"),
    (r"\d \d", "two numbers with nothing between"),
    (r"[.?!,:]\s*[.,:]", "doubled punctuation"),
    (r"[()\[\]]", "bracket character"),
    (r"[A-Z]{3,}", "capitals a voice may spell"),
    (r"\bThat works\.[!.]", "tick tidy"),
    (r"\b\d+[A-Za-z]\b(?<!st)(?<!nd)(?<!rd)(?<!th)", "number glued to a letter"),
    (r"—|–", "dash"),
]


def lines(q, entry):
    src = source_strings(q)
    yield "q", src["q"], entry["q"]
    for key in ("options", "hints", "steps"):
        for i, (a, b) in enumerate(zip(src[key], entry[key])):
            yield "%s[%d]" % (key, i), a, b


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "flags"
    with io.open(os.path.join(PARTS, "algebra.json"), encoding="utf-8") as f:
        part = json.load(f)
    qs = sorted((q for q in load_grade5() if topic_of(q) == "algebra"), key=lambda q: q["id"])
    longest = 0
    if mode == "latex":
        seen = set()
        for q in qs:
            for i, s in enumerate(q.get("stepByStep") or []):
                if not s.get("latex"):
                    continue
                key = re.sub(r"\d+", "N", s.get("text", "") + "|" + s["latex"])
                if key in seen and not q["id"].startswith("EXT_"):
                    continue
                seen.add(key)
                print("%s steps[%d]\n    T: %s\n    L: %s\n    S: %s" % (q["id"], i, s.get("text", ""), s["latex"], part[q["id"]]["steps"][i]))
        return
    for q in qs:
        entry = part[q["id"]]
        for label, a, b in lines(q, entry):
            longest = max(longest, len(b))
            if mode == "ext" and q["id"].startswith("EXT_") and a.strip():
                print("%s %s\n    P: %s\n    S: %s" % (q["id"], label, a, b))
            if mode == "flags":
                for pat, why in SUSPECT:
                    if re.search(pat, b):
                        print("%s %s [%s]\n    S: %s" % (q["id"], label, why, b))
    print("longest line: %d characters" % longest)


if __name__ == "__main__":
    main()
