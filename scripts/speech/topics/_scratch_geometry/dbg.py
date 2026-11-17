"""Why was a maths line not read?  python -X utf8 .../dbg.py            lists every step whose maths line was dropped."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
from common import load_grade5, number_tokens, topic_of  # noqa: E402
from geometry_imported_rules import IMPORTED_PREFIXES, maths_line, say_imported  # noqa: E402


def sub(small, big):
    it = iter(big)
    return all(x in it for x in small)


n = 0
for q in sorted(load_grade5(), key=lambda q: q["id"]):
    if topic_of(q) != "geometry" or not q["id"].startswith(IMPORTED_PREFIXES):
        continue
    for i, s in enumerate(q.get("stepByStep") or []):
        text, latex = s.get("text", ""), s.get("latex", "")
        if not latex.strip():
            continue
        plain = maths_line(latex)
        if plain is None:
            why = "unreadable"
        else:
            extra, told = number_tokens(plain), number_tokens(text)
            if (sub(extra, told) if extra else "=" in text):
                continue
            both = "%s %s" % (say_imported(text), say_imported(plain))
            allowed = number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)))
            if len(both) > 700:
                why = "too long"
            elif number_tokens(both) != allowed:
                why = "numbers %s vs %s" % (number_tokens(both), allowed)
            else:
                continue
        n += 1
        print("%s s%d [%s]\n   T %s\n   L %s\n   P %s" % (q["id"], i, why, text, latex, plain))
print(n, "dropped")
