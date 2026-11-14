"""Shared helpers for question narration (spoken scripts). Do not edit: every topic builds on this.

    from common import load_grade5, topic_of, effective_steps, speak, number_tokens, TOPICS

See scripts/speech/README.md for the brief.
"""
import io
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
FIGURES = os.path.join(ROOT, "src", "data", "questionFigures", "figures.json")
PARTS = os.path.join(ROOT, "data", "question-speech", "parts")

# The ten Grade 5 topics. Each question belongs to exactly one.
TOPICS = [
    "fractions", "place-value", "arithmetic", "factors", "squares-patterns",
    "money-percent", "measurement-speed", "ratio-word-problems", "algebra", "geometry",
]

# Auto-generated questions carry their family in the id: VAR_G5_vary_<family>_V<n>.
_AUTO_FAMILY = {
    "angles": "geometry", "perimeter_area": "geometry", "equation": "algebra",
    "simple_interest": "money-percent", "percentage": "money-percent", "bodmas": "arithmetic",
    "hcf_lcm": "factors", "fraction_arithmetic": "fractions",
}

# First match wins, tested against the sub-topic in lower case.
_RULES = [
    ("geometry", ["angle", "geometry", "perimeter", "area", "pythagor", "triangle"]),
    ("fractions", ["fraction"]),
    ("factors", ["hcf", "lcm", "divisib", "prime", "factor", "multiple"]),
    ("squares-patterns", ["square", "sequence", "series", "pattern"]),
    ("money-percent", ["money", "percent", "profit", "loss", "interest", "account"]),
    ("measurement-speed", ["measurement", "speed", "distance", "time", "rate problem"]),
    ("ratio-word-problems", ["ratio", "proportion", "unitary", "age problem", "word problem", "equal distribution", "combination", "venn", "sets"]),
    ("algebra", ["algebra", "equation", "substitution", "simultaneous"]),
    ("place-value", ["place value", "counting", "forming number", "number formation", "numbers ("]),
    ("arithmetic", ["bodmas", "addition", "subtraction", "multiplication", "division", "average", "cryptarithm", "product digit"]),
]


def topic_of(q):
    """The topic slug a Grade 5 question belongs to."""
    m = re.match(r"VAR_G5_vary_(.+)_V\d+$", q["id"])
    if m and m.group(1) in _AUTO_FAMILY:
        return _AUTO_FAMILY[m.group(1)]
    sub = q.get("subTopic", "").lower()
    for slug, words in _RULES:
        for w in words:
            if w in sub:
                return slug
    return "arithmetic"


def load_grade5():
    with io.open(SEED, encoding="utf-8") as f:
        return [q for q in json.load(f)["questions"] if q.get("topicId") == "grade5"]


_figures_cache = None


def effective_steps(q):
    """The step texts the app shows for a question: its own, or the computed ones from the figures file."""
    global _figures_cache
    own = q.get("stepByStep") or []
    if own:
        return [s.get("text", "") for s in own]
    if _figures_cache is None:
        with io.open(FIGURES, encoding="utf-8") as f:
            _figures_cache = json.load(f)
    computed = (_figures_cache.get(q["id"]) or {}).get("steps") or []
    return [s.get("text", "") for s in computed]


def option_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def source_strings(q):
    """What narration must cover, in the shape of a narration entry."""
    hints = list(q.get("hints") or [])
    while len(hints) < 3:
        hints.append("")
    return {
        "q": q.get("questionText", ""),
        "options": option_texts(q)[:4],
        "hints": hints[:3],
        "steps": effective_steps(q),
    }


# ── Numbers: the faithfulness check ──────────────────────────────────────────

_WORD_FRACTIONS = [
    (r"\bthree[ -](?:quarters|fourths)\b", " 3 4 "), (r"\btwo[ -]thirds\b", " 2 3 "),
    (r"\b(?:one|a)[ -]third\b", " 1 3 "), (r"\b(?:one|a)[ -](?:quarter|fourth)\b", " 1 4 "),
    (r"\b(?:one|a)[ -]half\b", " 1 2 "), (r"\bhalf\b", " 1 2 "), (r"\bhalves\b", " 1 2 "),
]
_UNICODE = {"½": " 1 2 ", "¼": " 1 4 ", "¾": " 3 4 ", "⅓": " 1 3 ", "⅔": " 2 3 ", "²": " squared ", "³": " cubed "}


def number_tokens(text):
    """The numbers in a piece of text, in order, written the same way whether it is print or speech.

    '2,345' and '2345' are the same token; '3/4', '¾' and 'three quarters' all give 3 then 4;
    'x^2', 'x²' and 'x squared' give nothing; '0.50' and '0.5' are the same.
    """
    s = text
    for k, v in _UNICODE.items():
        s = s.replace(k, v)
    s = re.sub(r"\^\s*\{?\s*2\s*\}?", " squared ", s)
    s = re.sub(r"\^\s*\{?\s*3\s*\}?", " cubed ", s)
    low = s.lower()
    for pat, rep in _WORD_FRACTIONS:
        low = re.sub(pat, rep, low)
    low = re.sub(r"(?<=\d),(?=\d)", "", low)
    out = []
    for m in re.findall(r"\d+(?:\.\d+)?", low):
        out.append(("%f" % float(m)).rstrip("0").rstrip(".") if "." in m else str(int(m)))
    return out


# ── A plain starting point for turning print into speech ─────────────────────

_UNITS = [
    (r"\bsq\.?\s*cm\b", "square centimetres"), (r"\bsq\.?\s*m\b", "square metres"), (r"\bsq\.?\s*km\b", "square kilometres"),
    (r"\bsq\.?\s*units?\b", "square units"), (r"\bcm\b", "centimetres"), (r"\bmm\b", "millimetres"), (r"\bkm\b", "kilometres"),
    (r"\bkg\b", "kilograms"), (r"\bmg\b", "milligrams"), (r"\bml\b", "millilitres"),
]


def speak(text):
    """A reasonable first pass. Topic scripts should improve on it, not rely on it."""
    s = text or ""
    for k, v in {"½": " one half ", "¼": " one quarter ", "¾": " three quarters ", "²": " squared ", "³": " cubed "}.items():
        s = s.replace(k, v)
    s = re.sub(r"(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d)\s*°", r"\1 degrees", s)
    s = re.sub(r"\bkm\s*/\s*h(?:r|our)?\b", "kilometres per hour", s)
    s = re.sub(r"\bm\s*/\s*s(?:ec)?\b", "metres per second", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    for pat, rep in _UNITS:
        s = re.sub(pat, rep, s)
    s = re.sub(r"(\d)\s*[-−–]\s*(?=\d)", r"\1 minus ", s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("=", " equals ")
    s = s.replace("−", " minus ").replace("√", " the square root of ").replace("≠", " is not equal to ")
    s = s.replace("<", " is less than ").replace(">", " is greater than ").replace("□", " blank ").replace("★", " star ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    return s
