"""Rules that turn printed fraction work into speech. Used by fractions.py.

    say(text)        the general converter for this topic's notation
    family(text)     a hand-written sentence pattern for the generated families, or None
"""
import re

_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
          ("1", "3"): "one third", ("2", "3"): "two thirds"}

_ABBREV = [
    (r"\bLCM\b", "L C M"), (r"\bHCF\b", "H C F"), (r"\bLCD\b", "L C D"), (r"\bGCD\b", "G C D"),
    (r"\bRHS\b", "the right-hand side"), (r"\bLHS\b", "the left-hand side"), (r"\bdenom\b", "denominator"),
    (r"(\d)\s*kg\b", r"\1 kilograms"), (r"(\d)\s*L\b", r"\1 litres"), (r"(\d)\s*min\b", r"\1 minutes"),
    (r"(\d)\s*yr\b", r"\1 years"), (r"(\d)\s*cm\b", r"\1 centimetres"), (r"(\d)\s*km\b", r"\1 kilometres"),
    (r"(\d)\s*ml\b", r"\1 millilitres"), (r"\b(\d+)\s*([ap])m\b", r"\1 \2 m"),
]

_OPS = [("×", " times "), ("÷", " divided by "), ("+", " plus "), ("−", " minus "), ("≈", " is about "),
        ("<", " is less than "), (">", " is greater than "), ("≠", " is not equal to ")]


def _of_word(m):
    word = _WORDS.get((m.group(1), m.group(2)))
    return (word if word else "%s over %s" % (m.group(1), m.group(2))) + " of "


def _equals(sentence):
    """First '=' is 'equals', later ones in the same sentence are ', which is'."""
    parts = sentence.split("=")
    if len(parts) == 1:
        return sentence
    out = parts[0]
    tail = re.search(r"\s*$", sentence).group(0)
    if not out.strip():
        out = "That equals " + parts[1].strip()
    else:
        out = out.rstrip() + " equals " + parts[1].strip()
    for p in parts[2:]:
        out = out.rstrip() + ", which is " + p.strip()
    return out + tail


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r":\s*,", ":", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"\.\s*\.", ".", s)
    s = re.sub(r"([.,?!:;])(?=[A-Za-z])", r"\1 ", s)
    if s:
        s = s[0].upper() + s[1:]
    return s


def say(text):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("-", "−") if re.fullmatch(r"-\d+(\.\d+)?", s) else s
    for k, v in {"½": " one half ", "¼": " one quarter ", "¾": " three quarters ", "²": " squared ", "³": " cubed "}.items():
        s = s.replace(k, v)
    s = s.replace("✓", " ").replace("✗", " ").replace("…", ".").replace("—", ", ")
    s = re.sub(r"(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    for pat, rep in _ABBREV:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\b(\d{1,2}):(\d\d)\b", r"\1 \2", s)                       # clock times
    s = re.sub(r"\bvs\.?\s", "and ", s)
    s = re.sub(r"\badd/subtract\b", "add or subtract", s)
    # clause by clause, so that '=' chains read naturally
    pieces = re.split(r"([.?!:;,]\s+)", s)
    s = "".join(p if i % 2 else _equals(p) for i, p in enumerate(pieces))
    # brackets over a number: (7+1)/9
    s = re.sub(r"\(([^()]+)\)\s*/\s*(\d+|[a-z]\b)", r"\1, all over \2", s)
    # mixed numbers, then fractions
    s = re.sub(r"\b(\d+) (\d+)\s*/\s*(\d+)", r"\1 and \2/\3", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)\s+of\s+", _of_word, s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)\s*(st|nd|rd|th)\b", r"\1/\2", s)        # '4/7 th full'
    s = re.sub(r"(\d+)\s*/\s*(\d+)\s*(?=[+−×÷])", r"\1 over \2, ", s)     # a pause after a fraction in a sum
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = re.sub(r"\b([A-Za-z])\s*/\s*(\d+)", lambda m: "%s over %s" % (m.group(1).upper() if m.group(1) == "a" else m.group(1), m.group(2)), s)
    s = re.sub(r"[?□]\s*/\s*(\d+)", r"what, over \1", s)
    s = re.sub(r"(\d)([a-z])\b", r"\1 \2", s)                              # 6x
    s = re.sub(r"(\d)\(", r"\1 times (", s)                               # 3(5)
    s = s.replace("□", " the missing number ").replace("✻", " the missing number ").replace("△", " triangle ")
    s = re.sub(r"\s*(?:→|⇒)\s*", ", so ", s)
    for k, v in _OPS:
        s = s.replace(k, v)
    s = re.sub(r"(\d)\s*-\s*(?=\d)", r"\1 minus ", s)
    s = re.sub(r"[()\[\]{}]", " ", s)
    s = s.replace("/", " or ")
    return tidy(s)
