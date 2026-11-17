"""Scratch helper for the ratio-word-problems narration extension.

    python -X utf8 scripts/speech/topics/_scratch_ratio/tool.py snapshot   # save the part file as it is now (refuses to overwrite)
    python -X utf8 scripts/speech/topics/_scratch_ratio/tool.py source     # write new_source.json: source of questions not in the snapshot
    python -X utf8 scripts/speech/topics/_scratch_ratio/tool.py compare    # check every snapshot entry is unchanged in the part file
    python -X utf8 scripts/speech/topics/_scratch_ratio/tool.py scan       # odd characters left in the new entries
    python -X utf8 scripts/speech/topics/_scratch_ratio/tool.py dump A B   # new entries A..B, source and narration, to review.txt
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

SLUG = "ratio-word-problems"
PART = os.path.join(PARTS, SLUG + ".json")
BEFORE = os.path.join(HERE, "part_before.json")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def new_questions():
    before = read(BEFORE)
    return sorted((q for q in load_grade5() if topic_of(q) == SLUG and q["id"] not in before), key=lambda q: q["id"])


def main():
    cmd = sys.argv[1]
    if cmd == "snapshot":
        if os.path.exists(BEFORE):
            sys.exit("snapshot already exists")
        with io.open(PART, encoding="utf-8", newline="") as f:
            raw = f.read()
        with io.open(BEFORE, "w", encoding="utf-8", newline="") as f:
            f.write(raw)
        print("saved %d entries" % len(json.loads(raw)))
    elif cmd == "source":
        out = {q["id"]: dict(source_strings(q), sub=q.get("subTopic", ""), src=q.get("source", "")) for q in new_questions()}
        with io.open(os.path.join(HERE, "new_source.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print("%d new questions" % len(out))
    elif cmd == "compare":
        before, now = read(BEFORE), read(PART)
        bad = [k for k in before if json.dumps(before[k], ensure_ascii=False, indent=1) != json.dumps(now.get(k), ensure_ascii=False, indent=1)]
        order_ok = [k for k in now if k in before] == list(before)
        print("%d old entries, %d now, %d changed, old order kept: %s" % (len(before), len(now), len(bad), order_ok))
        for k in bad:
            print("  CHANGED", k)
    elif cmd == "scan":
        now = read(PART)
        for q in new_questions():
            e = now.get(q["id"])
            if not e:
                print("MISSING", q["id"])
                continue
            for key in ("q", "options", "hints", "steps"):
                for i, line in enumerate([e[key]] if key == "q" else e[key]):
                    odd = [m.group(0) for m in re.finditer(r"[^A-Za-z0-9 .,?!'’:;\"-]|\d\s*:\s*\d|\b[A-Z]{2,}\b|(?<!['’])\b[b-jl-zB-HJ-Z]\b(?= [a-z])|\d \d|  |[,:;] ?[,:;.!?]|[a-z]-[a-z]|\b(\w+) \1\b", line)]
                    odd = [o for o in odd if o not in ("BODMAS",)]
                    if odd:
                        print("%s %s[%d] %s :: %s" % (q["id"], key, i, odd, line))
    elif cmd == "latex":
        lines = []
        for q in new_questions():
            lines.append(q["id"])
            for i, s in enumerate(q.get("stepByStep") or []):
                lines.append("  s%d %s || %s" % (i, s.get("text", "")[-40:].replace("\n", " "), s.get("latex", "")))
        with io.open(os.path.join(HERE, "latex.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        print("wrote %d lines" % len(lines))
    elif cmd == "dump":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        now = read(PART)
        lines = []
        for q in new_questions()[a:b]:
            src, e = source_strings(q), now.get(q["id"])
            lines.append("=" * 90)
            lines.append(q["id"])
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                said = None if e is None else ([e[key]] if key == "q" else e[key])
                for i, t in enumerate(items):
                    if len(sys.argv) > 4 and said is not None:
                        # spoken only, and only lines the rules changed beyond trivial punctuation
                        if key != "options" or said[i] != t:
                            lines.append("  %s%d %s" % (key[0], i, said[i]))
                        continue
                    lines.append("  %s[%d] P %s" % (key, i, t))
                    if said is not None:
                        lines.append("  %s    S %s" % (" " * len(key), said[i]))
        with io.open(os.path.join(HERE, "review.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        print("wrote %d lines" % len(lines))


if __name__ == "__main__":
    main()
