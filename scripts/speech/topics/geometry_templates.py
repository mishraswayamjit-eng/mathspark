"""Review helper for the geometry topic: one example of every distinct wording in the rule-narrated questions.

    python -X utf8 scripts/speech/topics/geometry_templates.py            # every template, print and spoken
    python -X utf8 scripts/speech/topics/geometry_templates.py --bad      # only templates whose narration fails
    python -X utf8 scripts/speech/topics/geometry_templates.py --hand     # failing lines of the hand-written questions

Reads the part file on disk, so run geometry.py first. Writes nothing.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402
from geometry_hand1 import HAND as H1  # noqa: E402
from geometry_hand2 import HAND as H2  # noqa: E402
from geometry_hand3 import HAND as H3  # noqa: E402


def main():
    only_bad = "--bad" in sys.argv
    hand_mode = "--hand" in sys.argv
    hand_ids = set(H1) | set(H2) | set(H3)
    with io.open(os.path.join(PARTS, "geometry.json"), encoding="utf-8") as f:
        part = json.load(f)
    questions = sorted((q for q in load_grade5() if topic_of(q) == "geometry"), key=lambda q: q["id"])
    seen = {}
    for q in questions:
        is_hand = q["id"] in hand_ids
        if is_hand != hand_mode:
            continue
        src = source_strings(q)
        entry = part.get(q["id"]) or {}
        own = q.get("stepByStep") or []
        for key in ("q", "options", "hints", "steps"):
            texts = [src[key]] if key == "q" else src[key]
            spoken = [entry.get(key, "")] if key == "q" else list(entry.get(key, []))
            for i, text in enumerate(texts):
                said = spoken[i] if i < len(spoken) else ""
                latex = own[i].get("latex", "") if key == "steps" and i < len(own) else ""
                also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
                bad = check_string(said, text, "x", also)
                if hand_mode and "--read" in sys.argv:
                    # Every hint and step of the hand-written questions, print over spoken.
                    if key in ("hints", "steps") and text:
                        print("%s %s[%d]%s\n   P %s\n   S %s" % (q["id"][7:], key, i, "  FAILS" if bad else "", text, said))
                    continue
                if hand_mode:
                    if bad or (i >= len(spoken)):
                        print("%s %s[%d]\n   PRINT  %s\n   LATEX  %s\n   SPOKEN %s" % (q["id"], key, i, text, latex, said))
                    continue
                template = (key, re.sub(r"\d+(?:\.\d+)?", "N", text))
                if template in seen:
                    seen[template][0] += 1
                    continue
                seen[template] = [1, q["id"], text, latex, said, bad]
    if hand_mode:
        return
    for (key, _), (n, qid, text, latex, said, bad) in seen.items():
        if only_bad and not bad:
            continue
        print("%d x %s | %s%s" % (n, key, qid, "  FAILS" if bad else ""))
        print("   PRINT  %s" % text)
        if latex:
            print("   LATEX  %s" % latex)
        print("   SPOKEN %s" % said)
    print("%d templates" % len(seen))


if __name__ == "__main__":
    main()
