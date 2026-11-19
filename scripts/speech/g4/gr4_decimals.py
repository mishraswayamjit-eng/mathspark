"""Write data/question-speech/parts-g4/gr4_decimals.json.

    python -X utf8 scripts/speech/g4/gr4_decimals.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_decimals.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_decimals.py --show 0 30 --diff   # only lines whose speech differs from print

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_decimals_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the rules (gr4_decimals_rules: family, then say), with a step's maths line spoken after its text
     when the maths line adds working that the text does not say;
  3. the shared base converter (common.speak), as a last resort.

A HAND entry is sparse: {"q": ..., "o0".."o3": ..., "h0".."h2": ..., "s0"..: ...}; lines left out go to the rules.
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
import gr4_decimals_rules as rules  # noqa: E402

NODE = "gr4_decimals"
OUT = ""
HAND = {}
LINES = {}


def configure(node, rules_module, hand_modules):
    """Point this builder at a topic. gr4_units.py (same writer) reuses it with its own rules and hand lines."""
    global NODE, OUT, rules
    NODE = node
    OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", node + ".json")
    rules = rules_module
    HAND.clear()
    LINES.clear()
    for name in hand_modules:
        try:
            module = __import__(name)
        except ImportError:
            continue
        for qid, lines in module.HAND.items():
            HAND.setdefault(qid, {}).update(lines)
        LINES.update(getattr(module, "LINES", {}))


configure("gr4_decimals", rules, ("gr4_decimals_hand1", "gr4_decimals_hand2", "gr4_decimals_hand3"))

stats = {"hand": 0, "rule": 0, "same": 0, "base": 0, "failed": 0}
failures = []
kinds = {}


def _contains(big, small):
    """True when every number of `small` is already said, in order, within `big`."""
    it = iter(big)
    return all(x in it for x in small)


def _end(spoken):
    """A sentence ends with a full stop (options are left as they are)."""
    if spoken and spoken[-1] not in ".?!":
        spoken = spoken.rstrip(":;,") + "."
    return spoken


def with_maths(source, latex):
    """A step's text followed by its maths line, when the maths line adds working the text does not say."""
    if not latex or re.fullmatch(r"\s*\\boxed\{.*\}\s*", latex):
        return None
    if re.search(r"\\(?:overline|underline|underset|overset|begin|phantom)", latex):
        return None          # layout (long division, columns, labels): the text carries it
    maths = rules.from_latex(latex)
    mt, st = common.number_tokens(maths), common.number_tokens(source)
    if not mt or _contains(st, mt):
        return None
    if _contains(st, [t for t in mt if t != "1"]) and re.search(r"\b1 ?\\text", latex):
        return None          # '1 m = 100 cm' under a text that already says 'one metre is 100 centimetres'
    text = rules.family(source) or rules.say(source)
    spoken = rules.say(maths)
    if not text or not spoken:
        return None
    if text[-1] not in ".?!":
        text = text.rstrip(":") + "."
    if spoken[-1] not in ".?!":
        spoken += "."
    return text + " " + spoken


def narrate_string(source, where, hand=None, also=None, latex="", sentence=True):
    if not source.strip():
        return ""
    tries = []
    hand = hand or LINES.get(source.strip())
    if hand:
        tries.append(("hand", hand))
    if latex:
        tries.append(("rule", with_maths(source, latex)))
    tries.append(("rule", rules.family(source)))
    tries.append(("rule", rules.say(source)))
    tries.append(("base", common.speak(source)))
    for kind, spoken in tries:
        if not spoken:
            continue
        if sentence and kind != "hand":
            spoken = _end(spoken)
        problems = check_string(spoken, source, where, also)
        if not problems:
            if kind == "rule" and spoken.rstrip(".") == source.strip().rstrip(".:"):
                kind = "same"
            stats[kind] += 1
            kinds[where] = kind
            return spoken
        if kind == "hand":
            failures.extend(problems)
    stats["failed"] += 1
    kinds[where] = "FAILED"
    failures.append("%s: no rule gives a passing line for: %s" % (where, source))
    return rules.say(source)


def narrate(q):
    src = common.source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []
    qid = q["id"]
    steps = []
    for i, text in enumerate(src["steps"]):
        latex = (own[i].get("latex") or "") if i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        steps.append(narrate_string(text, "%s.steps[%d]" % (qid, i), hand.get("s%d" % i), also, latex))
    return {
        "q": narrate_string(src["q"], qid + ".q", hand.get("q")),
        "options": [narrate_string(t, "%s.options[%d]" % (qid, i), hand.get("o%d" % i), sentence=False) for i, t in enumerate(src["options"])],
        "hints": [narrate_string(t, "%s.hints[%d]" % (qid, i), hand.get("h%d" % i)) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def show(q, entry, n, diff):
    src = common.source_strings(q)
    own = q.get("stepByStep") or []
    qid = q["id"]
    print("=" * 20, n, qid)

    def pair(tag, where, a, b, extra=""):
        if not a.strip():
            return
        k = kinds.get(where, "")
        if a.strip() == b:
            if not diff:
                print(" %s [%s] SAME  %s%s" % (tag, k, b, extra))
        else:
            print(" %s [%s] %s%s\n      > %s" % (tag, k, a.replace("\n", " // "), extra, b))

    pair("Q ", qid + ".q", src["q"], entry["q"])
    for i, a in enumerate(src["options"]):
        if "--noopt" in sys.argv and kinds.get("%s.options[%d]" % (qid, i)) != "hand":
            continue
        pair("O%d" % i, "%s.options[%d]" % (qid, i), a, entry["options"][i])
    for i, a in enumerate(src["hints"]):
        pair("H%d" % i, "%s.hints[%d]" % (qid, i), a, entry["hints"][i])
    for i, a in enumerate(src["steps"]):
        lx = (own[i].get("latex") or "") if i < len(own) else ""
        pair("S%d" % i, "%s.steps[%d]" % (qid, i), a, entry["steps"][i], ("   {%s}" % lx) if lx else "")


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
    if "--show" in sys.argv:
        i = sys.argv.index("--show")
        a, b = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        only = None
        if "--renarrate" in sys.argv:     # only the questions whose help was rewritten
            with io.open(os.path.join(common.ROOT, "data", "bank-import", "g4", "renarrate.json"), encoding="utf-8") as f:
                only = set(json.load(f).get(NODE, []))
        for n, q in enumerate(questions[a:b], a):
            if only is None or q["id"] in only:
                show(q, part[q["id"]], n, "--diff" in sys.argv)
    for p in failures[:80]:
        print("  FAIL " + p)


if __name__ == "__main__":
    main()
