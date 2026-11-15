"""Review helper for the factors topic.

    python -X utf8 scripts/speech/topics/factors_review.py families   # generated wordings no family rule knows, grouped
    python -X utf8 scripts/speech/topics/factors_review.py ext 0 20   # one-off questions: source next to narration
    python -X utf8 scripts/speech/topics/factors_review.py general    # every line that went through the general converter
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from common import load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402
import factors_rules as R  # noqa: E402
from factors import HAND, narrate  # noqa: E402


def rows_of(q):
    src = source_strings(q)
    entry = narrate(q)
    rows = [("q", src["q"], entry["q"])]
    rows += [("o%d" % i, s, e) for i, (s, e) in enumerate(zip(src["options"], entry["options"]))]
    rows += [("h%d" % i, s, e) for i, (s, e) in enumerate(zip(src["hints"], entry["hints"]))]
    rows += [("s%d" % i, s, e) for i, (s, e) in enumerate(zip(src["steps"], entry["steps"]))]
    return rows


def questions():
    return sorted((q for q in load_grade5() if topic_of(q) == "factors"), key=lambda q: q["id"])


def families():
    count = collections.Counter()
    example = {}
    for q in questions():
        if q["id"].startswith("EXT_"):
            continue
        for key, s, e in rows_of(q):
            if not s.strip() or R.family_line(s) is not None or re.fullmatch(r"[-−]?\d+", s.strip()):
                continue
            shape = (key[0], re.sub(r"\d+", "N", s))
            count[shape] += 1
            example.setdefault(shape, (q["id"], key, s))
    for shape, n in sorted(count.items(), key=lambda kv: (kv[0][0], -kv[1])):
        qid, key, s = example[shape]
        print("%3d %s %s\n      %s" % (n, qid, key, s))
    print("%d shapes" % len(count))


def ext(start, end):
    chosen = [q for q in questions() if q["id"].startswith("EXT_")][start:end]
    for q in chosen:
        hand = HAND.get(q["id"], {})
        print("## " + q["id"])
        for key, s, e in rows_of(q):
            if not s.strip() or re.fullmatch(r"\d+", s.strip()):
                continue
            is_hand = key in hand or (key[0] == "o" and "o" in hand)
            bad = check_string(e, s, key)
            flag = "BAD " if bad else ("hand" if is_hand else "rule")
            print("%s P: %s\n   %s: %s" % (key, s, flag, e))


def general():
    seen = set()
    for q in questions():
        hand = HAND.get(q["id"], {})
        for key, s, e in rows_of(q):
            if not s.strip() or key in hand or (key[0] == "o" and "o" in hand):
                continue
            if R.family_line(s) is not None or re.fullmatch(r"\d+", s.strip()) or (s, e) in seen:
                continue
            seen.add((s, e))
            print("%s %s\n   PRINT  %s\n   SPOKEN %s" % (q["id"], key, s, e))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "general"
    if mode == "families":
        families()
    elif mode == "ext":
        ext(int(sys.argv[2]), int(sys.argv[3]))
    else:
        general()
