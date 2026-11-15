"""Review helper for the money-percent narration (reads only; writes nothing).

    python -X utf8 scripts/speech/topics/money_percent_review.py gen        # one spoken example per generated template
    python -X utf8 scripts/speech/topics/money_percent_review.py ext [id]   # every one-off question, spoken lines only
    python -X utf8 scripts/speech/topics/money_percent_review.py scan       # things that may sound wrong
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402


def main():
    with io.open(os.path.join(PARTS, "money-percent.json"), encoding="utf-8") as f:
        part = json.load(f)
    qs = sorted((q for q in load_grade5() if topic_of(q) == "money-percent"), key=lambda q: q["id"])
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    if mode == "gen":
        seen = collections.Counter()
        example = {}
        for q in qs:
            if q["id"].startswith("EXT_"):
                continue
            s, e = source_strings(q), part[q["id"]]
            pairs = [("q", s["q"], e["q"])]
            for key in ("options", "hints", "steps"):
                pairs += [(key[0], a, b) for a, b in zip(s[key], e[key])]
            for kind, a, b in pairs:
                k = kind + " " + re.sub(r"\d[\d,]*(\.\d+)?", "N", re.sub(r"\b[A-Z][a-z]+ (buys|bought|is buying|paid)", r"X \1", a))
                k = re.sub(r"(a|N|one|Each) [a-z]+( set)?( for| at| cost| costs|\?)", r"\1 ITEM\3", k)
                seen[k] += 1
                example.setdefault(k, b)
        for k, v in sorted(seen.items(), key=lambda x: (x[0][0], -x[1])):
            print(v, "|", example[k])
    elif mode == "ext":
        for q in qs:
            if not q["id"].startswith("EXT_"):
                continue
            if len(sys.argv) > 2 and sys.argv[2] not in q["id"]:
                continue
            e = part[q["id"]]
            print("##", q["id"])
            print("q :", e["q"])
            for key in ("options", "hints", "steps"):
                for i, t in enumerate(e[key]):
                    if t:
                        print("%s%d:" % (key[0], i), t)
    else:
        odd = re.compile(r"[()]|,,|\.\.|, \.|\b[A-Z]{2,}\b|equals equals|which is, |, so [a-z]+, which|[a-z] \d+ \d|  ")
        for q in qs:
            e = part[q["id"]]
            for key in ("q", "options", "hints", "steps"):
                for t in ([e[key]] if key == "q" else e[key]):
                    if odd.search(t):
                        print(q["id"], key, "|", t)


if __name__ == "__main__":
    main()
