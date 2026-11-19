"""Write data/question-speech/parts-g4/gr4_numbers.json.

    python -X utf8 scripts/speech/g4/gr4_numbers.py                # write the part file
    python -X utf8 scripts/speech/g4/gr4_numbers.py --show 0 30    # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_numbers.py --ids          # also list the question ids

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_numbers_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the topic rules (gr4_numbers_rules.say);
  3. the shared base converter (common.speak), as a last resort.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import common  # noqa: E402
from validate import check_string  # noqa: E402
import gr4_numbers_rules as rules  # noqa: E402

NODE = "gr4_numbers"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")

HAND = {}
LINES = {}
for name in ("gr4_numbers_hand1", "gr4_numbers_hand2", "gr4_numbers_hand3", "gr4_numbers_hand4"):
    try:
        module = __import__(name)
    except ImportError:
        continue
    HAND.update(module.HAND)
    LINES.update(getattr(module, "LINES", {}))

stats = {"hand": 0, "rule": 0, "base": 0, "failed": 0}
failures = []
kinds = {}


def with_maths(source, latex):
    """A step's text followed by its maths line, when the maths line is plain working the text does not say."""
    maths = rules.from_latex(latex)
    if not maths:
        return None
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt or (len(mt) <= len(st) and st[-len(mt):] == mt):
        return None
    text = rules.say(source)
    spoken = rules.say(maths)
    if text[-1] not in ".?!:":
        text += "."
    if spoken[-1] not in ".?!":
        spoken += "."
    return text + " " + spoken


def narrate_string(source, where, hand=None, also=None, latex=""):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex)))
    tries.append(("rule", rules.say(source)))
    tries.append(("base", common.speak(source)))
    for kind, spoken in tries:
        if not spoken:
            continue
        problems = check_string(spoken, source, where, also)
        if not problems:
            stats[kind] += 1
            kinds[where] = kind
            return spoken
        if kind == "hand":
            failures.extend(problems)
    stats["failed"] += 1
    kinds[where] = "FAILED"
    failures.append("%s: no rule gives a passing line for: %s\n        rule said: %s" % (where, source, rules.say(source)))
    return rules.say(source)


def pick(hand, key, i):
    items = hand.get(key) or []
    return items[i] if i < len(items) else None


def narrate(q):
    src = common.source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []
    qid = q["id"]
    steps = []
    for i, text in enumerate(src["steps"]):
        latex = own[i].get("latex", "") if i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        steps.append(narrate_string(text, "%s.steps[%d]" % (qid, i), pick(hand, "steps", i), also, latex))
    return {
        "q": narrate_string(src["q"], qid + ".q", hand.get("q")),
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), pick(hand, "options", i)) for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), pick(hand, "hints", i)) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def show(q, entry, n):
    src = common.source_strings(q)
    own = q.get("stepByStep") or []
    qid = q["id"]
    print("=" * 20, n, qid, "|", q.get("subTopic", ""))

    def pair(tag, where, a, b, extra=""):
        if not a.strip():
            return
        k = kinds.get(where, "")[:1]
        if a.strip() == b:
            print(" %s %s= %s%s" % (tag, k, b, extra))
        else:
            print(" %s P: %s%s\n  %s S: %s" % (tag, a.replace("\n", " // "), extra, k, b))

    pair("Q", qid + ".q", src["q"], entry["q"])
    for i, a in enumerate(src["options"]):
        pair("O%d" % i, "%s.options[%d]" % (qid, i), a, entry["options"][i])
    for key in ("hints", "steps"):
        for i, a in enumerate(src[key]):
            extra = ""
            if key == "steps" and i < len(own) and own[i].get("latex"):
                extra = "   {LATEX: %s}" % own[i]["latex"]
            pair("%s%d" % (key[0].upper(), i), "%s.%s[%d]" % (qid, key, i), a, entry[key][i], extra)


def main():
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), OUT))
    print("lines:", stats)
    unknown = sorted(set(HAND) - set(part))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if "--ids" in sys.argv:
        for n, q in enumerate(questions):
            print(n, q["id"], "|", q.get("subTopic", ""), "|", q.get("questionText", "")[:80].replace("\n", " // "))
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            show(q, part[q["id"]], n)
    if "--spoken" in sys.argv:
        # only the narration, for reading back as the voice would say it
        i = sys.argv.index("--spoken")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            e = part[q["id"]]
            print("== %d %s" % (n, q["id"]))
            print(" Q: " + e["q"])
            print(" O: " + "  ¦  ".join(e["options"]))
            for key in ("hints", "steps"):
                for j, line in enumerate(e[key]):
                    if line:
                        print(" %s%d: %s" % (key[0].upper(), j, line))
    for p in failures[:int(os.environ.get("MAXFAIL", "80"))]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()
