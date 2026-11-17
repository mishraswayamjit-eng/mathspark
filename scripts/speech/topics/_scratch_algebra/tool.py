"""Scratch helper for the algebra narration extension. Writes only inside this folder.

    python -X utf8 scripts/speech/topics/_scratch_algebra/tool.py snapshot   # copy the part file as it is now (once)
    python -X utf8 scripts/speech/topics/_scratch_algebra/tool.py compare    # every snapshot entry unchanged?
    python -X utf8 scripts/speech/topics/_scratch_algebra/tool.py missing    # ids with no entry in the snapshot
    python -X utf8 scripts/speech/topics/_scratch_algebra/tool.py dump A B   # source + rule draft for new ids [A:B] -> draft_A_B.txt
    python -X utf8 scripts/speech/topics/_scratch_algebra/tool.py new A B    # print source and current narration for new ids [A:B]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS_DIR = os.path.dirname(HERE)
sys.path.insert(0, TOPICS_DIR)
sys.path.insert(0, os.path.dirname(TOPICS_DIR))

from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

PART = os.path.join(PARTS, "algebra.json")
SNAP = os.path.join(HERE, "before.json")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def new_questions():
    before = read(SNAP)
    qs = sorted((q for q in load_grade5() if topic_of(q) == "algebra"), key=lambda q: q["id"])
    return [q for q in qs if q["id"] not in before]


def main():
    mode = sys.argv[1]
    if mode == "snapshot":
        if os.path.exists(SNAP):
            sys.exit("snapshot already exists; not overwriting")
        with io.open(PART, "rb") as f:
            raw = f.read()
        with io.open(SNAP, "wb") as f:
            f.write(raw)
        print("saved %d bytes, %d entries" % (len(raw), len(json.loads(raw.decode("utf-8")))))
    elif mode == "restore":
        with io.open(SNAP, "rb") as f:
            raw = f.read()
        with io.open(PART, "wb") as f:
            f.write(raw)
        print("restored the part file from the snapshot (%d bytes)" % len(raw))
    elif mode == "compare":
        before, now = read(SNAP), read(PART)
        changed = [k for k in before if json.dumps(before[k], ensure_ascii=False, sort_keys=True) != json.dumps(now.get(k), ensure_ascii=False, sort_keys=True)]
        print("snapshot entries: %d, part entries: %d, new: %d, changed or missing: %d" % (len(before), len(now), len(set(now) - set(before)), len(changed)))
        for k in changed[:40]:
            print("  CHANGED " + k)
            if now.get(k):
                for key in ("q", "options", "hints", "steps"):
                    if before[k][key] != now[k][key]:
                        print("     %s\n       was %r\n       now %r" % (key, before[k][key], now[k][key]))
    elif mode == "missing":
        for i, q in enumerate(new_questions()):
            print("%4d %-34s %-18s %-34s %s" % (i, q["id"], q.get("source", ""), q.get("subTopic", "")[:34], q["questionText"][:70].replace("\n", " ")))
    elif mode == "said":
        import re
        a, b = int(sys.argv[2]), int(sys.argv[3])
        part = read(PART)
        for n, q in enumerate(new_questions()[a:b]):
            e = part[q["id"]]
            print("## %d %s" % (a + n, q["id"]))
            print("Q  " + e["q"])
            if any(re.search(r"[A-Za-z]", o) for o in e["options"]):
                print("O  " + " | ".join(e["options"]))
            for i, h in enumerate(e["hints"]):
                print("H%d %s" % (i, h))
            for i, s in enumerate(e["steps"]):
                print("S%d %s" % (i, s))
    elif mode == "flags":
        import re
        pats = [
            (r"(?<![.!?:] )(?<!^)\bA (?!plus|minus|times|equals|over|squared|is\b|and\b|with\b|into\b|samosas|from\b|to\b|by\b|gives|or\b|for\b)[a-z]{2,}", "capital A as article?"),
            (r"\ba (?:equals|plus|minus|times|over|squared)\b|(?:equals|plus|minus|times|by|over) a\b(?! [a-z]{3})", "variable a in lower case"),
            (r"[()\[\]]", "bracket"), (r"[-−–—]", "dash"), (r"\d [A-Z][a-z]", "sentence break missing?"),
            (r"[.?!,:;]\s*[.,:;]", "doubled punctuation"), (r"rupees[a-z]|[a-z]rupees", "glued rupees"),
            (r"\b[A-Z]{2,}\b", "capitals"), (r"\d \d", "two numbers together"), (r"\b\d+[a-z]\b(?<!st)(?<!nd)(?<!rd)(?<!th)", "number glued to letter"),
            (r"which is [A-Za-z]", "which is + word"), (r"equals equals|plus plus|minus minus|times times", "doubled operator"),
            (r"\b(?:yrs|approx|eq|vs|i\.e|e\.g|etc)\b", "abbreviation"), (r"\?[a-z]", "glued question mark"),
            (r"\bover\b(?! (?:\d|[a-z]\b|hour|the|both|all))", "over + word"), (r"'[^a-z]|[^a-z]'", "quote mark"),
        ]
        part = read(PART)
        for q in new_questions():
            e = part[q["id"]]
            for label, text in [("q", e["q"])] + [("o%d" % i, t) for i, t in enumerate(e["options"])] + [("h%d" % i, t) for i, t in enumerate(e["hints"])] + [("s%d" % i, t) for i, t in enumerate(e["steps"])]:
                for pat, why in pats:
                    m = re.search(pat, text)
                    if m:
                        a = max(0, m.start() - 50)
                        print("%s %s [%s] ...%s" % (q["id"][-12:], label, why, text[a:m.end() + 40]))
    elif mode == "src":
        qid, key = sys.argv[2], sys.argv[3]
        for q in new_questions():
            if q["id"].endswith(qid) or q["id"].startswith("AIGEN_grade5_" + qid):
                src = source_strings(q)
                own = q.get("stepByStep") or []
                items = [src["q"]] if key == "q" else src[key]
                for i, t in enumerate(items):
                    print("%s[%d] P %r" % (key, i, t))
                    if key == "steps" and i < len(own) and own[i].get("latex"):
                        print("       L %r" % own[i]["latex"])
    elif mode in ("dump", "new"):
        a, b = int(sys.argv[2]), int(sys.argv[3])
        part = read(PART)
        out = []
        for q in new_questions()[a:b]:
            src = source_strings(q)
            said = part.get(q["id"])
            own = q.get("stepByStep") or []
            out.append("=" * 90)
            out.append("%s | %s | %s | answer %s" % (q["id"], q.get("subTopic", ""), q.get("source", ""), q.get("correctAnswer", "")))
            out.append("  options   P %s" % " | ".join(src["options"]))
            if said is not None:
                out.append("            S %s" % " | ".join(said["options"]))
            for key in ("q", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = None if said is None else ([said[key]] if key == "q" else said[key])
                for i, text in enumerate(items):
                    label = key if key == "q" else "%s[%d]" % (key, i)
                    out.append("  %-9s P %r" % (label, text))
                    if key == "steps" and i < len(own) and own[i].get("latex"):
                        out.append("  %-9s L %r" % ("", own[i]["latex"]))
                    if spoken is not None and i < len(spoken):
                        out.append("  %-9s S %s" % ("", spoken[i]))
        text = "\n".join(out) + "\n"
        if mode == "dump":
            path = os.path.join(HERE, "draft_%d_%d.txt" % (a, b))
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("wrote " + path)
        else:
            sys.stdout.write(text)


if __name__ == "__main__":
    main()
