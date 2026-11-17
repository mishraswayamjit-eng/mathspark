"""Expressions for the imported-01 algebra lessons: show them, put numbers in, work them out.

An expression is a list of terms (coefficient, letters): 3x − 5y + 7 is [(3, "x"), (-5, "y"), (7, "")].
Two letters together multiply: gh is (1, "gh").
"""
from imported_01_lib import N, W


def show(terms):
    """3x − 5y + 7, as printed."""
    out = ""
    for i, (c, v) in enumerate(terms):
        body = (str(abs(c)) if (abs(c) != 1 or not v) else "") + v
        if i == 0:
            out = ("−" if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out


def _factor(n):
    return "(−%d)" % -n if n < 0 else str(n)


def subst(terms, vals):
    """The expression with each letter swapped for its number: 3 × 3 − 5 × 2 + 7."""
    out = ""
    for i, (c, v) in enumerate(terms):
        factors = [vals[ch] for ch in v]
        if not v:
            body = str(abs(c))
        elif abs(c) == 1:
            body = " × ".join(_factor(f) for f in factors)
        else:
            body = " × ".join([str(abs(c))] + [_factor(f) for f in factors])
        if i == 0:
            if c < 0 and body.startswith("("):
                out = "−" + body
            else:
                out = ("−" if c < 0 else "") + body
        else:
            out += (" − " if c < 0 else " + ") + body
    return out


def parts(terms, vals):
    """The value of each term, in order."""
    out = []
    for c, v in terms:
        p = c
        for ch in v:
            p *= vals[ch]
        out.append(p)
    return out


def value(terms, vals):
    return sum(parts(terms, vals))


def signed(n):
    return "−%d" % -n if n < 0 else str(n)


def worked(terms, vals):
    """After the multiplying is done: 9 − 10 + 7."""
    ps = parts(terms, vals)
    out = signed(ps[0])
    for p in ps[1:]:
        out += (" − %d" % -p) if p < 0 else (" + %d" % p)
    return out


def option_line(id, letter, terms, vals, middle=False):
    """A checked line for one choice, with its name noted above: '3 × 0 + 2 × 2 = 4'  (A: 3x + 2y)."""
    text = subst(terms, vals)
    if middle and worked(terms, vals) != text:
        text += " = " + worked(terms, vals)
    text += " = " + signed(value(terms, vals))
    return [W(id, text), N(id, text, "%s: %s" % (letter, show(terms)), "above")]
