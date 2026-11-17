"""Scratch helper for the place-value narration extension.

    python -X utf8 scripts/speech/topics/_scratch_place-value/tool.py snapshot   # copy the part file once
    python -X utf8 scripts/speech/topics/_scratch_place-value/tool.py source     # write new questions' source to new_source.json
    python -X utf8 scripts/speech/topics/_scratch_place-value/tool.py compare    # old entries unchanged?
    python -X utf8 scripts/speech/topics/_scratch_place-value/tool.py base       # common.speak first pass + checker problems
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEECH = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SPEECH)
from common import PARTS, load_grade5, source_strings, topic_of, speak  # noqa: E402
from validate import check_entry  # noqa: E402

PART = os.path.join(PARTS, "place-value.json")
SNAP = os.path.join(HERE, "part_before.json")


def new_questions():
    with io.open(SNAP, encoding="utf-8") as f:
        old = json.load(f)
    qs = sorted((q for q in load_grade5() if topic_of(q) == "place-value"), key=lambda q: q["id"])
    return [q for q in qs if q["id"] not in old]


def main():
    cmd = sys.argv[1]
    if cmd == "snapshot":
        if os.path.exists(SNAP):
            sys.exit("snapshot already exists")
        with io.open(PART, "rb") as f:
            data = f.read()
        with io.open(SNAP, "wb") as f:
            f.write(data)
        print("saved %d bytes, %d entries" % (len(data), len(json.loads(data.decode("utf-8")))))
    elif cmd == "source":
        qs = new_questions()
        out = {}
        for q in qs:
            s = source_strings(q)
            s["sub"] = q.get("subTopic", "")
            s["src"] = q.get("source", "")
            out[q["id"]] = s
        with io.open(os.path.join(HERE, "new_source.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print("%d new questions" % len(out))
    elif cmd == "compare":
        with io.open(SNAP, encoding="utf-8") as f:
            old = json.load(f)
        with io.open(PART, encoding="utf-8") as f:
            new = json.load(f)
        bad = [k for k in old if json.dumps(old[k], ensure_ascii=False, sort_keys=True)
               != json.dumps(new.get(k), ensure_ascii=False, sort_keys=True)]
        print("old entries: %d, now: %d, new: %d, changed or missing: %d" % (
            len(old), len(new), len([k for k in new if k not in old]), len(bad)))
        for k in bad:
            print("  CHANGED " + k)
    elif cmd == "spoken":
        # every narrated string of the new questions, one per line; optional id substring filter
        with io.open(PART, encoding="utf-8") as f:
            part = json.load(f)
        want = sys.argv[2] if len(sys.argv) > 2 else ""
        lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6
        for n, q in enumerate(new_questions()):
            if want not in q["id"] or not (lo <= n < hi):
                continue
            e = part.get(q["id"])
            if not e:
                print("## %s MISSING" % q["id"])
                continue
            print("## %d %s" % (n, q["id"]))
            print("Q  " + e["q"])
            for k in ("options", "hints", "steps"):
                for i, t in enumerate(e[k]):
                    print("%s%d %s" % (k[0].upper(), i, t))
    elif cmd == "latex":
        for q in new_questions():
            for i, s in enumerate(q.get("stepByStep") or []):
                if s.get("latex"):
                    print("%s [%d] %s" % (q["id"][-12:], i, s["latex"]))
    elif cmd == "base":
        for q in new_questions():
            s = source_strings(q)
            e = {"q": speak(s["q"]), "options": [speak(o) for o in s["options"]],
                 "hints": [speak(h) for h in s["hints"]], "steps": [speak(t) for t in s["steps"]]}
            for p in check_entry(q["id"], e, q):
                print(p)


if __name__ == "__main__":
    main()
