"""Write data/question-speech/parts-g4/<node>.json for gr4_equations.

    python -X utf8 scripts/speech/g4/gr4_equations.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_equations.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_equations.py --src 0 30    # print the source only (with maths lines)
    python -X utf8 scripts/speech/g4/gr4_equations.py --spoken 0 30 # print only the spoken lines that differ from print (~ marks a rule-made line)
    python -X utf8 scripts/speech/g4/gr4_equations.py --ids         # list the question ids

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (<node>_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the rules (gr4_equations_rules.say), with the step's maths line added where it carries the working;
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
import gr4_equations_rules as rules  # noqa: E402

NODE = "gr4_equations"

stats = {"hand": 0, "rule": 0, "base": 0, "failed": 0}
failures = []
kinds = {}
HAND = {}
LINES = {}


def load_hand(node):
    for n in range(1, 9):
        try:
            module = __import__("%s_hand%d" % (node, n))
        except ImportError:
            continue
        HAND.update(module.HAND)
        LINES.update(getattr(module, "LINES", {}))


def with_maths(source, latex):
    """A step's text followed by its maths line, when the maths line adds working the text does not say."""
    if not latex:
        return None
    maths = rules.from_latex(latex)
    if not maths:
        return None
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt:
        return None
    # The text already says this working: the maths line's numbers appear in it, in order.
    it = iter(st)
    if all(n in it for n in mt):
        return None
    # The text already ends on the same result, written as a sum.
    if "=" in source and st and st[-1] == mt[-1]:
        return None
    text = rules.say(source)
    spoken = rules.say(maths)
    if not text or not spoken:
        return None
    if text[-1] not in ".?!:,":
        text += "."
    if spoken[-1] not in ".?!":
        spoken += "."
    if not re.match(r"[A-Za-z] ", spoken):          # a letter that starts a sum stays as printed
        spoken = spoken[0].upper() + spoken[1:]
    return text + " " + spoken


def narrate_string(source, where, hand=None, also=None, latex="", stop=True):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex)))
    tries.append(("rule", rules.say(source, stop)))
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
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), pick(hand, "options", i), stop=False) for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), pick(hand, "hints", i)) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def show(q, entry, n, source_only=False):
    src = common.source_strings(q)
    own = q.get("stepByStep") or []
    qid = q["id"]
    print("=" * 6, n, qid)

    def pair(where, a, b, extra=""):
        if not a.strip():
            return
        tag = where.split(".", 1)[1]
        a1 = a.replace("\n", " // ")
        if source_only:
            print(" %s: %s%s" % (tag, a1, extra))
        elif "--spoken" in sys.argv:
            if a.strip() != b or tag == "q":
                short = tag[0].upper() + (tag[-2] if tag[-1] == "]" else "")
                print(" %s%s %s" % (short, "" if kinds.get(where) == "hand" else "~", b))
        elif a.strip() == b:
            print(" %s [%s] SAME  %s%s" % (tag, kinds.get(where, ""), b, extra))
        else:
            print(" %s [%s]\n   P: %s%s\n   S: %s" % (tag, kinds.get(where, ""), a1, extra, b))

    pair(qid + ".q", src["q"], entry["q"])
    for i, a in enumerate(src["options"]):
        pair("%s.options[%d]" % (qid, i), a, entry["options"][i])
    for key in ("hints", "steps"):
        for i, a in enumerate(src[key]):
            extra = ""
            if key == "steps" and i < len(own) and own[i].get("latex"):
                extra = "   {LATEX: %s}" % own[i]["latex"]
            pair("%s.%s[%d]" % (qid, key, i), a, entry[key][i], extra)


def main(node=NODE):
    load_hand(node)
    out = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", node + ".json")
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == node), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), out))
    print("lines:", stats)
    unknown = sorted(set(HAND) - set(part))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if "--ids" in sys.argv:
        for n, q in enumerate(questions):
            print(n, q["id"], "|", q.get("subTopic", ""), "|", q.get("questionText", "")[:80].replace("\n", " // "))
    for flag in ("--show", "--src", "--spoken"):
        if flag in sys.argv:
            i = sys.argv.index(flag)
            a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
            for n, q in enumerate(questions[a:b], a):
                show(q, part[q["id"]], n, flag == "--src")
    for p in failures[:0 if "--src" in sys.argv or "--quiet" in sys.argv else 80]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()
