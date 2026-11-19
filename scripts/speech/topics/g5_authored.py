"""Narration for the newly added Grade 5 questions (ids starting G5A_).

    python -X utf8 scripts/speech/topics/g5_authored.py

Writes data/bank-import/g5/speech-new.json: { "<question id>": entry }.
Check with: python -X utf8 scripts/speech/check_new.py data/bank-import/g5/speech-new.json

Each line is made by the rules in say(); where a rule does not give a line worth hearing,
the line is written by hand in the g5_authored_hand*.py tables (HAND[qid][field]).
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import common  # noqa: E402

OUT = os.path.join(common.ROOT, "data", "bank-import", "g5", "speech-new.json")


def questions():
    return [q for q in common.bank.load_bank(5) if q["id"].startswith("G5A_")]


import g5_authored_rules as rules  # noqa: E402


def say(text, q=None, option=False):
    """Rule-based narration of one printed string."""
    ratio = bool(q) and re.search(r"\bratio", q.get("subTopic", "").lower()) is not None
    return rules.say(text, ratio=ratio, option=option)


def say_step(q, i, text):
    """A step: its text, followed by its maths line when the text does not already give the result."""
    spoken = say(text, q)
    own = q.get("stepByStep") or []
    latex = own[i].get("latex") if i < len(own) else None
    if not latex or not spoken:
        return spoken
    plain = rules.latex_to_plain(latex)
    if plain is None:
        return spoken
    maths = say(plain, q)
    have = common.number_tokens(text)
    want = common.number_tokens(plain)
    if not want or want[-1] in have:
        return spoken
    maths = maths[0].upper() + maths[1:]
    if not maths.endswith("."):
        maths += "."
    if spoken[-1] not in ".:?!":
        spoken += "."
    return spoken + " " + maths


def load_hand():
    hand = {}
    for name in sorted(os.listdir(HERE)):
        if name.startswith("g5_authored_hand") and name.endswith(".py"):
            mod = __import__(name[:-3])
            for qid, fields in mod.HAND.items():
                hand.setdefault(qid, {}).update(fields)
    return hand


_HAND = None


def narrate(q):
    global _HAND
    if _HAND is None:
        _HAND = load_hand()
    src = common.source_strings(q)
    h = _HAND.get(q["id"], {})
    entry = {
        "q": h.get("q") or say(src["q"], q),
        "options": [say(s, q, option=True) for s in src["options"]],
        "hints": [say(s, q) for s in src["hints"]],
        "steps": [say_step(q, i, s) for i, s in enumerate(src["steps"])],
    }
    # Hand-written lines: "o" / "h" / "s" are either a full list, or {index: line}.
    for key, field in (("o", "options"), ("h", "hints"), ("s", "steps")):
        got = h.get(key)
        if isinstance(got, list):
            if len(got) != len(entry[field]):
                raise SystemExit("%s.%s: %d lines written, %d needed" % (q["id"], key, len(got), len(entry[field])))
            entry[field] = [g if g is not None else e for g, e in zip(got, entry[field])]
        elif isinstance(got, dict):
            for i, line in got.items():
                entry[field][i] = line
    return entry


def main():
    out = {}
    for q in questions():
        out[q["id"]] = narrate(q)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s (%d questions)" % (os.path.relpath(OUT, common.ROOT), len(out)))


if __name__ == "__main__":
    main()
