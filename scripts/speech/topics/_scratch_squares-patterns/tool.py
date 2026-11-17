"""Scratch helper for the squares-patterns narration work.

    python -X utf8 scripts/speech/topics/_scratch_squares-patterns/tool.py snapshot
    python -X utf8 scripts/speech/topics/_scratch_squares-patterns/tool.py compare
    python -X utf8 scripts/speech/topics/_scratch_squares-patterns/tool.py new [start] [end]     # source of new questions
    python -X utf8 scripts/speech/topics/_scratch_squares-patterns/tool.py side [start] [end]    # source and narration
    python -X utf8 scripts/speech/topics/_scratch_squares-patterns/tool.py symbols               # odd characters in new sources
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

SLUG = "squares-patterns"
PART = os.path.join(PARTS, SLUG + ".json")
SNAP = os.path.join(HERE, "part_before.json")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def new_questions():
    old = read(SNAP)
    qs = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    return [q for q in qs if q["id"] not in old]


def main():
    cmd = sys.argv[1]
    numeric = cmd in ("new", "side")
    a = int(sys.argv[2]) if numeric and len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if numeric and len(sys.argv) > 3 else None
    if cmd == "snapshot":
        if os.path.exists(SNAP):
            sys.exit("snapshot already exists; not overwriting")
        with io.open(PART, "rb") as f:
            raw = f.read()
        with io.open(SNAP, "wb") as f:
            f.write(raw)
        print("saved %d bytes, %d entries" % (len(raw), len(json.loads(raw.decode("utf-8")))))
    elif cmd == "restore":
        old, now = read(SNAP), read(PART)
        fixed = 0
        for k, v in old.items():
            if now.get(k) != v:
                now[k] = v
                fixed += 1
        with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
            json.dump({k: now[k] for k in sorted(now)}, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("restored %d old entries" % fixed)
    elif cmd == "compare":
        old, now = read(SNAP), read(PART)
        changed = [k for k in old if json.dumps(old[k], ensure_ascii=False, sort_keys=True)
                   != json.dumps(now.get(k), ensure_ascii=False, sort_keys=True)]
        print("old entries: %d, now: %d, new: %d" % (len(old), len(now), len(set(now) - set(old))))
        print("old entries changed or missing: %d" % len(changed))
        for k in changed[:40]:
            print("  ", k)
            if k in now:
                for key in ("q", "options", "hints", "steps"):
                    if old[k][key] != now[k][key]:
                        print("     was:", old[k][key])
                        print("     now:", now[k][key])
    elif cmd == "new":
        qs = new_questions()
        print("%d new questions" % len(qs))
        for i, q in list(enumerate(qs))[a:b]:
            src = source_strings(q)
            own = q.get("stepByStep") or []
            print("=" * 90)
            print(i, q["id"], "|", q.get("subTopic", ""), "| answer", q.get("correctAnswer"))
            print(" Q:", json.dumps(src["q"], ensure_ascii=False))
            for j, t in enumerate(src["options"]):
                print(" O%d: %s" % (j, json.dumps(t, ensure_ascii=False)))
            for j, t in enumerate(src["hints"]):
                print(" H%d: %s" % (j, json.dumps(t, ensure_ascii=False)))
            for j, t in enumerate(src["steps"]):
                lx = own[j].get("latex", "") if j < len(own) else ""
                print(" S%d: %s%s" % (j, json.dumps(t, ensure_ascii=False), ("   LATEX " + json.dumps(lx, ensure_ascii=False)) if lx else ""))
    elif cmd in ("side", "pick"):
        part = read(PART)
        qs = new_questions()
        chosen = list(enumerate(qs))[a:b]
        if cmd == "pick":
            want = {int(x) for x in sys.argv[2].split(",")}
            chosen = [(i, q) for i, q in enumerate(qs) if i in want]
        for i, q in chosen:
            src = source_strings(q)
            said = part.get(q["id"])
            print("=" * 90)
            print(i, q["id"])
            own = q.get("stepByStep") or []
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = None if said is None else ([said[key]] if key == "q" else said[key])
                if key == "options" and spoken == items:
                    print(" O: " + " | ".join(items))
                    continue
                for j, t in enumerate(items):
                    if not t.strip():
                        continue
                    lx = own[j].get("latex", "") if key == "steps" and j < len(own) else ""
                    sp = spoken[j] if spoken is not None and j < len(spoken) else "(none)"
                    if sp == t and not lx:
                        print(" %s%d = %s" % (key[0].upper(), j, t))
                        continue
                    print(" %s%d P: %s%s" % (key[0].upper(), j, t, ("  ||  " + lx) if lx else ""))
                    print("     S: %s" % sp)
    elif cmd == "brief":
        # Only the spoken lines that differ from print by more than capitals and dashes.
        import re
        a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        b = int(sys.argv[3]) if len(sys.argv) > 3 else None
        part = read(PART)

        def norm(t):
            t = re.sub(r"\s*—\s*", ", ", t.lower())
            t = re.sub(r"₹\s*([\d,]+)", r"\1 rupees", t)
            return re.sub(r"\s+", " ", t).strip()

        for i, q in list(enumerate(new_questions()))[a:b]:
            src = source_strings(q)
            said = part.get(q["id"])
            own = q.get("stepByStep") or []
            print("== %d %s" % (i, q["id"][-12:]))
            if said is None:
                print("   (no entry)")
                continue
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = [said[key]] if key == "q" else said[key]
                for j, t in enumerate(items):
                    if not t.strip() or norm(t) == norm(spoken[j]):
                        continue
                    print(" %s%d %s" % (key[0].upper(), j, spoken[j]))
    elif cmd == "sgrep":
        # Spoken lines matching a pattern, with their source.
        import re
        pat = re.compile(sys.argv[2])
        part = read(PART)
        n = 0
        for i, q in enumerate(new_questions()):
            src = source_strings(q)
            said = part.get(q["id"])
            own = q.get("stepByStep") or []
            if said is None:
                continue
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = [said[key]] if key == "q" else said[key]
                for j, t in enumerate(items):
                    if spoken[j] and pat.search(spoken[j]):
                        n += 1
                        lx = own[j].get("latex", "") if key == "steps" and j < len(own) else ""
                        print("%d %s %s%d P: %s%s" % (i, q["id"], key[0].upper(), j, json.dumps(t, ensure_ascii=False), ("  ||  " + lx) if lx else ""))
                        print("      S: %s" % spoken[j])
        print(n, "strings")
    elif cmd == "grep":
        import re
        pat = re.compile(sys.argv[2])
        part = read(PART)
        n = 0
        for i, q in enumerate(new_questions()):
            src = source_strings(q)
            said = part.get(q["id"])
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = None if said is None else ([said[key]] if key == "q" else said[key])
                for j, t in enumerate(items):
                    if pat.search(t):
                        n += 1
                        print("%d %s %s%d P: %s" % (i, q["id"][-12:], key[0].upper(), j, json.dumps(t, ensure_ascii=False)))
                        if spoken is not None:
                            print("      S: %s" % spoken[j])
        print(n, "strings")
    elif cmd == "latex":
        seen = collections.Counter()
        import re
        for q in new_questions():
            for s in q.get("stepByStep") or []:
                for m in re.findall(r"\\[a-zA-Z]+|\\.", s.get("latex", "") or ""):
                    seen[m] += 1
        for c, n in seen.most_common():
            print(repr(c), n)
        for q in new_questions():
            for s in q.get("stepByStep") or []:
                lx = s.get("latex", "") or ""
                if re.search(sys.argv[2] if len(sys.argv) > 2 else r"\\begin|\\left|\\cdot|\\underbrace|\\overline", lx):
                    print(q["id"][-12:], json.dumps(lx, ensure_ascii=False))
    elif cmd == "symbols":
        count = collections.Counter()
        for q in new_questions():
            src = source_strings(q)
            for t in [src["q"]] + src["options"] + src["hints"] + src["steps"]:
                for c in t:
                    if not (c.isalnum() or c in " .,?!'\"():;-"):
                        count[c] += 1
        for c, n in count.most_common():
            print(repr(c), n)


if __name__ == "__main__":
    main()
