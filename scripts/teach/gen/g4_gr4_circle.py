"""Build data/teach/parts/g4-gr4_circle.json: a lesson for every Grade 4 circle question.

    python -X utf8 scripts/teach/gen/g4_gr4_circle.py                 # build
    python -X utf8 scripts/teach/gen/g4_gr4_circle.py dump ids        # list the questions
    python -X utf8 scripts/teach/gen/g4_gr4_circle.py dump all 0 15   # print a slice in full
    python -X utf8 scripts/teach/gen/g4_gr4_circle.py dump missing    # questions with no lesson yet
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import g4_gr4_quads_lib as lib  # noqa: E402

TOPIC = "gr4_circle"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dump":
        lib.dump(TOPIC, sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "read":
        lib.read(TOPIC, sys.argv[2:])
    else:
        try:
            from g4_gr4_circle_rules import RULES
        except ImportError:
            RULES = []
        lib.build(TOPIC, RULES, "g4_gr4_circle_authored_")
