"""Narration rules for the imported place-value questions (AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_ ids).

These are one-off word problems and textbook items. The rules here turn their recurring
notation into speech; strings the rules cannot make sound right are written by hand in
place_value_imported_*.py and replace the rule's output.
"""
import re

PLACES = r"(?:ones|units|tens|hundreds|thousands|ten-thousands|lakhs|ten-lakhs|hundred-thousands)"


def _lines(text):
    """Bullets and line breaks become sentences."""
    out = ""
    for ln in text.split("\n"):
        ln = re.sub(r"^•\s*", "", ln.strip())
        if not ln:
            continue
        if out and out.rstrip("\"'”’")[-1:] not in ".!?:;,":
            out += "."
        out += (" " if out else "") + ln
    return out


def _equals(s):
    """'=' as speech: 'is' after a name, 'equals' after a number, ', which is' for the next one in the same clause."""
    out, last, start = [], None, 0
    for i, ch in enumerate(s):
        nxt = s[i + 1:i + 2]
        if ch == "=":
            clause = s[start:i].rstrip()
            prev = clause[-1:]
            since = s[last + 1:i] if last is not None else clause
            if last is not None and not re.search(r"[A-Za-z]", since):
                # a chain: 5 × 100 = 500 = ...
                out.append(", which is ")
            elif _VERB.search(since):
                # "its place value is 5 × 100 = 500": the clause already has its verb
                out.append(", which is ")
            elif prev.isalpha() or prev in ")'’" or _NAMED.search(clause):
                out.append(" is ")
            else:
                out.append(" equals ")
            last = i
            continue
        if ch in ".!?;:," and nxt in ("", " "):
            last, start = None, i + 1
        out.append(ch)
    return "".join(out)


_VERB = re.compile(r"\b(?:is|are|be|get|gives)\b")
_NAMED = re.compile(r"\b(?:value|digit)\b[^=]*\bof (?:the digit )?\d[\d,]*$")


def say(text):
    """Spoken form of one printed string of an imported question."""
    s = _lines(text or "")
    if not s:
        return ""
    s = s.replace("**", "").replace("*", "").replace("{", "").replace("}", "")
    # money
    s = s.replace("(in ₹)", "in rupees")
    s = re.sub(r"₹\s*([\d,]*\d)", r"\1 rupees", s)
    s = s.replace("₹", "rupees")
    # option letters, shouted words
    s = re.sub(r"\b([A-D])\) ", r"\1, ", s)
    s = re.sub(r"\bID\b", "I D", s)
    s = re.sub(r"\b[A-Z]{3,}(?:'[A-Z])?\b", lambda m: m.group(0).lower(), s)
    s = s.replace("etc.)", "and so on)")
    s = s.replace(" vs ", " versus ").replace("i.e.,", "that is,").replace("&", "and")
    # trailing-off dots
    s = s.replace("…", "...")
    s = re.sub(r"\bis\.\.\.\?", "is what?", s)
    s = re.sub(r":\s*\.\.\.(?=\d)", ": ", s)
    s = re.sub(r",\s*\.\.\.,\s*", ", and so on, up to ", s)
    s = re.sub(r"(\d)\.\.\.(?=\s+[A-Z])", r"\1, and so on.", s)
    s = re.sub(r"(\d)\.\.\.", r"\1, and so on", s)
    s = re.sub(r"\.\.\.\)", ", and so on)", s)
    s = re.sub(r"\.\.\.\s*(?=[A-Z])", ". ", s)
    s = re.sub(r"\.\.\.\s*", ", ", s)
    # dashes
    s = re.sub(r"(\d)–(\d)", r"\1 to \2", s)
    s = re.sub(r"\s*—\s*(what\b|which digit)", lambda m: ". " + m.group(1).capitalize(), s)
    s = re.sub(r"\s*—\s*", ", ", s)
    s = re.sub(r"=\s*\?", " equals what?", s)
    # "5 (hundreds)" and "5 → Hundreds" name the place of a digit
    s = re.sub(r"(\d) \((%s)\)" % PLACES, r"\1 in the \2 place", s)
    s = re.sub(r"(\d) → (%s)\b(?: place)?(?![- ]*(?:\(|place))" % PLACES,
               lambda m: "%s is in the %s place" % (m.group(1), m.group(2).lower()), s, flags=re.I)
    # other brackets are asides
    s = re.sub(r"\(=\s*", "(which is ", s)
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = s.replace("→", ", so ")
    s = _equals(s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("−", " minus ").replace("+", " plus ")
    s = s.replace(">", " is greater than ").replace("<", " is less than ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",+", ",", s)
    s = re.sub(r",([.!?:;])", r"\1", s)
    s = re.sub(r"([:;!?]),", r"\1", s)
    s = re.sub(r"([!?])\.", r"\1", s)
    s = re.sub(r"(?<=[a-z])/(?=[a-z])", " or ", s)
    return s


def sentence(text):
    """A question, hint or step: as `say`, closed with a full stop where the print has none."""
    s = say(text)
    if s and s[-1].isalnum():
        s += "."
    return s


def option(text):
    s = (text or "").strip()
    m = re.match(r"^₹\s*([\d,]+)$", s)
    if m:
        return m.group(1) + " rupees"
    return say(s)


_REJECT = ("{,}", "\\underset", "\\underbrace", "\\lfloor", "\\_", "\\ldots", "\\{", "₹", "\\neq", ">", "<", "\\sqrt")
_ITEM = re.compile(r"^(\d) (?:→ |is in the |\()?(%s)(?: place)?\)?$" % PLACES)


def maths(latex):
    """The maths line under a step, as speech; None if it is not a simple line.

    Lines that print a number with a grouping comma (50{,}000) are left out: the checker
    reads that as two numbers, so it cannot be said.
    """
    t = latex or ""
    if not re.search(r"\d", t) or any(x in t for x in _REJECT):
        return None
    t = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", t)
    t = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", t)

    def frac(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        return "%s ÷ %s" % (a, b) if a.isdigit() and b.isdigit() else "\\bad"

    t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, t)
    t = t.replace("\\times", "×").replace("\\div", "÷")
    t = re.sub(r"\\(?:rightarrow|Rightarrow|implies)", "→", t)
    t = re.sub(r"\\(?:quad|;|,| )", " ", t)
    t = re.sub(r"\(i\.e\.,\s*(\d+)\)", r"= \1", t)
    t = re.sub(r"(?<=[\d)]) - (?=[\d(])", " − ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+,", ",", t)
    if "\\" in t:
        return None
    # a list of digits with their places
    m = re.match(r"^(?:(\d[\d,]+) → )?(.+)$", t)
    items = [_ITEM.match(x.strip()) for x in m.group(2).split(", ")]
    if len(items) >= 2 and all(items):
        said = ["%s is in the %s place" % (i.group(1), i.group(2)) for i in items]
        body = ", ".join(said[:-1]) + ", and " + said[-1] + "."
        return ("In %s: %s" % (m.group(1), body)) if m.group(1) else body
    # the digits of a number set side by side
    m = re.match(r"^(\d(?: \d)+)(?: = (\d+))?$", t)
    if m:
        digits = ", ".join(m.group(1).split(" "))
        return digits + (". That makes %s." % m.group(2) if m.group(2) else ".")
    if not re.match(r"^[A-Za-z0-9 ,.=×÷−+():→-]+$", t):
        return None
    s = say(t)
    if s[-1] not in ".!?":
        s += "."
    return s[0].upper() + s[1:]


def step(text, latex):
    """A step: its text, followed by its maths line where the text leads up to it."""
    s = say(text)
    m = maths(latex)
    raw = (text or "").strip()
    lat = latex or ""
    if m:
        is_list = " is in the " in m and " place" in m and "=" not in lat
        computes = any(x in lat for x in ("\\times", "\\div", "\\frac", "+", " - "))
        if raw.endswith(":") or not re.search(r"\d", raw) or is_list or (computes and "=" not in raw):
            return (s + ":" if s[-1].isalnum() else s) + " " + m
    return sentence(text)
