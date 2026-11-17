"""Rules for the imported Grade 5 questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

    from arithmetic_imported_rules import say_new, say_option_new

These questions are one-off word problems and textbook items. Their notation differs from the
generated families (the rupee sign, x for times, units glued to numbers, step labels), so they
get a pass of their own before the shared engine. The engine itself is not changed, which keeps
every older entry exactly as it was.
"""
import re

from arithmetic_engine import say, say_option


_N = r"\d+(?:,\d{2,3})*(?:\.\d+)?"
_BIG = r"lakhs?|crores?|thousands?|hundreds?|millions?|billions?"

# Unit abbreviations: (pattern after a number, singular, plural).
_UNIT = [
    ("kg", "kilogram", "kilograms"), ("km", "kilometre", "kilometres"), ("cm", "centimetre", "centimetres"),
    ("mm", "millimetre", "millimetres"), ("m[lL]", "millilitre", "millilitres"), ("mg", "milligram", "milligrams"),
    ("gm?s?", "gram", "grams"), ("m", "metre", "metres"), ("[lL]", "litre", "litres"),
    ("hrs?", "hour", "hours"), ("mins?", "minute", "minutes"), ("secs?", "second", "seconds"),
]
_UNIT_WORD = {"kg": "kilogram", "km": "kilometre", "cm": "centimetre", "mm": "millimetre", "ml": "millilitre",
              "mL": "millilitre", "mg": "milligram", "g": "gram", "m": "metre", "l": "litre", "L": "litre",
              "hr": "hour", "h": "hour", "min": "minute", "sec": "second", "s": "second"}


def _one(num):
    return num in ("1", "1.0")


def _unit_rules(s):
    # "per" forms first: ₹12/kg, 60 km/h, 5 m/s, ₹40 per kg.
    s = re.sub(r"\bkm\s*/\s*(?:hr?|hour)\b|\bkmph\b|\bkm\s*p\.?h\b", "kilometres per hour", s)
    s = re.sub(r"\bm\s*/\s*s(?:ec)?\b", "metres per second", s)
    s = re.sub(r"\s*/\s*(kg|km|cm|mm|m[lL]|mg|g|m|[lL]|hr|h|min|sec|s)\b", lambda m: " per " + _UNIT_WORD[m.group(1)], s)
    s = re.sub(r"\bper\s+(kg|km|cm|mm|m[lL]|mg|g|m|[lL]|hr|min|sec)\b", lambda m: "per " + _UNIT_WORD[m.group(1)], s)
    s = re.sub(r"(?<=\d)\s*/\s*(?=[A-Za-z]{3,}\b)", " per ", s)
    s = re.sub(r"\bsq\.?\s*(?=(?:cm|m|km|mm|units?|metres?|centimetres?|feet|ft)\b)", "square ", s)
    for abbr, one, many in _UNIT:
        s = re.sub(r"(%s)\s*-?(?:%s)\b(?!\s*[=×÷+]\s*\d)(?!')" % (_N, abbr),
                   lambda m, one=one, many=many: "%s %s" % (m.group(1), one if _one(m.group(1)) else many), s)
    s = re.sub(r"\b(kg|km|cm|mm|ml|mL|mg)\b", lambda m: _UNIT_WORD[m.group(1)] + "s", s)
    return s


_WORD = {"+": "plus", "−": "minus", "-": "minus", "×": "times", "÷": "divided by"}


def _money_brackets(s):
    """A bracketed sum of amounts, ₹2,500 − (₹1,200 + ₹350), keeps its brackets in words."""
    def rep(m):
        op = (" %s" % _WORD[m.group(1)]) if m.group(1) else ""
        return "%s, open bracket, %s, close bracket, " % (op, m.group(2))
    return re.sub(r"([+−×÷-])?\s*\(\s*((?:₹\s*)?%s(?:\s*[+−×÷-]\s*(?:₹\s*)?%s)+)\s*\)" % (_N, _N),
                  lambda m: rep(m) if "₹" in m.group(2) else m.group(0), s)


def _money(s):
    s = s.replace("Rs.", "₹").replace("Rs ", "₹ ")
    s = _money_brackets(s)
    s = re.sub(r"₹\s*(%s)\s*(%s)\b" % (_N, _BIG), lambda m: "%s %s rupees" % (m.group(1), m.group(2)), s)
    s = re.sub(r"₹\s*(%s)\s*/\s*-" % _N, r"₹\1", s)
    s = re.sub(r"₹\s*(%s)" % _N, lambda m: "%s %s" % (m.group(1), "rupee" if _one(m.group(1)) else "rupees"), s)
    s = re.sub(r"\(\s*in\s*₹\s*\)", ", in rupees,", s)
    s = s.replace("₹", " rupees ")
    return s


def _pre(text):
    s = text or ""
    s = s.replace(" ", " ").replace("“", '"').replace("”", '"').replace("‘", "'")
    s = s.replace(" ", " ")
    # Pictures (stopwatch, stars, faces) are not read.
    s = "".join(c for c in s if not (0x2300 <= ord(c) <= 0x23FF or 0x2600 <= ord(c) <= 0x2712 or 0x2719 <= ord(c) <= 0x27BF or ord(c) >= 0x1F000 or ord(c) == 0xFE0F))
    # "5 Kg. packets", "80 Kg. Then": one spelling, and a full stop only where a sentence ends.
    s = re.sub(r"\b[Kk]gs?\b(\.?)(?=(\s+[A-Z]|\s*$)?)", lambda m: "kg" + (m.group(1) if m.group(2) is not None else ""), s)
    # Emphasis marks: **20 years**, *faster*.
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<![\w*])\*([A-Za-z][^*]*?)\*(?![\w*])", r"\1", s)
    # A star between spaced numbers is a times sign that lost its shape; glued into a number it is a missing digit.
    s = re.sub(r"(?<=\d) \* (?=\d)", " × ", s)
    s = re.sub(r"(?<=\d)[*_](?=\d)", " star ", s)
    s = re.sub(r"\bthe \* mark\b|\bthe mark \*", "the star", s)
    s = re.sub(r"\*", " star ", s)
    # Line breaks and bullets are sentence breaks.
    s = re.sub(r"(?<=[.!?:;,])\s*\n+\s*", " ", s)
    s = re.sub(r"\s*\n+\s*", ". ", s)
    s = re.sub(r"(?<=[.!?:;,])\s*[•●▪]\s*", " ", s)
    s = re.sub(r"\s*[•●▪]\s*", ". ", s)
    s = s.replace(" & ", " and ")
    # Names a voice would mangle once the engine lowers capitals.
    s = re.sub(r"\bMG Road\b", "M G Road", s)
    s = re.sub(r"\bTVs\b", "T V sets", s)
    s = re.sub(r"\bTV\b", "T V", s)
    s = re.sub(r"\bT20\b", "T 20", s)
    s = re.sub(r"\bNumber(\d)\b", r"Number \1", s)
    s = re.sub(r"(?<=\d)\s*(?:AM|a\.m\.?)(?![A-Za-z])", " a m", s)
    s = re.sub(r"(?<=\d)\s*(?:PM|p\.m\.?)(?![A-Za-z])", " p m", s)
    s = re.sub(r"\b(\d{1,2}):(\d{2}) (?=[ap] m\b)", r"\1 \2 ", s)
    s = re.sub(r"(?<=\d)\s*°\s*C\b", " degrees Celsius", s)
    s = re.sub(r"(?<=\d)\s*°", " degrees", s)
    s = re.sub(r"°\s*C\b", "degrees Celsius", s)
    # |−5| is the absolute value of −5.
    s = re.sub(r"\|([^|]{1,30})\|", lambda m: "the absolute value of " + (m.group(1) if re.fullmatch(r"\s*[−-]?\s*[\dA-Za-z.]+\s*", m.group(1)) else "(" + m.group(1) + ")"), s)
    s = re.sub(r"(the absolute value of [−-]?\s*\d[\d.,]*)\s*=\s*(?=[−-]?\d)", r"\1, which is ", s)
    # A signed number in brackets, inside a sum: (−8) + (−11), 70 + (−45), 10 − (−₹25).
    def signed(m):
        before, after = s[:m.start()].rstrip(), s[m.end():].lstrip()
        if not (before[-1:] in tuple("+−-×÷=") and before[-1:] or after[:1] in tuple("+−×÷=") and after[:1]):
            return m.group(0)
        return " %s %s%s " % ("positive" if m.group(1) == "+" else "negative", m.group(2), m.group(3))
    s = re.sub(r"\(\s*([+−-])\s*(₹?\s*)(%s)\s*\)" % _N, signed, s)
    # A bracket that held one of those, (−2 + (−5)) ÷ 2, keeps its brackets in words.
    s = re.sub(r"([+−×÷-])?\s*\(([^()]*\b(?:negative|positive) [^()]*)\)",
               lambda m: "%s, open bracket, %s, close bracket, " % ((" " + _WORD[m.group(1)]) if m.group(1) else "", m.group(2).strip())
               if re.search(r"[+−×÷]", m.group(2)) else m.group(0), s)
    # A short remark in brackets that the engine would take for maths: (up 5), (down 12).
    s = re.sub(r"\(([A-Za-z]{2,}\s+\d[\d.,]*(?:\s+[a-z]+)?)\)", r", \1,", s)
    # "positive = profit", "Sandstorm (left) = negative": an equals sign between words is "means".
    def means(m):
        left = re.split(r"[,.;:(]", s[:m.start()])[-1]
        right = re.split(r"[,.;:)]", s[m.end():])[0]
        if re.search(r"[\d+−×÷=]", left + right) or not left.strip() or not right.strip() or len(right.split()) > 3 or len(left.split()) > 3:
            return m.group(0)
        if left.strip().startswith(("Let", "let")) or not re.match(r"\s*[a-z]{3,}", right):
            return m.group(0)
        return " means "
    s = re.sub(r"(?<=[a-z)])\s*=\s*(?=[a-z])", means, s)
    # "12.5 + 8.75 = ? litres" asks how many litres.
    s = re.sub(r"=\s*\?\s+(litres|kilograms|metres|rupees|cups|runs|kg|km|ml|mL|L|m)\b\.?", r"equals how many \1?", s)
    # A list of the answer choices: "A) 615 m, B) 705 m".
    s = re.sub(r"(?:^|(?<=[\s,:;]))([A-D])\)\s+(?=[\dA-Z₹])", r"\1, ", s)
    # A sum with its answer and then a new remark, with the full stop missing: "= 2268 Perfect match!".
    s = re.sub(r"(=\s*[\d,]*\d(?:\.\d+)?)\s+(?=[A-Z][a-z])", r"\1. ", s)
    # A missing number: 65,269 + ? = 99,999.
    s = re.sub(r"([+−×÷])\s*\?\s*(?==)", r"\1 what number ", s)
    # An arrow from one number to the next.
    s = re.sub(r"(?<=\d)\s*→\s*(?=[−-]?\d)", ", which gives ", s)
    s = re.sub(r"\bi\.e\.,?\s*", "that is, ", s)
    s = re.sub(r"\be\.g\.,?\s*", "for example, ", s)
    # A decimal that goes on: "46.533... See how".
    s = re.sub(r"(?<=\d)\s*(?:…|\.\.\.)\s+(?=[A-Z])", " and so on. ", s)
    # A thought that trails off into the next: "3 − 6… we can't do this directly".
    s = re.sub(r"\s*(?:…|\.\.\.)\s*(?=[a-z])", ", ", s)
    # A range: Rounds 1–4.
    s = re.sub(r"(?<=\d)–(?=\d)", " to ", s)
    # A mixed number: 23 1/2.
    s = re.sub(r"\b(\d+) (\d+/\d+)\b", r"\1 and \2", s)
    for abbr, word in (("mts", "m"), ("yrs", "years"), ("nos", "numbers")):
        s = re.sub(r"\b%s\.(?=\s+[A-Z]|\s*$)" % abbr, word + ".", s)
        s = re.sub(r"\b%s\b\.?" % abbr, word, s)
    s = _money(s)
    s = _unit_rules(s)
    s = _plain_brackets(s)
    return s


def _plain_brackets(s):
    """Brackets that do not change the sum are not read: (3.5 × 4.2) + (2.5 × 5.6), 70 + (−45)."""
    def rep(m):
        before, after = s[:m.start()].rstrip(), s[m.end():].lstrip()
        if before[-1:] in tuple("×÷)]}") or before[-1:].isdigit():
            return m.group(0)
        if after[:1] in tuple("×÷([{") or after[:1].isdigit():
            return m.group(0)
        if not (before[-1:] in tuple("+−-=") or after[:1] in tuple("+−-=")):
            return m.group(0)
        return m.group(1)
    s = re.sub(r"\(\s*(%s(?:\s*[×÷]\s*%s)+)\s*\)" % (_N, _N), rep, s)

    # A bracketed sum that only an equals sign follows: "he sold (24 + 16) = 40 laddoos".
    def rep2(m):
        before = s[:m.start()].rstrip()
        if before[-1:] in tuple("×÷+−-)]}") or before[-1:].isdigit():
            return m.group(0)
        return m.group(1) + m.group(2)
    s = re.sub(r"\(\s*(%s(?:\s*[+−-]\s*%s)+)\s*\)(\s*=)" % (_N, _N), rep2, s)

    # A sum named in passing, with no operation on either side: "the two sums (22 + 47) and (11 + 22)".
    def rep3(m):
        before, after = s[:m.start()].rstrip(), s[m.end():].lstrip()
        if before[-1:] in tuple("×÷+−-=") or before[-1:].isdigit() or before[-1:] in tuple(")]}"):
            return m.group(0)
        if after[:1] in tuple("×÷+−-=([{") or after[:1].isdigit():
            return m.group(0)
        return ", %s," % m.group(1)
    return re.sub(r"\(\s*(%s(?:\s*[+−×÷-]\s*%s)+)\s*\)" % (_N, _N), rep3, s)


def _post(s):
    # A negative number in brackets: "plus, open bracket, minus 45, close bracket" is "plus minus 45".
    s = re.sub(r",? open bracket, minus (\d[\d,.]*), close bracket(,?)", r" negative \1\2", s)
    s = re.sub(r",? open bracket, plus (\d[\d,.]*), close bracket(,?)", r" positive \1\2", s)
    s = re.sub(r"^ ?(negative|positive) ", lambda m: m.group(1).capitalize() + " ", s)
    s = re.sub(r"\b(\d+) rupees (coins?|notes?)\b", r"\1 rupee \2", s)
    s = re.sub(r"\b(the|a|an) (\d[\d,.]*) rupees (loss|bonus|gift|target|fee|discount|penalty|tip|profit)\b", r"\1 \2 rupee \3", s)
    s = s.replace(", and, ", ", and ")
    s = re.sub(r"\b(\d[\d,.]*) (millilitre|litre|gram|kilogram|metre)s (cartons?|packets?|bottles?|bags?|cups?|glasses|glass|packs?|boxes|box|jars?|tins?|cans?|pouch|pouches|jugs?|containers?|pieces?|strips?|rolls?|dash|race)\b", r"\1 \2 \3", s)
    # Punctuation left doubled by a bracket or a quotation.
    s = re.sub(r"([!?])[.:]", r"\1", s)
    s = re.sub(r", that equals ", ", which equals ", s)
    s = re.sub(r"close bracket, which equals ", "close bracket, equals ", s)
    s = re.sub(r"([.!?])([\"'])\.", r"\1\2", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def say_new(text, stop=True):
    return _post(say(_pre(text), stop=stop))


def latex_plain(latex):
    """A step's maths line as printed text, or None if it holds something these rules do not know."""
    t = (latex or "").replace("{,}", ",")
    t = re.sub(r"\\(?:text|mathrm|mathbf|textbf|boxed|underline)\s*\{([^{}]*)\}", r" \1 ", t)
    def frac(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        wrap = lambda x: x if re.fullmatch(r"[\d.,]+|[A-Za-z]", x) else "(%s)" % x  # noqa: E731
        return "%s ÷ %s" % (wrap(a), wrap(b))
    t = re.sub(r"\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", frac, t)
    for a, b in (("\\times", "×"), ("\\div", "÷"), ("\\cdot", "×"), ("\\Rightarrow", " → "), ("\\rightarrow", " → "),
                 ("\\implies", " → "), ("\\neq", "≠"), ("\\approx", "≈"), ("\\quad", " ; "), ("\\qquad", " ; "),
                 ("\\left", ""), ("\\right", ""), ("\\%", "%"), ("\\,", " "), ("\\;", " "), ("\\!", ""), ("\\ ", " "),
                 ("\\\\", " ; "), ("\\{", "{"), ("\\}", "}"), ("\\$", ""), ("\\checkmark", "✓"), ("\\ldots", "…"), ("\\dots", "…")):
        t = t.replace(a, b)
    t = re.sub(r"\^\s*\{?\\circ\}?\s*", "°", t)
    if re.search(r"[\\{}^_&]", t):
        return None
    t = re.sub(r"(?<![A-Za-z])-(?=\s*[\d(])", "−", t)
    t = re.sub(r"\s*;\s*", ". ", t)
    return re.sub(r"\s+", " ", t).strip()


def say_step_new(text, latex):
    """A step. Where its words lead into the maths line ("Add the two totals:"), the maths is read too."""
    spoken = say_new(text)
    lead = (text or "").rstrip()
    if not latex or not lead.endswith(":"):
        return spoken
    plain = latex_plain(latex)
    if plain is None:
        return spoken
    maths = say_new(plain)
    if not maths:
        return spoken
    if not plain[0].isalpha():
        maths = maths[0].lower() + maths[1:]
    head = spoken.rstrip(".")
    if head.endswith(("!", "?")):
        return "%s %s" % (head, maths[0].upper() + maths[1:])
    return "%s: %s" % (head, maths)


def say_option_new(text):
    t = (text or "").strip()
    s = _post(say_option(_pre(t)))
    # A choice that is a single phrase does not end with a full stop.
    if s.endswith(".") and not re.search(r"[.!?] ", s):
        s = s[:-1]
    return s
