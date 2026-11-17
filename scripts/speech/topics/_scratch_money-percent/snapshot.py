"""Save the part file as it was at the start (once), or compare the current part file with it.

    python -X utf8 scripts/speech/topics/_scratch_money-percent/snapshot.py save
    python -X utf8 scripts/speech/topics/_scratch_money-percent/snapshot.py compare
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "data", "question-speech", "parts", "money-percent.json"))
BASE = os.path.join(HERE, "baseline.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "compare"
    if mode == "save":
        if os.path.exists(BASE):
            sys.exit("baseline already saved; not overwriting")
        with io.open(PART, encoding="utf-8", newline="") as f:
            raw = f.read()
        with io.open(BASE, "w", encoding="utf-8", newline="") as f:
            f.write(raw)
        print("saved baseline: %d entries" % len(json.loads(raw)))
        return
    base, now = load(BASE), load(PART)
    changed = [k for k in base if k in now and json.dumps(base[k], ensure_ascii=False, sort_keys=True) != json.dumps(now[k], ensure_ascii=False, sort_keys=True)]
    missing = [k for k in base if k not in now]
    new = [k for k in now if k not in base]
    print("baseline %d, now %d, new %d, changed %d, missing %d" % (len(base), len(now), len(new), len(changed), len(missing)))
    for k in changed[:20]:
        print("CHANGED", k)
    for k in missing[:20]:
        print("MISSING", k)


if __name__ == "__main__":
    main()
