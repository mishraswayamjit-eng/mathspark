"""Write data/question-speech/parts-g4/gr4_puzzles.json.

    python -X utf8 scripts/speech/g4/gr4_puzzles.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_puzzles.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_puzzles.py --show 0 30 --brief   # leave out lines spoken exactly as printed
    python -X utf8 scripts/speech/g4/gr4_puzzles.py --ids         # also list the question ids

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (<topic id>_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the step's text followed by its maths line, both by rule, when the text has no working of its own;
  3. the topic rules (<topic id>_rules.say);
  4. the shared base converter (common.speak), as a last resort.

run(node, rules) is the engine; gr4_time.py and gr4_data.py (same author) call it with their own rules.
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

stats = {"hand": 0, "rule": 0, "base": 0, "failed": 0}
failures = []
kinds = {}
HAND = {}
LINES = {}
RULES = None


def load_hand(node):
    for name in (node + "_hand1", node + "_hand2", node + "_hand3", node + "_hand4"):
        try:
            module = __import__(name)
        except ImportError:
            continue
        HAND.update(module.HAND)
        LINES.update(getattr(module, "LINES", {}))


def with_maths(source, latex):
    """A step's text then its maths line, when the text itself shows no working."""
    if not latex or "=" in source or re.fullmatch(r"\s*\\boxed\{.*\}\s*", latex):
        return None
    maths = RULES.from_latex(latex)
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt:
        return None
    for i in range(len(st) - len(mt) + 1):
        if st[i:i + len(mt)] == mt:
            return None
    text, spoken = RULES.say(source), RULES.say(maths)
    if not text or not spoken:
        return None
    if text[-1] not in ".?!:":
        text += "."
    if text[-1] == ":":
        text = text[:-1] + "."
    if spoken[-1] not in ".?!":
        spoken += "."
    return text + " " + spoken[0].upper() + spoken[1:]


def narrate_string(source, where, hand=None, also=None, latex=""):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex)))
    tries.append(("rule", RULES.say(source)))
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
    failures.append("%s: no rule gives a passing line for: %s\n        rule said: %s" % (where, source, RULES.say(source)))
    return RULES.say(source)


def pick(hand, key, i):
    items = hand.get(key) or []
    if isinstance(items, dict):
        return items.get(i)
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
    brief = "--brief" in sys.argv
    print("=" * 20, n, qid)

    def pair(where, a, b, extra=""):
        if not a.strip():
            return
        k = kinds.get(where, "")[:1]
        tag = where.split(".", 1)[1].replace("options", "o").replace("hints", "h").replace("steps", "s")
        if a.strip() == b:
            if not brief or tag == "q":
                print(" %s %s= %s%s" % (tag, k, b, extra))
        elif "--spoken" in sys.argv:
            print(" %s %s: %s" % (tag, k, b))
        else:
            print(" %s %s\n   P: %s%s\n   S: %s" % (tag, k, a.replace("\n", " // "), extra, b))

    pair(qid + ".q", src["q"], entry["q"])
    for key in ("options", "hints", "steps"):
        for i, a in enumerate(src[key]):
            extra = ""
            if key == "steps" and i < len(own) and own[i].get("latex"):
                extra = "   {LATEX: %s}" % own[i]["latex"]
            pair("%s.%s[%d]" % (qid, key, i), a, entry[key][i], extra)


def run(node, rules):
    global RULES
    RULES = rules
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
        print(" ".join(q["id"] for q in questions))
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        only = None
        if "--kind" in sys.argv:
            only = sys.argv[sys.argv.index("--kind") + 1]
        for n, q in enumerate(questions[a:b], a):
            if only and not q["id"].startswith(only):
                continue
            show(q, part[q["id"]], n)
    for p in failures[:int(os.environ.get("MAXFAIL", "80"))]:
        print("  FAIL " + p)


if __name__ == "__main__":
    import gr4_puzzles_rules
    run("gr4_puzzles", gr4_puzzles_rules)
