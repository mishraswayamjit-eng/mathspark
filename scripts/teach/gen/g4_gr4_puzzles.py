"""Build data/teach/parts/g4-gr4_puzzles.json.

    python -X utf8 scripts/teach/gen/g4_gr4_puzzles.py

Every question in this topic has a lesson written for it, in g4_gr4_puzzles_a.py,
_b.py, ... (each has a dict L). Shared helpers are in g4_gr4_sequences_lib.py.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_sequences_lib import build  # noqa: E402

TOPIC = "gr4_puzzles"


def main():
    authored = {}
    for suffix in "abcdefgh":
        name = "g4_gr4_puzzles_%s" % suffix
        if os.path.exists(os.path.join(HERE, name + ".py")):
            authored.update(importlib.import_module(name).L)
    build(TOPIC, [], authored)


if __name__ == "__main__":
    main()
