"""Look across every lesson for things the checker allows but a reader should see.

    python -X utf8 scripts/teach/audit.py

Reports, per part: how the lessons are built (beats, asks, marks, figures), marks that
land inside a longer number (a "2" that is really part of "12"), choices that hand over
the answer, and beats that run long. Nothing is changed.
"""
import collections
import glob
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PARTS = os.path.join(ROOT, "data", "teach", "parts")


def nth_index(text, target, nth):
    at = -1
    for _ in range(nth):
        at = text.find(target, at + 1 if at >= 0 else 0)
        if at < 0:
            return -1
        # non-overlapping, like the board
        nxt = at + len(target) - 1
        at = at if _ == nth - 1 else nxt
    return at


def find_nth(text, target, nth):
    pos = 0
    for k in range(nth):
        at = text.find(target, pos)
        if at < 0:
            return -1
        if k == nth - 1:
            return at
        pos = at + len(target)
    return -1


def inside_number(text, target, nth):
    """True when the targeted text is digits cut out of a longer number."""
    if not target or not (target[0].isdigit() or target[-1].isdigit()):
        return False
    at = find_nth(text, target, nth)
    if at < 0:
        return False
    before = text[at - 1] if at > 0 else ""
    after = text[at + len(target)] if at + len(target) < len(text) else ""
    return (target[0].isdigit() and (before.isdigit() or before == ".")) or \
           (target[-1].isdigit() and (after.isdigit() or (after == "." and at + len(target) + 1 < len(text) and text[at + len(target) + 1].isdigit())))


def main():
    grand = collections.Counter()
    for path in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
        name = os.path.splitext(os.path.basename(path))[0]
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        c = collections.Counter()
        inside = []
        long_beats = 0
        for qid, script in part.items():
            lines = {}
            c["lessons"] += 1
            for beat in script.get("beats", []):
                c["beats"] += 1
                say = beat.get("say", "")
                if len(re.findall(r"[.!?](?:\s|$)", say)) >= 4:
                    long_beats += 1
                if beat.get("ask"):
                    c["asks"] += 1
                    ask = beat["ask"]
                    if ask.get("kind") == "choose":
                        right = ask["choices"][ask["answer"]]
                        if re.search(r"=\s*\d", right) and not any(re.search(r"=\s*\d", ch) for i, ch in enumerate(ask["choices"]) if i != ask["answer"]):
                            c["choice shows its working"] += 1
                for op in beat.get("board", []):
                    kind = op.get("op")
                    if kind == "write":
                        lines[op["id"]] = op["text"]
                    elif kind == "clear":
                        lines = {}
                    elif kind == "figure":
                        c["figures"] += 1
                    else:
                        c["marks"] += 1
                        text = lines.get(op.get("line"), "")
                        targets = []
                        if kind == "arc":
                            targets = [op["from"]] + op["to"]
                        elif kind in ("strike", "note", "mark"):
                            targets = [op["target"]]
                        elif kind == "group":
                            targets = op["targets"]
                        for t in targets:
                            if inside_number(text, t["text"], t.get("nth", 1)):
                                inside.append((qid, kind, t["text"], t.get("nth", 1), text))
        n = max(1, c["lessons"])
        print("%-22s %4d lessons  %.1f beats  %.1f asks  %.1f marks  %.1f figures per lesson  | %d beats of 4+ sentences, %d marks inside a number, %d choices that show their working" % (
            name, c["lessons"], c["beats"] / n, c["asks"] / n, c["marks"] / n, c["figures"] / n, long_beats, len(inside), c["choice shows its working"]))
        for row in inside[:4]:
            print("      inside a number: %s %s %r (nth %d) on \"%s\"" % row)
        grand.update(c)
        grand["inside"] += len(inside)
        grand["long"] += long_beats
    print("\nall parts: %d lessons, %d beats, %d asks, %d marks, %d figures; %d marks inside a number; %d long beats" % (
        grand["lessons"], grand["beats"], grand["asks"], grand["marks"], grand["figures"], grand["inside"], grand["long"]))


if __name__ == "__main__":
    main()
