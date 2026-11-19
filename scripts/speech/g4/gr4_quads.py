"""Write data/question-speech/parts-g4/gr4_quads.json.

    python -X utf8 scripts/speech/g4/gr4_quads.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_quads.py --list        # also list every question
    python -X utf8 scripts/speech/g4/gr4_quads.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_quads.py --show 0 30 --brief   # leave out lines spoken exactly as printed

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_quads_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the geometry rules (gr4_quads_rules.say), for a step also its text followed by its maths line;
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
import gr4_quads_rules as rules  # noqa: E402

NODE = "gr4_quads"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")

HAND = {}
LINES = {}
for name in ("gr4_quads_hand1", "gr4_quads_hand2", "gr4_quads_hand3", "gr4_quads_hand4"):
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
    it = iter(st)
    if not mt or all(t in it for t in mt):          # the text already says these numbers, in this order
        return None
    text = rules.say(source)
    spoken = rules.say(maths)
    if not text or not spoken:
        return None
    if text[-1] not in ".?!:":
        text += "."
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
        tag = where.split(".", 1)[1]
        if a.strip() == b:
            if "--brief" not in sys.argv:
                print(" %s [%s] SAME %s%s" % (tag, k, json.dumps(b, ensure_ascii=False), extra))
        else:
            print(" %s [%s]\n   P: %s%s\n   S: %s" % (tag, k, json.dumps(a, ensure_ascii=False), extra, json.dumps(b, ensure_ascii=False)))

    pair(qid + ".q", src["q"], entry["q"])
    for key in ("options", "hints", "steps"):
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
    if "--list" in sys.argv:
        for n, q in enumerate(questions):
            print("%3d %-30s %s" % (n, q["id"], q.get("questionText", "").replace("\n", " // ")[:100]))
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        for n, q in enumerate(questions[a:b], a):
            show(q, part[q["id"]], n)
    if "--uniq" in sys.argv:
        # every different printed line once, with how it is spoken; digits masked so families collapse
        i = sys.argv.index("--uniq")
        prefix = sys.argv[i + 1] if len(sys.argv) > i + 1 else ""
        seen = {}
        for q in questions:
            if not q["id"].startswith(prefix):
                continue
            src = common.source_strings(q)
            e = part[q["id"]]
            pairs = [(src["q"], e["q"])] + list(zip(src["options"], e["options"])) + list(zip(src["hints"], e["hints"])) + list(zip(src["steps"], e["steps"]))
            for a, b in pairs:
                if not a.strip() or a.strip() == b:
                    continue
                key = re.sub(r"\d+", "#", a)
                if key not in seen:
                    seen[key] = (a, b, q["id"])
        for a, b, qid in seen.values():
            print("P: %s\nS: %s   [%s]\n" % (json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False), qid))
    # hand lines keyed by a printed line that no longer appears anywhere in the topic
    printed = set()
    for q in questions:
        src = common.source_strings(q)
        printed.update(t.strip() for t in [src["q"]] + src["options"] + src["hints"] + src["steps"])
    for key in LINES:
        if key not in printed:
            print("UNUSED hand line: %s" % json.dumps(key, ensure_ascii=False))
    if "--renarrate" in sys.argv:
        # the hints and steps of the questions whose teaching help was rewritten
        with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
            listed = set(json.load(f).get(NODE, []))
        i = sys.argv.index("--renarrate")
        lo = int(sys.argv[i + 1]) if len(sys.argv) > i + 1 and sys.argv[i + 1].isdigit() else 0
        hi = int(sys.argv[i + 2]) if len(sys.argv) > i + 2 and sys.argv[i + 2].isdigit() else 10 ** 6
        chosen = [q for q in questions if q["id"] in listed]
        print("listed for %s: %d, found in the topic: %d" % (NODE, len(listed), len(chosen)))
        print("hint and step lines of the listed questions:", dict(
            (k, sum(1 for q in chosen for w, v in kinds.items()
                    if w.startswith(q["id"] + ".") and (".hints[" in w or ".steps[" in w) and v == k))
            for k in ("hand", "rule", "base", "FAILED")))
        missing = sorted(listed - set(part))
        if missing:
            print("listed but not in the topic:", missing)
        for n, q in enumerate(chosen[lo:hi], lo):
            src = common.source_strings(q)
            own = q.get("stepByStep") or []
            e = part[q["id"]]
            print("=" * 20, n, q["id"], "| Q:", src["q"].replace("\n", " // ")[:90])
            for key in ("hints", "steps"):
                for j, a in enumerate(src[key]):
                    if not a.strip():
                        continue
                    where = "%s.%s[%d]" % (q["id"], key, j)
                    lx = own[j].get("latex") if key == "steps" and j < len(own) else ""
                    if a.strip() == e[key][j]:
                        print(" %s[%d] SAME %s" % (key[0], j, json.dumps(a, ensure_ascii=False)))
                    else:
                        print(" %s[%d] [%s] P: %s%s\n        S: %s" % (
                            key[0], j, kinds.get(where, ""), json.dumps(a, ensure_ascii=False),
                            ("  {%s}" % lx) if lx else "", json.dumps(e[key][j], ensure_ascii=False)))
    if "--odd" in sys.argv:
        # lines worth a second look: two numbers with nothing between them, or a stray lone letter or mark
        for q in questions:
            e = part[q["id"]]
            for b in [e["q"]] + e["options"] + e["hints"] + e["steps"]:
                if re.search(r"\d \d|\?[^ ]|[a-z]\?[a-z]| ,|\.\.|, which is [^,.]*, which is [^,.]*, which is|'", b):
                    print("ODD %s: %s" % (q["id"], b))
    for p in failures[:int(os.environ.get("MAXFAIL", "80"))]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()
