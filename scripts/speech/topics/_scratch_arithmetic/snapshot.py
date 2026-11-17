"""Scratch: keep a copy of the arithmetic part file as it was before the imported questions were narrated.

    python -X utf8 scripts/speech/topics/_scratch_arithmetic/snapshot.py          # save (never overwrites)
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/snapshot.py --check  # compare the part file with the copy
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
PART = os.path.join(ROOT, "data", "question-speech", "parts", "arithmetic.json")
COPY = os.path.join(HERE, "arithmetic_before.json")

if "--check" in sys.argv:
    with io.open(COPY, encoding="utf-8") as f:
        before = json.load(f)
    with io.open(PART, encoding="utf-8") as f:
        now = json.load(f)
    changed = [k for k in before if json.dumps(before[k], ensure_ascii=False, sort_keys=False) != json.dumps(now.get(k), ensure_ascii=False, sort_keys=False)]
    print("%d entries before, %d now, %d new, %d changed or missing" % (len(before), len(now), len(set(now) - set(before)), len(changed)))
    for k in changed[:40]:
        print("  " + k)
else:
    if os.path.exists(COPY):
        sys.exit("copy already exists; not overwriting")
    with io.open(PART, encoding="utf-8") as f:
        text = f.read()
    with io.open(COPY, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("saved %d characters, %d entries" % (len(text), len(json.loads(text))))
