"""Narration for the geometry topic (angles, triangles, perimeter and area, directions, clock angles).

    python -X utf8 scripts/speech/topics/geometry.py

Writes data/question-speech/parts/geometry.json.

Three layers, most specific first:
  1. HAND     whole entries written by hand, keyed by question id (past papers and worksheets).
  2. LINES    single strings written by hand, keyed by the exact printed text.
  3. say()    rules for the regular wording of the generated families.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from common import PARTS, load_grade5, number_tokens, source_strings, topic_of  # noqa: E402
from geometry_hand1 import HAND as HAND1  # noqa: E402
from geometry_hand2 import HAND as HAND2  # noqa: E402
from geometry_hand3 import HAND as HAND3  # noqa: E402
from geometry_lines import LINES  # noqa: E402
from geometry_imported_rules import IMPORTED_PREFIXES, maths_line, say_imported  # noqa: E402
from geometry_imported_hand1 import LINES as IMP_LINES1, SLOTS as IMP_SLOTS1  # noqa: E402

SLUG = "geometry"
IMP_SLOTS = {}
IMP_LINES = {}
for slots, lines in ((IMP_SLOTS1, IMP_LINES1),):
    IMP_SLOTS.update(slots)
    IMP_LINES.update(lines)
HAND = {}
for part in (HAND1, HAND2, HAND3):
    HAND.update(part)


def _unit(word):
    """A unit after a number: singular after exactly 1, plural otherwise."""
    def sub(m):
        return "%s %s" % (m.group(1), word[:-1] if m.group(1) == "1" else word)
    return sub


def say(text, sentence=True):
    """Rules for the generated families. Printed text in, speakable words out."""
    s = (text or "").strip()
    if not s:
        return ""
    # A line of working that starts with the equals sign.
    chained = s.startswith("=")
    s = re.sub(r"^=\s*", "That equals ", s)
    # Units. The raised 2 after a unit means "square"; anywhere else it means "squared".
    num = r"(\d[\d,]*(?:\.\d+)?)"
    s = re.sub(num + r"\s*(?:sq\.?\s*cm|cm²)(?![a-z])", _unit("square centimetres"), s)
    s = re.sub(num + r"\s*(?:sq\.?\s*m|m²)(?![a-z])", _unit("square metres"), s)
    s = re.sub(num + r"\s*cm\b", _unit("centimetres"), s)
    s = s.replace("²", " squared")
    # Degrees, after a number or a letter.
    s = re.sub(r"\b1°", "1 degree", s)
    s = re.sub(r"([0-9a-z])\s*°", r"\1 degrees", s)
    # Half of a product reads better than "half times".
    s = re.sub(r"(?:½|\bhalf)\s*×\s*", "half of ", s)
    s = s.replace("½", "half")
    s = s.replace("π", " pi ")
    # Algebra: 7x is "7 x". (Not "3s", as in "count up in 3s".)
    s = re.sub(r"(\d)([xyz])\b", r"\1 \2", s)
    # A product inside a longer sum gets a breath after it: "15 × 10 + 15 × 7", "2 × 7 + 15".
    s = re.sub(r"(\d\s*×\s*\d+(?:\.\d+)?)\s*([+−])", r"\1, \2", s)
    # ... and another before the result: "2 × 7, + 15 = 29" is "2 times 7, plus 15, equals 29".
    s = re.sub(r"(, [+−]\s*\d+(?:\.\d+)?)\s*=", r"\1, =", s)
    # A worked example is announced, then read as its own sentences.
    s = re.sub(r"^(Try another one): ([a-z])", lambda m: "%s. %s" % (m.group(1), m.group(2).upper()), s)
    # Signed numbers: "move −8", "becomes +8", an option "-1".
    s = re.sub(r"(^|(?<=[a-z] ))[−-](\d)", r"\1minus \2", s)
    s = re.sub(r"(?<=[a-z] )\+(\d)", r"plus \1", s)
    # Brackets around a sum being multiplied: "2 × (25 + 5)" is "2 times, 25 plus 5,".
    s = re.sub(r"×\s*\(([^()]*)\)", r"times, \1,", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    # A chain of equals signs: the first is "equals", the rest are ", which is".
    # A new sentence or clause (after . ? ! : or a comma) starts a new chain.
    first = [not chained]

    def eq(m):
        if m.group(1):
            first[0] = True
            return m.group(1)
        if first[0]:
            first[0] = False
            return " equals "
        return ", which is "
    s = re.sub(r"([.?!:,]\s)|\s*=\s*", eq, s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ")
    s = re.sub(r"\s*[−–]\s*", " minus ", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",([.,?!:;])", r"\1", s)
    if sentence and s[-1] not in ".?!:":
        s += "."
    return s


def say_maths_line(latex):
    """The maths line of a 'Solve' step, e.g. '7x = 6 + 8 = 14' or 'x = \\frac{14}{7} = \\boxed{2}'."""
    s = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"\1 over \2", latex)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)
    if "\\" in s:
        return None
    s = re.sub(r"(\d)\s*-\s*(\d)", r"\1 − \2", s)
    return say(s)


def _is_subsequence(small, big):
    it = iter(big)
    return all(x in it for x in small)


def narrate_imported(q, counts, used):
    """The imported one-off questions: hand-written slots and lines first, then say_imported.

    A step's maths line is read after its text when it adds working the text does not already say.
    """
    src = source_strings(q)
    own = q.get("stepByStep") or []

    def line(text, slot, sentence=True, latex=None):
        if not text.strip():
            return ""
        key = "%s:%s" % (q["id"], slot)
        if key in IMP_SLOTS:
            counts["imp_hand"] += 1
            used.add(key)
            return IMP_SLOTS[key]
        if text in IMP_LINES:
            counts["imp_hand"] += 1
            used.add(text)
            return IMP_LINES[text]
        counts["imp_rule"] += 1
        spoken = say_imported(text, sentence)
        plain = maths_line(latex) if latex else None
        if plain and re.search(r"[=×÷+−<>≠≈→]", plain):
            extra = number_tokens(plain)
            told = number_tokens(text)
            repeat = _is_subsequence(extra, told) if extra else "=" in text
            # A text that ends with a colon is waiting for its maths line, repeat or not.
            if not repeat or text.rstrip().endswith(":"):
                both = "%s %s" % (spoken, say_imported(plain, maths=True))
                allowed = number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)))
                if len(both) <= 700 and number_tokens(both) == allowed:
                    spoken = both
        return spoken

    steps = []
    for i, t in enumerate(src["steps"]):
        steps.append(line(t, "s%d" % i, latex=own[i].get("latex") if i < len(own) else None))
    return {
        "q": line(src["q"], "q"),
        "options": [line(t, "o%d" % i, sentence=False) for i, t in enumerate(src["options"])],
        "hints": [line(t, "h%d" % i) for i, t in enumerate(src["hints"])],
        "steps": steps,
    }


def narrate(q, counts):
    src = source_strings(q)
    hand = HAND.get(q["id"])
    if hand is not None:
        counts["hand"] += sum(1 for t in [hand["q"]] + hand["options"] + hand["hints"] + hand["steps"] if t)
        return hand
    own = q.get("stepByStep") or []
    solve = src["q"].startswith("Solve:")

    def line(text, sentence=True, latex=None):
        if not text.strip():
            return ""
        if text in LINES:
            counts["hand"] += 1
            return LINES[text]
        counts["rule"] += 1
        spoken = say(text, sentence)
        if latex:
            maths = say_maths_line(latex)
            if maths:
                spoken = "%s %s" % (spoken, maths)
        return spoken

    # A step's maths line is read only when the step text does not already state the working.
    steps = []
    for i, t in enumerate(src["steps"]):
        latex = own[i].get("latex") if (solve and i < len(own) and "=" not in t) else None
        steps.append(line(t, latex=latex))
    return {
        "q": line(src["q"]),
        "options": [line(t, sentence=False) for t in src["options"]],
        "hints": [line(t) for t in src["hints"]],
        "steps": steps,
    }


def main():
    counts = {"hand": 0, "rule": 0, "imp_hand": 0, "imp_rule": 0}
    questions = sorted((q for q in load_grade5() if topic_of(q) == SLUG), key=lambda q: q["id"])
    unknown = sorted(set(HAND) - {q["id"] for q in questions})
    if unknown:
        sys.exit("hand entries for ids not in this topic: %s" % ", ".join(unknown))
    used = set()
    part = {}
    imported = 0
    for q in questions:
        if q["id"].startswith(IMPORTED_PREFIXES):
            imported += 1
            part[q["id"]] = narrate_imported(q, counts, used)
        else:
            part[q["id"]] = narrate(q, counts)
    unused = sorted((set(IMP_SLOTS) | set(IMP_LINES)) - used)
    if unused:
        sys.exit("imported hand entries that match nothing:\n  %s" % "\n  ".join(u[:120] for u in unused))
    os.makedirs(PARTS, exist_ok=True)
    path = os.path.join(PARTS, SLUG + ".json")
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions: %d lines by hand, %d by rule" % (len(part), counts["hand"], counts["rule"]))
    print("of which %d imported questions: %d lines by hand, %d by rule" % (imported, counts["imp_hand"], counts["imp_rule"]))


if __name__ == "__main__":
    main()
