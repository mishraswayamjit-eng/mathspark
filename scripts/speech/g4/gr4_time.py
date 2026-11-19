"""Write data/question-speech/parts-g4/gr4_time.json.

    python -X utf8 scripts/speech/g4/gr4_time.py                       # write the part file
    python -X utf8 scripts/speech/g4/gr4_time.py --show 0 30 --brief   # also print questions 0..29, print beside speech
    python -X utf8 scripts/speech/g4/gr4_time.py --show 0 30 --brief --spoken   # speech only

Uses the engine in gr4_puzzles.py (same author) with the rules in gr4_time_rules.py and the
hand-written lines in gr4_time_hand*.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gr4_puzzles  # noqa: E402
import gr4_time_rules  # noqa: E402

if __name__ == "__main__":
    gr4_puzzles.run("gr4_time", gr4_time_rules)
