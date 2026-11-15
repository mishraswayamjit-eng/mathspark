"""Review aid: what the place-value script cannot narrate yet. Reads the seed; writes nothing.

    python -X utf8 scripts/speech/topics/place_value_gaps.py          # generated wordings with no rule (one example each)
    python -X utf8 scripts/speech/topics/place_value_gaps.py hand     # hand-narrated strings that no longer match, with their source
    python -X utf8 scripts/speech/topics/place_value_gaps.py hand 0 20  # ... only problems 0 to 19
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from common import load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402
import place_value_rules as rules  # noqa: E402

questions = sorted((q for q in load_grade5() if topic_of(q) == "place-value"), key=lambda q: q["id"])


def flat(d):
    return [("q", d["q"])] + [("o", o) for o in d["options"]] + [("h", h) for h in d["hints"]] + [("s", s) for s in d["steps"]]


if len(sys.argv) > 1 and sys.argv[1] == "hand":
    HAND = {}
    for name in ("place_value_hand_fp_a", "place_value_hand_fp_b", "place_value_hand_fp_c", "place_value_hand_ws",
                 "place_value_hand_ws2"):
        HAND.update(__import__(name).HAND)
    lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
    n = 0
    for q in questions:
        hand = HAND.get(q["id"])
        if not hand:
            continue
        src = source_strings(q)
        own = q.get("stepByStep") or []
        pairs = [("q", src["q"], hand["q"], None)]
        for i, h in enumerate(src["hints"]):
            pairs.append(("hints[%d]" % i, h, hand["hints"][i] if i < len(hand["hints"]) else None, None))
        for i, s in enumerate(src["steps"]):
            latex = own[i].get("latex") if i < len(own) else None
            pairs.append(("steps[%d]" % i, s, hand["steps"][i] if i < len(hand["steps"]) else None, latex))
        if len(hand["steps"]) != len(src["steps"]):
            pairs.append(("steps", "COUNT now %d, hand has %d" % (len(src["steps"]), len(hand["steps"])), None, None))
        for where, printed, spoken, latex in pairs:
            also = None if not latex else "%s %s" % (printed, re.sub(r"\\[a-zA-Z]+", " ", latex))
            if spoken is not None and not check_string(spoken, printed, where, also):
                # Passes the checker. With "drift", still show it when the words have moved far from the print.
                if "drift" not in sys.argv:
                    continue
                import difflib
                a = re.findall(r"[a-z]+", printed.lower())
                b = re.findall(r"[a-z]+", spoken.lower())
                if not a or difflib.SequenceMatcher(None, a, b).ratio() >= 0.62:
                    continue
            if lo <= n < hi:
                print("%3d %s %s" % (n, q["id"], where))
                print("    PRINT  %s%s" % (printed, ("   [LATEX %s]" % latex) if latex else ""))
                print("    OLD    %s" % spoken)
            n += 1
    print("%d hand problems" % n)
else:
    seen = {}
    for q in questions:
        if q["id"].startswith("EXT_"):
            continue
        src = source_strings(q)
        for kind, text in flat(src):
            try:
                rules.say(text, src["q"])
            except ValueError:
                key = (kind, re.sub(r"\d[\d,.]*", "N", text))
                seen.setdefault(key, [text, 0, q["id"]])
                seen[key][1] += 1
    for (kind, _), (text, n, qid) in sorted(seen.items()):
        print("%4d %s  %s   <%s>" % (n, kind, text, qid))
    print("%d wordings without a rule" % len(seen))
