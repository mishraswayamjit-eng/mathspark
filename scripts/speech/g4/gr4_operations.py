"""Write data/question-speech/parts-g4/gr4_operations.json.

    python -X utf8 scripts/speech/g4/gr4_operations.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_operations.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_operations.py --ids         # also list the question ids
    python -X utf8 scripts/speech/g4/gr4_operations.py --show 0 30 --brief   # leave out lines spoken exactly as printed

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_operations_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the arithmetic rules (gr4_operations_rules.say), with the step's maths line where it adds working;
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
import gr4_operations_rules as rules  # noqa: E402

NODE = "gr4_operations"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")

HAND = {}
LINES = {}
for name in ("gr4_operations_hand1", "gr4_operations_hand2", "gr4_operations_hand3", "gr4_operations_hand4"):
    try:
        module = __import__(name)
    except ImportError:
        continue
    HAND.update(module.HAND)
    LINES.update(getattr(module, "LINES", {}))

stats = {"hand": 0, "rule": 0, "base": 0, "failed": 0}
failures = []
kinds = {}


def with_maths(source, latex, box=None):
    """A step's text followed by its maths line, when the maths line adds working the text does not say."""
    if not latex:
        return None
    mt, st = common.number_tokens(rules.from_latex(latex)), common.number_tokens(source)
    if not mt or any(st[k:k + len(mt)] == mt for k in range(len(st) - len(mt) + 1)):
        return None             # the text already says this sum
    text = rules.say(source, "text", box)
    spoken = rules.say_maths(latex)
    if not text or not spoken:
        return None
    if spoken[-1] not in ".?!":
        spoken += "."
    # "So 82 − 8 = 74." followed by the sum that shows it: join the two with "because".
    last = re.split(r"(?<=[.?!])\s+", text)[-1]
    if last.startswith("So ") and text.endswith("."):
        return text[:-1] + ", because " + spoken
    if text[-1] not in ".?!:":
        text += "."
    return text + " " + spoken[0].upper() + spoken[1:]


def narrate_string(source, where, hand=None, also=None, latex="", kind="text", box=None):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex, box)))
    tries.append(("rule", rules.say(source, kind, box)))
    tries.append(("base", common.speak(source)))
    for how, spoken in tries:
        if not spoken:
            continue
        if kind == "line" and how != "hand" and spoken[-1] not in ".?!:":
            spoken += "."       # a hint or step is a sentence: let the voice close it
        problems = check_string(spoken, source, where, also)
        if not problems:
            stats[how] += 1
            kinds[where] = how
            return spoken
        if how == "hand":
            failures.extend(problems)
    stats["failed"] += 1
    kinds[where] = "FAILED"
    failures.append("%s: no rule gives a passing line for: %s\n        rule said: %s" % (where, source, rules.say(source, kind)))
    return rules.say(source, kind)


def pick(hand, key, i):
    items = hand.get(key) or []
    return items[i] if i < len(items) else None


def narrate(q):
    src = common.source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []
    qid = q["id"]
    # One word for the box in a sum throughout a question: "box" if its print talks of boxes.
    everything = " ".join([src["q"]] + src["hints"] + src["steps"])
    box = "box" if re.search(r"\bbox(?:es)?\b", everything) and re.search(r"□", everything) else None
    steps = []
    for i, text in enumerate(src["steps"]):
        latex = own[i].get("latex", "") if i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        steps.append(narrate_string(text, "%s.steps[%d]" % (qid, i), pick(hand, "steps", i), also, latex, "line", box))
    return {
        "q": narrate_string(src["q"], qid + ".q", hand.get("q"), kind="line", box=box),
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), pick(hand, "options", i), kind="option") for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), pick(hand, "hints", i), kind="line", box=box) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def show(q, entry, n):
    src = common.source_strings(q)
    own = q.get("stepByStep") or []
    qid = q["id"]
    brief = "--brief" in sys.argv
    print("=" * 20, n, qid, "|", q.get("subTopic", ""))

    def pair(where, a, b, extra=""):
        if not a.strip():
            return
        k = kinds.get(where, "")
        tag = where.split(".", 1)[1] if not where.endswith(".q") else "q"
        if a.strip() == b:
            if brief and tag != "q" and not extra:
                return
            print(" %s [%s] SAME  %s%s" % (tag, k, b, extra))
        else:
            print(" %s [%s]\n   P: %s%s\n   S: %s" % (tag, k, a.replace("\n", " // "), extra, b))

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
    printed = set()
    for q in questions:
        src = common.source_strings(q)
        printed.update(t.strip() for t in [src["q"]] + src["options"] + src["hints"] + src["steps"])
    unused = sorted(set(LINES) - printed)
    if unused:
        print("LINES entries no longer printed anywhere:", unused)
    unknown = sorted(set(HAND) - set(part))
    if unknown:
        print("hand entries for unknown ids:", unknown)
    if "--ids" in sys.argv:
        for i, q in enumerate(questions):
            print(i, q["id"], "|", q.get("subTopic", ""), "|", q.get("questionText", "")[:100].replace("\n", " // "))
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            show(q, part[q["id"]], n)
    if "--listed" in sys.argv:   # the questions whose help was rewritten (renarrate.json): print beside speech
        with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
            listed = json.load(f).get(NODE, [])
        mine = [q for q in questions if q["id"] in set(listed)]
        print("listed: %d, in topic now: %d" % (len(listed), len(mine)))
        print("listed but not in topic:", sorted(set(listed) - set(part)))
        print("hand entries with hints or steps for listed ids:",
              sorted(i for i in listed if i in HAND and (HAND[i].get("hints") or HAND[i].get("steps"))))
        count = {"hand": 0, "rule": 0, "base": 0, "FAILED": 0}
        for q in mine:
            src = common.source_strings(q)
            for key in ("hints", "steps"):
                for j, t in enumerate(src[key]):
                    if t.strip():
                        count[kinds.get("%s.%s[%d]" % (q["id"], key, j), "FAILED")] += 1
        print("hint and step lines of listed ids:", count)
        i = sys.argv.index("--listed")
        if len(sys.argv) > i + 2:
            a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
            for n, q in enumerate(mine[a:b], a):
                src = common.source_strings(q)
                own = q.get("stepByStep") or []
                e = part[q["id"]]
                print("== %d %s" % (n, q["id"]))
                print(" Q: " + src["q"].replace("\n", " // "))
                for key in ("hints", "steps"):
                    for j, t in enumerate(src[key]):
                        latex = own[j].get("latex", "") if key == "steps" and j < len(own) else ""
                        k = kinds.get("%s.%s[%d]" % (q["id"], key, j), "")
                        print(" %s%d P: %s%s" % (key[0], j, t.replace("\n", " // "), "   {%s}" % latex if latex else ""))
                        print("  [%s] S: %s" % (k[:1], e[key][j]))
        return
    if "--grep" in sys.argv:     # every spoken line matching a pattern, once each
        pattern = re.compile(sys.argv[sys.argv.index("--grep") + 1])
        seen = set()
        for q in questions:
            e = part[q["id"]]
            for where, line in [("q", e["q"])] + [(k + str(i), t) for k in ("options", "hints", "steps") for i, t in enumerate(e[k])]:
                if line and line not in seen and pattern.search(line):
                    seen.add(line)
                    print("%s.%s: %s" % (q["id"], where, line))
        return
    if "--src" in sys.argv:      # the printed source only, compact
        i = sys.argv.index("--src")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            src = common.source_strings(q)
            own = q.get("stepByStep") or []
            print("== %d %s" % (n, q["id"]))
            print("Q: " + src["q"].replace("\n", " // "))
            print("O: " + "  ¦  ".join(src["options"]))
            for j, h in enumerate(src["hints"]):
                print("H%d: %s" % (j, h.replace("\n", " // ")))
            for j, s in enumerate(src["steps"]):
                latex = own[j].get("latex", "") if j < len(own) else ""
                print("S%d: %s%s" % (j, s.replace("\n", " // "), "   {%s}" % latex if latex else ""))
        return
    for p in failures[:int(os.environ.get("MAXFAIL", "80"))]:
        print("  FAIL " + p)
    if len(failures) > 80:
        print("  ... %d failures in all" % len(failures))


if __name__ == "__main__":
    main()
