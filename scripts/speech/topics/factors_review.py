"""Review helper for the factors topic: prints every line that went through the general
converter (not hand-written, not a known family wording), so it can be read and judged.

    python -X utf8 scripts/speech/topics/factors_review.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from common import load_grade5, source_strings, topic_of  # noqa: E402
import factors_rules as R  # noqa: E402
from factors import HAND, narrate  # noqa: E402


def main():
    seen = set()
    for q in sorted((q for q in load_grade5() if topic_of(q) == "factors"), key=lambda q: q["id"]):
        src = source_strings(q)
        entry = narrate(q)
        hand = HAND.get(q["id"], {})
        rows = [("q", src["q"], entry["q"])]
        rows += [("o", s, e) for s, e in zip(src["options"], entry["options"])]
        rows += [("h%d" % i, s, e) for i, (s, e) in enumerate(zip(src["hints"], entry["hints"]))]
        rows += [("s%d" % i, s, e) for i, (s, e) in enumerate(zip(src["steps"], entry["steps"]))]
        for key, s, e in rows:
            if not s.strip() or key in hand or (key == "o" and "o" in hand):
                continue
            if R.family_line(s) is not None or re.fullmatch(r"\d+", s.strip()):
                continue
            if (s, e) in seen:
                continue
            seen.add((s, e))
            print("%s %s\n   PRINT  %s\n   SPOKEN %s" % (q["id"], key, s, e))


if __name__ == "__main__":
    main()
