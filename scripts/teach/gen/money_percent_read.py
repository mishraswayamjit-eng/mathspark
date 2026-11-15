"""Read money-percent lessons the way a child hears them, and look for rough edges.

    python -X utf8 scripts/teach/gen/money_percent_read.py sample 2     # 2 lessons of every rule wording, compact
    python -X utf8 scripts/teach/gen/money_percent_read.py ids <id> ...  # these lessons, compact
    python -X utf8 scripts/teach/gen/money_percent_read.py lint          # oddities across every lesson
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402
from money_percent_rules import rule_for  # noqa: E402

PART = os.path.join(ROOT, "data", "teach", "parts", "money-percent.json")


def compact(qid, q, script):
    print("=" * 78)
    print("%s  [%s]" % (qid, script["origin"]))
    print("Q: %s" % q["questionText"])
    for i, beat in enumerate(script["beats"], 1):
        print("%2d. %s" % (i, beat["say"]))
        for op in beat.get("board", []):
            if op["op"] == "write":
                print("      | %s%s" % (op["text"], "   (answer)" if op.get("tone") == "answer" else ""))
            elif op["op"] == "figure":
                print("      [figure: %s]" % op["spec"]["kind"])
            else:
                where = op.get("target", {}).get("text", "") if isinstance(op.get("target"), dict) else ""
                print("      (%s %s %s)" % (op["op"], where, op.get("text", op.get("note", op.get("shape", "")))))
        ask = beat.get("ask")
        if ask and ask["kind"] == "choose":
            print("      ? %s   -> %s" % (" / ".join(ask["choices"]), ask["choices"][ask["answer"]]))
            print("      if not: %s" % ask["ifNot"])


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sample"
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    qs = {q["id"]: q for q in load_grade5() if topic_of(q) == "money-percent"}
    if mode == "ids":
        for qid in sys.argv[2:]:
            compact(qid, qs[qid], part[qid])
        return
    if mode == "sample":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        skip = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        seen = collections.Counter()
        for qid in sorted(qs):
            found = rule_for(qs[qid])
            if not found or part[qid]["origin"] != "rule":
                continue
            seen[found[0]] += 1
            if skip < seen[found[0]] <= skip + n:
                compact(qid, qs[qid], part[qid])
        return
    # lint
    odd = []
    lengths = collections.Counter()
    asks = collections.Counter()
    first_right = 0
    total_asks = 0
    for qid, script in part.items():
        lengths[len(script["beats"])] += 1
        n_asks = 0
        for i, beat in enumerate(script["beats"]):
            say = beat["say"]
            where = "%s beat %d" % (qid, i + 1)
            sentences = [s for s in re.split(r"(?<=[.!?])\s+", say) if s]
            if len(sentences) > 4:
                odd.append("%s: %d sentences" % (where, len(sentences)))
            if len(say) > 215:
                odd.append("%s: %d characters" % (where, len(say)))
            for pat in (r"\b1 (hundreds|years|lots|pieces|rupees|times)\b", r"  ", r"\b(\w+) \1\b", r"\b0 ", r"\.\.", r" ,", r"\ba [aeiou]"):
                m = re.search(pat, say)
                if m:
                    odd.append("%s: '%s' in: %s" % (where, m.group(0), say))
            ask = beat.get("ask")
            if ask:
                n_asks += 1
                total_asks += 1
                if ask.get("answer") == 0:
                    first_right += 1
            if not beat.get("board") and not ask and i not in (0, len(script["beats"]) - 1):
                pass
        asks[n_asks] += 1
        marks = sum(1 for b in script["beats"] for op in b.get("board", []) if op["op"] not in ("write", "figure"))
        figs = sum(1 for b in script["beats"] for op in b.get("board", []) if op["op"] == "figure")
        if marks == 0:
            odd.append("%s: no marks on the board at all" % qid)
        if figs == 0:
            odd.append("%s: no figure" % qid)
    print("beats per lesson:", dict(sorted(lengths.items())))
    print("asks per lesson:", dict(sorted(asks.items())))
    print("right choice is first in %d of %d asks" % (first_right, total_asks))
    print("%d oddities" % len(odd))
    for o in odd[:int(sys.argv[2]) if len(sys.argv) > 2 else 80]:
        print("  " + o)


if __name__ == "__main__":
    main()
