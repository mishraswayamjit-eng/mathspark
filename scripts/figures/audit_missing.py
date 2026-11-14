"""Find Grade 5 questions whose text points at a picture that is not there.

    python -X utf8 scripts/figures/audit_missing.py

Scans every Grade 5 question (all sources) for wording that refers to a figure,
diagram, picture, graph, table, grid, number line, something "shown", "given
below", "adjoining", "shaded" and so on, and writes
data/question-figures/missing-figure-audit.json: a list of

    { id, source, subTopic, questionText, reason, verdict }

verdict is "needs figure" when the question cannot be answered as written, and
"fine" when the phrase is harmless (the data follows in the text or in the
answer choices, or the word is used in another sense).

The plain phrase "which of the following" is not treated as a reference to a
figure and is not listed: it always points at the answer choices.
"""
import collections
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
OUT = os.path.join(ROOT, "data", "question-figures", "missing-figure-audit.json")

# Words that can point at something drawn or laid out on the page.
CUE = re.compile(
    r"\b(figures?|diagrams?|pictures?|pictographs?|graphs?|charts?|tables?|images?|sketch(?:es)?|maps?|grids?|"
    r"number line|venn|tally|shown|drawn|marked|labell?ed|adjoining|adjacent|shaded|unshaded|"
    r"given below|as follows|below|above|the given|following (?:figure|diagram|picture|graph|chart|table|pattern|grid|shape|data)|"
    r"point [A-Z]|this (?:figure|shape|diagram|picture|pattern))\b",
    re.I)

DRAWN_THING = r"(?:figures?|diagrams?|pictures?|pictographs?|graphs?|charts?|tables?|images?|grids?|maps?|shapes?)"
# "in the figure", "of the given diagram", "from the adjoining table"...
IN_THE_FIGURE = re.compile(
    r"\b(?:in|of|from|on|using|see|study|observe|look at)\s+(?:the|this|a)\s+(?:given\s+|adjoining\s+|adjacent\s+|following\s+|above\s+|below\s+)?%s\b" % DRAWN_THING, re.I)
FIGURE_SHOWN = re.compile(r"\b%s\s+(?:given\s+)?(?:shown|below|above|drawn)\b|\b(?:shown|given|drawn)\s+(?:in|below|above)\b[^.?]*\b%s\b" % (DRAWN_THING, DRAWN_THING), re.I)
SHADING = re.compile(r"\b(?:un)?shaded\b", re.I)
NUMBER = re.compile(r"\d")
# "this figure has decreased by 90%": figure meaning a number.
FIGURE_AS_NUMBER = re.compile(r"\b(?:this|that|the) figure (?:has|had|is|was|will|rose|fell|increased|decreased)\b", re.I)
TIMES_TABLE = re.compile(r"\b(?:multiplication|times) tables?\b|\btable of \d", re.I)
BELOW_A_NUMBER = re.compile(r"\b(?:below|above)\s+\d", re.I)
# Data written out after the phrase: "the given series 13, 16, 19", "given equation: 12 − 7 × 5".
INLINE_DATA = re.compile(r"\d[^.?]*[,;×÷+−=/-][^.?]*\d|\n|:\s*\S")
POINT = re.compile(r"\bpoint ([A-Z])\b")


def point_is_placed(text, letter):
    """True when the text itself says where the lettered point is."""
    return bool(re.search(r"\b(?:point )?%s (?:is|lies|is marked|is placed)?\s*(?:at|on)\s+[\d(]" % letter, text)
                or re.search(r"\b%s\s*[=(]\s*[\d(]" % letter, text))


def judge(q):
    """(reason, verdict) for a question that mentions a figure-like thing, or None if it mentions none."""
    text = q.get("questionText", "")
    cues = sorted({m.group(1).lower() for m in CUE.finditer(text)})
    if not cues:
        return None
    options = " ".join(o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", []))
    listed = "mentions: " + ", ".join(cues)

    # 1. Shading can only be seen.
    if SHADING.search(text):
        described = re.search(r"\d+\s+(?:of|out of)\s+(?:the\s+)?\d+|\d+\s+(?:parts?|squares?|pieces?|sections?)\b", text)
        if not described:
            return (listed + "; asks about shaded or unshaded parts but the text never says how many parts there are or how many are shaded", "needs figure")
        return (listed + "; the shaded parts are counted out in words", "fine")

    # 2. A lettered point whose position is never stated.
    for m in POINT.finditer(text):
        letter = m.group(1)
        asked = re.search(r"\bpoint %s\b[^.?]*\?" % letter, text) or re.search(r"\b(?:what|which|where|find)\b[^.?]*\bpoint %s\b" % letter, text, re.I)
        if asked and not point_is_placed(text, letter):
            return (listed + "; asks about point %s but the text never says where point %s is" % (letter, letter), "needs figure")

    # 3. "in the figure", "the table below", "the graph shown".
    if (IN_THE_FIGURE.search(text) or FIGURE_SHOWN.search(text)) and not FIGURE_AS_NUMBER.search(text) and not TIMES_TABLE.search(text):
        if INLINE_DATA.search(text) and len(re.findall(r"\d+", text)) >= 4:
            return (listed + "; the figure is referred to, but its data is written out in the text", "fine")
        return (listed + "; refers to a figure, table or graph and the text does not carry its data", "needs figure")

    # 4. Something is "shown", "drawn" or "marked" with nothing in the text to stand in for it.
    if re.search(r"\b(?:shown|drawn|marked|labell?ed|adjoining)\b", text, re.I):
        if NUMBER.search(text) and re.search(r"\(|:|\bis at\b|\bare at\b|×", text):
            return (listed + "; what is shown is also described in the text", "fine")
        return (listed + "; something is shown or marked, and the text does not describe it", "needs figure")

    # Harmless uses, each with its own reason.
    if FIGURE_AS_NUMBER.search(text):
        return (listed + "; 'figure' here means a number, not a drawing", "fine")
    if TIMES_TABLE.search(text):
        return (listed + "; a multiplication table, not a drawn table", "fine")
    if BELOW_A_NUMBER.search(text):
        return (listed + "; 'below' or 'above' compares with a number", "fine")
    if "number line" in cues or any(c.startswith("point ") for c in cues):
        return (listed + "; the positions on the line are stated in the text", "fine")
    if re.search(r"\bgrids?\b", text, re.I) and NUMBER.search(text):
        return (listed + "; the grid is described by its size", "fine")
    if INLINE_DATA.search(text):
        return (listed + "; the thing referred to is written out in the question text", "fine")
    if NUMBER.search(options) or options.strip():
        return (listed + "; the phrase points at the answer choices, which hold the data", "fine")
    return (listed + "; nothing in the text or the choices carries what is referred to", "needs figure")


def main():
    with io.open(SEED, encoding="utf-8") as f:
        questions = [q for q in json.load(f)["questions"] if q.get("topicId") == "grade5"]

    rows = []
    for q in questions:
        result = judge(q)
        if result is None:
            continue
        reason, verdict = result
        rows.append({"id": q["id"], "source": q.get("source", ""), "subTopic": q.get("subTopic", ""),
                     "questionText": q.get("questionText", ""), "reason": reason, "verdict": verdict})
    rows.sort(key=lambda r: (r["verdict"] != "needs figure", r["id"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")

    counts = collections.Counter(r["verdict"] for r in rows)
    print("scanned %d Grade 5 questions; %d mention a figure-like thing" % (len(questions), len(rows)))
    print("  needs figure: %d" % counts["needs figure"])
    print("  fine:         %d" % counts["fine"])
    for r in rows:
        print("\n[%s] %s (%s)\n  %s\n  -> %s" % (r["verdict"], r["id"], r["source"], r["questionText"].replace("\n", " / ")[:260], r["reason"]))


if __name__ == "__main__":
    main()
