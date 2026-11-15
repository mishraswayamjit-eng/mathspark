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

from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
import squares_patterns_rules as rules  # noqa: E402

SLUG = "squares-patterns"

HAND = {}
for name in ("squares_patterns_hand1", "squares_patterns_hand2", "squares_patterns_hand3", "squares_patterns_hand4"):
    try:
        HAND.update(__import__(name).HAND)
    except ImportError:
        pass

stats = {"hand": 0, "template": 0, "fallback": 0}


def by_rule(text, latex=""):
    if not text.strip():
        return ""
    out = rules.equation_step(text, latex) if latex else None
    if out is None:
        out = rules.by_template(text)
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


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions: %d strings by hand, %d by template, %d by fallback"
          % (len(part), stats["hand"], stats["template"], stats["fallback"]))


if __name__ == "__main__":
    main()
