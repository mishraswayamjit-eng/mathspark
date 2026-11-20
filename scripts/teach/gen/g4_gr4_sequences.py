"""Build data/teach/parts/g4-gr4_sequences.json.

    python -X utf8 scripts/teach/gen/g4_gr4_sequences.py

Generated families come from g4_gr4_sequences_rules.py; every other question has a
lesson written for it in g4_gr4_sequences_a.py, _b.py, ... (each has a dict L).
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_sequences_lib import build  # noqa: E402
from g4_gr4_sequences_rules import RULES  # noqa: E402

TOPIC = "gr4_sequences"


def main():
    authored = {}
    for suffix in "abcdefgh":
        name = "g4_gr4_sequences_%s" % suffix
        if os.path.exists(os.path.join(HERE, name + ".py")):
            authored.update(importlib.import_module(name).L)
    build(TOPIC, RULES, authored)


if __name__ == "__main__":
    main()
