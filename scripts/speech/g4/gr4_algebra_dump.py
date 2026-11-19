"""Print the source of the gr4_algebra questions (and, with --spoken, the narration beside it).

    python -X utf8 scripts/speech/g4/gr4_algebra_dump.py [start] [count] [--spoken] [--ids]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import common  # noqa: E402

NODE = "gr4_algebra"


def e_has(entry, pattern):
    """Whether any spoken line of an entry matches a pattern (for --grep=<regex>)."""
    import re
    if not entry:
        return False
    lines = [entry["q"]] + entry["options"] + entry["hints"] + entry["steps"]
    return any(re.search(pattern, s) for s in lines)


def main(node=NODE):
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    start = int(args[0]) if args else 0
    count = int(args[1]) if len(args) > 1 else 10000
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == node), key=lambda q: q["id"])
    if "--ids" in flags:
        for i, q in enumerate(questions):
            print(i, q["id"], "|", q.get("subTopic", ""), "|", q.get("questionText", "")[:90].replace("\n", " // "))
        return
    part = {}
    path = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", node + ".json")
    if "--spoken" in flags and os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
    grep = [a[7:] for a in flags if a.startswith("--grep=")]
    if "--changed" in flags:
        # Only the questions whose hints and steps were rewritten in the bank.
        with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
            listed = set(json.load(f).get(node, []))
        questions = [q for q in questions if q["id"] in listed]
        flags.add("--help-only")
    for n, q in enumerate(questions[start:start + count], start):
        if grep and e_has(part.get(q["id"]), grep[0]) is False:
            continue
        src = common.source_strings(q)
        own = q.get("stepByStep") or []
        e = part.get(q["id"])
        print("=== %d %s" % (n, q["id"]))

        def show(tag, text, spoken):
            if "--only" in flags:
                # Review mode: just the spoken line, and only where it differs from the print.
                if spoken is not None and spoken.rstrip(".") != text.strip().rstrip("."):
                    print("%s> %s" % (tag, spoken))
                return
            print("%s: %s" % (tag, text.replace("\n", " // ")))
            if spoken is not None:
                print("%s> %s" % (" " * (len(tag) - 1), spoken))
        if "--help-only" in flags:
            print("Q: %s" % src["q"].replace("\n", " // "))
        else:
            show("Q", src["q"], e["q"] if e else None)
            for i, t in enumerate(src["options"]):
                show("O%d" % i, t, e["options"][i] if e else None)
        for i, t in enumerate(src["hints"]):
            show("H%d" % i, t, e["hints"][i] if e else None)
        for i, t in enumerate(src["steps"]):
            latex = own[i].get("latex", "") if i < len(own) else ""
            show("S%d" % i, t + ("   [[%s]]" % latex if latex else ""), e["steps"][i] if e else None)


if __name__ == "__main__":
    main()
