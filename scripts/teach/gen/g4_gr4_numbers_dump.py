"""Scratch helper: dump a Grade 4 topic's questions to a text file to read.

    python -X utf8 scripts/teach/gen/g4_gr4_numbers_dump.py gr4_numbers
    python -X utf8 scripts/teach/gen/g4_gr4_numbers_dump.py gr4_squares
    python -X utf8 scripts/teach/gen/g4_gr4_numbers_dump.py gr4_numbers --todo   # only those with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_numbers_dump.py --clean              # delete the scratch text files
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def opts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def main():
    if sys.argv[1] == "--clean":
        # Remove the scratch text files this script and g4_gr4_numbers_read.py leave behind.
        for topic in ("gr4_numbers", "gr4_squares"):
            for kind in ("dump", "todo", "read"):
                path = os.path.join(HERE, "g4_%s_%s.txt" % (topic, kind))
                if os.path.exists(path):
                    os.remove(path)
                    print("removed " + os.path.basename(path))
        return
    topic = sys.argv[1]
    todo = "--todo" in sys.argv
    qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
    done = {}
    part = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    if os.path.exists(part):
        with io.open(part, encoding="utf-8") as f:
            done = json.load(f)
    figs = {}
    fpath = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
    if os.path.exists(fpath):
        with io.open(fpath, encoding="utf-8") as f:
            figs = json.load(f)
    out = os.path.join(HERE, "g4_%s_%s.txt" % (topic, "todo" if todo else "dump"))
    pref = collections.Counter()
    n = 0
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        for i, q in enumerate(qs):
            pref[re.sub(r"\d+", "#", q["id"])] += 1
            if todo and q["id"] in done:
                continue
            n += 1
            fig = figs.get(q["id"])
            f.write("#%d %s [%s] {%s} %s%s\n" % (i, q["id"], q.get("subTopic", ""), q.get("source", ""), q.get("difficulty", ""),
                                               " FIG" if fig else ""))
            f.write("Q: %s\n" % q["questionText"].replace("\n", " // "))
            f.write("O: %s  KEY %s\n" % (" | ".join(opts(q)), q.get("correctAnswer")))
            for s in q.get("stepByStep") or []:
                f.write("S: %s\n" % s.get("text", "").replace("\n", " // "))
            for k, v in sorted((q.get("misconceptions") or {}).items()):
                if v:
                    f.write("M%s: %s\n" % (k, v.replace("\n", " // ")))
            if fig and "--fig" in sys.argv:
                f.write("F: %s\n" % json.dumps(fig, ensure_ascii=False))
            f.write("\n")
    print("%s: %d questions, %d written to %s" % (topic, len(qs), n, os.path.basename(out)))
    for k, v in sorted(pref.items()):
        print("  %-30s %d" % (k, v))


if __name__ == "__main__":
    main()
