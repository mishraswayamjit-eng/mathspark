"""Scratch: print the imported arithmetic questions, printed text and narration together.

    python -X utf8 scripts/speech/topics/_scratch_arithmetic/dump_new.py 0 30          # by position among the imported ones
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/dump_new.py 0 30 --src    # printed text only
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/dump_new.py 0 999 --bad   # only lines the checker rejects
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/dump_new.py 0 999 --grep "regex"   # only lines whose print or speech matches
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/dump_new.py 0 999 --spoken  # narration only
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEECH = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, SPEECH)
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402
from validate import check_string  # noqa: E402

PRE = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
qs = sorted((q for q in load_grade5() if topic_of(q) == "arithmetic" and q["id"].startswith(PRE)), key=lambda q: q["id"])
with io.open(os.path.join(PARTS, "arithmetic.json"), encoding="utf-8") as f:
    part = json.load(f)
a, b = int(sys.argv[1]), int(sys.argv[2])
only_src = "--src" in sys.argv
only_bad = "--bad" in sys.argv
only_spoken = "--spoken" in sys.argv
pat = re.compile(sys.argv[sys.argv.index("--grep") + 1]) if "--grep" in sys.argv else None
spat = re.compile(sys.argv[sys.argv.index("--sgrep") + 1]) if "--sgrep" in sys.argv else None  # narration only
nbad = 0
for n, q in enumerate(qs[a:b]):
    e, src = part.get(q["id"]), source_strings(q)
    own = q.get("stepByStep") or []
    lines = []
    for key in ("q", "options", "hints", "steps"):
        items = [src[key]] if key == "q" else src[key]
        said = None if e is None else ([e[key]] if key == "q" else e[key])
        for i, t in enumerate(items):
            if not t:
                continue
            label = "q" if key == "q" else "%s%d" % (key[0], i)
            sp = said[i] if said is not None and i < len(said) else None
            also = None
            latex = ""
            if key == "steps" and i < len(own) and own[i].get("latex"):
                latex = own[i]["latex"]
                also = "%s %s" % (t, re.sub(r"\\[a-zA-Z]+", " ", latex))
            probs = check_string(sp, t, label, also) if sp is not None else []
            if only_bad and not probs:
                continue
            if pat and not (pat.search(t) or (sp and pat.search(sp))):
                continue
            if spat and not (sp and spat.search(sp)):
                continue
            if "--lean" in sys.argv and sp is not None:
                # Hide lines the rules barely touched: plain sentences, and bare amounts.
                if sp.rstrip(".") == t.strip().rstrip(".:") or re.fullmatch(r"(?:[Mm]inus |[Pp]lus )?[\d,.]+(?: [a-z]+)?", sp):
                    continue
                if label != "q" and not re.search(r"[^\w\s.,!?'’:;\"-]", t) and not re.search(r"\d\s*-\s*\d|[A-Z]{2}", t):
                    continue
            if not only_spoken:
                lines.append("  %-3s< %s%s" % (label, t.replace("\n", " // "), ("   [LATEX %s]" % latex) if latex else ""))
            if sp is not None and not only_src:
                lines.append("  %-3s: %s" % (label, sp))
            for p in probs:
                nbad += 1
                lines.append("     !! " + p)
    if lines:
        print("## %d %s | %s | ans %s" % (a + n, q["id"], q.get("subTopic", ""), q.get("correctAnswer")))
        print("\n".join(lines))
print("%d imported questions in all; %d problems shown" % (len(qs), nbad))
