"""Narration for the topic ratio-word-problems (Grade 5).

    python -X utf8 scripts/speech/topics/ratio-word-problems.py

Writes data/question-speech/parts/ratio-word-problems.json.

Two layers:
  1. Rules for the generated families (ratio sharing, proportion "a : b = c : x", ratio of ages,
     sum and difference of ages), whose wording is regular.
  2. Hand-written lines for every past-paper and worksheet question, in
     ratio_word_problems_hand1.py, _hand2.py and _hand3.py.
Answer choices are short and regular, so they are spoken by rule everywhere.

Ratio convention for this topic: "3 : 5" is always "3 is to 5"; "a : b = c : d" is
"a is to b, as c is to d".
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from common import PARTS, load_grade5, source_strings, speak, topic_of  # noqa: E402

SLUG = "ratio-word-problems"

HAND = {}
for _name in ("ratio_word_problems_hand1", "ratio_word_problems_hand2", "ratio_word_problems_hand3"):
    try:
        HAND.update(__import__(_name).HAND)
    except ImportError:
        pass


# ── Answer choices ───────────────────────────────────────────────────────────

_OPTION_UNITS = {
    "hrs": "hours", "hr": "hours", "kg": "kilograms", "g": "grams", "gm": "grams",
    "km": "kilometres", "ml": "millilitres", "l": "litres",
}


def say_option(text):
    t = text.strip()
    m = re.fullmatch(r"(?:Rs\.?|₹)\s*([\d,]+(?:\.\d+)?)", t)
    if m:
        return m.group(1) + " rupees"
    m = re.fullmatch(r"[-−]\s*(\d+(?:\.\d+)?)", t)
    if m:
        return "minus " + m.group(1)
    m = re.fullmatch(r"([\d,]+(?:\.\d+)?)\s*([A-Za-z]+)\.?", t)
    if m and m.group(2).lower() in _OPTION_UNITS:
        return "%s %s" % (m.group(1), _OPTION_UNITS[m.group(2).lower()])
    return say(t)


# ── General fallback: print to speech ────────────────────────────────────────

def say(text):
    """Rule-based speech for a string no family rule or hand line covers."""
    s = text or ""
    s = s.replace("✓", "").replace("→", ", so ").replace("⇒", ", so ")
    s = re.sub(r"(\d)\s*:\s*(\d+)\s*=\s*(\d+)\s*:\s*([\dA-Za-z]+)", r"\1 is to \2, as \3 is to \4", s)
    s = re.sub(r"(\d)\s*:\s*(?=\d)", r"\1 is to ", s)
    s = re.sub(r"\bgm\b", "grams", s)
    s = re.sub(r"(\d)\s*hrs?\b\.?", r"\1 hours", s)
    s = re.sub(r"(\d)\s*g\b", r"\1 grams", s)
    s = re.sub(r"\bkg\s*/\s*day\b", "kilograms a day", s)
    s = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", s)
    s = s.replace("'part'", "part")
    s = speak(s)
    s = s.replace("(", ", ").replace(")", ", ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*([.?!:;,])", r"\1", s)
    return s.strip(" ,")


# ── Generated families: regular wording, so written once as rules ────────────

N = r"(\d+)"
W = r"([A-Za-z]+)"

FAMILY = [
    # questions
    (r"%s has %s %s and divides them in the ratio %s:%s\. How many (\w+) are in the larger group\?" % (W, N, W, N, N),
     r"\1 has \2 \3, and divides them in the ratio \4 is to \5. How many \6 are in the larger group?"),
    (r"Divide %s in the ratio %s:%s\. What is the smaller share\?" % (N, N, N),
     r"Divide \1 in the ratio \2 is to \3. What is the smaller share?"),
    (r"If %s : %s = %s : x, find x\." % (N, N, N),
     r"If \1 is to \2, as \3 is to x, find x."),
    (r"The ages of %s and %s are in the ratio %s:%s\. If %s is %s years old, how old is %s\?" % (W, W, N, N, W, N, W),
     r"The ages of \1 and \2 are in the ratio \3 is to \4. If \5 is \6 years old, how old is \7?"),
    (r"%s is %s years old and %s is %s years old\. What will be the sum of their ages after %s years\?" % (W, N, W, N, N),
     r"\1 is \2 years old, and \3 is \4 years old. What will be the sum of their ages, after \5 years?"),
    (r"%s is %s years old and %s is %s years old\. What was the difference in their ages %s years ago\?" % (W, N, W, N, N),
     r"\1 is \2 years old, and \3 is \4 years old. What was the difference in their ages, \5 years ago?"),
    # hints
    (r"Sum the ratio parts to find the total number of parts\.", r"Sum the ratio parts, to find the total number of parts."),
    (r"Divide the total by the sum of parts to find one part\.", r"Divide the total by the sum of parts, to find one part."),
    (r"Multiply to find each share\.", r"Multiply, to find each share."),
    (r"If the ratio is %s:%s and %s is %s, find one 'part'\." % (N, N, W, N),
     r"If the ratio is \1 is to \2, and \3 is \4, find one part."),
    (r"One part = %s ÷ %s\." % (N, N), r"One part equals \1 divided by \2."),
    (r"Then %s's age = %s × one part\." % (W, N), r"Then \1's age equals \2 times one part."),
    (r"Add %s years to each person's age\." % N, r"Add \1 years to each person's age."),
    (r"Then add their future ages together\.", r"Then add their future ages together."),
    (r"Both age by %s years, so total increases by %s\." % (N, N), r"Both age by \1 years, so the total increases by \2."),
    (r"Here's a key insight: the age difference between two people never changes\.",
     r"Here's a key insight: the age difference between two people never changes."),
    (r"It doesn't matter if we go forward or backward in time\.", r"It doesn't matter if we go forward, or backward, in time."),
    (r"The difference was, is, and always will be %s years\." % N, r"The difference was, is, and always will be, \1 years."),
    # steps
    (r"Identify the ratio parts and total\.", r"Identify the ratio parts, and the total."),
    (r"Compute the answer: %s" % N, r"Compute the answer. It is \1."),
    (r"Ratio = %s:%s, %s = %s" % (N, N, W, N), r"The ratio is \1 is to \2, and \3 is \4."),
    (r"One part = %s ÷ %s = %s" % (N, N, N), r"One part equals \1 divided by \2, which is \3."),
    (r"%s's age = %s × %s = %s" % (W, N, N, N), r"\1's age equals \2 times \3, which is \4."),
    (r"After %s years: %s = %s, %s = %s" % (N, W, N, W, N), r"After \1 years, \2 is \3, and \4 is \5."),
    (r"Sum = %s \+ %s = %s" % (N, N, N), r"The sum is \1 plus \2, which equals \3."),
    (r"The age difference never changes!", r"The age difference never changes!"),
    (r"Difference = %s − %s = %s" % (N, N, N), r"The difference is \1 minus \2, which equals \3."),
]
FAMILY = [(re.compile(p), r) for p, r in FAMILY]

STATS = {"rule": 0, "hand": 0, "fallback": 0, "option": 0}
FALLBACKS = []


def say_line(text, where):
    """A question, hint or step with no hand-written line: family rule, else the general fallback."""
    if not text.strip():
        return ""
    for pat, rep in FAMILY:
        m = pat.fullmatch(text.strip())
        if m:
            STATS["rule"] += 1
            return m.expand(rep)
    STATS["fallback"] += 1
    FALLBACKS.append(where)
    return say(text)


def narrate(q):
    src = source_strings(q)
    hand = HAND.get(q["id"], {})
    entry = {}

    def pick(key, i, text):
        got = hand.get(key)
        if got is not None:
            line = got if key == "q" else (got[i] if i < len(got) else None)
            if line is not None:
                if text.strip():
                    STATS["hand"] += 1
                return line
        return say_line(text, "%s.%s[%d]" % (q["id"], key, i))

    entry["q"] = pick("q", 0, src["q"])
    if "options" in hand:
        entry["options"] = list(hand["options"])
    else:
        entry["options"] = [say_option(o) for o in src["options"]]
    STATS["option"] += len(entry["options"])
    entry["hints"] = [pick("hints", i, t) for i, t in enumerate(src["hints"])]
    entry["steps"] = [pick("steps", i, t) for i, t in enumerate(src["steps"])]
    return entry


def main():
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    part = {q["id"]: narrate(q) for q in questions}
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions to %s" % (len(part), path))
    print("lines: %(hand)d by hand, %(rule)d by family rule, %(fallback)d by general fallback, %(option)d answer choices by rule" % STATS)
    if FALLBACKS:
        print("general fallback used for: " + ", ".join(FALLBACKS[:40]))


if __name__ == "__main__":
    main()
