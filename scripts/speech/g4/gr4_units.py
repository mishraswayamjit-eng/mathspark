"""Write data/question-speech/parts-g4/gr4_units.json.

    python -X utf8 scripts/speech/g4/gr4_units.py                      # write the part file
    python -X utf8 scripts/speech/g4/gr4_units.py --show 0 30          # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_units.py --show 0 30 --diff   # only lines whose speech differs from print

Each line is narrated by the first of these that gives a line passing the checker:
  1. a hand-written line (gr4_units_hand*.py: HAND keyed by question id, LINES keyed by the printed line);
  2. the rules (gr4_units_rules: family, then say), with a step's maths line spoken after its text
     when the maths line adds working that the text does not say;
  3. the shared base converter (common.speak), as a last resort.

The builder itself (narrate, show, main) is the one in gr4_decimals.py, written by the same writer;
this script points it at gr4_units with this topic's rules and hand lines.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))

import gr4_decimals as builder  # noqa: E402
import gr4_units_rules as rules  # noqa: E402

if __name__ == "__main__":
    builder.configure("gr4_units", rules, ("gr4_units_hand1", "gr4_units_hand2", "gr4_units_hand3"))
    builder.main()
