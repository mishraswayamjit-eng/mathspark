"""Print lessons the way a child hears them (what is said, what is written, each ask), compactly.

    python -X utf8 scripts/teach/gen/ratio_word_problems_read.py <id prefix> [<id prefix> ...]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PART = os.path.join(ROOT, "data", "teach", "parts", "ratio-word-problems.json")


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    prefixes = tuple(sys.argv[1:]) or ("",)
    shown = 0
    for qid, script in part.items():
        if not qid.startswith(prefixes):
            continue
        shown += 1
        print("=" * 60)
        print(qid, "(%s, %d beats)" % (script["origin"], len(script["beats"])))
        for i, b in enumerate(script["beats"]):
            print("%2d. %s" % (i + 1, b["say"]))
            for op in b.get("board", []):
                kind = op["op"]
                if kind == "write":
                    print("      [%s] %s" % (op.get("tone", "work"), op["text"]))
                elif kind == "figure":
                    print("      (figure: %s)" % op["spec"]["kind"])
                else:
                    target = op.get("target", {}).get("text") or op.get("from", {}).get("text") or ""
                    extra = op.get("note") or op.get("text") or op.get("shape") or ""
                    print("      (%s %r %s)" % (kind, target, extra))
            a = b.get("ask")
            if a and a["kind"] == "choose":
                print("      ASK %s -> %s" % (" | ".join(a["choices"]), a["choices"][a["answer"]]))
                print("      IF NOT: %s" % a["ifNot"])
            elif a:
                print("      ASK (think)")
    print(shown, "lessons")


if __name__ == "__main__":
    main()
