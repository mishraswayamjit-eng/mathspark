"""Print source and current narration for the new Grade 5 questions (ids G5A_...).

    python -X utf8 scripts/speech/topics/g5_authored_dump.py <start> <count> [raw|bad|both]

Default: the narration only, with the source shown under any line that fails the checker (!!).
raw: the source only.  both: source and narration.  bad: only questions with a failing line.
A third form, `... dump.py id G5A_X_001 G5A_Y_002`, prints those questions in "both" form.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import common  # noqa: E402
import validate  # noqa: E402
import g5_authored  # noqa: E402


def main():
    args = sys.argv[1:]
    qs = g5_authored.questions()
    raw = "raw" in args
    only_bad = "bad" in args
    both = "both" in args
    if args and args[0] == "id":
        wanted = set(args[1:])
        qs = [q for q in qs if q["id"] in wanted]
        both = True
    else:
        nums = [a for a in args if a.isdigit()]
        start = int(nums[0]) if nums else 0
        count = int(nums[1]) if len(nums) > 1 else 20
        qs = qs[start:start + count]
    n_bad = 0
    for q in qs:
        src = common.source_strings(q)
        entry = g5_authored.narrate(q)
        own = q.get("stepByStep") or []
        lines = []
        bad_any = False

        def show(tag, s, n, also=None):
            nonlocal bad_any
            bad = validate.check_string(n, s, tag, also)
            if bad:
                bad_any = True
            if raw:
                lines.append("  %s %s" % (tag, s))
                return
            if both or bad:
                lines.append("  %s S: %s" % (tag, s))
                lines.append("  %s %s %s" % (" " * len(tag), "!!" if bad else "N:", n))
            else:
                lines.append("  %s %s" % (tag, n))
            for b in bad:
                lines.append("        " + b.split(": ", 1)[-1])

        show("q ", src["q"], entry["q"])
        if not (raw or both) and all(not validate.check_string(n, s, "o") for s, n in zip(src["options"], entry["options"])):
            lines.append("  o  " + " | ".join(entry["options"]))
        else:
            for i, s in enumerate(src["options"]):
                show("o%d" % i, s, entry["options"][i])
        for i, s in enumerate(src["hints"]):
            show("h%d" % i, s, entry["hints"][i])
        for i, s in enumerate(src["steps"]):
            also = None
            if i < len(own) and own[i].get("latex"):
                if raw or both:
                    lines.append("  s%d latex: %s" % (i, own[i]["latex"]))
                also = "%s %s" % (s, re.sub(r"\\[a-zA-Z]+", " ", own[i]["latex"]))
            show("s%d" % i, s, entry["steps"][i], also)
        if bad_any:
            n_bad += 1
        if only_bad and not bad_any:
            continue
        print("%s ans=%s" % (q["id"], q.get("correctAnswer", "")))
        print("\n".join(lines))
    print("-- %d questions shown range, %d with a failing line" % (len(qs), n_bad))


if __name__ == "__main__":
    main()
