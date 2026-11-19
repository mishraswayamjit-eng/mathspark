"""Write data/question-speech/parts-g4/gr4_ratio.json.

    python -X utf8 scripts/speech/g4/gr4_ratio.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_ratio.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_ratio.py --brief --show 0 30   # the same, only the lines that changed
    python -X utf8 scripts/speech/g4/gr4_ratio.py --ids         # also list the question ids

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_ratio_hand*.py, keyed by question id, or LINES keyed by the printed line);
  2. the ratio rules (gr4_ratio_rules.say), which add ratio notation to the fraction rules;
  3. the shared base converter (common.speak), as a last resort.

The narrating loop itself is the one in gr4_fractions.py; this script points it at this topic.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import common  # noqa: E402
import gr4_fractions as engine  # noqa: E402
import gr4_ratio_rules as rules  # noqa: E402

NODE = "gr4_ratio"

HAND = {}
LINES = {}
for name in ("gr4_ratio_hand1", "gr4_ratio_hand2", "gr4_ratio_hand3"):
    try:
        module = __import__(name)
    except ImportError:
        continue
    HAND.update(module.HAND)
    LINES.update(getattr(module, "LINES", {}))


def main():
    engine.NODE = NODE
    engine.OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")
    engine.HAND = HAND
    engine.LINES = LINES
    engine.rules = rules
    engine.main()


if __name__ == "__main__":
    main()
