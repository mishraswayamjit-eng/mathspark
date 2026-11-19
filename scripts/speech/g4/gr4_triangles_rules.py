"""Rules for gr4_triangles: lengths, areas, side comparisons and angle ratios, on top of the angle rules.

say() prepares the notation that is special to triangles, then hands over to gr4_angles_rules.say.
"""
import re

import gr4_angles_rules as base

_NUM = r"(\d[\d,]*(?:\.\d+)?)"


def _unit(word):
    def sub(m):
        return "%s %s" % (m.group(1), word[:-1] if m.group(1) == "1" else word)
    return sub


def prepare(text):
    s = (text or "").strip()
    # A times sign typed as the letter x: "5 x 5 = 25".
    s = re.sub(r"(\d)\s+x\s+(?=\d)", r"\1 × ", s)
    # A length that describes a thing stays singular: "the 12 cm side", "a 10 cm straw".
    s = re.sub(r"\b([Aa]n?|[Tt]he) (\d+) cm (?=side\b|straw\b|stick\b|piece\b|square\b|triangle\b)", r"\1 \2 centimetre ", s)
    # Units. The raised 2 after a unit means "square".
    s = re.sub(_NUM + r"\s*cm\.\s*sq\b\.?", _unit("square centimetres"), s)      # "152 cm.sq." in one past paper
    s = re.sub(_NUM + r"\s*m\.\s*sq\b\.?", _unit("square metres"), s)
    s = re.sub(_NUM + r"\s*(?:sq\.?\s*cm|cm²)(?![a-z])", _unit("square centimetres"), s)
    s = re.sub(_NUM + r"\s*(?:sq\.?\s*m|m²)(?![a-z])", _unit("square metres"), s)
    s = re.sub(_NUM + r"\s*cm\b", _unit("centimetres"), s)
    s = re.sub(_NUM + r"\s*m\b(?!\.)", _unit("metres"), s)
    s = s.replace("cm²", "square centimetres")
    s = re.sub(r"\bsq\.?\s*cm\b", "square centimetres", s)
    s = re.sub(r"\bcm\b", "centimetres", s)
    # Labelled working in the generated families: "Third = 180° − 41° − 40° = 99°".
    s = re.sub(r"^(Third|Largest|Smallest) = ", lambda m: "The %s angle is " % m.group(1).lower(), s)
    s = re.sub(r"^One part = ", "One part is ", s)
    s = re.sub(r"^Sum of ratio parts = ", "The sum of the ratio parts is ", s)
    s = re.sub(r"^Area of (?:a )?triangle = ", "The area of a triangle is ", s)
    # Half of a product: "½ × base × height".
    s = re.sub(r"(?:½|\b1/2|\bhalf)\s*×\s*", "half of ", s)
    s = re.sub(r"(?<![\d ])½|(?<=[a-z] )½", "half", s)
    # A three-part ratio of angles: 3:1:1.
    s = re.sub(r"\b(\d+)\s*:\s*(\d+)\s*:\s*(\d+)\b", r"\1 is to \2 is to \3", s)
    # Named triangles and sides: triangle ABC, side AB.
    s = re.sub(r"\b([Tt]riangle|△)\s*([A-Z])([A-Z])([A-Z])\b", r"\1 \2 \3 \4", s)
    s = re.sub(r"\b([Ss]ides?|[Ll]ine) ([A-Z])([A-Z])\b", r"\1 \2 \3", s)
    # Comparisons in the triangle rule: 3 + 4 > 5.
    s = s.replace("≠", " is not equal to ").replace("≤", " is at most ").replace("≥", " is at least ")
    s = re.sub(r"\s*>\s*", " is greater than ", s)
    s = re.sub(r"\s*<\s*", " is less than ", s)
    return s


def say(text, sentence=True):
    return base.say(prepare(text), sentence)


def maths_line(latex):
    s = latex
    if "boxed" in s:
        return None
    s = s.replace("\\text{ cm}^2", " cm²").replace("\\text{ cm}", " cm")
    s = s.replace("^\\circ", "°").replace("\\div", "÷").replace("\\times", "×")
    s = re.sub(r"\\frac\{1\}\{2\}\s*×\s*", "half of ", s)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1 over \2", s)
    s = s.replace("\\text{ and }", ", and ")
    s = base.bracket_first(s)
    if re.search(r"[\\{}?()^]", s) or not re.search(r"[=+×÷<>-]", s):
        return None
    s = s.replace("-", "−")
    s = re.sub(r"(×\s*\d[\d.]*°?)\s*([+−])", r"\1, \2", s)
    s = re.sub(r"(, [+−]\s*\d[\d.]*°?)\s*=", r"\1, =", s)
    return say(s)
