"""Scratch helper for the geometry narration work.

    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py snapshot     # save the part file as it is now (once)
    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py compare      # old entries unchanged?
    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py missing      # ids with no entry in the snapshot
    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py source A B   # source of new questions [A:B] as JSON
    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py show A B     # source and narration of new questions [A:B]
    python -X utf8 scripts/speech/topics/_scratch_geometry/tool.py grep REGEX   # spoken strings of new entries matching
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

PART = os.path.join(PARTS, "geometry.json")
SNAP = os.path.join(HERE, "geometry_before.json")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def new_questions():
    old = read(SNAP)
    qs = sorted((q for q in load_grade5() if topic_of(q) == "geometry"), key=lambda q: q["id"])
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
    elif cmd == "compare":
        old, new = read(SNAP), read(PART)
        changed = [k for k in old if json.dumps(old[k], ensure_ascii=False) != json.dumps(new.get(k), ensure_ascii=False)]
        print("old entries: %d, now: %d, added: %d, changed or missing: %d" % (len(old), len(new), len(set(new) - set(old)), len(changed)))
        for k in changed[:20]:
            print("  CHANGED", k)
        # byte check: the old file's text for each old entry must appear in the new file
        with io.open(SNAP, encoding="utf-8") as f:
            old_text = f.read()
        with io.open(PART, encoding="utf-8") as f:
            new_text = f.read()
        bad = 0
        for k, v in old.items():
            chunk = ' %s: %s' % (json.dumps(k), json.dumps(v, ensure_ascii=False, indent=1).replace("\n", "\n "))
            if chunk not in old_text:
                sys.exit("internal: cannot find old chunk for %s" % k)
            if chunk not in new_text:
                bad += 1
        print("old entries whose bytes are not in the new file: %d" % bad)
    elif cmd == "missing":
        for i, q in enumerate(new_questions()):
            src = source_strings(q)
            print("%4d %-28s %-18s o%d h%d s%d | %s" % (i, q["id"], q.get("source", ""), len(src["options"]),
                  sum(1 for h in src["hints"] if h), len(src["steps"]), q["questionText"][:110].replace("\n", " ")))
    elif cmd == "source":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        out = {q["id"]: source_strings(q) for q in new_questions()[a:b]}
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif cmd == "show":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        part = read(PART)
        for q in new_questions()[a:b]:
            src = source_strings(q)
            said = part.get(q["id"])
            print("=" * 90)
            print(q["id"], "|", q.get("subTopic", ""))
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = None if said is None else ([said[key]] if key == "q" else said[key])
                for i, text in enumerate(items):
                    print("  %s%d P %s" % (key[0], i, text))
                    if spoken is not None and i < len(spoken) and spoken[i] != text:
                        print("     S %s" % spoken[i])
    elif cmd == "grep":
        pat = re.compile(sys.argv[2])
        part = read(PART)
        n = 0
        for q in new_questions():
            said = part.get(q["id"])
            if not said:
                continue
            for key in ("q", "options", "hints", "steps"):
                for i, t in enumerate([said[key]] if key == "q" else said[key]):
                    if pat.search(t):
                        n += 1
                        print("%s %s%d: %s" % (q["id"], key[0], i, t))
        print(n, "matches")
    elif cmd == "latex":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        for q in new_questions()[a:b]:
            print(q["id"], "| qLatex:", repr(q.get("questionLatex", "")))
            for s in q.get("stepByStep") or []:
                print("   T %s" % s.get("text", ""))
                print("   L %s" % s.get("latex", ""))
    elif cmd == "say":
        a, b = int(sys.argv[2]), int(sys.argv[3])
        part = read(PART)
        for n, q in enumerate(new_questions()[a:b]):
            said = part[q["id"]]
            print("== %d %s" % (a + n, q["id"]))
            print("q: " + said["q"])
            print("o: " + " | ".join(said["options"]))
            for i, t in enumerate(said["hints"]):
                print("h%d: %s" % (i, t))
            for i, t in enumerate(said["steps"]):
                print("s%d: %s" % (i, t))
    elif cmd == "diff":
        old, new = read(SNAP), read(PART)
        qs = {q["id"]: q for q in load_grade5()}
        for k in old:
            if old[k] == new.get(k):
                continue
            print("=" * 80)
            print(k)
            src = source_strings(qs[k])
            for key in ("q", "options", "hints", "steps"):
                a = [old[k][key]] if key == "q" else old[k][key]
                b = [new[k][key]] if key == "q" else new[k][key]
                c = [src[key]] if key == "q" else src[key]
                if len(a) != len(b):
                    print("  %s: lengths %d -> %d" % (key, len(a), len(b)))
                for i in range(max(len(a), len(b))):
                    x = a[i] if i < len(a) else None
                    y = b[i] if i < len(b) else None
                    if x != y:
                        print("  %s[%d] SRC %s" % (key, i, c[i] if i < len(c) else None))
                        print("        OLD %s" % x)
                        print("        NEW %s" % y)
    elif cmd == "one":
        # one N slot slot ...   exact source (repr) and maths line of the named slots of new question N
        q = new_questions()[int(sys.argv[2])]
        src = source_strings(q)
        own = q.get("stepByStep") or []
        print(q["id"])
        for slot in sys.argv[3:]:
            kind, i = slot[0], int(slot[1:] or 0)
            text = src["q"] if kind == "q" else {"o": src["options"], "h": src["hints"], "s": src["steps"]}[kind][i]
            print("%s T %r" % (slot, text))
            if kind == "s" and i < len(own):
                print("%s L %r" % (slot, own[i].get("latex", "")))
    elif cmd == "latexcmds":
        import collections
        c = collections.Counter()
        ex = {}
        for q in new_questions():
            for s in q.get("stepByStep") or []:
                for w in re.findall(r"\\[a-zA-Z]+|\\.|[_^]\{?[^\\ ]{0,6}", s.get("latex", "")):
                    c[w] += 1
                    ex.setdefault(w, s.get("latex", ""))
        for w, n in sorted(c.items(), key=lambda kv: -kv[1]):
            print("%5d %-14s %s" % (n, w, ex[w][:110]))
    elif cmd == "latexgrep":
        pat = re.compile(sys.argv[2])
        for q in new_questions():
            for i, s in enumerate(q.get("stepByStep") or []):
                if pat.search(s.get("latex", "")):
                    print("%s s%d: %s || %s" % (q["id"][-12:], i, s.get("text", ""), s.get("latex", "")))
    elif cmd == "caps":
        import collections
        c = collections.Counter()
        for q in new_questions():
            src = source_strings(q)
            for t in [src["q"]] + src["options"] + src["hints"] + src["steps"]:
                for w in re.findall(r"\b[A-Z]{2,}\b", t):
                    c[w] += 1
        print(sorted(c.items()))
    elif cmd == "chars":
        import collections
        c = collections.Counter()
        for q in new_questions():
            src = source_strings(q)
            for t in [src["q"]] + src["options"] + src["hints"] + src["steps"]:
                for ch in t:
                    if not (ch.isalnum() or ch in " .,?!'"):
                        c[ch] += 1
        print(sorted(c.items(), key=lambda kv: -kv[1]))
    elif cmd == "srcgrep":
        pat = re.compile(sys.argv[2])
        n = 0
        for q in new_questions():
            src = source_strings(q)
            for key in ("q", "options", "hints", "steps"):
                for i, t in enumerate([src[key]] if key == "q" else src[key]):
                    if pat.search(t):
                        n += 1
                        print("%s %s%d: %s" % (q["id"], key[0], i, t))
        print(n, "matches")


if __name__ == "__main__":
    main()
