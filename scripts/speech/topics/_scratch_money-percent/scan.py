"""Count notation in the new questions' source strings: caps tokens, odd characters, unit-like tokens."""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import load_grade5, source_strings, topic_of  # noqa: E402

with io.open(os.path.join(HERE, "baseline.json"), encoding="utf-8") as f:
    BASE = json.load(f)

qs = [q for q in load_grade5() if topic_of(q) == "money-percent" and q["id"] not in BASE]
caps, chars, units, pats = collections.Counter(), collections.Counter(), collections.Counter(), collections.defaultdict(list)
PATS = {
    "digit-paren": r"[\dA-Za-z]\(",
    "slash": r"\S*/\S*",
    "hyphen-digit": r"\d\s*[-–]\s*\d\S*",
    "dash-space": r"\s[-–]\s",
    "single-cap": r"(?<![A-Za-z'])[B-HJ-Z](?![A-Za-z'])",
    "rupee-nondigit": r"₹[^\d]\S*",
    "decimal": r"\d+\.\d+\S*",
    "paren-short": r"\([^()]{1,12}\)",
    "colon-digit": r"\d\s*:\s*\d",
    "x-times": r"\d\s*x\s*\d",
    "star": r"[*_#`~^|\\<>≤≥≠≈√°]",
    "lt": r"\S*\s*[<>]\s*\S*",
    "quote": r"['\"‘’“”]\S*",
    "num-letter": r"\d[A-Za-z]+\b",
    "abbrev-dot": r"\b(?:[A-Za-z]\.){1,3}",
}
for q in qs:
    src = source_strings(q)
    for t in [src["q"]] + src["options"] + src["hints"] + src["steps"]:
        for w in re.findall(r"\b[A-Z]{2,}\b", t):
            caps[w] += 1
        for c in t:
            if ord(c) > 126:
                chars[c] += 1
        for w in re.findall(r"\d\s*([a-zA-Z]{1,3})\b", t):
            units[w] += 1
        for name, pat in PATS.items():
            for m in re.finditer(pat, t):
                pats[name].append(t[max(0, m.start() - 25):m.end() + 25])
print("CAPS", caps.most_common())
print("CHARS", chars.most_common())
print("UNITS", units.most_common())
for name, found in pats.items():
    print("==", name, len(found))
    for s in sorted(set(found))[:int(sys.argv[1]) if len(sys.argv) > 1 else 25]:
        print("    ", s)
