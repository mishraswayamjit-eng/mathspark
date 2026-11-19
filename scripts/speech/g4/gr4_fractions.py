"""Write data/question-speech/parts-g4/gr4_fractions.json.

    python -X utf8 scripts/speech/g4/gr4_fractions.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_fractions.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_fractions.py --ids         # also list the question ids

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_fractions_hand*.py, keyed by question id, or LINES keyed by the printed line);
  2. the fraction rules (gr4_fractions_rules.say);
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
import gr4_fractions_rules as rules  # noqa: E402

NODE = "gr4_fractions"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")

HAND = {}
LINES = {}
for name in ("gr4_fractions_hand1", "gr4_fractions_hand2", "gr4_fractions_hand3", "gr4_fractions_hand4"):
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
    """A step's text followed by its maths line, when the maths line adds working the text does not say."""
    if not latex or re.fullmatch(r"\s*\\boxed\{.*\}\s*", latex):
        return None
    maths = rules.from_latex(latex)
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt:
        return None
    it = iter(st)
    if all(t in it for t in mt):       # the text already says the numbers of the maths line, in order
        return None
    text = rules.family(source) or rules.say(source)
    spoken = rules.say(maths)
    if not text or not spoken:
        return None
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
    tries.append(("rule", rules.family(source)))
    tries.append(("rule", rules.say(source, sentence=".options[" not in where)))
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
    failures.append("%s: no rule gives a passing line for: %s" % (where, source))
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
    print("=" * 30, n, qid)

    def pair(where, a, b, extra=""):
        if not a.strip():
            return
        k = kinds.get(where, "")
        if a.strip() == b and "--brief" in sys.argv and not where.endswith(".q"):
            return
        if a.strip() == b:
            print(" %s [%s] SAME  %s%s" % (where.split(".", 1)[1], k, b, extra))
        else:
            print(" %s [%s]\n   P: %s%s\n   S: %s" % (where.split(".", 1)[1], k, a.replace("\n", " // "), extra, b))

    pair(qid + ".q", src["q"], entry["q"])
    if src["options"] != entry["options"]:
        print(" optP: " + "  ¦  ".join(src["options"]))
    print(" optS: " + "  ¦  ".join(entry["options"]) + "   " + ",".join(kinds.get("%s.options[%d]" % (qid, i), "") for i in range(4)))
    for key in ("hints", "steps"):
        for i, a in enumerate(src[key]):
            extra = ""
            if key == "steps" and i < len(own) and own[i].get("latex"):
                extra = "   {LATEX: %s}" % own[i]["latex"]
            pair("%s.%s[%d]" % (qid, key, i), a, entry[key][i], extra)


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
        print(" ".join(q["id"] for q in questions))
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            show(q, part[q["id"]], n)
    for p in failures[:int(os.environ.get("MAXFAIL", "80"))]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()
