"""Write data/question-speech/parts/squares-patterns.json.

    python -X utf8 scripts/speech/topics/squares-patterns.py

Generated families are narrated by template (squares_patterns_rules.py). Past-paper and
worksheet questions are narrated by hand (squares_patterns_hand*.py); any string a hand
entry leaves out falls back to the rules.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

from common import PARTS, load_grade5, number_tokens, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402
import squares_patterns_rules as rules  # noqa: E402
import squares_patterns_imported_rules as irules  # noqa: E402

SLUG = "squares-patterns"

HAND = {}
for name in ("squares_patterns_hand1", "squares_patterns_hand2", "squares_patterns_hand3", "squares_patterns_hand4"):
    try:
        HAND.update(__import__(name).HAND)
    except ImportError:
        pass

stats = {"hand": 0, "template": 0, "fallback": 0, "imported_rule": 0, "imported_hand": 0}


def by_rule(text, latex=""):
    if not text.strip():
        return ""
    out = rules.by_template(text)
    if out is None and latex:
        out = rules.equation_step(text, latex)
    if out is not None:
        stats["template"] += 1
        return out
    stats["fallback"] += 1
    return rules.basic(text)


_CLOSED_LIST = re.compile(r"(?<![\d.,])((?:\d+, ){2,})(\d+)(?=[.!?](?:\s|$)|, which)")


def polish(line):
    """Last touches for the ear, applied to every line. Never changes the numbers said."""
    # "3-digit" can be read as "3 minus digit".
    line = re.sub(r"(\d)-digit", r"\1 digit", line)
    # A finished list of numbers gets "and" before its last item: "11, 13 and 17."
    return _CLOSED_LIST.sub(lambda m: m.group(1)[:-2] + " and " + m.group(2), line)


def narrate(q):
    src = source_strings(q)
    hand = HAND.get(q["id"], {})
    own = q.get("stepByStep") or []

    def one(key, i, text):
        given = hand.get(key)
        if key == "q":
            line = given
        else:
            line = given[i] if given is not None and i < len(given) else None
        if line is not None and text.strip():
            stats["hand"] += 1
            return polish(line)
        latex = own[i].get("latex", "") if key == "steps" and i < len(own) else ""
        return polish(by_rule(text, latex))

    return {
        "q": one("q", 0, src["q"]),
        "options": [one("options", i, t) for i, t in enumerate(src["options"])],
        "hints": [one("hints", i, t) for i, t in enumerate(src["hints"])],
        "steps": [one("steps", i, t) for i, t in enumerate(src["steps"])],
    }


# ── Imported questions (AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_) ───────────
# One-off word problems: narrated by squares_patterns_imported_rules.py, with hand-written
# lines from squares_patterns_imported*.py wherever a rule does not sound right.

IMPORTED = {}
for name in sorted(os.path.splitext(f)[0] for f in os.listdir(HERE)
                   if re.match(r"squares_patterns_imported\d+\.py$", f)):
    IMPORTED.update(__import__(name).HAND)

imported_failures = []


def _given(hand, key, i):
    given = hand.get(key)
    if given is None or key == "q":
        return given
    if isinstance(given, dict):
        return given.get(i)
    return given[i] if i < len(given) else None


def _latex_adds(text, latex):
    """False when the maths line only repeats numbers the step's text has already said."""
    want, have = number_tokens(re.sub(r"\\[a-zA-Z]+", " ", latex)), number_tokens(text)
    if not want:
        return "=" not in text      # a formula in letters; the text has said it if it has its own sum
    if any(have[-k:] == want[:k] for k in range(3, min(len(have), len(want)) + 1)):
        return False        # the text ends with the very sum the maths line starts with
    if "=" in text and have and have[-1] == want[-1] and not text.rstrip().endswith(":"):
        return False        # the text has already worked the sum through to the same result
    return not any(have[k:k + len(want)] == want for k in range(len(have) - len(want) + 1))


def narrate_imported(q):
    src = source_strings(q)
    hand = IMPORTED.get(q["id"], {})
    own = q.get("stepByStep") or []

    def one(key, i, text):
        if not text.strip():
            return ""
        where = "%s.%s[%d]" % (q["id"], key, i)
        latex = own[i].get("latex", "") if key == "steps" and i < len(own) else ""
        also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)) if latex else None
        line = _given(hand, key, i)
        if line is not None:
            stats["imported_hand"] += 1
        else:
            stats["imported_rule"] += 1
            line = polish(irules.say(text))
            spoken_maths = irules.say_latex(latex) if latex else None
            if spoken_maths and spoken_maths.lower().rstrip(".") in line.lower():
                spoken_maths = None     # the text has just said exactly this
            wanted = bool(latex) and (_latex_adds(text, latex) or text.rstrip().endswith(":"))
            if spoken_maths and wanted:
                head = line if line[-1] in ".!?:" else line + "."
                tail = spoken_maths if spoken_maths[-1] in ".!?" else spoken_maths + "."
                both = polish(head + " " + tail)
                if not check_string(both, text, where, also):
                    line = both
                    wanted = False
            if wanted and "--dropped" in sys.argv:
                print("maths line not spoken: %s\n    %s || %s" % (where, text, latex))
            if line.endswith(":"):
                line = line[:-1] + "."      # nothing follows the colon in speech
            elif key != "options" and line[-1].isalnum():
                line += "."                 # a sentence printed without its full stop
        found = check_string(line, text, where, also)
        if found:
            imported_failures.extend(found)
            imported_failures.append("      PRINT  " + text + (" || " + latex if latex else ""))
            imported_failures.append("      SPOKEN " + line)
        return line

    return {
        "q": one("q", 0, src["q"]),
        "options": [one("options", i, t) for i, t in enumerate(src["options"])],
        "hints": [one("hints", i, t) for i, t in enumerate(src["hints"])],
        "steps": [one("steps", i, t) for i, t in enumerate(src["steps"])],
    }


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    path = os.path.join(PARTS, SLUG + ".json")
    # Entries written before the imported questions arrived are kept exactly as they are on disk:
    # some of their source texts have since been edited, and their narration was reviewed as it stands.
    # Pass --rebuild-old to narrate them afresh.
    kept = {}
    if os.path.exists(path) and "--rebuild-old" not in sys.argv:
        with io.open(path, encoding="utf-8") as f:
            kept = {k: v for k, v in json.load(f).items() if not k.startswith(irules.IMPORTED_PREFIXES)}
    part = {}
    held_back = 0
    for q in questions:
        if q["id"] in kept:
            part[q["id"]] = kept[q["id"]]
            continue
        if not q["id"].startswith(irules.IMPORTED_PREFIXES):
            part[q["id"]] = narrate(q)
            continue
        before = len(imported_failures)
        entry = narrate_imported(q)
        if len(imported_failures) == before:
            part[q["id"]] = entry
        else:
            held_back += 1      # keeps the part file valid: an entry is written only once every line passes
    if imported_failures:
        print("%d imported lines do not pass yet (%d questions held back):" % (len(imported_failures) // 3, held_back))
        for line in imported_failures[:int(os.environ.get("SHOW_FAILURES", "90"))]:
            print("  " + line)
    os.makedirs(PARTS, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions: %d earlier entries kept as they were; %d strings by hand, %d by template, %d by fallback"
          % (len(part), len([k for k in part if k in kept]), stats["hand"], stats["template"], stats["fallback"]))
    print("imported questions: %d strings by rule, %d by hand"
          % (stats["imported_rule"], stats["imported_hand"]))


if __name__ == "__main__":
    main()
