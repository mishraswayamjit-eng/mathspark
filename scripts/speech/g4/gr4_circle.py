"""Write data/question-speech/parts-g4/gr4_circle.json.

    python -X utf8 scripts/speech/g4/gr4_circle.py               # write the part file
    python -X utf8 scripts/speech/g4/gr4_circle.py --list        # also list every question
    python -X utf8 scripts/speech/g4/gr4_circle.py --show 0 30   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_circle.py --show 0 30 --brief
    python -X utf8 scripts/speech/g4/gr4_circle.py --uniq        # every different printed line once, with its speech
    python -X utf8 scripts/speech/g4/gr4_circle.py --odd         # lines worth a second look

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_circle_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the circle rules (gr4_circle_rules.say), for a step also its text followed by its maths line;
  3. the shared base converter (common.speak), as a last resort.

The narrating and printing machinery is the same as for quadrilaterals (gr4_quads.py); this script
points it at the circle topic, the circle rules and the circle hand-written lines.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import common  # noqa: E402
import gr4_quads as machinery  # noqa: E402
import gr4_circle_rules as rules  # noqa: E402

NODE = "gr4_circle"

machinery.NODE = NODE
machinery.OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")
machinery.rules = rules
machinery.HAND.clear()
machinery.LINES.clear()
for name in ("gr4_circle_hand1", "gr4_circle_hand2", "gr4_circle_hand3"):
    try:
        module = __import__(name)
    except ImportError:
        continue
    machinery.HAND.update(module.HAND)
    machinery.LINES.update(getattr(module, "LINES", {}))

if __name__ == "__main__":
    machinery.main()
