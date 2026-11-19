"""Write data/question-speech/parts-g4/gr4_ages.json.

    python -X utf8 scripts/speech/g4/gr4_ages.py                # write the part file
    python -X utf8 scripts/speech/g4/gr4_ages.py --src 0 30     # print the source only (with maths lines)
    python -X utf8 scripts/speech/g4/gr4_ages.py --spoken 0 30  # print the spoken lines that differ from print
    python -X utf8 scripts/speech/g4/gr4_ages.py --show 0 30    # print beside speech
    python -X utf8 scripts/speech/g4/gr4_ages.py --ids          # list the question ids

Age problems use the same notation as equations, so this runs the equations builder
(gr4_equations.py: hand-written lines first, then the rules, then the base converter)
on the gr4_ages questions, with the hand-written lines of gr4_ages_hand*.py and the rules of
gr4_ages_rules.py (the equation rules plus names with ages, ratios and "yr").
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gr4_equations as builder  # noqa: E402
import gr4_ages_rules  # noqa: E402

NODE = "gr4_ages"

if __name__ == "__main__":
    builder.rules = gr4_ages_rules          # the equation rules, plus the notation of age problems
    builder.main(NODE)
