"""Rules for gr4_ages: the equation rules (gr4_equations_rules), plus the notation of age problems.

    say(text)          the spoken line for a printed line
    from_latex(latex)  a step's maths line as print
"""
import re

import gr4_equations_rules as base

from_latex = base.from_latex


def say(text, stop=True):
    s = text or ""
    # "After 10 years: Arjun = 37, Riya = 38": a name and an age, not a sum.
    # "Difference = 47 − 9 = 38", "Sum = 37 + 38 = 75".
    s = re.sub(r"^\s*Difference = ", "The difference is ", s)
    s = re.sub(r"^\s*Sum = ", "The sum is ", s)
    s = re.sub(r": ([A-Z][a-z]+) = (\d+), ([A-Z][a-z]+) = (\d+)\s*$", r": \1 is \2, and \3 is \4", s)
    s = re.sub(r"\b([A-Z][a-z]+) = (?=\d)", r"\1 is ", s)
    # Ratios are printed with a space on each side of the colon ("2 : 5"); "by 6: 9 + 6" is not one.
    s = re.sub(r"(\d+) : (\d+)", r"\1 is to \2", s)
    # Short forms of "years".
    s = re.sub(r"(\d)\s*yrs?\b", r"\1 years", s)
    s = base.say(s, stop)
    s = s.replace("is to 1 years", "is to 1 year")
    return s
