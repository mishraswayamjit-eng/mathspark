"""Read-only helpers for the variants-papers part.

    python -X utf8 scripts/fixes/gen/variants_papers_dump.py shapes            # variant wordings grouped, numbers masked
    python -X utf8 scripts/fixes/gen/variants_papers_dump.py show <prefix> [n]  # questions in full
    python -X utf8 scripts/fixes/gen/variants_papers_dump.py grep <regex> [n]   # variants whose hints/steps/question match
    python -X utf8 scripts/fixes/gen/variants_papers_dump.py problems <prefix>  # questions find.py flags (not empty-hint only)
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
from check import load_seed  # noqa: E402
from find import problems_of  # noqa: E402

RESERVED = set(io.open(os.path.join(HERE, "..", "answers_ids.txt"), encoding="utf-8").read().split())


def is_variant(q):
    return (q.get("source") or "").startswith("variant_generator_phase")


def mask(t):
    return re.sub(r"\d+(?:\.\d+)?", "#", t)


def dump(q, found=None):
    print("=== %s [%s] key=%s src=%s %s" % (q["id"], q.get("subTopic"), q.get("correctAnswer"), q.get("source"), ",".join(found or problems_of(q))))
    print("Q: " + q.get("questionText", ""))
    for letter, o in zip("ABCD", q.get("options", [])):
        print("  %s) %s" % (letter, o.get("text", "") if isinstance(o, dict) else o))
    for i, h in enumerate(q.get("hints") or []):
        print("  H%d: %s" % (i + 1, h))
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  S%d: %s%s" % (i + 1, s.get("text", ""), ("  [latex: %s]" % s["latex"]) if s.get("latex") else ""))


def main():
    qs = load_seed()
    mode = sys.argv[1]
    if mode == "shapes":
        groups = collections.defaultdict(list)
        for qid in sorted(qs):
            q = qs[qid]
            if not is_variant(q):
                continue
            key = (tuple(mask(h) for h in q.get("hints") or []), tuple(mask(s.get("text", "")) for s in q.get("stepByStep") or []))
            groups[key].append(q)
        minimum = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        for key, members in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            if len(members) < minimum:
                continue
            probs = collections.Counter(p for q in members for p in problems_of(q))
            if len(sys.argv) > 3 and sys.argv[3] == "flagged" and not probs:
                continue
            if len(sys.argv) > 3 and sys.argv[3] == "small" and len(members) >= 4:
                continue
            print("##### %d questions  %s  e.g. %s" % (len(members), dict(probs), members[0]["id"]))
            qshapes = collections.Counter(mask(q["questionText"]) for q in members)
            for s, n in qshapes.most_common(4):
                print("  Q(%d): %s" % (n, s[:150]))
            for h in key[0]:
                print("  H: " + h)
            for s in key[1]:
                print("  S: " + s)
        print("%d shapes" % len(groups))
    elif mode == "show":
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
        n = 0
        for qid in sorted(qs):
            if qid.startswith(sys.argv[2]) and n < limit:
                dump(qs[qid])
                n += 1
    elif mode == "grep":
        rx = re.compile(sys.argv[2])
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
        n = 0
        for qid in sorted(qs):
            q = qs[qid]
            if not is_variant(q):
                continue
            blob = "\n".join([q["questionText"]] + list(q.get("hints") or []) + [s.get("text", "") for s in q.get("stepByStep") or []])
            if rx.search(blob):
                n += 1
                if n <= limit:
                    dump(q)
        print("%d match" % n)
    elif mode == "ids":
        for qid in sys.argv[2].split(","):
            dump(qs[qid])
    elif mode == "sums":
        # A looser scan than check.py: every "a op b = c" in a variant's hints and steps.
        from fractions import Fraction
        rx = re.compile(r"(\d+(?:\.\d+)?)\s*([÷×+−/-])\s*(\d+(?:\.\d+)?)\s*=\s*(?:Rs\.\s*)?(\d+(?:\.\d+)?)(?![\d/]|\.\d)")
        n = 0
        for qid in sorted(qs):
            q = qs[qid]
            if not is_variant(q):
                continue
            texts = list(q.get("hints") or []) + [s.get("text", "") for s in q.get("stepByStep") or []]
            bad = []
            for t in texts:
                for m in rx.finditer(t):
                    if t[:m.start()].rstrip()[-1:] in ("×", "÷", "+", "−", "-", "/", "("):
                        continue
                    if t[m.end():].lstrip()[:1] in ("×", "÷", "/"):
                        continue
                    a, op, b, c = Fraction(m.group(1)), m.group(2), Fraction(m.group(3)), Fraction(m.group(4))
                    if op in "÷/" and b == 0:
                        continue
                    v = {"÷": lambda: a / b, "/": lambda: a / b, "×": lambda: a * b, "+": lambda: a + b, "−": lambda: a - b, "-": lambda: a - b}[op]()
                    if v != c:
                        bad.append(m.group(0) + "   <<< in: " + t)
            if bad:
                n += 1
                print("=== %s%s  %s" % (qid, " RESERVED" if qid in RESERVED else "", q["questionText"]))
                for b in bad:
                    print("    " + b)
        print("%d questions" % n)
    elif mode == "noop":
        rx = re.compile(r"(?<![\d/])(\d+/\d+) = \1(?![\d/])")
        n = 0
        for qid in sorted(qs):
            q = qs[qid]
            if not is_variant(q):
                continue
            hit = [s.get("text", "") for s in q.get("stepByStep") or [] if rx.search(s.get("text", ""))]
            if hit:
                n += 1
                print("%s%s | %s | %s" % (qid, " RESERVED" if qid in RESERVED else "", q["questionText"], " || ".join(hit)))
        print("%d questions" % n)
    elif mode == "problems":
        n = 0
        skip = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else {"empty-hint"}
        for qid in sorted(qs):
            q = qs[qid]
            if not qid.startswith(sys.argv[2]):
                continue
            found = [p for p in problems_of(q) if p not in skip]
            if found:
                n += 1
                dump(q, found + (["RESERVED"] if qid in RESERVED else []))
        print("%d questions" % n)


if __name__ == "__main__":
    main()
