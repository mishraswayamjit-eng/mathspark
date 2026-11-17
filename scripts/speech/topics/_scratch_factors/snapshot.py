"""Scratch tools for the factors narration extension.

    python -X utf8 scripts/speech/topics/_scratch_factors/snapshot.py save      # copy the part file once (never overwrites)
    python -X utf8 scripts/speech/topics/_scratch_factors/snapshot.py compare   # existing entries unchanged?
    python -X utf8 scripts/speech/topics/_scratch_factors/snapshot.py new 0 20  # source of new questions, as JSON
    python -X utf8 scripts/speech/topics/_scratch_factors/snapshot.py show 0 20 # new questions: source next to narration
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402

PART = os.path.join(PARTS, "factors.json")
SNAP = os.path.join(HERE, "factors_before.json")


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def new_questions():
    old = load(SNAP)
    return sorted((q for q in load_grade5() if topic_of(q) == "factors" and q["id"] not in old), key=lambda q: q["id"])


def main():
    mode = sys.argv[1]
    if mode == "save":
        if os.path.exists(SNAP):
            sys.exit("snapshot already exists; not overwriting")
        with io.open(PART, "rb") as f:
            data = f.read()
        with io.open(SNAP, "wb") as f:
            f.write(data)
        print("saved %d bytes, %d entries" % (len(data), len(json.loads(data.decode("utf-8")))))
    elif mode == "compare":
        old, new = load(SNAP), load(PART)
        changed = [k for k in old if json.dumps(old[k], ensure_ascii=False) != json.dumps(new.get(k), ensure_ascii=False)]
        print("before %d entries, now %d; added %d; existing changed or missing: %d"
              % (len(old), len(new), len(set(new) - set(old)), len(changed)))
        for k in changed[:20]:
            print("  CHANGED", k)
        # byte-level: each old entry's serialised block must appear verbatim in the new file
        with io.open(PART, encoding="utf-8") as f:
            text = f.read()
        missing = 0
        for k, v in old.items():
            block = json.dumps({k: v}, ensure_ascii=False, indent=1)[2:-2]
            if block not in text:
                missing += 1
        print("old entry blocks not found verbatim in file: %d" % missing)
    elif mode == "new":
        qs = new_questions()[int(sys.argv[2]):int(sys.argv[3])]
        out = {}
        for q in qs:
            src = source_strings(q)
            own = q.get("stepByStep") or []
            src["latex"] = [s.get("latex", "") for s in own]
            src["sub"] = q.get("subTopic", "")
            out[q["id"]] = src
        print(json.dumps(out, ensure_ascii=False, indent=1))
    elif mode in ("one", "grep"):
        part = load(PART)
        wanted = sys.argv[2:]
        for q in new_questions():
            src, said = source_strings(q), part.get(q["id"])
            rows = [("q", src["q"], said["q"])]
            rows += [("o%d" % i, s, e) for i, (s, e) in enumerate(zip(src["options"], said["options"]))]
            rows += [("h%d" % i, s, e) for i, (s, e) in enumerate(zip(src["hints"], said["hints"]))]
            rows += [("s%d" % i, s, e) for i, (s, e) in enumerate(zip(src["steps"], said["steps"]))]
            own = q.get("stepByStep") or []
            short = q["id"].replace("AIGEN_grade5_", "")[:8] if q["id"].startswith("AIGEN") else q["id"]
            for key, s, e in rows:
                if mode == "one":
                    hit = any(w == "%s.%s" % (short, key) for w in wanted)
                else:
                    hit = bool(re.search(wanted[0], e))
                if hit:
                    latex = own[int(key[1:])].get("latex", "") if key[0] == "s" and int(key[1:]) < len(own) else ""
                    print("%s.%s\n  P: %s\n  S: %s%s" % (short, key, s.replace("\n", " ⏎ "), e, "\n  L: " + latex if latex else ""))
    elif mode == "caps":
        import collections
        seen = collections.Counter()
        odd = collections.Counter()
        for q in new_questions():
            src = source_strings(q)
            for t in [src["q"]] + src["options"] + src["hints"] + src["steps"]:
                seen.update(re.findall(r"\b[A-Z]{2,}\b", t))
                odd.update(c for c in t if ord(c) > 127 or c in "*_^{}[]|/\\<>~#@$")
        print(sorted(seen.items()))
        print(sorted(odd.items()))
    elif mode == "show":
        part = load(PART)
        qs = new_questions()[int(sys.argv[2]):int(sys.argv[3])]
        for q in qs:
            src, said = source_strings(q), part.get(q["id"])
            print("## " + q["id"])
            rows = [("q", src["q"], said["q"])]
            rows += [("o%d" % i, s, e) for i, (s, e) in enumerate(zip(src["options"], said["options"]))]
            rows += [("h%d" % i, s, e) for i, (s, e) in enumerate(zip(src["hints"], said["hints"]))]
            rows += [("s%d" % i, s, e) for i, (s, e) in enumerate(zip(src["steps"], said["steps"]))]
            own = q.get("stepByStep") or []
            brief = len(sys.argv) > 4
            for key, s, e in rows:
                if not s.strip() or s.strip() == e:
                    continue
                also = None
                if key[0] == "s" and int(key[1:]) < len(own) and own[int(key[1:])].get("latex"):
                    latex = own[int(key[1:])]["latex"]
                    also = "%s %s" % (s, re.sub(r"\\[a-zA-Z]+", " ", latex))
                bad = check_string(e, s, key, also)
                odd = bad or re.search(r"[→\n*{}/\\^_|⃣]|\bR\d|\.\.\.|…", s)
                if brief and not odd:
                    print("%s: %s" % (key, e))
                else:
                    print("%s P: %s\n   %s: %s" % (key, s.replace("\n", " ⏎ "), "BAD" if bad else "  S", e))
                if brief and also and key[0] == "s":
                    print("     [latex] %s" % latex)


if __name__ == "__main__":
    main()
